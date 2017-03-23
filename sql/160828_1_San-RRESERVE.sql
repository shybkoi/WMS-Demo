

SET TERM ^ ;

create procedure WH_RRESERVE_SUMMARY_DATA
returns (
    WID type of column GWARES.waresid,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    OBJID type of column OBJECT.objid,
    OBJNAME type of R_VARCHAR255,
    Q1 type of column WH_RESERVE.amount,
    Q2 type of column WH_RESERVE.amountsale,
    PRDATE type of column WH_RESERVE.productdate
)
as
begin
    for
        select g.waresid, g.code, g.name,
               r.objid, (select objname from wh_get_objectname(r.objid)),
               r.amount, r.amountsale, r.productdate
          from wh_reserve r
               left join gwares g on g.waresid = r.waresid
         where r.amount > 0.0000001
          into :wid, :wcode, :wname,
               :objid, :objname,
               :q1, :q2, :prdate
    do
        suspend;
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
     where wl.waresid = new.waresid
       and wl.productdate = new.productdate
       and wl.status = '1'
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



CREATE INDEX PALLET_FINISHPRINT_IDX_DT
ON PALLET_FINISHPRINT (DATETIME);

