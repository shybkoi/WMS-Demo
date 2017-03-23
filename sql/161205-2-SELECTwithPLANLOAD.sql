

SET TERM ^ ;

CREATE OR ALTER procedure WH_SALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I'
)
AS
declare variable queueid type of column R_QUEUE.queueid;
declare variable waresid type of column GWARES.WARESID;
declare variable wcode type of column GWARES.code;
declare variable docid_fundsale type of column DOCUMENT.docid;
declare variable ttid_loadauto type of column WM_TASKTYPE.tasktypeid;
declare variable dbtid_fundsale type of column DOCBONDTYPE.docbondtid;
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
    
        select d.queueid, d.docbondid
          from imp_document d
         where d.docid = :docid
          into :queueid, :docid_fundsale;
    
        select first(1) u.waresid
          from (select ir.waresid as waresid, ir.productdate as productdate, ir.amount as amount
                  from imp_reserve ir
                 where ir.docid = :docid
                 union all
                select rcc.waresid as waresid, rcc.productdate as productdate, -rcc.amount  as amount
                  from wh_reserve_client_changes rcc
                 where rcc.docid = :docid_fundsale) u
         group by u.waresid, u.productdate
        having abs(sum(u.amount)) > 0.0001
          into :waresid;
    
        if (:waresid is NOT NULL) then
        begin
            select g.code
              from gwares g
             where g.waresid = :waresid
              into :wcode;
    
            exception exc_wh_wrongamount 'Ќе верные данные по резерву у товара с кодом ' || :wcode;
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
            exception exc_wh_wrongdocstat '” документа уже есть задание на погрузку!';

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

create or alter procedure U3S_SELMANAG_LISTCLIENTDOCS (
    OBJID type of column OBJECT.objid,
    CLID type of column OBJECT.objid,
    CLDATE R_DATE,
    DTCODES r_varchar255)
returns (
    DOCID type of column DOCUMENT.docid,
    DOCDATE type of column DOCUMENT.docdate,
    RDOCDATE type of column DOCUMENT.realdocdate,
    DOCNUM type of column DOCUMENT.number,
    DOCSUM type of column DOCUMENT.amount,
    STAT type of column R_STATUS.code,
    STATNAME type of column R_STATUS.name,
    THROUGHNAME type of R_FULLNAME,
    GATASKID type of column WM_TASK.TASKID,
    GASTAT type of column R_STATUS.code,
    GASTATNAME type of column R_STATUS.name,
    GASITENAME type of column SITE.name,
    GAAUTONAME type of column T_AUTO.name,
    GADATETIME type of column WM_TASK.plandatetime
)
AS
declare variable doctid type of column DOCTYPE.doctid;
declare variable ttid_loadauto type of column WM_TASKTYPE.tasktypeid;
begin
    execute procedure wh_ttid_loadauto
     returning_values :ttid_loadauto;

    for
        select dt.doctid
          from r_listwords(:dtcodes,',',0) r
               left join doctype dt on dt.code = r.word
          into :doctid
    do
    for
        select d.docid,d.docdate,d.number,d.amount,d.realdocdate,d.status,rs.name,
               (select objname from wh_get_objectname(d.throughobj)),
               ga.taskid, gast.code, gast.name, gas.name, gaa.name, ga.plandatetime
          from K_SELMANAG_UTIL_DOCTYPESTATUSES(:doctid,'a') k
               left join document d
                    left join r_status rs on rs.statustype='O' and rs.code=d.status
                    left join wm_task ga
                         left join r_status gast on gast.statustype='T' and gast.code=d.status
                         left join site gas on gas.siteid = ga.siteid
                         left join t_auto gaa on gaa.aid = ga.infoid
                      on ga.docid = d.docid and ga.tasktypeid = :ttid_loadauto
                 on d.doctype = :doctid and d.status = k.stat
                    and d.fromobj = :objid and d.toobj = :clid and d.realdocdate = :cldate
         where d.docid is NOT NULL
          into :docid,:docdate,:docnum,:docsum,:rdocdate,:stat,:statname,:throughname,
               :gataskid, :gastat, :gastatname, :gasitename, :gaautoname, :gadatetime
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SELMANAG_LISTCLIENTDOCS (
    OBJID type of column OBJECT.objid,
    CLID type of column OBJECT.objid,
    CLDATE R_DATE,
    DTCODES r_varchar255)
