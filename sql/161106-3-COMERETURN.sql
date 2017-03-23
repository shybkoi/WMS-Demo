

SET TERM ^ ;

CREATE OR ALTER trigger pallet_comeretprint_bi for pallet_comeretprint
active before insert position 0
as
 declare variable flag       type of r_flag;
 declare variable palnumber bigint;

 declare variable generatorname type of r_dbname;
 declare variable mingenid type of column PALLET_TYPE.mingenid;
 declare variable maxgenid type of column PALLET_TYPE.maxgenid;
 declare variable prefixbc type of column PALLET_TYPE.prefix;
 declare variable prefixnum type of column PALLET_TYPE.prefixnum;
 declare variable palnumlength type of column PALLET_TYPE.palnumlength;
begin
    if (new.whid is NULL or new.zoneid is NULL) then
    begin
        select sz.zoneid, sz.objid
          from employee e
               left join sitezone sz on sz.zoneid = e.currentzone
         where e.employeeid = new.manid
          into new.zoneid, new.whid;

        if (new.zoneid is NULL) then
            exception exc_wh_workeremptyzone;
        else if (new.whid is NULL) then
            exception exc_wh_workeremptywh;
    end
    else if (new.zoneid is NULL) then
    begin
        select e.currentzone
          from employee e
         where e.employeeid = new.manid
          into new.zoneid;
        if (new.zoneid is NULL) then
            exception exc_wh_workeremptyzone;
    end
    else if (new.whid is NULL) then
    begin
        select sz.objid
          from employee e
               left join sitezone sz on sz.zoneid = e.currentzone
         where e.employeeid = new.manid
          into new.whid;
        if (new.whid is NULL) then
            exception exc_wh_workeremptywh;
    end
    if (new.enabled is NULL) then new.enabled = '1';

    if (new.number is NULL) then
    begin
        flag = '1';
    
        select coalesce(pt.prefix,''), coalesce(pt.prefixnum, ''),
               coalesce(pt.mingenid, 9999), coalesce(pt.maxgenid, 99999),
               coalesce(pt.palnumlength, 6)
          from pallet_type pt
         where pt.code = 'CR'
          into :prefixbc, :prefixnum, :mingenid, :maxgenid, :palnumlength;
        if (:palnumlength is NULL) then
            exception exc_k_common 'Не задана длина номера паллета';
    
        if (:generatorname is NULL) then
            generatorname = 'G_PALLET'|| trim(:prefixbc)|| 'BARCODE';
    
        while (:flag = '1') do
        begin
          execute statement 'select GEN_ID('|| :generatorname ||', 1)
                                     from wm_config'
              into :palnumber;
          if (:palnumber > :maxgenid) then
          begin
            execute statement 'select GEN_ID(' || :generatorname || ',-' || cast((:palnumber - :mingenid) as varchar(10)) ||')
                                         from wm_config'
                into :palnumber;
    
            update pallet_type pt
               set pt.series = coalesce(pt.series, 0) +1
             where pt.code = 'CR';
          end
    
          --new.number =  :linenumber || cast(:pcode as varchar(7)) || padleft(cast(:palnumber as varchar(9)),9,'0');
          new.number =  :prefixnum || padleft(cast(:palnumber as varchar(6)), :palnumlength ,'0');
    
          update pallet_comeretprint pfp
             set pfp.enabled = '0'
           where pfp.number = new.number
                 and pfp.enabled = '1';
    
          update pallet p
             set p.status = '2'
           where p.number = new.number
                 and p.status = '0';
    
          if (not exists(select *
                           from pallet p
                          where p.number = new.number
                            and p.status = '1')) then flag = '0';
        end
    end

    if (new.barcode is NULL) then
        new.barcode = 'P'||new.number;

    if (new.datetime is NULL) then
        new.datetime = current_timestamp;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_PRINT_COMERETURNPALBARCODE (
    MANID type of R_ID,
    PALLETID type of R_ID)
returns (
    NUM1 varchar(3),
    NUM2 varchar(3),
    BARCODE R_BARCODE,
    ZONENAME R_NAME,
    EMPLNAME R_FULLNAME,
    DETAIL integer)
AS
declare variable pnumber r_barcode;
declare variable objid r_id;
declare variable objid_whreject r_id;
declare variable zoneid r_id;
BEGIN
     if (:palletid is NULL or :palletid=0) then
     begin
        select sz.objid
          from employee e
               left join sitezone sz on sz.zoneid=e.currentzone
         where e.employeeid = :manid
          into :objid;

        execute procedure wh_obj_rejectid(:objid) returning_values :objid_whreject;
        select coalesce(oi.returnzone,oi.incomezone)
          from wh_obj_info oi
         where oi.objid = :objid_whreject
          into :zoneid;


        insert into pallet_comeretprint(manid, whid, zoneid)
        values (:manid, :objid_whreject, :zoneid)
        returning number, barcode
        into :pnumber, :barcode;

        detail = 0;
     end
     else
     begin
        select p.zoneid, p.number, p.barcode
          from pallet p
         where p.palletid = :palletid
          into :zoneid, :pnumber, :barcode;

        detail = 1;
     end

    num1 = SUBSTR(:pnumber, 1, 3);
    num2 = SUBSTR(:pnumber, 4, 3);
    barcode = '*' || :barcode || '*';

    select fullname
      from getobjectname(:manid,'03')
      into :emplname;

    select sz.name
      from sitezone sz
     where sz.zoneid = :zoneid
      into :zonename;

    SUSPEND;
END^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_PALTYPEID_COMERETURN
returns (
    ID type of R_ID,
    CODE type of R_CODE,
    NAME type of R_NAME)
AS
begin
    select pt.id, pt.code, pt.name
      from pallet_type pt
     where pt.code = 'CR'
      into :id, :code, :name;

    if (:id is NULL) then
        execute procedure r_raiseerror('PALLETTYPE_NOTFOUND','CR');

    suspend;
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
declare variable palnumber type of R_NUMBER;
declare variable paltypeid_comereturn type of R_ID;
declare variable paltypeid type of R_ID;
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

            select pip.manid, pip.whid, pip.zoneid, pip.number
              from pallet_comeretprint pip
             where pip.barcode = :barcode
               and pip.enabled = '1'
              into :palmanid, :palwhid, :palzoneid, :palnumber;

            if (:palnumber is NULL) then
                exception exc_wh_palincomeprintnotfound;
            if (:usermanid <> :palmanid) then
                exception exc_wh_palincomeprinterrman;
            if (:objid_whreject <> :palwhid) then
                exception exc_wh_palincomeprinterrwh;

            if (:siteid is null) then
                exception exc_k_wrongsite 'К заданию не привязано МП!';

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

            select pip.manid, pip.whid, pip.zoneid, pip.number
              from pallet_comeretprint pip
             where pip.barcode = :barcode
               and pip.enabled = '1'
              into :palmanid, :palwhid, :palzoneid, :palnumber;

            if (:palnumber is NULL) then
                exception exc_wh_palincomeprintnotfound;
            if (:usermanid <> :palmanid) then
                exception exc_wh_palincomeprinterrman;
            if (:objid_whreject <> :palwhid) then
                exception exc_wh_palincomeprinterrwh;

            if (:siteid is null) then
                exception exc_k_wrongsite 'К заданию не привязано МП!';

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

