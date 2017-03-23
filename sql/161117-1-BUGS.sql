

SET TERM ^ ;

CREATE OR ALTER procedure WH_DOCMNGR_LISTCARGO (
    DOCID type of column DOCUMENT.DOCID,
    CGID type of column CARGO.CARGOID)
returns (
    CARGOID type of column CARGO.CARGOID,
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    AMOUNT type of column CARGO.AMOUNT,
    PRICE type of column CARGO.PRICE,
    DOCSUM type of column CARGO.DOCSUM,
    MUF type of column WARESUNIT.FACTOR,
    MUC type of column UNIT.SHORTNAME,
    VUF type of column WARESUNIT.FACTOR,
    VUC type of column UNIT.SHORTNAME,
    BRUTTO type of R_DOUBLE,
    NETTO type of R_DOUBLE,
    CAPACITY type of R_DOUBLE)
AS
begin
  if (:cgid is NULL) then
  begin
      for
        select w.cargoid, w.waresid, g.code, g.name,
               w.amount, w.price, w.docsum,
               mwu.factor, mu.shortname, vwu.factor, vu.shortname,
               wc.brutto, wc.netto, wc.capacity
          from wh_idx_listcargo(:docid) w
               left join gwares g
                    left join waresunit mwu
                         left join unit mu on mu.unitid = mwu.unitid
                      on mwu.waresunitid = g.mainunitid
                    left join waresunit vwu
                         left join unit vu on vu.unitid = vwu.unitid
                      on vwu.waresunitid = g.viewunitid
                 on g.waresid = w.waresid
               left join wh_wares_weightcapacity(g.waresid, w.amount) wc on 1=1
          into :cargoid, :wid, :wcode, :wname,
               :amount, :price, :docsum,
               :muf, :muc, :vuf, :vuc,
               :brutto, :netto, :capacity
      do
        suspend;
  end
  else
  begin
      select cg.cargoid, g.waresid, g.code, g.name,
             cg.amount, cg.price, cg.docsum,
             mwu.factor, mu.shortname, vwu.factor, vu.shortname,
             wc.brutto, wc.netto, wc.capacity
        from cargo cg
             left join gwares g
                  left join waresunit mwu
                       left join unit mu on mu.unitid = mwu.unitid
                    on mwu.waresunitid = g.mainunitid
                  left join waresunit vwu
                       left join unit vu on vu.unitid = vwu.unitid
                    on vwu.waresunitid = g.viewunitid
               on g.waresid = cg.waresid
             left join wh_wares_weightcapacity(g.waresid, cg.amount) wc on 1=1
       where cg.document = :docid and cg.cargoid = :cgid
        into :cargoid, :wid, :wcode, :wname,
             :amount, :price, :docsum,
             :muf, :muc, :vuf, :vuc,
             :brutto, :netto, :capacity;

      suspend;
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_COMERETURN_CHKBARCODE (
    TASKID R_ID,
    BARCODE R_BARCODE,
    WMSESID type of R_ID = null)
returns (
    PALLETID R_ID,
    SITEID R_ID)