returns (
    DOCID type of column DOCUMENT.docid,
    DOCDATE type of column DOCUMENT.docdate,
    RDOCDATE type of column DOCUMENT.realdocdate,
    DOCNUM type of column DOCUMENT.number,
    DOCSUM type of column DOCUMENT.amount,
    STAT type of column R_STATUS.code,
    STATNAME type of column R_STATUS.name,
    THROUGHNAME type of R_FULLNAME,
    GATASKID type of column WM_TASK.TASKID,
    GASTAT type of column R_STATUS.code,
    GASTATNAME type of column R_STATUS.name,
    GASITENAME type of column SITE.name,
    GAAUTONAME type of column T_AUTO.name,
    GADATETIME type of column WM_TASK.plandatetime
)
AS
declare variable doctid type of column DOCTYPE.doctid;
declare variable ttid_loadauto type of column WM_TASKTYPE.tasktypeid;
declare variable tbtid_cardocs type of column WH_TASKBONDTYPE.id;
begin
    execute procedure wh_ttid_loadauto
     returning_values :ttid_loadauto;

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    for
        select dt.doctid
          from r_listwords(:dtcodes,',',0) r
               left join doctype dt on dt.code = r.word
          into :doctid
    do
    for
        select d.docid,d.docdate,d.number,d.amount,d.realdocdate,d.status,rs.name,
               (select objname from wh_get_objectname(d.throughobj)),
               ga.taskid, gast.code, gast.name, gas.name, gaa.name, ga.plandatetime
          from K_SELMANAG_UTIL_DOCTYPESTATUSES(:doctid,'a') k
               left join document d
                    left join r_status rs on rs.statustype='O' and rs.code=d.status
                    left join wm_task ld
                         left join wh_taskbond tbcd
                              left join wm_task ga
                                   left join r_status gast on gast.statustype='T' and gast.code=d.status
                                   left join site gas on gas.siteid = ga.siteid
                                   left join t_auto gaa on gaa.aid = ga.infoid
                                on ga.taskid= tbcd.task1id
                           on tbcd.task2id = ga.taskid and tbcd.taskbondtid = :tbtid_cardocs
                      on ld.docid = d.docid and ld.tasktypeid = :ttid_loadauto
                 on d.doctype = :doctid and d.status = k.stat
                    and d.fromobj = :objid and d.toobj = :clid and d.realdocdate = :cldate
         where d.docid is NOT NULL
          into :docid,:docdate,:docnum,:docsum,:rdocdate,:stat,:statname,:throughname,
               :gataskid, :gastat, :gastatname, :gasitename, :gaautoname, :gadatetime
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SELMANAG_LISTCLIENTDOCS (
    OBJID type of column OBJECT.objid,
    CLID type of column OBJECT.objid,
    CLDATE R_DATE,
    DTCODES r_varchar255)
returns (
    DOCID type of column DOCUMENT.docid,
    DOCDATE type of column DOCUMENT.docdate,
    RDOCDATE type of column DOCUMENT.realdocdate,
    DOCNUM type of column DOCUMENT.number,
    DOCSUM type of column DOCUMENT.amount,
    STAT type of column R_STATUS.code,
    STATNAME type of column R_STATUS.name,
    THROUGHNAME type of R_FULLNAME,
    GATASKID type of column WM_TASK.TASKID,
    GASTAT type of column R_STATUS.code,
    GASTATNAME type of column R_STATUS.name,
    GASITENAME type of column SITE.name,
    GAAUTONAME type of column T_AUTO.name,
    GADATETIME type of column WM_TASK.plandatetime
)
AS
declare variable doctid type of column DOCTYPE.doctid;
declare variable ttid_loadauto type of column WM_TASKTYPE.tasktypeid;
declare variable tbtid_cardocs type of column WH_TASKBONDTYPE.id;
begin
    execute procedure wh_ttid_loadauto
     returning_values :ttid_loadauto;

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    for
        select dt.doctid
          from r_listwords(:dtcodes,',',0) r
               left join doctype dt on dt.code = r.word
          into :doctid
    do
    for
        select d.docid,d.docdate,d.number,d.amount,d.realdocdate,d.status,rs.name,
               (select objname from wh_get_objectname(d.throughobj)),
               ga.taskid, gast.code, gast.name, gas.name, gaa.name, ga.plandatetime
          from K_SELMANAG_UTIL_DOCTYPESTATUSES(:doctid,'a') k
               left join document d
                    left join r_status rs on rs.statustype='O' and rs.code=d.status
                    left join wm_task ld
                         left join wh_taskbond tbcd
                              left join wm_task ga
                                   left join r_status gast on gast.statustype='T' and gast.code=d.status
                                   left join site gas on gas.siteid = ga.siteid
                                   left join t_auto gaa on gaa.aid = ga.infoid
                                on ga.taskid= tbcd.task1id
                           on tbcd.task2id = ld.taskid and tbcd.taskbondtid = :tbtid_cardocs
                      on ld.docid = d.docid and ld.tasktypeid = :ttid_loadauto
                 on d.doctype = :doctid and d.status = k.stat
                    and d.fromobj = :objid and d.toobj = :clid and d.realdocdate = :cldate
         where d.docid is NOT NULL
          into :docid,:docdate,:docnum,:docsum,:rdocdate,:stat,:statname,:throughname,
               :gataskid, :gastat, :gastatname, :gasitename, :gaautoname, :gadatetime
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADAUTODC_GETTASKBYDOC (
    DOCID type of column DOCUMENT.docid
)
returns (
    TID_LOADAUTO type of column WM_TASK.taskid,
    TID_GATEAUTO type of column WM_TASK.taskid
)
AS
declare variable ttid_loadauto type of column WM_TASKTYPE.tasktypeid;