CREATE OR ALTER procedure WH_COMERETURN_ADD (
    TASKID type of R_ID,
    WUID type of R_ID,
    PRODUCTDATE type of R_DATE,
    AMOUNT type of R_DOUBLE,
    BARCODE type of R_BARCODE,
    WMSESSIONID type of R_ID,
    BEGINTIME type of R_DATETIME = null)
AS
declare variable palletid type of r_id;
declare variable wlotid type of r_id;
declare variable waresid type of r_id;
declare variable taskwaresid type of r_id;
declare variable factor type of r_double;
declare variable wlamount type of r_double;
declare variable toobj type of r_id;
declare variable fromobj type of r_id;
declare variable ttid type of r_id;
declare variable tmid type of r_id;
declare variable tstatus type of r_status;
declare variable paramValue varchar(1023);
declare variable zoneid r_id;
declare variable wlincomeid r_id;
declare variable docid r_id64;
declare variable objid_whreject r_id;
declare variable zoneid_whreject r_id;
declare variable wlotid_whreject r_id;
declare variable wlincomeid_whreject r_id;
declare variable tid_automoving_plus r_id;
declare variable tid_automoving_minus r_id;
declare variable pid_trash r_id;
declare variable twid_automoving_minus r_id;
declare variable twid_automoving_plus r_id;
declare variable wmsid_admin r_id;
declare variable docid_automoving_minus r_id64;
declare variable docid_automoving_plus r_id64;
begin
    if (:barcode is NULL) then exception exc_wh_emptybarcode;
    if (:amount is NULL or :amount < 0.0001) then exception exc_wh_emptyamount;
    if (:wuid is NULL) then exception exc_wh_emptywaresunit;
    if (:productdate is NULL or (:productdate>current_date) ) then exception exc_wh_wrongproductdate;

    select t.tasktypeid,t.taskmethodid,d.toobj,d.fromobj,t.status,d.docid
      from wm_task t
           left join document d on d.docid = t.docid
     where t.taskid = :taskid
      into :ttid,:tmid,:toobj,:fromobj,:tstatus,:docid;

    if (:tstatus='2') then exception exc_k_wrongtaskstat;

    select palletid
      from wh_comereturn_chkbarcode(:taskid,:barcode,:wmsessionid)
      into :palletid;

    select wu.factor,wu.waresid
      from waresunit wu
     where wu.waresunitid = :wuid
      into :factor,:waresid;

    amount = :factor * :amount;

    select tw.taskwaresid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.waresid = :waresid
      into :taskwaresid;

    if (:taskwaresid is NULL) then
    begin
        -- Можно убрать исключение и будет работать схема с проверкой
        select paramValue
          from k_sitezonemethod_paramvalue(:ttid,:tmid,:toobj,:fromobj,'ADDTASKWARES')
          into :paramValue;

        if (:paramvalue is NULL or :paramvalue<>'1') then
            exception exc_ur_common 'Товар не найден в задании!';
        else
            insert into wm_task_wares(taskid, waresid, successscan, status, begintime, endtime)
            values (:taskid, :waresid, 0.000, '0', :begintime, NULL)
            returning taskwaresid
            into :taskwaresid;
    end

    select coalesce(oi.returnzone,oi.incomezone)
      from wh_obj_info oi
     where oi.objid = :toobj
      into :zoneid;

    update or insert into wareslot (waresid, productdate, status, objid, zoneid)
    values(:waresid, :productdate, '1', :toobj, :zoneid)
    matching (waresid, productdate, objid, zoneid)
    returning wlotid
    into :wlotid;

    update or insert into wareslotincomes(wlotid, docid)
    values(:wlotid,:docid)
    matching(wlotid, docid)
    returning id
    into :wlincomeid;

    execute procedure WH_CORE_PALLETGETOBJ(:palletid)
     returning_values :objid_whreject;
    if (:objid_whreject is NULL) then exception exc_wh_whreject_notfound;

    if (:toobj = :objid_whreject) then
    begin
        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:taskwaresid, :wlotid, :palletid, :amount, '1', :wmsessionid, :wlincomeid);
    
        select sum(tl.quantity)
          from wm_task_lot tl
         where tl.taskwaresid = :taskwaresid
          into :wlamount;
    
        update wm_task_wares tw
           set tw.quantity = :wlamount,tw.wm_sessionid=:wmsessionid,tw.endtime=current_timestamp
         where tw.taskwaresid = :taskwaresid;
    
        update cargo cg
           set cg.amount = :wlamount,cg.docsum = NULL
         where cg.document = :docid and cg.waresid = :waresid and abs(cg.amount - :wlamount)>0.00001;
    end
    else
    begin
        select tid_plus,tid_minus
          from wh_automoving_gettaskes(:taskid,'COMERETURN','PM')
          into :tid_automoving_plus,:tid_automoving_minus;

        select k.pid
          from k_wh_get_trash(:toobj) k
          into :pid_trash;

        -- Ставим на недостачу
        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:taskwaresid, :wlotid, :pid_trash, :amount, '1', :wmsessionid, :wlincomeid);

        update wm_task_wares tw
           set tw.quantity = coalesce(tw.quantity,0.000)+:amount,tw.wm_sessionid=:wmsessionid,tw.endtime=current_timestamp
         where tw.taskwaresid = :taskwaresid;

        -- Находим данные админа для автоматической переброски
        execute procedure WH_ADMIN_GETWMSESSIONID returning_values :wmsid_admin;
        -- Сразу же с нее списываем
        select tw.taskwaresid
          from wm_task_wares tw
         where tw.taskid = :tid_automoving_minus
           and tw.waresid = :waresid
          into :twid_automoving_minus;
        if (:twid_automoving_minus is NULL) then
            insert into wm_task_wares(taskid, waresid, status, begintime, quantity)
            values (:tid_automoving_minus,:waresid, '2', current_timestamp, :amount)
            returning taskwaresid
            into :twid_automoving_minus;
        else
            update wm_task_wares tw
               set tw.quantity = coalesce(tw.quantity,0.000) + :amount,tw.status = '2'
             where tw.taskwaresid = :twid_automoving_minus;

        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:twid_automoving_minus, :wlotid, :pid_trash, -:amount, '1', :wmsid_admin, :wlincomeid);

        -- Ставим на приход другого склада
        select tw.taskwaresid
          from wm_task_wares tw
         where tw.taskid = :tid_automoving_plus
           and tw.waresid = :waresid
          into :twid_automoving_plus;

        if (:twid_automoving_plus is NULL) then
            insert into wm_task_wares(taskid, waresid, status, begintime, quantity)
            values (:tid_automoving_plus,:waresid, '2', current_timestamp, :amount)
            returning taskwaresid
            into :twid_automoving_plus;
        else
            update wm_task_wares tw
               set tw.quantity = coalesce(tw.quantity,0.000) + :amount,tw.status = '2'
             where tw.taskwaresid = :twid_automoving_plus;

        select coalesce(wh.returnzone,wh.incomezone)
          from wh_obj_info wh
         where wh.objid = :objid_whreject
          into :zoneid_whreject;

        update or insert into wareslot (waresid, productdate, status, objid, zoneid)
        values(:waresid, :productdate, '1', :objid_whreject, :zoneid_whreject)
        matching (waresid, productdate, objid, zoneid)
        returning wlotid
        into :wlotid_whreject;

        update or insert into wareslotincomes(wlotid, docid)
        values(:wlotid_whreject,NULL)
        matching(wlotid, docid)
        returning id
        into :wlincomeid_whreject;

        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:twid_automoving_plus, :wlotid_whreject, :palletid, :amount, '1', :wmsid_admin, :wlincomeid_whreject);

        update cargo cg
           set cg.amount = cg.amount + :amount,cg.docsum = NULL
         where cg.document = :docid and cg.waresid = :waresid;

        select t.docid
          from wm_task t
         where t.taskid = :tid_automoving_minus
          into :docid_automoving_minus;
        if (:docid_automoving_minus is NOT NULL) then
            update cargo cg
               set cg.amount = cg.amount + :amount,cg.docsum = NULL
             where cg.document = :docid_automoving_minus and cg.waresid = :waresid;
            
        select t.docid
          from wm_task t
         where t.taskid = :tid_automoving_plus
          into :docid_automoving_plus;
        if (:docid_automoving_plus is NOT NULL) then
            update cargo cg
               set cg.amount = cg.amount + :amount,cg.docsum = NULL
             where cg.document = :docid_automoving_plus and cg.waresid = :waresid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger t_bipallet for pallet
