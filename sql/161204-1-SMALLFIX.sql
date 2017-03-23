

SET TERM ^ ;

CREATE OR ALTER procedure U3S_SELECT_TASKP_SITESET (
    TASKID type of column WM_TASK.TASKID)
AS
declare variable waresid type of column GWARES.waresid;
declare variable taskwaresid type of column wm_task_wares.taskwaresid;
declare variable siteid type of column SITE.siteid;
declare variable palcurcnt type of column site_stack.palcurcnt;
declare variable palblkcnt type of column site_stack.palblkcnt;
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable tmid_select_p type of column wm_taskmethod.methodid;
declare variable productdate type of column WARESLOT.productdate;
begin
    select tw.taskwaresid, tw.waresid, tw.siteid, tw.plandatetime
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.status <> '2'
      into :taskwaresid, :waresid, :siteid, :productdate;

    if (:siteid is not NULL) then exit;

    select t.tasktypeid, t.taskmethodid
      from wm_task t
     where t.taskid = :taskid
      into :ttid_select, :tmid_select_p;

    for
        select ss.siteid,ss.palcurcnt
          from site_stack ss
         where ss.waresid = :waresid
           and ss.productdate = :productdate
           and ss.siteid is NOT NULL
         order by iif(ss.palmaxcnt=ss.palcurcnt,1,0) ascending,
               ss.palcurcnt ascending,
               ss.dt ascending nulls first
          into :siteid, :palcurcnt
    do
    begin
        palblkcnt = NULL;
        /*select count(tw.taskwaresid)
          from wm_task_wares tw
               left join wm_task t on t.taskid = tw.taskid
         where tw.tasktypeid = :ttid_select
           and tw.status in ('0','1')
           and tw.siteid = :siteid
           and tw.waresid = :waresid
           and t.status <> '2'
           and t.taskmethodid = :tmid_select_p
           and t.taskid <> :taskid
          into :palblkcnt;*/
        with tw as (
            select tw.taskwaresid, tw.taskid
              from wm_task_wares tw
             where tw.tasktypeid = :ttid_select
               and tw.status = '1'
               and tw.siteid = :siteid
               and tw.waresid = :waresid
             union distinct
            select tw.taskwaresid, tw.taskid
              from wm_task_wares tw
             where tw.tasktypeid = :ttid_select
               and tw.status = '0'
               and tw.siteid = :siteid
               and tw.waresid = :waresid
        )
        select count(distinct tw.taskwaresid)
          from tw
               left join wm_task t on t.taskid = tw.taskid
         where t.status <> '2'
           and t.taskmethodid = :tmid_select_p
           and t.taskid <> :taskid
          into :palblkcnt;

        if (:palblkcnt is not NULL) then
            palcurcnt = :palcurcnt - :palblkcnt;

        if (:palcurcnt > 0) then
        begin
            break;
        end
    end

    update site_stack ss
       set ss.palblkcnt = coalesce(ss.palblkcnt,0) + 1
     where ss.siteid = :siteid;

    update wm_task_wares tw
       set tw.siteid = :siteid
     where tw.taskwaresid = :taskwaresid;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_DBTID_FUNDINCOME
returns (
    DBTID type of column DOCBONDTYPE.DOCBONDTID)
