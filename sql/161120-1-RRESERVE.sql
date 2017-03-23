

CREATE EXCEPTION EXC_WH_WRONGDOCTYPE 'Не верный тип документа!';



SET TERM ^ ;

create procedure U3S_FUNDSALE_LISTDIFF (
    DOCID type of column document.docid
)
returns (
    WARESID type of column GWARES.waresid,
    PRODUCTDATE type of column WH_RESERVE.productdate,
    PLANQ type of column wh_reserve_client.amount,
    FACTQ type of column WH_RESERVE.amount
)
as
declare variable dtCode type of column doctype.code;
declare variable docid_sale type of column DOCUMENT.docid;
declare variable docid_fund type of column DOCUMENT.docid;
begin
    select dt.code
      from document d
           left join doctype dt on dt.doctid = d.doctype
     where d.docid = :docid
      into :dtCode;

    if (:dtcode = 'SALE') then
    begin
        docid_sale = :docid;

        select db.doc1id
          from docbond db
               left join docbondtype dbt on dbt.docbondtid = db.docbondtid
         where db.doc2id = :docid_sale
           and dbt.code = 'FUNDSALE'
          into :docid_fund;
    end
    else if (:dtcode = 'FUNDSALE') then
    begin
        docid_fund = :docid;

        select db.doc2id
          from docbond db
               left join docbondtype dbt on dbt.docbondtid = db.docbondtid
         where db.doc1id = :docid_fund
           and dbt.code = 'FUNDSALE'
          into :docid_sale;
    end
    else
    begin
        exception exc_wh_wrongdoctype;
    end

    for
        select w.waresid, w.prdate, sum(w.rcq), sum(w.roq)
          from (select rc.waresid as waresid, rc.productdate as prdate, rc.amount as rcq, 0.000 as roq
                  from wh_reserve_client_changes rc
                 where rc.docid = :docid_fund
                 union all
                select ro.waresid as waresid, ro.productdate as prdate, 0.000 as rcq, -ro.amount as roq
                  from wh_reserve_changes ro
                 where ro.docid = :docid_sale) w
          group by w.waresid, w.prdate
         having abs(sum(w.rcq)-sum(w.roq)) > 0.0001
           into :waresid, :productdate, :planq, :factq
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_SALE_STATUSCHG (
    DOCID R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable FROMOBJ type of R_ID;
declare variable DOCTID type of R_ID;
declare variable DOCTCODE type of R_CODE;
declare variable DOCSUBTYPE type of R_CODE3;
declare variable tid_gateauto type of R_ID;
declare variable ttid_select type of r_id;
begin
    select d.doctype,dt.code,d.fromobj,d.docsubtype
      from document d
           left join doctype dt on dt.doctid=d.doctype
     where d.docid = :docid
      into :doctid,:doctcode,:fromobj,:docsubtype;

    if (:doctcode <> 'SALE') then
        exception exc_k_wrongdoctype;

    if (:newstat = 'g' and coalesce(:docsubtype,'') not in ('WP','AM')) then
    begin
        -- Если повышение статуса
        if (exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.upcodes containing :newstat )) then
        begin
            execute procedure u3s_taskselect_create(:docid);

            if (not exists(select *
                             from wm_task t
                                  left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                            where t.docid = :docid
                              and tt.code = 'SELECT'
                              and t.taskmethodid is NOT NULL)) then
                update document d
                   set d.status = '2'
                 where d.docid = :docid;
        end

    end
    else if (:newstat = '2') then
    begin
        -- Если повышение статуса
        if (coalesce(:docsubtype,'') not in ('WP','AM') and
            exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.upcodes containing :newstat )) then
        begin
            if (exists(select *
                         from wm_task t
                              left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                        where t.docid = :docid
                          and tt.code = 'SELECT'
                          and t.taskmethodid is NOT NULL
                          and t.status<>'2')) then
                exception exc_k_common 'У документа есть не завершенные задания на отборку!';

            -- Поправим сам док на верные количества
            execute procedure wh_ttid_select
             returning_values :ttid_select;
            execute procedure wh_core_setdocbytask(:docid,:ttid_select,'SCANQUANT');

            -- Активируем задания на погрузку поддонов в машину
/*            select t.tid_gateauto
              from WH_LOADAUTODC_GETTASKBYDOC(:docid) t
              into :tid_gateauto;
            if (:tid_gateauto is NOT NULL) then
                execute procedure wh_loadpalletdc_createtaskes(:tid_gateauto);*/
        end
        else if (:oldstat='k') then
        begin
            execute procedure WH_SALE_SETBYPALLETS(:docid);
        end
    end
    else if (:newstat = 'e') then
    begin
        if (exists(select *
                     from wm_task t
                          left join wm_tasktype tt
                            on tt.tasktypeid = t.tasktypeid
                    where t.docid = :docid
                      and tt.code = 'LOADAUTO'
                      and t.status <> '2')) then
            exception exc_k_common 'Не завершена погрузка паллетов документа в машину!';

        -- Поправим сам док наверные количества
        execute procedure wh_core_setdocbytasklot(:docid,-1);

