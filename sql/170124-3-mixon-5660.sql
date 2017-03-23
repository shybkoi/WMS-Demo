

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
           count(distinct case sp.code when 'STACK' then wli.palletid else NULL end), -- Штабель Кол-во паллет
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

CREATE OR ALTER procedure WH_WARESLOTREST_WARESLOT (
    OBJID type of R_ID,
    WARESID type of R_ID,
    ZONEID type of R_ID = null)
returns (
    PDATE type of column WARESLOT.PRODUCTDATE,
    QB type of column WARESLOTITEM.AMOUNT,
    QS type of column WARESLOTITEM.AMOUNT,
    QSP type of R_NUMBER,
    QSN type of R_NUMBER,
    QSNTITLE type of RBS_BIGVARCHAR,
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
           count(distinct case sp.code when 'STACK' then wli.palletid else NULL end), -- Штабель Кол-во паллет
           count(distinct case sp.code when 'STACK' then p.siteid else NULL end), -- Штабель Кол-во штабелей
           list(distinct case sp.code when 'STACK' then s.name else NULL end), -- Штабель наименования
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
      into :pdate, :qb, :qs, :qsp, :qsn, :qsntitle, :qr, :qe, :qa, :qt, :qn
  do
  begin
    suspend;
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARESLOTREST_BY_DATE (
    OBJID type of column OBJECT.OBJID,
    ZONEID type of column SITEZONE.ZONEID,
    WARESID type of column GWARES.WARESID,
    PDATE type of column WARESLOT.PRODUCTDATE,
    CODE type of R_CODE)
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
                     left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                  on p.palletid = wli.palletid
             on wli.wlotid = wl.wlotid
     where wl.objid = :objid
       and wl.waresid = :waresid
       and extractdate(coalesce(:pdate,wl.productdate)) = wl.productdate
       and coalesce(:zoneid,wl.zoneid) = wl.zoneid
       and wl.status = '1'
       and (
           (:code is NULL) or
           (:code = 'B' and sp.code = 'B') or
           (:code = 'STACK' and sp.code = 'STACK') or
           (:code = 'BUYRET' and sp.code starting 'BUYRET') or
           (:code = 'E' and sp.code in ('E', 'GATE')) or
           (:code = 'TRASH' and sp.code = 'TRASH' and p.pallettype <> '1') or
           (:code = 'DEFICIT' and sp.code = 'TRASH' and p.pallettype = '1')
       )
      into :pnumber, :sname, :wliamount, :apdate
  do
    suspend;
end^

SET TERM ; ^

