

SET TERM ^ ;

CREATE OR ALTER procedure FG_GET_PRODLINES
returns (
    ID_PRODLINE type of R_ID,
    NUMBER type of R_NUMBER,
    NAME type of R_NAME,
    CHGDATE type of R_FLAG,
    PRODUCERS type of R_VARCHAR255)
AS
begin
  for select id_prodline,
             number,
             name,
             coalesce(chgdate,'0'),
             listproducers
      from fg_prodlines pl
      where pl.generatorname is not null
      order by pl.name
      into :id_prodline,
           :number,
           :name,
           :chgdate,
           :producers
  do
    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_PALLETFP_INFO (
    ID R_ID)
returns (
    PAL_ID type of R_ID,
    PAL_NUM type of R_BARCODE,
    PAL_BARCODE type of R_BARCODE,
    PAL_STAT type of R_FLAG,
    PAL_SID type of R_ID,
    PAL_SCURCNT type of R_NUMBER,
    PAL_SMAXCNT type of R_NUMBER,
    PAL_SNAME type of R_NAME,
    PAL_SPCODE type of R_CODE,
    PAL_OBJID type of R_ID,
    PAL_TCANMOVE type of R_FLAG,
    PAL_TCODE type of R_CODE3,
    PAL_N type of R_NUMBER,
    PAL_FEATUREID type of R_ID,
    PAL_FEATURECODE type of R_CODE,
    PAL_FEATURENAME type of R_NAME,
    WID type of R_ID,
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    PRODUCTDATE type of R_DATE,
    BESTBEFOREDATE type of R_DATE,
    WQPLAN type of R_DOUBLE,
    WQ type of R_DOUBLE,
    PRODUCERID type of R_ID,
    PRODUCERNAME type of R_NAME,
    VUFACTOR type of R_DOUBLE,
    VUCODE type of R_CODE,
    MUFACTOR type of R_DOUBLE,
    MUCODE type of R_CODE,
    WSID type of R_ID,
    WSNAME type of R_NAME,
    REC_SID type of R_ID,
    REC_SNAME type of R_NAME)
AS
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
           vwu.factor, vu.shortname, mwu.factor, mu.shortname
      from pallet_finishprint pf
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
           :vufactor, :vucode, :mufactor, :mucode;

    select fullname
      from getobjectname(:producerid,'03')
      into :producername;

    select sum(wli.amount)
      from wareslotitem wli
     where wli.palletid = :pal_id
      into :wq;

    select wso.siteid, s.name
      from wares_select_options wso
           left join site s on s.siteid = wso.siteid
     where wso.objid = :pal_objid and wso.waresid = :wid
      into :wsid, :wsname;

    if (:pal_spcode <> 'STACK') then
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
    end
    else
    begin
        select first(1) sw.siteid
          from MODEL_STACK_REF_WARESID w
               left join MODEL_STACK_REF_SITE_WARES sw
                    left join site_stack ss on ss.siteid = sw.siteid
                 on sw.waresid = w.waresid and sw.modelid = w.modelid
         where w.waresid = :wid
           and sw.waresid is NULL
         order by w.priority ascending, sw.palletcount descending
          into :rec_sid;

        if (:rec_sid is NOT NULL) then
            select s.name
              from site s
             where s.siteid = :rec_sid
              into :rec_sname;
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_PALLETFP_INFO (
    ID R_ID)
returns (
    PAL_ID type of R_ID,
    PAL_NUM type of R_BARCODE,
    PAL_BARCODE type of R_BARCODE,
    PAL_STAT type of R_FLAG,
    PAL_SID type of R_ID,
    PAL_SCURCNT type of R_NUMBER,
    PAL_SMAXCNT type of R_NUMBER,
    PAL_SNAME type of R_NAME,
    PAL_SPCODE type of R_CODE,
    PAL_OBJID type of R_ID,
    PAL_TCANMOVE type of R_FLAG,
    PAL_TCODE type of R_CODE3,
    PAL_N type of R_NUMBER,
    PAL_FEATUREID type of R_ID,
    PAL_FEATURECODE type of R_CODE,
    PAL_FEATURENAME type of R_NAME,
    WID type of R_ID,
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    PRODUCTDATE type of R_DATE,
    BESTBEFOREDATE type of R_DATE,
    WQPLAN type of R_DOUBLE,
    WQ type of R_DOUBLE,
    PRODUCERID type of R_ID,
    PRODUCERNAME type of R_NAME,
    VUFACTOR type of R_DOUBLE,
    VUCODE type of R_CODE,
    MUFACTOR type of R_DOUBLE,
    MUCODE type of R_CODE,
    WSID type of R_ID,
    WSNAME type of R_NAME,
    REC_SID type of R_ID,
    REC_SNAME type of R_NAME)
