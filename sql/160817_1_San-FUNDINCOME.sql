

SET TERM ^ ;

create procedure Q_EXP_CARGO_FUNDINCOME_PRDATE (
    DOCID type of column DOCUMENT.DOCID,
    WARESID type of column GWARES.WARESID)
returns (
    Q type of column WM_TASK_LOT.QUANTITY,
    PRDATE type of column WARESLOT.PRODUCTDATE)
AS
begin
    select d.realdocdate
      from DOCUMENT d
     where d.docid = :docid
      into :prdate;

    select cg.amount
      from cargo cg
     where cg.document = :docid
       and cg.waresid = :waresid
       and cg.cargo2id is NULL
      into :q;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure Q_EXP_CARGO_FUNDINCOME_PRDATE (
    DOCID type of column DOCUMENT.DOCID,
    WARESID type of column GWARES.WARESID)
returns (
    Q type of column CARGO.AMOUNT,
    PRDATE type of column WARESLOT.PRODUCTDATE)
AS
begin
    select d.realdocdate
      from DOCUMENT d
     where d.docid = :docid
      into :prdate;

    select cg.amount
      from cargo cg
     where cg.document = :docid
       and cg.waresid = :waresid
       and cg.cargo2id is NULL
      into :q;

    suspend;
end^

SET TERM ; ^



CREATE TABLE WH_RESERVE (
    WARESID R_ID,
    PRODUCTDATE R_DATE,
    AMOUNT R_DOUBLE,
    OBJID R_ID,
    ID R_ID NOT NULL);

ALTER TABLE WH_RESERVE
ADD CONSTRAINT PK_WH_RESERVE
PRIMARY KEY (ID);

CREATE SEQUENCE GEN_WH_RESERVE_ID;



ALTER TABLE WH_RESERVE
ADD CONSTRAINT FK_WH_RESERVE_WID
FOREIGN KEY (WARESID)
REFERENCES GWARES(WARESID)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE WH_RESERVE
ADD CONSTRAINT FK_WH_RESERVE_OID
FOREIGN KEY (OBJID)
REFERENCES OBJECT(OBJID)
ON DELETE CASCADE
ON UPDATE CASCADE;



update RDB$RELATION_FIELDS set
RDB$NULL_FLAG = 1
where (RDB$FIELD_NAME = 'WARESID') and
(RDB$RELATION_NAME = 'WH_RESERVE')
;



update RDB$RELATION_FIELDS set
RDB$NULL_FLAG = 1
where (RDB$FIELD_NAME = 'OBJID') and
(RDB$RELATION_NAME = 'WH_RESERVE')
;



update RDB$RELATION_FIELDS set
RDB$NULL_FLAG = 1
where (RDB$FIELD_NAME = 'AMOUNT') and
(RDB$RELATION_NAME = 'WH_RESERVE')
;



update RDB$RELATION_FIELDS set
RDB$NULL_FLAG = 1
where (RDB$FIELD_NAME = 'PRODUCTDATE') and
(RDB$RELATION_NAME = 'WH_RESERVE')
;



SET TERM ^ ;

create trigger wh_reserve_bi for wh_reserve
active before insert position 0
as
begin
  if (new.id is null) then
    new.id = gen_id(gen_wh_reserve_id,1);
end^

SET TERM ; ^



CREATE EXCEPTION EXC_WH_RESERVE 'ќшибка резерва';



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_bi for wh_reserve
active before insert position 0
as
declare variable wliamount type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
begin
  select sum(wli.amount)
    from wareslot wl
         left join wareslotitem wli on wli.wlotid = wl.wlotid
   where wl.objid = new.objid
     and wl.waresid = new.waresid
     and wl.productdate = new.productdate
    into :wliamount;

  select sum(r.amount)
    from wh_reserve r
   where r.waresid = new.waresid
     and r.productdate = new.productdate
    into :ramount;

  if (:wliamount - :ramount - new.amount < -0.000001) then
    exception exc_wh_reserve 'Ќельз€ рарезервировать больше остатка!';

  if (new.id is null) then
    new.id = gen_id(gen_wh_reserve_id,1);
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_bi for wh_reserve
active before insert position 0
as
declare variable wliamount type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
begin
  select sum(wli.amount)
    from wareslot wl
         left join wareslotitem wli on wli.wlotid = wl.wlotid
   where wl.objid = new.objid
     and wl.waresid = new.waresid
     and wl.productdate = new.productdate
    into :wliamount;

  select sum(r.amount)
    from wh_reserve r
   where r.waresid = new.waresid
     and r.productdate = new.productdate
    into :ramount;

  if (:wliamount - :ramount - new.amount < -0.000001) then
    exception exc_wh_reserve 'Ќельз€ зарезервировать больше остатка!';

  if (new.id is null) then
    new.id = gen_id(gen_wh_reserve_id,1);
