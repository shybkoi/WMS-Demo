

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
   else
   begin
        insert into wh_reserve_client_changes ( OBJID, WARESID, PRODUCTDATE, CLIENTID, AMOUNT, DOCID)
        select t.objid, t.waresid,  t.productdate, t.clientid, t.amount, t.docid
          from wh_tmp_reserve_client_changes t;
   end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_IMP_FUNDINCOME_RESERVE_CANC (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable errmes type of rbs_bigvarchar;
declare variable excmes type of r_exceptionusermes;
declare variable errcnt type of r_shortnumber;
begin
    with pre as(
        select rc.objid, rc.waresid, rc.productdate, sum(rc.amount) as amount
          from wh_reserve_changes rc
         where rc.docid = :docid
         group by rc.waresid, rc.productdate, rc.objid
        having abs(sum(rc.amount)) > 0.0000001
    )
    select list(distinct g.externalcode || '->' || g.code ), count(distinct g.waresid)
      from pre
           left join wh_reserve r
                left join gwares g on g.waresid = r.waresid
             on r.objid = pre.objid
                and r.productdate = pre.productdate
                and r.waresid = pre.waresid
     where pre.amount - coalesce(r.amount, 0.000) > 0.0001
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
        insert into wh_reserve_changes ( OBJID, WARESID, PRODUCTDATE, AMOUNT, DOCID, AMOUNTBAD)
        select rc.objid, rc.waresid, rc.productdate, -sum(rc.amount), rc.docid, 0.000
          from wh_reserve_changes rc
         where rc.docid = :docid
         group by rc.waresid, rc.productdate, rc.objid, rc.docid
        having abs(sum(rc.amount)) > 0.0000001;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDINCOME_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I'
)
AS
declare variable docstat type of column document.status;
declare variable docbondid type of column document.docid;
declare variable docnum type of column document.number;
begin
    select id.docbondid, id.number
      from imp_document id
     where id.docid = :docid
      into :docbondid, :docnum;

    if (:docbondid is NOT NULL) then
    begin
        update imp_document id
           set id.docid = :docbondid
         where id.docid = :docid;

        docid = :docbondid;
    end

    select d.status
      from document d
     where d.docid = :docid
      into :docstat;

    if (:actioncode = 'I') then
    begin
        if (:docstat = 'w') then
        begin
            execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid);
            execute procedure WH_IMP_CARGO_CHK(:docid);
    
            execute procedure wh_imp_fundincome_reserve_do(:docid);
    
            update document d
               set d.status = 'e', d.number = :docnum
             where d.docid = :docid;
    
            delete from imp_document id
             where id.docid = :docid;
        end
        else
        begin
            exception exc_wh_wrongdocstat;
        end
    end
    else if (:actioncode = 'D') then
    begin
        if (:docstat = 'e') then
        begin
            execute procedure WH_IMP_FUNDINCOME_RESERVE_CANC(:docid);

            update document d
               set d.status = 'w', d.number = :docnum
             where d.docid = :docid;
    
            delete from imp_document id
             where id.docid = :docid;
        end
        else
        begin
            exception exc_wh_wrongdocstat;
        end
    end
    else
    begin
        exception exc_wh_wrongdocstat 'wrong ACTIONCODE';
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_DOC_RESERVE_LVL1_CANC (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable errmes type of rbs_bigvarchar;
declare variable excmes type of r_exceptionusermes;
declare variable errcnt type of r_shortnumber;
begin
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
                left join gwares g on g.waresid = r.waresid
             on r.objid = pre.objid
                and r.productdate = pre.productdate
                and r.waresid = pre.waresid
     where pre.amount - coalesce(r.amountfree, 0.000) > 0.0001
        or pre.amountbad - coalesce(r.amountbad, 0.000) > 0.0001
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
        insert into wh_reserve_changes ( OBJID, WARESID, PRODUCTDATE, AMOUNT, DOCID, AMOUNTBAD)
        select rc.objid, rc.waresid, rc.productdate, -sum(rc.amount), rc.docid, -sum(rc.amountbad)
          from wh_reserve_changes rc
         where rc.docid = :docid
         group by rc.waresid, rc.productdate, rc.objid, rc.docid
        having abs(sum(rc.amount)) > 0.0000001;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDINCOME_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I'
)
AS
declare variable docstat type of column document.status;
declare variable docbondid type of column document.docid;
declare variable docnum type of column document.number;
begin
    select id.docbondid, id.number
      from imp_document id
     where id.docid = :docid
      into :docbondid, :docnum;

    if (:docbondid is NOT NULL) then
    begin
        update imp_document id
           set id.docid = :docbondid
         where id.docid = :docid;

        docid = :docbondid;
    end

    select d.status
      from document d
     where d.docid = :docid
      into :docstat;

    if (:actioncode = 'I') then
    begin
        if (:docstat = 'w') then
        begin
            execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid);
            execute procedure WH_IMP_CARGO_CHK(:docid);
    
            execute procedure wh_imp_fundincome_reserve_do(:docid);
    
            update document d
               set d.status = 'e', d.number = :docnum
             where d.docid = :docid;
    
            delete from imp_document id
             where id.docid = :docid;
        end
        else
        begin
            exception exc_wh_wrongdocstat;
        end
    end
    else if (:actioncode = 'D') then
    begin
        if (:docstat = 'e') then
        begin
            execute procedure WH_DOC_RESERVE_LVL1_CANC(:docid);

            update document d
               set d.status = 'w', d.number = :docnum
             where d.docid = :docid;
    
            delete from imp_document id
             where id.docid = :docid;
        end
        else
        begin
            exception exc_wh_wrongdocstat;
        end
    end
    else
    begin
        exception exc_wh_wrongdocstat 'wrong ACTIONCODE';
    end
end^

SET TERM ; ^



DROP PROCEDURE WH_IMP_FUNDINCOME_RESERVE_CANC;



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDMOVING_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I'
)
AS
declare variable queueid type of column R_QUEUE.queueid;
begin
    if (:actioncode = 'I') then
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
    end
    else if (:actioncode = 'D') then
    begin
        execute procedure WH_DOC_RESERVE_LVL1_CANC(:docid);

        delete from cargo cg
         where cg.document = :docid;

        update document d
           set d.status = '”'
         where d.docid = :docid;

        delete from imp_document id
         where id.docid = :docid;
    end

end^

SET TERM ; ^