AS
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
           vwu.factor, vu.shortname, mwu.factor, mu.shortname
      from pallet_finishprint pf
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
           :vufactor, :vucode, :mufactor, :mucode;

    select fullname
      from getobjectname(:producerid,'03')
      into :producername;

    select sum(wli.amount)
      from wareslotitem wli
     where wli.palletid = :pal_id
      into :wq;

    select wso.siteid, s.name
      from wares_select_options wso
           left join site s on s.siteid = wso.siteid
     where wso.objid = :pal_objid and wso.waresid = :wid
      into :wsid, :wsname;

    if (:pal_spcode <> 'STACK') then
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
            select first(1) sw.siteid
              from MODEL_STACK_REF_WARESID w
                   left join MODEL_STACK_REF_SITE_WARES sw
                        left join site_stack ss on ss.siteid = sw.siteid
                     on sw.waresid = w.waresid and sw.modelid = w.modelid
             where w.waresid = :wid
               and sw.waresid is NULL
             order by w.priority ascending, sw.palletcount descending
              into :rec_sid;
        
            if (:rec_sid is NOT NULL) then
                select s.name
                  from site s
                 where s.siteid = :rec_sid
                  into :rec_sname;
        end
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_PALLETFP_INFO (
    ID R_ID)
returns (
    PAL_ID type of R_ID,
    PAL_NUM type of R_BARCODE,
    PAL_BARCODE type of R_BARCODE,
    PAL_STAT type of R_FLAG,
    PAL_SID type of R_ID,
    PAL_SCURCNT type of R_NUMBER,
    PAL_SMAXCNT type of R_NUMBER,
    PAL_SNAME type of R_NAME,
    PAL_SPCODE type of R_CODE,
    PAL_OBJID type of R_ID,
    PAL_TCANMOVE type of R_FLAG,
    PAL_TCODE type of R_CODE3,
    PAL_N type of R_NUMBER,
    PAL_FEATUREID type of R_ID,
    PAL_FEATURECODE type of R_CODE,
    PAL_FEATURENAME type of R_NAME,
    WID type of R_ID,
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    PRODUCTDATE type of R_DATE,
    BESTBEFOREDATE type of R_DATE,
    WQPLAN type of R_DOUBLE,
    WQ type of R_DOUBLE,
    PRODUCERID type of R_ID,
    PRODUCERNAME type of R_NAME,
    VUFACTOR type of R_DOUBLE,
    VUCODE type of R_CODE,
    MUFACTOR type of R_DOUBLE,
    MUCODE type of R_CODE,
    WSID type of R_ID,
    WSNAME type of R_NAME,
    REC_SID type of R_ID,
    REC_SNAME type of R_NAME)
AS
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
           vwu.factor, vu.shortname, mwu.factor, mu.shortname
      from pallet_finishprint pf
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
           :vufactor, :vucode, :mufactor, :mucode;

    select fullname
      from getobjectname(:producerid,'03')
      into :producername;

    select sum(wli.amount)
      from wareslotitem wli
     where wli.palletid = :pal_id
      into :wq;

    select wso.siteid, s.name
      from wares_select_options wso
           left join site s on s.siteid = wso.siteid
     where wso.objid = :pal_objid and wso.waresid = :wid
      into :wsid, :wsname;

    if (:pal_spcode <> 'STACK') then
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

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger site_stack_bi for site_stack
active before insert position 0
as
begin
    if (new.palmaxcnt is NULL) then
    begin
        /*select count(s.number)
          from scheme_modelstack s
         where s.modelid = new.modelid
          into new.palmaxcnt;*/

        select w.palletcount
          from MODEL_STACK_REF_SITE_WARES w
         where w.siteid = new.siteid
           and w.waresid = new.waresid
           and w.modelid = new.modelid
          into new.palmaxcnt;
    end

    if (new.palcurcnt is NULL) then
        new.palcurcnt = 0;

    new.dt = current_timestamp;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_GET_MONITORING_STACK (
    SITEID type of column SITE.siteid)
