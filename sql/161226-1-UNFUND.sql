

SET TERM ^ ;

create procedure WH_DOC_UNFUND(
    DOCID type of column DOCUMENT.docid
)
as
declare variable dtCode type of column DOCTYPE.code;
declare variable fromobj type of column OBJECT.objid;
declare variable toobj type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable productdate type of column wh_reserve.productdate;
declare variable amount type of column wh_reserve.amount;
declare variable amountbad type of column wh_reserve.amountbad;
begin
    select d.fromobj, d.toobj, dt.code
      from document d
           left join doctype dt on dt.doctid = d.doctype
     where d.docid = :docid
      into :fromobj, :toobj, :dtCode;

    if (:dtcode not in ('FUNDMOVING')) then
        exception exc_wh_wrongdoctype;

    for
        with pre as(
            select rc.objid, rc.waresid, rc.productdate, sum(rc.amount) as amount, sum(rc.amountbad) as amountbad
              from wh_reserve_changes rc
             where rc.docid = :docid
               and rc.objid = :toobj
             group by rc.objid, rc.waresid, rc.productdate, rc.objid
            having sum(rc.amount) > 0.0001 or sum(rc.amountbad) > 0.0001
        )
        select pre.waresid, pre.productdate, pre.amount, pre.amountbad
          from pre
               left join wh_reserve r
                 on r.objid = pre.objid and r.productdate = pre.productdate and r.waresid = pre.waresid
         where coalesce(r.amountfree, 0.000) - pre.amount > -0.0001
           and coalesce(r.amountbad, 0.000) - pre.amountbad > -0.0001
          into :waresid, :productdate, :amount, :amountbad
    do
    begin
        insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
        values ( :docid, :waresid, :productdate, -:amount, :toobj, -:amountbad);
        
        insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
        values ( :docid, :waresid, :productdate, :amount, :fromobj, :amountbad);

        update cargo cg
           set cg.amount = cg.amount - :amount, cg.docsum = NULL
         where cg.document = :docid and cg.waresid = :waresid;
    end

    if (not exists(select *
                     from cargo cg
                    where cg.document = :docid
                      and cg.amount > 0.0001)) then
    begin
        update document d
           set d.status = 'У', d.descript = 'Удаление зависших резервов'
         where d.docid = :docid;
    end
    else
    begin
        update document d
           set d.descript = 'Удаление зависших резервов'
         where d.docid = :docid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDINCOME_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
--declare variable objid type of column OBJECT.objid;
begin
/*   select d.toobj
     from document d
    where d.docid = :docid
     into :objid;

   insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
   select :docid, ir.waresid, ir.productdate, ir.amount, :objid
     from imp_reserve ir
    where ir.docid = :docid;*/

   insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
   with w as(
       select d.docid as docid, cg.waresid as waresid, cast(d.realdocdate as r_date) as productdate, cg.amount as amount, d.toobj as whid
         from document d
              left join cargo cg on cg.document = d.docid
        where d.docid = :docid
          and cg.cargoid is NOT NULL
        union all
       select rc.docid as docid, rc.waresid as waresid, rc.productdate as productdate, -rc.amount as amount, rc.objid as whid
         from wh_reserve_changes rc
        where rc.docid = :docid
    )
   select w.docid, w.waresid, w.productdate, sum(w.amount), w.whid
     from w
    group by w.docid, w.waresid, w.productdate, w.whid
   having abs(sum(w.amount)) > 0.0001;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_bu0 for wh_reserve