active before insert position 1
AS
declare variable ptypecode type of r_code3;
declare variable ptypeprefix type of r_flag;
declare variable flag type of r_flag;
BEGIN
  select pt.oldpallettype,pt.code,coalesce(pt.prefix,'')
    from pallet_type pt
   where pt.id = new.ptypeid
    into new.pallettype,:ptypecode,:ptypeprefix;

  if (:ptypecode = 'V') then
  begin
    new.barcode = NULL;
    new.zoneid = NULL;
    new.objid = NULL;
  end
  else if (:ptypecode = 'NOT') then
  begin
    new.barcode = NULL;    
    new.zoneid = NULL;
    new.objid = NULL;
  end
  else if (:ptypecode in ('I','T','FP','CR')) then -- Паллет приемки или транзита
  begin
      if (new.barcode is not NULL) then
      begin
        if (exists(select *
                     from pallet p
                    where p.barcode = new.barcode
                      and p.status <> '2'
                      and p.palletid <> new.palletid)) then
            execute procedure r_raiseerror('PALLET_EXISTSBARCODE',new.barcode);
      end
      else if (new.number is NOT NULL) then
      begin
        if (exists(select *
                     from pallet p
                    where p.number = new.number
                      and p.status <> '2'
                      and p.ptypeid = new.ptypeid
                      and p.palletid <> new.palletid)) then
            execute procedure r_raiseerror('PALLET_EXISTSNUMBER',new.barcode);
      end

      -- Генерация должна пройти через таблицу PALLET_INCOMEPRINT
      if (new.barcode is NULL or new.number is NULL) then
            execute procedure r_raiseerror('ERROR_DATA');
  end
  else
  begin
      if (new.zoneid is NULL) then
      begin
        if (new.objid is NOT NULL) then
            select wh.incomezone
              from wh_obj_info wh
             where wh.objid = new.objid
              into new.zoneid;
        if (new.zoneid is NULL) then
            execute procedure r_raiseerror('PALLET_EMPTYZONE');
      end
      else if (new.objid is NULL) then
      begin
        if (new.zoneid is NOT NULL) then
            select sz.objid
              from sitezone sz
             where sz.zoneid = new.zoneid
              into new.objid;
        if (new.objid is NULL) then
            execute procedure r_raiseerror('PALLET_EMPTYOBJECT');
      end
      else
      begin
        if (not exists(select *
                         from sitezone sz
                        where sz.zoneid = new.zoneid
                          and sz.objid = new.objid )) then
            execute procedure r_raiseerror('ZONE_ERROROBJECT');
      end

      if (:ptypeprefix='') then
        execute procedure r_raiseerror('PALLETTYPE_EMPTYPREFIX',:ptypecode);

      flag = '1';
      while (:flag = '1') do
      begin
        execute statement 'select GEN_ID(G_PALLET'||:ptypeprefix||'BARCODE, 1)
                             from wm_config'
           into new.number;
        if (new.number = '100000') then
            execute statement 'select GEN_ID(G_PALLET'||:ptypeprefix||'BARCODE, -90000)
                                 from wm_config'
               into new.number;
        new.number = :ptypeprefix || new.number;

        update pallet p
           set p.status = '2'
         where p.number = new.number and p.status = '0';

        if (not exists(select *
                         from pallet p
                        where p.number = new.number
                          and p.status = '1'
                          and p.ptypeid = new.ptypeid)) then flag = '0';
      end

      new.barcode = 'P' || new.number;
  end

  new.status = '0'; -- Должен стать 1 когда на него попадет товар
END^

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

            select pip.manid, pip.whid, pip.zoneid, pip.number
              from pallet_comeretprint pip
             where pip.barcode = :barcode
               and pip.enabled = '1'
              into :palmanid, :palwhid, :palzoneid, :palnumber;

            if (:palnumber is NULL) then
                exception exc_wh_palincomeprintnotfound;
            if (:usermanid <> :palmanid) then
                exception exc_wh_palincomeprinterrman;
            if (:objid_whreject <> :palwhid) then
                exception exc_wh_palincomeprinterrwh;

            if (:siteid is null) then
                exception exc_k_wrongsite 'К заданию не привязано МП!';

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

CREATE OR ALTER procedure WH_COMERETURN_ADD (
    TASKID type of R_ID,
    WUID type of R_ID,
    PRODUCTDATE type of R_DATE,
    AMOUNT type of R_DOUBLE,
    BARCODE type of R_BARCODE,
    WMSESSIONID type of R_ID,
    BEGINTIME type of R_DATETIME = null)