AS
declare variable USERCODE type of R_SHORTNAME;
declare variable TTID type of R_ID;
declare variable TMID type of R_ID;
declare variable TOOBJ type of R_ID;
declare variable SPCODES type of R_FULLNAME;
declare variable OBJID_WHREJECT R_ID;
declare variable TBTID_COMERETURN R_ID;
declare variable TTID_AUTOMOVING R_ID;
declare variable TID_AUTOMOVING_PLUS R_ID;
declare variable usermanid type of R_ID;
declare variable userzoneid type of R_ID;
declare variable userwhid type of R_ID;
declare variable palmanid type of R_ID;
declare variable palzoneid type of R_ID;
declare variable palwhid type of R_ID;
declare variable palnumber type of column PALLET.number;
declare variable paltypeid_comereturn type of column pallet_type.id;
declare variable paltypeid type of column pallet_type.id;
declare variable errparam type of r_varchar255;
begin
    select first(1) wm.usercode
      from wm_prefix wm
     where :barcode starting wm.prefix
     order by strlen(wm.prefix) descending
      into :usercode;

    if (:usercode is null) then
      exception exc_ur_common 'ШК не идентифицирован!';

    select t.tasktypeid,t.taskmethodid,t.siteid,d.toobj,coalesce(:wmsesid,t.wm_sessionid)
      from wm_task t
           left join document d on d.docid = t.docid
     where t.taskid = :taskid
      into :ttid,:tmid,:siteid,:toobj,:wmsesid;

    execute procedure WH_OBJ_REJECTID(:toobj) returning_values :objid_whreject;
    if (:objid_whreject is null) then
        exception exc_wh_whreject_notfound;

    -- Получаем задания для переброски остатков
    if (:toobj <> :objid_whreject) then
    begin
        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'COMERETURN'
          into :tbtid_comereturn;

        execute procedure WH_TTID_AUTOMOVING returning_values :ttid_automoving;

        select t.taskid
          from wh_taskbond tb
               left join wm_task t
                    left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                 on t.taskid = tb.task2id
         where tb.task1id = :taskid
           and tb.taskbondtid = :tbtid_comereturn
           and t.tasktypeid = :ttid_automoving
           and tm.algorithm = 'P'
          into :tid_automoving_plus;
    end

    if (:usercode='PALLET') then
    begin
        select p.palletid, p.ptypeid, coalesce(p.number,s.name)
          from pallet p
               left join site s on s.siteid = p.siteid
         where p.barcode = :barcode
           and p.status = '1'
          into :palletid, :paltypeid, :errparam;

        select pt.id
          from wh_paltypeid_comereturn pt
          into :paltypeid_comereturn;

        select t.siteid,d.toobj,coalesce(:wmsesid,t.wm_sessionid)
          from wm_task t
               left join document d on d.docid = t.docid
         where t.taskid = :taskid
          into :siteid,:toobj,:wmsesid;

        if (:palletid is null) then
        begin
            if (:siteid is NULL) then
                exception exc_wh_taskemptysite;

            select e.employeeid,sz.zoneid,sz.objid
              from wm_session wms
                   left join employee e
                        left join sitezone sz on sz.zoneid = e.currentzone
                     on e.employeeid = wms.objid
             where wms.sessionid = :wmsesid
              into :usermanid, :userzoneid, :userwhid;
            if (:usermanid is NULL) then
                exception exc_wh_workeremptyman;
            else if (:userzoneid is NULL) then
                exception exc_wh_workeremptyzone;
            else if (:userwhid is NULL) then
                exception exc_wh_workeremptywh;
            else if (:userwhid <> :toobj) then
                exception exc_wh_workeremptywh;

            select pip.manid, pip.whid, pip.zoneid, pip.number, pip.palletid
              from pallet_comeretprint pip
             where pip.barcode = :barcode
               and pip.enabled = '1'
              into :palmanid, :palwhid, :palzoneid, :palnumber, :palletid;

            if (:palnumber is NULL) then
                exception exc_wh_palincomeprintnotfound;
            if (:usermanid <> :palmanid) then
                exception exc_wh_palincomeprinterrman;
            if (:objid_whreject <> :palwhid) then
                exception exc_wh_palincomeprinterrwh;

            if (:siteid is null) then
                exception exc_k_wrongsite 'К заданию не привязано МП!';

            if (:palletid is NULL) then
                insert into pallet(status, barcode, number, ptypeid, siteid, objid, zoneid)
                values ('1',:barcode,:palnumber,:paltypeid_comereturn,:siteid,:palwhid,:palzoneid)
                returning palletid
                into :palletid;

            if (:toobj <> :objid_whreject) then
            begin
                select tid_plus
                  from WH_AUTOMOVING_GETTASKES(:taskid,'COMERETURN','P')
                  into :tid_automoving_plus;

                insert into wm_task_pallet (taskid, palletid, siteid, status)
                values (:tid_automoving_plus, :palletid, :siteid, '2');
            end
            else
            begin
                insert into wm_task_pallet (taskid, palletid, siteid, status)
                values (:taskid, :palletid, :siteid, '2');
            end
        end
        else
        begin
            if (:paltypeid <> :paltypeid_comereturn) then
                execute procedure r_raiseerror('PALLET_ERRORTYPE',:errparam);

            if (not exists(select *
                             from pallet p
                            where p.palletid = :palletid
                              and p.objid = :objid_whreject)) then
                exception exc_wh_wrongpalletobj;
        end
    end
    else if (:usercode = 'SITE') then
    begin
        select coalesce(paramValue,'')
          from K_SITEZONEMETHOD_PARAMVALUE(:ttid,:tmid,:toobj,null,'SPCODES')
          into :spcodes;

        siteid = NULL;
        select s.siteid
          from site s
               left join sitespecies ss on s.sitespeciesid = ss.sitespeciesid
         where s.barcode = :barcode
         and (:spcodes||',') containing (ss.code||',')
          into :siteid;

        if (:siteid is null) then
            exception exc_wh_wrongsitetype;

        execute procedure wh_session_chksite(:wmsesid,:siteid,'C');

        select k.palletid
          from k_waresslot_get_sitepallet(:siteid) k
          into :palletid;

        if (:palletid is null) then
            exception exc_k_common 'К местоположению не привязан поддон!';
    end
    else
        exception exc_k_common 'Не верный ШК!';

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECT_CLIENTUNFUND (
    TASKID type of column WM_TASK.TASKID)
