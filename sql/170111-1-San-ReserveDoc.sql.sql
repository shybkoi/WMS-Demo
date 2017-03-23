

SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE_PREP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable waresid type of column GWARES.waresid;
declare variable selgroupid type of column k_wares_selgroup.id;
declare variable maxfactor type of r_double;
declare variable amount type of r_double;
declare variable numpallet type of r_number;
declare variable numpos type of r_number;
declare variable palletunitid type of r_id;
declare variable ttid_select type of r_id;
declare variable tmid_pallet type of column wm_taskmethod.methodid;
declare variable tmid_f type of column wm_taskmethod.methodid;
declare variable objid type of r_id;
declare variable weight type of r_double;
declare variable capacity type of r_double;
declare variable zoneid type of r_id;
declare variable cntzone type of r_number;
declare variable docid_fundsale type of column DOCUMENT.docid;
declare variable productdate type of column WARESLOT.productdate;
begin
    select distinct db.doc1id
      from docbond db
     where db.doc2id = :docid
       and db.docbondtid = (select dbtid from wh_dbtid_fundsale)
      into :docid_fundsale;

    if (:docid_fundsale is NULL) then
        exception exc_wh_wrongdocstat 'Документ резерва продажи не найден!';


    select wm.palletunitid
      from wm_config wm
      into :palletunitid;

    select k.ttid
      from k_tasktype_by_code('SELECT',NULL) k
      into :ttid_select;

    select tm.methodid
      from wm_taskmethod tm
     where tm.tasktypeid = :ttid_select and tm.algorithm = 'P'
      into :tmid_pallet;

    select tm.methodid
      from wm_taskmethod tm
     where tm.tasktypeid = :ttid_select and tm.algorithm = 'F'
      into :tmid_f;

    if (:tmid_f is NULL) then
        exception exc_k_common 'Не найден метод отборки с паллета!';

    select d.fromobj
      from document d
     where d.docid = :docid
      into :objid;

    -- Зона по умолчанию
    for
        select sz.zoneid
          from sitezone sz
         where sz.objid = :objid
          into :zoneid
    do
        cntzone = :cntzone + 1;
    if (:cntzone <> 1) then zoneid = 0;

    numpallet = 0;
    numpos = 1;
    for
        with wares as(
            select r.waresid as waresid, r.productdate as productdate, sum(rd.amount)  as amount
              from wh_reserve_doc rd
                   left join wh_reserve r on r.id = rd.reserveid
             where rd.docid = :docid_fundsale
            group by r.waresid, r.productdate
        )
        select w.waresid,w.productdate,w.amount,coalesce(g.selgroup,0),wu.factor
          from wares w
               left join gwares g on g.waresid = w.waresid
               left join waresunit wu on wu.waresid = w.waresid and wu.unitid = :palletunitid
          into :waresid,:productdate,:amount,:selgroupid,:maxfactor
    do
    begin
        -- Откидываем полные поддоны
        if (:maxfactor is NOT NULL) then
            while (:amount-:maxfactor > -0.000001) do -- and :rest - :maxfactor > -0.000001) do
            begin
                weight = NULL; capacity = NULL;
                select wc.weight,wc.capacity
                  from WM_GETWARESWEIGHTCAPACITY(:waresid,:maxfactor) wc
                  into :weight,:capacity;

                numpallet = :numpallet + 1;
                insert into k_tbltmp_select_docwares(waresid,amount,selgroupid,taskmethodid,rest,slotid,rowid,weight,capacity,numpallet,num,zoneid,productdate)
                values(:waresid,:maxfactor,:selgroupid,:tmid_pallet,NULL,NULL,NULL,:weight,:capacity,:numpallet,:numpos,:zoneid,:productdate);

                amount = :amount - :maxfactor;
            end
        
        -- Скидываем остатки
        if (:amount>0.00001) then
        begin
            weight = NULL; capacity = NULL;
            select wc.weight,wc.capacity
              from WM_GETWARESWEIGHTCAPACITY(:waresid,:amount) wc
              into :weight,:capacity;

             insert into k_tbltmp_select_docwares(waresid,amount,selgroupid,taskmethodid,rest,slotid,rowid,weight,capacity,zoneid,sitesegmentid,productdate)
             values(:waresid,:amount,:selgroupid,:tmid_f,NULL,NULL,NULL,:weight,:capacity,:zoneid,NULL,:productdate);
        end
    end

    update k_tbltmp_select_docwares sd
       set sd.numpallet = :numpallet + 1
     where sd.taskmethodid=:tmid_f
       and numpallet is NULL;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_FUNDSALE_LISTDIFF (
    DOCID type of column DOCUMENT.DOCID)