AS
declare variable palletid type of r_id;
declare variable wlotid type of r_id;
declare variable waresid type of r_id;
declare variable taskwaresid type of r_id;
declare variable factor type of r_double;
declare variable wlamount type of r_double;
declare variable toobj type of r_id;
declare variable fromobj type of r_id;
declare variable ttid type of r_id;
declare variable tmid type of r_id;
declare variable tstatus type of r_status;
declare variable paramValue varchar(1023);
declare variable zoneid r_id;
declare variable wlincomeid r_id;
declare variable docid r_id64;
declare variable objid_whreject r_id;
declare variable zoneid_whreject r_id;
declare variable wlotid_whreject r_id;
declare variable wlincomeid_whreject r_id;
declare variable tid_automoving_plus r_id;
declare variable tid_automoving_minus r_id;
declare variable pid_trash r_id;
declare variable twid_automoving_minus r_id;
declare variable twid_automoving_plus r_id;
declare variable wmsid_admin r_id;
declare variable docid_automoving_minus r_id64;
declare variable docid_automoving_plus r_id64;
begin
    if (:barcode is NULL) then exception exc_wh_emptybarcode;
    if (:amount is NULL or :amount < 0.0001) then exception exc_wh_emptyamount;
    if (:wuid is NULL) then exception exc_wh_emptywaresunit;
    if (:productdate is NULL or (:productdate>current_date) ) then exception exc_wh_wrongproductdate;

    select t.tasktypeid,t.taskmethodid,d.toobj,d.fromobj,t.status,d.docid
      from wm_task t
           left join document d on d.docid = t.docid
     where t.taskid = :taskid
      into :ttid,:tmid,:toobj,:fromobj,:tstatus,:docid;

    if (:tstatus='2') then exception exc_k_wrongtaskstat;

    select palletid
      from wh_comereturn_chkbarcode(:taskid,:barcode,:wmsessionid)
      into :palletid;

    select wu.factor,wu.waresid
      from waresunit wu
     where wu.waresunitid = :wuid
      into :factor,:waresid;

    amount = :factor * :amount;

    select tw.taskwaresid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.waresid = :waresid
      into :taskwaresid;

    if (:taskwaresid is NULL) then
    begin
        -- Можно убрать исключение и будет работать схема с проверкой
        select paramValue
          from k_sitezonemethod_paramvalue(:ttid,:tmid,:toobj,:fromobj,'ADDTASKWARES')
          into :paramValue;

        if (:paramvalue is NULL or :paramvalue<>'1') then
            exception exc_ur_common 'Товар не найден в задании!';
        else
            insert into wm_task_wares(taskid, waresid, successscan, status, begintime, endtime)
            values (:taskid, :waresid, 0.000, '0', :begintime, NULL)
            returning taskwaresid
            into :taskwaresid;
    end

    select coalesce(oi.returnzone,oi.incomezone)
      from wh_obj_info oi
     where oi.objid = :toobj
      into :zoneid;

    update or insert into wareslot (waresid, productdate, status, objid, zoneid)
    values(:waresid, :productdate, '1', :toobj, :zoneid)
    matching (waresid, productdate, objid, zoneid)
    returning wlotid
    into :wlotid;

    update or insert into wareslotincomes(wlotid, docid)
    values(:wlotid,:docid)
    matching(wlotid, docid)
    returning id
    into :wlincomeid;

    execute procedure WH_CORE_PALLETGETOBJ(:palletid)
     returning_values :objid_whreject;
    if (:objid_whreject is NULL) then exception exc_wh_whreject_notfound;

    if (:toobj = :objid_whreject) then
    begin
        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:taskwaresid, :wlotid, :palletid, :amount, '1', :wmsessionid, :wlincomeid);
    
        select sum(tl.quantity)
          from wm_task_lot tl
         where tl.taskwaresid = :taskwaresid
          into :wlamount;
    
        update wm_task_wares tw
           set tw.quantity = :wlamount,tw.wm_sessionid=:wmsessionid,tw.endtime=current_timestamp
         where tw.taskwaresid = :taskwaresid;
    
        update cargo cg
           set cg.amount = :wlamount,cg.docsum = NULL
         where cg.document = :docid and cg.waresid = :waresid and abs(cg.amount - :wlamount)>0.00001;
    end
    else
    begin
        select tid_plus,tid_minus
          from wh_automoving_gettaskes(:taskid,'COMERETURN','PM')
          into :tid_automoving_plus,:tid_automoving_minus;

        select k.pid
          from k_wh_get_trash(:toobj) k
          into :pid_trash;

        -- Ставим на недостачу
        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:taskwaresid, :wlotid, :pid_trash, :amount, '1', :wmsessionid, :wlincomeid);

        update wm_task_wares tw
           set tw.quantity = coalesce(tw.quantity,0.000)+:amount,tw.wm_sessionid=:wmsessionid,tw.endtime=current_timestamp
         where tw.taskwaresid = :taskwaresid;

        -- Находим данные админа для автоматической переброски
        execute procedure WH_ADMIN_GETWMSESSIONID returning_values :wmsid_admin;
        -- Сразу же с нее списываем
        select tw.taskwaresid
          from wm_task_wares tw
         where tw.taskid = :tid_automoving_minus
           and tw.waresid = :waresid
          into :twid_automoving_minus;
        if (:twid_automoving_minus is NULL) then
            insert into wm_task_wares(taskid, waresid, status, begintime, quantity)
            values (:tid_automoving_minus,:waresid, '2', current_timestamp, :amount)
            returning taskwaresid
            into :twid_automoving_minus;
        else
            update wm_task_wares tw
               set tw.quantity = coalesce(tw.quantity,0.000) + :amount,tw.status = '2'
             where tw.taskwaresid = :twid_automoving_minus;

        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:twid_automoving_minus, :wlotid, :pid_trash, -:amount, '1', :wmsid_admin, :wlincomeid);

        -- Ставим на приход другого склада
        select tw.taskwaresid
          from wm_task_wares tw
         where tw.taskid = :tid_automoving_plus
           and tw.waresid = :waresid
          into :twid_automoving_plus;

        if (:twid_automoving_plus is NULL) then
            insert into wm_task_wares(taskid, waresid, status, begintime, quantity)
            values (:tid_automoving_plus,:waresid, '2', current_timestamp, :amount)
            returning taskwaresid
            into :twid_automoving_plus;
        else
            update wm_task_wares tw
               set tw.quantity = coalesce(tw.quantity,0.000) + :amount,tw.status = '2'
             where tw.taskwaresid = :twid_automoving_plus;

        select coalesce(wh.returnzone,wh.incomezone)
          from wh_obj_info wh
         where wh.objid = :objid_whreject
          into :zoneid_whreject;

        update or insert into wareslot (waresid, productdate, status, objid, zoneid)
        values(:waresid, :productdate, '1', :objid_whreject, :zoneid_whreject)
        matching (waresid, productdate, objid, zoneid)
        returning wlotid
        into :wlotid_whreject;

        update or insert into wareslotincomes(wlotid, docid)
        values(:wlotid_whreject,NULL)
        matching(wlotid, docid)
        returning id
        into :wlincomeid_whreject;

        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:twid_automoving_plus, :wlotid_whreject, :palletid, :amount, '1', :wmsid_admin, :wlincomeid_whreject);

        update cargo cg
           set cg.amount = cg.amount + :amount,cg.docsum = NULL
         where cg.document = :docid and cg.waresid = :waresid;

        select t.docid
          from wm_task t
         where t.taskid = :tid_automoving_minus
          into :docid_automoving_minus;
        if (:docid_automoving_minus is NOT NULL) then
            update cargo cg
               set cg.amount = cg.amount + :amount,cg.docsum = NULL
             where cg.document = :docid_automoving_minus and cg.waresid = :waresid;
            
        select t.docid
          from wm_task t
         where t.taskid = :tid_automoving_plus
          into :docid_automoving_plus;
        if (:docid_automoving_plus is NOT NULL) then
            update cargo cg
               set cg.amount = cg.amount + :amount,cg.docsum = NULL
             where cg.document = :docid_automoving_plus and cg.waresid = :waresid;
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

            select pip.manid, pip.whid, pip.zoneid, pip.number
              from pallet_comeretprint pip
             where pip.barcode = :barcode
               and pip.enabled = '1'
              into :palmanid, :palwhid, :palzoneid, :palnumber;

            if (:palnumber is NULL) then
                exception exc_wh_palincomeprintnotfound;
            if (:usermanid <> :palmanid) then
                exception exc_wh_palincomeprinterrman;
            if (:objid_whreject <> :palwhid) then
                exception exc_wh_palincomeprinterrwh;

            if (:siteid is null) then
                exception exc_k_wrongsite 'К заданию не привязано МП!';

            insert into pallet(status, barcode, number, ptypeid, siteid, objid, zoneid)
            values ('1',:barcode,:palnumber,:paltypeid_comereturn,:siteid,:palwhid,:palzoneid)
            returning palletid,number
            into :palletid,:palnumber;

            exception exc_k_common :palnumber;

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