end^

SET TERM ; ^



SET TERM ^ ;

CREATE trigger wh_reserve_bu0 for wh_reserve
active before update position 0
as
declare variable wliamount type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
begin
  if (old.amount - new.amount < -0.00001) then
  begin
      select sum(wli.amount)
        from wareslot wl
             left join wareslotitem wli on wli.wlotid = wl.wlotid
       where wl.objid = new.objid
         and wl.waresid = new.waresid
         and wl.productdate = new.productdate
        into :wliamount;

      select sum(r.amount)
        from wh_reserve r
       where r.waresid = new.waresid
         and r.productdate = new.productdate
        into :ramount;

      if (:wliamount - :ramount + old.amount - new.amount < -0.000001) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать больше остатка!';

  end
end^

SET TERM ; ^



CREATE TABLE IMP_RESERVE (
    DOCID R_ID64 NOT NULL,
    WARESID R_ID NOT NULL,
    PRODUCTDATE R_DATE,
    AMOUNT R_DOUBLE NOT NULL,
    ID R_ID NOT NULL);

ALTER TABLE IMP_RESERVE
ADD CONSTRAINT PK_IMP_RESERVE
PRIMARY KEY (ID);

CREATE SEQUENCE GEN_IMP_RESERVE_ID;

SET TERM ^ ;

create trigger imp_reserve_bi for imp_reserve
active before insert position 0
as
begin
  if (new.id is null) then
    new.id = gen_id(gen_imp_reserve_id,1);
end^

SET TERM ; ^



ALTER TABLE IMP_RESERVE
ADD CONSTRAINT FK_IMP_RESERVE_DOCID
FOREIGN KEY (DOCID)
REFERENCES DOCUMENT(DOCID)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE IMP_RESERVE
ADD CONSTRAINT FK_IMP_RESERVE_WARESID
FOREIGN KEY (WARESID)
REFERENCES GWARES(WARESID)
ON DELETE CASCADE
ON UPDATE CASCADE;



CREATE TABLE WH_RESERVE_CHANGES (
    DOCID R_ID64,
    WARESID R_ID NOT NULL,
    PRODUCTDATE R_DATE NOT NULL,
    AMOUNT R_DOUBLE NOT NULL,
    OBJID R_ID NOT NULL,
    ID INTEGER NOT NULL);

ALTER TABLE WH_RESERVE_CHANGES
ADD CONSTRAINT PK_WH_RESERVE_CHANGES
PRIMARY KEY (ID);

CREATE SEQUENCE GEN_WH_RESERVE_CHANGES_ID;

SET TERM ^ ;

create trigger wh_reserve_changes_bi for wh_reserve_changes
active before insert position 0
as
begin
  if (new.id is null) then
    new.id = gen_id(gen_wh_reserve_changes_id,1);
end^

SET TERM ; ^



ALTER TABLE WH_RESERVE_CHANGES
ADD CONSTRAINT FK_WH_RESERVE_CHANGES_DOCID
FOREIGN KEY (DOCID)
REFERENCES DOCUMENT(DOCID)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE WH_RESERVE_CHANGES
ADD CONSTRAINT FK_WH_RESERVE_CHANGES_WARESID
FOREIGN KEY (WARESID)
REFERENCES GWARES(WARESID)
ON DELETE CASCADE
ON UPDATE CASCADE;



ALTER TABLE WH_RESERVE_CHANGES
ADD CONSTRAINT FK_WH_RESERVE_CHANGES_OBJID
FOREIGN KEY (OBJID)
REFERENCES OBJECT(OBJID)
ON DELETE CASCADE
ON UPDATE CASCADE;



SET TERM ^ ;

CREATE trigger wh_reserve_changes_ai0 for wh_reserve_changes
active after insert position 0
AS
declare variable reserveid type of column wh_reserve.id;
begin
    select r.id
      from wh_reserve r
     where r.objid = new.objid
       and r.waresid = new.waresid
       and r.productdate = new.productdate
      into :reserveid;

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

