

CREATE EXCEPTION EXC_WH_SYACK 'Ошибка штабелирования';



DROP EXCEPTION EXC_WH_SYACK;

CREATE EXCEPTION EXC_WH_STACK 'Ошибка штабелирования';



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

        if (new.palmaxcnt is NULL) then
            exception exc_wh_stack 'Не установлено макисмально возмоное количество паллет в штабеле!';
    end

    if (new.palcurcnt is NULL) then
        new.palcurcnt = 0;

    new.dt = current_timestamp;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYSTACK (
    TASKID type of R_ID,
    STACKID type of R_ID,
    WARESID type of R_ID,
    MODELID type of R_ID,
    LINEID type of R_ID,
    PRODUCERID type of R_ID,
    PCNT type of R_NUMBER,
    PQ type of R_DOUBLE,
    PRODUCTDATE type of R_DATE,
    BESTBEFOREDATE type of R_DATE,
    IDUSER type of R_ID,
    DTBEG type of R_DATETIME = current_timestamp)
AS
declare variable i type of R_NUMBER;
declare variable WHID type of R_ID;
declare variable ZONEID type of R_ID;
declare variable MANID type of R_ID;
declare variable PNUMBER type of R_BARCODE;
declare variable PBARCODE type of R_BARCODE;
declare variable wmsid r_id;
declare variable taskwaresid r_id;
declare variable ptypeid_finishgood r_id;
declare variable palletid r_id;
declare variable wlincomeid r_id;
declare variable wlotid r_id;
declare variable docid r_id64;
declare variable cargoid r_id;
declare variable spCode type of column sitespecies.code;
begin
  if (:pq is NULL) then
      exception exc_wh_wrongamount;

  select sp.code
    from site s
         left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
   where s.siteid = :stackid
    into :spCode;


  if (:spcode not in ('STACK', 'B')) then
      exception exc_wh_wrongsitetype;

  execute procedure WH_INCOMEFG_BYPALLET_FUNDINCOME(:producerid, :whid, :waresid, :productdate, :pq*:pcnt);

  select t.docid
    from wm_task t
   where t.taskid = :taskid
    into :docid;

  select wh.zoneid, wh.whid, wh.manid
    from wh_user_infoshort(:iduser) wh
    into :zoneid, :whid, :manid;

  select k.sid
    from k_get_user_wmsessionid(:manid, 'M') k
    into :wmsid;

  select wh.id
    from wh_paltypeid_finishgood wh
    into :ptypeid_finishgood;

  update or insert into wareslot(objid, zoneid, waresid, productdate, status)
  values(:whid, :zoneid, :waresid, :productdate, '1')
  matching(objid, zoneid, waresid, productdate)
  returning wlotid
  into :wlotid;

  update or insert into wareslotincomes(docid, wlotid)
  values(:docid, :wlotid)
  matching(docid, wlotid)
  returning id
  into :wlincomeid;


  if (:spcode = 'STACK') then
      insert into site_stack(siteid, modelid, waresid, productdate, bestbeforedate)
      values( :stackid, :modelid, :waresid, :productdate, :bestbeforedate);

  i = 0;

  while (i < :pcnt) do
  begin
    insert into pallet_finishprint (manid, prodlineid, waresid, productdate, quantity, bestbeforedate, producerid)
    values (:manid, :lineid, :waresid, :productdate, :pq, :bestbeforedate, :producerid)
    returning number, barcode
    into :pnumber, :pbarcode;

    insert into pallet(ptypeid, barcode, number, siteid, zoneid, objid, status)
    values(:ptypeid_finishgood, :pbarcode, :pnumber, :stackid, :zoneid, :whid, '0')
    returning palletid
    into :palletid;

    insert into wm_task_pallet(taskid, palletid, status)
    values(:taskid, :palletid, '2');

    select tw.taskwaresid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.waresid = :waresid
      into :taskwaresid;

    if (:taskwaresid is Null) then
        insert into wm_task_wares(taskid, waresid, status, wm_sessionid, successscan, quantity, begintime)
        values(:taskid, :waresid, '1', :wmsid, :pq, :pq, :dtbeg)
        returning taskwaresid
        into :taskwaresid;
    else
        update wm_task_wares tw
           set tw.status='2',
               tw.successscan = coalesce(tw.successscan,0.000) + :pq,
               tw.quantity = coalesce(tw.quantity,0.000) + :pq,
               tw.begintime = :dtbeg,
               tw.endtime = current_timestamp,
               tw.wm_sessionid = :wmsid
         where tw.taskwaresid = :taskwaresid;

    insert into wm_task_lot(palletid,  wlotid, taskwaresid, chgwli, wlincomeid, quantity, wm_sessionid)
    values(:palletid, :wlotid, :taskwaresid, '1', :wlincomeid, :pq, :wmsid);

    execute procedure k_get_cargoid(:docid, :waresid)
      returning_values :cargoid;

    if (:cargoid is NULL) then
        insert into cargo(document, waresid, amount, price)
        values(:docid, :waresid, :pq, 0.000);
    else
        update cargo cg
           set cg.amount = cg.amount + :pq
         where cg.cargoid = :cargoid;
    
    i = :i + 1;
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYSTACK (
    TASKID type of R_ID,
    STACKID type of R_ID,
    WARESID type of R_ID,
    MODELID type of R_ID,
    LINEID type of R_ID,
    PRODUCERID type of R_ID,
    PCNT type of R_NUMBER,
    PQ type of R_DOUBLE,
    PRODUCTDATE type of R_DATE,
    BESTBEFOREDATE type of R_DATE,
    IDUSER type of R_ID,
    DTBEG type of R_DATETIME = current_timestamp)