CREATE OR ALTER trigger pallet_ai for pallet
active after insert position 0
as
declare variable ptypecode type of r_code3;
begin
  select pt.code
    from pallet_type pt
   where pt.id = new.ptypeid
    into :ptypecode;

  if (:ptypecode = 'I') then -- Паллет прихода
    update pallet_incomeprint pip
       set pip.palletid = new.palletid, pip.enabled = '0'
     where pip.barcode = new.barcode and pip.enabled = '1' and pip.palletid is NULL;
  else if (:ptypecode = 'RC') then -- Паллет прихода возвратов от клиентов
    update pallet_comeretprint pip
       set pip.palletid = new.palletid, pip.enabled = '0'
     where pip.barcode = new.barcode and pip.enabled = '1' and pip.palletid is NULL;
  else if (:ptypecode = 'T') then -- Транзитный паллет
    update pallet_transitprint ptp
       set ptp.palletid = new.palletid, ptp.enabled = '0', ptp.palletstatus = new.status
     where ptp.barcode = new.barcode and ptp.enabled = '1' and ptp.palletid is NULL;
  else if (:ptypecode = 'FP') then -- Транзитный паллет
    update pallet_finishprint ptp
       set ptp.palletid = new.palletid, ptp.enabled = '0'
     where ptp.barcode = new.barcode and ptp.enabled = '1' and ptp.palletid is NULL;
    
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

            select pip.manid, pip.whid, pip.zoneid, pip.number
              from pallet_comeretprint pip
             where pip.barcode = :barcode
               and pip.enabled = '1'
              into :palmanid, :palwhid, :palzoneid, :palnumber;

            if (:palnumber is NULL) then
                exception exc_wh_palincomeprintnotfound;
            if (:usermanid <> :palmanid) then
                exception exc_wh_palincomeprinterrman;
            if (:objid_whreject <> :palwhid) then
                exception exc_wh_palincomeprinterrwh;

            if (:siteid is null) then
                exception exc_k_wrongsite 'К заданию не привязано МП!';

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

CREATE OR ALTER procedure WH_COMERETURN_ADD (
    TASKID type of R_ID,
    WUID type of R_ID,
    PRODUCTDATE type of R_DATE,
    AMOUNT type of R_DOUBLE,
    BARCODE type of R_BARCODE,
    WMSESSIONID type of R_ID,
    BEGINTIME type of R_DATETIME = null)
AS
declare variable palletid type of r_id;
declare variable wlotid type of r_id;
declare variable waresid type of r_id;
declare variable taskwaresid type of r_id;
declare variable factor type of r_double;
declare variable wlamount type of r_double;
declare variable toobj type of r_id;
declare variable fromobj type of r_id;
declare variable ttid type of r_id;
declare variable tmid type of r_id;
declare variable tstatus type of r_status;
declare variable paramValue varchar(1023);
declare variable zoneid r_id;
declare variable wlincomeid r_id;
declare variable docid r_id64;
declare variable objid_whreject r_id;
declare variable zoneid_whreject r_id;
declare variable wlotid_whreject r_id;
declare variable wlincomeid_whreject r_id;
declare variable tid_automoving_plus r_id;
declare variable tid_automoving_minus r_id;
declare variable pid_trash r_id;
declare variable twid_automoving_minus r_id;
declare variable twid_automoving_plus r_id;
declare variable wmsid_admin r_id;
declare variable docid_automoving_minus r_id64;
declare variable docid_automoving_plus r_id64;
begin
    if (:barcode is NULL) then exception exc_wh_emptybarcode;
    if (:amount is NULL or :amount < 0.0001) then exception exc_wh_emptyamount;
    if (:wuid is NULL) then exception exc_wh_emptywaresunit;
    if (:productdate is NULL or (:productdate>current_date) ) then exception exc_wh_wrongproductdate;

    select t.tasktypeid,t.taskmethodid,d.toobj,d.fromobj,t.status,d.docid
      from wm_task t
           left join document d on d.docid = t.docid
     where t.taskid = :taskid
      into :ttid,:tmid,:toobj,:fromobj,:tstatus,:docid;

    if (:tstatus='2') then exception exc_k_wrongtaskstat;

    select palletid
      from wh_comereturn_chkbarcode(:taskid,:barcode,:wmsessionid)
      into :palletid;

    select wu.factor,wu.waresid
      from waresunit wu
     where wu.waresunitid = :wuid
      into :factor,:waresid;

    amount = :factor * :amount;

    select tw.taskwaresid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.waresid = :waresid
      into :taskwaresid;

    if (:taskwaresid is NULL) then
    begin
        -- Можно убрать исключение и будет работать схема с проверкой
        select paramValue
          from k_sitezonemethod_paramvalue(:ttid,:tmid,:toobj,:fromobj,'ADDTASKWARES')
          into :paramValue;

        if (:paramvalue is NULL or :paramvalue<>'1') then
            exception exc_ur_common 'Товар не найден в задании!';
        else
            insert into wm_task_wares(taskid, waresid, successscan, status, begintime, endtime)
            values (:taskid, :waresid, 0.000, '0', :begintime, NULL)
            returning taskwaresid
            into :taskwaresid;
    end

    select coalesce(oi.returnzone,oi.incomezone)
      from wh_obj_info oi
     where oi.objid = :toobj
      into :zoneid;

    update or insert into wareslot (waresid, productdate, status, objid, zoneid)
    values(:waresid, :productdate, '1', :toobj, :zoneid)
    matching (waresid, productdate, objid, zoneid)
    returning wlotid
    into :wlotid;

    update or insert into wareslotincomes(wlotid, docid)
    values(:wlotid,:docid)
    matching(wlotid, docid)
    returning id
    into :wlincomeid;

    execute procedure WH_CORE_PALLETGETOBJ(:palletid)
     returning_values :objid_whreject;
    if (:objid_whreject is NULL) then exception exc_wh_whreject_notfound;

    if (:toobj = :objid_whreject) then
    begin
        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:taskwaresid, :wlotid, :palletid, :amount, '1', :wmsessionid, :wlincomeid);
    
        select sum(tl.quantity)
          from wm_task_lot tl
         where tl.taskwaresid = :taskwaresid
          into :wlamount;
    
        update wm_task_wares tw
           set tw.quantity = :wlamount,tw.wm_sessionid=:wmsessionid,tw.endtime=current_timestamp
         where tw.taskwaresid = :taskwaresid;
    
        update cargo cg
           set cg.amount = :wlamount,cg.docsum = NULL
         where cg.document = :docid and cg.waresid = :waresid and abs(cg.amount - :wlamount)>0.00001;
    end
    else
    begin
        select tid_plus,tid_minus
          from wh_automoving_gettaskes(:taskid,'COMERETURN','PM')
          into :tid_automoving_plus,:tid_automoving_minus;

        select k.pid
          from k_wh_get_trash(:toobj) k
          into :pid_trash;

        -- Ставим на недостачу
        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:taskwaresid, :wlotid, :pid_trash, :amount, '1', :wmsessionid, :wlincomeid);

        update wm_task_wares tw
           set tw.quantity = coalesce(tw.quantity,0.000)+:amount,tw.wm_sessionid=:wmsessionid,tw.endtime=current_timestamp
         where tw.taskwaresid = :taskwaresid;

        -- Находим данные админа для автоматической переброски
        execute procedure WH_ADMIN_GETWMSESSIONID returning_values :wmsid_admin;
        -- Сразу же с нее списываем
        select tw.taskwaresid
          from wm_task_wares tw
         where tw.taskid = :tid_automoving_minus
           and tw.waresid = :waresid
          into :twid_automoving_minus;
        if (:twid_automoving_minus is NULL) then
            insert into wm_task_wares(taskid, waresid, status, begintime, quantity)
            values (:tid_automoving_minus,:waresid, '2', current_timestamp, :amount)
            returning taskwaresid
            into :twid_automoving_minus;
        else
            update wm_task_wares tw
               set tw.quantity = coalesce(tw.quantity,0.000) + :amount,tw.status = '2'
             where tw.taskwaresid = :twid_automoving_minus;

        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:twid_automoving_minus, :wlotid, :pid_trash, -:amount, '1', :wmsid_admin, :wlincomeid);

        -- Ставим на приход другого склада
        select tw.taskwaresid
          from wm_task_wares tw
         where tw.taskid = :tid_automoving_plus
           and tw.waresid = :waresid
          into :twid_automoving_plus;

        if (:twid_automoving_plus is NULL) then
            insert into wm_task_wares(taskid, waresid, status, begintime, quantity)
            values (:tid_automoving_plus,:waresid, '2', current_timestamp, :amount)
            returning taskwaresid
            into :twid_automoving_plus;
        else
            update wm_task_wares tw
               set tw.quantity = coalesce(tw.quantity,0.000) + :amount,tw.status = '2'
             where tw.taskwaresid = :twid_automoving_plus;

        select coalesce(wh.returnzone,wh.incomezone)
          from wh_obj_info wh
         where wh.objid = :objid_whreject
          into :zoneid_whreject;

        update or insert into wareslot (waresid, productdate, status, objid, zoneid)
        values(:waresid, :productdate, '1', :objid_whreject, :zoneid_whreject)
        matching (waresid, productdate, objid, zoneid)
        returning wlotid
        into :wlotid_whreject;

        update or insert into wareslotincomes(wlotid, docid)
        values(:wlotid_whreject,NULL)
        matching(wlotid, docid)
        returning id
        into :wlincomeid_whreject;

        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:twid_automoving_plus, :wlotid_whreject, :palletid, :amount, '1', :wmsid_admin, :wlincomeid_whreject);

        update cargo cg
           set cg.amount = cg.amount + :amount,cg.docsum = NULL
         where cg.document = :docid and cg.waresid = :waresid;

        select t.docid
          from wm_task t
         where t.taskid = :tid_automoving_minus
          into :docid_automoving_minus;
        if (:docid_automoving_minus is NOT NULL) then
            update cargo cg
               set cg.amount = cg.amount + :amount,cg.docsum = NULL
             where cg.document = :docid_automoving_minus and cg.waresid = :waresid;
            
        select t.docid
          from wm_task t
         where t.taskid = :tid_automoving_plus
          into :docid_automoving_plus;
        if (:docid_automoving_plus is NOT NULL) then
            update cargo cg
               set cg.amount = cg.amount + :amount,cg.docsum = NULL
             where cg.document = :docid_automoving_plus and cg.waresid = :waresid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_COMERETURN_SITESET (
    TASKID R_ID,
    SITEID R_ID)