AS
begin
    select dbt.docbondtid
      from docbondtype dbt
     where dbt.code = 'FUNDINCOME'
      into :dbtid;

    if (:dbtid is NULL) then
        exception EXC_WH_DOCBONDTYPE_NOTFOUND;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_INCOMEFG_QSUMMARY (
    docid_income type of column DOCUMENT.docid
)
returns(
    wcode type of column GWARES.code,
    wname type of column GWARES.name,
    wexternalcode type of column GWARES.externalcode,
    waresid type of column GWARES.waresid,
    qdocincome type of R_DOUBLE,
    qtasklot type of R_DOUBLE,
    qdocfund type of R_DOUBLE
)
as
declare variable ttid_incomefg type of column WM_TASKTYPE.tasktypeid;
declare variable dbtid_fundincome type of column DOCBONDTYPE.docbondtid;
begin
    execute procedure wh_ttid_incomefg
     returning_values :ttid_incomefg;

    execute procedure wh_dbtid_fundincome
     returning_values :dbtid_fundincome;

    for
        with w as (
            select cg.waresid, cg.amount as qdocincome, 0.000 as qtasklot, 0.000 as qdocfund
              from cargo cg
             where cg.document = :docid_income
             union all
            select wl.waresid, 0.000 as qdocincome, tl.quantity as qtasklot, 0.000 as qdocfund
              from wm_task t
                   left join wm_task_wares tw
                        left join wm_task_lot tl
                             left join wareslot wl on wl.wlotid = tl.wlotid
                          on tl.taskwaresid = tw.taskwaresid
                     on tw.taskid = t.taskid
             where t.docid = :docid_income
               and t.tasktypeid = :ttid_incomefg
             union all
            select cg.waresid, 0.000 as qdocincome, 0.000 as qtasklot, cg.amount as qdocfund
              from docbond db
                   left join cargo cg on cg.document = db.doc1id
             where db.doc2id = :docid_income
               and db.docbondtid = :dbtid_fundincome
        )
        select min(g.code), min(g.name), min(g.externalcode),
               w.waresid,
               sum(w.qdocincome), sum(w.qtasklot), sum(w.qdocfund)
          from w
               left join gwares g on g.waresid = w.waresid
         group by w.waresid
          into :wcode, :wname, :wexternalcode, :waresid,
               :qdocincome, :qtasklot, :qdocfund
    do
        suspend;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_EDITTASK (
    TASKID type of R_ID,
    TDATE type of R_DATETIME,
    GATEID type of R_ID)
AS
begin
    if (exists(select *
                 from wm_task t
                where t.taskid = :taskid
                  and t.status = '4')) then
    begin
      update wm_task t
         set t.plandatetime = :tdate, 
             t.siteid = :gateid
       where t.taskid = :taskid;
    end
    else
    begin
        exception exc_wh_wrongstatus 'Задание на погрузку разрешено редактировать только в статусе: Отложено';
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_QSUMMARY (
    DOCID_INCOME type of column DOCUMENT.DOCID)
returns (
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WEXTERNALCODE type of column GWARES.EXTERNALCODE,
    WARESID type of column GWARES.WARESID,
    QDOCINCOME type of R_DOUBLE,
    QDOCINCOMEP type of r_number,
    QDOCINCOMEM type of R_DOUBLE,
    QTASKLOT type of R_DOUBLE,
    QTASKLOTP type of r_number,
    QTASKLOTM type of R_DOUBLE,
    QDOCFUND type of R_DOUBLE,
    QDOCFUNDP type of r_number,
    QDOCFUNDM type of R_DOUBLE,
    PUFACTOR type of column WARESUNIT.factor
)
AS
declare variable ttid_incomefg type of column WM_TASKTYPE.tasktypeid;
declare variable dbtid_fundincome type of column DOCBONDTYPE.docbondtid;
declare variable palletunitid type of column UNIT.unitid;
begin
    execute procedure wh_ttid_incomefg
     returning_values :ttid_incomefg;

    execute procedure wh_dbtid_fundincome
     returning_values :dbtid_fundincome;

    select w.palletunitid
      from wm_config w
      into :palletunitid;

    for
        with w as (
            select cg.waresid, cg.amount as qdocincome, 0.000 as qtasklot, 0.000 as qdocfund
              from cargo cg
             where cg.document = :docid_income
             union all
            select wl.waresid, 0.000 as qdocincome, tl.quantity as qtasklot, 0.000 as qdocfund
              from wm_task t
                   left join wm_task_wares tw
                        left join wm_task_lot tl
                             left join wareslot wl on wl.wlotid = tl.wlotid
                          on tl.taskwaresid = tw.taskwaresid
                     on tw.taskid = t.taskid
             where t.docid = :docid_income
               and t.tasktypeid = :ttid_incomefg
             union all
            select cg.waresid, 0.000 as qdocincome, 0.000 as qtasklot, cg.amount as qdocfund
              from docbond db
                   left join cargo cg on cg.document = db.doc1id
             where db.doc2id = :docid_income
               and db.docbondtid = :dbtid_fundincome
        )
        select min(g.code), min(g.name), min(g.externalcode),
               w.waresid,
               sum(w.qdocincome), sum(w.qtasklot), sum(w.qdocfund)
          from w
               left join gwares g on g.waresid = w.waresid
         group by w.waresid
          into :wcode, :wname, :wexternalcode, :waresid,
               :qdocincome, :qtasklot, :qdocfund
    do
    begin
        pufactor = NULL;
        select wu.factor
          from waresunit wu
         where wu.waresid = :waresid
           and wu.unitid = :palletunitid
          into :pufactor;

        if (:pufactor is NOT NULL and :pufactor > 0.0001) then
        begin
            qdocincomep = floor(:qdocincome / :pufactor);
            qtasklotp = floor(:qtasklot / :pufactor);
            qdocfundp = floor(:qdocfund / :pufactor);

            qdocincomem = mod(:qdocincome, :pufactor);
            qtasklotm = mod(:qtasklot, :pufactor);
            qdocfundm = mod(:qdocfund, :pufactor);
        end
        else
        begin
            qdocincomep = NULL;
            qtasklotp = NULL;
            qdocfundp = NULL;

            qdocincomem = :qdocincome;
            qtasklotm = :qtasklot;
            qdocfundm = :qdocfund;
        end

        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDSALE_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable OBJID type of column OBJECT.OBJID;
