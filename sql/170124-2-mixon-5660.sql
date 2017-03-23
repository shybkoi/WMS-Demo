
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
    DLCODE type of column UNIT.SHORTNAME,
    EXTERNALCODE type of column GWARES.EXTERNALCODE)
as
begin
    for
        select distinct wlr.waresid, g.code, g.name, g.externalcode,
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
               :vufactor, :vucode, :mufactor, :mucode, :externalcode,
               :dlfactor, :dlcode
    do
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
    DLCODE type of column UNIT.SHORTNAME,
    EXTERNALCODE type of column GWARES.EXTERNALCODE)
as
begin
    for
        select distinct wlr.waresid, g.code, g.name, g.externalcode,
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
          into :wid, :wcode, :wname, :externalcode,
               :vufactor, :vucode, :mufactor, :mucode,
               :dlfactor, :dlcode
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
    QSP type of R_NUMBER,
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
           count(p.palletid), -- Штабель Кол-во паллет
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
      into :pdate, :qb, :qs, :qsp, :qr, :qe, :qa, :qt, :qn
  do
  begin
    suspend;
  end
end^

SET TERM ; ^



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
     and u.shortname = 'дкл'
    into :shortname, :factor;
  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_WARESLOTREST_BY_DATE (
    OBJID type of column OBJECT.OBJID,
    ZONEID type of column SITEZONE.ZONEID,
    WARESID type of column GWARES.WARESID,
    PDATE type of column WARESLOT.PRODUCTDATE)
returns (
    PNUMBER type of column PALLET.NUMBER,
    SNAME type of column SITE.NAME,
    WLIAMOUNT type of column WARESLOTITEM.AMOUNT)
as
begin
  for
   select p.number, s.name, wli.amount
     from wareslot wl
           left join wareslotitem wli
                left join pallet p
                     left join pallet_feature pf on pf.id = p.featureid
                     left join site s on s.siteid = p.siteid
                  on p.palletid = wli.palletid
             on wli.wlotid = wl.wlotid
     where wl.objid = :objid
       and wl.waresid = :waresid
       and wl.productdate = :pdate
       and coalesce(:zoneid,wl.zoneid) = wl.zoneid
       and wl.status = '1'
      into :pnumber, :sname, :wliamount
  do
    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARESLOTREST_BY_DATE (
    OBJID type of column OBJECT.OBJID,
    ZONEID type of column SITEZONE.ZONEID,
    WARESID type of column GWARES.WARESID,
    PDATE type of column WARESLOT.PRODUCTDATE)
returns (
    PNUMBER type of column PALLET.NUMBER,
    SNAME type of column SITE.NAME,
    WLIAMOUNT type of column WARESLOTITEM.AMOUNT)
as
begin
  for
   select p.number, s.name, wli.amount
     from wareslot wl
           left join wareslotitem wli
                left join pallet p
                     left join pallet_feature pf on pf.id = p.featureid
                     left join site s on s.siteid = p.siteid
                  on p.palletid = wli.palletid
             on wli.wlotid = wl.wlotid
     where wl.objid = :objid
       and wl.waresid = :waresid
       and wl.productdate = extractdate(:pdate)
       and coalesce(:zoneid,wl.zoneid) = wl.zoneid
       and wl.status = '1'
      into :pnumber, :sname, :wliamount
  do
    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARESLOTREST_BY_DATE (
    OBJID type of column OBJECT.OBJID,
    ZONEID type of column SITEZONE.ZONEID,
    WARESID type of column GWARES.WARESID,
    PDATE type of column WARESLOT.PRODUCTDATE)
returns (
    PNUMBER type of column PALLET.NUMBER,
    SNAME type of column SITE.NAME,
    WLIAMOUNT type of column WARESLOTITEM.AMOUNT)
