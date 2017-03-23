

SET TERM ^ ;

create or alter procedure K_U3S_WRITEOFF_STATUSCHG (
    DOCID type of R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable taskid type of r_id;
declare variable doctid type of r_id;
declare variable ttinitst type of r_status;
declare variable waresid type of r_id;
declare variable amount type of r_double;
declare variable docsum type of r_double;
declare variable ttid_docfreesel type of r_id;
declare variable tmid_docfreesel type of r_id;
begin
    select d.doctype
      from document d
     where d.docid = :docid
      into :doctid;

    if (:newstat = 'g') then
    begin
        execute procedure wh_ttid_docfreesel returning_values :ttid_docfreesel;
        execute procedure wh_tmid_get(:ttid_docfreesel,'W') returning_values :tmid_docfreesel;
        execute procedure wh_get_taskinitstatus(:ttid_docfreesel,:tmid_docfreesel) returning_values :ttinitst;

        select first(1) t.taskid
          from wm_task t
         where t.docid = :docid and t.tasktypeid = :ttid_docfreesel
          into :taskid;


        if (:taskid is NULL) then
        begin
            INSERT INTO wm_task(tasktypeid,status,docid,wm_sessionid,taskmethodid)
            VALUES(:ttid_docfreesel,:ttinitst,:docid,null,:tmid_docfreesel)
            returning taskid
            into :taskid;
        end
        else
        begin
            update wm_task t
               set t.taskmethodid = :tmid_docfreesel, t.wm_sessionid = NULL, t.status = :ttinitst
              where t.taskid = :taskid;
        end

        -- ≈сли повышение статуса
        if (exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.upcodes containing :newstat )) then
        begin
            for
                select cg.waresid,cg.amount,cg.docsum
                  from cargo cg
                 where cg.document = :docid
                   and cg.amount > 0.00001
                  into :waresid,:amount,:docsum
            do
                update or insert into wm_task_wares(taskid, waresid, successscan, summa, status, endtime)
                values (:taskid, :waresid, :amount, :docsum, '0', NULL)
                matching (taskid, waresid);
        end

        update wm_task_wares tw
           set tw.status = '0'
         where tw.taskid = :taskid
           and abs(coalesce(tw.successscan,0.0000)-coalesce(tw.quantity,0.00000)) > 0.000001
           and tw.status <> '0';

        update cargo cg
           set cg.amount = 0,cg.docsum = 0
         where cg.document = :docid and abs(cg.amount)>0.000001;
    end
    else if (:newstat = '2') then
    begin
        execute procedure wh_ttid_docfreesel returning_values :ttid_docfreesel;
        execute procedure wh_tmid_get(:ttid_docfreesel,'W') returning_values :tmid_docfreesel;

        select first(1) t.taskid
          from wm_task t
         where t.docid = :docid and t.tasktypeid = :ttid_docfreesel and t.taskmethodid = :tmid_docfreesel and t.status = '2'
          into :taskid;

        if (:taskid is NULL) then exception exc_wh_tasknotfound;
        else execute procedure wh_core_setdocbytask(:docid,:ttid_docfreesel);

        execute procedure RBS_Q_CREATETASKEXPORT('»зменение статуса документа: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
         returning_values :taskid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_TASKINFO (
    TASKID type of column WM_TASK.taskid )
returns (
    TID type of column WM_TASK.taskid,
    TSTAT type of column R_STATUS.code,
    SITEID type of column SITE.siteid,
    SNAME type of column SITE.name,
    DOCID type of column DOCUMENT.docid,
    DOCNUM type of column DOCUMENT.number,
    DOCDATE type of R_DATE,
    DOCSTAT type of column R_STATUS.code,
    ALGORITHM type of column wm_taskmethod.algorithm,
    FROMID type of column OBJECT.objid,
    FROMNAME type of R_FULLNAME,
    THROUGHID type of column OBJECT.objid,
    THROUGHNAME type of R_FULLNAME,
    TOID type of column OBJECT.objid,
    TONAME type of R_FULLNAME,
    INFOID type of column WM_TASK.infoid,
    INFOTYPECODE type of column wh_taskinfotype.code,
    INFONAME varchar(1023),
    PLANDT type of column WM_TASK.plandatetime)
AS
begin
    select t.taskid,t.siteid, t.status,
           d.docid,d.docdate,d.number,d.status,tm.algorithm,
           d.fromobj,(select fullname from getobjectname(d.fromobj,NULL)),
           d.throughobj,(select fullname from getobjectname(d.throughobj,NULL)),
           d.toobj,(select fullname from getobjectname(d.toobj,NULL)),
           t.infoid,s.name,tit.code,t.plandatetime,ig.info
      from wm_task t
           left join wm_taskmethod tm on tm.methodid=t.taskmethodid
           left join document d on d.docid=t.docid
           left join site s on s.siteid = t.siteid
           left join wh_taskinfotype tit on tit.id = t.typeinfoid
           left join wh_id_getinfo(t.infoid,t.typeinfoid) ig on 1=1
     where t.taskid = :taskid
      into :tid,:siteid,:tstat,
           :docid,:docdate,:docnum,:docstat,:algorithm,
           :fromid, :fromname,
           :throughid, :throughname,
           :toid, :toname,
           :infoid,:sname,:infotypecode,:plandt,:infoname;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_DOCFREESEL_LISTTASKES (
    WMSESID type of column WM_SESSION.sessionid )
returns (
    DOCID type of column DOCUMENT.docid,
    FROMID type of column OBJECT.objid,
    FROMNAME type of R_FULLNAME,
    THROUGHID type of column OBJECT.objid,
    THROUGHNAME type of R_FULLNAME,
    TOID type of column OBJECT.objid,
    TONAME type of R_FULLNAME,
    DOCDATE type of R_DATE,
    DOCNUM type of column DOCUMENT.number,
    TASKID type of column WM_TASK.taskid,
    TMID type of column wm_taskmethod.methodid,
    TTID type of column WM_TASKTYPE.tasktypeid,
    TMALGO type of column wm_taskmethod.algorithm,
    TSTAT type of column R_STATUS.code)
AS
declare variable whid r_id;
begin
    execute procedure wh_ttid_docfreesel returning_values :ttid;

    select k.objid
      from k_wh_sessionzoneobj(:wmsesid) k
      into :whid;

    for
        select d.fromobj,(select fullname from getobjectname(d.fromobj,NULL)),
               d.throughobj,(select fullname from getobjectname(d.throughobj,NULL)),
               d.toobj,(select fullname from getobjectname(d.toobj,NULL)),
               d.docid,d.docdate,d.number,t.taskid,t.status,t.taskmethodid,tm.algorithm
          from wm_task t
               left join wm_taskmethod tm on tm.methodid = t.taskmethodid
               left join document d on d.docid = t.docid
         where t.tasktypeid = :ttid
           and t.wm_sessionid = :wmsesid
           and t.status = '1'
           and d.fromobj = :whid
          into :fromid,:fromname,
               :throughid,:throughname,
               :toid,:toname,
               :docid,:docdate,:docnum,:taskid,:tstat,:tmid,:tmalgo
    do
        suspend;

    if (:taskid is NULL) then
    for
        select d.fromobj,(select fullname from getobjectname(d.fromobj,NULL)),
               d.throughobj,(select fullname from getobjectname(d.throughobj,NULL)),
               d.toobj,(select fullname from getobjectname(d.toobj,NULL)),
               d.docid,d.docdate,d.number,t.taskid,t.status,t.taskmethodid,tm.algorithm
          from wm_task t
               left join wm_taskmethod tm on tm.methodid = t.taskmethodid
               left join document d on d.docid = t.docid
         where t.tasktypeid = :ttid
           and t.wm_sessionid is NULL
           and t.status = '0'
           and d.fromobj = :whid
          into :fromid,:fromname,
               :throughid,:throughname,
               :toid,:toname,
               :docid,:docdate,:docnum,:taskid,:tstat,:tmid,:tmalgo
    do
        suspend;

end^

SET TERM ; ^



CREATE GLOBAL TEMPORARY TABLE WH_TMP_RESERVE_CHANGES (
    DOCID R_ID64,
    WARESID R_ID NOT NULL,
    PRODUCTDATE R_DATE NOT NULL,
    AMOUNT R_DOUBLE,
    OBJID R_ID NOT NULL,
    AMOUNTBAD R_DOUBLE) ON COMMIT DELETE ROWS;



CREATE DOMAIN R_EXCEPTIONUSERMES AS
VARCHAR(1021);

SET TERM ^ ;

create procedure WH_TEXT_TO_EXCMES (
    STR type of rbs_bigvarchar
)
returns (
    excmes type of r_exceptionusermes
)
as
begin
    if (char_length(:str)>1021) then
    begin
        excmes = substring(:str from 1 for 1018) || '...';
    end
    else
    begin
        excmes = :str;
    end
  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDMOVING_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable fromobj type of column OBJECT.objid;
declare variable toobj type of column OBJECT.objid;
declare variable clientid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable icamount type of column IMP_CARGO.amount;
declare variable productdate type of column WARESLOT.productdate;
declare variable iramount type of column IMP_RESERVE.amount;
declare variable realdocdate type of column DOCUMENT.realdocdate;
declare variable saledbeg type of R_DATE;
declare variable errmes type of rbs_bigvarchar;
declare variable excmes type of r_exceptionusermes;
declare variable errcnt type of r_shortnumber;
begin
   select d.fromobj, d.toobj, d.throughobj, d.realdocdate
     from imp_document d
    where d.docid = :docid
     into :fromobj, :toobj, :clientid, :realdocdate;

   for
    select ic.waresid, ic.amount
      from imp_cargo ic
     where ic.document = :docid
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
    begin
       insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
       values(:docid, :waresid, :productdate, -:iramount, :fromobj);

       insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
       values(:docid, :waresid, :productdate, :iramount, :toobj);

       icamount = :icamount - :iramount;
    end

    if (:icamount > 0.0000001) then
    begin
        select w.dbeg
          from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
          into :saledbeg;
        
        for
            select r.amountfree, r.productdate
              from wh_reserve r
             where r.objid = :fromobj
               and r.waresid = :waresid
               and r.productdate > :saledbeg
               and r.amountfree > 0.0000001
             order by r.productdate ascending
              into :iramount, :productdate
        do
        begin
           if (:iramount - :icamount > 0.0000001) then
                iramount = :icamount;

           insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           values(:docid, :waresid, :productdate, -:iramount, :fromobj);
    
           insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           values(:docid, :waresid, :productdate, :iramount, :toobj);

           icamount = :icamount - :iramount;

           if (:icamount < 0.0000001) then
            break;
        end
    end
   end

   with chg as (
       select w.docid as docid, w.waresid as waresid, sum(w.amount) as amount
         from wh_tmp_reserve_changes w
        where w.objid = :toobj
          and w.docid = :docid
        group by w.docid, w.waresid
   )
   select list(distinct g.code), count(distinct g.waresid)
     from chg
          left join imp_cargo ic
               left join gwares g on g.waresid = ic.waresid
            on ic.document = chg.docid and ic.waresid = chg.waresid
    where abs(ic.amount - chg.amount) > 0.0001
     into :errmes, :errcnt;

   if (:errcnt is NOT NULL and :errcnt > 0) then
   begin
        errmes = 'Ќевозможно зарезервировать в нужном количестве товары: '||:excmes;
        execute procedure WH_TEXT_TO_EXCMES(:excmes)
         returning_values :excmes;
        exception exc_wh_wrongamount :excmes;
   end
   else
   begin
        insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
        select t.docid, t.waresid, t.productdate, t.amount, t.objid, t.amountbad
          from wh_tmp_reserve_changes t;
   end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDMOVING_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable queueid type of column R_QUEUE.queueid;
begin
    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');

    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    execute procedure wh_imp_fundmoving_reserve_do(:docid);

    select d.queueid
      from imp_document d
     where d.docid = :docid
      into :queueid;
    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');

    execute procedure RBS_Q_CREATETASKEXPORT('–езультат перемещени€ резерва',:docid,NULL,NULL)
      returning_values :queueid;

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDMOVING_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable fromobj type of column OBJECT.objid;
declare variable toobj type of column OBJECT.objid;
declare variable clientid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable icamount type of column IMP_CARGO.amount;
declare variable productdate type of column WARESLOT.productdate;
declare variable iramount type of column IMP_RESERVE.amount;
declare variable realdocdate type of column DOCUMENT.realdocdate;
declare variable saledbeg type of R_DATE;
declare variable errmes type of rbs_bigvarchar;
declare variable excmes type of r_exceptionusermes;
declare variable errcnt type of r_shortnumber;
begin
   select d.fromobj, d.toobj, d.throughobj, d.realdocdate
     from imp_document d
    where d.docid = :docid
     into :fromobj, :toobj, :clientid, :realdocdate;

   for
    select ic.waresid, ic.amount
      from imp_cargo ic
     where ic.document = :docid
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
                where r.objid = :fromobj
                  and r.waresid = :waresid
                  and r.productdate = :productdate
                  and r.amountfree - :iramount > -0.0001)) then
    begin
       insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
       values(:docid, :waresid, :productdate, -:iramount, :fromobj);

       insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
       values(:docid, :waresid, :productdate, :iramount, :toobj);

       icamount = :icamount - :iramount;
    end
    else
    begin
       icamount = 0.000;
       break;
    end

    if (:icamount > 0.0000001) then
    begin
        select w.dbeg
          from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
          into :saledbeg;
        
        for
            select r.amountfree, r.productdate
              from wh_reserve r
             where r.objid = :fromobj
               and r.waresid = :waresid
               and r.productdate > :saledbeg
               and r.amountfree > 0.0000001
             order by r.productdate ascending
              into :iramount, :productdate
        do
        begin
           if (:iramount - :icamount > 0.0000001) then
                iramount = :icamount;

           insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           values(:docid, :waresid, :productdate, -:iramount, :fromobj);
    
           insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           values(:docid, :waresid, :productdate, :iramount, :toobj);

           icamount = :icamount - :iramount;

           if (:icamount < 0.0000001) then
            break;
        end
    end
   end

   with chg as (
       select w.docid as docid, w.waresid as waresid, sum(w.amount) as amount
         from wh_tmp_reserve_changes w
        where w.objid = :toobj
          and w.docid = :docid
        group by w.docid, w.waresid
   )
   select list(distinct g.code), count(distinct g.waresid)
     from chg
          left join imp_cargo ic
               left join gwares g on g.waresid = ic.waresid
            on ic.document = chg.docid and ic.waresid = chg.waresid
    where abs(ic.amount - chg.amount) > 0.0001
     into :errmes, :errcnt;

   if (:errcnt is NOT NULL and :errcnt > 0) then
   begin
        errmes = 'Ќевозможно зарезервировать в нужном количестве товары: '||:excmes;
        execute procedure WH_TEXT_TO_EXCMES(:excmes)
         returning_values :excmes;
        exception exc_wh_wrongamount :excmes;
   end
   else
   begin
        insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
        select t.docid, t.waresid, t.productdate, t.amount, t.objid, t.amountbad
          from wh_tmp_reserve_changes t;
   end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDMOVING_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable fromobj type of column OBJECT.objid;