AS
declare variable i type of R_NUMBER;
declare variable WHID type of R_ID;
declare variable ZONEID type of R_ID;
declare variable MANID type of R_ID;
declare variable PNUMBER type of R_BARCODE;
declare variable PBARCODE type of R_BARCODE;
declare variable wmsid r_id;
declare variable taskwaresid r_id;
declare variable ptypeid_finishgood r_id;
declare variable palletid r_id;
declare variable wlincomeid r_id;
declare variable wlotid r_id;
declare variable docid r_id64;
declare variable cargoid r_id;
declare variable spCode type of column sitespecies.code;
begin
  if (:pq is NULL) then
      exception exc_wh_wrongamount;

  select sp.code
    from site s
         left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
   where s.siteid = :stackid
    into :spCode;


  if (:spcode not in ('STACK', 'B')) then
      exception exc_wh_wrongsitetype;

  select t.docid
    from wm_task t
   where t.taskid = :taskid
    into :docid;

  select wh.zoneid, wh.whid, wh.manid
    from wh_user_infoshort(:iduser) wh
    into :zoneid, :whid, :manid;

  execute procedure WH_INCOMEFG_BYPALLET_FUNDINCOME(:producerid, :whid, :waresid, :productdate, :pq*:pcnt);

  select k.sid
    from k_get_user_wmsessionid(:manid, 'M') k
    into :wmsid;

  select wh.id
    from wh_paltypeid_finishgood wh
    into :ptypeid_finishgood;

  update or insert into wareslot(objid, zoneid, waresid, productdate, status)
  values(:whid, :zoneid, :waresid, :productdate, '1')
  matching(objid, zoneid, waresid, productdate)
  returning wlotid
  into :wlotid;

  update or insert into wareslotincomes(docid, wlotid)
  values(:docid, :wlotid)
  matching(docid, wlotid)
  returning id
  into :wlincomeid;


  if (:spcode = 'STACK') then
      insert into site_stack(siteid, modelid, waresid, productdate, bestbeforedate)
      values( :stackid, :modelid, :waresid, :productdate, :bestbeforedate);

  i = 0;

  while (i < :pcnt) do
  begin
    insert into pallet_finishprint (manid, prodlineid, waresid, productdate, quantity, bestbeforedate, producerid)
    values (:manid, :lineid, :waresid, :productdate, :pq, :bestbeforedate, :producerid)
    returning number, barcode
    into :pnumber, :pbarcode;

    insert into pallet(ptypeid, barcode, number, siteid, zoneid, objid, status)
    values(:ptypeid_finishgood, :pbarcode, :pnumber, :stackid, :zoneid, :whid, '0')
    returning palletid
    into :palletid;

    insert into wm_task_pallet(taskid, palletid, status)
    values(:taskid, :palletid, '2');

    select tw.taskwaresid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.waresid = :waresid
      into :taskwaresid;

    if (:taskwaresid is Null) then
        insert into wm_task_wares(taskid, waresid, status, wm_sessionid, successscan, quantity, begintime)
        values(:taskid, :waresid, '1', :wmsid, :pq, :pq, :dtbeg)
        returning taskwaresid
        into :taskwaresid;
    else
        update wm_task_wares tw
           set tw.status='2',
               tw.successscan = coalesce(tw.successscan,0.000) + :pq,
               tw.quantity = coalesce(tw.quantity,0.000) + :pq,
               tw.begintime = :dtbeg,
               tw.endtime = current_timestamp,
               tw.wm_sessionid = :wmsid
         where tw.taskwaresid = :taskwaresid;

    insert into wm_task_lot(palletid,  wlotid, taskwaresid, chgwli, wlincomeid, quantity, wm_sessionid)
    values(:palletid, :wlotid, :taskwaresid, '1', :wlincomeid, :pq, :wmsid);

    execute procedure k_get_cargoid(:docid, :waresid)
      returning_values :cargoid;

    if (:cargoid is NULL) then
        insert into cargo(document, waresid, amount, price)
        values(:docid, :waresid, :pq, 0.000);
    else
        update cargo cg
           set cg.amount = cg.amount + :pq
         where cg.cargoid = :cargoid;
    
    i = :i + 1;
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_PRINTPALLET (
    PRINTERID R_ID,
    STACKID R_ID,
    PALLETID R_ID,
    IDUSER R_ID)
