

SET TERM ^ ;

create or alter procedure WH_RRESERVE_DOC (
    OBJID type of column OBJECT.OBJID,
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of column WH_RESERVE_CHANGES.PRODUCTDATE
)
returns (
    AMOUNT type of column WH_RESERVE_CHANGES.AMOUNT,
    DOCNUM type of column DOCUMENT.NUMBER,
    DOCDATE type of column DOCUMENT.REALDOCDATE,
    DTNAME type of column DOCTYPE.NAME,
    FROMNAME type of R_FULLNAME,
    THROUGHNAME type of R_FULLNAME,
    TONAME type of R_FULLNAME,
    DOCSTAT type of column R_STATUS.CODE,
    DOCSTATNAME type of column R_STATUS.NAME
)
AS
declare variable reserveid type of column WH_RESERVE.id;
begin
    select r.id
      from wh_reserve r
     where r.objid = :objid
       and r.waresid = :waresid
       and r.productdate = :productdate
      into :reserveid;

    if (:reserveid is NOT NULL) then
    for
        select rc.amount,
               d.number, d.realdocdate,
               (select objname from wh_get_objectname(d.fromobj)),
               (select objname from wh_get_objectname(d.throughobj)),
               (select objname from wh_get_objectname(d.toobj)),
               rs.code, rs.name, dt.name
          from wh_reserve_doc rc
               left join document d
                    left join r_status rs on rs.code = d.status and rs.statustype = 'O'
                    left join doctype dt on dt.doctid = d.doctype
                 on d.docid = rc.docid
         where rc.reserveid = :reserveid
          into :amount,
               :docnum, :docdate, :fromname, :throughname, :toname,
               :docstat, :docstatname, :dtname
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_DOC_SUMMARY_DATA (
    DOCID type of column DOCUMENT.DOCID)
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
        with res as(
            select rc.waresid, rc.productdate, rc.objid, rc.amount as amount, rc.amountbad as amountbad, 0.000 as amountsale, 0.000 as amountdoc
              from wh_reserve_changes rc
             where rc.docid = :docid
             union all
            select rc.waresid, rc.productdate, rc.objid, 0.000 as amount, 0.000 as amountbad, rc.amount as amountsale, 0.000 as amountdoc
              from wh_reserve_client_changes rc
             where rc.docid = :docid
             union all
            select rd.waresid, rd.productdate, rd.objid, 0.000 as amount, 0.000 as amountbad, 0.000 as amountsale, rd.amount as amountdoc
              from wh_reserve_doc_changes rd
             where rd.docid = :docid
               and rd.rdocid = :docid
        )
        select g.waresid, g.code, g.name, g.externalcode,
               r.objid, (select objname from wh_get_objectname(r.objid)),
               r.amount, r.amountsale, r.productdate, r.amountbad, r.amountdoc
          from res r
               left join gwares g on g.waresid = r.waresid
          into :wid, :wcode, :wname, :wexternalcode,
               :objid, :objname,
               :q1, :q2, :prdate, :qb, :qd
    do
        suspend;
end^

SET TERM ; ^

