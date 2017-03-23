

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
       insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
       values(:docid, :waresid, :productdate, -:iramount, :fromobj);

       insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
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

           insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           values(:docid, :waresid, :productdate, -:iramount, :fromobj);
    
           insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           values(:docid, :waresid, :productdate, :iramount, :toobj);

           icamount = :icamount - :iramount;

           if (:icamount < 0.0000001) then
            break;
        end
    end
   end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDMOVING_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
begin
    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');
    execute procedure wh_imp_fundmoving_reserve_do(:docid);

    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDMOVING_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable queueid type of column R_QUEUE.queueid;
begin
    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');
    execute procedure wh_imp_fundmoving_reserve_do(:docid);

    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    select d.queueid
      from imp_document d
     where d.docid = :docid
      into :queueid;
    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'T');

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDMOVING_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable queueid type of column R_QUEUE.queueid;
begin
    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');
    execute procedure wh_imp_fundmoving_reserve_do(:docid);

    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    select d.queueid
      from imp_document d
     where d.docid = :docid
      into :queueid;
    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'T');

/*    delete from imp_document id
     where id.docid = :docid;*/
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
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'T');

/*    delete from imp_document id
     where id.docid = :docid;*/
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

/*    delete from imp_document id
     where id.docid = :docid;*/
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDSALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I')
AS
begin
    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');
    execute procedure WH_IMP_FUNDSALE_RESERVE_CANC(:docid);

    if (:ACTIONCODE = 'D') then
    begin
        delete from imp_cargo ic
         where ic.document = :docid;
    end
    else
    begin
        execute procedure WH_IMP_FUNDSALE_RESERVE_DO(:docid);
    end
        
    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

/*    delete from imp_document id
     where id.docid = :docid;*/
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
begin
   select coalesce(d.throughobj, d.fromobj), d.toobj, d.realdocdate
     from imp_document d
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
        begin
           insert into wh_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
           values(:docid, :waresid, :productdate, :iramount, :objid, :clientid);
    
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
    
               insert into wh_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
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

CREATE OR ALTER procedure WH_FUNDSALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I')
AS
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
    end
    else
    begin
        execute procedure WH_IMP_FUNDSALE_RESERVE_DO(:docid);
    end
        
/*    delete from imp_document id
     where id.docid = :docid;*/
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_GET_RESERVEOBJ (
    objidin TYPE OF COLUMN object.objid
)
returns (
    objid type of column object.OBJID
)
as
begin
    if (exists(select *
                  from wh_reserve_objects o
                 where o.objid = :objidin )) then
    begin
        objid = :objidin;
    end
    else
    begin
        select first(1) oi.objid
          from wh_obj_info oi
          into :objid;
    end

    suspend;
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
        begin
           insert into wh_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
           values(:docid, :waresid, :productdate, :iramount, :objid, :clientid);
    
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
    
               insert into wh_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
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

CREATE OR ALTER procedure WH_FUNDSALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I')
AS
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
    end
    else
    begin
        execute procedure WH_IMP_FUNDSALE_RESERVE_DO(:docid);
    end
        
/*    delete from imp_document id
     where id.docid = :docid;*/
end^

SET TERM ; ^



SET TERM ^ ;

create procedure EXP_DOC_FUNSALE_WARESRESERVE (
    DOCID type of column DOCUMENT.docid,
    WARESID type of column GWARES.waresid
)
returns (
    PRDATE type of column wh_reserve_changes.productdate,
    AMOUNT type of column wh_reserve_changes.amount
)
as
begin
    for
        select rcc.productdate, sum(rcc.amount)
          from wh_reserve_client_changes rcc
         where rcc.docid = :docid
           and rcc.waresid = :waresid
         group by rcc.productdate
          into :prdate, :amount
    do
        suspend;
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
    end
    else
    begin
        execute procedure WH_IMP_FUNDSALE_RESERVE_DO(:docid);
    end

    select d.queueid
      from imp_document d
     where d.docid = :docid
      into :queueid;
    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');
        
/*    delete from imp_document id
     where id.docid = :docid;*/
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
    end
    else
    begin
        execute procedure WH_IMP_FUNDSALE_RESERVE_DO(:docid);
    end

    select d.queueid
      from imp_document d
     where d.docid = :docid
      into :queueid;
    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');
        

     execute procedure RBS_Q_CREATETASKEXPORT('Результат резервирование продажи',:docid,NULL,NULL)
      returning_values :queueid;

    delete from imp_document id
     where id.docid = :docid;
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
    end
    else
    begin
        execute procedure WH_IMP_FUNDSALE_RESERVE_DO(:docid);
    end

    select d.queueid
      from imp_document d
     where d.docid = :docid
      into :queueid;
    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');
        
    execute procedure RBS_Q_CREATETASKEXPORT('Результат резервирование продажи',:docid,NULL,NULL)
      returning_values :queueid;

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^

