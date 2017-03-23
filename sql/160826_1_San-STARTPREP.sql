

CREATE TABLE WH_RESERVE_CLIENT (
    RESERVEID R_ID NOT NULL,
    DOCID R_ID64 NOT NULL,
    AMOUNT R_DOUBLE NOT NULL,
    ID R_ID NOT NULL);

ALTER TABLE WH_RESERVE_CLIENT
ADD CONSTRAINT PK_WH_RESERVE_CLIENT
PRIMARY KEY (ID);

CREATE SEQUENCE GEN_WH_RESERVE_CLIENT_ID;

SET TERM ^ ;

create trigger wh_reserve_client_bi for wh_reserve_client
active before insert position 0
as
begin
  if (new.id is null) then
    new.id = gen_id(gen_wh_reserve_client_id,1);
end^

SET TERM ; ^



SET TERM ^ ;

CREATE trigger wh_reserve_client_ai0 for wh_reserve_client
active after insert position 0
AS
begin
    update wh_reserve r
       set r.amountsale = r.amountsale + new.amount
     where r.id = new.reserveid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE trigger wh_reserve_client_au0 for wh_reserve_client
active after update position 0
AS
begin
    if (old.reserveid = new.reserveid) then
    begin
        update wh_reserve r
           set r.amountsale = r.amountsale - old.amount + new.amount
         where r.id = new.reserveid;
    end
    else
    begin
        update wh_reserve r
           set r.amountsale = r.amountsale - old.amount
         where r.id = old.reserveid;

        update wh_reserve r
           set r.amountsale = r.amountsale + new.amount
         where r.id = new.reserveid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_client_au0 for wh_reserve_client
active after update position 0
AS
begin
    if (old.reserveid = new.reserveid) then
    begin
        update wh_reserve r
           set r.amountsale = r.amountsale - old.amount + new.amount
         where r.id = new.reserveid;
    end
    else
    begin
        update wh_reserve r
           set r.amountsale = r.amountsale - old.amount
         where r.id = old.reserveid;

        update wh_reserve r
           set r.amountsale = r.amountsale + new.amount
         where r.id = new.reserveid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE trigger wh_reserve_client_ad0 for wh_reserve_client
active after delete position 0
AS
begin
    update wh_reserve r
       set r.amountsale = r.amountsale - old.amount
     where r.id = old.reserveid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE trigger wh_reserve_bd0 for wh_reserve
active before delete position 0
AS
begin
    if (old.amountsale > 0.0000001
        or
        exists(select * from wh_reserve_client rc where rc.reserveid = old.id)
    ) then
        exception exc_wh_reserve 'Есть резерв для клиента: удаление невозможно!';

end^

SET TERM ; ^



ALTER TABLE WH_RESERVE_CLIENT
ADD CLIENTID R_ID
NOT NULL ;



ALTER TABLE WH_RESERVE_CLIENT
ADD CONSTRAINT FK_WH_RESERVE_CLIENT_RID
FOREIGN KEY (RESERVEID)
REFERENCES WH_RESERVE(ID);

ALTER TABLE WH_RESERVE_CLIENT
ADD CONSTRAINT FK_WH_RESERVE_CLIENT_CLID
FOREIGN KEY (CLIENTID)
REFERENCES OBJECT(OBJID)
ON DELETE CASCADE
ON UPDATE CASCADE;



ALTER TABLE WH_RESERVE_CLIENT
ADD CONSTRAINT FK_WH_RESERVE_CLIENT_DOCID
FOREIGN KEY (DOCID)
REFERENCES DOCUMENT(DOCID)
ON DELETE CASCADE
ON UPDATE CASCADE;



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_client_au0 for wh_reserve_client
active after update position 0
AS
begin
    if (old.reserveid = new.reserveid) then
    begin
        update wh_reserve r
           set r.amountsale = r.amountsale - old.amount + new.amount
         where r.id = new.reserveid;
    end
    else
    begin
        update wh_reserve r
           set r.amountsale = r.amountsale - old.amount
         where r.id = old.reserveid;

        update wh_reserve r
           set r.amountsale = r.amountsale + new.amount
         where r.id = new.reserveid;
    end

    if (new.amount < 0.0000001) then
        delete from wh_reserve_client rc
         where rc.id = new.id;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_client_au0 for wh_reserve_client
active after update position 0
AS
begin
    if (old.reserveid = new.reserveid) then
    begin
        update wh_reserve r
           set r.amountsale = r.amountsale - old.amount + new.amount
         where r.id = new.reserveid;
    end
    else
    begin
        update wh_reserve r
           set r.amountsale = r.amountsale - old.amount
         where r.id = old.reserveid;

        update wh_reserve r
           set r.amountsale = r.amountsale + new.amount
         where r.id = new.reserveid;
    end

    if (new.amount < 0.0000001) then
        delete from wh_reserve_client rc
         where rc.id = new.id;
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
declare variable irid type of R_DATE;
begin
   select d.fromobj, d.toobj, d.throughobj, d.realdocdate
     from document d
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
     from document d
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



