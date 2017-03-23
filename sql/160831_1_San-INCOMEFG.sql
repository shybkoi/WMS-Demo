

SET TERM ^ ;

CREATE OR ALTER procedure WH_FG_PRINTPALLET (
    UID type of R_ID,
    WARESID type of R_ID,
    PRODUCERID type of R_ID,
    PRODLINEID type of R_ID,
    CNT smallint,
    PRINTERID type of R_ID,
    PRDATE type of R_DATE,
    PFID type of R_ID)
AS
 declare variable quetaskid   type of r_id;
 declare variable manid       type of r_id;
 declare variable rule        varchar(60);
 declare variable userfio     varchar(255);
 declare variable params      varchar(8192);
 declare variable i           smallint;
 declare variable tasktypeid  r_id;
 declare variable printername type of r_name;
begin

  if (:cnt <= 0) then
    exception exc_ur_common 'Количество должно быть больше 0';

  if (not exists(select *
                   from WH_WARES_GETPALLETUNIT(:waresid) pu
                  where pu.W_PWUID is NOT NULL
                    and pu.W_PUFACTOR > 0.0000001 )) then
    exception exc_ur_common 'У товара не задана кратность поддона!';

  select quetaskid
    from wm_config
    into :quetaskid;
  if (:quetaskid is null) then
    exception exc_ur_common 'Не установлена ID очереди заданий!';

  select tt.tasktypeid
    from wm_tasktype tt
   where tt.code = 'INCOMEFG'
    into :tasktypeid;
  execute procedure wm_getparamvalue(:tasktypeid, null, null, 'REPORTS')
      returning_values rule;
  select name
    from r_report
   where reportid = :rule
    into rule;

  if (:rule is null) then
    exception exc_ur_common 'Не найден тип отчета!';

  /*select wms.objid
    from wm_session wms
   where wms.sessionid = :wmsesid  */
  select u.id_man
    from k_users u
   where u.id_user = :uid
    into :manid;
  if (:manid is null) then
    exception exc_ur_common 'Не установлен пользователь!';

  /*select p.printerid
    from wm_printers p
   where p.printerid = :printerid
    into :printerid;
  if (:printerid is null) then
    exception exc_ur_common 'Принтер не найден!';   */
  select name
    from wm_printers
   where printerid = :printerid
    into :printername;
  if (printername is null) then
    exception exc_ur_common 'Не найден принтер с таким штрих-кодом.';

  select fp.objid
    from fg_producer fp
   where fp.objid = :producerid
    into :producerid;
  if (:producerid is null) then
    exception exc_ur_common 'Неверный объект!';


  params = '<params><ProdLineID value="' || cast(:prodlineid as varchar(10)) || '"/>
            <WaresID value="' || cast(:waresid as varchar(10)) || '"/>
            <ManID value="' || cast(:manid as varchar(10)) || '"/>
            <ProducerID value="' || cast(:producerid as varchar(10)) || '"/>
            <PalletID value="0"/>
            <PrDate value="' || iif(:prdate is Not Null, datetostr(:prdate, '%d.%m.%Y'), 'None') || '"/>
            <PFID value="' || iif(:pfid is Not Null, cast(:pfid as varchar(10)), 'None') || '"/>
            <printer value="'||:PrinterName||'"/>
            <PrintAfterDone value="1"/></params>';

  select fullname
    from getobjectname(:manid, '03')
    into :userfio;

  i = 0;
  while (:i < :cnt) do
  begin
    execute procedure wm_createqueuetask(:quetaskid, :rule, :userfio, :params)
        returning_values :tasktypeid;
    i = :i + 1;
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_INCOME_STATUSCHG (
    DOCID type of column DOCUMENT.docid,
    OLDSTAT type of column R_STATUS.code,
    NEWSTAT type of column R_STATUS.code)