declare variable tbtid_cardocs type of column wh_taskbondtype.id;
begin
    execute procedure wh_ttid_loadauto returning_values :ttid_loadauto;

    select t.taskid
      from wm_task t
     where t.docid = :docid
       and t.tasktypeid = :ttid_loadauto
      into :tid_loadauto;

    if (:tid_loadauto is NOT NULL) then
    begin
        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'CARDOCS'
          into :tbtid_cardocs;

        select tb.task1id
          from wh_taskbond tb
         where tb.task2id = :tid_loadauto
           and tb.taskbondtid = :tbtid_cardocs
          into :tid_gateauto;
    end
            
    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADAUTODC_GETTASKBYDOC (
    DOCID type of column DOCUMENT.docid
)
returns (
    TID_LOADAUTO type of column WM_TASK.taskid,
    TID_GATEAUTO type of column WM_TASK.taskid
)
AS
declare variable ttid_loadauto type of column WM_TASKTYPE.tasktypeid;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
begin
    execute procedure wh_ttid_loadauto returning_values :ttid_loadauto;

    select t.taskid
      from wm_task t
     where t.docid = :docid
       and t.tasktypeid = :ttid_loadauto
      into :tid_loadauto;

    if (:tid_loadauto is NOT NULL) then
    begin
        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'CARDOCS'
          into :tbtid_cardocs;

        select tb.task1id
          from wh_taskbond tb
         where tb.task2id = :tid_loadauto
           and tb.taskbondtid = :tbtid_cardocs
          into :tid_gateauto;
    end
            
    suspend;
end^

SET TERM ; ^




SET TERM ^ ;

CREATE OR ALTER procedure U3S_SELMANAG_LISTCLIENTDOCS (
    OBJID type of column OBJECT.objid,
    CLID type of column OBJECT.objid,
    CLDATE R_DATE,
    DTCODES r_varchar255)