CREATE OR ALTER trigger wh_reserve_bi for wh_reserve
active before insert position 0
as
declare variable wliamount type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
begin
    if (new.amount < -0.0001) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать отрицательное количество!';

    select sum(wli.amount)
      from wareslot wl
           left join wareslotitem wli on wli.wlotid = wl.wlotid
     where wl.objid = new.objid
       and wl.waresid = new.waresid
       and wl.productdate = new.productdate
      into :wliamount;
    
    select sum(r.amount)
      from wh_reserve r
     where r.waresid = new.waresid
       and r.productdate = new.productdate
      into :ramount;
    
    if (:wliamount - :ramount - new.amount < -0.000001) then
      exception exc_wh_reserve 'Ќельз€ зарезервировать больше остатка!';
    
    if (new.id is null) then
      new.id = gen_id(gen_wh_reserve_id,1);
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_bu0 for wh_reserve
active before update position 0
as
declare variable wliamount type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
begin
  if (new.amount < -0.0001) then
      exception exc_wh_reserve 'Ќельз€ зарезервировать отрицательное количество!';

  if (old.amount - new.amount < -0.00001) then
  begin
      select sum(wli.amount)
        from wareslot wl
             left join wareslotitem wli on wli.wlotid = wl.wlotid
       where wl.objid = new.objid
         and wl.waresid = new.waresid
         and wl.productdate = new.productdate
        into :wliamount;

      select sum(r.amount)
        from wh_reserve r
       where r.waresid = new.waresid
         and r.productdate = new.productdate
        into :ramount;

      if (:wliamount - :ramount + old.amount - new.amount < -0.000001) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать больше остатка!';

  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE trigger wh_reserve_au0 for wh_reserve
active after update position 0
AS
begin
    if (new.amount < 0.000001) then
        delete from wh_reserve r
         where r.id = new.id;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_bi for wh_reserve
