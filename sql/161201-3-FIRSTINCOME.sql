

SET TERM ^ ;

CREATE OR ALTER procedure WH_FIRSTINCOMEFG_SITESTACK_INFO (
    ID type of column SITE.SITEID)
returns (
    S_ID type of column SITE.SITEID,
    S_NAME type of column SITE.NAME,
    S_STAT type of column SITE.STATUS,
    S_MODELID type of column MODEL_STACK.MODELID,
    S_MODELNAME type of column MODEL_STACK.NAME,
    S_PALID type of column PALLET.PALLETID,
    S_PALNUM type of column PALLET.NUMBER,
    S_PALBARCODE type of column PALLET.BARCODE,
    S_SPCODE type of column SITESPECIES.CODE,
    S_SPNAME type of column SITESPECIES.NAME,
    S_PL type of column SITE.PL,
    S_PW type of column SITE.PW,
    S_PH type of column SITE.PH,
    S_WID type of column GWARES.WARESID,
    S_WCODE type of column GWARES.CODE,
    S_WNAME type of column GWARES.NAME,
    S_WVUFACTOR type of column WARESUNIT.FACTOR,
    S_WVUCODE type of column UNIT.SHORTNAME,
    S_WMUFACTOR type of column WARESUNIT.FACTOR,
    S_WMUCODE type of column UNIT.SHORTNAME,
    S_WPRODUCTDATE type of column SITE_STACK.PRODUCTDATE,
    S_WBESTBEFOREDATE type of column SITE_STACK.BESTBEFOREDATE,
    S_PALMAXCNT type of column SITE_STACK.PALMAXCNT,
    S_PALCURCNT type of column SITE_STACK.PALCURCNT)
AS
begin
    select s.siteid,s.status,s.name,
           sp.code, sp.name,
           s.pl, s.pw, s.ph
      from site s
            left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
     where s.siteid = :id
      into :s_id,:s_stat,:s_name,
           :s_spcode, :s_spname,
           :s_pl, :s_pw, :s_ph;

    if (:s_spcode = 'STACK') then
    begin
        select ms.modelid, ms.name,
               st.productdate, st.bestbeforedate,
               st.palmaxcnt, st.palcurcnt,
               g.waresid, g.code, g.name,
               vwu.factor, vu.shortname, mwu.factor, mu.shortname,
               p.palletid, p.number, p.barcode
          from site_stack st
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
         where st.siteid = :id
          into :s_modelid, s_modelname,
               :s_wproductdate, :s_wbestbeforedate,
               :s_palmaxcnt, :s_palcurcnt,
               :s_wid, :s_wcode, :s_wname,
               :s_wvufactor, :s_wvucode, :s_wmufactor, :s_wmucode,
               :s_palid, :s_palnum, :s_palbarcode;
    end
    else if (:s_spcode = 'B') then
    begin
        select first(1)
               pfp.productdate, pfp.bestbeforedate,
               g.waresid, g.code, g.name,
               vwu.factor, vu.shortname, mwu.factor, mu.shortname,
               p.palletid, p.number, p.barcode
          from pallet p
               left join pallet_finishprint pfp
                    left join gwares g
                         left join waresunit vwu
                              left join unit vu on vu.unitid = vwu.unitid
                           on vwu.waresunitid = g.viewunitid
                         left join waresunit mwu
                              left join unit mu on mu.unitid = mwu.unitid
                           on mwu.waresunitid = g.mainunitid
                      on g.waresid = pfp.waresid
                 on pfp.palletid = p.palletid
         where p.siteid = :id
         order by p.lastdate desc
          into :s_wproductdate, :s_wbestbeforedate,
               :s_wid, :s_wcode, :s_wname,
               :s_wvufactor, :s_wvucode, :s_wmufactor, :s_wmucode,
               :s_palid, :s_palnum, :s_palbarcode;
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_FIRSTINCOMEFG_SITEPALLETS (
    ID type of column SITE.SITEID)