returns (
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of column WH_RESERVE.PRODUCTDATE,
    PLANQ type of column WH_RESERVE_CLIENT.AMOUNT,
    FACTQ type of column WH_RESERVE.AMOUNT)
AS
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
                  from wh_reserve_doc_changes rc
                 where rc.docid = :docid_fund
                   and rc.rdocid = :docid_fund
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

CREATE OR ALTER procedure EXP_DOC_FUNDSALE_WARESRESERVE (
    DOCID type of column DOCUMENT.DOCID,
    WARESID type of column GWARES.WARESID)
returns (
    PRDATE type of column WH_RESERVE_CHANGES.PRODUCTDATE,
    AMOUNT type of column WH_RESERVE_CHANGES.AMOUNT)
AS
begin
    for
        select rcc.productdate, sum(rcc.amount)
          from wh_reserve_doc_changes rcc
         where rcc.docid = :docid
           and rcc.waresid = :waresid
           and rcc.rdocid = :docid
         group by rcc.productdate
          into :prdate, :amount
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPLAN_FUNDSALE (
    TASKID_GATEAUTO type of column WM_TASK.TASKID)
returns (
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WEXTERNALCODE type of column GWARES.EXTERNALCODE,
    AMOUNT type of column WH_RESERVE_CLIENT_CHANGES.AMOUNT,
    PRODUCTDATE type of column WH_RESERVE_CLIENT_CHANGES.PRODUCTDATE,
    DOCNUMS type of RBS_BIGVARCHAR)