AS
declare variable PrinterName type of R_NAME;
declare variable QUETASKID type of R_ID;
declare variable MANID type of R_ID;
declare variable rule varchar(60);
declare variable userfio varchar(255);
declare variable params varchar(8192);
declare variable tasktypeid R_ID;
begin
  select Name
    from WM_PRINTERS
   where printerid = :printerid
    into :PrinterName;
  if (PrinterName is null) then
    exception exc_ur_common 'Не найден принтер с таким штрих-кодом.';

  select QuetaskID from WM_CONFIG into :QUETASKID;

  execute procedure wh_ttid_incomefg
   returning_values :tasktypeid;

  execute procedure WM_GETPARAMVALUE(:tasktypeid, null,  null,  'REPORTS')
  returning_values Rule;
  select Name
    from R_REPORT
   where ReportID = :Rule
    into Rule;

  select ku.id_man, ku.fio
    from k_users ku
   where ku.id_user = :iduser
    into :manid, :userfio;
  if (:palletid is NULL) then palletid = 0;

  if (:palletid is NOT NULL and :palletid>0) then
  begin
    params = '<params><ProdLineID value="None"/>
            <WaresID value="None"/>
            <ManID value="' || cast(:manid as varchar(10)) || '"/>
            <ProducerID value="None"/>
            <PrDate value="None"/>
            <PFID value="None"/>
            <PalletID value="'||cast(:palletid as varchar(10))||'"/>
            <printer value="'||:PrinterName||'"/>
            <PrintAfterDone value="1"/></params>';

     execute procedure WM_CREATEQUEUETASK(:QUETASKID,:RULE,:userfio,:PARAMS)
      returning_values :tasktypeid;
  end
  else
  begin
    for
        select p.p_id
          from wh_incomefg_stacklistpallets(:stackid) p
          into :palletid
    do
    begin
        params = '<params><ProdLineID value="None"/>
                <WaresID value="None"/>
                <ManID value="' || cast(:manid as varchar(10)) || '"/>
                <ProducerID value="None"/>
                <PrDate value="None"/>
                <PalletID value="'||cast(:palletid as varchar(10))||'"/>
                <printer value="'||:PrinterName||'"/>
                <PrintAfterDone value="1"/></params>';
    
         execute procedure WM_CREATEQUEUETASK(:QUETASKID,:RULE,:userfio,:PARAMS)
          returning_values :tasktypeid;
    end
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYPALLET_FUNDINCOME (
    PRODUCERID type of column OBJECT.OBJID,
    WHID type of column OBJECT.OBJID,
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of R_DATE,
    QUANTITY type of R_QUANTITY)