active before insert position 0
as
declare variable wliamount type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
begin
    if (new.amount < -0.0001) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать отрицательное количество!';

    if (new.amount < 0.0001) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать нулевое количество!';

    select sum(wli.amount)
      from wareslot wl
           left join wareslotitem wli on wli.wlotid = wl.wlotid
     where wl.objid = new.objid
       and wl.waresid = new.waresid
       and wl.productdate = new.productdate
      into :wliamount;
    
    select sum(r.amount)
      from wh_reserve r
     where r.waresid = new.waresid
       and r.productdate = new.productdate
      into :ramount;
    
    if (:wliamount - :ramount - new.amount < -0.000001) then
      exception exc_wh_reserve 'Ќельз€ зарезервировать больше остатка!';
    
    if (new.id is null) then
      new.id = gen_id(gen_wh_reserve_id,1);
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_bi for wh_reserve
active before insert position 0
as
declare variable wliamount type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
begin
    if (new.amount < -0.0001) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать отрицательное количество!';

    if (new.amount < 0.0001) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать нулевое количество!';

    select sum(wli.amount)
      from wareslot wl
           left join wareslotitem wli on wli.wlotid = wl.wlotid
     where wl.objid = new.objid
       and wl.waresid = new.waresid
       and wl.productdate = new.productdate
      into :wliamount;
    if (:wliamount is NULL) then
        wliamount = 0.000;
    
    select sum(r.amount)
      from wh_reserve r
     where r.waresid = new.waresid
       and r.productdate = new.productdate
      into :ramount;
    if (:ramount is NULL) then
        ramount = 0.000;

    if (:wliamount - :ramount - new.amount < -0.000001) then
      exception exc_wh_reserve 'Ќельз€ зарезервировать больше остатка!';
    
    if (new.id is null) then
      new.id = gen_id(gen_wh_reserve_id,1);
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_bu0 for wh_reserve
active before update position 0
as
declare variable wliamount type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
begin
  if (new.amount < -0.0001) then
      exception exc_wh_reserve 'Ќельз€ зарезервировать отрицательное количество!';

  if (old.amount - new.amount < -0.00001) then
  begin
      select sum(wli.amount)
        from wareslot wl
             left join wareslotitem wli on wli.wlotid = wl.wlotid
       where wl.objid = new.objid
         and wl.waresid = new.waresid
         and wl.productdate = new.productdate
        into :wliamount;
      if (:wliamount is NULL) then
          wliamount = 0.000;

      select sum(r.amount)
        from wh_reserve r
       where r.waresid = new.waresid
         and r.productdate = new.productdate
        into :ramount;
      if (:ramount is NULL) then
          ramount = 0.000;

      if (:wliamount - :ramount + old.amount - new.amount < -0.000001) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать больше остатка!';

  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE trigger wh_reserve_changes_au0 for wh_reserve_changes
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
        select r.id
          from wh_reserve r
         where r.objid = old.objid
           and r.waresid = old.waresid
           and r.productdate = old.productdate
          into :reserveid;

        if (:reserveid is NULL) then
            insert into wh_reserve ( WARESID, PRODUCTDATE, AMOUNT, OBJID)
            values ( old.waresid, old.productdate, - old.amount, old.objid);
        else
            update wh_reserve r
               set r.amount = r.amount + - old.amount
             where r.id = :reserveid;

        reserveid = NULL;
        select r.id
          from wh_reserve r
         where r.objid = new.objid
           and r.waresid = new.waresid
           and r.productdate = new.productdate
          into :reserveid;

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
        select r.id
          from wh_reserve r
         where r.objid = new.objid
           and r.waresid = new.waresid
           and r.productdate = new.productdate
          into :reserveid;

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
    select r.id
      from wh_reserve r
     where r.objid = old.objid
       and r.waresid = old.waresid
       and r.productdate = old.productdate
      into :reserveid;

    if (:reserveid is NULL) then
        insert into wh_reserve ( WARESID, PRODUCTDATE, AMOUNT, OBJID)
        values ( old.waresid, old.productdate, - old.amount, old.objid);
    else
        update wh_reserve r
           set r.amount = r.amount - old.amount
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
        select r.id
          from wh_reserve r
         where r.objid = old.objid
           and r.waresid = old.waresid
           and r.productdate = old.productdate
          into :reserveid;

        if (:reserveid is NULL) then
            insert into wh_reserve ( WARESID, PRODUCTDATE, AMOUNT, OBJID)
            values ( old.waresid, old.productdate, - old.amount, old.objid);
        else
            update wh_reserve r
               set r.amount = r.amount - old.amount
             where r.id = :reserveid;

        reserveid = NULL;
        select r.id
          from wh_reserve r
         where r.objid = new.objid
           and r.waresid = new.waresid
           and r.productdate = new.productdate
          into :reserveid;

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
        select r.id
          from wh_reserve r
         where r.objid = new.objid
           and r.waresid = new.waresid
           and r.productdate = new.productdate
          into :reserveid;

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



CREATE TABLE WH_RESERVE_OBJECTS (
    OBJID R_ID NOT NULL,
    DESCRIPT R_VARCHAR255);

ALTER TABLE WH_RESERVE_OBJECTS
ADD CONSTRAINT PK_WH_RESERVE_OBJECTS
PRIMARY KEY (OBJID);



ALTER TABLE WH_RESERVE_OBJECTS
ADD CONSTRAINT FK_WH_RESERVE_OBJECTS_OBJID
FOREIGN KEY (OBJID)
REFERENCES OBJECT(OBJID)
ON DELETE CASCADE
ON UPDATE CASCADE;



ALTER TABLE WH_RESERVE_CHANGES
ADD DATETIME R_DATETIME
NOT NULL ;



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_changes_bi for wh_reserve_changes
active before insert position 0
as
begin
  if (not exists(select *
                   from wh_reserve_objects o
                  where o.objid = new.objid)) then
    exception exc_wh_reserve '”казанного объекта нет в списке разрешенных дл€ резервировани€!';

  if (new.id is null) then
    new.id = gen_id(gen_wh_reserve_changes_id,1);

  if (new.datetime is NULL) then
    new.datetime = current_timestamp;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_IMP_FUNDINCOME_RESERVE_DO (
    DOCID type of column DOCUMENT.docid
)
as
declare variable objid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable productdate type of column WARESLOT.productdate;
declare variable amount type of column WH_RESERVE.amount;
begin
    select d.toobj
      from document d
     where d.docid = :docid
      into :objid;

    for
        select ir.waresid, ir.productdate, ir.amount
          from imp_reserve ir
         where ir.docid = :docid
          into :waresid, :productdate, :amount
    do
    begin
       insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
       values ( :docid, :waresid, :productdate, :amount, :objid);
    end

    delete from imp_reserve ir
     where ir.docid = :docid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_DOCTYPE_BY_CODE (
    DTCODE type of column doctype.code,
    FLAGS varchar(10))
