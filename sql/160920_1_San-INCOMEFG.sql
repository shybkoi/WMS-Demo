

SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_CARGO_CHK (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable wid type of column GWARES.waresid;
declare variable wname type of column GWARES.name;
begin
     select first(1) w.waresid
      from (select ic.waresid as waresid, ic.amount as q
              from imp_cargo ic
             where ic.document = :docid
             union all
            select cg.waresid as waresid, -cg.amount as q
              from cargo cg
             where cg.document = :docid) w
      group by w.waresid
      having abs(sum(w.q)) > 0.00001
       into :wid;

     if (:wid is NOT NULL) then
     begin
        select g.name
          from gwares g
         where g.waresid = :wid
          into :wname;

        exception exc_wh_reserve :wname || ': количества в файле не совпадает с количеством по документу!';
     end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDSALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I')
AS
begin
    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');
    execute procedure WH_IMP_FUNDSALE_RESERVE_CANC(:docid);

    if (:ACTIONCODE = 'D') then
    begin
        delete from imp_cargo ic
         where ic.document = :docid;
    end
    else
    begin
        execute procedure WH_IMP_FUNDSALE_RESERVE_DO(:docid);
    end
        
    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^



ALTER TABLE WH_OBJ_INFO
ADD INCOMEPRODLINEID R_ID;



ALTER TABLE WH_OBJ_INFO
ADD CONSTRAINT FK_WH_OBJ_INFO_PRID
FOREIGN KEY (INCOMEPRODLINEID)
REFERENCES FG_PRODLINES(ID_PRODLINE)
ON DELETE SET NULL
ON UPDATE SET NULL;



ALTER TABLE WH_OBJ_INFO DROP CONSTRAINT FK_WH_OBJ_INFO_PRID;



ALTER TABLE WH_OBJ_INFO ALTER INCOMEPRODLINEID TO FIRSTINCOMEPRODLINEID;



ALTER TABLE WH_OBJ_INFO
ADD CONSTRAINT FK_WH_OBJ_INFO_FIPLID
FOREIGN KEY (FIRSTINCOMEPRODLINEID)
REFERENCES FG_PRODLINES(ID_PRODLINE)
ON DELETE SET NULL
ON UPDATE SET NULL;



SET TERM ^ ;

create or alter procedure WH_FIRSTINCOMEFG_PRODLINES(
    taskid type of column wm_task.taskid
)
returns (
    ID_PRODLINE type of column fg_prodlines.id_prodline,
    NUMBER type of column fg_prodlines.number,
    NAME type of column fg_prodlines.name,
    CHGDATE type of column fg_prodlines.chgdate,
    PRODUCERS type of column fg_prodlines.listproducers)
AS
declare variable whid type of column OBJECT.objid;
begin
    select d.toobj
      from wm_task t
           left join document d on d.docid = t.docid
     where t.taskid = :taskid
      into :whid;

    select oi.firstincomeprodlineid
      from wh_obj_info oi
     where oi.objid = :whid
      into :id_prodline;


    if (:id_prodline is NOT NULL) then
    begin
      for
        select pl.id_prodline, pl.number, pl.name, coalesce(pl.chgdate,'0'), pl.listproducers
          from fg_prodlines pl
         where pl.id_prodline = :id_prodline
           and pl.generatorname is not null
          into :id_prodline, :number, :name, :chgdate, :producers
      do
        suspend;

    end
    else
    begin
        for
            select pl.id_prodline, pl.number, pl.name, pl.chgdate, pl.producers
              from fg_get_prodlines pl
              into :id_prodline, :number, :name, :chgdate, :producers
        do
            suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_INCOME_STATUSCHG (
    DOCID type of column DOCUMENT.DOCID,
    OLDSTAT type of column R_STATUS.CODE,
    NEWSTAT type of column R_STATUS.CODE)
AS
declare variable TASKID type of column WM_TASK.taskid;
declare variable TASKTYPEID type of column WM_TASKTYPE.tasktypeid;
declare variable TASKMETHODID type of column wm_taskmethod.methodid;
declare variable TTINITST type of column R_STATUS.code;
declare variable DOCDATE type of column DOCUMENT.docdate;
declare variable FROMOBJ type of column OBJECT.objid;
declare variable SITEID type of column SITE.siteid;
declare variable OBJID type of column OBJECT.objid;
declare variable oifromobjincome type of column OBJECT.objid;
declare variable oidatestart type of column wh_obj_info.datestart;
declare variable dtid type of column DOCTYPE.doctid;
begin
    if (:newstat = 'c') then
    begin
        SELECT ttid,ttinitst
          FROM k_tasktype_by_code('INCOMEFG','1')
          into :tasktypeid,:ttinitst;

        select d.fromobj, d.toobj, d.realdocdate, d.doctype
          from document d
         where d.docid = :docid
          into :fromobj, :objid, :docdate, :dtid;

        select wh.datestart, coalesce(wh.fromobjincome,0)
          from wh_obj_info wh
         where wh.objid = :objid
          into :oidatestart, :oifromobjincome;

        if (:oidatestart >= :docdate and :oifromobjincome = coalesce(:fromobj,0)) then
        begin
            if (exists(select *
                         from document d
                        where d.toobj = :objid
                          and d.docdate <= :oidatestart
                          and d.status = 'c'
                          and d.doctype = :dtid
                          and coalesce(d.fromobj,0) = :oifromobjincome
                          and d.docid <> :docid)) then
                    exception exc_wh_wrongdocstat 'Уже есть документ первого прихода!';

            select tm.methodid
              from wm_taskmethod tm
             where tm.tasktypeid = :tasktypeid
               and tm.algorithm = 'F'
              into :taskmethodid;

            if (:taskmethodid is NULL) then
                exception exc_k_wrongtasktype 'Не найден метод с кодом F у типа задания приемка от поставщика!';

            select first(1) t.taskid
              from wm_task t
             where t.docid = :docid
               and t.tasktypeid = :tasktypeid
              into :taskid;

            if (:taskid is NULL) then
            begin
                siteid = NULL;
                select first(1) s.siteid
                  from sitespecies sp
                       left join site s on s.sitespeciesid = sp.sitespeciesid
                 where sp.code = 'E'
                  into :siteid;

                INSERT INTO wm_task(tasktypeid,status,docid,wm_sessionid,taskmethodid,siteid)
                VALUES(:tasktypeid,:ttinitst,:docid,null,:taskmethodid,:siteid)
                returning taskid
                into :taskid;
            end
            else
            begin
                update wm_task t
                   set t.taskmethodid = :taskmethodid,
                       t.wm_sessionid = NULL,
                       t.status = :ttinitst
                  where t.taskid = :taskid;
            end
        end
    end
    else if (:newstat = 'w') then
    begin
         taskid = NULL;
         for
            select t.taskid
              from wm_task t
                   left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                   left join wm_taskmethod tm on tm.methodid = t.taskmethodid
             where t.docid = :docid
               and tt.code = 'INCOMEFG'
               and tm.algorithm = 'F'
              into :taskid
         do
            update wm_task t
               set t.status = '2',t.endtime = current_timestamp
             where t.taskid = :taskid and t.status <> '2';

        execute procedure wh_core_setdocbytasklot(:docid);
/*        execute procedure RBS_Q_CREATETASKEXPORT('K_UV_INCOMEFG_STATUSCHG: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
         returning_values :docid;*/

    end
end^

SET TERM ; ^

