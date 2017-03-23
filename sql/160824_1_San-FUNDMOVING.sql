

SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_CARGO_CHK_RESERVE (
    DOCID type of column DOCUMENT.DOCID,
    FLAGS VARCHAR(3) = '=')
AS
declare variable wid type of column GWARES.waresid;
declare variable wname type of column GWARES.name;
begin
    if (:flags containing '>=') then
    begin
     select first(1) w.waresid
      from (select cg.waresid as waresid, cg.amount as q
              from imp_cargo cg
             where cg.document = :docid
             union all
            select ir.waresid as waresid, -ir.amount as q
              from imp_reserve ir
             where ir.docid = :docid) w
      group by w.waresid
      having sum(w.q) < -0.00001
       into :wid;
    end
    else if (:flags containing '<=') then
    begin
     select first(1) w.waresid
      from (select cg.waresid as waresid, cg.amount as q
              from imp_cargo cg
             where cg.document = :docid
             union all
            select ir.waresid as waresid, -ir.amount as q
              from imp_reserve ir
             where ir.docid = :docid) w
      group by w.waresid
      having sum(w.q) > 0.00001
       into :wid;
    end
    else if (:flags containing '>') then
    begin
     select first(1) w.waresid
      from (select cg.waresid as waresid, cg.amount as q
              from imp_cargo cg
             where cg.document = :docid
             union all
            select ir.waresid as waresid, -ir.amount as q
              from imp_reserve ir
             where ir.docid = :docid) w
      group by w.waresid
      having sum(w.q) < 0.00001
       into :wid;
    end
    else if (:flags containing '<') then
    begin
     select first(1) w.waresid
      from (select cg.waresid as waresid, cg.amount as q
              from imp_cargo cg
             where cg.document = :docid
             union all
            select ir.waresid as waresid, -ir.amount as q
              from imp_reserve ir
             where ir.docid = :docid) w
      group by w.waresid
      having sum(w.q) > -0.00001
       into :wid;
    end
    else if (:flags containing '=') then
    begin
     select first(1) w.waresid
      from (select cg.waresid as waresid, cg.amount as q
              from imp_cargo cg
             where cg.document = :docid
             union all
            select ir.waresid as waresid, -ir.amount as q
              from imp_reserve ir
             where ir.docid = :docid) w
      group by w.waresid
      having abs(sum(w.q)) > 0.00001
       into :wid;
    end


     if (:wid is NOT NULL) then
     begin
        select g.name
          from gwares g
         where g.waresid = :wid
          into :wname;

        exception exc_wh_reserve :wname || ': в файле количества по документу и по резерву не совпадают!';
     end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_FUNDMOVING_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
begin
    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');
--    execute procedure wh_imp_fundincome_reserve_do(:docid);
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_CARGO_CHK_RESERVE (
    DOCID type of column DOCUMENT.DOCID,
    FLAGS VARCHAR(3) = '=')
AS
declare variable wid type of column GWARES.waresid;
declare variable wname type of column GWARES.name;
begin
    if (:flags containing '>=') then
    begin
     select first(1) w.waresid
      from (select cg.waresid as waresid, cg.amount as q
              from imp_cargo cg
             where cg.document = :docid
             union all
            select ir.waresid as waresid, -ir.amount as q
              from imp_reserve ir
             where ir.docid = :docid) w
      group by w.waresid
      having sum(w.q) < -0.0000001
       into :wid;
    end
    else if (:flags containing '<=') then
    begin
     select first(1) w.waresid
      from (select cg.waresid as waresid, cg.amount as q
              from imp_cargo cg
             where cg.document = :docid
             union all
            select ir.waresid as waresid, -ir.amount as q
              from imp_reserve ir
             where ir.docid = :docid) w
      group by w.waresid
      having sum(w.q) > 0.0000001
       into :wid;
    end
    else if (:flags containing '>') then
    begin
     select first(1) w.waresid
      from (select cg.waresid as waresid, cg.amount as q
              from imp_cargo cg
             where cg.document = :docid
             union all
            select ir.waresid as waresid, -ir.amount as q
              from imp_reserve ir
             where ir.docid = :docid) w
      group by w.waresid
      having sum(w.q) < 0.0000001
       into :wid;
    end
    else if (:flags containing '<') then
    begin
     select first(1) w.waresid
      from (select cg.waresid as waresid, cg.amount as q
              from imp_cargo cg
             where cg.document = :docid
             union all
            select ir.waresid as waresid, -ir.amount as q
              from imp_reserve ir
             where ir.docid = :docid) w
      group by w.waresid
      having sum(w.q) > -0.0000001
       into :wid;
    end
    else if (:flags containing '=') then
    begin
     select first(1) w.waresid
      from (select cg.waresid as waresid, cg.amount as q
              from imp_cargo cg
             where cg.document = :docid
             union all
            select ir.waresid as waresid, -ir.amount as q
              from imp_reserve ir
             where ir.docid = :docid) w
      group by w.waresid
      having abs(sum(w.q)) > 0.0000001
       into :wid;
    end


     if (:wid is NOT NULL) then
     begin
        select g.name
          from gwares g
         where g.waresid = :wid
          into :wname;

        exception exc_wh_reserve :wname || ': в файле количества по документу и по резерву не совпадают!';
     end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDINCOME_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable docstat type of column document.status;
begin
    select d.status
      from document d
     where d.docid = :docid
      into :docstat;

    if (:docstat = 'w') then
    begin
        execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid);
        execute procedure WH_IMP_CARGO_CHK(:docid);

        execute procedure wh_imp_fundincome_reserve_do(:docid);

        update document d
           set d.status = 'e'
         where d.docid = :docid;

        delete from imp_document id
         where id.docid = :docid;
    end
    else
    begin
        exception exc_wh_wrongdocstat;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDINCOME_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable objid type of column OBJECT.objid;