CREATE TABLE WH_RESERVE_CLIENT_CHANGES (
    WHID R_ID NOT NULL,
    WARESID R_ID NOT NULL,
    PRODUCTDATE R_DATE NOT NULL,
    CLIENTID R_ID NOT NULL,
    AMOUNT R_DOUBLE NOT NULL,
    DOCID R_ID64);



ALTER TABLE WH_RESERVE_CLIENT_CHANGES
ADD CONSTRAINT FK_WH_RESERVE_CLIENT_CHANGES_WH
FOREIGN KEY (WHID)
REFERENCES OBJECT(OBJID)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE WH_RESERVE_CLIENT_CHANGES
ADD CONSTRAINT FK_WH_RESERVE_CLIENT_CHANGES_W
FOREIGN KEY (WARESID)
REFERENCES GWARES(WARESID)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE WH_RESERVE_CLIENT_CHANGES
ADD CONSTRAINT FK_WH_RESERVE_CLIENT_CHANGES_D
FOREIGN KEY (DOCID)
REFERENCES DOCUMENT(DOCID)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE WH_RESERVE_CLIENT_CHANGES
ADD CONSTRAINT FK_WH_RESERVE_CLIENT_CHANGES_CL
FOREIGN KEY (CLIENTID)
REFERENCES OBJECT(OBJID)
ON DELETE CASCADE
ON UPDATE CASCADE;



CREATE UNIQUE INDEX WH_RESERVE_IDX_OWDATE
ON WH_RESERVE (OBJID,WARESID,PRODUCTDATE);



DROP INDEX WH_RESERVE_IDX_OWDATEFREE;



SET TERM ^ ;

create procedure WH_RESERVE_GETID (
    OBJID type of column wh_reserve.objid,
    WARESID type of column wh_reserve.waresid,
    PRODUCTDATE type of column wh_reserve.productdate
)
returns (
    ID type of column wh_reserve.id
)
as
begin
    select r.id
      from wh_reserve r
     where r.objid = :objid
       and r.waresid = :waresid
       and r.productdate = :productdate
      into :id;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_changes_ai0 for wh_reserve_changes
active after insert position 0
AS
declare variable reserveid type of column wh_reserve.id;
begin
    execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
     returning_values :reserveid;

    if (:reserveid is NULL) then
        insert into wh_reserve ( WARESID, PRODUCTDATE, AMOUNT, OBJID)
        values ( new.waresid, new.productdate, new.amount, new.objid);
    else
        update wh_reserve r
           set r.amount = r.amount + new.amount
         where r.id = :reserveid;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_changes_au0 for wh_reserve_changes
active after update position 0
AS
declare variable reserveid type of column wh_reserve.id;
begin
    if (
        new.objid <> old.objid
        or
        new.waresid <> old.waresid
        or
        new.productdate <> old.productdate
    ) then
    begin
        execute procedure wh_reserve_getid(old.objid, old.waresid, old.productdate)
         returning_values :reserveid;

        if (:reserveid is NULL) then
            insert into wh_reserve ( WARESID, PRODUCTDATE, AMOUNT, OBJID)
            values ( old.waresid, old.productdate, - old.amount, old.objid);
        else
            update wh_reserve r
               set r.amount = r.amount - old.amount
             where r.id = :reserveid;

        reserveid = NULL;
        execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
         returning_values :reserveid;

        if (:reserveid is NULL) then
            insert into wh_reserve ( WARESID, PRODUCTDATE, AMOUNT, OBJID)
            values ( new.waresid, new.productdate, new.amount, new.objid);
        else
            update wh_reserve r
               set r.amount = r.amount + new.amount
             where r.id = :reserveid;    
    end
    else if (abs(new.amount - old.amount) > 0.000001) then
    begin
        execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
         returning_values :reserveid;

        if (:reserveid is NULL) then
            insert into wh_reserve ( WARESID, PRODUCTDATE, AMOUNT, OBJID)
            values ( new.waresid, new.productdate, new.amount - old.amount, new.objid);
        else
            update wh_reserve r
               set r.amount = r.amount + new.amount - old.amount
             where r.id = :reserveid;    
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_changes_ad0 for wh_reserve_changes
active after delete position 0
AS
declare variable reserveid type of column wh_reserve.id;
begin
    execute procedure wh_reserve_getid(old.objid, old.waresid, old.productdate)
     returning_values :reserveid;

    if (:reserveid is NULL) then
        insert into wh_reserve ( WARESID, PRODUCTDATE, AMOUNT, OBJID)
        values ( old.waresid, old.productdate, - old.amount, old.objid);
    else
        update wh_reserve r
           set r.amount = r.amount - old.amount
         where r.id = :reserveid;
end^

SET TERM ; ^



ALTER TABLE WH_RESERVE_CLIENT_CHANGES DROP CONSTRAINT FK_WH_RESERVE_CLIENT_CHANGES_WH;



