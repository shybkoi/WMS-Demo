

SET TERM ^ ;

CREATE OR ALTER procedure K_WH_DECALITREQ (
    WARESID type of column GWARES.WARESID)
returns (
    FACTOR type of column WARESUNIT.FACTOR,
    SHORTNAME type of column UNIT.SHORTNAME)
as
begin
  /* TODO */
  select u.shortname, wu.factor
    from unit u
         left join waresunit wu on u.unitid = wu.unitid
   where wu.waresid = :waresid
     and wu.typewaresunit = 'report'
    into :shortname, :factor;
  suspend;
end^

SET TERM ; ^