AS
declare variable manid type of r_id;
begin
    if (not exists(select *
                     from site s
                          left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                    where s.siteid = :siteid
                      and sp.code in ('E','GATE','B'))) then
        exception exc_wh_wrongsitetype;

    if (not exists(select *
                     from site_options sos
                          left join siteoption so on so.id = sos.optionid
                    where sos.siteid = :siteid
                      and so.code = 'COMERETURN')) then
        exception exc_wh_wrongsite;

    select wms.objid
      from wm_task t
           left join wm_session wms on wms.sessionid = t.wm_sessionid
     where t.taskid = :taskid
      into :manid;

    execute procedure wh_chk_siteforman(:siteid,:manid);

    update wm_task t
       set t.siteid = :siteid
     where t.taskid = :taskid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_BUYRETURN_STATUSCHG (
    DOCID type of R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable TASKID type of R_ID;
declare variable ttid_comereturn type of R_ID;
declare variable TTINITST type of R_STATUS;
declare variable WARESID type of R_ID;
declare variable AMOUNT type of R_DOUBLE;
declare variable DOCSUM type of R_DOUBLE;
declare variable FROMOBJ type of R_ID;
declare variable OBJID type of R_ID;
declare variable doctid type of R_ID;
declare variable docdate type of R_DATE;
declare variable taskmethodid type of R_ID;
declare variable siteid type of R_ID;
begin
    select d.fromobj,d.toobj,d.doctype,d.docdate
      from document d
     where d.docid = :docid
      into :fromobj,:objid,:doctid,:docdate;

    if (:newstat='c') then
    begin
        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        select coalesce(tt.initstatus,'0') from wm_tasktype tt where tt.tasktypeid = :ttid_comereturn into :ttinitst;

        if (exists(select *
                     from wh_obj_info wh
                    where wh.objid = :objid
                      and wh.datestart >= :docdate
                      and wh.fromobjincome = :fromobj )) then
        begin
            select tm.methodid
              from wm_taskmethod tm
             where tm.tasktypeid = :ttid_comereturn
               and tm.algorithm = 'F'
              into :taskmethodid;

            if (:taskmethodid is NULL) then exception exc_k_wrongtasktype;

            select first(1) t.taskid
              from wm_task t
             where t.docid = :docid
               and t.tasktypeid = :ttid_comereturn
              into :taskid;

            if (:taskid is NULL) then
            begin
                siteid = NULL;
                select first(1) s.siteid
                  from sitespecies sp
                       left join site s on s.sitespeciesid = sp.sitespeciesid
                 where sp.code = 'E'
                  into :siteid;

                INSERT INTO wm_task(tasktypeid,status,docid,wm_sessionid,taskmethodid,siteid)
                VALUES(:ttid_comereturn,:ttinitst,:docid,null,:taskmethodid,:siteid)
                returning taskid
                into :taskid;
            end
            else
            begin
                update wm_task t
                   set t.taskmethodid = :taskmethodid,
                       t.wm_sessionid = NULL,
                       t.status = :ttinitst
                  where t.taskid = :taskid;
            end
        end
        else
        begin
            select first(1) szm.methodid
              from wm_taskmethod tm
                   left join sitezone_method szm
                        left join sitezone sz on sz.zoneid = szm.zoneid
                     on szm.methodid = tm.methodid
             where tm.tasktypeid = :ttid_comereturn
               and sz.objid = :objid
              into :taskmethodid;

            UPDATE or INSERT INTO wm_task(tasktypeid,status,docid,wm_sessionid,taskmethodid)
            VALUES(:ttid_comereturn,:ttinitst,:docid,null,:taskmethodid)
            matching (tasktypeid,docid)
            returning taskid
            into :taskid;
        end

        -- Если повышение статуса
        if (exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.upcodes containing :newstat )) then
        begin
            for
                select cg.waresid,cg.amount,cg.docsum
                  from cargo cg
                 where cg.document = :docid
                   and cg.amount > 0.00001
                  into :waresid,:amount,:docsum
            do
                update or insert into wm_task_wares(taskid, waresid, successscan, summa, status, endtime)
                values (:taskid, :waresid, :amount, :docsum, '0', NULL)
                matching (taskid, waresid);
        end
        -- понижение статуса
        if (exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.downcodes containing :newstat))
        then
        begin
          update wm_task_wares tw
             set tw.status = '0'
           where tw.taskid = :taskid
                 and abs(coalesce(tw.successscan,0.0000)-coalesce(tw.quantity,0.00000)) > 0.000001;
        end

        execute procedure WH_CORE_SETDOCBYTASK(:docid,:ttid_comereturn);
    end
    else if (:newstat='w') then
    begin
        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        execute procedure WH_CORE_SETDOCBYTASK(:docid,:ttid_comereturn);
        execute procedure WH_COMERETURN_DOCSRENEW(:docid);

        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        if (not exists(select *
                         from wm_task t
                              left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                        where t.docid = :docid
                          and t.tasktypeid = :ttid_comereturn
                          and coalesce(tm.algorithm,'')='F' )) then
            execute procedure RBS_Q_CREATETASKEXPORT('Изменение статуса: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
             returning_values :taskid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_COMERETURN_ADD (
    TASKID type of R_ID,
    WUID type of R_ID,
    PRODUCTDATE type of R_DATE,
    AMOUNT type of R_DOUBLE,
    BARCODE type of R_BARCODE,
    WMSESSIONID type of R_ID,
    BEGINTIME type of R_DATETIME = null)
AS
declare variable palletid type of r_id;
declare variable wlotid type of r_id;
declare variable waresid type of r_id;
declare variable taskwaresid type of r_id;
declare variable factor type of r_double;
declare variable wlamount type of r_double;
declare variable toobj type of r_id;
declare variable fromobj type of r_id;
declare variable ttid type of r_id;
declare variable tmid type of r_id;
declare variable tstatus type of r_status;
declare variable paramValue varchar(1023);
declare variable zoneid r_id;
declare variable wlincomeid r_id;
declare variable docid r_id64;
declare variable objid_whreject r_id;
declare variable zoneid_whreject r_id;
declare variable wlotid_whreject r_id;
declare variable wlincomeid_whreject r_id;
declare variable tid_automoving_plus r_id;
declare variable tid_automoving_minus r_id;
declare variable pid_trash r_id;
declare variable twid_automoving_minus r_id;
declare variable twid_automoving_plus r_id;
declare variable wmsid_admin r_id;
declare variable docid_automoving_minus r_id64;
declare variable docid_automoving_plus r_id64;
begin
    if (:barcode is NULL) then exception exc_wh_emptybarcode;
    if (:amount is NULL or :amount < 0.0001) then exception exc_wh_emptyamount;
    if (:wuid is NULL) then exception exc_wh_emptywaresunit;
    if (:productdate is NULL or (:productdate>current_date) ) then exception exc_wh_wrongproductdate;

    select t.tasktypeid,t.taskmethodid,d.toobj,d.fromobj,t.status,d.docid
      from wm_task t
           left join document d on d.docid = t.docid
     where t.taskid = :taskid
      into :ttid,:tmid,:toobj,:fromobj,:tstatus,:docid;

    if (:tstatus='2') then exception exc_k_wrongtaskstat;

    select palletid
      from wh_comereturn_chkbarcode(:taskid,:barcode,:wmsessionid)
      into :palletid;

    select wu.factor,wu.waresid
      from waresunit wu
     where wu.waresunitid = :wuid
      into :factor,:waresid;

    amount = :factor * :amount;

    select tw.taskwaresid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.waresid = :waresid
      into :taskwaresid;

    if (:taskwaresid is NULL) then
    begin
        -- Можно убрать исключение и будет работать схема с проверкой
        select paramValue
          from k_sitezonemethod_paramvalue(:ttid,:tmid,:toobj,:fromobj,'ADDTASKWARES')
          into :paramValue;

        if (:paramvalue is NULL or :paramvalue<>'1') then
            exception exc_ur_common 'Товар не найден в задании!';
        else
            insert into wm_task_wares(taskid, waresid, successscan, status, begintime, endtime)
            values (:taskid, :waresid, 0.000, '0', :begintime, NULL)
            returning taskwaresid
            into :taskwaresid;
    end

    select coalesce(oi.returnzone,oi.incomezone)
      from wh_obj_info oi
     where oi.objid = :toobj
      into :zoneid;

    update or insert into wareslot (waresid, productdate, status, objid, zoneid)
    values(:waresid, :productdate, '1', :toobj, :zoneid)
    matching (waresid, productdate, objid, zoneid)
    returning wlotid
    into :wlotid;

    update or insert into wareslotincomes(wlotid, docid, status)
    values(:wlotid, :docid, '0')
    matching(wlotid, docid)
    returning id
    into :wlincomeid;

    execute procedure WH_CORE_PALLETGETOBJ(:palletid)
     returning_values :objid_whreject;
    if (:objid_whreject is NULL) then exception exc_wh_whreject_notfound;

    if (:toobj = :objid_whreject) then
    begin
        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:taskwaresid, :wlotid, :palletid, :amount, '1', :wmsessionid, :wlincomeid);
    
        select sum(tl.quantity)
          from wm_task_lot tl
         where tl.taskwaresid = :taskwaresid
          into :wlamount;
    
        update wm_task_wares tw
           set tw.quantity = :wlamount,tw.wm_sessionid=:wmsessionid,tw.endtime=current_timestamp
         where tw.taskwaresid = :taskwaresid;
    
        update cargo cg
           set cg.amount = :wlamount,cg.docsum = NULL
         where cg.document = :docid and cg.waresid = :waresid and abs(cg.amount - :wlamount)>0.00001;
    end
    else
    begin
        select tid_plus,tid_minus
          from wh_automoving_gettaskes(:taskid,'COMERETURN','PM')
          into :tid_automoving_plus,:tid_automoving_minus;

        select k.pid
          from k_wh_get_trash(:toobj) k
          into :pid_trash;

        -- Ставим на недостачу
        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:taskwaresid, :wlotid, :pid_trash, :amount, '1', :wmsessionid, :wlincomeid);

        update wm_task_wares tw
           set tw.quantity = coalesce(tw.quantity,0.000)+:amount,tw.wm_sessionid=:wmsessionid,tw.endtime=current_timestamp
         where tw.taskwaresid = :taskwaresid;

        -- Находим данные админа для автоматической переброски
        execute procedure WH_ADMIN_GETWMSESSIONID returning_values :wmsid_admin;
        -- Сразу же с нее списываем
        select tw.taskwaresid
          from wm_task_wares tw
         where tw.taskid = :tid_automoving_minus
           and tw.waresid = :waresid
          into :twid_automoving_minus;
        if (:twid_automoving_minus is NULL) then
            insert into wm_task_wares(taskid, waresid, status, begintime, quantity)
            values (:tid_automoving_minus,:waresid, '2', current_timestamp, :amount)
            returning taskwaresid
            into :twid_automoving_minus;
        else
            update wm_task_wares tw
               set tw.quantity = coalesce(tw.quantity,0.000) + :amount,tw.status = '2'
             where tw.taskwaresid = :twid_automoving_minus;

        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:twid_automoving_minus, :wlotid, :pid_trash, -:amount, '1', :wmsid_admin, :wlincomeid);

        -- Ставим на приход другого склада
        select tw.taskwaresid
          from wm_task_wares tw
         where tw.taskid = :tid_automoving_plus
           and tw.waresid = :waresid
          into :twid_automoving_plus;

        if (:twid_automoving_plus is NULL) then
            insert into wm_task_wares(taskid, waresid, status, begintime, quantity)
            values (:tid_automoving_plus,:waresid, '2', current_timestamp, :amount)
            returning taskwaresid
            into :twid_automoving_plus;
        else
            update wm_task_wares tw
               set tw.quantity = coalesce(tw.quantity,0.000) + :amount,tw.status = '2'
             where tw.taskwaresid = :twid_automoving_plus;

        select coalesce(wh.returnzone,wh.incomezone)
          from wh_obj_info wh
         where wh.objid = :objid_whreject
          into :zoneid_whreject;

        update or insert into wareslot (waresid, productdate, status, objid, zoneid)
        values(:waresid, :productdate, '1', :objid_whreject, :zoneid_whreject)
        matching (waresid, productdate, objid, zoneid)
        returning wlotid
        into :wlotid_whreject;

        update or insert into wareslotincomes(wlotid, docid)
        values(:wlotid_whreject,NULL)
        matching(wlotid, docid)
        returning id
        into :wlincomeid_whreject;

        insert into wm_task_lot(taskwaresid, wlotid, palletid, quantity, chgwli, wm_sessionid, wlincomeid)
        values(:twid_automoving_plus, :wlotid_whreject, :palletid, :amount, '1', :wmsid_admin, :wlincomeid_whreject);

        update cargo cg
           set cg.amount = cg.amount + :amount,cg.docsum = NULL
         where cg.document = :docid and cg.waresid = :waresid;

        select t.docid
          from wm_task t
         where t.taskid = :tid_automoving_minus
          into :docid_automoving_minus;
        if (:docid_automoving_minus is NOT NULL) then
            update cargo cg
               set cg.amount = cg.amount + :amount,cg.docsum = NULL
             where cg.document = :docid_automoving_minus and cg.waresid = :waresid;
            
        select t.docid
          from wm_task t
         where t.taskid = :tid_automoving_plus
          into :docid_automoving_plus;
        if (:docid_automoving_plus is NOT NULL) then
            update cargo cg
               set cg.amount = cg.amount + :amount,cg.docsum = NULL
             where cg.document = :docid_automoving_plus and cg.waresid = :waresid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_BUYRETURN_STATUSCHG (
    DOCID type of R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable TASKID type of R_ID;
declare variable ttid_comereturn type of R_ID;
declare variable TTINITST type of R_STATUS;
declare variable WARESID type of R_ID;
declare variable AMOUNT type of R_DOUBLE;
declare variable DOCSUM type of R_DOUBLE;
declare variable FROMOBJ type of R_ID;
declare variable OBJID type of R_ID;
declare variable doctid type of R_ID;
declare variable docdate type of R_DATE;
declare variable taskmethodid type of R_ID;
declare variable siteid type of R_ID;
begin
    select d.fromobj,d.toobj,d.doctype,d.docdate
      from document d
     where d.docid = :docid
      into :fromobj,:objid,:doctid,:docdate;

    if (:newstat='c') then
    begin
        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        select coalesce(tt.initstatus,'0') from wm_tasktype tt where tt.tasktypeid = :ttid_comereturn into :ttinitst;

        if (exists(select *
                     from wh_obj_info wh
                    where wh.objid = :objid
                      and wh.datestart >= :docdate
                      and wh.fromobjincome = :fromobj )) then
        begin
            select tm.methodid
              from wm_taskmethod tm
             where tm.tasktypeid = :ttid_comereturn
               and tm.algorithm = 'F'
              into :taskmethodid;

            if (:taskmethodid is NULL) then exception exc_k_wrongtasktype;

            select first(1) t.taskid
              from wm_task t
             where t.docid = :docid
               and t.tasktypeid = :ttid_comereturn
              into :taskid;

            if (:taskid is NULL) then
            begin
                siteid = NULL;
                select first(1) s.siteid
                  from sitespecies sp
                       left join site s on s.sitespeciesid = sp.sitespeciesid
                 where sp.code = 'E'
                  into :siteid;

                INSERT INTO wm_task(tasktypeid,status,docid,wm_sessionid,taskmethodid,siteid)
                VALUES(:ttid_comereturn,:ttinitst,:docid,null,:taskmethodid,:siteid)
                returning taskid
                into :taskid;
            end
            else
            begin
                update wm_task t
                   set t.taskmethodid = :taskmethodid,
                       t.wm_sessionid = NULL,
                       t.status = :ttinitst
                  where t.taskid = :taskid;
            end
        end
        else
        begin
            select first(1) szm.methodid
              from wm_taskmethod tm
                   left join sitezone_method szm
                        left join sitezone sz on sz.zoneid = szm.zoneid
                     on szm.methodid = tm.methodid
             where tm.tasktypeid = :ttid_comereturn
               and sz.objid = :objid
              into :taskmethodid;

            UPDATE or INSERT INTO wm_task(tasktypeid,status,docid,wm_sessionid,taskmethodid)
            VALUES(:ttid_comereturn,:ttinitst,:docid,null,:taskmethodid)
            matching (tasktypeid,docid)
            returning taskid
            into :taskid;
        end

        -- Если повышение статуса
        if (exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.upcodes containing :newstat )) then
        begin
            for
                select cg.waresid,cg.amount,cg.docsum
                  from cargo cg
                 where cg.document = :docid
                   and cg.amount > 0.00001
                  into :waresid,:amount,:docsum
            do
                update or insert into wm_task_wares(taskid, waresid, successscan, summa, status, endtime)
                values (:taskid, :waresid, :amount, :docsum, '0', NULL)
                matching (taskid, waresid);
        end
        -- понижение статуса
        if (exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.downcodes containing :newstat))
        then
        begin
          update wm_task_wares tw
             set tw.status = '0'
           where tw.taskid = :taskid
                 and abs(coalesce(tw.successscan,0.0000)-coalesce(tw.quantity,0.00000)) > 0.000001;
        end

        execute procedure WH_CORE_SETDOCBYTASK(:docid,:ttid_comereturn);
    end
    else if (:newstat='w') then
    begin
        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        execute procedure WH_CORE_SETDOCBYTASK(:docid,:ttid_comereturn);
        execute procedure WH_COMERETURN_DOCSRENEW(:docid);

        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        if (not exists(select *
                         from wm_task t
                              left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                        where t.docid = :docid
                          and t.tasktypeid = :ttid_comereturn
                          and coalesce(tm.algorithm,'')='F' )) then
            execute procedure RBS_Q_CREATETASKEXPORT('Изменение статуса: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
             returning_values :taskid;
    end
    else if (:newstat = 'e') then
    begin
        update wareslotincomes wlin
           set wlin.status = '1'
         where wlin.docid = :docid and wlin.status = '0';
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_COMERETURN_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable docstat type of column document.status;
begin
    select d.status
      from document d
     where d.docid = :docid
      into :docstat;

    if (:docstat = 'w') then
    begin
        execute procedure WH_IMP_CARGO_CHK(:docid);

        update document d
           set d.status = 'e', d.number = (select id.number from imp_document id where id.docid = :docid)
         where d.docid = :docid;

        delete from imp_document id
         where id.docid = :docid;
    end
    else
    begin
        exception exc_wh_wrongdocstat;
    end
end^

SET TERM ; ^

