/******************************************************************************/
/***                                 Tables                                 ***/
/******************************************************************************/



CREATE TABLE WH_RESERVE_DOC_CHANGES (
    OBJID        R_ID NOT NULL /* R_ID = INTEGER */,
    WARESID      R_ID NOT NULL /* R_ID = INTEGER */,
    PRODUCTDATE  R_DATE NOT NULL /* R_DATE = DATE */,
    RDOCID       R_ID NOT NULL /* R_ID = INTEGER */,
    AMOUNT       R_DOUBLE NOT NULL /* R_DOUBLE = DOUBLE PRECISION */,
    DOCID        R_ID64 /* R_ID64 = DOUBLE PRECISION */,
    DATETIME     R_DATETIME /* R_DATETIME = TIMESTAMP */
);




/******************************************************************************/
/***                              Foreign Keys                              ***/
/******************************************************************************/

ALTER TABLE WH_RESERVE_DOC_CHANGES ADD CONSTRAINT FK_WH_RESERVE_DOC_CHANGES_RD FOREIGN KEY (RDOCID) REFERENCES DOCUMENT (DOCID) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE WH_RESERVE_DOC_CHANGES ADD CONSTRAINT FK_WH_RESERVE_DOC_CHANGES_D FOREIGN KEY (DOCID) REFERENCES DOCUMENT (DOCID) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE WH_RESERVE_DOC_CHANGES ADD CONSTRAINT FK_WH_RESERVE_DOC_CHANGES_O FOREIGN KEY (OBJID) REFERENCES OBJECT (OBJID) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE WH_RESERVE_DOC_CHANGES ADD CONSTRAINT FK_WH_RESERVE_DOC_CHANGES_W FOREIGN KEY (WARESID) REFERENCES GWARES (WARESID) ON DELETE CASCADE ON UPDATE CASCADE;


/******************************************************************************/
/***                                Triggers                                ***/
/******************************************************************************/


SET TERM ^ ;



/******************************************************************************/
/***                          Triggers for tables                           ***/
/******************************************************************************/



/* Trigger: WH_RESERVE_CLIENT_CHANGES_AD0 */
CREATE OR ALTER TRIGGER WH_RESERVE_DOC_CHANGES_AD0 FOR WH_RESERVE_DOC_CHANGES
ACTIVE AFTER DELETE POSITION 0
AS
declare variable reserveid type of column wh_reserve.id;
begin
    execute procedure wh_reserve_getid(old.objid, old.waresid, old.productdate)
     returning_values :reserveid;


    execute procedure WH_RESERVE_DOC_QDIFFSET(:reserveid, old.rdocid, -old.amount);
end
^


/* Trigger: WH_RESERVE_CLIENT_CHANGES_AI0 */
CREATE OR ALTER TRIGGER WH_RESERVE_DOC_CHANGES_AI0 FOR WH_RESERVE_DOC_CHANGES
ACTIVE AFTER INSERT POSITION 0
AS
declare variable reserveid type of column wh_reserve.id;
begin
    execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
     returning_values :reserveid;

    execute procedure WH_RESERVE_DOC_QDIFFSET(:reserveid, new.rdocid, new.amount);
end
^


/* Trigger: WH_RESERVE_CLIENT_CHANGES_AU0 */
CREATE OR ALTER TRIGGER WH_RESERVE_DOC_CHANGES_AU0 FOR WH_RESERVE_DOC_CHANGES
ACTIVE AFTER UPDATE POSITION 0
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
        new.rdocid <> old.rdocid
    ) then
    begin
        reserveid = NULL;
        execute procedure wh_reserve_getid(old.objid, old.waresid, old.productdate)
         returning_values :reserveid;

        execute procedure WH_RESERVE_DOC_QDIFFSET(:reserveid, old.rdocid, -old.amount);

        reserveid = NULL;
        execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
         returning_values :reserveid;

        execute procedure WH_RESERVE_DOC_QDIFFSET(:reserveid, new.rdocid, new.amount);
    end
    else if (abs(old.amount - new.amount) > 0.0000001) then
    begin
        reserveid = NULL;
        execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
         returning_values :reserveid;

        execute procedure WH_RESERVE_DOC_QDIFFSET(:reserveid, new.rdocid, new.amount - old.amount);
    end
end
^


/* Trigger: WH_RESERVE_CLIENT_CHANGES_BI0 */
CREATE OR ALTER TRIGGER WH_RESERVE_DOC_CHANGES_BI0 FOR WH_RESERVE_DOC_CHANGES
ACTIVE BEFORE INSERT POSITION 0
AS
begin
    new.datetime = current_timestamp;
end
^


SET TERM ; ^