returns (
    DOCID type of column DOCUMENT.docid,
    DOCDATE type of column DOCUMENT.docdate,
    RDOCDATE type of column DOCUMENT.realdocdate,
    DOCNUM type of column DOCUMENT.number,
    DOCSUM type of column DOCUMENT.amount,
    STAT type of column R_STATUS.code,
    STATNAME type of column R_STATUS.name,
    THROUGHNAME type of R_FULLNAME,
    GATASKID type of column WM_TASK.TASKID,
    GASTAT type of column R_STATUS.code,
    GASTATNAME type of column R_STATUS.name,
    GASITENAME type of column SITE.name,
    GAAUTONAME type of column T_AUTO.name,
    GADATETIME type of column WM_TASK.plandatetime
)
AS
declare variable doctid type of column DOCTYPE.doctid;
declare variable ttid_loadauto type of column WM_TASKTYPE.tasktypeid;
declare variable tbtid_cardocs type of column WH_TASKBONDTYPE.id;
begin
    for
        select d.DOCID, d.DOCDATE, d.RDOCDATE, d.DOCNUM, d.DOCSUM, d.STAT, d.STATNAME, d.THROUGHNAME,
               ga.taskid, gast.code, gast.name, gas.name, gaa.name, ga.plandatetime
          from k_selmanag_listclientdocs(:objid, :clid, :cldate, :dtcodes) d
               left join wh_loadautodc_gettaskbydoc(d.docid) tbcd
                    left join wm_task ga
                         left join r_status gast on gast.statustype='T' and gast.code=ga.status
                         left join site gas on gas.siteid = ga.siteid
                         left join t_auto gaa on gaa.aid = ga.infoid
                      on ga.taskid = tbcd.tid_gateauto
                 on 1=1
          into :DOCID, :DOCDATE, :RDOCDATE, :DOCNUM, :DOCSUM, :STAT, :STATNAME, :THROUGHNAME,
               :gataskid, :gastat, :gastatname, :gasitename, :gaautoname, :gadatetime
    do
    begin
        suspend;
    end

    /*execute procedure wh_ttid_loadauto
     returning_values :ttid_loadauto;

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    for
        select dt.doctid
          from r_listwords(:dtcodes,',',0) r
               left join doctype dt on dt.code = r.word
          into :doctid
    do
    for
        select d.docid,d.docdate,d.number,d.amount,d.realdocdate,d.status,rs.name,
               (select objname from wh_get_objectname(d.throughobj)),
               ga.taskid, gast.code, gast.name, gas.name, gaa.name, ga.plandatetime
          from K_SELMANAG_UTIL_DOCTYPESTATUSES(:doctid,'a') k
               left join document d
                    left join r_status rs on rs.statustype='O' and rs.code=d.status
                    left join wm_task ld
                         left join wh_taskbond tbcd
                              left join wm_task ga
                                   left join r_status gast on gast.statustype='T' and gast.code=d.status
                                   left join site gas on gas.siteid = ga.siteid
                                   left join t_auto gaa on gaa.aid = ga.infoid
                                on ga.taskid= tbcd.task1id
                           on tbcd.task2id = ld.taskid and tbcd.taskbondtid = :tbtid_cardocs
                      on ld.docid = d.docid and ld.tasktypeid = :ttid_loadauto
                 on d.doctype = :doctid and d.status = k.stat
                    and d.fromobj = :objid and d.toobj = :clid and d.realdocdate = :cldate
         where d.docid is NOT NULL
          into :docid,:docdate,:docnum,:docsum,:rdocdate,:stat,:statname,:throughname,
               :gataskid, :gastat, :gastatname, :gasitename, :gaautoname, :gadatetime
    do
    begin
        suspend;
    end*/
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SELMANAG_LISTCLIENTDOCS (
    OBJID type of column OBJECT.objid,
    CLID type of column OBJECT.objid,
    CLDATE R_DATE,
    DTCODES r_varchar255)
returns (
    DOCID type of column DOCUMENT.docid,
    DOCDATE type of column DOCUMENT.docdate,
    RDOCDATE type of column DOCUMENT.realdocdate,
    DOCNUM type of column DOCUMENT.number,
    DOCSUM type of column DOCUMENT.amount,
    STAT type of column R_STATUS.code,
    STATNAME type of column R_STATUS.name,
    THROUGHNAME type of R_FULLNAME,
    GATASKID type of column WM_TASK.TASKID,
    GASTAT type of column R_STATUS.code,
    GASTATNAME type of column R_STATUS.name,
    GASITENAME type of column SITE.name,
    GAAUTONAME type of column T_AUTO.name,
    GADATETIME type of column WM_TASK.plandatetime
)
AS
begin
    for
        select d.DOCID, d.DOCDATE, d.RDOCDATE, d.DOCNUM, d.DOCSUM, d.STAT, d.STATNAME, d.THROUGHNAME,
               ga.taskid, gast.code, gast.name, gas.name, gaa.name, ga.plandatetime
          from k_selmanag_listclientdocs(:objid, :clid, :cldate, :dtcodes) d
               left join wh_loadautodc_gettaskbydoc(d.docid) tbcd
                    left join wm_task ga
                         left join r_status gast on gast.statustype='T' and gast.code=ga.status
                         left join site gas on gas.siteid = ga.siteid
                         left join t_auto gaa on gaa.aid = ga.infoid
                      on ga.taskid = tbcd.tid_gateauto
                 on 1=1
          into :DOCID, :DOCDATE, :RDOCDATE, :DOCNUM, :DOCSUM, :STAT, :STATNAME, :THROUGHNAME,
               :gataskid, :gastat, :gastatname, :gasitename, :gaautoname, :gadatetime
    do
    begin
        suspend;
    end
end^

SET TERM ; ^

