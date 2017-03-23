

SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_TMPRESERVE_PREP (
    DOCID type of column DOCUMENT.DOCID,
    OBJID type of column OBJECT.OBJID,
    CLIENTID type of column OBJECT.OBJID,
    REALDOCDATE type of R_DATE)
AS
declare variable WARESID type of column GWARES.WARESID;
declare variable ICAMOUNT type of column IMP_CARGO.AMOUNT;
declare variable PRODUCTDATE type of column WARESLOT.PRODUCTDATE;
declare variable IRAMOUNT type of column IMP_RESERVE.AMOUNT;
declare variable SALEDBEG type of R_DATE;
declare variable ERRMES type of RBS_BIGVARCHAR;
declare variable EXCMES type of R_EXCEPTIONUSERMES;
declare variable ERRCNT type of R_SHORTNUMBER;
declare variable PUFACTOR type of column WARESUNIT.FACTOR;
declare variable SUFACTOR type of column WARESUNIT.FACTOR;
declare variable RAMOUNT type of column IMP_RESERVE.AMOUNT;
declare variable FLAG type of R_FLAG;
declare variable suvalue type of r_double;
declare variable sunull type of r_double;
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

            sufactor = NULL;
            select w.W_SUFACTOR
              from wh_wares_getsecondunit(:waresid) w
              into :sufactor;
            if (:sufactor < 0.0001) then
                sufactor = NULL;

            if (:sufactor is NULL) then
            begin
                suvalue = 0;
                sunull = 0.00001;
            end
            else
            begin
                suvalue = :sufactor;
                sunull = -0.00001;
            end

            if (:pufactor is NOT NULL and :sufactor is NOT NULL and abs(:pufactor - :sufactor) < 0.0001) then
            begin
                select g.externalcode || '->' || g.code
                  from gwares g
                 where g.waresid = :waresid
                  into :errmes;

                excmes = '“овар '||:errmes||': кратности поддона и вторичной единицы измерени€ совпадают';
                exception exc_wh_wrongwares :excmes;
            end

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
                               and r.amountfree - coalesce(t.amount, 0.000) - :suvalue > :sunull
                               and mod(r.amountfree - coalesce(t.amount, 0.000), :sufactor) > 0.0001
                             order by r.productdate ascending
                              into :iramount, :productdate
                        do
                        begin
                           ramount = minvalue(:iramount, :icamount);
                           if (:sufactor is NOT NULL) then
                            ramount = :ramount - mod(:ramount, :sufactor);

                           insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
                           values(:docid, :waresid, :productdate, :ramount, :objid);
    
                           icamount = :icamount - :ramount;
                
                           if (:icamount < 0.0000001) then
                            break;
                        end
                        flag = '1';
                    end

                    --if (:icamount < 0.0001) then
                    --  flag = 1;
                end
            end

            if (:icamount > 0.0001) then
            begin
                for
                    select r.amountfree - coalesce(t.amount, 0.000), r.productdate
                      from wh_reserve r
                           left join WH_IMP_TMPRESERVE_OBJWARDATESUM(r.waresid, r.objid, r.productdate) t on 1=1
                     where r.objid = :objid
                       and r.waresid = :waresid
                       and r.productdate > :saledbeg
                       and r.amountfree - coalesce(t.amount, 0.000) - :suvalue > :sunull
                     order by r.productdate ascending
                      into :iramount, :productdate
                do
                begin
                   ramount = minvalue(:iramount, :icamount);
                   if (:sufactor is NOT NULL) then
                    ramount = :ramount - mod(:ramount, :sufactor);

                   insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
                   values(:docid, :waresid, :productdate, :ramount, :objid);

                   icamount = :icamount - :ramount;

                   if (:icamount < 0.0000001) then
                    break;
                end
            end
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
        errmes = 'Ќевозможно зарезервировать в нужном количестве товары: '||:errmes;
        execute procedure WH_TEXT_TO_EXCMES(:errmes)
         returning_values :excmes;
        exception exc_wh_wrongamount :excmes;
   end
end^

SET TERM ; ^