returns (
    PALLETID type of column PALLET.palletid,
    PNUMBER type of column PALLET.barcode,
    PNUM type of column PALLET.number,
    PN type of column pallet.num,
    X type of R_COORD_FLOAT,
    Y type of R_COORD_FLOAT,
    Z type of R_COORD_FLOAT)
AS
declare variable modelid type of column model_stack.modelid;
declare variable palcurcnt type of column site_stack.palcurcnt;
declare variable psize type of column model_stack.psize;
declare variable psize_dp type of R_DOUBLE;
declare variable pnum_scheme type of column scheme_modelstack.number;
begin
/*  for
   select p.palletid, p.number, p.num, sm.x_coord, sm.y_coord, sm.z_coord
     from site_stack ss
     left join pallet p on p.siteid = ss.siteid
     left join scheme_modelstack sm on sm.modelid = ss.modelid and p.num = sm.number
    where ss.siteid = :siteid and p.status = 1
     into :palletid, :pnumber, :pnum, :x, :y, :z
  do
    suspend;*/

  select ss.modelid, ss.palcurcnt, ms.psize
    from site_stack ss
         left join model_stack ms on ms.modelid = ss.modelid
   where ss.siteid = :siteid
    into :modelid, :palcurcnt, :psize;
  psize_dp = cast(:psize as r_double);

  x = 0;
  y = 0;
  z = 0;

  pn = 0;
  pnum_scheme = 1;
  while (:pn < :palcurcnt) do
  begin
    pn = :pn + 1;
    select p.barcode, p.number, p.palletid
      from pallet p
     where p.siteid = :siteid
       and p.num = :pn
      into :pnumber, :pnum, :palletid;

    suspend;

    select sms.nextnumber, :x + sms.x_pdiff * :psize_dp, :y + sms.y_pdiff * :psize_dp, :z + sms.z_pdiff * :psize_dp
      from scheme_modelstack sms
     where sms.modelid = :modelid
       and sms.number = :pnum_scheme
      into :pnum_scheme, :x, :y, :z;
  end

  /*for
   select p.palletid, p.number, p.num, sm.x_coord, sm.y_coord, sm.z_coord
     from site_stack ss
          left join pallet p on p.siteid = ss.siteid
          left join scheme_modelstack sm on sm.modelid = ss.modelid and p.num = sm.number
    where ss.siteid = :siteid and p.status = 1
     into :palletid, :pnumber, :pnum, :x, :y, :z
  do
    suspend;*/
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_GET_MONITORING_STACK (
    SITEID type of column SITE.siteid)
returns (
    PALLETID type of column PALLET.palletid,
    PNUMBER type of column PALLET.barcode,
    PNUM type of column PALLET.number,
    PN type of column pallet.num,
    X type of R_COORD_FLOAT,
    Y type of R_COORD_FLOAT,
    Z type of R_COORD_FLOAT)
