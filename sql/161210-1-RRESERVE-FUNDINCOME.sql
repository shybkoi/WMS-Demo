

SET TERM ^ ;

create procedure WH_RRESERVE_FUNDINCOMEDOCS
returns (
    DOCID type of column DOCUMENT.docid,
    DOCNUM type of column DOCUMENT.number,
    DOCDATE type of R_DATE,
    FROMOBJ type of column OBJECT.objid,
    THROUGHOBJ type of column OBJECT.objid,
    TOOBJ type of column OBJECT.objid,
    FROMOBJNAME type of R_FULLNAME,
    THROUGHOBJNAME type of R_FULLNAME,
    TOOBJNAME type of R_FULLNAME,
    DOCREALDATE type of R_DATE,
    DESCRIPT type of column DOCUMENT.DESCRIPT,
    DOCSUBTYPE type of column DOCSUBTYPE.code,
    DOCSUBTYPENAME type of column DOCSUBTYPE.name,
    LASTDATE type of column DOCUMENT.lastdate
)
as
declare variable dtid_fundincome type of column DOCTYPE.doctid;
begin
    execute procedure wh_dtid_fundincome
     returning_values :dtid_fundincome;

    for
        select d.docid, d.number, d.docdate, d.realdocdate, d.lastdate, d.descript,
               d.fromobj, d.throughobj, d.toobj,
               (select objname from wh_get_objectname(d.fromobj)),
               (select objname from wh_get_objectname(d.throughobj)),
               (select objname from wh_get_objectname(d.toobj)),
               dst.code, dst.name
          from document d
               left join docsubtype dst on dst.doctid = d.doctype
         where d.doctype = :dtid_fundincome
           and d.status = 'c'
          into :docid, :docnum, :docdate, :docrealdate, :lastdate, :descript,
               :fromobj, :throughobj, :toobj,
               :fromobjname, :throughobjname, :toobjname,
               :docsubtype, :docsubtypename
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_RRESERVE_DTFUNDINCOMEOBJ
returns (
    NUMOBJ type of column DOCTYPEOBJ.numobj,
    CAPTION type of column DOCTYPEOBJ.caption
)
as
declare variable dtid_fundincome type of column DOCTYPE.doctid ;
begin
    execute procedure wh_dtid_fundincome
     returning_values :dtid_fundincome;

    for
        select dto.numobj, dto.caption
          from doctypeobj dto
         where dto.doctid = :dtid_fundincome
          into :numobj, :caption
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_RRESERVE_FUNDINCOMEDOCWARES (
    DOCID type of column DOCUMENT.docid
)
returns (
    WID type of column GWARES.waresid,
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    PRODUCTDATE type of R_DATE,
    QDOC type of column CARGO.amount,
    QFUND type of column wh_reserve_changes.amount,
    VUF type of column WARESUNIT.factor,
    VUC type of column UNIT.shortname,
    MUF type of column WARESUNIT.factor,
    MUC type of column UNIT.shortname
)
as
begin
    for
        with wdata as (
            select cast(d.realdocdate as r_date) as productdate, cg.waresid as waresid, cg.amount as qdoc, 0.000 as qfund
              from document d
                   left join cargo cg on cg.document = d.docid
             where cg.document = :docid
               and cg.cargoid is NOT NULL
             union
            select rcc.productdate as productdate, rcc.waresid as waresid, 0.000 as qdoc, rcc.amount as qfund
              from wh_reserve_changes rcc
             where rcc.docid = :docid
        ),
        wgroup as(
            select productdate, waresid, sum(qdoc) as qdoc, sum(qfund) as qfund
              from wdata
            group by productdate, waresid
        )
        select wgroup.productdate, wgroup.qdoc, wgroup.qfund,
               g.waresid, g.code, g.name,
               vwu.factor, vu.shortname, mwu.factor, mu.shortname
          from wgroup
               left join gwares g
                    left join waresunit vwu
                         left join unit vu on vu.unitid = vwu.unitid
                      on vwu.waresunitid = g.viewunitid
                    left join waresunit mwu
                         left join unit mu on mu.unitid = mwu.unitid
                      on mwu.waresunitid = g.mainunitid
                 on g.waresid = wgroup.waresid
          into :productdate, :qdoc, :qfund,
               :wid, :wcode, :wname,
               :vuf, :vuc, :muf, :muc
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_FUNDINCOMEDOCWARES (
    DOCID type of column DOCUMENT.docid
)
returns (
    WID type of column GWARES.waresid,
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    PRODUCTDATE type of R_DATE,
    QDOC type of column CARGO.amount,
    QFUND type of column wh_reserve_changes.amount,
    VUF type of column WARESUNIT.factor,
    VUC type of column UNIT.shortname,
    MUF type of column WARESUNIT.factor,
    MUC type of column UNIT.shortname
)
as
begin
    for
        with wdata as (
            select cast(d.realdocdate as r_date) as productdate, cg.waresid as waresid, cg.amount as qdoc, 0.000 as qfund
              from document d
                   left join cargo cg on cg.document = d.docid
             where d.docid = :docid
               and cg.cargoid is NOT NULL
             union
            select rcc.productdate as productdate, rcc.waresid as waresid, 0.000 as qdoc, rcc.amount as qfund
              from wh_reserve_changes rcc
             where rcc.docid = :docid
        ),
        wgroup as(
            select productdate, waresid, sum(qdoc) as qdoc, sum(qfund) as qfund
              from wdata
            group by productdate, waresid
        )
        select wgroup.productdate, wgroup.qdoc, wgroup.qfund,
               g.waresid, g.code, g.name,
               vwu.factor, vu.shortname, mwu.factor, mu.shortname
          from wgroup
               left join gwares g
                    left join waresunit vwu
                         left join unit vu on vu.unitid = vwu.unitid
                      on vwu.waresunitid = g.viewunitid
                    left join waresunit mwu
                         left join unit mu on mu.unitid = mwu.unitid
                      on mwu.waresunitid = g.mainunitid
                 on g.waresid = wgroup.waresid
          into :productdate, :qdoc, :qfund,
               :wid, :wcode, :wname,
               :vuf, :vuc, :muf, :muc
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_FUNDINCOMEDOCWARES (
    DOCID type of column DOCUMENT.docid,
    WARESID type of column GWARES.waresid = NULL
)
returns (
    WID type of column GWARES.waresid,
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    PRODUCTDATE type of R_DATE,
    QDOC type of column CARGO.amount,
    QFUND type of column wh_reserve_changes.amount,
    VUF type of column WARESUNIT.factor,
    VUC type of column UNIT.shortname,
    MUF type of column WARESUNIT.factor,
    MUC type of column UNIT.shortname
)
as
begin
    if (:waresid is NULL) then
    begin
        for
            with wdata as (
                select cast(d.realdocdate as r_date) as productdate, cg.waresid as waresid, cg.amount as qdoc, 0.000 as qfund
                  from document d
                       left join cargo cg on cg.document = d.docid
                 where d.docid = :docid
                   and cg.cargoid is NOT NULL
                 union
                select rcc.productdate as productdate, rcc.waresid as waresid, 0.000 as qdoc, rcc.amount as qfund
                  from wh_reserve_changes rcc
                 where rcc.docid = :docid
            ),
            wgroup as(
                select productdate, waresid, sum(qdoc) as qdoc, sum(qfund) as qfund
                  from wdata
                group by productdate, waresid
            )
            select wgroup.productdate, wgroup.qdoc, wgroup.qfund,
                   g.waresid, g.code, g.name,
                   vwu.factor, vu.shortname, mwu.factor, mu.shortname
              from wgroup
                   left join gwares g
                        left join waresunit vwu
                             left join unit vu on vu.unitid = vwu.unitid
                          on vwu.waresunitid = g.viewunitid
                        left join waresunit mwu
                             left join unit mu on mu.unitid = mwu.unitid
                          on mwu.waresunitid = g.mainunitid
                     on g.waresid = wgroup.waresid
              into :productdate, :qdoc, :qfund,
                   :wid, :wcode, :wname,
                   :vuf, :vuc, :muf, :muc
        do
            suspend;
    end
    else
    begin
        for
            with wdata as (
                select cast(d.realdocdate as r_date) as productdate, cg.waresid as waresid, cg.amount as qdoc, 0.000 as qfund
                  from document d
                       left join cargo cg on cg.document = d.docid
                 where d.docid = :docid
                   and cg.waresid = :waresid
                 union
                select rcc.productdate as productdate, rcc.waresid as waresid, 0.000 as qdoc, rcc.amount as qfund
                  from wh_reserve_changes rcc
                 where rcc.docid = :docid
                   and rcc.waresid = :waresid
            ),
            wgroup as(
                select productdate, waresid, sum(qdoc) as qdoc, sum(qfund) as qfund
                  from wdata
                group by productdate, waresid
            )
            select wgroup.productdate, wgroup.qdoc, wgroup.qfund,
                   g.waresid, g.code, g.name,
                   vwu.factor, vu.shortname, mwu.factor, mu.shortname
              from wgroup
                   left join gwares g
                        left join waresunit vwu
                             left join unit vu on vu.unitid = vwu.unitid
                          on vwu.waresunitid = g.viewunitid
                        left join waresunit mwu
                             left join unit mu on mu.unitid = mwu.unitid
                          on mwu.waresunitid = g.mainunitid
                     on g.waresid = wgroup.waresid
              into :productdate, :qdoc, :qfund,
                   :wid, :wcode, :wname,
                   :vuf, :vuc, :muf, :muc
        do
            suspend;
    end
end^

SET TERM ; ^