declare variable CLIENTID type of column OBJECT.OBJID;
declare variable WARESID type of column GWARES.WARESID;
declare variable ICAMOUNT type of column IMP_CARGO.AMOUNT;
declare variable PRODUCTDATE type of column WARESLOT.PRODUCTDATE;
declare variable IRAMOUNT type of column IMP_RESERVE.AMOUNT;
declare variable REALDOCDATE type of column DOCUMENT.REALDOCDATE;
declare variable SALEDBEG type of R_DATE;
declare variable ERRMES type of RBS_BIGVARCHAR;
declare variable EXCMES type of R_EXCEPTIONUSERMES;
declare variable ERRCNT type of R_SHORTNUMBER;
declare variable PUFACTOR type of column WARESUNIT.FACTOR;
declare variable FLAG type of R_FLAG;
begin
   select gor.objid, d.toobj, d.realdocdate
     from imp_document d
          left join wh_get_reserveobj(coalesce(d.throughobj, d.fromobj)) gor on 1=1
    where d.docid = :docid
     into :objid, :clientid, :realdocdate;

   for
    select ic.waresid, ic.amount
      from imp_cargo ic
     where ic.document = :docid
       and ic.amount > 0.000001
      into :waresid, :icamount
   do
   begin
        for
            select ir.productdate, ir.amount
              from imp_reserve ir
             where ir.docid = :docid
               and ir.waresid = :waresid
              into :productdate, :iramount
        do
        if (exists(select *
                     from wh_reserve r
                    where r.objid = :objid
                      and r.waresid = :waresid
                      and r.productdate = :productdate
                      and r.amountfree - :iramount > -0.0001)) then
        begin
           insert into wh_tmp_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
           values(:docid, :waresid, :productdate, :iramount, :objid, :clientid);
    
           icamount = :icamount - :iramount;
        end
        else
        begin
           icamount = 0.000;
           break;
        end

        if (:icamount > 0.0000001) then
        begin
            pufactor = NULL;
            select w.W_PUFACTOR
              from wh_wares_getpalletunit(:waresid) w
              into :pufactor;
            if (:pufactor < 0.0001) then
                pufactor = NULL;

            select w.dbeg
              from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
              into :saledbeg;
            
            if (:pufactor is NOT NULL) then
            begin
                flag = NULL;
                while (:flag is NULL) do
                begin
                    if (:icamount - :pufactor > -0.0001) then
                    begin
                        iramount = NULL;
                        select first(1) r.amountfree - coalesce(t.amount, 0), r.productdate
                          from wh_reserve r
                               left join WH_IMP_FUNDSALE_RESERVE_DO_TMP(r.waresid, r.objid, r.productdate) t on 1=1
                         where r.objid = :objid
                           and r.waresid = :waresid
                           and r.productdate > :saledbeg