ALTER TABLE WH_RESERVE_CLIENT_CHANGES ALTER WHID TO OBJID;



ALTER TABLE WH_RESERVE_CLIENT_CHANGES
ADD CONSTRAINT FK_WH_RESERVE_CLIENT_CHANGES_O
FOREIGN KEY (OBJID)
REFERENCES OBJECT(OBJID)
ON DELETE CASCADE
ON UPDATE CASCADE;



SET TERM ^ ;

CREATE trigger wh_reserve_client_changes_ai0 for wh_reserve_client_changes
active after insert position 0
AS
declare variable reserveid type of column wh_reserve.id;
begin
    execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
     returning_values :reserveid;

    insert into wh_reserve_client ( RESERVEID, DOCID, AMOUNT, CLIENTID)
    values (:reserveid, new.docid, new.amount, new.clientid);
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_client_changes_ai0 for wh_reserve_client_changes
active after insert position 0
AS
declare variable reserveid type of column wh_reserve.id;
declare variable reserveclientid type of column wh_reserve_client.id;
begin
    execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
     returning_values :reserveid;

    if (:reserveid is NULL) then
    begin
        exception exc_wh_reserve 'Резерв не найден!';
    end
    else
    begin
        select rc.id
          from wh_reserve_client rc
         where rc.reserveid = :reserveid
           and rc.clientid = new.clientid
           and rc.docid = new.docid
          into :reserveclientid;

        if (:reserveclientid is NULL) then
            insert into wh_reserve_client ( RESERVEID, DOCID, AMOUNT, CLIENTID)
            values (:reserveid, new.docid, new.amount, new.clientid)    ;    
        else
            update wh_reserve_client rc
               set rc.amount = rc.amount + new.amount
             where rc.id = :reserveclientid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_client_changes_ai0 for wh_reserve_client_changes
active after insert position 0
AS
declare variable reserveid type of column wh_reserve.id;
declare variable reserveclientid type of column wh_reserve_client.id;
begin
    execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
     returning_values :reserveid;

    if (:reserveid is NULL) then
    begin
        exception exc_wh_reserve 'Резерв не найден!';
    end
    else
    begin
        select rc.id
          from wh_reserve_client rc
         where rc.reserveid = :reserveid
           and rc.clientid = new.clientid
           and rc.docid = new.docid
          into :reserveclientid;

        if (:reserveclientid is NULL) then
            insert into wh_reserve_client ( RESERVEID, DOCID, AMOUNT, CLIENTID)
            values (:reserveid, new.docid, new.amount, new.clientid);
        else
            update wh_reserve_client rc
               set rc.amount = rc.amount + new.amount
             where rc.id = :reserveclientid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_client_changes_ai0 for wh_reserve_client_changes
active after insert position 0
AS
declare variable reserveid type of column wh_reserve.id;
declare variable reserveclientid type of column wh_reserve_client.id;
begin
    execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
     returning_values :reserveid;

    if (:reserveid is NULL) then
    begin
        exception exc_wh_reserve 'Резерв не найден!';
    end
    else
    begin
        select rc.id
          from wh_reserve_client rc
         where rc.reserveid = :reserveid
           and rc.clientid = new.clientid
          into :reserveclientid;

        if (:reserveclientid is NULL) then
            insert into wh_reserve_client ( RESERVEID, AMOUNT, CLIENTID)
            values (:reserveid, new.amount, new.clientid);
        else
            update wh_reserve_client rc
               set rc.amount = rc.amount + new.amount
             where rc.id = :reserveclientid;
    end
end^

SET TERM ; ^



ALTER TABLE WH_RESERVE_CLIENT DROP CONSTRAINT FK_WH_RESERVE_CLIENT_DOCID;



ALTER TABLE WH_RESERVE_CLIENT DROP DOCID;



SET TERM ^ ;

create procedure WH_RESERVE_CLIENT_QDIFFSET (
    RESERVEID type of column wh_reserve.id,
    clientid type of column OBJECT.objid,
    QDIFF type of R_DOUBLE
)
as
declare variable reserveclientid type of column wh_reserve_client.id;
begin
    select rc.id
      from wh_reserve_client rc
     where rc.reserveid = :reserveid
       and rc.clientid = :clientid
      into :reserveclientid;

    if (:reserveclientid is NULL) then
        insert into wh_reserve_client ( RESERVEID, AMOUNT, CLIENTID)
        values (:reserveid, :qdiff, :clientid);
    else
        update wh_reserve_client rc
           set rc.amount = rc.amount + :qdiff
         where rc.id = :reserveclientid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_client_changes_ai0 for wh_reserve_client_changes
