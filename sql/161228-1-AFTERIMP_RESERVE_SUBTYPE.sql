

SET TERM ^ ;

create procedure WH_IMP_TMPRESERVE_PREP_IR (
    DOCID type of column DOCUMENT.docid,
    OBJID type of column OBJECT.objid,
    WARESID type of column GWARES.waresid,
    AMOUNT type of column IMP_CARGO.amount,
    FLAG type of R_FLAG
)
returns (
    NEWAMOUNT type of column IMP_CARGO.amount
)
as
declare variable IRAMOUNT type of column imp_reserve.amount;
declare variable productdate type of column imp_reserve.productdate;
begin
    if (:flag is not NULL and :flag = 'C') then
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
                          left join WH_IMP_TMPRESERVE_OBJWARDATESUM(r.waresid, r.objid, r.productdate) t on 1=1
                    where r.objid = :objid
                      and r.waresid = :waresid
                      and r.productdate = :productdate
                      and r.amountfree - coalesce(t.amount, 0.000) - :iramount > -0.0001)) then
        begin
           insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           values(:docid, :waresid, :productdate, :iramount, :objid);
    
           amount = :amount - :iramount;
        end
        else
        begin
           amount = 0.000;
           break;
        end
        newamount = :amount;
    end
    else
    begin
        select sum(ir.amount)
          from imp_reserve ir
         where ir.docid = :docid
           and ir.waresid = :waresid
          into :iramount;

        newamount = :amount - coalesce(:iramount, 0.000);
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_IMP_TMPRESERVE_PREP_FP (
    DOCID type of column DOCUMENT.DOCID,
    OBJID type of column OBJECT.OBJID,
    WARESID type of column GWARES.WARESID,
    AMOUNT type of column IMP_CARGO.AMOUNT,
    saledbeg type of column WH_RESERVE.productdate,
    PUFACTOR type of column WARESUNIT.factor
)
returns (
    NEWAMOUNT type of column IMP_CARGO.AMOUNT)