returns (
    S_PALID type of column PALLET.PALLETID,
    S_PALNUM type of column PALLET.NUMBER,
    S_PALBARCODE type of column PALLET.BARCODE,
    S_WID type of column GWARES.WARESID,
    S_WCODE type of column GWARES.CODE,
    S_WNAME type of column GWARES.NAME,
    S_WVUFACTOR type of column WARESUNIT.FACTOR,
    S_WVUCODE type of column UNIT.SHORTNAME,
    S_WMUFACTOR type of column WARESUNIT.FACTOR,
    S_WMUCODE type of column UNIT.SHORTNAME,
    S_WPRODUCTDATE type of column SITE_STACK.PRODUCTDATE,
    S_WBESTBEFOREDATE type of column SITE_STACK.BESTBEFOREDATE
)
AS
begin
    for
        select pfp.productdate, pfp.bestbeforedate,
               g.waresid, g.code, g.name,
               vwu.factor, vu.shortname, mwu.factor, mu.shortname,
               p.palletid, p.number, p.barcode
          from pallet p
               left join pallet_finishprint pfp
                    left join gwares g
                         left join waresunit vwu
                              left join unit vu on vu.unitid = vwu.unitid
                           on vwu.waresunitid = g.viewunitid
                         left join waresunit mwu
                              left join unit mu on mu.unitid = mwu.unitid
                           on mwu.waresunitid = g.mainunitid
                      on g.waresid = pfp.waresid
                 on pfp.palletid = p.palletid
         where p.siteid = :id
         order by p.lastdate desc
          into :s_wproductdate, :s_wbestbeforedate,
               :s_wid, :s_wcode, :s_wname,
               :s_wvufactor, :s_wvucode, :s_wmufactor, :s_wmucode,
               :s_palid, :s_palnum, :s_palbarcode
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FIRSTINCOMEFG_SITEPALLETS (
    SITEID type of column SITE.SITEID,
    PALLETID type of column PALLET.palletid = null)
returns (
    S_PALID type of column PALLET.PALLETID,
    S_PALNUM type of column PALLET.NUMBER,
    S_PALBARCODE type of column PALLET.BARCODE,
    S_WID type of column GWARES.WARESID,
    S_WCODE type of column GWARES.CODE,
    S_WNAME type of column GWARES.NAME,
    S_WVUFACTOR type of column WARESUNIT.FACTOR,
    S_WVUCODE type of column UNIT.SHORTNAME,
    S_WMUFACTOR type of column WARESUNIT.FACTOR,
    S_WMUCODE type of column UNIT.SHORTNAME,
    S_WPRODUCTDATE type of column SITE_STACK.PRODUCTDATE,
    S_WBESTBEFOREDATE type of column SITE_STACK.BESTBEFOREDATE
)
AS
begin
    if (:palletid is null) then
    begin
        for
            select pfp.productdate, pfp.bestbeforedate,
                   g.waresid, g.code, g.name,
                   vwu.factor, vu.shortname, mwu.factor, mu.shortname,
                   p.palletid, p.number, p.barcode
              from pallet p
                   left join pallet_finishprint pfp
                        left join gwares g
                             left join waresunit vwu
                                  left join unit vu on vu.unitid = vwu.unitid
                               on vwu.waresunitid = g.viewunitid
                             left join waresunit mwu
                                  left join unit mu on mu.unitid = mwu.unitid
                               on mwu.waresunitid = g.mainunitid
                          on g.waresid = pfp.waresid
                     on pfp.palletid = p.palletid
             where p.siteid = :siteid
             order by p.lastdate desc
              into :s_wproductdate, :s_wbestbeforedate,
                   :s_wid, :s_wcode, :s_wname,
                   :s_wvufactor, :s_wvucode, :s_wmufactor, :s_wmucode,
                   :s_palid, :s_palnum, :s_palbarcode
        do
        begin
            suspend;
        end
    end
    else
    begin
        for
            select pfp.productdate, pfp.bestbeforedate,
                   g.waresid, g.code, g.name,
                   vwu.factor, vu.shortname, mwu.factor, mu.shortname,
                   p.palletid, p.number, p.barcode
              from pallet p
                   left join pallet_finishprint pfp
                        left join gwares g
                             left join waresunit vwu
                                  left join unit vu on vu.unitid = vwu.unitid
                               on vwu.waresunitid = g.viewunitid
                             left join waresunit mwu
                                  left join unit mu on mu.unitid = mwu.unitid
                               on mwu.waresunitid = g.mainunitid
                          on g.waresid = pfp.waresid
                     on pfp.palletid = p.palletid
             where p.siteid = :siteid
               and p.palletid = :palletid
             order by p.lastdate desc
              into :s_wproductdate, :s_wbestbeforedate,
                   :s_wid, :s_wcode, :s_wname,
                   :s_wvufactor, :s_wvucode, :s_wmufactor, :s_wmucode,
                   :s_palid, :s_palnum, :s_palbarcode
        do
        begin
            suspend;
        end        
    end
end^

SET TERM ; ^

