

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
                   and s.status = '1'
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
                   and s.status = '1'
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
               and s.status = '1'
             order by s.name
              into :rec_sid, :rec_sname;
        end
    end

    suspend;
end^

SET TERM ; ^



ALTER TABLE PALLET_TYPE
ADD FUNDLVL1TYPE R_CODE3;



SET TERM ^ ;

CREATE OR ALTER procedure WH_DOCFREESEL_PALWARLOTS (
    TASKID type of column WM_TASK.TASKID,
    PALLETID type of column PALLET.PALLETID,
    WARESID type of column GWARES.WARESID)
returns (
    WLOTID type of column WARESLOT.WLOTID,
    PRODUCTDATE type of R_DATE,
    WLNUMBER type of column WARESLOT.WLNUMBER,
    AMOUNT type of column WARESLOTITEM.AMOUNT,
    RESERVE type of column WH_RESERVE.AMOUNT)
AS
declare variable reserveobjid type of column OBJECT.objid;
declare variable fundlvl1type type of column PALLET_TYPE.fundlvl1type;
begin
  select t.fundobjid
    from WH_DOCFREESEL_TASK_FUNDINFO(:taskid) t
    into :reserveobjid;

  select coalesce(pt.fundlvl1type, 'A')
    from pallet p
         left join pallet_type pt on pt.id = p.ptypeid
   where p.palletid = :palletid
    into :fundlvl1type;

  For
    select wl.wlotid,min(wl.productdate),min(wl.wlnumber),sum(wli.amount),
           min(iif(:fundlvl1type='BAD', r.amountbad, r.amountfree))
      from wareslotitem wli
           left join wareslot wl on wl.wlotid = wli.wlotid
           left join wh_reserve r on r.waresid = wl.waresid and r.productdate = wl.productdate and r.objid = :reserveobjid
     where wli.palletid = :palletid
       and wl.waresid = :waresid
     group by wl.wlotid
      into :wlotid,:productdate,:wlnumber,:amount,:reserve
  do
    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TVERIFY_CORRECTPALLETWARES (
    WMSESID type of R_ID,
    PALLETID type of R_ID,
    WUID type of R_ID,
    WARESLOTS varchar(1023),
    AMOUNTS varchar(1023),
    DBEG type of R_DATETIME)
