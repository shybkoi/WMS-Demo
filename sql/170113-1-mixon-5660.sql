

SET TERM ^ ;

create or alter procedure WH_WARESLOTREST_LIST
returns (
    WID type of column WARESLOTREST.WARESID)
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

CREATE OR ALTER procedure WH_WARESLOTREST_LIST (
    OBJID type of column WARESLOTREST.OBJID)
returns (
    WID type of column WARESLOTREST.WARESID)
as
begin
    for
        select distinct wlr.waresid
          from wareslotrest wlr
         where wlr.objid = :objid
          into :wid
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_WARESLOTREST_WARESLOT (
    OBJID type of R_ID,
    WARESID type of R_ID,
    ZONEID type of R_ID = null)
returns (
    PDATE type of column WARESLOT.PRODUCTDATE,
    QB type of column WARESLOTITEM.AMOUNT,
    QS type of column WARESLOTITEM.AMOUNT,
    QR type of column WARESLOTITEM.AMOUNT,
    QE type of column WARESLOTITEM.AMOUNT,
    QA type of column WARESLOTITEM.AMOUNT)
as
begin
  for
    select wl.productdate,
           sum(case sp.code when 'B' then wli.amount else 0.000 end), -- МХ
           sum(case sp.code when 'S' then wli.amount else 0.000 end), -- МО
           sum(case when sp.code starting 'BUYRET' then wli.amount else 0.000 end), -- Возврат
           sum(case sp.code when 'E' then wli.amount else 0.000 end), -- Экспедиция
           sum(case sp.calcrest when '1' then wli.amount else 0.0000 end)
      from wareslot wl
           left join wareslotitem wli
                left join pallet p
                     left join pallet_feature pf on pf.id = p.featureid
                     left join site s
                          left join sitespecies sp
                            on sp.sitespeciesid = s.sitespeciesid
                       on s.siteid = p.siteid
                     left join pallet_type pt on pt.id = p.ptypeid
                  on p.palletid = wli.palletid
             on wli.wlotid = wl.wlotid
     where wl.objid = :objid
       and wl.waresid = :waresid
       and coalesce(:zoneid,wl.zoneid) = wl.zoneid
       and wl.status = '1'
     group by 1
      into :pdate, :qb, :qs, :qr, :qe, :qa
  do
  begin
    suspend;
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARESLOTREST_LIST (
    OBJID type of column WARESLOTREST.OBJID)
returns (
    WID type of column WARESLOTREST.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    VUFACTOR type of column WARESUNIT.FACTOR,
    VUCODE type of column UNIT.SHORTNAME,
    MUFACTOR type of column WARESUNIT.FACTOR,
    MUCODE type of column UNIT.SHORTNAME)
as
begin
    for
        select distinct wlr.waresid, g.code, g.name,
               vwu.factor, vu.shortname, mwu.factor, mu.shortname
          from wareslotrest wlr
               left join gwares g on wlr.waresid = g.waresid
               left join waresunit vwu
                    left join unit vu on vu.unitid=vwu.unitid
                 on vwu.waresunitid = g.viewunitid
               left join waresunit mwu
                    left join unit mu on mu.unitid=mwu.unitid
                 on mwu.waresunitid = g.mainunitid
         where wlr.objid = :objid
          into :wid, :wcode, :wname,
               :vufactor, :vucode, :mufactor, :mucode
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARESLOTREST_WARESLOT (
    OBJID type of R_ID,
    WARESID type of R_ID,
    ZONEID type of R_ID = null)
returns (
    PDATE type of column WARESLOT.PRODUCTDATE,
    QB type of column WARESLOTITEM.AMOUNT,
    QS type of column WARESLOTITEM.AMOUNT,
    QR type of column WARESLOTITEM.AMOUNT,
    QE type of column WARESLOTITEM.AMOUNT,
    QA type of column WARESLOTITEM.AMOUNT)
as
begin
  for
    select wl.productdate,
           sum(case sp.code when 'B' then wli.amount else 0.000 end), -- МХ
           sum(case sp.code when 'STACK' then wli.amount else 0.000 end), -- МО
           sum(case when sp.code starting 'BUYRET' then wli.amount else 0.000 end), -- Возврат
           sum(case sp.code when 'E' then wli.amount else 0.000 end), -- Экспедиция
           sum(case sp.calcrest when '1' then wli.amount else 0.0000 end)
      from wareslot wl
           left join wareslotitem wli
                left join pallet p
                     left join pallet_feature pf on pf.id = p.featureid
                     left join site s
                          left join sitespecies sp
                            on sp.sitespeciesid = s.sitespeciesid
                       on s.siteid = p.siteid
                     left join pallet_type pt on pt.id = p.ptypeid
                  on p.palletid = wli.palletid
             on wli.wlotid = wl.wlotid
     where wl.objid = :objid
       and wl.waresid = :waresid
       and coalesce(:zoneid,wl.zoneid) = wl.zoneid
       and wl.status = '1'
     group by 1
      into :pdate, :qb, :qs, :qr, :qe, :qa
  do
  begin
    suspend;
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARESLOTREST_WARESLOT (
    OBJID type of R_ID,
    WARESID type of R_ID,
    ZONEID type of R_ID = null)