AS
declare variable modelid type of column model_stack.modelid;
declare variable palcurcnt type of column site_stack.palcurcnt;
declare variable psize type of column model_stack.psize;
declare variable psize_dp type of R_DOUBLE;
declare variable pnum_scheme type of column scheme_modelstack.number;
begin
/*  for
   select p.palletid, p.number, p.num, sm.x_coord, sm.y_coord, sm.z_coord
     from site_stack ss
     left join pallet p on p.siteid = ss.siteid
     left join scheme_modelstack sm on sm.modelid = ss.modelid and p.num = sm.number
    where ss.siteid = :siteid and p.status = 1
     into :palletid, :pnumber, :pnum, :x, :y, :z
  do
    suspend;*/

  select ss.modelid, ss.palcurcnt, ms.psize
    from site_stack ss
         left join model_stack ms on ms.modelid = ss.modelid
   where ss.siteid = :siteid
    into :modelid, :palcurcnt, :psize;
  psize_dp = cast(:psize as r_double);

  x = 0;
  y = 0;
  z = 0;

  pn = 0;
  pnum_scheme = 1;
  while (:pn < :palcurcnt) do
  begin
    pn = :pn + 1;
    select p.barcode, p.number, p.palletid
      from pallet p
     where p.siteid = :siteid
       and p.num = :pn
      into :pnumber, :pnum, :palletid;

    suspend;

    select sms.nextnumber, :x - sms.x_pdiff * :psize_dp, :y - sms.y_pdiff * :psize_dp, :z - sms.z_pdiff * :psize_dp
      from scheme_modelstack sms
     where sms.modelid = :modelid
       and sms.number = :pnum_scheme
      into :pnum_scheme, :x, :y, :z;
  end

  /*for
   select p.palletid, p.number, p.num, sm.x_coord, sm.y_coord, sm.z_coord
     from site_stack ss
          left join pallet p on p.siteid = ss.siteid
          left join scheme_modelstack sm on sm.modelid = ss.modelid and p.num = sm.number
    where ss.siteid = :siteid and p.status = 1
     into :palletid, :pnumber, :pnum, :x, :y, :z
  do
    suspend;*/
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_GET_MONITORING_STACK (
    SITEID type of column SITE.siteid)
returns (
    PALLETID type of column PALLET.palletid,
    PNUMBER type of column PALLET.barcode,
    PNUM type of column PALLET.number,
    PN type of column pallet.num,
    X type of R_COORD_FLOAT,
    Y type of R_COORD_FLOAT,
    Z type of R_COORD_FLOAT)
AS
declare variable modelid type of column model_stack.modelid;
declare variable palcurcnt type of column site_stack.palcurcnt;
declare variable psize type of column model_stack.psize;
declare variable psize_dp type of R_DOUBLE;
declare variable pnum_scheme type of column scheme_modelstack.number;
begin
/*  for
   select p.palletid, p.number, p.num, sm.x_coord, sm.y_coord, sm.z_coord
     from site_stack ss
     left join pallet p on p.siteid = ss.siteid
     left join scheme_modelstack sm on sm.modelid = ss.modelid and p.num = sm.number
    where ss.siteid = :siteid and p.status = 1
     into :palletid, :pnumber, :pnum, :x, :y, :z
  do
    suspend;*/

  select ss.modelid, ss.palcurcnt, ms.psize
    from site_stack ss
         left join model_stack ms on ms.modelid = ss.modelid
   where ss.siteid = :siteid
    into :modelid, :palcurcnt, :psize;
  psize_dp = cast(:psize as r_double);

  x = 0;
  y = 0;
  z = 0;

  pn = 0;
  pnum_scheme = 1;
  while (:pn < :palcurcnt) do
  begin
    pn = :pn + 1;
    select p.barcode, p.number, p.palletid
      from pallet p
     where p.siteid = :siteid
       and p.num = :pn
      into :pnumber, :pnum, :palletid;

    suspend;

    select sms.nextnumber, :x + sms.x_pdiff * :psize_dp, :y + sms.y_pdiff * :psize_dp, :z + sms.z_pdiff * :psize_dp
      from scheme_modelstack sms
     where sms.modelid = :modelid
       and sms.number = :pnum_scheme
      into :pnum_scheme, :x, :y, :z;
  end

  /*for
   select p.palletid, p.number, p.num, sm.x_coord, sm.y_coord, sm.z_coord
     from site_stack ss
          left join pallet p on p.siteid = ss.siteid
          left join scheme_modelstack sm on sm.modelid = ss.modelid and p.num = sm.number
    where ss.siteid = :siteid and p.status = 1
     into :palletid, :pnumber, :pnum, :x, :y, :z
  do
    suspend;*/
end^

SET TERM ; ^