returns (
    DTID type of column doctype.doctid,
    DTNAME type of column doctype.name)
AS
begin
  IF (Substr(:Flags, 1, 1) = '') THEN Flags = '1';

  select dt.doctid,dt.name
    from doctype dt
   where dt.code = :dtcode
    into :dtid,:dtname;

  if (:dtid is NULL and Substr(:Flags, 1, 1)='1') then
    exception exc_ur_common 'Ќе найден тип документа с кодом: '||:dtcode;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_DTID_FUNDINCOME(
    flags varchar(10) = ''
)
returns (
    DTID type of column doctype.doctid)
AS
begin
    select k.dtid
      from k_doctype_by_code('FUNDINCOME',:flags) k
      into :dtid;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_DTID_INORDER
returns (
    DTID type of column doctype.doctid)
AS
begin
    select k.dtid
      from k_doctype_by_code('INORDER',NULL) k
      into :dtid;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_INCOMEFG_BYPALLET_FUNDINCOME (
    producerid type of column OBJECT.objid,
    whid type of column OBJECT.objid,
    waresid type of column GWARES.waresid,
    PRODUCTDATE type of R_DATE,
    quantity type of r_quantity
)
as
declare variable dtid_fundincome type of column doctype.doctid;
declare variable docid type of column DOCUMENT.docid;
declare variable docstat type of column r_status.code;
declare variable cargoid type of column cargo.cargoid;
begin
    execute procedure wh_dtid_fundincome('0')
     returning_values :dtid_fundincome;

    if (:dtid_fundincome is NOT NULL) then
    begin
        select first(1) d.docid, d.status
          from document d
         where d.doctype = :dtid_fundincome
           and d.fromobj = :producerid
           and d.toobj = :whid
           and d.realdocdate = :productdate
          into :docid, :docstat;
    
        if (:docid is NULL) then
        begin
            select k.docid
              from k_doccreate(:producerid, :whid, NULL, :dtid_fundincome,
                               current_date, :productdate,
                               NULL, NULL, null, NULL, NULL) k
              into :docid;
    
            update document d
               set d.status = 'c'
             where d.docid = :docid;
        end
        else if (:docstat <> 'C') then
        begin
            exception exc_wh_reserve 'Ќе верный статус документа прихода резерва!';
        end

        execute procedure k_get_cargoid(:docid, :waresid)
          returning_values :cargoid;

        if (:cargoid is NULL) then
            insert into cargo(document, waresid, amount, price)
            values(:docid, :waresid, :quantity, 0.000);
        else
            update cargo cg
               set cg.amount = cg.amount + :quantity
             where cg.cargoid = :cargoid;

    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYPALLET (
    PBARCODE type of R_BARCODE,
    QUANTITY type of R_DOUBLE,
    IDUSER type of R_ID,
    DTBEG type of R_DATETIME = current_timestamp,
    FEATUREID type of R_ID = null)