AS
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable dbtid_fundsale type of column DOCBONDTYPE.docbondtid;
begin
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    execute procedure wh_dbtid_fundsale
     returning_values :dbtid_fundsale;

    for
        with doc as(
            select distinct d.docid, d.number
              from wh_taskbond tb
                   left join wm_task t
                        left join docbond db
                             left join document d on d.docid = db.doc1id
                          on db.doc2id = t.docid
                     on t.taskid = tb.task2id
             where tb.task1id = :taskid_gateauto
               and tb.taskbondtid = :tbtid_cardocs
               and db.docbondtid = :dbtid_fundsale
        )
        select g.waresid, rcc.productdate,
               sum(rcc.amount), list(distinct doc.number),
               max(g.code), max(g.name), max(g.externalcode)
          from doc
               left join wh_reserve_doc_changes rcc
                    left join gwares g on g.waresid = rcc.waresid
                 on rcc.docid = doc.docid and rcc.rdocid = doc.docid
         group by g.waresid, rcc.productdate
        having sum(rcc.amount) > 0.0001
          into :wid, :productdate,
               :amount, :docnums,
               :wcode, :wname, :wexternalcode
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I')
AS
declare variable queueid type of column R_QUEUE.queueid;
declare variable waresid type of column GWARES.WARESID;
declare variable wcode type of column GWARES.code;
declare variable docid_fundsale type of column DOCUMENT.docid;
declare variable ttid_loadauto type of column WM_TASKTYPE.tasktypeid;
declare variable dbtid_fundsale type of column DOCBONDTYPE.docbondtid;
declare variable idtoobj type of column OBJECT.objid;
declare variable dtoobj type of column OBJECT.objid;
begin
    if (not exists(select *
                     from imp_document id
                          left join doctype dt on id.doctype = dt.doctid
                    where id.docid = :docid
                      and dt.code = 'SALE')) then
        exception exc_wh_wrongdoctype;


    if (:actioncode = 'I') then
    begin
        execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '=');
    
        select id.queueid, d.docid, id.toobj, d.toobj
          from imp_document id
               left join document d on d.docid = id.docbondid
         where id.docid = :docid
          into :queueid, :docid_fundsale, :idtoobj, :dtoobj;

        if (:docid_fundsale is NULL) then
            exception exc_wh_wrongdocstat 'Не найден документ продажи резерва';
    
        if (:idtoobj<>:dtoobj) then
            exception exc_wh_wrongdocstat 'Не верный клиент';

        select first(1) u.waresid
          from (select ir.waresid as waresid, ir.productdate as productdate, ir.amount as amount
                  from imp_reserve ir
                 where ir.docid = :docid
                 union all
                select rcc.waresid as waresid, rcc.productdate as productdate, -rcc.amount  as amount
                  from wh_reserve_doc_changes rcc
                 where rcc.docid = :docid_fundsale
                   and rcc.rdocid = :docid_fundsale) u
         group by u.waresid, u.productdate
        having abs(sum(u.amount)) > 0.0001
          into :waresid;
    
        if (:waresid is NOT NULL) then
        begin
            select g.code
              from gwares g
             where g.waresid = :waresid
              into :wcode;
    
            exception exc_wh_wrongamount 'Не верные данные по резерву у товара с кодом ' || :wcode;
        end
    
        update imp_document id
           set id.status = '1'
         where id.docid = :docid;
    
        execute procedure wh_imp_doc_transfer(:docid);
    
        update or insert into docbond (DOCBONDTID, DOC1ID, DOC2ID)
        values ( (select dbtid from wh_dbtid_fundsale), :docid_fundsale, :docid)
        matching (DOCBONDTID, DOC1ID, DOC2ID);
    
        if (:queueid is NOT NULL) then
            execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');
    end
    else if (:actioncode = 'D') then
    begin
        execute procedure wh_ttid_loadauto
         returning_values :ttid_loadauto;

        if (exists(select *
                     from wm_task t
                    where t.docid = :docid
                      and t.tasktypeid = :ttid_loadauto)) then
            exception exc_wh_wrongdocstat 'У документа уже есть задание на погрузку!';

        select dbt.docbondtid
          from docbondtype dbt
         where dbt.code = 'FUNDSALE'
          into :dbtid_fundsale;

        delete from docbond db
         where db.doc2id = :docid and db.docbondtid = :dbtid_fundsale;

        delete from document d
         where d.docid = :docid;
    end
    else
    begin
         exception exc_wh_wrongdocstat 'wrong ACTIONCODE';
    end

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPLAN_FUNDSALE (
    TASKID_GATEAUTO type of column WM_TASK.TASKID)
returns (
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WEXTERNALCODE type of column GWARES.EXTERNALCODE,
    AMOUNT type of column WH_RESERVE_CLIENT_CHANGES.AMOUNT,
    PRODUCTDATE type of column WH_RESERVE_DOC_CHANGES.PRODUCTDATE,
    DOCNUMS type of RBS_BIGVARCHAR)
AS
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable dbtid_fundsale type of column DOCBONDTYPE.docbondtid;
begin
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    execute procedure wh_dbtid_fundsale
     returning_values :dbtid_fundsale;

    for
        with doc as(
            select distinct d.docid, d.number
              from wh_taskbond tb
                   left join wm_task t
                        left join docbond db
                             left join document d on d.docid = db.doc1id
                          on db.doc2id = t.docid
                     on t.taskid = tb.task2id
             where tb.task1id = :taskid_gateauto
               and tb.taskbondtid = :tbtid_cardocs
               and db.docbondtid = :dbtid_fundsale
        )
        select g.waresid, rcc.productdate,
               sum(rcc.amount), list(distinct doc.number),
               max(g.code), max(g.name), max(g.externalcode)
          from doc
               left join wh_reserve_doc_changes rcc
                    left join gwares g on g.waresid = rcc.waresid
                 on rcc.docid = doc.docid and rcc.rdocid = doc.docid
         group by g.waresid, rcc.productdate
        having sum(rcc.amount) > 0.0001
          into :wid, :productdate,
               :amount, :docnums,
               :wcode, :wname, :wexternalcode
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPLAN_FUNDSALE (
    TASKID_GATEAUTO type of column WM_TASK.TASKID)
