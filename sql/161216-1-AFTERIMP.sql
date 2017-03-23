


SET TERM ^ ;

create or alter procedure WH_IMP_TMPRESERVE_OBJWARDATESUM (
    WARESID type of column GWARES.waresid,
    OBJID type of column OBJECT.objid,
    PRODUCTDATE type of R_DATE)
returns (
    AMOUNT type of column wh_tmp_reserve_changes.amount)
AS
begin
    select sum (t.amount)
      from wh_tmp_reserve_changes t
     where t.waresid = :waresid
       and t.objid = :objid
       and t.productdate = :productdate
      into :amount;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_IMP_TMPRESERVE_PREP (
    DOCID type of column DOCUMENT.docid,
    OBJID type of column OBJECT.objid,
    CLIENTID type of column OBJECT.objid,
    REALDOCDATE type of R_DATE
)
as
declare variable WARESID type of column GWARES.WARESID;
declare variable ICAMOUNT type of column IMP_CARGO.AMOUNT;
declare variable PRODUCTDATE type of column WARESLOT.PRODUCTDATE;
declare variable IRAMOUNT type of column IMP_RESERVE.AMOUNT;
declare variable SALEDBEG type of R_DATE;
declare variable ERRMES type of RBS_BIGVARCHAR;
declare variable EXCMES type of R_EXCEPTIONUSERMES;
declare variable ERRCNT type of R_SHORTNUMBER;
declare variable PUFACTOR type of column WARESUNIT.FACTOR;
declare variable RAMOUNT type of column IMP_RESERVE.AMOUNT;
declare variable FLAG type of R_FLAG;
begin
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
           insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           values(:docid, :waresid, :productdate, :iramount, :objid);
    
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
                               left join WH_IMP_TMPRESERVE_OBJWARDATESUM(r.waresid, r.objid, r.productdate) t on 1=1
                         where r.objid = :objid
                           and r.waresid = :waresid
                           and r.productdate > :saledbeg
--                           and r.amountfree - :pufactor > -0.0001
                           and r.amountfree - coalesce(t.amount, 0) - :pufactor > -0.0001
                         order by r.productdate ascending
                          into :iramount, :productdate;
                        
                        if (:iramount is NOT NULL and :iramount > 0.00001) then
                        begin
                            ramount = minvalue(:iramount, :icamount);
                            ramount = :ramount - mod(:ramount, :pufactor);

                            insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
                            values(:docid, :waresid, :productdate, :ramount, :objid);
    
                            icamount = :icamount - :ramount;
                        end
                        else
                        begin
                            flag = '1';
                        end
                    end
                    else
                    begin
                        for
                            select mod(r.amountfree - coalesce(t.amount, 0.000), :pufactor), r.productdate
                              from wh_reserve r
                                   left join wh_imp_tmpreserve_objwardatesum(r.waresid, r.objid, r.productdate) t on 1=1
                             where r.objid = :objid
                               and r.waresid = :waresid
                               and r.productdate > :saledbeg
                               and r.amountfree > 0.0000001
                               and mod(r.amountfree - coalesce(t.amount, 0.000), :pufactor) > 0.0001
                             order by r.productdate ascending
                              into :iramount, :productdate
                        do
                        begin
                           if (:iramount - :icamount > 0.0000001) then
                                iramount = :icamount;
                
                           insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
                           values(:docid, :waresid, :productdate, :iramount, :objid);
                    
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

            /*if (:icamount > 0.0001) then
            begin
                for
                    select r.amountfree - coalesce(t.amount, 0.000), r.productdate
                      from wh_reserve r
                           left join WH_IMP_TMPRESERVE_OBJWARDATESUM(r.waresid, r.objid, r.productdate) t on 1=1
                     where r.objid = :objid
                       and r.waresid = :waresid
                       and r.productdate > :saledbeg
                       and r.amountfree - coalesce(t.amount, 0.000) > 0.0000001
                     order by r.productdate ascending
                      into :iramount, :productdate
                do
                begin
                   if (:iramount - :icamount > 0.0000001) then
                        iramount = :icamount;
        
                   insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
                   values(:docid, :waresid, :productdate, :iramount, :objid);
            
                   icamount = :icamount - :iramount;
        
                   if (:icamount < 0.0000001) then
                    break;
                end
            end*/
        end
   end

   with chg1 as (
       select w.waresid as waresid, w.amount as amount
         from wh_tmp_reserve_changes w
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
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDSALE_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable OBJID type of column OBJECT.OBJID;
declare variable CLIENTID type of column OBJECT.OBJID;
declare variable REALDOCDATE type of column DOCUMENT.REALDOCDATE;
begin
   select gor.objid, d.toobj, d.realdocdate
     from imp_document d
          left join wh_get_reserveobj(coalesce(d.throughobj, d.fromobj)) gor on 1=1
    where d.docid = :docid
     into :objid, :clientid, :realdocdate;

   execute procedure wh_imp_tmpreserve_prep(:docid, :objid, :clientid, :realdocdate);

   insert into wh_reserve_client_changes ( OBJID, WARESID, PRODUCTDATE, CLIENTID, AMOUNT, DOCID)
   select t.objid, t.waresid,  t.productdate, :clientid, sum(t.amount), t.docid
     from wh_tmp_reserve_changes t
    group by t.objid, t.waresid,  t.productdate, t.docid
   having abs(sum(t.amount)) > 0.0001;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDMOVING_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable fromobj type of column OBJECT.objid;
declare variable toobj type of column OBJECT.objid;
declare variable clientid type of column OBJECT.objid;
declare variable realdocdate type of column DOCUMENT.realdocdate;
begin
   select d.fromobj, d.toobj, d.throughobj, d.realdocdate
     from imp_document d
    where d.docid = :docid
     into :fromobj, :toobj, :clientid, :realdocdate;

   execute procedure wh_imp_tmpreserve_prep(:docid, :fromobj, :clientid, :realdocdate);

   insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
   select t.docid, t.waresid, t.productdate, -sum(t.amount), :fromobj, - sum(t.amountbad)
     from wh_tmp_reserve_changes t
    where t.objid = :fromobj
    group by t.waresid, t.productdate, t.docid
   having abs(sum(t.amount)) > 0.0001;

   insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
   select t.docid, t.waresid, t.productdate, sum(t.amount), :toobj, sum(t.amountbad)
     from wh_tmp_reserve_changes t
    where t.objid = :fromobj
    group by t.waresid, t.productdate, t.docid
   having abs(sum(t.amount)) > 0.0001;
end^

SET TERM ; ^



DROP PROCEDURE WH_IMP_FUNDSALE_RESERVE_DO_TMP;



DROP PROCEDURE WH_IMP_FUNDSALE_RESERVE_DO_V1;



DROP TABLE WH_TMP_RESERVE_CLIENT_CHANGES;