AS
declare variable productdate r_date;
declare variable waresid r_id;
declare variable qplan r_double;
declare variable producerid r_id;
declare variable manid r_id;
declare variable mansiteid r_id;
declare variable zoneid r_id;
declare variable whid r_id;
declare variable ttid_income r_id;
declare variable taskid r_id;
declare variable wmsid r_id;
declare variable taskwaresid r_id;
declare variable pnumber r_barcode;
declare variable ptypeid_finishgood r_id;
declare variable palletid r_id;
declare variable wlincomeid r_id;
declare variable wlotid r_id;
declare variable dtid_income r_id;
declare variable docid r_id64;
declare variable cargoid r_id;
begin
    if (:quantity is NULL) then
        exception exc_wh_wrongamount;

    select wh.zoneid, wh.whid, wh.manid
      from wh_user_infoshort(:iduser) wh
      into :zoneid, :whid, :manid;

    select pfp.productdate, pfp.waresid, pfp.quantity, pfp.producerid, pfp.number,
           coalesce(pfp.dtid_income, pl.dtid_income, p.dtid_income_print, p.dtid_income)
      from pallet_finishprint pfp
           left join fg_producer p on p.objid = pfp.producerid
           left join fg_prodlines pl on pl.id_prodline = pfp.prodlineid
     where pfp.barcode = :pbarcode and pfp.enabled = '1'
      into :productdate, :waresid, :qplan, :producerid, :pnumber, :dtid_income;

    execute procedure WH_INCOMEFG_BYPALLET_FUNDINCOME(:producerid, :whid, :productdate, :waresid, :quantity);
    select k.sid
      from k_get_user_wmsessionid(:manid, 'M') k
      into :wmsid;

    select m.siteid
      from wh_man_getsite(:manid) m
      into :mansiteid;

    execute procedure wh_ttid_incomefg
     returning_values :ttid_income;

    insert into wm_task(tasktypeid, zoneid, status, siteid)
    values(:ttid_income, :zoneid, '0', :mansiteid)
    returning taskid
    into :taskid;

    select wh.id
      from wh_paltypeid_finishgood wh
      into :ptypeid_finishgood;

    insert into pallet(ptypeid, barcode, number, siteid, zoneid, objid)
    values(:ptypeid_finishgood, :pbarcode, :pnumber, :mansiteid, :zoneid, :whid)
    returning palletid
    into :palletid;
    execute procedure wh_pallet_feature_set(:palletid, :featureid, :manid, 'M');

    update wm_task t
       set t.wm_sessionid = :wmsid, t.begintime = :dtbeg, t.status = '1'
     where t.taskid = :taskid;

    insert into wm_task_pallet(taskid, palletid, status)
    values(:taskid, :palletid, '2');

    update or insert into wareslot(objid, zoneid, waresid, productdate, status)
    values(:whid, :zoneid, :waresid, :productdate, '1')
    matching(objid, zoneid, waresid, productdate)
    returning wlotid
    into :wlotid;

    select first(1) d.docid
      from document d
     where d.doctype = :dtid_income
       and d.fromobj = :producerid
       and d.toobj = :whid
       and d.status = 'c'
       and d.docdate = cast(:dtbeg as date)
      into :docid;

    if (:docid is NULL) then
    begin
        select k.docid
          from k_doccreate(:producerid, :whid, NULL, :dtid_income,
                           cast(:dtbeg as date), cast(:dtbeg as date),
                           NULL, NULL, null, NULL, NULL) k
          into :docid;

        update document d
           set d.status = 'c'
         where d.docid = :docid;
    end

    update or insert into wareslotincomes(docid, wlotid)
    values(:docid, :wlotid)
    matching(docid, wlotid)
    returning id
    into :wlincomeid;

    insert into wm_task_wares(taskid, waresid, status, wm_sessionid, successscan, quantity, begintime)
    values(:taskid, :waresid, '1', :wmsid, :qplan, :quantity, :dtbeg)
    returning taskwaresid
    into :taskwaresid;

    insert into wm_task_lot(palletid,  wlotid, taskwaresid, chgwli, wlincomeid, quantity)
    values(:palletid, :wlotid, :taskwaresid, '1', :wlincomeid, :quantity);

    update wm_task_wares tw
       set tw.status='2',tw.endtime = current_timestamp
     where tw.taskwaresid = :taskwaresid;

    update wm_task t
       set t.status = '2',t.docid = :docid
     where t.taskid = :taskid;

    execute procedure k_get_cargoid(:docid, :waresid)
      returning_values :cargoid;

    if (:cargoid is NULL) then
        insert into cargo(document, waresid, amount, price)
        values(:docid, :waresid, :quantity, 0.000);
    else
        update cargo cg
           set cg.amount = cg.amount + :quantity
         where cg.cargoid = :cargoid;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYPALLET (
    PBARCODE type of R_BARCODE,
    QUANTITY type of R_DOUBLE,
    IDUSER type of R_ID,
    DTBEG type of R_DATETIME = current_timestamp,
    FEATUREID type of R_ID = null)