returns (
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WEXTERNALCODE type of column GWARES.EXTERNALCODE,
    AMOUNT type of column WH_RESERVE_DOC_CHANGES.AMOUNT,
    PRODUCTDATE type of column WH_RESERVE_DOC_CHANGES.PRODUCTDATE,
    DOCNUMS type of RBS_BIGVARCHAR)
AS
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable dbtid_fundsale type of column DOCBONDTYPE.docbondtid;
begin
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    execute procedure wh_dbtid_fundsale
     returning_values :dbtid_fundsale;

    for
        with doc as(
            select distinct d.docid, d.number
              from wh_taskbond tb
                   left join wm_task t
                        left join docbond db
                             left join document d on d.docid = db.doc1id
                          on db.doc2id = t.docid
                     on t.taskid = tb.task2id
             where tb.task1id = :taskid_gateauto
               and tb.taskbondtid = :tbtid_cardocs
               and db.docbondtid = :dbtid_fundsale
        )
        select g.waresid, rcc.productdate,
               sum(rcc.amount), list(distinct doc.number),
               max(g.code), max(g.name), max(g.externalcode)
          from doc
               left join wh_reserve_doc_changes rcc
                    left join gwares g on g.waresid = rcc.waresid
                 on rcc.docid = doc.docid and rcc.rdocid = doc.docid
         group by g.waresid, rcc.productdate
        having sum(rcc.amount) > 0.0001
          into :wid, :productdate,
               :amount, :docnums,
               :wcode, :wname, :wexternalcode
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDSALE_RESERVE_CANC (
    DOCID type of column DOCUMENT.DOCID)
AS
begin
    insert into wh_reserve_client_changes ( OBJID, WARESID, PRODUCTDATE, CLIENTID, AMOUNT, DOCID)
    select rc.objid, rc.waresid, rc.productdate, rc.clientid, -sum(rc.amount), rc.docid
      from wh_reserve_client_changes rc
     where rc.docid = :docid
     group by rc.waresid, rc.productdate, rc.objid, rc.clientid, rc.docid
    having abs(sum(rc.amount)) > 0.0000001;

    insert into wh_reserve_doc_changes ( OBJID, WARESID, PRODUCTDATE, RDOCID, AMOUNT, DOCID)
    select rc.objid, rc.waresid, rc.productdate, rc.rdocid, -sum(rc.amount), rc.docid
      from wh_reserve_doc_changes rc
     where rc.docid = :docid
       and rc.rdocid = :docid
     group by rc.waresid, rc.productdate, rc.objid, rc.rdocid, rc.docid
    having abs(sum(rc.amount)) > 0.0000001;

    insert into wh_reserve_doc_changes ( OBJID, WARESID, PRODUCTDATE, RDOCID, AMOUNT, DOCID)
    select rc.objid, rc.waresid, rc.productdate, rc.rdocid, -sum(rc.amount), rc.docid
      from wh_reserve_doc_changes rc
     where rc.docid = :docid
       and rc.rdocid <> :docid
     group by rc.waresid, rc.productdate, rc.objid, rc.rdocid, rc.docid
    having abs(sum(rc.amount)) > 0.0000001;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_FUNDSALE_LISTDIFF (
    DOCID type of column DOCUMENT.DOCID)
returns (
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of column WH_RESERVE.PRODUCTDATE,
    PLANQ type of column WH_RESERVE_DOC.AMOUNT,
    FACTQ type of column WH_RESERVE.AMOUNT)
AS
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
                  from wh_reserve_doc_changes rc
                 where rc.docid = :docid_fund
                   and rc.rdocid = :docid_fund
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