--                           and r.amountfree - :pufactor > -0.0001
                           and r.amountfree - coalesce(t.amount, 0) - :pufactor > -0.0001
                         order by r.productdate ascending
                          into :iramount, :productdate;
                        
                        if (:iramount is NOT NULL and :iramount > 0.00001) then
                        begin
                            insert into wh_tmp_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
                            values(:docid, :waresid, :productdate, :pufactor, :objid, :clientid);
    
                            icamount = :icamount - :pufactor;
                        end
                        else
                        begin
                            flag = '1';
                        end
                    end
                    else
                    begin
                        for
                            select mod(r.amountfree, :pufactor), r.productdate
                              from wh_reserve r
                             where r.objid = :objid
                               and r.waresid = :waresid
                               and r.productdate > :saledbeg
                               and r.amountfree > 0.0000001
                               and mod(r.amountfree, :pufactor) > 0.0001
                             order by r.productdate ascending
                              into :iramount, :productdate
                        do
                        begin
                           if (:iramount - :icamount > 0.0000001) then
                                iramount = :icamount;
                
                           insert into wh_tmp_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
                           values(:docid, :waresid, :productdate, :iramount, :objid, :clientid);
                    
                           icamount = :icamount - :iramount;

                           if (:icamount < 0.0000001) then
                            break;
                        end
                        flag = 1;
                    end

                    --if (:icamount < 0.0001) then
                    --  flag = 1;
                end
            end

            if (:icamount > 0.0001) then
            begin
                for
                    select r.amountfree, r.productdate
                      from wh_reserve r
                     where r.objid = :objid
                       and r.waresid = :waresid
                       and r.productdate > :saledbeg
                       and r.amountfree > 0.0000001
                     order by r.productdate ascending
                      into :iramount, :productdate
                do
                begin
                   if (:iramount - :icamount > 0.0000001) then
                        iramount = :icamount;
        
                   insert into wh_tmp_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
                   values(:docid, :waresid, :productdate, :iramount, :objid, :clientid);
            
                   icamount = :icamount - :iramount;
        
                   if (:icamount < 0.0000001) then
                    break;
                end
            end
        end
   end

   with chg1 as (
       select w.waresid as waresid, w.amount as amount
         from wh_tmp_reserve_client_changes w
        where w.docid = :docid
        union all
       select ic.waresid as waresid, -ic.amount as amount
         from imp_cargo ic
        where ic.document = :docid
   ),
   chg2 as (
    select chg1.waresid as waresid, sum(chg1.amount) as amount
      from chg1
     group by chg1.waresid
    having abs(sum(chg1.amount)) > 0.0001
   )
   select list(distinct g.externalcode || '->' || g.code), count(distinct g.waresid)
     from chg2
          left join gwares g on g.waresid = chg2.waresid
     into :errmes, :errcnt;

   if (:errcnt is NOT NULL and :errcnt > 0) then
   begin
        errmes = 'Невозможно зарезервировать в нужном количестве товары: '||:errmes;
        execute procedure WH_TEXT_TO_EXCMES(:errmes)
         returning_values :excmes;
        exception exc_wh_wrongamount :excmes;
   end
   else
   begin
        insert into wh_reserve_client_changes ( OBJID, WARESID, PRODUCTDATE, CLIENTID, AMOUNT, DOCID)
        select t.objid, t.waresid,  t.productdate, t.clientid, sum(t.amount), t.docid
          from wh_tmp_reserve_client_changes t
         group by t.objid, t.waresid,  t.productdate, t.clientid, t.docid;
   end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDSALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I')
AS
declare variable queueid type of column r_queue.queueid;
begin
    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');
    execute procedure WH_IMP_FUNDSALE_RESERVE_CANC(:docid);

    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    if (:ACTIONCODE = 'D') then
    begin
        delete from imp_cargo ic
         where ic.document = :docid;

        delete from imp_document id
         where id.docid = :docid;
    end
    else if (:actioncode = 'I') then
    begin
        execute procedure WH_IMP_FUNDSALE_RESERVE_DO(:docid);

        select d.queueid
          from imp_document d
         where d.docid = :docid
          into :queueid;
        if (:queueid is NOT NULL) then
            execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');

        execute procedure RBS_Q_CREATETASKEXPORT('Результат резервирования продажи',:docid,NULL,NULL)
          returning_values :queueid;
    
        delete from imp_document id
         where id.docid = :docid;
    end
    else
    begin
        exception exc_wh_wrongdocstat 'wrong ACTIONCODE';
    end
end^

SET TERM ; ^