begin
   select d.toobj
     from document d
    where d.docid = :docid
     into :objid;

   insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
   select :docid, ir.waresid, ir.productdate, ir.amount, :objid
     from imp_reserve ir
    where ir.docid = :docid;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_WARES_SALEDBEG (
    WARESID type of column GWARES.waresid,
    CLIENTID type of column OBJECT.objid = NULL,
    ACTUALDATE type of R_DATE = current_date
)
returns (
    DBEG type of R_DATE
)
as
declare variable wdVAL type of R_CUSTOMDATA;
begin
    dbeg = '01.01.2000';

    if (:clientid is NOT NULL) then
    begin
        select val
          from k_get_wares_data_obj_val(NULL,'SALEPERIOD',:waresid, :clientid, :actualdate)
          into :wdval;
        
        if (:wdval is NOT NULL) then
            dbeg = :actualdate - cast(:wdval as integer);
    end

    suspend;
end^

SET TERM ; ^



CREATE UNIQUE INDEX K_WARES_DATATYPE_IDXCODE
ON K_WARES_DATATYPE (CODE);



SET TERM ^ ;

CREATE OR ALTER procedure K_GET_WARES_DATA_OBJ_VAL (
    WDTID type of R_ID,
    WDTCODE type of R_CODE,
    WARESID type of R_ID,
    OBJID type of R_ID,
    FDATE type of R_DATE)
returns (
    VAL type of R_CUSTOMDATA)
AS
begin
    if (:wdtid is NULL and :wdtcode is NOT NULL) then
        select kwdt.id_wares_datatype
          from k_wares_datatype kwdt
         where kwdt.code = :wdtcode
          into :wdtid;

    if (:wdtid is NOT NULL) then
    begin
        if (:fdate is NULL) then
            fdate = current_date;
    
        if (:objid is NOT NULL) then
            select kw."VALUE"
              from k_wares_data_obj kw
             where kw.waresid = :waresid
               and kw.objid = :objid
               and kw.id_wares_datatype = :wdtid
               and :fdate between kw.dbeg and kw.dend
              into :val;
    
        if (:val is NULL) then
            select kw."VALUE"
              from k_wares_data kw
             where kw.waresid = :waresid
               and kw.id_wares_datatype = :wdtid
               and :fdate between kw.dbeg and kw.dend
              into :val;
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARES_SALEDBEG (
    WARESID type of column GWARES.waresid,
    CLIENTID type of column OBJECT.objid = NULL,
    ACTUALDATE type of R_DATE = current_date
)
returns (
    DBEG type of R_DATE
)
as
declare variable wdVAL type of R_CUSTOMDATA;
begin
    dbeg = '01.01.2000';

    if (:clientid is NOT NULL) then
    begin
        select val
          from k_get_wares_data_obj_val(NULL,'SALEPERIOD',:waresid, :clientid, :actualdate)
          into :wdval;
        
        if (:wdval is NOT NULL) then
            dbeg = :actualdate - cast(:wdval as integer);
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_IMP_FUNDMOVING_RESERVE_DO (
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

    if (:iramount > 0.0000001) then
    begin
        select w.dbeg
          from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
          into :saledbeg;

    end
   end
end^

SET TERM ; ^



ALTER TABLE WH_RESERVE
ADD AMOUNTSALE R_DOUBLE
NOT NULL ;



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
    
    if (new.amountsale is NULL) then
        new.amountsale = 0.000;

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

    if (new.amountsale is NULL) then
        new.amountsale = 0.000;
    
    if (new.amount - new.amountsale < -0.0000001) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать меньше резерва под продажу!';

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

  if (new.amount - new.amountsale < -0.0000001) then
    exception exc_wh_reserve 'Ќельз€ зарезервировать меньше резерва под продажу!';

end^

SET TERM ; ^



ALTER TABLE WH_RESERVE
ADD AMOUNTFREE R_DOUBLE
NOT NULL ;



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

    if (new.amountsale is NULL) then
        new.amountsale = 0.000;
    
    if (new.amount - new.amountsale < -0.0000001) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать меньше резерва под продажу!';

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
    
    new.amountfree = new.amount - new.amountsale;

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

  if (new.amount - new.amountsale < -0.0000001) then
    exception exc_wh_reserve 'Ќельз€ зарезервировать меньше резерва под продажу!';

  new.amountfree = new.amount - new.amountsale;

end^

SET TERM ; ^



CREATE INDEX WH_RESERVE_IDX_OWDATEFREE
ON WH_RESERVE (OBJID,WARESID,PRODUCTDATE,AMOUNTFREE);



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
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDMOVING_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
begin
    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');
    execute procedure wh_imp_fundmoving_reserve_do(:docid);
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_IMP_DOC_TRANSFER (
    DOCID type of column DOCUMENT.docid
)
as
begin
    if (exists(select *
                 from document d
                where d.docid = :docid)) then
    begin

    end
    else
    begin
        insert into document ( DOCID, DOCTYPE, DOCDATE, NUMBER, FROMOBJ, THROUGHOBJ, TOOBJ, AMOUNT, DESCRIPT, REALDOCDATE, STATUS, REASON, DOCSUBTYPE, DELAY, NUMBERLINK, EXTERNALINTID)
        select id.docid, id.doctype, id.docdate, id.number, id.fromobj, id.throughobj, id.toobj, id.amount, id.descript, id.realdocdate, id.status, id.realdocdate, id.docsubtype, id.descript, id.numberlink, id.externalintid
          from imp_document id
         where id.docid = :docid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_DOC_TRANSFER (
    DOCID type of column DOCUMENT.docid
)
as
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