as
begin
  for
   select p.number, s.name, wli.amount
     from wareslot wl
           left join wareslotitem wli
                left join pallet p
                     left join pallet_feature pf on pf.id = p.featureid
                     left join site s on s.siteid = p.siteid
                  on p.palletid = wli.palletid
             on wli.wlotid = wl.wlotid
     where wl.objid = :objid
       and wl.waresid = :waresid
       and coalesce(:pdate,wl.productdate) = extractdate(:pdate)
       and coalesce(:zoneid,wl.zoneid) = wl.zoneid
       and wl.status = '1'
      into :pnumber, :sname, :wliamount
  do
    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARESLOTREST_BY_DATE (
    OBJID type of column OBJECT.OBJID,
    ZONEID type of column SITEZONE.ZONEID,
    WARESID type of column GWARES.WARESID,
    PDATE type of column WARESLOT.PRODUCTDATE)
returns (
    PNUMBER type of column PALLET.NUMBER,
    SNAME type of column SITE.NAME,
    WLIAMOUNT type of column WARESLOTITEM.AMOUNT,
    APDATE type of column WARESLOT.PRODUCTDATE)
as
begin
  for
   select p.number, s.name, wli.amount, wl.productdate
     from wareslot wl
           left join wareslotitem wli
                left join pallet p
                     left join pallet_feature pf on pf.id = p.featureid
                     left join site s on s.siteid = p.siteid
                  on p.palletid = wli.palletid
             on wli.wlotid = wl.wlotid
     where wl.objid = :objid
       and wl.waresid = :waresid
       and coalesce(:pdate,wl.productdate) = extractdate(:pdate)
       and coalesce(:zoneid,wl.zoneid) = wl.zoneid
       and wl.status = '1'
      into :pnumber, :sname, :wliamount, :apdate
  do
    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARESLOTREST_BY_DATE (
    OBJID type of column OBJECT.OBJID,
    ZONEID type of column SITEZONE.ZONEID,
    WARESID type of column GWARES.WARESID,
    PDATE type of column WARESLOT.PRODUCTDATE)
returns (
    PNUMBER type of column PALLET.NUMBER,
    SNAME type of column SITE.NAME,
    WLIAMOUNT type of column WARESLOTITEM.AMOUNT,
    APDATE type of column WARESLOT.PRODUCTDATE)
as
begin
  for
   select p.number, s.name, wli.amount, wl.productdate
     from wareslot wl
           left join wareslotitem wli
                left join pallet p
                     left join pallet_feature pf on pf.id = p.featureid
                     left join site s on s.siteid = p.siteid
                  on p.palletid = wli.palletid
             on wli.wlotid = wl.wlotid
     where wl.objid = :objid
       and wl.waresid = :waresid
       and coalesce(extractdate(:pdate),wl.productdate) = wl.productdate
       and coalesce(:zoneid,wl.zoneid) = wl.zoneid
       and wl.status = '1'
      into :pnumber, :sname, :wliamount, :apdate
  do
    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARESLOTREST_BY_DATE (
    OBJID type of column OBJECT.OBJID,
    ZONEID type of column SITEZONE.ZONEID,
    WARESID type of column GWARES.WARESID,
    PDATE type of column WARESLOT.PRODUCTDATE)
returns (
    PNUMBER type of column PALLET.NUMBER,
    SNAME type of column SITE.NAME,
    WLIAMOUNT type of column WARESLOTITEM.AMOUNT,
    APDATE type of column WARESLOT.PRODUCTDATE)
as
begin
  for
   select p.number, s.name, wli.amount, wl.productdate
     from wareslot wl
           left join wareslotitem wli
                left join pallet p
                     left join pallet_feature pf on pf.id = p.featureid
                     left join site s on s.siteid = p.siteid
                  on p.palletid = wli.palletid
             on wli.wlotid = wl.wlotid
     where wl.objid = :objid
       and wl.waresid = :waresid
       and extractdate(coalesce(:pdate,wl.productdate)) = wl.productdate
       and coalesce(:zoneid,wl.zoneid) = wl.zoneid
       and wl.status = '1'
      into :pnumber, :sname, :wliamount, :apdate
  do
    suspend;
end^

SET TERM ; ^