active after insert position 0
AS
declare variable reserveid type of column wh_reserve.id;
begin
    execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
     returning_values :reserveid;

    if (:reserveid is NULL) then
    begin
        exception exc_wh_reserve 'Резерв не найден!';
    end
    else
    begin
        execute procedure WH_RESERVE_CLIENT_QDIFFSET(:reserveid, new.clientid, new.amount);
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RESERVE_CLIENT_QDIFFSET (
    RESERVEID type of column wh_reserve.id,
    clientid type of column OBJECT.objid,
    QDIFF type of R_DOUBLE
)
as
declare variable reserveclientid type of column wh_reserve_client.id;
begin
    if (:reserveid is NULL) then
        exception exc_wh_reserve 'Не установлен идентификатор резерва!';

    select rc.id
      from wh_reserve_client rc
     where rc.reserveid = :reserveid
       and rc.clientid = :clientid
      into :reserveclientid;

    if (:reserveclientid is NULL) then
        insert into wh_reserve_client ( RESERVEID, AMOUNT, CLIENTID)
        values (:reserveid, :qdiff, :clientid);
    else
        update wh_reserve_client rc
           set rc.amount = rc.amount + :qdiff
         where rc.id = :reserveclientid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_client_changes_ai0 for wh_reserve_client_changes
active after insert position 0
AS
declare variable reserveid type of column wh_reserve.id;
begin
    execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
     returning_values :reserveid;

    execute procedure WH_RESERVE_CLIENT_QDIFFSET(:reserveid, new.clientid, new.amount);
end^

SET TERM ; ^



SET TERM ^ ;

CREATE trigger wh_reserve_client_changes_au0 for wh_reserve_client_changes
active after update position 0
AS
declare variable reserveid type of column wh_reserve.id;
begin
    if (
        new.objid <> old.objid
        or
        new.waresid <> old.waresid
        or
        new.productdate <> old.productdate
        or
        new.clientid <> old.clientid
    ) then
    begin
        reserveid = NULL;
        execute procedure wh_reserve_getid(old.objid, old.waresid, old.productdate)
         returning_values :reserveid;

        execute procedure WH_RESERVE_CLIENT_QDIFFSET(:reserveid, old.clientid, -old.amount);

        reserveid = NULL;
        execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
         returning_values :reserveid;

        execute procedure WH_RESERVE_CLIENT_QDIFFSET(:reserveid, new.clientid, new.amount);
    end
    else if (abs(old.amount - new.amount) > 0.0000001) then
    begin
        reserveid = NULL;
        execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
         returning_values :reserveid;

        execute procedure WH_RESERVE_CLIENT_QDIFFSET(:reserveid, new.clientid, new.amount - old.amount);
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE trigger wh_reserve_client_changes_ad0 for wh_reserve_client_changes
active after delete position 0
AS
declare variable reserveid type of column wh_reserve.id;
begin
    execute procedure wh_reserve_getid(old.objid, old.waresid, old.productdate)
     returning_values :reserveid;

    execute procedure WH_RESERVE_CLIENT_QDIFFSET(:reserveid, old.clientid, -old.amount);
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_client_bi for wh_reserve_client
active before insert position 0
as
begin
  if (new.amount < 0.000001) then
    exception exc_wh_reserve 'Резерв должен быть положительным числом!';

  if (new.id is null) then
    new.id = gen_id(gen_wh_reserve_client_id,1);
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_FUNDSALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
begin /*$$IBE$$ 
    
    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    delete from imp_document id
     where id.docid = :docid;
 $$IBE$$*/ EXIT;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_IMP_FUNDSALE_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
 /*$$IBE$$ declare variable fromobj type of column OBJECT.objid;
declare variable toobj type of column OBJECT.objid;
declare variable clientid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable icamount type of column IMP_CARGO.amount;
declare variable productdate type of column WARESLOT.productdate;
declare variable iramount type of column IMP_RESERVE.amount;
declare variable realdocdate type of column DOCUMENT.realdocdate;
declare variable saledbeg type of R_DATE;
declare variable irid type of R_DATE; $$IBE$$*/ 
begin /*$$IBE$$ 
   select d.fromobj, d.toobj, d.throughobj, d.realdocdate
     from document d
    where d.docid = :docid
     into :fromobj, :toobj, :clientid, :realdocdate;

   for
    select ic.waresid, ic.amount
      from imp_cargo ic
     where ic.document = :docid
       and ic.amount > 0.000001
      into :waresid, :icamount
   do
   begin
        select w.dbeg
          from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
          into :saledbeg;
        
        for
            select r.amountfree, r.productdate, r.id
              from wh_reserve r
             where r.objid = :fromobj
               and r.waresid = :waresid
               and r.productdate > :saledbeg
               and r.amountfree > 0.0000001
              into :iramount, :productdate, :reserveid
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
 $$IBE$$*/ EXIT;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE trigger wh_reserve_client_bu0 for wh_reserve_client
