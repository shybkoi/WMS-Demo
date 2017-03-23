

SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_SUMMARY_DATA
returns (
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WEXTERNALCODE type of column GWARES.EXTERNALCODE,
    OBJID type of column OBJECT.OBJID,
    OBJNAME type of R_VARCHAR255,
    Q1 type of column WH_RESERVE.AMOUNT,
    Q2 type of column WH_RESERVE.AMOUNTSALE,
    QB type of column WH_RESERVE.AMOUNTBAD,
    QD type of column WH_RESERVE.amountdoc,
    PRDATE type of column WH_RESERVE.PRODUCTDATE)
AS
begin
    for
        select g.waresid, g.code, g.name, g.externalcode,
               r.objid, (select objname from wh_get_objectname(r.objid)),
               r.amount, r.amountsale, r.productdate, r.amountbad, r.amountdoc
          from wh_reserve r
               left join gwares g on g.waresid = r.waresid
         where r.amount + r.amountbad > 0.0000001
          into :wid, :wcode, :wname, :wexternalcode,
               :objid, :objname,
               :q1, :q2, :prdate, :qb, :qd
    do
        suspend;
end^

SET TERM ; ^