AS
declare variable dtid_fundincome type of column doctype.doctid;
declare variable docid type of column DOCUMENT.docid;
declare variable docstat type of column r_status.code;
declare variable cargoid type of column cargo.cargoid;
begin
    execute procedure wh_dtid_fundincome('0')
     returning_values :dtid_fundincome;

    if (:dtid_fundincome is NOT NULL) then
    begin
        select first(1) d.docid, d.status
          from document d
         where d.doctype = :dtid_fundincome
           and d.fromobj = :producerid
           and d.toobj = :whid
           and d.realdocdate = :productdate
          into :docid, :docstat;
    
        if (:docid is NULL) then
        begin
            select k.docid
              from k_doccreate(:producerid, :whid, NULL, :dtid_fundincome,
                               current_date, :productdate,
                               NULL, NULL, null, NULL, NULL) k
              into :docid;
    
            update document d
               set d.status = 'c'
             where d.docid = :docid;
        end
        else if (:docstat <> 'c') then
        begin
            exception exc_wh_reserve 'Не верный статус документа прихода резерва!';
        end

        execute procedure k_get_cargoid(:docid, :waresid)
          returning_values :cargoid;

        if (:cargoid is NULL) then
            insert into cargo(document, waresid, amount, price)
            values(:docid, :waresid, :quantity, 0.000);
        else
            update cargo cg
               set cg.amount = cg.amount + :quantity
             where cg.cargoid = :cargoid;

    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYSTACK (
    TASKID type of R_ID,
    STACKID type of R_ID,
    WARESID type of R_ID,
    MODELID type of R_ID,
    LINEID type of R_ID,
    PRODUCERID type of R_ID,
    PCNT type of R_NUMBER,
    PQ type of R_DOUBLE,
    PRODUCTDATE type of R_DATE,
    BESTBEFOREDATE type of R_DATE,
    IDUSER type of R_ID,
    DTBEG type of R_DATETIME = current_timestamp)