AS
declare variable TASKID type of column WM_TASK.taskid;
declare variable TASKTYPEID type of column WM_TASKTYPE.tasktypeid;
declare variable TASKMETHODID type of column wm_taskmethod.methodid;
declare variable TTINITST type of column R_STATUS.code;
declare variable DOCDATE type of column DOCUMENT.docdate;
declare variable FROMOBJ type of column OBJECT.objid;
declare variable SITEID type of column SITE.siteid;
declare variable OBJID type of column OBJECT.objid;
declare variable oifromobjincome type of column OBJECT.objid;
declare variable oidatestart type of column wh_obj_info.datestart;
declare variable dtid type of column DOCTYPE.doctid;
begin
    if (:newstat = 'c') then
    begin
        SELECT ttid,ttinitst
          FROM k_tasktype_by_code('INCOMEFG','1')
          into :tasktypeid,:ttinitst;

        select d.fromobj, d.toobj, d.realdocdate, d.doctype
          from document d
         where d.docid = :docid
          into :fromobj, :objid, :docdate, :dtid;

        select wh.datestart, coalesce(wh.fromobjincome,0)
          from wh_obj_info wh
         where wh.objid = :objid
          into :oidatestart, :oifromobjincome;

        if (:oidatestart >= :docdate and :oifromobjincome = coalesce(:fromobj,0)) then
        begin
            if (exists(select *
                         from document d
                        where d.toobj = :objid
                          and d.docdate <= :oidatestart
                          and d.status = 'c'
                          and d.doctype = :dtid
                          and coalesce(d.fromobj,0) = :oifromobjincome )) then
                    exception exc_wh_wrongdocstat 'Уже есть документ первого прихода!';

            select tm.methodid
              from wm_taskmethod tm
             where tm.tasktypeid = :tasktypeid
               and tm.algorithm = 'F'
              into :taskmethodid;

            if (:taskmethodid is NULL) then
                exception exc_k_wrongtasktype 'Не найден метод с кодом F у типа задания приемка от поставщика!';

            select first(1) t.taskid
              from wm_task t
             where t.docid = :docid
               and t.tasktypeid = :tasktypeid
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
                VALUES(:tasktypeid,:ttinitst,:docid,null,:taskmethodid,:siteid)
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
    end
    else if (:newstat = 'w') then
    begin
         taskid = NULL;
         for
            select t.taskid
              from wm_task t
                   left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                   left join wm_taskmethod tm on tm.methodid = t.taskmethodid
             where t.docid = :docid
               and tt.code = 'INCOMEFG'
               and tm.algorithm = 'F'
              into :taskid
         do
            update wm_task t
               set t.status = '2',t.endtime = current_timestamp
             where t.taskid = :taskid and t.status <> '2';

        execute procedure wh_core_setdocbytasklot(:docid);