active before update position 0
as
declare variable wliamount type of column wareslotitem.amount;
declare variable wliamount_bad type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
declare variable ramount_bad type of column wh_reserve.amountbad;
declare variable ptypeid_cr type of column pallet_type.id;
declare variable excmes type of r_exceptionusermes;
begin
  if (new.amountbad is NULL) then
      new.amountbad = 0.000;

  if (new.amount < -0.0001 or new.amountbad < -0.0001) then
      exception exc_wh_reserve 'Нельзя зарезервировать отрицательное количество!';

  if (old.amount - new.amount < -0.00001 or old.amountbad - new.amountbad < -0.00001 ) then
  begin
    select w.id
      from WH_PALTYPEID_COMERETURN w
      into :ptypeid_cr;

        select sum(
                case
                    when p.ptypeid = :ptypeid_cr then 0.000
                    else wli.amount
                end
               ),
               sum(
                case
                    when p.ptypeid = :ptypeid_cr then wli.amount
                    else 0.000
                end
               )
          from wareslot wl
               left join wareslotitem wli
                    left join pallet p
                      on p.palletid = wli.palletid
                 on wli.wlotid = wl.wlotid
         where wl.waresid = new.waresid
           and wl.productdate = new.productdate
           and wl.status = '1'
          into :wliamount, :wliamount_bad;
        if (:wliamount is NULL) then
            wliamount = 0.000;
        if (:wliamount_bad is NULL) then
            wliamount_bad = 0.000;

        select sum(r.amount), sum(r.amountbad)
          from wh_reserve r
         where r.waresid = new.waresid
           and r.productdate = new.productdate
          into :ramount, :ramount_bad;
        if (:ramount is NULL) then
            ramount = 0.000;
        if (:ramount_bad is NULL) then
            ramount_bad = 0.000;

/*        if (:wliamount - :ramount + old.amount - new.amount < -0.000001) then
          exception exc_wh_reserve 'Нельзя зарезервировать больше остатка!';*/

        if (:wliamount_bad - :ramount_bad + old.amountbad - new.amountbad < -0.000001) then
          exception exc_wh_reserve 'Нельзя зарезервировать больше остатка!';
  end

  if (new.amount - new.amountsale < -0.0000001) then
  begin
    execute procedure WH_WARES_EXCTEXT(new.waresid, 'Нельзя зарезервировать меньше резерва под продажу: :wares:!')
     returning_values :excmes;
    exception exc_wh_reserve :excmes;
  end

  new.amountfree = new.amount - new.amountsale;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_bu0 for wh_reserve
active before update position 0
as
declare variable wliamount type of column wareslotitem.amount;
declare variable wliamount_bad type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
declare variable ramount_bad type of column wh_reserve.amountbad;
declare variable ptypeid_cr type of column pallet_type.id;
declare variable excmes type of r_exceptionusermes;
begin
  if (new.amountbad is NULL) then
      new.amountbad = 0.000;

  if (new.amount < -0.0001 or new.amountbad < -0.0001) then
      exception exc_wh_reserve 'Нельзя зарезервировать отрицательное количество!';

  if (old.amount - new.amount < -0.00001 or old.amountbad - new.amountbad < -0.00001 ) then
  begin
    select w.id
      from WH_PALTYPEID_COMERETURN w
      into :ptypeid_cr;

        select sum(
                case
                    when p.ptypeid = :ptypeid_cr then 0.000
                    else wli.amount
                end
               ),
               sum(
                case
                    when p.ptypeid = :ptypeid_cr then wli.amount
                    else 0.000
                end
               )
          from wareslot wl
               left join wareslotitem wli
                    left join pallet p
                      on p.palletid = wli.palletid
                 on wli.wlotid = wl.wlotid
         where wl.waresid = new.waresid
           and wl.productdate = new.productdate
           and wl.status = '1'
          into :wliamount, :wliamount_bad;
        if (:wliamount is NULL) then
            wliamount = 0.000;
        if (:wliamount_bad is NULL) then
            wliamount_bad = 0.000;

        select sum(r.amount), sum(r.amountbad)
          from wh_reserve r
         where r.waresid = new.waresid
           and r.productdate = new.productdate
          into :ramount, :ramount_bad;
        if (:ramount is NULL) then
            ramount = 0.000;
        if (:ramount_bad is NULL) then
            ramount_bad = 0.000;

        if (:wliamount - :ramount + old.amount - new.amount < -0.000001) then
          exception exc_wh_reserve 'Нельзя зарезервировать больше остатка!';

        if (:wliamount_bad - :ramount_bad + old.amountbad - new.amountbad < -0.000001) then
          exception exc_wh_reserve 'Нельзя зарезервировать больше остатка!';
  end

  if (new.amount - new.amountsale < -0.0000001) then
  begin
    execute procedure WH_WARES_EXCTEXT(new.waresid, 'Нельзя зарезервировать меньше резерва под продажу: :wares:!')
     returning_values :excmes;
    exception exc_wh_reserve :excmes;
  end

  new.amountfree = new.amount - new.amountsale;

end^

SET TERM ; ^