AS
declare variable productdate r_date;
declare variable waresid r_id;
declare variable qplan r_double;
declare variable producerid r_id;
declare variable manid r_id;
declare variable mansiteid r_id;
declare variable zoneid r_id;
declare variable whid r_id;
declare variable ttid_income r_id;
declare variable taskid r_id;
declare variable wmsid r_id;
declare variable taskwaresid r_id;
declare variable pnumber r_barcode;
declare variable ptypeid_finishgood r_id;
declare variable palletid r_id;
declare variable wlincomeid r_id;
declare variable wlotid r_id;
declare variable dtid_income r_id;
declare variable docid r_id64;
declare variable cargoid r_id;
begin
    if (:quantity is NULL) then
        exception exc_wh_wrongamount;

    select wh.zoneid, wh.whid, wh.manid
      from wh_user_infoshort(:iduser) wh
      into :zoneid, :whid, :manid;

    select pfp.productdate, pfp.waresid, pfp.quantity, pfp.producerid, pfp.number,
           coalesce(pfp.dtid_income, pl.dtid_income, p.dtid_income_print, p.dtid_income)
      from pallet_finishprint pfp
           left join fg_producer p on p.objid = pfp.producerid
           left join fg_prodlines pl on pl.id_prodline = pfp.prodlineid
     where pfp.barcode = :pbarcode and pfp.enabled = '1'
      into :productdate, :waresid, :qplan, :producerid, :pnumber, :dtid_income;

    execute procedure WH_INCOMEFG_BYPALLET_FUNDINCOME(:producerid, :whid, :waresid, :productdate, :quantity);
    select k.sid
      from k_get_user_wmsessionid(:manid, 'M') k
      into :wmsid;

    select m.siteid
      from wh_man_getsite(:manid) m
      into :mansiteid;

    execute procedure wh_ttid_incomefg
     returning_values :ttid_income;

    insert into wm_task(tasktypeid, zoneid, status, siteid)
    values(:ttid_income, :zoneid, '0', :mansiteid)
    returning taskid
    into :taskid;

    select wh.id
      from wh_paltypeid_finishgood wh
      into :ptypeid_finishgood;

    insert into pallet(ptypeid, barcode, number, siteid, zoneid, objid)
    values(:ptypeid_finishgood, :pbarcode, :pnumber, :mansiteid, :zoneid, :whid)
    returning palletid
    into :palletid;
    execute procedure wh_pallet_feature_set(:palletid, :featureid, :manid, 'M');

    update wm_task t
       set t.wm_sessionid = :wmsid, t.begintime = :dtbeg, t.status = '1'
     where t.taskid = :taskid;

    insert into wm_task_pallet(taskid, palletid, status)
    values(:taskid, :palletid, '2');

    update or insert into wareslot(objid, zoneid, waresid, productdate, status)
    values(:whid, :zoneid, :waresid, :productdate, '1')
    matching(objid, zoneid, waresid, productdate)
    returning wlotid
    into :wlotid;

    select first(1) d.docid
      from document d
     where d.doctype = :dtid_income
       and d.fromobj = :producerid
       and d.toobj = :whid
       and d.status = 'c'
       and d.docdate = cast(:dtbeg as date)
      into :docid;

    if (:docid is NULL) then
    begin
        select k.docid
          from k_doccreate(:producerid, :whid, NULL, :dtid_income,
                           cast(:dtbeg as date), cast(:dtbeg as date),
                           NULL, NULL, null, NULL, NULL) k
          into :docid;

        update document d
           set d.status = 'c'
         where d.docid = :docid;
    end

    update or insert into wareslotincomes(docid, wlotid)
    values(:docid, :wlotid)
    matching(docid, wlotid)
    returning id
    into :wlincomeid;

    insert into wm_task_wares(taskid, waresid, status, wm_sessionid, successscan, quantity, begintime)
    values(:taskid, :waresid, '1', :wmsid, :qplan, :quantity, :dtbeg)
    returning taskwaresid
    into :taskwaresid;

    insert into wm_task_lot(palletid,  wlotid, taskwaresid, chgwli, wlincomeid, quantity)
    values(:palletid, :wlotid, :taskwaresid, '1', :wlincomeid, :quantity);

    update wm_task_wares tw
       set tw.status='2',tw.endtime = current_timestamp
     where tw.taskwaresid = :taskwaresid;

    update wm_task t
       set t.status = '2',t.docid = :docid
     where t.taskid = :taskid;

    execute procedure k_get_cargoid(:docid, :waresid)
      returning_values :cargoid;

    if (:cargoid is NULL) then
        insert into cargo(document, waresid, amount, price)
        values(:docid, :waresid, :quantity, 0.000);
    else
        update cargo cg
           set cg.amount = cg.amount + :quantity
         where cg.cargoid = :cargoid;

end^

SET TERM ; ^



ALTER SEQUENCE G_DOCTOBJID RESTART WITH 64;