AS
declare variable wordwlotid varchar(1023);
declare variable wordamount varchar(1023);
declare variable amount double precision;
declare variable qdiff double precision;
declare variable taskid type of r_id;
declare variable waresid type of r_id;
declare variable ptrashid type of r_id;
declare variable wlid type of r_id;
declare variable wufactor type of r_id;
declare variable twid type of r_id;
declare variable wlamount type of r_quantity;
declare variable i smallint;
declare variable docid type of r_id64;
declare variable qpalletwares type of r_double;
declare variable needtaskend type of r_flag;
declare variable wlincomeid type of r_id;
declare variable ptype type of r_flag;
declare variable zoneid type of column sitezone.zoneid;
declare variable objid type of column OBJECT.objid;
declare variable siteid type of column SITE.siteid;
declare variable fundlvl1type type of column pallet_type.fundlvl1type;
declare variable productdate type of R_DATE;
BEGIN
  select k.taskid
    from wh_tverify_getusertask(:wmsesid,'P',:palletid) k
    into :taskid;

  if (:dbeg is null) then dbeg = current_timestamp;

  select p.pallettype,p.zoneid,p.objid,p.siteid, coalesce(pt.fundlvl1type, 'A')
    from pallet p
         left join pallet_type pt on pt.id = p.ptypeid
   where p.palletid = :palletid
    into :ptype,:zoneid,:objid,:siteid,:fundlvl1type;

  if (:ptype = '1' and (:zoneid is NULL or :objid is NULL)) then
    select szi.zoneid,sz.objid
      from sitezone_items szi
           left join sitezone sz on sz.zoneid = szi.zoneid
     where szi.siteid = :siteid
      into :zoneid,:objid;

  select wu.factor,wu.waresid
    from waresunit wu
   where wu.waresunitid = :wuid
    into :wufactor,:waresid;

  I = 0;
  FOR
    select r.word
      from r_listwords(:wareslots, ';', 0) r
      into :wordwlotid
  do
  begin
    I = :I + 1;
    wordamount = WORDNUM(:amounts,:I,';','0');

    if (:wordamount is NULL or trim(:wordamount)='') then
        amount = 0.0000;
    else
        amount = cast(:wordamount as double precision);

    amount = :amount * :wufactor;
    if (:amount > 0.0000001) then
        insert into k_wh_siteverify_wareslot_tmp(wareslotid,amount)
        values (cast(:wordwlotid as integer),:amount);
  end


  select pid
    from k_wh_get_trash(:objid)
    into :ptrashid;

  if (:ptrashid is NULL) then
    exception exc_ur_common 'Не найден поддон НЕДОСТАЧА!';

  -- WM_TASK_WARES->QUANTITY : Кол-во, которое было на поддоне
  -- WM_TASK_WARES->SCANQUANT : Кол-во, которое стало на поддоне
  -- WM_TASK_WARES->PALLETID : Поддон

  if (:taskid is NULL) then
  begin
    execute procedure wh_tverify_taskcreate(:wmsesid,'P',:palletid,:dbeg)
     returning_values :taskid;
    needtaskend = 'T';
  end
  else needtaskend = 'F';
    

  qpalletwares = NULL;
  execute procedure wh_tverify_taskcreatewares(:taskid,:waresid,:dbeg);
  select tw.taskwaresid,tw.quantity
    from wm_task_wares tw
   where tw.taskid = :taskid and tw.waresid = :waresid and tw.status = '1'
    into :twid,:qpalletwares;
  if (:qpalletwares is NULL) then
  begin
      select sum(wli.amount)
        from wareslotitem wli
             left join wareslot wl on wl.wlotid = wli.wlotid
       where wli.palletid = :palletid
         and wl.waresid = :waresid
         and coalesce(wl.objid,:objid) = :objid
         and coalesce(wl.zoneid,:zoneid) = :zoneid
        into :qpalletwares;
    
      update wm_task_wares tw
         set tw.quantity = coalesce(:qpalletwares,0.0000)
       where tw.taskwaresid = :twid;
  end

  -- 1
  -- Сбрасываем не нужные партии в корзину на поддон Недостача
  for
    select wl.wlotid, sum(wli.amount), wl.productdate
      from wareslotitem wli
           left join wareslot wl on wl.wlotid = wli.wlotid
     where wli.palletid = :palletid
       and wl.waresid = :waresid
       and coalesce(wl.objid,:objid) = :objid
       and coalesce(wl.zoneid,:zoneid) = :zoneid
       and not exists(select *
                        from k_wh_siteverify_wareslot_tmp k
                       where k.wareslotid = wl.wlotid
                         and k.amount > 0.000001)
     group by wl.wlotid,wl.productdate
    having sum(wli.amount)>0.00001
      into :wlid, :wlamount, :productdate
  do
  begin
     if (:fundlvl1type = 'BAD') then
         insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
         values ( :waresid, :productdate, 0.000, :objid, -:wlamount, :taskid);
     else
         insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
         values ( :waresid, :productdate, -:wlamount, :objid, 0.00, :taskid);

     FOR
        select o.amount,o.wlincomeid
          from core_listwlincomes(:wlid,:palletid,-:wlamount) o
          into :amount,:wlincomeid
     do
     begin
          -- Процедура вернет расходные количества, поэтому при приходовании знак наоборот
          insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
          values(:twid,:wlid,:palletid,:amount,'1',:wlincomeid,:wmsesid);
    
          insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
          values(:twid,:wlid,:ptrashid,-:amount,'1',:wlincomeid,:wmsesid);
     end
  end
  -- 2
  -- Обрабатываем все партии, которые остались на поддоне
  for
    select k.wareslotid,k.amount,wl.productdate
      from k_wh_siteverify_wareslot_tmp k
           left join wareslot wl on wl.wlotid = k.wareslotid
     where k.amount > 0.000001
      into :wlid, :amount, :productdate
  do
  begin
    wlamount = NULL;
    select sum(wli.amount)
      from wareslotitem wli
     where wli.wlotid = :wlid and wli.palletid = :palletid
      into :wlamount;
    if (:wlamount is NULL) then wlamount = 0.000;

    qdiff = :amount - :wlamount;
    if (abs(:qdiff)>0.00001) then
    begin
        if (:qdiff < -0.00001) then -- если уменьшилось количество в партии
        begin
          if (:fundlvl1type = 'BAD') then
             insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
             values ( :waresid, :productdate, 0.000, :objid, :qdiff, :taskid);
          else
             insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
             values ( :waresid, :productdate, :qdiff, :objid, 0.00, :taskid);

          -- Сначала списываем с поддона, а потом ложим на недостачу
          FOR
            select o.amount,o.wlincomeid
              from core_listwlincomes(:wlid,:palletid,:qdiff,'N') o
              into :amount,:wlincomeid
          do
          begin
              -- Процедура вернет расходные количества, поэтому при приходовании знак наоборот
              insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
              values(:twid,:wlid,:palletid,:amount,'2',:wlincomeid,:wmsesid);
        
              insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
              values(:twid,:wlid,:ptrashid,-:amount,'2',:wlincomeid,:wmsesid);
          end
        end
        else
        begin
          -- Теперь наоборот сначала с недостачи
          FOR
            select o.amount,o.wlincomeid
              from core_listwlincomes(:wlid,:ptrashid,-:qdiff,'N') o
              into :amount,:wlincomeid
          do
          begin
              -- Процедура вернет расходные количества, поэтому при приходовании знак наоборот
              insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
              values(:twid,:wlid,:ptrashid,:amount,'2',:wlincomeid,:wmsesid);
        
              insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
              values(:twid,:wlid,:palletid,-:amount,'2',:wlincomeid,:wmsesid);
          end

          if (:fundlvl1type = 'BAD') then
             insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
             values ( :waresid, :productdate, 0.000, :objid, :qdiff, :taskid);
          else
             insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
             values ( :waresid, :productdate, :qdiff, :objid, 0.00, :taskid);
        end
    end
  end

  qpalletwares = NULL;
  select sum(tl.quantity)
    from wm_task_lot tl
   where tl.palletid = :palletid
     and tl.taskwaresid = :twid
    into :qpalletwares;
  if (:qpalletwares is NULL) then qpalletwares = 0.000;

  update wm_task_wares tw
     set tw.palletid=:palletid,tw.status = '2',
         tw.endtime=current_timestamp,
         tw.scanquant = coalesce(tw.quantity,0.000)+:qpalletwares
   where tw.taskwaresid = :twid;

  if (:needtaskend = 'T') then
    execute procedure wh_term_endtask(:taskid,:WMSESID);

  --создание документа Выверки
  select dc.docid
    from k_wh_siteverify_doc_create(:taskid,:objid,:palletid) dc
    into :docid;