active before update position 0
AS
begin
  if (new.amount < -0.000001) then
    exception exc_wh_reserve 'Резерв должен быть положительным числом!';
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
declare variable reserveid type of column wh_reserve.id;
begin
   select coalesce(d.throughobj, d.fromobj), d.toobj, d.realdocdate
     from document d
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
        select w.dbeg
          from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
          into :saledbeg;
        
        for
            select r.amountfree, r.productdate, r.id
              from wh_reserve r
             where r.objid = :objid
               and r.waresid = :waresid
               and r.productdate > :saledbeg
               and r.amountfree > 0.0000001
              into :iramount, :productdate, :reserveid
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
     from document d
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
     from document d
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
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDSALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
begin
    execute procedure WH_IMP_FUNDSALE_RESERVE_DO(:docid);

    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDSALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTONCODE type of r_flag = 'I'
)
AS
begin
    if (:actoncode = 'I') then
        execute procedure WH_IMP_FUNDSALE_RESERVE_DO(:docid);

    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_DOC_TRANSFER (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable iddoctype type of column document.doctype;
declare variable iddocdate type of column document.docdate;
declare variable idnumber type of column document.number;
declare variable idfromobj type of column document.fromobj;
declare variable idthroughobj type of column document.throughobj;
declare variable idtoobj type of column document.toobj;
declare variable idamount type of column document.amount;
declare variable iddescript type of column document.descript;
declare variable idrealdocdate type of column document.realdocdate;
declare variable idstatus type of column document.status;
declare variable idreason type of column document.reason;
declare variable iddocsubtype type of column document.docsubtype;
declare variable iddelay type of column document.delay;
declare variable idnumberlink type of column document.numberlink;
declare variable idexternalintid type of column document.externalintid;
declare variable cgamount type of column cargo.amount;
declare variable cgprice type of column cargo.price;
declare variable waresid type of column GWARES.waresid;
begin
    if (exists(select *
                 from document d
                where d.docid = :docid)) then
    begin
        select id.doctype, id.docdate, id.number, id.fromobj, id.throughobj, id.toobj,
               id.amount, id.descript, id.realdocdate, id.status, id.reason, id.docsubtype, id.delay,
               id.numberlink, id.externalintid
          from imp_document id
         where id.docid = :docid
          into :iddoctype, :iddocdate, :idnumber, :idfromobj, :idthroughobj, :idtoobj,
               :idamount, :iddescript, :idrealdocdate, :idstatus, :idreason, :iddocsubtype, :iddelay,
               :idnumberlink, :idexternalintid;

        update document d
           set d.doctype = :iddoctype,
               d.docdate = :iddocdate,
               d.number = :idnumber,
               d.fromobj = :idfromobj,
               d.throughobj = :idthroughobj,
               d.toobj = :idtoobj,
               d.amount = :idamount,
               d.descript = :iddescript,
               d.realdocdate = :idrealdocdate,
               d.status = :idstatus,
               d.reason = :idreason,
               d.docsubtype = :iddocsubtype,
               d.delay = :iddelay,
               d.numberlink = :idnumberlink,
               d.externalintid = :idexternalintid
         where d.docid = :docid;
    end
    else
    begin
        insert into document ( DOCID, DOCTYPE, DOCDATE, NUMBER, FROMOBJ, THROUGHOBJ, TOOBJ, AMOUNT, DESCRIPT, REALDOCDATE, STATUS, REASON, DOCSUBTYPE, DELAY, NUMBERLINK, EXTERNALINTID)
        select id.docid, id.doctype, id.docdate, id.number, id.fromobj, id.throughobj, id.toobj, id.amount, id.descript, id.realdocdate, id.status, id.reason, id.docsubtype, id.delay, id.numberlink, id.externalintid
          from imp_document id
         where id.docid = :docid;
    end

    update cargo cg
       set cg.amount = 0.000, cg.docsum = 0.000
     where cg.document = :docid;

    for
        select cg.waresid, cg.amount, cg.price
          from imp_cargo cg
         where cg.document = :docid
          into :waresid, :cgamount, :cgprice
    do
    begin
        update or insert into cargo(document, waresid, amount, price, docsum)
        values(:docid, :waresid, :cgamount, :cgprice, NULL)
        matching(document, waresid);
    end

    delete from cargo cg
     where cg.document = :docid and abs(cg.amount) < 0.0000001;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_IMP_FUNDSALE_RESERVE_CANC (
    DOCID type of column DOCUMENT.DOCID)
AS
begin
    insert into wh_reserve_client_changes ( OBJID, WARESID, PRODUCTDATE, CLIENTID, AMOUNT, DOCID)
    select rc.objid, rc.waresid, rc.productdate, rc.clientid, -sum(rc.amount), rc.docid
      from wh_reserve_client_changes rc
     where rc.docid = :docid
     group by rc.waresid, rc.productdate, rc.objid, rc.clientid, rc.docid
    having abs(sum(rc.amount)) > 0.0000001;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDSALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTONCODE type of r_flag = 'I'
)
AS
begin
    if (:actoncode = 'D') then
    begin
        execute procedure WH_IMP_FUNDSALE_RESERVE_CANC(:docid);
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

    delete from imp_document id
     where id.docid = :docid;
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
     from document d
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
    ACTONCODE type of R_FLAG = 'I'
)
AS
begin
    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');
    execute procedure WH_IMP_FUNDSALE_RESERVE_CANC(:docid);

    if (:actoncode = 'D') then
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

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_FUNDINCOME_STATUSCHG (
    DOCID type of column DOCUMENT.DOCID,
    OLDSTAT type of column R_STATUS.CODE,
    NEWSTAT type of column R_STATUS.CODE)
