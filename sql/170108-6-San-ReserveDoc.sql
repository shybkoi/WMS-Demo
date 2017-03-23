

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

   if (:clientid is NOT NULL) then
       insert into wh_reserve_doc_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, RDOCID)
       select t.docid, t.waresid, t.productdate, sum(t.amount), :toobj, t.docid
         from wh_tmp_reserve_changes t
        where t.objid = :fromobj
        group by t.waresid, t.productdate, t.docid
       having abs(sum(t.amount)) > 0.0001;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_DOC_RESERVE_LVL1_CANC (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable errmes type of rbs_bigvarchar;
declare variable excmes type of r_exceptionusermes;
declare variable errcnt type of r_shortnumber;
begin
    with pre as(
        select rc.objid, rc.waresid, rc.productdate, sum(rc.amount) as amount
          from wh_reserve_doc_changes rc
         where rc.docid = :docid
         group by rc.waresid, rc.productdate, rc.objid
        having sum(rc.amount) > 0.0001
    )
    select list(distinct g.externalcode || '->' || g.code ), count(distinct g.waresid)
      from pre
           left join wh_reserve r
             on r.objid = pre.objid
                and r.productdate = pre.productdate
                and r.waresid = pre.waresid
           left join gwares g on g.waresid = pre.waresid
     where pre.amount - coalesce(r.amountdoc, 0.000) > 0.0001
      into :errmes, :errcnt;

    if (:errcnt is NOT NULL and :errcnt > 0) then
    begin
        errmes = 'Невозможно обработать в нужном количестве резерв для товаров: '||:errmes;
        execute procedure WH_TEXT_TO_EXCMES(:errmes)
         returning_values :excmes;
        exception exc_wh_wrongamount :excmes;
    end

    with pre as(
        select rc.objid, rc.waresid, rc.productdate, sum(rc.amount) as amount, sum(rc.amountbad) as amountbad
          from wh_reserve_changes rc
         where rc.docid = :docid
         group by rc.waresid, rc.productdate, rc.objid
        having sum(rc.amount) > 0.0001 or sum(rc.amountbad) > 0.0001
--        having abs(sum(rc.amount)) > 0.0001 or abs(sum(rc.amountbad)) > 0.0001
    )
    select list(distinct g.externalcode || '->' || g.code ), count(distinct g.waresid)
      from pre
           left join wh_reserve r
             on r.objid = pre.objid
                and r.productdate = pre.productdate
                and r.waresid = pre.waresid
           left join gwares g on g.waresid = pre.waresid
     where pre.amount - coalesce(r.amountfree, 0.000) > 0.0001
        or pre.amountbad - coalesce(r.amountbad, 0.000) > 0.0001
      into :errmes, :errcnt;

    if (:errcnt is NOT NULL and :errcnt > 0) then
    begin
        errmes = 'Невозможно обработать в нужном количестве резерв для товаров: '||:errmes;
        execute procedure WH_TEXT_TO_EXCMES(:errmes)
         returning_values :excmes;
        exception exc_wh_wrongamount :excmes;
    end

    insert into wh_reserve_doc_changes ( OBJID, WARESID, PRODUCTDATE, RDOCID, AMOUNT, DOCID)
    select rc.objid, rc.waresid, rc.productdate, rc.rdocid, -sum(rc.amount), rc.docid
      from wh_reserve_doc_changes rc
     where rc.docid = :docid
     group by rc.waresid, rc.productdate, rc.objid, rc.rdocid, rc.docid
    having abs(sum(rc.amount)) > 0.0000001;

    insert into wh_reserve_changes ( OBJID, WARESID, PRODUCTDATE, AMOUNT, DOCID, AMOUNTBAD)
    select rc.objid, rc.waresid, rc.productdate, -sum(rc.amount), rc.docid, -sum(rc.amountbad)
      from wh_reserve_changes rc
     where rc.docid = :docid
     group by rc.waresid, rc.productdate, rc.objid, rc.docid
    having abs(sum(rc.amount)) > 0.0000001;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_IMP_TMPRESERVEDOC_PREP (
    DOCID type of column DOCUMENT.DOCID,
    RDOCID type of column DOCUMENT.DOCID,
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
declare variable suvalue type of r_double;
declare variable sunull type of r_double;
declare variable dst type of column docsubtype.code;
begin
   select coalesce(d.docsubtype,'')
     from document d
    where d.docid = :docid
     into :dst;

   for
    select ic.waresid, ic.amount
      from imp_cargo ic
     where ic.document = :docid
       and ic.amount > 0.000001
      into :waresid, :icamount
   do
   begin
        if (:dst = 'БК') then
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
                              join wh_reserve_doc rd on rd.reserveid = r.id
                        where r.objid = :objid
                          and r.waresid = :waresid
                          and r.productdate = :productdate
                          and rd.amount - :iramount > -0.0001)) then
            begin
               insert into wh_tmp_reservedoc_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, RDOCID)
               values(:docid, :waresid, :productdate, -:iramount, :objid, :rdocid);

               insert into wh_tmp_reservedoc_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, RDOCID)
               values(:docid, :waresid, :productdate, :iramount, :objid, :docid);
        
               icamount = :icamount - :iramount;
            end
            else
            begin
               icamount = 0.000;
               break;
            end
        end
        else
        begin
            select sum(ir.amount)
              from imp_reserve ir
             where ir.docid = :docid
               and ir.waresid = :waresid
              into :iramount;
    
            icamount = :icamount - coalesce(:iramount, 0.000);
        end

        if (:icamount > 0.0000001 and :dst in ('ТПП', 'СП')) then
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

                excmes = 'Товар '||:errmes||': кратности поддона и вторичной единицы измерения совпадают';
                exception exc_wh_wrongwares :excmes;
            end

            select w.dbeg
              from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
              into :saledbeg;
            
            if (:icamount > 0.00001 and :pufactor is NOT NULL and :dst in ('ТПП', 'СП')) then
            begin
                for
                    with pre as (
                            select r.productdate as productdate, r.amountfree as amount
                              from wh_reserve r
                                   join wh_reserve_doc rd on rd.reserveid = r.id
                             where r.objid = :objid
                               and r.waresid = :waresid
                               and r.productdate > :saledbeg
                               and rd.docid = :rdocid
                             union all
                            select t.productdate as productdate, t.amount as amount
                              from wh_tmp_reservedoc_changes t
                             where t.waresid = :waresid
                               and t.objid = :objid
                               and t.docid = :docid
                               and t.rdocid = :rdocid
                               and t.productdate > :saledbeg
                    )
                    select pre.productdate, sum(pre.amount)
                      from pre
                     group by pre.productdate
                    having sum(pre.amount) - :pufactor > -0.00001
                     order by pre.productdate asc
                      into :productdate, :iramount
                do
                begin
                    ramount = minvalue(:iramount, :icamount);
                    ramount = :ramount - mod(:ramount, :pufactor);
            
                    insert into wh_tmp_reservedoc_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, RDOCID)
                    values(:docid, :waresid, :productdate, -:ramount, :objid, :rdocid);

                    insert into wh_tmp_reservedoc_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, RDOCID)
                    values(:docid, :waresid, :productdate, :ramount, :objid, :docid);
            
                    icamount = :icamount - :ramount;
                    if (:icamount - :pufactor < -0.00001) then
                        break;
                end
            end

            if (:icamount > 0.00001 and :pufactor > 0.0001 and :dst = 'СП') then
            begin
                for
                    with pre as (
                            select r.productdate as productdate, r.amountfree as amount
                              from wh_reserve r
                                   join wh_reserve_doc rd on rd.reserveid = r.id
                             where r.objid = :objid
                               and r.waresid = :waresid
                               and r.productdate > :saledbeg
                               and rd.docid = :rdocid
                             union all
                            select t.productdate as productdate, t.amount as amount
                              from wh_tmp_reservedoc_changes t
                             where t.waresid = :waresid
                               and t.objid = :objid
                               and t.docid = :docid
                               and t.rdocid = :rdocid
                               and t.productdate > :saledbeg
                    )
                    select pre.productdate, mod(sum(pre.amount), :pufactor)
                      from pre
                     group by pre.productdate
                    having sum(pre.amount) - :pufactor - :suvalue > :sunull
                       and mod(sum(pre.amount), :pufactor) > 0.0001
                     order by pre.productdate asc
                      into :productdate, :iramount
                do
                begin
                   ramount = minvalue(:iramount, :icamount);
                   if (:sufactor is NOT NULL) then
                    ramount = :ramount - mod(:ramount, :sufactor);

                   insert into wh_tmp_reservedoc_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, RDOCID)
                   values(:docid, :waresid, :productdate, -:ramount, :objid, :rdocid);

                   insert into wh_tmp_reservedoc_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, RDOCID)
                   values(:docid, :waresid, :productdate, :ramount, :objid, :docid);

                   icamount = :icamount - :ramount;
        
                   if (:icamount < 0.0000001) then
                    break;
                end
            end

            if (:icamount > 0.0001 and :dst = 'ФЕ') then
            begin
                for
                    with pre as (
                            select r.productdate as productdate, r.amountfree as amount
                              from wh_reserve r
                                   join wh_reserve_doc rd on rd.reserveid = r.id
                             where r.objid = :objid
                               and r.waresid = :waresid
                               and r.productdate > :saledbeg
                               and rd.docid = :rdocid
                             union all
                            select t.productdate as productdate, t.amount as amount
                              from wh_tmp_reservedoc_changes t
                             where t.waresid = :waresid
                               and t.objid = :objid
                               and t.docid = :docid
                               and t.productdate > :saledbeg
                               and t.rdocid = :rdocid
                    )
                    select sum(pre.amount), pre.productdate
                      from pre
                     group by pre.productdate
                    having sum(pre.amount) - :suvalue > :sunull
                     order by pre.productdate ascending
                      into :iramount, :productdate
                do
                begin
                   ramount = minvalue(:iramount, :icamount);
                   if (:sufactor is NOT NULL) then
                    ramount = :ramount - mod(:ramount, :sufactor);

                   insert into wh_tmp_reservedoc_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, RDOCID)
                   values(:docid, :waresid, :productdate, -:ramount, :objid, :rdocid);

                   insert into wh_tmp_reservedoc_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, RDOCID)
                   values(:docid, :waresid, :productdate, :ramount, :objid, :docid);

                   icamount = :icamount - :ramount;

                   if (:icamount < 0.0000001) then
                    break;
                end
            end
        end
   end

   with chg1 as (
       select w.waresid as waresid, w.amount as amount
         from wh_tmp_reservedoc_changes w
        where w.docid = :docid and w.rdocid = :docid
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
declare variable RDOCID type of column DOCUMENT.docid;
begin
   select gor.objid, d.toobj, d.realdocdate, d.docbondid
     from imp_document d
          left join wh_get_reserveobj(coalesce(d.throughobj, d.fromobj)) gor on 1=1
    where d.docid = :docid
     into :objid, :clientid, :realdocdate, :rdocid;

   if (:rdocid is NULL) then
   begin
       execute procedure wh_imp_tmpreserve_prep(:docid, :objid, :clientid, :realdocdate);
    
       insert into wh_reserve_client_changes ( OBJID, WARESID, PRODUCTDATE, CLIENTID, AMOUNT, DOCID)
       select t.objid, t.waresid,  t.productdate, :clientid, sum(t.amount), t.docid
         from wh_tmp_reserve_changes t
        group by t.objid, t.waresid,  t.productdate, t.docid
       having abs(sum(t.amount)) > 0.0001;
   end
   else
   begin
       execute procedure wh_imp_tmpreservedoc_prep(:docid, :rdocid, :objid, :clientid, :realdocdate);
    
       insert into wh_reserve_doc_changes ( OBJID, WARESID, PRODUCTDATE, RDOCID, AMOUNT, DOCID)
       select t.objid, t.waresid,  t.productdate, t.rdocid, sum(t.amount), t.docid
         from wh_tmp_reservedoc_changes t
        group by t.objid, t.waresid,  t.productdate, t.docid, t.rdocid
       having abs(sum(t.amount)) > 0.0001;
   end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECT_CLIENTUNFUND (
    TASKID type of column WM_TASK.TASKID)
AS
declare variable clientid type of column OBJECT.objid;
declare variable fundobjid type of column OBJECT.objid;
declare variable docid type of column DOCUMENT.docid ;
declare variable tmid type of column wm_taskmethod.methodid;
begin
   select gor.objid, d.toobj, d.docid, t.taskmethodid
     from wm_task t
          left join document d
               left join wh_get_reserveobj(coalesce(d.throughobj, d.fromobj)) gor on 1=1
            on d.docid = t.docid
    where t.taskid = :taskid
     into :fundobjid, :clientid, :docid, :tmid;

   if (exists(select *
                 from wh_reserve_doc rd
                where rd.docid = :docid)) then
       insert into wh_reserve_doc_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, RDOCID)
       select :docid, tw.waresid, tw.plandatetime, -tw.quantity, :fundobjid, :docid
         from wm_task_wares tw
        where tw.taskid = :taskid;
   else
       insert into wh_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
       select :docid, tw.waresid, tw.plandatetime, -tw.quantity, :fundobjid, :clientid
         from wm_task_wares tw
        where tw.taskid = :taskid;

   if (:tmid is NOT NULL) then
       insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, TASKID)
       select :docid, tw.waresid, tw.plandatetime, -tw.scanquant, :fundobjid, :taskid
         from wm_task_wares tw
        where tw.taskid = :taskid
          and coalesce(tw.scanquant, 0.000) > 0.0001;
end^

SET TERM ; ^