returns (
    PDATE type of column WARESLOT.PRODUCTDATE,
    QB type of column WARESLOTITEM.AMOUNT,
    QS type of column WARESLOTITEM.AMOUNT,
    QR type of column WARESLOTITEM.AMOUNT,
    QE type of column WARESLOTITEM.AMOUNT,
    QA type of column WARESLOTITEM.AMOUNT,
    QT type of column WARESLOTITEM.AMOUNT,
    QN type of column WARESLOTITEM.AMOUNT)
as
begin
  for
    select wl.productdate,
           sum(case sp.code when 'B' then wli.amount else 0.000 end), -- МХ
           sum(case sp.code when 'STACK' then wli.amount else 0.000 end), -- Штабель
           sum(case when sp.code starting 'BUYRET' then wli.amount else 0.000 end), -- Возврат
           sum(case sp.code when 'E' then wli.amount else 0.000 end), -- Экспедиция
           sum(case sp.calcrest when '1' then wli.amount else 0.0000 end),
           sum(case when sp.code = 'TRASH' and p.pallettype <> '1' then wli.amount else 0.000 end), -- Корзина
           sum(case when sp.code = 'TRASH' and p.pallettype = '1' then wli.amount else 0.000 end) -- Недостача
      from wareslot wl
           left join wareslotitem wli
                left join pallet p
                     left join pallet_feature pf on pf.id = p.featureid
                     left join site s
                          left join sitespecies sp
                            on sp.sitespeciesid = s.sitespeciesid
                       on s.siteid = p.siteid
                     left join pallet_type pt on pt.id = p.ptypeid
                  on p.palletid = wli.palletid
             on wli.wlotid = wl.wlotid
     where wl.objid = :objid
       and wl.waresid = :waresid
       and coalesce(:zoneid,wl.zoneid) = wl.zoneid
       and wl.status = '1'
     group by 1
      into :pdate, :qb, :qs, :qr, :qe, :qa, :qt, :qn
  do
  begin
    suspend;
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARESLOTREST_WARESLOT (
    OBJID type of R_ID,
    WARESID type of R_ID,
    ZONEID type of R_ID = null)
returns (
    PDATE type of column WARESLOT.PRODUCTDATE,
    QB type of column WARESLOTITEM.AMOUNT,
    QS type of column WARESLOTITEM.AMOUNT,
    QR type of column WARESLOTITEM.AMOUNT,
    QE type of column WARESLOTITEM.AMOUNT,
    QA type of column WARESLOTITEM.AMOUNT,
    QT type of column WARESLOTITEM.AMOUNT,
    QN type of column WARESLOTITEM.AMOUNT)
as
begin
  for
    select wl.productdate,
           sum(case sp.code when 'B' then wli.amount else 0.000 end), -- МХ
           sum(case sp.code when 'STACK' then wli.amount else 0.000 end), -- Штабель
           sum(case when sp.code starting 'BUYRET' then wli.amount else 0.000 end), -- Возврат
           sum(case when sp.code in ('E', 'GATE') then wli.amount else 0.000 end), -- Экспедиция
           sum(case sp.calcrest when '1' then wli.amount else 0.0000 end),
           sum(case when sp.code = 'TRASH' and p.pallettype <> '1' then wli.amount else 0.000 end), -- Корзина
           sum(case when sp.code = 'TRASH' and p.pallettype = '1' then wli.amount else 0.000 end) -- Недостача
      from wareslot wl
           left join wareslotitem wli
                left join pallet p
                     left join pallet_feature pf on pf.id = p.featureid
                     left join site s
                          left join sitespecies sp
                            on sp.sitespeciesid = s.sitespeciesid
                       on s.siteid = p.siteid
                     left join pallet_type pt on pt.id = p.ptypeid
                  on p.palletid = wli.palletid
             on wli.wlotid = wl.wlotid
     where wl.objid = :objid
       and wl.waresid = :waresid
       and coalesce(:zoneid,wl.zoneid) = wl.zoneid
       and wl.status = '1'
     group by 1
      into :pdate, :qb, :qs, :qr, :qe, :qa, :qt, :qn
  do
  begin
    suspend;
  end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_WH_DECALITREQ (
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
     and u.unitid = -1
    into :shortname, :factor;
  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARESLOTREST_LIST (
    OBJID type of column WARESLOTREST.OBJID)
returns (
    WID type of column WARESLOTREST.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    VUFACTOR type of column WARESUNIT.FACTOR,
    VUCODE type of column UNIT.SHORTNAME,
    MUFACTOR type of column WARESUNIT.FACTOR,
    MUCODE type of column UNIT.SHORTNAME,
    DLFACTOR type of column WARESUNIT.FACTOR,
    DLCODE type of column UNIT.SHORTNAME)
as
begin
    for
        select distinct wlr.waresid, g.code, g.name,
               vwu.factor, vu.shortname, mwu.factor, mu.shortname,
               dl.factor, dl.shortname
          from wareslotrest wlr
               left join gwares g on wlr.waresid = g.waresid
               left join waresunit vwu
                    left join unit vu on vu.unitid=vwu.unitid
                 on vwu.waresunitid = g.viewunitid
               left join waresunit mwu
                    left join unit mu on mu.unitid=mwu.unitid
                 on mwu.waresunitid = g.mainunitid
               left join k_wh_decalitreq(g.waresid) dl on 1=1
         where wlr.objid = :objid
          into :wid, :wcode, :wname,
               :vufactor, :vucode, :mufactor, :mucode,
               :dlfactor, :dlcode
    do
        suspend;
end^

SET TERM ; ^

