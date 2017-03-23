

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
   select list(distinct g.externalcode || '->' || g.code ), count(distinct g.waresid)
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
        insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
        select t.docid, t.waresid, t.productdate, t.amount, t.objid, t.amountbad
          from wh_tmp_reserve_changes t;
   end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_DOCMANAGER_DOCTYPES (
    WMSESID R_ID)
returns (
    DOCTID integer,
    NAME varchar(80),
    DOCMANAGEREDITDISABLE char(1),
    CODE type of R_CODE,
    WSETID integer,
    FIRSTSTATUS type of R_STATUS,
    CANCREATE type of R_FLAG,
    CANEDIT type of R_FLAG,
    APPROVEDSTATUS type of R_FLAG)
AS
begin
        for
          select dt.doctid,dt.name,dt.docmanagereditdisable,dt.code,dt.wsetid,dt.firststatus,
                 md.cancreate, md.canedit, dt.approvedstatus
            from wm_session wms
                 left join man_doctype md
                      left join doctype dt on dt.doctid = md.doctid
                   on wms.objid = md.manid
           where wms.sessionid = :wmsesid
             and dt.doctid is NOT NULL
            into :doctid,:name,:docmanagereditdisable,:code,:wsetid,:firststatus,
                 :cancreate, :canedit, :approvedstatus
        do
          suspend;
end^

SET TERM ; ^