declare variable toobj type of column OBJECT.objid;
declare variable clientid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable icamount type of column IMP_CARGO.amount;
declare variable productdate type of column WARESLOT.productdate;
declare variable iramount type of column IMP_RESERVE.amount;
declare variable realdocdate type of column DOCUMENT.realdocdate;
declare variable saledbeg type of R_DATE;
declare variable errmes type of rbs_bigvarchar;
declare variable excmes type of r_exceptionusermes;
declare variable errcnt type of r_shortnumber;
begin
   select d.fromobj, d.toobj, d.throughobj, d.realdocdate
     from imp_document d
    where d.docid = :docid
     into :fromobj, :toobj, :clientid, :realdocdate;

   for
    select ic.waresid, ic.amount
      from imp_cargo ic
     where ic.document = :docid
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
                where r.objid = :fromobj
                  and r.waresid = :waresid
                  and r.productdate = :productdate
                  and r.amountfree - :iramount > -0.0001)) then
    begin
       insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
       values(:docid, :waresid, :productdate, -:iramount, :fromobj);

       insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
       values(:docid, :waresid, :productdate, :iramount, :toobj);

       icamount = :icamount - :iramount;
    end
    else
    begin
       icamount = 0.000;
       break;
    end

    if (:icamount > 0.0000001) then
    begin
        select w.dbeg
          from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
          into :saledbeg;
        
        for
            select r.amountfree, r.productdate
              from wh_reserve r
             where r.objid = :fromobj
               and r.waresid = :waresid
               and r.productdate > :saledbeg
               and r.amountfree > 0.0000001
             order by r.productdate ascending
              into :iramount, :productdate
        do
        begin
           if (:iramount - :icamount > 0.0000001) then
                iramount = :icamount;

           insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           values(:docid, :waresid, :productdate, -:iramount, :fromobj);
    
           insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           values(:docid, :waresid, :productdate, :iramount, :toobj);

           icamount = :icamount - :iramount;

           if (:icamount < 0.0000001) then
            break;
        end
    end
   end

   with chg as (
       select w.docid as docid, w.waresid as waresid, sum(w.amount) as amount
         from wh_tmp_reserve_changes w
        where w.objid = :toobj
          and w.docid = :docid
        group by w.docid, w.waresid
   )
   select list(distinct g.code), count(distinct g.waresid)
     from chg
          left join imp_cargo ic
               left join gwares g on g.waresid = ic.waresid
            on ic.document = chg.docid and ic.waresid = chg.waresid
    where abs(ic.amount - chg.amount) > 0.0001
     into :errmes, :errcnt;

   if (:errcnt is NOT NULL and :errcnt > 0) then
   begin
        errmes = 'Ќевозможно зарезервировать в нужном количестве товары: '||:excmes;
        execute procedure WH_TEXT_TO_EXCMES(:errmes)
         returning_values :excmes;
        exception exc_wh_wrongamount :excmes;
   end
   else
   begin
        insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
        select t.docid, t.waresid, t.productdate, t.amount, t.objid, t.amountbad
          from wh_tmp_reserve_changes t;
   end
