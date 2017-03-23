

SET TERM ^ ;

create procedure WH_SITEOPTIONID_NOTFILLPAL
returns (
    SITEOPTIONID type of column siteoption.id
)
as
begin
    select so.id
      from siteoption so
     where so.code = 'NOTFILLPAL'
      into :siteoptionid;

    suspend;
end^

SET TERM ; ^



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
begin
    select p.palletid, p.number, p.barcode, p.status, p.objid,
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
      into :pal_id, :pal_num, :pal_barcode, :pal_stat, :pal_objid,
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
                            left join site_stack ss on ss.siteid = sw.siteid
                            left join site s on s.siteid = sw.siteid
                         on sw.waresid = w.waresid and sw.modelid = w.modelid
                 where w.waresid = :wid
                   and ss.waresid is NULL
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
                        left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                     on s.siteid = so.siteid
                   left join pallet p on p.siteid = so.siteid and p.status = '1'
             where so.optionid = :siteoptionid_notfillpal
               and p.palletid is NULL
               and sp.code = 'B'
             order by s.name
              into :rec_sid, :rec_sname;
        end
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SITEOPTIONID_NOTFILLPAL
returns (
    SITEOPTIONID type of column siteoption.id
)
as
begin
    select so.id
      from siteoption so
     where so.code = 'NOTFULLPAL'
      into :siteoptionid;

    suspend;
end^

SET TERM ; ^



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
begin
    select p.palletid, p.number, p.barcode, p.status, p.objid,
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
      into :pal_id, :pal_num, :pal_barcode, :pal_stat, :pal_objid,
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
                            left join site_stack ss on ss.siteid = sw.siteid
                            left join site s on s.siteid = sw.siteid
                         on sw.waresid = w.waresid and sw.modelid = w.modelid
                 where w.waresid = :wid
                   and ss.waresid is NULL
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
                        left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                     on s.siteid = so.siteid
                   left join pallet p on p.siteid = so.siteid and p.status = '1'
             where so.optionid = :siteoptionid_notfillpal
               and p.palletid is NULL
               and sp.code = 'B'
             order by s.name
              into :rec_sid, :rec_sname;
        end
    end

    suspend;
end^

SET TERM ; ^



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
begin
    select p.palletid, p.number, p.barcode, p.status, p.objid,
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
      into :pal_id, :pal_num, :pal_barcode, :pal_stat, :pal_objid,
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
                            left join site_stack ss on ss.siteid = sw.siteid
                            left join site s on s.siteid = sw.siteid
                         on sw.waresid = w.waresid and sw.modelid = w.modelid
                 where w.waresid = :wid
                   and ss.waresid is NULL
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
                        left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                     on s.siteid = so.siteid
                   left join pallet p on p.siteid = so.siteid and p.status = '1'
             where so.optionid = :siteoptionid_notfillpal
               and p.palletid is NULL
               and sp.code = 'B'
             order by s.name
              into :rec_sid, :rec_sname;
        end
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_STACKPAL_INFO (
    SID type of column SITE.siteid,
    PID type of column pallet.palletid,
    WMSID type of column wm_session.sessionid)
returns (
    S_ID type of column SITE.siteid,
    S_NAME type of column SITE.NAME,
    S_STAT type of column SITE.STATUS,
    S_MODELID type of column model_stack.modelid,
    S_MODELNAME type of column model_stack.NAME,
    S_PALID type of column PALLET.palletid,
    S_PALNUM type of column PALLET.number,
    S_PALBARCODE type of column PALLET.barcode,
    S_PALMAXCNT type of column site_stack.palmaxcnt,
    S_PALCURCNT type of column site_stack.palcurcnt,
    S_PALFEATUREID type of column pallet_feature.id,
    S_PALFEATURECODE type of column pallet_feature.code,
    S_PALFEATURENAME type of column pallet_feature.name,
    S_SPCODE type of column sitespecies.code,
    W_ID type of column GWARES.waresid,
    W_CODE type of column GWARES.CODE,
    W_NAME type of column GWARES.NAME,
    W_VUFACTOR type of column WARESUNIT.factor,
    W_VUCODE type of column UNIT.shortname,
    W_MUFACTOR type of column WARESUNIT.factor,
    W_MUCODE type of column UNIT.shortname,
    W_PRODUCTDATE type of column site_stack.productdate,
    W_BESTBEFOREDATE type of column site_stack.bestbeforedate,
    P_ID type of column PALLET.palletid,
    P_NUM type of column PALLET.number,
    P_BARCODE type of column PALLET.barcode,
    P_STAT type of column PALLET.status,
    P_SID type of column SITE.siteid,
    P_SNAME type of column SITE.NAME,
    P_SPCODE type of column sitespecies.code,
    P_OBJID type of column OBJECT.objid,
    P_TCANMOVE type of column pallet_type.canmove,
    P_TCODE type of column pallet_type.code,
    P_WQ type of column WARESLOTITEM.amount,
    P_WQPLAN type of column pallet_finishprint.quantity,
    P_FEATUREID type of column pallet_feature.id,
    P_FEATURECODE type of column pallet_feature.code,
    P_FEATURENAME type of column pallet_feature.name,
    CDT type of R_DATETIME)