/*        execute procedure RBS_Q_CREATETASKEXPORT('K_UV_INCOMEFG_STATUSCHG: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
         returning_values :docid;*/

    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_U3S_BUYRETURN_STATUSCHG (
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
            execute procedure RBS_Q_CREATETASKEXPORT('K_VT_BUYRETURN_STATUSCHG: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
             returning_values :taskid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_COMERETURN_CLIENTJOINEDTASK (
    CLIENTID type of column OBJECT.OBJID,
    SESSIONID type of column WM_SESSION.SESSIONID)
returns (
    TASKID type of column WM_TASK.TASKID,
    SITEID type of column SITE.SITEID,
    DOCID type of column DOCUMENT.DOCID,
    DOCNUM type of column DOCUMENT.NUMBER,
    DOCDATE type of R_DATE)
AS
declare variable seszoneobjid type of column object.objid;
declare variable ttid_comereturn type of column wm_tasktype.tasktypeid;
begin
    select objid
      from k_wh_sessionzoneobj(:sessionid)
      into :seszoneobjid;

    execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;

    for
        select t.taskid as taskid, t.siteid,
               d.docid as docid, d.number, d.docdate
          from wm_task t
               left join document d on d.docid = t.docid
         where t.tasktypeid = :ttid_comereturn
           and t.status = '1'
           and t.wm_sessionid = :sessionid
           and d.status = 'c'
           and d.toobj = :seszoneobjid
           and d.fromobj = :clientid
         order by t.siteid asc nulls first, d.docdate asc, d.number asc
          into :taskid, :siteid, :docid, :docnum, :docdate
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_COMERETURN_CLIENTSITESET (
    CLIENTID type of column OBJECT.OBJID,
    SESSIONID type of column WM_SESSION.SESSIONID,
    SITEID type of column SITE.SITEID)
AS
declare variable taskid type of column WM_TASK.taskid;
begin
    for
        select w.taskid
          from WH_COMERETURN_CLIENTJOINEDTASK(:clientid, :sessionid) w
         where w.siteid is NULL
          into :taskid
    do
        update wm_task t
           set t.siteid = :siteid
         where t.taskid = :taskid;
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
 /*$$IBE$$ declare variable i type of R_NUMBER;
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
declare variable spCode type of column sitespecies.code; $$IBE$$*/ 
begin /*$$IBE$$ 
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
 $$IBE$$*/ EXIT;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYPALLET (
    PBARCODE type of R_BARCODE,
    QUANTITY type of R_DOUBLE,
    IDUSER type of R_ID,
    DTBEG type of R_DATETIME = current_timestamp,
    FEATUREID type of R_ID = null)
AS
 /*$$IBE$$ declare variable productdate r_date;
declare variable waresid r_id;
declare variable qplan r_double;
declare variable producerid r_id;
declare variable manid r_id;
declare variable mansiteid r_id;
declare variable zoneid r_id;
declare variable whid r_id;
declare variable ttid_income r_id;
declare variable taskid r_id;
declare variable wmsid r_id;
declare variable taskwaresid r_id;
declare variable pnumber r_barcode;
declare variable ptypeid_finishgood r_id;
declare variable palletid r_id;
declare variable wlincomeid r_id;
declare variable wlotid r_id;
declare variable dtid_income r_id;
declare variable docid r_id64;
declare variable cargoid r_id; $$IBE$$*/ 
begin /*$$IBE$$ 
    if (:quantity is NULL) then
        exception exc_wh_wrongamount;

    select wh.zoneid, wh.whid, wh.manid
      from wh_user_infoshort(:iduser) wh
      into :zoneid, :whid, :manid;

    select pfp.productdate, pfp.waresid, pfp.quantity, pfp.producerid, pfp.number,
           coalesce(pfp.dtid_income, pl.dtid_income, p.dtid_income_print, p.dtid_income)
      from pallet_finishprint pfp
           left join fg_producer p on p.objid = pfp.producerid
           left join fg_prodlines pl on pl.id_prodline = pfp.prodlineid
     where pfp.barcode = :pbarcode and pfp.enabled = '1'
      into :productdate, :waresid, :qplan, :producerid, :pnumber, :dtid_income;

    execute procedure WH_INCOMEFG_BYPALLET_FUNDINCOME(:producerid, :whid, :waresid, :productdate, :quantity);
    select k.sid
      from k_get_user_wmsessionid(:manid, 'M') k
      into :wmsid;

    select m.siteid
      from wh_man_getsite(:manid) m
      into :mansiteid;

    execute procedure wh_ttid_incomefg
     returning_values :ttid_income;

    insert into wm_task(tasktypeid, zoneid, status, siteid)
    values(:ttid_income, :zoneid, '0', :mansiteid)
    returning taskid
    into :taskid;

    select wh.id
      from wh_paltypeid_finishgood wh
      into :ptypeid_finishgood;

    insert into pallet(ptypeid, barcode, number, siteid, zoneid, objid)
    values(:ptypeid_finishgood, :pbarcode, :pnumber, :mansiteid, :zoneid, :whid)
    returning palletid
    into :palletid;

    if (:featureid is NOT NULL) then
        execute procedure wh_pallet_feature_set(:palletid, :featureid, :manid, 'M');

    update wm_task t
       set t.wm_sessionid = :wmsid, t.begintime = :dtbeg, t.status = '1'
     where t.taskid = :taskid;

    insert into wm_task_pallet(taskid, palletid, status)
    values(:taskid, :palletid, '2');

    update or insert into wareslot(objid, zoneid, waresid, productdate, status)
    values(:whid, :zoneid, :waresid, :productdate, '1')
    matching(objid, zoneid, waresid, productdate)
    returning wlotid
    into :wlotid;

    select first(1) d.docid
      from document d
     where d.doctype = :dtid_income
       and d.fromobj = :producerid
       and d.toobj = :whid
       and d.status = 'c'
       and d.docdate = cast(:dtbeg as date)
      into :docid;

    if (:docid is NULL) then
    begin
        select k.docid
          from k_doccreate(:producerid, :whid, NULL, :dtid_income,
                           cast(:dtbeg as date), cast(:dtbeg as date),
                           NULL, NULL, null, NULL, NULL) k
          into :docid;

        update document d
           set d.status = 'c'
         where d.docid = :docid;
    end

    update or insert into wareslotincomes(docid, wlotid)
    values(:docid, :wlotid)
    matching(docid, wlotid)
    returning id
    into :wlincomeid;

    insert into wm_task_wares(taskid, waresid, status, wm_sessionid, successscan, quantity, begintime)
    values(:taskid, :waresid, '1', :wmsid, :qplan, :quantity, :dtbeg)
    returning taskwaresid
    into :taskwaresid;

    insert into wm_task_lot(palletid,  wlotid, taskwaresid, chgwli, wlincomeid, quantity)
    values(:palletid, :wlotid, :taskwaresid, '1', :wlincomeid, :quantity);

    update wm_task_wares tw
       set tw.status='2',tw.endtime = current_timestamp
     where tw.taskwaresid = :taskwaresid;

    update wm_task t
       set t.status = '2',t.docid = :docid
     where t.taskid = :taskid;

    execute procedure k_get_cargoid(:docid, :waresid)
      returning_values :cargoid;

    if (:cargoid is NULL) then
        insert into cargo(document, waresid, amount, price)
        values(:docid, :waresid, :quantity, 0.000);
    else
        update cargo cg
           set cg.amount = cg.amount + :quantity
         where cg.cargoid = :cargoid;

 $$IBE$$*/ EXIT;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYPALLET_FUNDINCOME (
    PRODUCERID type of column OBJECT.OBJID,
    WHID type of column OBJECT.OBJID,
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of R_DATE,
    QUANTITY type of R_QUANTITY)
RETURNS(
    DOCID type of column DOCUMENT.docid
)
AS
declare variable dtid_fundincome type of column doctype.doctid;
declare variable docstat type of column r_status.code;
declare variable cargoid type of column cargo.cargoid;
declare variable singularityid type of column waresgroup_singularity.id;
declare variable singularityname type of column waresgroup_singularity.name = NULL;
begin
    execute procedure wh_dtid_fundincome('0')
     returning_values :dtid_fundincome;

    if (:dtid_fundincome is NOT NULL) then
    begin
        with recursive wgf as(
            select wg.waresgrid, wg.higher, wg.singularityid
              from gwares g
                   left join waresgroup wg
                     on wg.waresgrid = g.waresgroup
             where g.waresid = :waresid
             union all
            select wg.waresgrid, wg.higher, wg.singularityid
              from wgf
                   join waresgroup wg on wg.waresgrid = wgf.higher
             where wg.singularityid is NULL
        )
        select first(1) wgf.singularityid
          from wgf
         where wgf.singularityid is NOT NULL
          into :singularityid;

        if (:singularityid is NULL) then
        begin
            select first(1) d.docid, d.status
              from document d
                   left join document_wgsingularity ds on ds.docid = d.docid
             where d.doctype = :dtid_fundincome
               and d.fromobj = :producerid
               and d.toobj = :whid
               and d.realdocdate = :productdate
               and ds.singularityid is NULL
              into :docid, :docstat;
        end
        else
        begin
            select first(1) d.docid, d.status
              from document d
                   left join document_wgsingularity ds on ds.docid = d.docid
             where d.doctype = :dtid_fundincome
               and d.fromobj = :producerid
               and d.toobj = :whid
               and d.realdocdate = :productdate
               and ds.singularityid = :singularityid
              into :docid, :docstat;
        end

        if (:docid is NULL) then
        begin                               
            if (:singularityid is NOT NULL) then
                select wsg.name
                  from waresgroup_singularity wsg
                 where wsg.id = :singularityid
                  into :singularityname;

            select k.docid
              from k_doccreate(:producerid, :whid, NULL, :dtid_fundincome,
                               current_date, :productdate,
                               NULL, NULL, :singularityname, NULL, NULL) k
              into :docid;

            if (:singularityid is NOT NULL) then
                insert into document_wgsingularity(docid, singularityid)
                values(:docid, :singularityid);
    
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

        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYPALLET (
    PBARCODE type of R_BARCODE,
    QUANTITY type of R_DOUBLE,
    IDUSER type of R_ID,
    DTBEG type of R_DATETIME = current_timestamp,
    FEATUREID type of R_ID = null)
AS
declare variable productdate r_date;
declare variable waresid r_id;
declare variable qplan r_double;
declare variable producerid r_id;
declare variable manid r_id;
declare variable mansiteid r_id;
declare variable zoneid r_id;
declare variable whid r_id;
declare variable ttid_income r_id;
declare variable taskid r_id;
declare variable wmsid r_id;
declare variable taskwaresid r_id;
declare variable pnumber r_barcode;
declare variable ptypeid_finishgood r_id;
declare variable palletid r_id;
declare variable wlincomeid r_id;
declare variable wlotid r_id;
declare variable dtid_income r_id;
declare variable docid type of column DOCUMENT.docid;
declare variable cargoid type of column cargo.cargoid;
declare variable docid_fundincome type of column DOCUMENT.docid;
begin
    if (:quantity is NULL) then
        exception exc_wh_wrongamount;

    select wh.zoneid, wh.whid, wh.manid
      from wh_user_infoshort(:iduser) wh
      into :zoneid, :whid, :manid;

    select pfp.productdate, pfp.waresid, pfp.quantity, pfp.producerid, pfp.number,
           coalesce(pfp.dtid_income, pl.dtid_income, p.dtid_income_print, p.dtid_income)
      from pallet_finishprint pfp
           left join fg_producer p on p.objid = pfp.producerid
           left join fg_prodlines pl on pl.id_prodline = pfp.prodlineid
     where pfp.barcode = :pbarcode and pfp.enabled = '1'
      into :productdate, :waresid, :qplan, :producerid, :pnumber, :dtid_income;

    execute procedure WH_INCOMEFG_BYPALLET_FUNDINCOME(:producerid, :whid, :waresid, :productdate, :quantity)
     returning_values :docid_fundincome;

    select k.sid
      from k_get_user_wmsessionid(:manid, 'M') k
      into :wmsid;

    select m.siteid
      from wh_man_getsite(:manid) m
      into :mansiteid;

    execute procedure wh_ttid_incomefg
     returning_values :ttid_income;

    insert into wm_task(tasktypeid, zoneid, status, siteid)
    values(:ttid_income, :zoneid, '0', :mansiteid)
    returning taskid
    into :taskid;

    select wh.id
      from wh_paltypeid_finishgood wh
      into :ptypeid_finishgood;

    insert into pallet(ptypeid, barcode, number, siteid, zoneid, objid)
    values(:ptypeid_finishgood, :pbarcode, :pnumber, :mansiteid, :zoneid, :whid)
    returning palletid
    into :palletid;

    if (:featureid is NOT NULL) then
        execute procedure wh_pallet_feature_set(:palletid, :featureid, :manid, 'M');

    update wm_task t
       set t.wm_sessionid = :wmsid, t.begintime = :dtbeg, t.status = '1'
     where t.taskid = :taskid;

    insert into wm_task_pallet(taskid, palletid, status)
    values(:taskid, :palletid, '2');

    update or insert into wareslot(objid, zoneid, waresid, productdate, status)
    values(:whid, :zoneid, :waresid, :productdate, '1')
    matching(objid, zoneid, waresid, productdate)
    returning wlotid
    into :wlotid;

    select first(1) d.docid
      from document d
     where d.doctype = :dtid_income
       and d.fromobj = :producerid
       and d.toobj = :whid
       and d.status = 'c'
       and d.docdate = cast(:dtbeg as date)
      into :docid;

    if (:docid is NULL) then
    begin
        select k.docid
          from k_doccreate(:producerid, :whid, NULL, :dtid_income,
                           cast(:dtbeg as date), cast(:dtbeg as date),
                           NULL, NULL, null, NULL, NULL) k
          into :docid;

        update document d
           set d.status = 'c'
         where d.docid = :docid;
    end

    update or insert into docbond ( DOCBONDTID, DOC1ID, DOC2ID)
    values ( (select dbt.docbondtid from docbondtype dbt where dbt.code = 'FUNDINCOME'), :docid_fundincome, :docid)
    matching (DOCBONDTID, DOC1ID, DOC2ID);

    update or insert into wareslotincomes(docid, wlotid)
    values(:docid, :wlotid)
    matching(docid, wlotid)
    returning id
    into :wlincomeid;

    insert into wm_task_wares(taskid, waresid, status, wm_sessionid, successscan, quantity, begintime)
    values(:taskid, :waresid, '1', :wmsid, :qplan, :quantity, :dtbeg)
    returning taskwaresid
    into :taskwaresid;

    insert into wm_task_lot(palletid,  wlotid, taskwaresid, chgwli, wlincomeid, quantity)
    values(:palletid, :wlotid, :taskwaresid, '1', :wlincomeid, :quantity);

    update wm_task_wares tw
       set tw.status='2',tw.endtime = current_timestamp
     where tw.taskwaresid = :taskwaresid;

    update wm_task t
       set t.status = '2',t.docid = :docid
     where t.taskid = :taskid;

    execute procedure k_get_cargoid(:docid, :waresid)
      returning_values :cargoid;

    if (:cargoid is NULL) then
        insert into cargo(document, waresid, amount, price)
        values(:docid, :waresid, :quantity, 0.000);
    else
        update cargo cg
           set cg.amount = cg.amount + :quantity
         where cg.cargoid = :cargoid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYSTACK (
    TASKID type of column wm_task.taskid,
    STACKID type of column site.siteid,
    WARESID type of column GWARES.waresid,
    MODELID type of column model_stack.modelid,
    LINEID type of column fg_prodlines.id_prodline,
    PRODUCERID type of column OBJECT.objid,
    PCNT type of R_NUMBER,
    PQ type of R_DOUBLE,
    PRODUCTDATE type of R_DATE,
    BESTBEFOREDATE type of R_DATE,
    IDUSER type of R_ID,
    DTBEG type of R_DATETIME = current_timestamp)
AS
declare variable i type of R_NUMBER;
declare variable WHID type of column OBJECT.objid;
declare variable ZONEID type of column SITEZONE.zoneid;
declare variable MANID type of column MAN.manid;
declare variable PNUMBER type of column PALLET.number;
declare variable PBARCODE type of column PALLET.barcode;
declare variable wmsid type of column WM_SESSION.sessionid;
declare variable taskwaresid type of column wm_task_wares.taskwaresid;
declare variable ptypeid_finishgood type of column pallet_type.id;
declare variable palletid type of column PALLET.palletid;
declare variable wlincomeid type of column wareslotincomes.id;
declare variable wlotid type of column WARESLOT.wlotid;
declare variable docid type of column DOCUMENT.docid;
declare variable docid_fundincome type of column DOCUMENT.docid;
declare variable cargoid type of column CARGO.cargoid;
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

  execute procedure WH_INCOMEFG_BYPALLET_FUNDINCOME(:producerid, :whid, :waresid, :productdate, :pq*:pcnt)
   returning_values :docid_fundincome;

  update or insert into docbond ( DOCBONDTID, DOC1ID, DOC2ID)
  values ( (select dbt.docbondtid from docbondtype dbt where dbt.code = 'FUNDINCOME'), :docid_fundincome, :docid)
  matching (DOCBONDTID, DOC1ID, DOC2ID);


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

create procedure WH_FUNDINCOME_ISFIRST (
    DOCID_FUNDINCOME type of column DOCUMENT.docid
)
returns (
    ISFIRST type of R_FLAG
)
as
begin
    -- ISFIRST:
    -- = 1 - FirstIncome
    -- = 0 - Else

    if (exists(select *
                 from docbond db
                      left join docbondtype dbt
                        on dbt.docbondtid = db.docbondtid
                      left join wm_task t
                           left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                           left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                        on t.docid = db.doc2id
                where db.doc1id = :docid_fundincome
                  and dbt.code = 'FUNDINCOME'
                  and tt.code in ('INCOME', 'INCOMEFG')
                  and tm.algorithm = 'F'
    )) then
        isfirst = '1';
    else
        isfirst = '0';

    suspend;
end^

SET TERM ; ^