AS
declare variable clientid type of column OBJECT.objid;
declare variable fundobjid type of column OBJECT.objid;
declare variable docid type of column DOCUMENT.docid ;
declare variable tmid type of column wm_taskmethod.methodid;
begin
   select gor.objid, d.toobj, d.docid, t.taskmethodid
     from wm_task t
          left join document d
               left join wh_get_reserveobj(coalesce(d.throughobj, d.fromobj)) gor on 1=1
            on d.docid = t.docid
    where t.taskid = :taskid
     into :fundobjid, :clientid, :docid, :tmid;

   insert into wh_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
   select :docid, tw.waresid, tw.plandatetime, -tw.quantity, :fundobjid, :clientid
     from wm_task_wares tw
    where tw.taskid = :taskid;

   if (:tmid is NOT NULL) then
       insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
       select :docid, tw.waresid, tw.plandatetime, -tw.quantity, :fundobjid
         from wm_task_wares tw
        where tw.taskid = :taskid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable ttinitst_select type of column wm_tasktype.initstatus;
declare variable tmid_select type of column wm_taskmethod.methodid;
declare variable waresid type of column GWARES.waresid;
declare variable amount type of r_double;
declare variable numpallet type of r_number;
declare variable numpos type of r_number;
declare variable status type of r_status;
declare variable slotid type of r_id;
declare variable taskid type of r_id;
declare variable taskpalletnum type of r_number;
declare variable price type of r_double;
declare variable CAPACITY type of r_double;
declare variable WEIGHT type of r_double;
declare variable Zoneid type of r_id;
declare variable productdate type of column wm_task_wares.plandatetime;
begin
    execute procedure u3s_taskselect_create_prep(:docid);

    select k.ttid,coalesce(k.ttinitst,'0')
      from k_tasktype_by_code('SELECT',NULL) k
      into :ttid_select,:ttinitst_select;


    taskid = NULL;
    taskpalletnum = -1;
    for
        select coalesce(k.numpallet,0),k.num,k.taskmethodid,k.waresid,k.amount,k.slotid,coalesce(tm.startstatus,:ttinitst_select),k.zoneid,k.productdate
          from k_tbltmp_select_docwares k
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
         order by k.numpallet ascending nulls last,k.num ascending nulls last
          into :numpallet,:numpos,:tmid_select,:waresid,:amount,:slotid,:status,:zoneid,:productdate
    do
    begin
        if (:taskpalletnum <> :numpallet and :taskpalletnum is NOT NULL and :numpallet is NOT NULL) then
        begin
            if (:taskid is NOT NULL) then
            begin
                select sum(ww.weight),sum(ww.capacity)
                  from wm_task_wares tw
                       left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
                 where tw.taskid = :taskid
                  into :WEIGHT,:CAPACITY;
            
                update wm_task t
                   set t.weight = :weight,t.capacity = :capacity
                 where t.taskid = :taskid;
            end

            taskpalletnum = :numpallet;

            if (:zoneid = 0) then zoneid = NULL;
            insert into wm_task(tasktypeid,taskmethodid,status,docid,num,zoneid)
            values (:ttid_select,:tmid_select,:status,:docid,:numpallet,:zoneid)
            returning taskid
            into :taskid;
        end

        price = NULL;
        select round(sum(cg.docsum)/sum(cg.amount),4)
          from cargo cg
         where cg.document = :docid
           and cg.waresid = :waresid
           and cg.cargo2id is NULL
           and cg.amount > 0.0001
          into :price;
        if (:price is null) then price = 0.000;

        insert into wm_task_wares(taskid,waresid,status,quantity,siteid,num,summa,plandatetime)
        values(:taskid,:waresid,iif(:tmid_select is NOT NULL,'0',NULL),:amount,:slotid,:numpos,:price,:productdate);
    end

    if (:taskid is NOT NULL) then
    begin
        select sum(ww.weight),sum(ww.capacity)
          from wm_task_wares tw
               left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
         where tw.taskid = :taskid
          into :WEIGHT,:CAPACITY;
    
        update wm_task t
           set t.weight = :weight,t.capacity = :capacity
         where t.taskid = :taskid;
    end

    for
        select t.taskid
          from wm_task t
         where t.docid = :docid
           and t.tasktypeid = :ttid_select
           and t.taskmethodid is NULL
          into :taskid
    do
    begin
        execute procedure wh_select_clientunfund(:taskid);
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_SELECT_TASKFINISH (
    TASKID R_ID)