AS
declare variable siteoptionid_notfullpal type of column siteoption.id;
begin
    if (:wmsid is NOT NULL) then
        execute procedure WH_SESSION_CHKSITE(:wmsid,:sid,'');

    select s.siteid,s.status,s.name,sp.code,
           ms.modelid, ms.name,
           st.productdate, st.bestbeforedate,
           coalesce(st.palmaxcnt,0), coalesce(st.palcurcnt,0),
           pf.id, pf.code, pf.name,
           g.waresid, g.code, g.name,
           vwu.factor, vu.shortname, mwu.factor, mu.shortname,
           p.palletid, p.number, p.barcode
      from site s
           left join site_stack st
                left join model_stack ms on ms.modelid = st.modelid
                left join gwares g
                     left join waresunit vwu
                          left join unit vu on vu.unitid = vwu.unitid
                       on vwu.waresunitid = g.viewunitid
                     left join waresunit mwu
                          left join unit mu on mu.unitid = mwu.unitid
                       on mwu.waresunitid = g.mainunitid
                  on g.waresid = st.waresid
                left join pallet p on p.palletid = st.palletid
                left join pallet_feature pf on pf.id = p.featureid
              on s.siteid = st.siteid
           left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
     where s.siteid = :sid
      into :s_id,:s_stat,:s_name,:s_spcode,
           :s_modelid, s_modelname,
           :w_productdate, :w_bestbeforedate,
           :s_palmaxcnt, :s_palcurcnt,
           :s_palfeatureid, :s_palfeaturecode, :s_palfeaturename,
           :w_id, :w_code, :w_name,
           :w_vufactor, :w_vucode, :w_mufactor, :w_mucode,
           :s_palid, :s_palnum, :s_palbarcode;

    select p.palletid, p.number, p.barcode, p.status, p.objid,
           s.siteid, s.name, sp.code, pt.code, pt.canmove,
           pf.id, pf.code, pf.name
      from pallet p
           left join site s on s.siteid=p.siteid
           left join sitespecies sp on sp.sitespeciesid=s.sitespeciesid
           left join pallet_type pt on pt.id = p.ptypeid
           left join pallet_feature pf on pf.id = p.featureid
     where p.palletid = :pid
      into :p_id, :p_num, :p_barcode, :p_stat, :p_objid,
           :p_sid, :p_sname, :p_spcode, :p_tcode, :p_tcanmove,
           :p_featureid, :p_featurecode, :p_featurename;

    select sum(wli.amount)
      from wareslotitem wli
           left join wareslot wl on wl.wlotid = wli.wlotid
     where wli.palletid = :p_id
       and wl.waresid = :w_id
      into :p_wq;

    if (:s_modelid is NOT NULL) then
    begin
        if (not exists(select *
                         from pallet_finishprint pfp
                        where pfp.palletid = :p_id
                          and pfp.waresid = :w_id
                          and pfp.productdate = :w_productdate
                          and pfp.bestbeforedate = :w_bestbeforedate
                          and abs(pfp.quantity - :p_wq) < 0.0001 )) then
            execute procedure r_raiseerror('SITESTACK_WARESINCORRECT');
    end
    else
    begin
        select pfp.productdate, pfp.bestbeforedate, pfp.quantity,
               g.waresid, g.code, g.name,
               vwu.factor, vu.shortname, mwu.factor, mu.shortname
          from pallet_finishprint pfp
               left join gwares g
                    left join waresunit vwu
                         left join unit vu on vu.unitid = vwu.unitid
                      on vwu.waresunitid = g.viewunitid
                    left join waresunit mwu
                         left join unit mu on mu.unitid = mwu.unitid
                      on mwu.waresunitid = g.mainunitid
                 on g.waresid = pfp.waresid
         where pfp.palletid = :p_id
          into :w_productdate, :w_bestbeforedate, :p_wqplan,
               :w_id, :w_code, :w_name,
               :w_vufactor, :w_vucode, :w_mufactor, :w_mucode;

        if (:s_spcode = 'STACK') then
        begin
            if (abs(:p_wqplan - :p_wq) > 0.00001) then
                exception exc_wh_wrongsitetype;
        end
        else
        begin
            if (abs(:p_wqplan - :p_wq) > 0.00001) then
            begin
                if (:s_spcode <> 'B') then
                        exception exc_wh_wrongsitetype;
                else
                begin
                    execute procedure wh_siteoptionid_notfillpal
                     returning_values :siteoptionid_notfullpal;

                    if (:siteoptionid_notfullpal is NOT NULL and
                        not exists(select *
                                     from site_options so
                                    where so.siteid = :s_id
                                      and so.optionid = :siteoptionid_notfullpal )
                    ) then
                        exception exc_wh_wrongsite;
                end
            end
            else
            begin
                if (:s_spcode = 'STACK') then
                    exception exc_wh_wrongsitetype;
            end
        end

    end

    CDT = current_timestamp;
    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_STACKPAL_INFO (
    SID type of column SITE.siteid,
    PID type of column pallet.palletid,
    WMSID type of column wm_session.sessionid)