end^

SET TERM ; ^



CREATE GLOBAL TEMPORARY TABLE WH_TMP_RESERVE_CLIENT_CHANGES (
    OBJID R_ID NOT NULL,
    WARESID R_ID NOT NULL,
    PRODUCTDATE R_DATE NOT NULL,
    CLIENTID R_ID NOT NULL,
    AMOUNT R_DOUBLE NOT NULL,
    DOCID R_ID64) ON COMMIT DELETE ROWS;



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDSALE_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable objid type of column OBJECT.objid;
declare variable clientid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable icamount type of column IMP_CARGO.amount;
declare variable productdate type of column WARESLOT.productdate;
declare variable iramount type of column IMP_RESERVE.amount;
declare variable realdocdate type of column DOCUMENT.realdocdate;
declare variable saledbeg type of R_DATE;
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
            select w.dbeg
              from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
              into :saledbeg;
            
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
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDMOVING_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable fromobj type of column OBJECT.objid;
declare variable toobj type of column OBJECT.objid;
declare variable clientid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable icamount type of column IMP_CARGO.amount;
declare variable productdate type of column WARESLOT.productdate;
declare variable iramount type of column IMP_RESERVE.amount;
declare variable realdocdate type of column DOCUMENT.realdocdate;
declare variable saledbeg type of R_DATE;
declare variable errmes type of rbs_bigvarchar;
declare variable excmes type of r_exceptionusermes;
declare variable errcnt type of r_shortnumber;
begin
   select d.fromobj, d.toobj, d.throughobj, d.realdocdate
     from imp_document d
    where d.docid = :docid
     into :fromobj, :toobj, :clientid, :realdocdate;

   for
    select ic.waresid, ic.amount
      from imp_cargo ic
     where ic.document = :docid
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
                where r.objid = :fromobj
                  and r.waresid = :waresid
                  and r.productdate = :productdate
                  and r.amountfree - :iramount > -0.0001)) then
    begin
       insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
       values(:docid, :waresid, :productdate, -:iramount, :fromobj);

       insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
       values(:docid, :waresid, :productdate, :iramount, :toobj);

       icamount = :icamount - :iramount;
    end
    else
    begin
       icamount = 0.000;
       break;
    end

    if (:icamount > 0.0000001) then
    begin
        select w.dbeg
          from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
          into :saledbeg;
        
        for
            select r.amountfree, r.productdate
              from wh_reserve r
             where r.objid = :fromobj
               and r.waresid = :waresid
               and r.productdate > :saledbeg
               and r.amountfree > 0.0000001
             order by r.productdate ascending
              into :iramount, :productdate
        do
        begin
           if (:iramount - :icamount > 0.0000001) then
                iramount = :icamount;

           insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           values(:docid, :waresid, :productdate, -:iramount, :fromobj);
    
           insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           values(:docid, :waresid, :productdate, :iramount, :toobj);

           icamount = :icamount - :iramount;

           if (:icamount < 0.0000001) then
            break;
        end
    end
   end

   with chg1 as (
       select w.waresid as waresid, w.amount as amount
         from wh_tmp_reserve_changes w
        where w.objid = :toobj
          and w.docid = :docid
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
   select list(distinct g.code), count(distinct g.waresid)
     from chg2
          left join gwares g on g.waresid = chg2.waresid
     into :errmes, :errcnt;

   if (:errcnt is NOT NULL and :errcnt > 0) then
   begin
        errmes = 'Ќевозможно зарезервировать в нужном количестве товары: '||:excmes;
        execute procedure WH_TEXT_TO_EXCMES(:errmes)
         returning_values :excmes;
        exception exc_wh_wrongamount :excmes;
   end
   else
   begin
        insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
        select t.docid, t.waresid, t.productdate, t.amount, t.objid, t.amountbad
          from wh_tmp_reserve_changes t;
   end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDSALE_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable objid type of column OBJECT.objid;
declare variable clientid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable icamount type of column IMP_CARGO.amount;
declare variable productdate type of column WARESLOT.productdate;
declare variable iramount type of column IMP_RESERVE.amount;
declare variable realdocdate type of column DOCUMENT.realdocdate;
declare variable saledbeg type of R_DATE;
declare variable errmes type of rbs_bigvarchar;
declare variable excmes type of r_exceptionusermes;
declare variable errcnt type of r_shortnumber;
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
            select w.dbeg
              from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
              into :saledbeg;
            
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
   select list(distinct g.code), count(distinct g.waresid)
     from chg2
          left join gwares g on g.waresid = chg2.waresid
     into :errmes, :errcnt;

   if (:errcnt is NOT NULL and :errcnt > 0) then
   begin
        errmes = 'Ќевозможно зарезервировать в нужном количестве товары: '||:excmes;
        execute procedure WH_TEXT_TO_EXCMES(:errmes)
         returning_values :excmes;
        exception exc_wh_wrongamount :excmes;
   end
   else
   begin
        insert into wh_reserve_client_changes ( OBJID, WARESID, PRODUCTDATE, CLIENTID, AMOUNT, DOCID)
        select t.objid, t.waresid,  t.productdate, t.clientid, t.amount, t.docid
          from wh_reserve_client_changes t;
   end
end^

SET TERM ; ^