returns (
    TID type of R_ID,
    TSTAT type of R_STATUS,
    TSTATNAME type of R_NAME)
AS
declare variable ttCode type of r_code;
declare variable tbtid_loadselect type of r_id;
declare variable tid_loadpallet type of r_id;
declare variable tbtid_docpallets type of r_id;
declare variable tid_loaddoc type of r_id;
declare variable docid type of r_id64;
declare variable ttid_select type of r_id;
declare variable tid_gateauto type of r_id;
declare variable nextstep type of r_flag;
begin
    select tt.code,t.status,t.docid,t.tasktypeid
      from wm_task t
           left join wm_tasktype tt on tt.tasktypeid=t.tasktypeid
     where t.taskid = :taskid
      into :ttcode,:tstat,:docid,:ttid_select;

    if (:ttcode is NULL or :ttcode<>'SELECT' ) then
        exception exc_ur_common 'Задание должно быть на отборку!';

    if (:tstat<>'5') then
        exception exc_ur_common 'Задание должно быть в статусе Ожидает подтверждения!';

    select w.nextstep
      from WH_SELECTDC_TASKEND(:taskid) w
      into :nextstep;

    /*update wm_task t
       set t.taskmethodid = NULL, t.status = '0', t.wm_sessionid = NULL
     where t.taskid = :taskid;

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'DOCPALLETS'
      into :tbtid_docpallets;

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'LOADSELECT'
      into :tbtid_loadselect;

    select tb.task1id
      from wh_taskbond tb
     where tb.task2id = :tid
       and tb.taskbondtid = :tbtid_loadselect
      into :tid_loadpallet;

    if (:tid_loadpallet is NOT NULL) then
    begin
      delete from wh_taskbond tb
       where tb.task1id = :tid_loadpallet and tb.task2id = :tid and tb.taskbondtid = :tbtid_loadselect;

      select tb.task1id
        from wh_taskbond tb
       where tb.task2id = :tid_loadpallet
         and tb.taskbondtid = :tbtid_docpallets
        into :tid_loaddoc;

      if (:tid_loaddoc is NOT NULL) then
          delete from wh_taskbond tb
           where tb.task1id = :tid_loaddoc and tb.task2id = :tid_loadpallet and tb.taskbondtid = :tbtid_docpallets;

      delete from wm_task t
       where t.taskid = :tid_loadpallet;
    end

    tid_loaddoc = NULL;
    select t.taskid
      from wm_task t    
           left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
     where t.docid = :docid
       and tt.code = 'LOADAUTO'
      into :tid_loaddoc;

    if (:tid_loaddoc is NOT NULL) then
    begin
        select t.tid_gateauto
          from WH_LOADAUTODC_GETTASKBYDOC(:docid) t
          into :tid_gateauto;
        if (:tid_gateauto is NOT NULL) then
            execute procedure wh_loadpalletdc_createtaskes(:tid_gateauto);

        if (not exists(select *
                     from wh_taskbond tb
                          left join wm_task t on t.taskid = tb.task2id
                    where tb.task1id = :tid_loaddoc
                      and tb.taskbondtid = :tbtid_docpallets
                      and coalesce(t.status,'0') <> '2')) then
        begin
          execute procedure wh_ttid_select
           returning_values :ttid_select;
    
          if (not exists(select *
                           from wm_task t
                          where t.docid = :docid
                            and t.taskmethodid is NOT NULL
                            and t.tasktypeid = :ttid_select
                            and coalesce(t.status,'0') <> '2')) then
          begin
              UPDATE wm_task t
                 set t.status = '2',t.endtime = current_timestamp
               where t.taskid = :tid_loaddoc;
          end
        end
    end*/

    select t.taskid,t.status,rs.name
      from wm_task t
           left join r_status rs on rs.statustype = 'T' and rs.code=t.status
     where t.taskid = :taskid
      into :tid,:tstat,:tstatname;

    suspend;
end^

SET TERM ; ^