returns (
    S_ID type of column SITE.siteid,
    S_NAME type of column SITE.NAME,
    S_STAT type of column SITE.STATUS,
    S_MODELID type of column model_stack.modelid,
    S_MODELNAME type of column model_stack.NAME,
    S_PALID type of column PALLET.palletid,
    S_PALNUM type of column PALLET.number,
    S_PALBARCODE type of column PALLET.barcode,
    S_PALMAXCNT type of column site_stack.palmaxcnt,
    S_PALCURCNT type of column site_stack.palcurcnt,
    S_PALFEATUREID type of column pallet_feature.id,
    S_PALFEATURECODE type of column pallet_feature.code,
    S_PALFEATURENAME type of column pallet_feature.name,
    S_SPCODE type of column sitespecies.code,
    W_ID type of column GWARES.waresid,
    W_CODE type of column GWARES.CODE,
    W_NAME type of column GWARES.NAME,
    W_VUFACTOR type of column WARESUNIT.factor,
    W_VUCODE type of column UNIT.shortname,
    W_MUFACTOR type of column WARESUNIT.factor,
    W_MUCODE type of column UNIT.shortname,
    W_PRODUCTDATE type of column site_stack.productdate,
    W_BESTBEFOREDATE type of column site_stack.bestbeforedate,
    P_ID type of column PALLET.palletid,
    P_NUM type of column PALLET.number,
    P_BARCODE type of column PALLET.barcode,
    P_STAT type of column PALLET.status,
    P_SID type of column SITE.siteid,
    P_SNAME type of column SITE.NAME,
    P_SPCODE type of column sitespecies.code,
    P_OBJID type of column OBJECT.objid,
    P_TCANMOVE type of column pallet_type.canmove,
    P_TCODE type of column pallet_type.code,
    P_WQ type of column WARESLOTITEM.amount,
    P_WQPLAN type of column pallet_finishprint.quantity,
    P_FEATUREID type of column pallet_feature.id,
    P_FEATURECODE type of column pallet_feature.code,
    P_FEATURENAME type of column pallet_feature.name,
    CDT type of R_DATETIME)
