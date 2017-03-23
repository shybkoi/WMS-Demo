

SET TERM ^ ;

create or alter procedure WH_BUYRETURN_AFTERIMP (
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
        execute procedure WH_IMP_CARGO_CHK(:docid);

        update document d
           set d.status = 'e', d.number = (select id.number from imp_document id where id.docid = :docid)
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



DROP PROCEDURE WH_COMERETURN_AFTERIMP;



ALTER TABLE WH_RESERVE
ADD AMOUNTBAD R_DOUBLE;



SET TERM ^ ;

create procedure WH_SITEOPTIONID_BAD
returns (
    OPTIONID type of column siteoption.id
)
as
begin
    select so.id
      from siteoption so
     where so.code = 'COMERETURN'
      into :optionid;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_bi for wh_reserve
active before insert position 0
as
declare variable wliamount type of column wareslotitem.amount;
declare variable wliamount_bad type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
declare variable ramount_bad type of column wh_reserve.amountbad;
declare variable optionid_bad type of column siteoption.id;
begin
    if (new.amountbad is NULL) then
        new.amountbad = 0.000;

    if (new.amount + new.amountbad < 0.0001) then
        exception exc_wh_reserve '–езервировать можно только количество товара большее нул€!';

    if (new.amount < -0.0001 or new.amountbad < -0.0001 ) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать отрицательное количество!';


    if (new.amountsale is NULL) then
        new.amountsale = 0.000;
    
    if (new.amount - new.amountsale < -0.0000001) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать меньше резерва под продажу!';

    execute procedure WH_SITEOPTIONID_BAD
     returning_values :optionid_bad;

    select sum(
            case
                when so.siteid is NULL then wli.amount
                else 0.000
            end
           ),
           sum(
            case
                when so.siteid is not NULL then wli.amount
                else 0.000
            end
           )
      from wareslot wl
           left join wareslotitem wli
                left join pallet p
                     left join site_options so on so.siteid = p.siteid and so.optionid = :optionid_bad
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

    if (:wliamount - :ramount - new.amount < -0.000001) then
      exception exc_wh_reserve 'Ќельз€ зарезервировать больше остатка!';
    
    if (:wliamount_bad - :ramount_bad - new.amountbad < -0.000001) then
      exception exc_wh_reserve 'Ќельз€ зарезервировать больше остатка!';

    new.amountfree = new.amount - new.amountsale;

    if (new.id is null) then
      new.id = gen_id(gen_wh_reserve_id,1);
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_au0 for wh_reserve
active after update position 0
AS
begin
    if (new.amount < 0.000001 and new.amountbad < 0.00001) then
        delete from wh_reserve r
         where r.id = new.id;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_bi for wh_reserve
active before insert position 0
as
declare variable wliamount type of column wareslotitem.amount;
declare variable wliamount_bad type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
declare variable ramount_bad type of column wh_reserve.amountbad;
declare variable ptypeid_cr type of column pallet_type.id;
begin
    if (new.amountbad is NULL) then
        new.amountbad = 0.000;

    if (new.amount + new.amountbad < 0.0001) then
        exception exc_wh_reserve '–езервировать можно только количество товара большее нул€!';

    if (new.amount < -0.0001 or new.amountbad < -0.0001 ) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать отрицательное количество!';


    if (new.amountsale is NULL) then
        new.amountsale = 0.000;
    
    if (new.amount - new.amountsale < -0.0000001) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать меньше резерва под продажу!';

    select w.id
      from WH_PALTYPEID_COMERETURN w
      into :ptypeid_cr;

    select sum(
            case
                when p.ptypeid = :ptypeid_cr then wli.amount
                else 0.000
            end
           ),
           sum(
            case
                when p.ptypeid = :ptypeid_cr then 0.000
                else wli.amount
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

    if (:wliamount - :ramount - new.amount < -0.000001) then
      exception exc_wh_reserve 'Ќельз€ зарезервировать больше остатка!';
    
    if (:wliamount_bad - :ramount_bad - new.amountbad < -0.000001) then
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
declare variable wliamount_bad type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
declare variable ramount_bad type of column wh_reserve.amountbad;
declare variable ptypeid_cr type of column pallet_type.id;
begin
  if (new.amountbad is NULL) then
      new.amountbad = 0.000;

  if (new.amount < -0.0001 or new.amountbad < -0.0001) then
      exception exc_wh_reserve 'Ќельз€ зарезервировать отрицательное количество!';

  if (old.amount - new.amount < -0.00001 or old.amountbad - new.amountbad < -0.00001 ) then
  begin
    select w.id
      from WH_PALTYPEID_COMERETURN w
      into :ptypeid_cr;

        select sum(
                case
                    when p.ptypeid = :ptypeid_cr then wli.amount
                    else 0.000
                end
               ),
               sum(
                case
                    when p.ptypeid = :ptypeid_cr then 0.000
                    else wli.amount
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
          exception exc_wh_reserve 'Ќельз€ зарезервировать больше остатка!';

        if (:wliamount_bad - :ramount_bad + old.amountbad - new.amountbad < -0.000001) then
          exception exc_wh_reserve 'Ќельз€ зарезервировать больше остатка!';
  end

  if (new.amount - new.amountsale < -0.0000001) then
    exception exc_wh_reserve 'Ќельз€ зарезервировать меньше резерва под продажу!';

  new.amountfree = new.amount - new.amountsale;

end^

SET TERM ; ^