END^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TVERIFY_PALLETWARESLOTS (
    PALLETID type of column PALLET.palletid,
    WARESID type of column GWARES.waresid,
    WMSESID type of column WM_SESSION.sessionid
)
returns (
    WLOTID type of column WARESLOT.wlotid,
    PRODUCTDATE type of R_DATE,
    WLNUMBER type of column WARESLOT.wlnumber,
    AMOUNT type of column WARESLOTITEM.amount,
    CANEDIT type of R_BOOL,
    RESERVE type of column WH_RESERVE.AMOUNT
)
AS
declare variable seszoneid type of column SITEZONE.zoneid;
declare variable seszoneobjid type of column OBJECT.objid;
declare variable ptCode type of column PALLET_TYPE.code;
begin
    select e.currentzone,sz.objid
      from wm_session wms
           left join employee e
                left join sitezone sz on sz.zoneid = e.currentzone
             on e.employeeid = wms.objid
     where wms.sessionid = :wmsesid
      into :seszoneid,:seszoneobjid;

    select pt.code
      from pallet p
           left join pallet_type pt on pt.id = p.ptypeid
     where p.palletid = :palletid
      into :ptCode;

    For
        select wl.wlotid,min(wl.productdate),min(wl.wlnumber),sum(wli.amount),
               max(case
                    when coalesce(wl.objid,:seszoneobjid) = :seszoneobjid and
                         coalesce(wl.zoneid,:seszoneid) = :seszoneid then '1'
                    else '0'
                   end)
          from wareslotitem wli
               left join wareslot wl
                 on wl.wlotid = wli.wlotid
               left join wh_reserve r
                 on r.waresid = wl.waresid and r.productdate = wl.productdate and r.objid = :seszoneobjid
         where wli.palletid = :palletid
           and wl.waresid = :waresid
         group by wl.wlotid
          into :wlotid,:productdate,:wlnumber,:amount,:canedit
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TVERIFY_PALLETWARESLOTS (
    PALLETID type of column PALLET.palletid,
    WARESID type of column GWARES.waresid,
    WMSESID type of column WM_SESSION.sessionid
)
returns (
    WLOTID type of column WARESLOT.wlotid,
    PRODUCTDATE type of R_DATE,
    WLNUMBER type of column WARESLOT.wlnumber,
    AMOUNT type of column WARESLOTITEM.amount,
    CANEDIT type of R_BOOL,
    RESERVE type of column WH_RESERVE.AMOUNT
)
AS
declare variable seszoneid type of column SITEZONE.zoneid;
declare variable seszoneobjid type of column OBJECT.objid;
declare variable fundlvl1type type of column PALLET_TYPE.fundlvl1type;
begin
    select e.currentzone,sz.objid
      from wm_session wms
           left join employee e
                left join sitezone sz on sz.zoneid = e.currentzone
             on e.employeeid = wms.objid
     where wms.sessionid = :wmsesid
      into :seszoneid,:seszoneobjid;

    select coalesce(pt.fundlvl1type,'A')
      from pallet p
           left join pallet_type pt on pt.id = p.ptypeid
     where p.palletid = :palletid
      into :fundlvl1type;

    For
        select wl.wlotid,min(wl.productdate),min(wl.wlnumber),sum(wli.amount),
               max(case
                    when coalesce(wl.objid,:seszoneobjid) = :seszoneobjid and
                         coalesce(wl.zoneid,:seszoneid) = :seszoneid then '1'
                    else '0'
                   end),
               min(iif(:fundlvl1type='BAD', r.amountbad, r.amountfree))
          from wareslotitem wli
               left join wareslot wl
                 on wl.wlotid = wli.wlotid
               left join wh_reserve r
                 on r.waresid = wl.waresid and r.productdate = wl.productdate and r.objid = :seszoneobjid
         where wli.palletid = :palletid
           and wl.waresid = :waresid
         group by wl.wlotid
          into :wlotid,:productdate,:wlnumber,:amount,:canedit,:reserve
    do
        suspend;
end^

SET TERM ; ^