AS
declare variable siteoptionid_notfullpal type of column siteoption.id;
begin
    if (:wmsid is NOT NULL) then
        execute procedure WH_SESSION_CHKSITE(:wmsid,:sid,'');

    select s.siteid,s.status,s.name,sp.code,
           ms.modelid, ms.name,
           st.productdate, st.bestbeforedate,
           coalesce(st.palmaxcnt,0), coalesce(st.palcurcnt,0),
           pf.id, pf.code, pf.name,
           g.waresid, g.code, g.name,
           vwu.factor, vu.shortname, mwu.factor, mu.shortname,
           p.palletid, p.number, p.barcode
      from site s
           left join site_stack st
                left join model_stack ms on ms.modelid = st.modelid
                left join gwares g
                     left join waresunit vwu
                          left join unit vu on vu.unitid = vwu.unitid
                       on vwu.waresunitid = g.viewunitid
                     left join waresunit mwu
                          left join unit mu on mu.unitid = mwu.unitid
                       on mwu.waresunitid = g.mainunitid
                  on g.waresid = st.waresid
                left join pallet p on p.palletid = st.palletid
                left join pallet_feature pf on pf.id = p.featureid
              on s.siteid = st.siteid
           left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
     where s.siteid = :sid
      into :s_id,:s_stat,:s_name,:s_spcode,
           :s_modelid, s_modelname,
           :w_productdate, :w_bestbeforedate,
           :s_palmaxcnt, :s_palcurcnt,
           :s_palfeatureid, :s_palfeaturecode, :s_palfeaturename,
           :w_id, :w_code, :w_name,
           :w_vufactor, :w_vucode, :w_mufactor, :w_mucode,
           :s_palid, :s_palnum, :s_palbarcode;

    select p.palletid, p.number, p.barcode, p.status, p.objid,
           s.siteid, s.name, sp.code, pt.code, pt.canmove,
           pf.id, pf.code, pf.name
      from pallet p
           left join site s on s.siteid=p.siteid
           left join sitespecies sp on sp.sitespeciesid=s.sitespeciesid
           left join pallet_type pt on pt.id = p.ptypeid
           left join pallet_feature pf on pf.id = p.featureid
     where p.palletid = :pid
      into :p_id, :p_num, :p_barcode, :p_stat, :p_objid,
           :p_sid, :p_sname, :p_spcode, :p_tcode, :p_tcanmove,
           :p_featureid, :p_featurecode, :p_featurename;

    select sum(wli.amount)
      from wareslotitem wli
     where wli.palletid = :p_id
      into :p_wq;

    if (:s_modelid is NOT NULL) then
    begin
        if (not exists(select *
                         from pallet_finishprint pfp
                        where pfp.palletid = :p_id
                          and pfp.waresid = :w_id
                          and pfp.productdate = :w_productdate
                          and pfp.bestbeforedate = :w_bestbeforedate
                          and abs(pfp.quantity - :p_wq) < 0.0001 )) then
            execute procedure r_raiseerror('SITESTACK_WARESINCORRECT');
    end
    else
    begin
        select pfp.productdate, pfp.bestbeforedate, pfp.quantity,
               g.waresid, g.code, g.name,
               vwu.factor, vu.shortname, mwu.factor, mu.shortname
          from pallet_finishprint pfp
               left join gwares g
                    left join waresunit vwu
                         left join unit vu on vu.unitid = vwu.unitid
                      on vwu.waresunitid = g.viewunitid
                    left join waresunit mwu
                         left join unit mu on mu.unitid = mwu.unitid
                      on mwu.waresunitid = g.mainunitid
                 on g.waresid = pfp.waresid
         where pfp.palletid = :p_id
          into :w_productdate, :w_bestbeforedate, :p_wqplan,
               :w_id, :w_code, :w_name,
               :w_vufactor, :w_vucode, :w_mufactor, :w_mucode;

        if (:s_spcode = 'STACK') then
        begin
            if (abs(:p_wqplan - :p_wq) > 0.00001) then
                exception exc_wh_wrongsitetype;
        end
        else
        begin
            if (abs(:p_wqplan - :p_wq) > 0.00001) then
            begin
                if (:s_spcode <> 'B') then
                        exception exc_wh_wrongsitetype;
                else
                begin
                    execute procedure wh_siteoptionid_notfillpal
                     returning_values :siteoptionid_notfullpal;

                    if (:siteoptionid_notfullpal is NOT NULL and
                        not exists(select *
                                     from site_options so
                                    where so.siteid = :s_id
                                      and so.optionid = :siteoptionid_notfullpal )
                    ) then
                        exception exc_wh_wrongsite;
                end
            end
            else
            begin
                if (:s_spcode = 'STACK') then
                    exception exc_wh_wrongsitetype;
            end
        end

    end

    CDT = current_timestamp;
    suspend;
end^

SET TERM ; ^

