

SET TERM ^ ;

create procedure WH_SITE_PARENTFIRSTDRAW (
    SITEID type of column SITE.siteid
)
returns (
    SID type of column SITE.siteid,
    SNAME type of column SITE.name
)
as
begin
    with recursive sr as (
        select s.siteid, s.name, s.higher, s.x_coord, s.y_coord
          from site s
         where s.siteid = :siteid
         union all
        select s.siteid, s.name, s.higher, s.x_coord, s.y_coord
          from sr
               join site s on s.siteid = sr.higher
         where sr.x_coord is NULL or sr.y_coord is NULL
    )
    select sr.siteid, sr.name
      from sr
     where sr.x_coord is not NULL and sr.y_coord is NOT NULL
      into :sid,  :sname;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_MONITORING_WARESLOC (
    SITEWHID type of column SITE.siteid,
    WARESID type of column GWARES.waresid)
returns (
    SID type of column SITE.siteid,
    SNAME type of column SITE.name,
    AMOUNT type of column WARESLOTITEM.amount
)
AS
begin
    for
        with sq as(
            select p.siteid as siteid, sum(wli.amount) as q
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.waresid = :waresid
               and wl.status = '1'
               and wli.amount > 0.0001
               and p.siteid is not null
             group by p.siteid
        )
        select coalesce(p.sid, sq.siteid), iif(p.sid is NULL, s.name, p.sname),
                sum(sq.q)
          from sq
               left join wh_site_parentfirstdraw(sq.siteid) p on 1=1
               left join site s on s.siteid = sq.siteid
         group by 1,2
          into :sid, :sname, :amount
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_MONITORING_WARESLOC (
    SITEWHID type of column SITE.siteid,
    WARESID type of column GWARES.waresid)
returns (
    SID type of column SITE.siteid,
    SNAME type of column SITE.name,
    AMOUNT type of column WARESLOTITEM.amount
)
AS
begin
/*
    for
        with sq as(
            select p.siteid as siteid, sum(wli.amount) as q
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.waresid = :waresid
               and wl.status = '1'
               and wli.amount > 0.0001
               and p.siteid is not null
             group by p.siteid
        ),
        recursive sqr as(

        )
        select coalesce(p.sid, sq.siteid), iif(p.sid is NULL, s.name, p.sname),
                sum(sq.q)
          from sq
               left join wh_site_parentfirstdraw(sq.siteid) p on 1=1
               left join site s on s.siteid = sq.siteid
         group by 1,2
          into :sid, :sname, :amount
    do
        suspend;
*/

for
        with recursive sqr as(
            select s.siteid as siteid, s.higher as higher, sum(wli.amount) as q, s.siteid as site2id
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join site s on s.siteid = p.siteid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.waresid = :waresid
               and wl.status = '1'
               and wli.amount > 0.0001
               and p.siteid is not null
             group by s.siteid, s.higher
             union all
            select s.siteid as siteid, s.higher as higher, sqr.q as q, sqr.site2id as site2id
              from sqr
                   join site s on s.siteid = sqr.higher
        )
        select coalesce(p.sid, sqr.siteid), iif(p.sid is NULL, s.name, p.sname),
                sum(sqr.q)
          from sqr
               left join wh_site_parentfirstdraw(sqr.siteid) p on 1=1
               left join site s on s.siteid = sqr.siteid
        where sqr.site2id = :sitewhid
         group by 1,2
          into :sid, :sname, :amount
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_MONITORING_WARESLOC (
    SITEWHID type of column SITE.siteid,
    WARESID type of column GWARES.waresid)
returns (
    SID type of column SITE.siteid,
    SNAME type of column SITE.name,
    AMOUNT type of column WARESLOTITEM.amount
)
AS
begin
    for
        with recursive sqr as(
            select s.siteid as siteid, s.higher as higher, sum(wli.amount) as q, s.siteid as site1id
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join site s on s.siteid = p.siteid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.waresid = :waresid
               and wl.status = '1'
               and wli.amount > 0.0001
               and p.siteid is not null
             group by s.siteid, s.higher
             union all
            select s.siteid as siteid, s.higher as higher, sqr.q as q, sqr.site1id as site1id
              from sqr
                   join site s on s.siteid = sqr.higher
        )
        select coalesce(p.sid, sqr.site1id), iif(p.sid is NULL, s.name, p.sname),
                sum(sqr.q)
          from sqr
               left join wh_site_parentfirstdraw(sqr.site1id) p on 1=1
               left join site s on s.siteid = sqr.site1id
        where sqr.siteid = :sitewhid
         group by 1,2
          into :sid, :sname, :amount
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_MONITORING_WARESLOC (
    SITEWHID type of column SITE.siteid,
    WARESID type of column GWARES.waresid)
returns (
    SID type of column SITE.siteid,
    SNAME type of column SITE.name,
    AMOUNT type of column WARESLOTITEM.amount
)
AS
begin
    for
        with recursive sqr as(
            select s.siteid as siteid, s.higher as higher, sum(wli.amount) as q, s.siteid as site1id
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join site s on s.siteid = p.siteid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.waresid = :waresid
               and wl.status = '1'
               and wli.amount > 0.0001
               and p.siteid is not null
             group by s.siteid, s.higher
             union all
            select s.siteid as siteid, s.higher as higher, sqr.q as q, sqr.site1id as site1id
              from sqr
                   join site s on s.siteid = sqr.higher
        )
        select coalesce(p.sid, sqr.site1id), iif(p.sid is NULL, s.name, p.sname),
               sum(sqr.q)
          from sqr
               left join wh_site_parentfirstdraw(sqr.site1id) p on 1=1
               left join site s on s.siteid = sqr.site1id
        where sqr.siteid = :sitewhid
         group by 1,2
          into :sid, :sname, :amount
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_SITE_BRANCH_WARESREST (
    SITEID type of column SITE.siteid,
    WARESID type of column GWARES.waresid
)
returns (
    SNAME type of column SITE.name,
    PNUMBER type of column PALLET.number,
    pnum type of column PALLET.num,
    PRODUCTDATE type of column WARESLOT.productdate,
    AMOUNT type of column WARESLOTITEM.amount
)
as
begin
    for
        with recursive sr as (
            select s.siteid, s.name
              from site s
             where s.siteid = :siteid
             union all
            select s.siteid, s.name
              from sr
                   join site s on s.higher = sr.siteid
        )
        select sr.name, p.number, p.num, wl.productdate, sum(wli.amount)
          from sr
               left join pallet p
                    left join wareslotitem wli
                         left join wareslot wl on wl.wlotid = wli.wlotid
                      on wli.palletid = p.palletid
                 on p.siteid = sr.siteid
         where wl.waresid = :waresid
         group by sr.name, p.number, p.num, wl.productdate
          into :sname, :pnumber, :pnum, :productdate, :amount
    do
        suspend;
end^

SET TERM ; ^

