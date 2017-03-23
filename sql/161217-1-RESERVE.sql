

SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_SUMMARY_DATA
returns (
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WEXTERNALCODE type of column GWARES.externalcode,
    OBJID type of column OBJECT.OBJID,
    OBJNAME type of R_VARCHAR255,
    Q1 type of column WH_RESERVE.AMOUNT,
    Q2 type of column WH_RESERVE.AMOUNTSALE,
    QB type of column WH_RESERVE.AMOUNTBAD,
    PRDATE type of column WH_RESERVE.PRODUCTDATE)
AS
begin
    for
        select g.waresid, g.code, g.name, g.externalcode,
               r.objid, (select objname from wh_get_objectname(r.objid)),
               r.amount, r.amountsale, r.productdate, r.amountbad
          from wh_reserve r
               left join gwares g on g.waresid = r.waresid
         where r.amount + r.amountbad > 0.0000001
          into :wid, :wcode, :wname, :wexternalcode,
               :objid, :objname,
               :q1, :q2, :prdate, :qb
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_RRESERVE_WARESLOTREST_LIST
returns (
    WARESID type of column GWARES.waresid
)
as
begin
    for
        select distinct wlr.waresid
          from wareslotrest wlr
          into :waresid
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_WARESLOTREST_LIST
returns (
    WARESID type of column GWARES.waresid
)
as
begin
    for
        select distinct wlr.waresid
          from wareslotrest wlr
          into :waresid
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_RRESERVE_WARESLOTREST_DATA(
    WARESID type of column GWARES.waresid
)
returns (
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WEXTERNALCODE type of column GWARES.externalcode,
    R type of column WARESLOTITEM.AMOUNT,
    RTRASH type of column WARESLOTITEM.AMOUNT,
    PRDATE type of column WARESLOT.productdate
)
as
begin
    select g.waresid, g.code, g.name, g.externalcode
      from gwares g
     where g.waresid = :waresid
      into :wid, :wcode, :wname, :wexternalcode;

    for
            select wl.productdate,
                   sum(case when sp.code = 'TRASH' then wli.amount else 0.000 end),
                   sum(case sp.calcrest when '1' then wli.amount else 0.0000 end)
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join site s
                                  left join sitespecies sp
                                    on sp.sitespeciesid = s.sitespeciesid
                               on s.siteid = p.siteid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.waresid = :waresid
               and wl.status = '1'
             group by wl.productdate
              into :prdate, :r, :rtrash
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_WARESLOTREST_LIST
returns (
    WID type of column GWARES.waresid
)
as
begin
    for
        select distinct wlr.waresid
          from wareslotrest wlr
          into :wid
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_WARESLOTREST_DATA(
    WARESID type of column GWARES.waresid
)
returns (
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WEXTERNALCODE type of column GWARES.externalcode,
    R type of column WARESLOTITEM.AMOUNT,
    RTRASH type of column WARESLOTITEM.AMOUNT,
    RBAD type of column WARESLOTITEM.AMOUNT,
    PRDATE type of column WARESLOT.productdate
)
as
begin
    select g.waresid, g.code, g.name, g.externalcode
      from gwares g
     where g.waresid = :waresid
      into :wid, :wcode, :wname, :wexternalcode;

    for
            select wl.productdate,
                   sum(case when sp.code = 'TRASH' then wli.amount else 0.000 end),
                   sum(case when sp.calcrest='1' and coalesce(pt.fundlvl1type,'')<>'BAD' then wli.amount else 0.0000 end),
                   sum(case when sp.calcrest='1' and coalesce(pt.fundlvl1type,'')='BAD' then wli.amount else 0.0000 end)
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join site s
                                  left join sitespecies sp
                                    on sp.sitespeciesid = s.sitespeciesid
                               on s.siteid = p.siteid
                             left join pallet_type pt on pt.id = p.ptypeid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.waresid = :waresid
               and wl.status = '1'
             group by wl.productdate
              into :prdate, :r, :rtrash, :rbad
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_WARESLOTREST_DATA(
    WARESID type of column GWARES.waresid
)
returns (
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WEXTERNALCODE type of column GWARES.externalcode,
    R type of column WARESLOTITEM.AMOUNT,
    RTRASH type of column WARESLOTITEM.AMOUNT,
    RBAD type of column WARESLOTITEM.AMOUNT,
    PRDATE type of column WARESLOT.productdate
)
as
begin
    select g.waresid, g.code, g.name, g.externalcode
      from gwares g
     where g.waresid = :waresid
      into :wid, :wcode, :wname, :wexternalcode;

    for
            select wl.productdate,
                   sum(case when sp.code = 'TRASH' then wli.amount else 0.000 end),
                   sum(case when sp.calcrest='1' and coalesce(pt.fundlvl1type,'')<>'BAD' then wli.amount else 0.0000 end),
                   sum(case when sp.calcrest='1' and coalesce(pt.fundlvl1type,'')='BAD' then wli.amount else 0.0000 end)
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join site s
                                  left join sitespecies sp
                                    on sp.sitespeciesid = s.sitespeciesid
                               on s.siteid = p.siteid
                             left join pallet_type pt on pt.id = p.ptypeid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.waresid = :waresid
               and wl.status = '1'
             group by wl.productdate
              into :prdate, :rtrash, :r, :rbad
    do
        suspend;
end^

SET TERM ; ^

