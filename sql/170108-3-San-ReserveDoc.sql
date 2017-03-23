

SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_bd0 for wh_reserve
active before delete position 0
AS
begin
    if (old.amountsale > 0.0000001
        or
        exists(select * from wh_reserve_client rc where rc.reserveid = old.id)
    ) then
        exception exc_wh_reserve 'Есть резерв для клиента: удаление невозможно!';

    if (old.amountdoc > 0.0000001
        or
        exists(select * from wh_reserve_doc rc where rc.reserveid = old.id)
    ) then
        exception exc_wh_reserve 'Есть резерв для документа: удаление невозможно!';

end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_RESERVE_DOC_QDIFFSET (
    RESERVEID type of column WH_RESERVE.ID,
    DOCID type of column OBJECT.OBJID,
    QDIFF type of R_DOUBLE)
AS
declare variable reservedocid type of column wh_reserve_doc.id;
begin
    if (:reserveid is NULL) then
        exception exc_wh_reserve 'Не установлен идентификатор резерва!';

    select rc.id
      from wh_reserve_doc rc
     where rc.reserveid = :reserveid
       and rc.docid = :docid
      into :reservedocid;

    if (:reservedocid is NULL) then
        insert into wh_reserve_doc ( RESERVEID, AMOUNT, DOCID)
        values (:reserveid, :qdiff, :docid);
    else
        update wh_reserve_doc rc
           set rc.amount = rc.amount + :qdiff
         where rc.id = :reservedocid;
end^

SET TERM ; ^