AS
declare variable queueid type of column r_queue.queueid;
declare variable egaisneed type of column waresgroup_singularity.egaisneed;
declare variable whid type of column OBJECT.objid;
declare variable realdocdate type of column DOCUMENT.realdocdate;
begin
    if (:newstat = 'w') then
    begin
        select wsg.egaisneed
          from document_wgsingularity ds
               left join waresgroup_singularity wsg
                 on wsg.id = ds.singularityid
         where ds.docid = :docid
          into :egaisneed;

        if (:egaisneed is NULL or :egaisneed = '1') then
        begin
         execute procedure RBS_Q_CREATETASKEXPORT('FUNDINCOME_STATUSCHG: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
          returning_values :queueid;
        end
        else
        begin
            select d.toobj, d.realdocdate
              from document d
             where d.docid = :docid
              into :whid, :realdocdate;

           insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           select :docid, cg.waresid, :realdocdate, cg.amount, :whid
             from cargo cg
            where cg.document = :docid;

           update document d
              set d.status = 'e'
            where d.docid = :docid;
       end
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure U3S_TASKSELECT_CREATE_PREP (
    DOCID type of column DOCUMENT.docid)
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
begin
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
        select w.waresid,w.amount,coalesce(g.selgroup,0),wu.factor
          from (select cg.waresid as waresid,sum(cg.amount) as amount
                  from cargo cg
                       left join gwares g on g.waresid = cg.waresid
                 where cg.document = :docid
                   and cg.cargo2id is NULL
                   and coalesce(g.pa,'1') <> '0'
                 group by cg.waresid) w
               left join gwares g on g.waresid = w.waresid
               left join waresunit wu on wu.waresid = w.waresid and wu.unitid = :palletunitid
         order by g.frailty descending nulls last
          into :waresid,:amount,:selgroupid,:maxfactor
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
                insert into k_tbltmp_select_docwares(waresid,amount,selgroupid,taskmethodid,rest,slotid,rowid,weight,capacity,numpallet,num,zoneid)
                values(:waresid,:maxfactor,:selgroupid,:tmid_pallet,NULL,NULL,NULL,:weight,:capacity,:numpallet,:numpos,:zoneid);

                amount = :amount - :maxfactor;
            end
        
        -- Скидываем остатки
        if (:amount>0.00001) then
        begin
            weight = NULL; capacity = NULL;
            select wc.weight,wc.capacity
              from WM_GETWARESWEIGHTCAPACITY(:waresid,:amount) wc
              into :weight,:capacity;

             insert into k_tbltmp_select_docwares(waresid,amount,selgroupid,taskmethodid,rest,slotid,rowid,weight,capacity,zoneid,sitesegmentid)
             values(:waresid,:amount,:selgroupid,:tmid_f,NULL,NULL,NULL,:weight,:capacity,:zoneid,NULL);
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure U3S_TASKSELECT_CREATE_PREVIEW (
    DOCID type of column DOCUMENT.docid)
returns (
    NUMPALLET type of R_NUMBER,
    ZONEID type of column SITEZONE.zoneid,
    ZONENAME type of column SITEZONE.name,
    NUMPOS type of R_NUMBER,
    TMALGO type of column wm_taskmethod.algorithm,
    TMNAME type of column wm_taskmethod.name,
    WID type of column GWARES.waresid,
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    WQUANTITY type of R_DOUBLE,
    WWEIGHT type of R_DOUBLE,
    WCAPACITY type of R_DOUBLE,
    VUCODE type of column UNIT.shortname,
    VUFACTOR type of column WARESUNIT.factor,
    MUCODE type of column UNIT.shortname,
    MUFACTOR type of column WARESUNIT.factor,
    WSGCODE type of column k_wares_selgroup.code,
    WSGNAME type of column k_wares_selgroup.name,
    WSGWEIGHT type of R_DOUBLE,
    WSGCAPACITY type of R_DOUBLE)
AS
begin
    execute procedure u3s_taskselect_create_prep(:docid);

    for
        select g.waresid,g.code,g.name,
               mwu.factor,mu.shortname,vwu.factor,vu.shortname,
               k.numpallet,k.num,k.amount,k.capacity,k.weight,
               tm.algorithm,tm.name,
               wsg.code,wsg.name,wsg.capacity,wsg.weight,
               k.zoneid,sz.name
          from k_tbltmp_select_docwares k
               left join gwares g
                    left join waresunit vwu
                         left join unit vu on vu.unitid = vwu.unitid
                      on vwu.waresunitid = g.viewunitid
                    left join waresunit mwu
                         left join unit mu on mu.unitid = mwu.unitid
                      on mwu.waresunitid = g.mainunitid
                 on g.waresid = k.waresid
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
               left join k_wares_selgroup wsg on wsg.id = k.selgroupid
               left join sitezone sz on sz.zoneid = k.zoneid
         order by k.numpallet ascending Nulls first,k.num ascending nulls first
          into :wid,:wcode,:wname,:mufactor,:mucode,:vufactor,:vucode,
               :numpallet,:numpos,:wquantity,:wcapacity,:wweight,
               :tmalgo,:tmname,:wsgcode,:wsgname,:wsgcapacity,:wsgweight,
               :zoneid,:zonename
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure U3S_TASKSELECT_CREATE (
    DOCID type of column DOCUMENT.docid)
AS
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable ttinitst_select type of column wm_tasktype.initstatus;
declare variable tmid_select type of column wm_taskmethod.methodid;
declare variable waresid type of column GWARES.waresid;
declare variable amount type of r_double;
declare variable numpallet type of r_number;
declare variable numpos type of r_number;
declare variable status type of r_status;
declare variable slotid type of r_id;
declare variable taskid type of r_id;
declare variable taskpalletnum type of r_number;
declare variable price type of r_double;
declare variable CAPACITY type of r_double;
declare variable WEIGHT type of r_double;
declare variable Zoneid type of r_id;
begin
    execute procedure u3s_taskselect_create_prep(:docid);

    select k.ttid,coalesce(k.ttinitst,'0')
      from k_tasktype_by_code('SELECT',NULL) k
      into :ttid_select,:ttinitst_select;


    taskid = NULL;
    taskpalletnum = -1;
    for
        select coalesce(k.numpallet,0),k.num,k.taskmethodid,k.waresid,k.amount,k.slotid,coalesce(tm.startstatus,:ttinitst_select),k.zoneid
          from k_tbltmp_select_docwares k
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
         order by k.numpallet ascending nulls last,k.num ascending nulls last
          into :numpallet,:numpos,:tmid_select,:waresid,:amount,:slotid,:status,:zoneid
    do
    begin
        if (:taskpalletnum <> :numpallet and :taskpalletnum is NOT NULL and :numpallet is NOT NULL) then
        begin
            if (:taskid is NOT NULL) then
            begin
                select sum(ww.weight),sum(ww.capacity)
                  from wm_task_wares tw
                       left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
                 where tw.taskid = :taskid
                  into :WEIGHT,:CAPACITY;
            
                update wm_task t
                   set t.weight = :weight,t.capacity = :capacity
                 where t.taskid = :taskid;
            end

            taskpalletnum = :numpallet;

            if (:zoneid = 0) then zoneid = NULL;
            insert into wm_task(tasktypeid,taskmethodid,status,docid,num,zoneid)
            values (:ttid_select,:tmid_select,:status,:docid,:numpallet,:zoneid)
            returning taskid
            into :taskid;
        end

        price = NULL;
        select round(sum(cg.docsum)/sum(cg.amount),4)
          from cargo cg
         where cg.document = :docid
           and cg.waresid = :waresid
           and cg.cargo2id is NULL
           and cg.amount > 0.0001
          into :price;
        if (:price is null) then price = 0.000;

        insert into wm_task_wares(taskid,waresid,status,quantity,siteid,num,summa)
        values(:taskid,:waresid,iif(:tmid_select is NOT NULL,'0',NULL),:amount,:slotid,:numpos,:price);
    end

    if (:taskid is NOT NULL) then
    begin
        select sum(ww.weight),sum(ww.capacity)
          from wm_task_wares tw
               left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
         where tw.taskid = :taskid
          into :WEIGHT,:CAPACITY;
    
        update wm_task t
           set t.weight = :weight,t.capacity = :capacity
         where t.taskid = :taskid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_U3S_SALE_STATUSCHG (
    DOCID R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable FROMOBJ type of R_ID;
declare variable DOCTID type of R_ID;
declare variable DOCTCODE type of R_CODE;
declare variable DOCSUBTYPE type of R_CODE3;
declare variable tid_gateauto type of R_ID;
declare variable ttid_select type of r_id;
begin
    select d.doctype,dt.code,d.fromobj,d.docsubtype
      from document d
           left join doctype dt on dt.doctid=d.doctype
     where d.docid = :docid
      into :doctid,:doctcode,:fromobj,:docsubtype;

    if (:doctcode <> 'SALE') then
        exception exc_k_wrongdoctype;

    if (:newstat = 'g' and coalesce(:docsubtype,'') not in ('WP','AM')) then
    begin
        -- Если повышение статуса
        if (exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.upcodes containing :newstat )) then
        begin
            execute procedure u3s_taskselect_create(:docid);

            if (not exists(select *
                             from wm_task t
                                  left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                            where t.docid = :docid
                              and tt.code = 'SELECT'
                              and t.taskmethodid is NOT NULL)) then
                update document d
                   set d.status = '2'
                 where d.docid = :docid;
        end

    end
    else if (:newstat = '2') then
    begin
        -- Если повышение статуса
        if (coalesce(:docsubtype,'') not in ('WP','AM') and
            exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.upcodes containing :newstat )) then
        begin
            if (exists(select *
                         from wm_task t
                              left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                        where t.docid = :docid
                          and tt.code = 'SELECT'
                          and t.taskmethodid is NOT NULL
                          and t.status<>'2')) then
                exception exc_k_common 'У документа есть не завершенные задания на отборку!';

            -- Поправим сам док на верные количества
            execute procedure wh_ttid_select
             returning_values :ttid_select;
            execute procedure wh_core_setdocbytask(:docid,:ttid_select,'SCANQUANT');

            -- Активируем задания на погрузку поддонов в машину