--        execute procedure uv_sale_taraset(:docid);

        -- Выгружаем
        if (coalesce(:docsubtype,'') not in ('WP','AM')) then
        begin
            if (exists(select *
                         from u3s_fundsale_listdiff(:docid)
                        where waresid is NOT NULL)) then
          execute procedure RBS_Q_CREATETASKEXPORT('U3S_SALE_STATUSCHG: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
           returning_values :docid;
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_RRESERVE_CHANGES (
    OBJID type of column OBJECT.objid,
    WARESID type of column GWARES.waresid,
    PRODUCTDATE type of column wh_reserve_changes.productdate
)
returns (
    DT type of column wh_reserve_changes.datetime,
    amount type of column wh_reserve_changes.amount,
    amountbad type of column wh_reserve_changes.amountbad,
    docnum type of column DOCUMENT.number,
    docdate type of column DOCUMENT.realdocdate,
    dtName type of column DOCTYPE.name,
    fromname type of R_FULLNAME,
    throughname type of R_FULLNAME,
    toname type of R_FULLNAME,
    docstat type of column R_STATUS.code,
    docstatname type of column R_STATUS.name,
    taskid type of column WM_TASK.taskid,
    ttName type of column WM_TASKTYPE.name,
    taskman type of R_FULLNAME
)
as
begin
    for
        select rc.datetime, rc.amount, rc.amountbad,
               d.number, d.realdocdate,
               (select objname from wh_get_objectname(d.fromobj)),
               (select objname from wh_get_objectname(d.throughobj)),
               (select objname from wh_get_objectname(d.toobj)),
               rs.code, rs.name, dt.name,
               t.taskid, tt.name, (select objname from wh_get_objectname(s.objid))
          from wh_reserve_changes rc
               left join wm_task t
                    left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                    left join wm_session s on s.sessionid = t.wm_sessionid
                 on t.taskid = rc.taskid
               left join document d
                    left join r_status rs on rs.code = d.status and rs.statustype = 'O'
                    left join doctype dt on dt.doctid = d.doctype
                 on d.docid = rc.docid
         where rc.objid = :objid
           and rc.waresid = :waresid
           and rc.productdate = :productdate
          into :dt, :amount, :amountbad,
               :docnum, :docdate, :fromname, :throughname, :toname,
               :docstat, :docstatname, :dtname,
               :taskid, :ttname, :taskman
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_CHANGES (
    OBJID type of column OBJECT.objid,
    WARESID type of column GWARES.waresid,
    PRODUCTDATE type of column wh_reserve_changes.productdate,
    flag type of r_flag
)
returns (
    DT type of column wh_reserve_changes.datetime,
    amount type of column wh_reserve_changes.amount,
    amountbad type of column wh_reserve_changes.amountbad,
    docnum type of column DOCUMENT.number,
    docdate type of column DOCUMENT.realdocdate,
    dtName type of column DOCTYPE.name,
    fromname type of R_FULLNAME,
    throughname type of R_FULLNAME,
    toname type of R_FULLNAME,
    docstat type of column R_STATUS.code,
    docstatname type of column R_STATUS.name,
    taskid type of column WM_TASK.taskid,
    ttName type of column WM_TASKTYPE.name,
    taskman type of R_FULLNAME
)
as
begin
    for
        select rc.datetime, rc.amount, rc.amountbad,
               d.number, d.realdocdate,
               (select objname from wh_get_objectname(d.fromobj)),
               (select objname from wh_get_objectname(d.throughobj)),
               (select objname from wh_get_objectname(d.toobj)),
               rs.code, rs.name, dt.name,
               t.taskid, tt.name, (select objname from wh_get_objectname(s.objid))
          from wh_reserve_changes rc
               left join wm_task t
                    left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                    left join wm_session s on s.sessionid = t.wm_sessionid
                 on t.taskid = rc.taskid
               left join document d
                    left join r_status rs on rs.code = d.status and rs.statustype = 'O'
                    left join doctype dt on dt.doctid = d.doctype
                 on d.docid = rc.docid
         where rc.objid = :objid
           and rc.waresid = :waresid
           and rc.productdate = :productdate
          into :dt, :amount, :amountbad,
               :docnum, :docdate, :fromname, :throughname, :toname,
               :docstat, :docstatname, :dtname,
               :taskid, :ttname, :taskman
    do
    begin
        if (:flag is NULL) then
        begin
            suspend;
        end
        else
        begin
            if (:flag = 'B' and abs(:amountbad)>0.0001) then
                suspend;

            if (:flag = 'G' and abs(:amount)>0.0001) then
                suspend;
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_RRESERVE_CLIENTS (
    OBJID type of column OBJECT.OBJID,
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of column WH_RESERVE.PRODUCTDATE
)
returns (
    CLIENTID type of column OBJECT.objid,
    CLIENTNAME type of R_FULLNAME,
    AMOUNT type of column WH_RESERVE_CLIENT.amount
)
AS
declare variable reserveid type of column wh_reserve.id;
begin
    select r.id
      from wh_reserve r
     where r.objid = :objid
       and r.productdate = :productdate
       and r.waresid = :waresid
      into :reserveid;

    if (:reserveid is NOT NULL) then
    for
        select rc.clientid, rc.amount,
               (select objname from wh_get_objectname(rc.clientid))
          from wh_reserve_client rc
         where rc.reserveid = :reserveid
          into :clientid, :amount, :clientname
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



ALTER TABLE WH_RESERVE_CLIENT_CHANGES
ADD DATETIME R_DATETIME;



SET TERM ^ ;

CREATE trigger wh_reserve_client_changes_bi0 for wh_reserve_client_changes
active before insert position 0
AS
begin
    new.datetime = current_timestamp;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_RRESERVE_CLIENT_CHANGES (
    OBJID type of column OBJECT.OBJID,
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of column WH_RESERVE_CHANGES.PRODUCTDATE,
    CLIENTID type of column OBJECT.objid
)
returns (
    DT type of column WH_RESERVE_CHANGES.DATETIME,
    AMOUNT type of column WH_RESERVE_CHANGES.AMOUNT,
--    AMOUNTBAD type of column WH_RESERVE_CHANGES.AMOUNTBAD,
    DOCNUM type of column DOCUMENT.NUMBER,
    DOCDATE type of column DOCUMENT.REALDOCDATE,
    DTNAME type of column DOCTYPE.NAME,
    FROMNAME type of R_FULLNAME,
    THROUGHNAME type of R_FULLNAME,
    TONAME type of R_FULLNAME,
    DOCSTAT type of column R_STATUS.CODE,
    DOCSTATNAME type of column R_STATUS.NAME --,
--    TASKID type of column WM_TASK.TASKID,
--    TTNAME type of column WM_TASKTYPE.NAME,
--    TASKMAN type of R_FULLNAME
)
AS
begin
    for
        select rc.datetime, rc.amount, --rc.amountbad,
               d.number, d.realdocdate,
               (select objname from wh_get_objectname(d.fromobj)),
               (select objname from wh_get_objectname(d.throughobj)),
               (select objname from wh_get_objectname(d.toobj)),
               rs.code, rs.name, dt.name --,
--               t.taskid, tt.name, (select objname from wh_get_objectname(s.objid))
          from wh_reserve_client_changes rc
/*               left join wm_task t
                    left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                    left join wm_session s on s.sessionid = t.wm_sessionid
                 on t.taskid = rc.taskid*/
               left join document d
                    left join r_status rs on rs.code = d.status and rs.statustype = 'O'
                    left join doctype dt on dt.doctid = d.doctype
                 on d.docid = rc.docid
         where rc.objid = :objid
           and rc.waresid = :waresid
           and rc.productdate = :productdate
           and rc.clientid = :clientid
          into :dt, :amount, --:amountbad,
               :docnum, :docdate, :fromname, :throughname, :toname,
               :docstat, :docstatname, :dtname --,
--               :taskid, :ttname, :taskman
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_CLIENTS (
    OBJID type of column OBJECT.OBJID,
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of column WH_RESERVE.PRODUCTDATE
)
returns (
    CLIENTID type of column OBJECT.objid,
    CLIENTNAME type of R_FULLNAME,
    AMOUNT type of column WH_RESERVE_CLIENT.amount
)
AS
--declare variable reserveid type of column wh_reserve.id;
begin
    /*select r.id
      from wh_reserve r
     where r.objid = :objid
       and r.productdate = :productdate
       and r.waresid = :waresid
      into :reserveid;*/

--    if (:reserveid is NOT NULL) then
    for
        select rcc.clientid, sum(rcc.amount)
          from wh_reserve_client_changes rcc
         where rcc.objid = :objid
           and rcc.waresid = :waresid
           and rcc.productdate = :productdate
         group by rcc.clientid
          into :clientid, :amount
    do
    begin
        clientname = NULL;
        select w.objname
          from wh_get_objectname(:clientid) w
          into :clientname;

        suspend;
    end

    /*for
        select rc.clientid, rc.amount,
               (select objname from wh_get_objectname(rc.clientid))
          from wh_reserve_client rc
         where rc.reserveid = :reserveid
          into :clientid, :amount, :clientname
    do
    begin
        suspend;
    end*/
end^

SET TERM ; ^

