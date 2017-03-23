

SET TERM ^ ;

CREATE OR ALTER procedure K_WH_SPWARES_LOCATE (
    CODE type of R_CODE,
    NAME type of R_NAME,
    BCODE type of R_BARCODE)
returns (
    WID type of R_ID,
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    WSTAT type of R_STATUS,
    WGNAME type of R_NAME,
    WCOUNTRYID type of R_ID,
    WCOUNTRYNAME type of R_SHORTNAME,
    WTCODE type of R_CHOICE,
    WTNAME type of R_NAME,
    WUSEBYDATE type of R_SHORTNUMBER,
    WUBTCODE type of R_CODE,
    WUBTNAME type of R_NAME,
    WUFACTOR type of R_MULTIPLE,
    UCODE type of R_CODE,
    WPRODUCERID type of R_ID,
    WPRODUCERNAME type of R_FULLNAME,
    FRAILTY type of R_QUANTITY,
    VIEWUNIT type of R_CODE,
    VUFACTOR type of R_DOUBLE,
    WUID type of R_ID,
    ARTICUL type of R_CODE25,
    WSELGRID type of R_ID,
    WSELGRCODE type of R_CODE3,
    WSELGRNAME type of R_NAME,
    WUBTDAYS type of R_QUANTITY,
    PA type of R_FLAG)
AS
begin
  if (:code is NOT NULL) then
    for
        select g.waresid,g.code,g.name,g.status,g.frailty,g.articul,
               g.country,c.name,
               rcT.code,rcT.name,
               g.usebydate,rcU.code,rcU.name,
               wu.factor,u.shortname,
               g.producer,(select fullname from getobjectname(g.producer,NULL)),
               wg.name,vu.shortname,vwu.factor,
               wsg.id,wsg.code,wsg.name,
               cast(rcU.data as double precision)*g.usebydate,
               coalesce(g.pa,'1')
          from gwares g
               left join waresgroup wg on wg.waresgrid=g.waresgroup
               left join r_choice rcT on rcT.chtype='WT' and rcT.code=g.wartype
               left join r_choice rcU on rcU.chtype='P' and rcU.code=g.ubdtype
               left join country c on c.countryid=g.country
               left join waresunit wu
                    left join unit u on u.unitid=wu.unitid
                 on wu.waresunitid=g.mainunitid
               left join waresunit vwu
                    left join unit vu on vu.unitid=vwu.unitid
                 on vwu.waresunitid=g.viewunitid
               left join k_wares_selgroup wsg on wsg.id = g.selgroup
         where g.code = :code
          into :wid,:wcode,:wname,:wstat,:frailty,:articul,
               :wcountryid,:wcountryname,
               :wtcode,:wtname,
               :wusebydate,:wubtcode,:wubtname,
               :wufactor,:ucode,
               :wproducerid,:wproducername,
               :wgname,:viewunit,:vufactor,
               :wselgrid,:wselgrcode,:wselgrname,
               :WUBTDAYS, :pa
    do
      suspend;

  if (:bcode is NOT NULL) then
    for
        select g.waresid,g.code,g.name,g.status,g.frailty,
               g.country,c.name,
               rcT.code,rcT.name,
               g.usebydate,rcU.code,rcU.name,
               wu.factor,u.shortname,
               g.producer,(select fullname from getobjectname(g.producer,NULL)),
               wg.name,vu.shortname,vwu.factor,
               cast(rcU.data as double precision)*g.usebydate,
               coalesce(g.pa,'1')
          from waresbarcode wbc
               left join waresunit wubc on wubc.waresunitid=wbc.waresunitid
               left join gwares g on g.waresid=wubc.waresid
               left join waresgroup wg on wg.waresgrid=g.waresgroup
               left join r_choice rcT on rcT.chtype='WT' and rcT.code=g.wartype
               left join r_choice rcU on rcU.chtype='P' and rcU.code=g.ubdtype
               left join country c on c.countryid=g.country
               left join waresunit wu
                    left join unit u on u.unitid=wu.unitid
                 on wu.waresunitid=g.mainunitid
               left join waresunit vwu
                    left join unit vu on vu.unitid=vwu.unitid
                 on vwu.waresunitid=g.viewunitid
         where wbc.barcode = :bcode
          into :wid,:wcode,:wname,:wstat,:frailty,
               :wcountryid,:wcountryname,
               :wtcode,:wtname,
               :wusebydate,:wubtcode,:wubtname,
               :wufactor,:ucode,
               :wproducerid,:wproducername,
               :wgname,:viewunit,:vufactor,
               :WUBTDAYS, :pa
    do
      suspend;

  if (:name is NOT NULL) then
    for
        select g.waresid,g.code,g.name,g.status,g.frailty,
               g.country,c.name,
               rcT.code,rcT.name,
               g.usebydate,rcU.code,rcU.name,
               wu.factor,u.shortname,
               g.producer,(select fullname from getobjectname(g.producer,NULL)),
               wg.name,vu.shortname,vwu.factor,
               cast(rcU.data as double precision)*g.usebydate,
               coalesce(g.pa,'1')
          from gwares g
               left join waresgroup wg on wg.waresgrid=g.waresgroup
               left join r_choice rcT on rcT.chtype='WT' and rcT.code=g.wartype
               left join r_choice rcU on rcU.chtype='P' and rcU.code=g.ubdtype
               left join country c on c.countryid=g.country
               left join waresunit wu
                    left join unit u on u.unitid=wu.unitid
                 on wu.waresunitid=g.mainunitid
               left join waresunit vwu
                    left join unit vu on vu.unitid=vwu.unitid
                 on vwu.waresunitid=g.viewunitid
         where g.name containing :name
          into :wid,:wcode,:wname,:wstat,:frailty,
               :wcountryid,:wcountryname,
               :wtcode,:wtname,
               :wusebydate,:wubtcode,:wubtname,
               :wufactor,:ucode,
               :wproducerid,:wproducername,
               :wgname,:viewunit,:vufactor,
               :WUBTDAYS, :pa
    do
      suspend;

end^

SET TERM ; ^