/*            select t.tid_gateauto
              from WH_LOADAUTODC_GETTASKBYDOC(:docid) t
              into :tid_gateauto;
            if (:tid_gateauto is NOT NULL) then
                execute procedure wh_loadpalletdc_createtaskes(:tid_gateauto);*/
        end
        else if (:oldstat='k') then
        begin
            execute procedure WH_SALE_SETBYPALLETS(:docid);
        end
    end
    else if (:newstat = 'e') then
    begin
        if (exists(select *
                     from wm_task t
                          left join wm_tasktype tt
                            on tt.tasktypeid = t.tasktypeid
                    where t.docid = :docid
                      and tt.code = 'LOADAUTO'
                      and t.status <> '2')) then
            exception exc_k_common 'Не завершена погрузка паллетов документа в машину!';

        -- Поправим сам док наверные количества
        execute procedure wh_core_setdocbytasklot(:docid,-1);

--        execute procedure uv_sale_taraset(:docid);

        -- Выгружаем
        if (coalesce(:docsubtype,'') not in ('WP','AM')) then
          execute procedure RBS_Q_CREATETASKEXPORT('K_VT_SALE_STATUSCHG: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
           returning_values :docid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_SALE_STATUSCHG (
    DOCID R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable FROMOBJ type of R_ID;
declare variable DOCTID type of R_ID;
declare variable DOCTCODE type of R_CODE;
declare variable DOCSUBTYPE type of R_CODE3;
declare variable tid_gateauto type of R_ID;
declare variable ttid_select type of r_id;
begin
    select d.doctype,dt.code,d.fromobj,d.docsubtype
      from document d
           left join doctype dt on dt.doctid=d.doctype
     where d.docid = :docid
      into :doctid,:doctcode,:fromobj,:docsubtype;

    if (:doctcode <> 'SALE') then
        exception exc_k_wrongdoctype;

    if (:newstat = 'g' and coalesce(:docsubtype,'') not in ('WP','AM')) then
    begin
        -- Если повышение статуса
        if (exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.upcodes containing :newstat )) then
        begin
            execute procedure u3s_taskselect_create(:docid);

            if (not exists(select *
                             from wm_task t
                                  left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                            where t.docid = :docid
                              and tt.code = 'SELECT'
                              and t.taskmethodid is NOT NULL)) then
                update document d
                   set d.status = '2'
                 where d.docid = :docid;
        end

    end
    else if (:newstat = '2') then
    begin
        -- Если повышение статуса
        if (coalesce(:docsubtype,'') not in ('WP','AM') and
            exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.upcodes containing :newstat )) then
        begin
            if (exists(select *
                         from wm_task t
                              left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                        where t.docid = :docid
                          and tt.code = 'SELECT'
                          and t.taskmethodid is NOT NULL
                          and t.status<>'2')) then
                exception exc_k_common 'У документа есть не завершенные задания на отборку!';

            -- Поправим сам док на верные количества
            execute procedure wh_ttid_select
             returning_values :ttid_select;
            execute procedure wh_core_setdocbytask(:docid,:ttid_select,'SCANQUANT');

            -- Активируем задания на погрузку поддонов в машину
/*            select t.tid_gateauto
              from WH_LOADAUTODC_GETTASKBYDOC(:docid) t
              into :tid_gateauto;
            if (:tid_gateauto is NOT NULL) then
                execute procedure wh_loadpalletdc_createtaskes(:tid_gateauto);*/
        end
        else if (:oldstat='k') then
        begin
            execute procedure WH_SALE_SETBYPALLETS(:docid);
        end
    end
    else if (:newstat = 'e') then
    begin
        if (exists(select *
                     from wm_task t
                          left join wm_tasktype tt
                            on tt.tasktypeid = t.tasktypeid
                    where t.docid = :docid
                      and tt.code = 'LOADAUTO'
                      and t.status <> '2')) then
            exception exc_k_common 'Не завершена погрузка паллетов документа в машину!';

        -- Поправим сам док наверные количества
        execute procedure wh_core_setdocbytasklot(:docid,-1);

--        execute procedure uv_sale_taraset(:docid);

        -- Выгружаем
        if (coalesce(:docsubtype,'') not in ('WP','AM')) then
          execute procedure RBS_Q_CREATETASKEXPORT('U3S_SALE_STATUSCHG: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
           returning_values :docid;
    end
end^

SET TERM ; ^