AS
declare variable i type of R_NUMBER;
declare variable WHID type of R_ID;
declare variable ZONEID type of R_ID;
declare variable MANID type of R_ID;
declare variable PNUMBER type of R_BARCODE;
declare variable PBARCODE type of R_BARCODE;
declare variable wmsid r_id;
declare variable taskwaresid r_id;
declare variable ptypeid_finishgood r_id;
declare variable palletid r_id;
declare variable wlincomeid r_id;
declare variable wlotid r_id;
declare variable docid r_id64;
declare variable cargoid r_id;
declare variable spCode type of column sitespecies.code;
begin
  if (:pq is NULL) then
      exception exc_wh_wrongamount;

  select sp.code
    from site s
         left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
   where s.siteid = :stackid
    into :spCode;


  if (:spcode not in ('STACK', 'B')) then
      exception exc_wh_wrongsitetype;

  select t.docid
    from wm_task t
   where t.taskid = :taskid
    into :docid;

  select wh.zoneid, wh.whid, wh.manid
    from wh_user_infoshort(:iduser) wh
    into :zoneid, :whid, :manid;

  execute procedure WH_INCOMEFG_BYPALLET_FUNDINCOME(:producerid, :whid, :waresid, :productdate, :pq*:pcnt);

  select k.sid
    from k_get_user_wmsessionid(:manid, 'M') k
    into :wmsid;

  select wh.id
    from wh_paltypeid_finishgood wh
    into :ptypeid_finishgood;

  update or insert into wareslot(objid, zoneid, waresid, productdate, status)
  values(:whid, :zoneid, :waresid, :productdate, '1')
  matching(objid, zoneid, waresid, productdate)
  returning wlotid
  into :wlotid;

  update or insert into wareslotincomes(docid, wlotid)
  values(:docid, :wlotid)
  matching(docid, wlotid)
  returning id
  into :wlincomeid;


  if (:spcode = 'STACK') then
      insert into site_stack(siteid, modelid, waresid, productdate, bestbeforedate)
      values( :stackid, :modelid, :waresid, :productdate, :bestbeforedate);

  i = 0;

  while (i < :pcnt) do
  begin
    insert into pallet_finishprint (manid, prodlineid, waresid, productdate, quantity, bestbeforedate, producerid)
    values (:manid, :lineid, :waresid, :productdate, :pq, :bestbeforedate, :producerid)
    returning number, barcode
    into :pnumber, :pbarcode;

    insert into pallet(ptypeid, barcode, number, siteid, zoneid, objid, status)
    values(:ptypeid_finishgood, :pbarcode, :pnumber, :stackid, :zoneid, :whid, '0')
    returning palletid
    into :palletid;

    insert into wm_task_pallet(taskid, palletid, status)
    values(:taskid, :palletid, '2');

    select tw.taskwaresid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.waresid = :waresid
      into :taskwaresid;

    if (:taskwaresid is Null) then
        insert into wm_task_wares(taskid, waresid, status, wm_sessionid, successscan, quantity, begintime)
        values(:taskid, :waresid, '1', :wmsid, :pq, :pq, :dtbeg)
        returning taskwaresid
        into :taskwaresid;
    else
        update wm_task_wares tw
           set tw.status='2',
               tw.successscan = coalesce(tw.successscan,0.000) + :pq,
               tw.quantity = coalesce(tw.quantity,0.000) + :pq,
               tw.begintime = :dtbeg,
               tw.endtime = current_timestamp,
               tw.wm_sessionid = :wmsid
         where tw.taskwaresid = :taskwaresid;

    insert into wm_task_lot(palletid,  wlotid, taskwaresid, chgwli, wlincomeid, quantity, wm_sessionid)
    values(:palletid, :wlotid, :taskwaresid, '1', :wlincomeid, :pq, :wmsid);

    execute procedure k_get_cargoid(:docid, :waresid)
      returning_values :cargoid;

    if (:cargoid is NULL) then
        insert into cargo(document, waresid, amount, price)
        values(:docid, :waresid, :pq, 0.000);
    else
        update cargo cg
           set cg.amount = cg.amount + :pq
         where cg.cargoid = :cargoid;
    
    i = :i + 1;
  end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_FIRSTINCOMEFG_SITESTACK_INFO (
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
          into :s_wproductdate, :s_wbestbeforedate,
               :s_wid, :s_wcode, :s_wname,
               :s_wvufactor, :s_wvucode, :s_wmufactor, :s_wmucode,
               :s_palid, :s_palnum, :s_palbarcode;
    end

    suspend;
end^

SET TERM ; ^



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
          into :s_wproductdate, :s_wbestbeforedate,
               :s_wid, :s_wcode, :s_wname,
               :s_wvufactor, :s_wvucode, :s_wmufactor, :s_wmucode,
               :s_palid, :s_palnum, :s_palbarcode;
    end

    suspend;
end^

SET TERM ; ^