AS
declare variable productdate type of column wh_reserve.productdate;
declare variable iramount type of column wh_reserve.amount;
declare variable ramount type of column wh_reserve.amount;
begin
    for
        with pre as (
                select r.productdate as productdate, r.amountfree as amount
                  from wh_reserve r
                 where r.objid = :objid
                   and r.waresid = :waresid
                   and r.productdate > :saledbeg
                 union all
                select t.productdate as productdate, -t.amount as amount
                  from wh_tmp_reserve_changes t
                 where t.waresid = :waresid
                   and t.objid = :objid
                   and t.docid = :docid
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
        ramount = minvalue(:iramount, :amount);
        ramount = :ramount - mod(:ramount, :pufactor);

        insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
        values(:docid, :waresid, :productdate, :ramount, :objid);

        amount = :amount - :ramount;
    end

    newamount = :amount;
    suspend;
end^

SET TERM ; ^



DROP PROCEDURE WH_IMP_TMPRESERVE_PREP_FP;



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_TMPRESERVE_PREP (
    DOCID type of column DOCUMENT.DOCID,
    OBJID type of column OBJECT.OBJID,
    CLIENTID type of column OBJECT.OBJID,
    REALDOCDATE type of R_DATE
)
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
        if (:dst = '��') then
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

        if (:icamount > 0.0000001 and :dst in ('���', '��')) then
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

                excmes = '����� '||:errmes||': ��������� ������� � ��������� ������� ��������� ���������';
                exception exc_wh_wrongwares :excmes;
            end

            select w.dbeg
              from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
              into :saledbeg;
            
            if (:icamount > 0.00001 and :pufactor is NOT NULL and :dst in ('���', '��')) then
            begin
                for
                    with pre as (
                            select r.productdate as productdate, r.amountfree as amount
                              from wh_reserve r
                             where r.objid = :objid
                               and r.waresid = :waresid
                               and r.productdate > :saledbeg
                             union all
                            select t.productdate as productdate, -t.amount as amount
                              from wh_tmp_reserve_changes t
                             where t.waresid = :waresid
                               and t.objid = :objid
                               and t.docid = :docid
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
            
                    insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
                    values(:docid, :waresid, :productdate, :ramount, :objid);
            
                    icamount = :icamount - :ramount;
                    if (:icamount - :pufactor < -0.00001) then
                        break;
                end
            end

            if (:icamount > 0.00001 and :pufactor > 0.0001 and :dst = '��') then
            begin
                for
                    with pre as (
                            select r.productdate as productdate, r.amountfree as amount
                              from wh_reserve r
                             where r.objid = :objid
                               and r.waresid = :waresid
                               and r.productdate > :saledbeg
                             union all
                            select t.productdate as productdate, -t.amount as amount
                              from wh_tmp_reserve_changes t
                             where t.waresid = :waresid
                               and t.objid = :objid
                               and t.docid = :docid
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

                   insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
                   values(:docid, :waresid, :productdate, :ramount, :objid);

                   icamount = :icamount - :ramount;
        
                   if (:icamount < 0.0000001) then
                    break;
                end
            end

            if (:icamount > 0.0001 and :dst = '��') then
            begin
                for
                    with pre as (
                            select r.productdate as productdate, r.amountfree as amount
                              from wh_reserve r
                             where r.objid = :objid
                               and r.waresid = :waresid
                               and r.productdate > :saledbeg
                             union all
                            select t.productdate as productdate, -t.amount as amount
                              from wh_tmp_reserve_changes t
                             where t.waresid = :waresid
                               and t.objid = :objid
                               and t.docid = :docid
                               and t.productdate > :saledbeg
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
        errmes = '���������� ��������������� � ������ ���������� ������: '||:errmes;
        execute procedure WH_TEXT_TO_EXCMES(:errmes)
         returning_values :excmes;
        exception exc_wh_wrongamount :excmes;
   end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_TMPRESERVE_PREP (
    DOCID type of column DOCUMENT.DOCID,
    OBJID type of column OBJECT.OBJID,
    CLIENTID type of column OBJECT.OBJID,
    REALDOCDATE type of R_DATE
)
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
        if (:dst = '��') then
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

        if (:icamount > 0.0000001 and :dst in ('���', '��')) then
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

                excmes = '����� '||:errmes||': ��������� ������� � ��������� ������� ��������� ���������';
                exception exc_wh_wrongwares :excmes;
            end

            select w.dbeg
              from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
              into :saledbeg;
            
            if (:icamount > 0.00001 and :pufactor is NOT NULL and :dst in ('���', '��')) then
            begin
                for
                    with pre as (
                            select r.productdate as productdate, r.amountfree as amount
                              from wh_reserve r
                             where r.objid = :objid
                               and r.waresid = :waresid
                               and r.productdate > :saledbeg
                             union all
                            select t.productdate as productdate, -t.amount as amount
                              from wh_tmp_reserve_changes t
                             where t.waresid = :waresid
                               and t.objid = :objid
                               and t.docid = :docid
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
            
                    insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
                    values(:docid, :waresid, :productdate, :ramount, :objid);
            
                    icamount = :icamount - :ramount;
                    if (:icamount - :pufactor < -0.00001) then
                        break;
                end
            end

            if (:icamount > 0.00001 and :pufactor > 0.0001 and :dst = '��') then
            begin
                for
                    with pre as (
                            select r.productdate as productdate, r.amountfree as amount
                              from wh_reserve r
                             where r.objid = :objid
                               and r.waresid = :waresid
                               and r.productdate > :saledbeg
                             union all
                            select t.productdate as productdate, -t.amount as amount
                              from wh_tmp_reserve_changes t
                             where t.waresid = :waresid
                               and t.objid = :objid
                               and t.docid = :docid
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

                   insert into wh_tmp_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
                   values(:docid, :waresid, :productdate, :ramount, :objid);

                   icamount = :icamount - :ramount;
        
                   if (:icamount < 0.0000001) then
                    break;
                end
            end

            if (:icamount > 0.0001 and :dst = '��') then
            begin
                for
                    with pre as (
                            select r.productdate as productdate, r.amountfree as amount
                              from wh_reserve r
                             where r.objid = :objid
                               and r.waresid = :waresid
                               and r.productdate > :saledbeg
                             union all
                            select t.productdate as productdate, -t.amount as amount
                              from wh_tmp_reserve_changes t
                             where t.waresid = :waresid
                               and t.objid = :objid
                               and t.docid = :docid
                               and t.productdate > :saledbeg
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
        errmes = '���������� ��������������� � ������ ���������� ������: '||:errmes;
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

CREATE OR ALTER procedure WH_FUNDSALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I')
AS
declare variable queueid type of column r_queue.queueid;
begin
    if (not exists(select *
                     from imp_document id
                          left join doctype dt on id.doctype = dt.doctid
                    where id.docid = :docid
                      and dt.code = 'FUNDSALE')) then
        exception exc_wh_wrongdoctype;

    if (:actioncode = 'D') then
    begin
        if (not exists(select *
                         from document d
                        where d.docid = :docid)) then
        begin
            delete from imp_document id
             where id.docid = :docid;

            exit;
        end

        if (exists(select *
                     from docbond db
                          left join docbondtype dbt on dbt.docbondtid = db.docbondtid
                    where db.doc1id = :docid
                      and dbt.code = 'FUNDSALE')) then
            exception exc_wh_wrongdocstat '������� ����� �������� �������� �������!';
        
    end


    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');
    execute procedure WH_IMP_FUNDSALE_RESERVE_CANC(:docid);

    if (:ACTIONCODE = 'D') then
    begin
        update imp_document id
           set id.status = '�'
         where id.docid = :docid;

        delete from imp_document id
         where id.docid = :docid;
    end
    else if (:actioncode = 'I') then
    begin
        update imp_document id
           set id.status = '1'
         where id.docid = :docid;
    
        execute procedure wh_imp_doc_transfer(:docid);

        execute procedure WH_IMP_FUNDSALE_RESERVE_DO(:docid);

        select d.queueid
          from imp_document d
         where d.docid = :docid
          into :queueid;
        if (:queueid is NOT NULL) then
            execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');

        execute procedure RBS_Q_CREATETASKEXPORT('��������� �������������� �������',:docid,NULL,NULL)
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



DROP PROCEDURE WH_IMP_TMPRESERVE_PREP_IR;

