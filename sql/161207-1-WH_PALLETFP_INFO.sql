

SET TERM ^ ;

CREATE OR ALTER procedure WH_PALLETFP_INFO (
    ID type of column PALLET.PALLETID)
returns (
    PAL_ID type of column PALLET.PALLETID,
    PAL_NUM type of column PALLET.NUMBER,
    PAL_BARCODE type of column PALLET.BARCODE,
    PAL_STAT type of column PALLET.STATUS,
    PAL_SID type of column SITE.SITEID,
    PAL_SCURCNT type of column SITE_STACK.PALCURCNT,
    PAL_SMAXCNT type of column SITE_STACK.PALMAXCNT,
    PAL_SNAME type of column SITE.NAME,
    PAL_SPCODE type of column SITESPECIES.CODE,
    PAL_OBJID type of column OBJECT.OBJID,
    PAL_TCANMOVE type of column PALLET_TYPE.CANMOVE,
    PAL_TCODE type of column PALLET_TYPE.CODE,
    PAL_N type of column PALLET.NUM,
    PAL_FEATUREID type of column PALLET_FEATURE.ID,
    PAL_FEATURECODE type of column PALLET_FEATURE.CODE,
    PAL_FEATURENAME type of column PALLET_FEATURE.NAME,
    PAL_PRODLINENAME type of column FG_PRODLINES.NAME,
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    PRODUCTDATE type of column PALLET_FINISHPRINT.PRODUCTDATE,
    BESTBEFOREDATE type of column PALLET_FINISHPRINT.BESTBEFOREDATE,
    WQPLAN type of column PALLET_FINISHPRINT.QUANTITY,
    WQ type of column WARESLOTITEM.AMOUNT,
    PRODUCERID type of column FG_PRODUCER.OBJID,
    PRODUCERNAME type of R_VARCHAR255,
    VUFACTOR type of column WARESUNIT.FACTOR,
    VUCODE type of column UNIT.SHORTNAME,
    MUFACTOR type of column WARESUNIT.FACTOR,
    MUCODE type of column UNIT.SHORTNAME,
    WSID type of column SITE.SITEID,
    WSNAME type of column SITE.NAME,
    REC_SID type of column SITE.SITEID,
    REC_SNAME type of column SITE.NAME)
AS
declare variable siteoptionid_notfillpal type of column siteoption.id;
declare variable pal_zoneid type of column SITEZONE.zoneid;
begin
    select p.palletid, p.number, p.barcode, p.status, p.objid, p.zoneid,
           s.siteid, s.name, sp.code, pt.code, p.num,
           case
                when coalesce(p.num,0) < coalesce(ss.palcurcnt,0) then '0'
                else pt.canmove
           end, ss.palcurcnt, ss.palmaxcnt, pf.id, pf.code, pf.name
      from pallet p
           left join site s on s.siteid=p.siteid
           left join sitespecies sp on sp.sitespeciesid=s.sitespeciesid
           left join pallet_type pt on pt.id = p.ptypeid
           left join site_stack ss on ss.siteid = p.siteid
           left join pallet_feature pf on pf.id = p.featureid
     where p.palletid = :id
      into :pal_id, :pal_num, :pal_barcode, :pal_stat, :pal_objid, :pal_zoneid,
           :pal_sid, :pal_sname, :pal_spcode, :pal_tcode, :pal_n, :pal_tcanmove,
           :pal_scurcnt, :pal_smaxcnt,
           :pal_featureid, :pal_featurecode, :pal_featurename;

    select pf.waresid, g.code, g.name,
           pf.productdate, pf.quantity, pf.bestbeforedate,
           pf.producerid,
           vwu.factor, vu.shortname, mwu.factor, mu.shortname,
           pl.name
      from pallet_finishprint pf
           left join fg_prodlines pl on pl.id_prodline = pf.prodlineid
           left join gwares g
                left join waresunit vwu
                     left join unit vu on vu.unitid = vwu.unitid
                  on vwu.waresunitid = g.viewunitid
                left join waresunit mwu
                     left join unit mu on mu.unitid = mwu.unitid
                  on mwu.waresunitid = g.mainunitid
             on g.waresid = pf.waresid
     where pf.palletid = :id
      into :wid, :wcode, :wname,
           :productdate, :wqplan, :bestbeforedate,
           :producerid,
           :vufactor, :vucode, :mufactor, :mucode,
           :pal_prodlinename;

    select fullname
      from getobjectname(:producerid,'03')
      into :producername;

    select sum(wli.amount)
      from wareslotitem wli
           left join wareslot wl on wl.wlotid = wli.wlotid
     where wli.palletid = :pal_id
       and wl.waresid = :wid
      into :wq;
    if (:wq is NULL) then
        wq = 0.000;

    select wso.siteid, s.name
      from wares_select_options wso
           left join site s on s.siteid = wso.siteid
     where wso.objid = :pal_objid and wso.waresid = :wid
      into :wsid, :wsname;

    if (:pal_spcode = 'USER') then
    begin
        if (abs(:wq - :wqplan) < 0.00001) then
        begin
            if (:pal_featureid is NULL) then
                select first(1) ss.siteid, s.name
                  from site_stack ss
                       left join site s on s.siteid = ss.siteid
                 where ss.waresid = :wid
                   and ss.productdate = :productdate
                   and ss.bestbeforedate = :bestbeforedate
                   and coalesce(ss.palcurcnt,0) < coalesce(ss.palmaxcnt, 0)
                   and ss.palfeatureid is NULL
                  into :rec_sid, :rec_sname;
            else
                select first(1) ss.siteid, s.name
                  from site_stack ss
                       left join site s on s.siteid = ss.siteid
                 where ss.waresid = :wid
                   and ss.productdate = :productdate
                   and ss.bestbeforedate = :bestbeforedate
                   and coalesce(ss.palcurcnt,0) < coalesce(ss.palmaxcnt, 0)
                   and ss.palfeatureid = :pal_featureid
                  into :rec_sid, :rec_sname;
    
            if (:rec_sid is NULL) then
            begin
                select first(1) sw.siteid, s.name
                  from MODEL_STACK_REF_WARESID w
                       left join MODEL_STACK_REF_SITE_WARES sw
                            left join site_stack ss
                                 left join sitezone_items szi on szi.siteid = ss.siteid
                                 left join site s on s.siteid = sw.siteid
                              on ss.siteid = sw.siteid
                         on sw.waresid = w.waresid and sw.modelid = w.modelid
                 where w.waresid = :wid
                   and ss.waresid is NULL
                   and s.status = '1'
                   and szi.zoneid = :pal_zoneid
                 order by w.priority ascending, sw.palletcount descending, s.name ascending
                  into :rec_sid, :rec_sname;
            end
        end
        else
        begin
            execute procedure WH_SITEOPTIONID_NOTFILLPAL
             returning_values :siteoptionid_notfillpal;

            select first(1) so.siteid, s.name
              from site_options so
                   left join site s
                        left join sitezone_items szi on szi.siteid = s.siteid
                        left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                     on s.siteid = so.siteid
                   left join pallet p on p.siteid = so.siteid and p.status = '1'
             where so.optionid = :siteoptionid_notfillpal
               and p.palletid is NULL
               and sp.code = 'B'
               and s.status = '1'
               and szi.zoneid = :pal_zoneid
             order by s.name
              into :rec_sid, :rec_sname;
        end
    end

    suspend;
end^

SET TERM ; ^


