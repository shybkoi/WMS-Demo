

SET TERM ^ ;

CREATE trigger pallet_comeretprint_ai0 for pallet_comeretprint
active after insert position 0
AS
declare variable ptid_cr type of column pallet_type.id;
declare variable palletid type of column pallet.palletid;
declare variable siteid type of column site.siteid;
begin
    select w.id
      from wh_paltypeid_comereturn w
      into :ptid_cr;

    select w.siteid
      from wh_man_getsite(new.manid) w
      into :siteid;

    insert into pallet(status, barcode, number, ptypeid, siteid, objid, zoneid)
    values ('0',new.barcode,new.number,:ptid_cr,:siteid,new.whid,new.zoneid)
    returning palletid
    into :palletid;

    update pallet_comeretprint pcr
       set pcr.palletid = :palletid
     where pcr.number = new.number and pcr.enabled = '0';
end^

SET TERM ; ^



CREATE UNIQUE INDEX PALLET_TYPE_IDX_CODE
ON PALLET_TYPE (CODE);



CREATE UNIQUE INDEX SITESPECIES_IDX_CODE
ON SITESPECIES (CODE);



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

CREATE OR ALTER procedure WH_USER_LISTPALLET (
    UID R_ID)
returns (
    PID R_ID,
    PNUM R_BARCODE)
AS
declare variable manid type of r_id;
declare variable mansiteid type of r_id;
begin
    select wh.manid
      from wh_user_infoshort(:uid) wh
      into :manid;

    select m.siteid
      from wh_man_getsite(:manid) m
      into :mansiteid;

    for
        select p.palletid, p.number
          from pallet p
         where p.siteid = :mansiteid
           and p.status = '1'
          into :pid, :pnum
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE trigger pallet_incomeprint_ai0 for pallet_incomeprint
active after insert position 0
AS
declare variable ptid_income type of column pallet_type.id;
declare variable palletid type of column pallet.palletid;
declare variable siteid type of column site.siteid;
begin
    select w.id
      from wh_paltypeid_income w
      into :ptid_income;

    select w.siteid
      from wh_man_getsite(new.manid) w
      into :siteid;

    insert into pallet(status, barcode, number, ptypeid, siteid, objid, zoneid)
    values ('0',new.barcode,new.number,:ptid_income,:siteid,new.whid,new.zoneid)
    returning palletid
    into :palletid;

    update pallet_comeretprint pcr
       set pcr.palletid = :palletid
     where pcr.number = new.number and pcr.enabled = '0';
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger pallet_incomeprint_ai0 for pallet_incomeprint
active after insert position 0
AS
declare variable ptid_income type of column pallet_type.id;
declare variable palletid type of column pallet.palletid;
declare variable siteid type of column site.siteid;
begin
    select w.id
      from wh_paltypeid_income w
      into :ptid_income;

    select w.siteid
      from wh_man_getsite(new.manid) w
      into :siteid;

    insert into pallet(status, barcode, number, ptypeid, siteid, objid, zoneid)
    values ('0',new.barcode,new.number,:ptid_income,:siteid,new.whid,new.zoneid)
    returning palletid
    into :palletid;

    update pallet_incomeprint pcr
       set pcr.palletid = :palletid
     where pcr.number = new.number and pcr.enabled = '0';
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger pallet_incomeprint_bi for pallet_incomeprint
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
         where pt.code = 'I'
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



CREATE SEQUENCE G_PALLETIBARCODE;



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_bu0 for wh_reserve
active before update position 0
as
declare variable wliamount type of column wareslotitem.amount;
declare variable wliamount_bad type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
declare variable ramount_bad type of column wh_reserve.amountbad;
declare variable ptypeid_cr type of column pallet_type.id;
begin
  if (new.amountbad is NULL) then
      new.amountbad = 0.000;

  if (new.amount < -0.0001 or new.amountbad < -0.0001) then
      exception exc_wh_reserve 'Нельзя зарезервировать отрицательное количество!';

  if (old.amount - new.amount < -0.00001 or old.amountbad - new.amountbad < -0.00001 ) then
  begin
    select w.id
      from WH_PALTYPEID_COMERETURN w
      into :ptypeid_cr;

        select sum(
                case
                    when p.ptypeid = :ptypeid_cr then 0.000
                    else wli.amount
                end
               ),
               sum(
                case
                    when p.ptypeid = :ptypeid_cr then wli.amount
                    else 0.000
                end
               )
          from wareslot wl
               left join wareslotitem wli
                    left join pallet p
                      on p.palletid = wli.palletid
                 on wli.wlotid = wl.wlotid
         where wl.waresid = new.waresid
           and wl.productdate = new.productdate
           and wl.status = '1'
          into :wliamount, :wliamount_bad;
        if (:wliamount is NULL) then
            wliamount = 0.000;
        if (:wliamount_bad is NULL) then
            wliamount_bad = 0.000;

        select sum(r.amount), sum(r.amountbad)
          from wh_reserve r
         where r.waresid = new.waresid
           and r.productdate = new.productdate
          into :ramount, :ramount_bad;
        if (:ramount is NULL) then
            ramount = 0.000;
        if (:ramount_bad is NULL) then
            ramount_bad = 0.000;

        if (:wliamount - :ramount + old.amount - new.amount < -0.000001) then
          exception exc_wh_reserve 'Нельзя зарезервировать больше остатка!';

        if (:wliamount_bad - :ramount_bad + old.amountbad - new.amountbad < -0.000001) then
          exception exc_wh_reserve 'Нельзя зарезервировать больше остатка!';
  end

  if (new.amount - new.amountsale < -0.0000001) then
    exception exc_wh_reserve 'Нельзя зарезервировать меньше резерва под продажу!';

  new.amountfree = new.amount - new.amountsale;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_WORKPALLET_SAVE (
    WMSESID type of column WM_SESSION.sessionid,
    PALLETID type of column PALLET.palletid,
    WUID type of column WARESUNIT.waresunitid,
    WARESLOTS varchar(1023),
    AMOUNTS varchar(1023),
    NEWPALLETID type of column PALLET.palletid,
    DBEG type of R_DATETIME)
AS
declare variable wordwlotid varchar(1024);
declare variable wordamount varchar(1024);
declare variable amount double precision;
declare variable taskid type of r_id;
declare variable waresid type of r_id;
declare variable ttid type of r_id;
declare variable siteid type of r_id;
declare variable newsiteid type of r_id;
declare variable newobjid type of r_id;
declare variable wlid type of r_id;
declare variable wufactor type of r_id;
declare variable twid type of r_id;
declare variable seszoneobjid type of r_id;
declare variable i smallint;
declare variable paramvalue varchar(255);
declare variable tmid_minus type of r_id;
declare variable tmid_plus type of r_id;
declare variable taskid_minus type of r_id;
declare variable taskid_plus type of r_id;
declare variable docid_minus type of r_id;
declare variable docid_plus type of r_id;
declare variable twid_minus type of r_id;
declare variable twid_plus type of r_id;
declare variable productdate type of r_date;
declare variable new_wlid type of r_id;
declare variable wlincomeid type of r_id;
declare variable ispalletcr type of R_FLAG;
declare variable isnewpalletcr type of R_FLAG;
declare variable whid type of column OBJECT.objid;
declare variable fundobjid type of column OBJECT.objid;
declare variable spCode type of column sitespecies.code;
BEGIN
  if (:dbeg is null) then dbeg = current_timestamp;
  if (:palletid = :newpalletid) then
    exception exc_k_common 'Нельзя переместить с себя на себя!';

  select objid
    from k_wh_sessionzoneobj(:wmsesid)
    into :seszoneobjid;

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

  if (exists(select wl.wlotid
               from wareslotitem wli
                    left join wareslot wl
                         left join k_wh_siteverify_wareslot_tmp tmp on tmp.wareslotid = wl.wlotid
                      on wl.wlotid = wli.wlotid
              where wli.palletid = :palletid
                and wl.waresid = :waresid
              group by wl.wlotid
             having sum(wli.amount)-min(tmp.amount)<-0.00001)) then
        exception exc_k_common 'Невозможно взять с партии больше, чем есть!';


  amount = NULL;
  select sum(tmp.amount)
    from k_wh_siteverify_wareslot_tmp tmp
   where tmp.amount > 0.00001
    into :amount;
  if (:amount is NULL) then amount = 0.0000;

  if (:amount < 0.00001) then
        exception exc_k_common 'Нечего перемещать!';

  siteid = NULL;
  select p.siteid, iif(pt.code='CR', '1', '0'), sp.code
    from pallet p
         left join pallet_type pt on pt.id = p.ptypeid
         left join site s
              left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
           on s.siteid = p.siteid
   where p.palletid = :palletid
     and p.pallettype <> '2'
    into :siteid, :ispalletcr, :spcode;
  if (:siteid is NULL) then
    exception exc_wh_wrongpallet 'Не верный тип поддона - отправителя!';
  if (:spCode = 'STACK') then
    exception exc_wh_wrongpallet 'Перемещение товара запрещено для паллетов в штабеле';
  execute procedure wh_session_chkpallet(:wmsesid,:palletid,NULL);

  select p.siteid,p.objid,iif(pt.code='CR', '1', '0'),sp.code
    from pallet p
         left join pallet_type pt on pt.id = p.ptypeid
         left join site s
              left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
           on s.siteid = p.siteid
   where p.palletid = :newpalletid
     and p.pallettype <> '2'
    into :newsiteid,:newobjid,:isnewpalletcr,:spCOde;
  if (:spCode = 'STACK') then
    exception exc_wh_wrongpallet 'Перемещение товара запрещено для паллетов в штабеле';

  SELECT tt.tasktypeid
    FROM wm_tasktype tt
   where tt.code = 'WORKPALLET'
    into :ttid;

  if (:newpalletid is NOT NULL and :seszoneobjid<>:newobjid) then
  begin
        select k.paramvalue
          from K_SITEZONEMETHOD_PARAMVALUE(:ttid,NULL,:seszoneobjid,NULL,'saleincome') k
          into :paramvalue;

        if (:paramvalue is NOT NULL and :paramValue = '1') then
        begin
          -- проверим а сам объект может быть доступен?
          if (not exists(select *
                           from wm_session wms
                                left join sitezone_employees sze
                                     left join sitezone sz on sz.zoneid = sze.zoneid
                                  on sze.employeeid = wms.objid
                          where wms.sessionid = :wmsesid
                            and sz.objid = :newobjid)) then
            exception exc_k_wrongtasktype 'Поддон привязан к зоне, вам запрещенной!';

          -- Подготовка списания
          select tm.methodid
            from wm_taskmethod tm
           where tm.tasktypeid = :ttid
             and tm.algorithm = '-'
            into :tmid_minus;
          if (:tmid_minus is NULL) then
            exception exc_k_wrongtasktype 'Нет метода списания у работы с поддоном!';

          paramvalue = NULL;
          select k.paramvalue
            from K_SITEZONEMETHOD_PARAMVALUE(:ttid,:tmid_minus,:seszoneobjid,NULL,'doctid') k
            into :paramvalue;
          if (:paramvalue is NULL) then
            exception exc_k_wrongtasktype 'Не задан документ списания остатков!';

          execute procedure k_doccreate_docman(:seszoneobjid,NULL,:newobjid,NULL,cast(:paramvalue as integer),current_date, current_date, NULL, NULL, NULL, NULL, 'WP')
           returning_values :docid_minus;

          insert into wm_task(tasktypeid,taskmethodid,status,wm_sessionid,begintime,endtime,assigntime,docid)
          values (:ttid,:tmid_minus,'2',:wmsesid,:dbeg,current_timestamp,:dbeg,:docid_minus)
          returning taskid
          into :taskid_minus;

          insert into wm_task_pallet(taskid,palletid,siteid,status)
          values (:taskid_minus,:palletid,:siteid,'1');

          insert into wm_task_wares(taskid, waresid, status, quantity, begintime, endtime, wm_sessionid, palletid, siteid)
          values(:taskid_minus, :waresid, '2', :amount, :dbeg, current_timestamp, :wmsesid, :palletid, :siteid)
          returning taskwaresid
          into :twid_minus;

          insert into cargo(document,waresid,amount,price)
          values(:docid_minus,:waresid,:amount,0.000);
    
          -- Подготовка прихода
          select tm.methodid
            from wm_taskmethod tm
           where tm.tasktypeid = :ttid
             and tm.algorithm = '+'
            into :tmid_plus;
          if (:tmid_plus is NUll) then
            exception exc_k_wrongtasktype 'Нет метода приемки у работы с поддоном!';

          paramvalue = NULL;
          select k.paramvalue
            from K_SITEZONEMETHOD_PARAMVALUE(:ttid,:tmid_plus,:seszoneobjid,NULL,'doctid') k
            into :paramvalue;
          if (:paramvalue is NULL) then
            exception exc_k_wrongtasktype 'Не задан документ приемка товара!';

          execute procedure k_doccreate_docman(:seszoneobjid,NULL,:newobjid,NULL,cast(:paramvalue as integer),current_date, current_date, NULL, NULL, NULL, NULL, 'WP')
           returning_values :docid_plus;

          insert into wm_task(tasktypeid,taskmethodid,status,wm_sessionid,begintime,endtime,assigntime,docid)
          values (:ttid,:tmid_plus,'2',:wmsesid,:dbeg,current_timestamp,:dbeg,:docid_plus)
          returning taskid
          into :taskid_plus;

          insert into wm_task_pallet(taskid,palletid,siteid,status)
          values (:taskid_plus,:newpalletid,:newsiteid,'1');

          insert into wm_task_wares(taskid, waresid, status, quantity, begintime, endtime, wm_sessionid, palletid, siteid)
          values(:taskid_plus, :waresid, '2', :amount, :dbeg, current_timestamp, :wmsesid, :newpalletid, :newsiteid)
          returning taskwaresid
          into :twid_plus;

          insert into cargo(document,waresid,amount,price)
          values(:docid_plus,:waresid,:amount,0.000);

          -- Перебрасываем остатки
          for
              select tmp.wareslotid,tmp.amount,wl.productdate
                from k_wh_siteverify_wareslot_tmp tmp
                     left join wareslot wl on wl.wlotid = tmp.wareslotid
               where tmp.amount > 0.00001
                into :wlid,:amount,:productdate
          do
          begin
              insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity, wm_sessionid, chgwli,wlincomeid)
              select :twid_minus,:wlid,:palletid,o.amount,:wmsesid,'1',o.wlincomeid
                from core_listwlincomes(:wlid,:palletid,-:amount) o;
        
              update or insert into wareslot(waresid, productdate, status,objid)
              values (:waresid, :productdate, '1', :newobjid)
              matching(waresid, productdate, objid)
              returning wlotid
              into :new_wlid;

              insert into wareslotincomes(wlotid,docid)
              values(:new_wlid,:docid_plus)
              returning id
              into :wlincomeid;

              -- Триггер проставит wlincomeid, но может добавить записи
              insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,wm_sessionid,chgwli,wlincomeid)
              values (:twid_plus,:new_wlid,:newpalletid,:amount,:wmsesid,'1',:wlincomeid);
          end

          -- Связываем документы
          insert into docbond(doc1id,doc2id,docbondtid,restchange1,restchange2)
          values(:docid_minus,:docid_plus,(select dbt.docbondtid from docbondtype dbt where dbt.code='WORKPALLET') ,'0','0');

          -- Поднимаем статусы документов
          execute procedure K_WH_WORKPALLET_SAVE_DOCSTATUP(:docid_minus);
          execute procedure K_WH_WORKPALLET_SAVE_DOCSTATUP(:docid_plus);
        end
        else
            exception exc_k_common 'Не верный тип или владелец поддона - получателя!';
  end
  else
  begin
      insert into wm_task(tasktypeid,status,wm_sessionid,begintime,endtime,assigntime)
      values (:ttid,'2',:wmsesid,:dbeg,current_timestamp,:dbeg)
      returning taskid
      into :taskid;

      insert into wm_task_pallet(taskid,palletid,siteid,status)
      values (:taskid,:palletid,:siteid,'1');

      insert into wm_task_wares(taskid, waresid, status, quantity, begintime, endtime, wm_sessionid, palletid, siteid)
      values(:taskid, :waresid, '2', :amount, :dbeg, current_timestamp, :wmsesid, :newpalletid, :siteid)
      returning taskwaresid
      into :twid;
    

      for
          select tmp.wareslotid,tmp.amount,wl.productdate
            from k_wh_siteverify_wareslot_tmp tmp
                 left join wareslot wl on wl.wlotid = tmp.wareslotid
           where tmp.amount > 0.00001
            into :wlid,:amount,:productdate
      do
      FOR
        select o.amount, o.wlincomeid, fo.fundobjid
          from core_listwlincomes(:wlid,:palletid,-:amount) o
               left join wh_incomedoc_getobjectsfund(o.docid) fo on 1=1
          into :amount, :wlincomeid, :fundobjid
      do
      begin
          if (:ispalletcr <> :isnewpalletcr) then
          begin
            if (:ispalletcr = '1') then
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, 0.000, :fundobjid, :amount, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, :amount, :fundobjid, 0.000, :taskid);
            end
          end

          -- Процедура вернет расходные количества, поэтому при приходовании знак наоборот
          insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
          values(:twid,:wlid,:palletid,:amount,'1',:wlincomeid,:wmsesid);

          insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
          values(:twid,:wlid,:newpalletid,-:amount,'1',:wlincomeid,:wmsesid);

          if (:ispalletcr <> :isnewpalletcr) then
          begin
            if (:ispalletcr = '1') then
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, -:amount, :fundobjid, 0.000, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, 0.000, :fundobjid, -:amount, :taskid);
            end
          end
      end
  end
END^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_RPALLETPRINT_I_DATA (
    DTBEG type of R_DATETIME,
    DTEND type of R_DATETIME)
returns (
    PNUM type of column PALLET_INCOMEPRINT.NUMBER,
    DT type of column PALLET_INCOMEPRINT.DATETIME,
    MANFIO type of R_VARCHAR255,
    PID type of column PALLET.PALLETID)
AS
begin
    for
        select p.datetime, p.palletid, p.number,
               (select objname from wh_get_objectname(p.manid))
          from pallet_incomeprint p
         where p.datetime between :dtbeg and :dtend
          into :dt, :pid, :pnum, :manfio
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger pallet_au_rcrest for pallet
active after update position 0
as
declare variable oldcalcrest type of r_flag;
declare variable newcalcrest type of r_flag;
declare variable waresid type of r_id;
declare variable objid type of r_id;
declare variable amount type of r_double;
declare variable oldcanrefill type of r_flag;
declare variable newcanrefill type of r_flag;
declare variable ptCode type of column PALLET_TYPE.code;
begin
    if (old.siteid <> new.siteid) then
    begin
        select coalesce(sp.calcrest,'1')
          from site s
               left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
         where s.siteid = old.siteid
          into :oldcalcrest;

        select coalesce(sp.calcrest,'1')
          from site s
               left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
         where s.siteid = new.siteid
          into :newcalcrest;

        if (:oldcalcrest <> :newcalcrest) then
        begin
            execute procedure wh_pallet_refillchk(old.palletid,old.ptypeid)
             returning_values :oldcanrefill;

            if (old.ptypeid = new.ptypeid) then
                newcanrefill = :oldcanrefill;
            else
                execute procedure wh_pallet_refillchk(new.palletid,new.ptypeid)
                 returning_values :newcanrefill;

            if (:oldcalcrest = '1') then
            begin
                for
                    select wl.waresid,wl.objid,sum(wli.amount)
                      from wareslotitem wli
                           left join wareslot wl on wl.wlotid = wli.wlotid
                     where wli.palletid = new.palletid
                       and wli.amount > 0.00001
                     group by wl.waresid,wl.objid
                      into :waresid,:objid,:amount
                do
                    update wareslotrest wlr
                       set wlr.rest = wlr.rest - :amount,
                           wlr.refill = wlr.refill - iif(:oldcanrefill='1', :amount, 0.000)
                     where wlr.objid = :objid
                       and wlr.waresid = :waresid;
            end

            if (:newcalcrest = '1') then
            begin
                for
                    select wl.waresid,wl.objid,sum(wli.amount)
                      from wareslotitem wli
                           left join wareslot wl on wl.wlotid = wli.wlotid
                     where wli.palletid = new.palletid
                       and wli.amount > 0.00001
                     group by wl.waresid,wl.objid
                      into :waresid,:objid,:amount
                do
                if (exists(select *
                             from wareslotrest wlr
                            where wlr.objid= :objid
                              and wlr.waresid = :waresid)) then
                    update wareslotrest wlr
                       set wlr.rest = wlr.rest + :amount,
                           wlr.refill = wlr.refill + iif(:newcanrefill='1', :amount, 0.000)
                     where wlr.objid = :objid
                       and wlr.waresid = :waresid;
                else
                   insert into wareslotrest(objid, waresid, rest, refill)
                   values(:objid, :waresid, :amount, iif(:newcanrefill='1', :amount, 0.000));
            end
        end
    end
    else if (old.ptypeid <> new.ptypeid) then
    begin
        execute procedure wh_pallet_refillchk(old.palletid,old.ptypeid)
         returning_values :oldcanrefill;

        execute procedure wh_pallet_refillchk(new.palletid,new.ptypeid)
         returning_values :newcanrefill;
        
        if (:oldcanrefill <> :newcanrefill) then
        begin
            if (:oldcanrefill = '1') then
                for
                    select wl.waresid,wl.objid,sum(wli.amount)
                      from wareslotitem wli
                           left join wareslot wl on wl.wlotid = wli.wlotid
                     where wli.palletid = new.palletid
                       and wli.amount > 0.00001
                     group by wl.waresid,wl.objid
                      into :waresid,:objid,:amount
                do
                    update wareslotrest wlr
                       set wlr.refill = wlr.refill - :amount
                     where wlr.objid = :objid
                       and wlr.waresid = :waresid;

            if (:newcanrefill = '1') then
                for
                    select wl.waresid,wl.objid,sum(wli.amount)
                      from wareslotitem wli
                           left join wareslot wl on wl.wlotid = wli.wlotid
                     where wli.palletid = new.palletid
                       and wli.amount > 0.00001
                     group by wl.waresid,wl.objid
                      into :waresid,:objid,:amount
                do
                if (exists(select *
                             from wareslotrest wlr
                            where wlr.objid= :objid
                              and wlr.waresid = :waresid)) then
                    update wareslotrest wlr
                       set wlr.refill = wlr.refill + :amount
                     where wlr.objid = :objid
                       and wlr.waresid = :waresid;
                else
                   insert into wareslotrest(objid, waresid, rest, refill)
                   values(:objid, :waresid, :amount, :amount);
        end
    end

    if (old.status = '0' and new.status='1') then
    begin
        select pt.code
          from pallet_type pt
         where pt.id = new.ptypeid
          into :ptCode;

        if (:ptCode = 'I') then
            update pallet_incomeprint pp
               set pp.enabled = '1'
             where pp.palletid = new.palletid and pp.enabled = '0';
        else if (:ptCode = 'CR') then
            update pallet_comeretprint pp
               set pp.enabled = '1'
             where pp.palletid = new.palletid and pp.enabled = '0';
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger pallet_incomeprint_bu for pallet_incomeprint
inactive before update position 0
as
begin
    if (old.palletid is NULL and new.palletid is NOT NULL and new.enabled = '1') then
        new.enabled = '0';
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger pallet_au_rcrest for pallet
active after update position 0
as
declare variable oldcalcrest type of r_flag;
declare variable newcalcrest type of r_flag;
declare variable waresid type of r_id;
declare variable objid type of r_id;
declare variable amount type of r_double;
declare variable oldcanrefill type of r_flag;
declare variable newcanrefill type of r_flag;
declare variable ptCode type of column PALLET_TYPE.code;
begin
    if (old.siteid <> new.siteid) then
    begin
        select coalesce(sp.calcrest,'1')
          from site s
               left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
         where s.siteid = old.siteid
          into :oldcalcrest;

        select coalesce(sp.calcrest,'1')
          from site s
               left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
         where s.siteid = new.siteid
          into :newcalcrest;

        if (:oldcalcrest <> :newcalcrest) then
        begin
            execute procedure wh_pallet_refillchk(old.palletid,old.ptypeid)
             returning_values :oldcanrefill;

            if (old.ptypeid = new.ptypeid) then
                newcanrefill = :oldcanrefill;
            else
                execute procedure wh_pallet_refillchk(new.palletid,new.ptypeid)
                 returning_values :newcanrefill;

            if (:oldcalcrest = '1') then
            begin
                for
                    select wl.waresid,wl.objid,sum(wli.amount)
                      from wareslotitem wli
                           left join wareslot wl on wl.wlotid = wli.wlotid
                     where wli.palletid = new.palletid
                       and wli.amount > 0.00001
                     group by wl.waresid,wl.objid
                      into :waresid,:objid,:amount
                do
                    update wareslotrest wlr
                       set wlr.rest = wlr.rest - :amount,
                           wlr.refill = wlr.refill - iif(:oldcanrefill='1', :amount, 0.000)
                     where wlr.objid = :objid
                       and wlr.waresid = :waresid;
            end

            if (:newcalcrest = '1') then
            begin
                for
                    select wl.waresid,wl.objid,sum(wli.amount)
                      from wareslotitem wli
                           left join wareslot wl on wl.wlotid = wli.wlotid
                     where wli.palletid = new.palletid
                       and wli.amount > 0.00001
                     group by wl.waresid,wl.objid
                      into :waresid,:objid,:amount
                do
                if (exists(select *
                             from wareslotrest wlr
                            where wlr.objid= :objid
                              and wlr.waresid = :waresid)) then
                    update wareslotrest wlr
                       set wlr.rest = wlr.rest + :amount,
                           wlr.refill = wlr.refill + iif(:newcanrefill='1', :amount, 0.000)
                     where wlr.objid = :objid
                       and wlr.waresid = :waresid;
                else
                   insert into wareslotrest(objid, waresid, rest, refill)
                   values(:objid, :waresid, :amount, iif(:newcanrefill='1', :amount, 0.000));
            end
        end
    end
    else if (old.ptypeid <> new.ptypeid) then
    begin
        execute procedure wh_pallet_refillchk(old.palletid,old.ptypeid)
         returning_values :oldcanrefill;

        execute procedure wh_pallet_refillchk(new.palletid,new.ptypeid)
         returning_values :newcanrefill;
        
        if (:oldcanrefill <> :newcanrefill) then
        begin
            if (:oldcanrefill = '1') then
                for
                    select wl.waresid,wl.objid,sum(wli.amount)
                      from wareslotitem wli
                           left join wareslot wl on wl.wlotid = wli.wlotid
                     where wli.palletid = new.palletid
                       and wli.amount > 0.00001
                     group by wl.waresid,wl.objid
                      into :waresid,:objid,:amount
                do
                    update wareslotrest wlr
                       set wlr.refill = wlr.refill - :amount
                     where wlr.objid = :objid
                       and wlr.waresid = :waresid;

            if (:newcanrefill = '1') then
                for
                    select wl.waresid,wl.objid,sum(wli.amount)
                      from wareslotitem wli
                           left join wareslot wl on wl.wlotid = wli.wlotid
                     where wli.palletid = new.palletid
                       and wli.amount > 0.00001
                     group by wl.waresid,wl.objid
                      into :waresid,:objid,:amount
                do
                if (exists(select *
                             from wareslotrest wlr
                            where wlr.objid= :objid
                              and wlr.waresid = :waresid)) then
                    update wareslotrest wlr
                       set wlr.refill = wlr.refill + :amount
                     where wlr.objid = :objid
                       and wlr.waresid = :waresid;
                else
                   insert into wareslotrest(objid, waresid, rest, refill)
                   values(:objid, :waresid, :amount, :amount);
        end
    end

    if (old.status = '0' and new.status='1') then
    begin
        select pt.code
          from pallet_type pt
         where pt.id = new.ptypeid
          into :ptCode;

        if (:ptCode = 'I') then
            update pallet_incomeprint pp
               set pp.enabled = '0'
             where pp.palletid = new.palletid and pp.enabled = '1';
        else if (:ptCode = 'CR') then
            update pallet_comeretprint pp
               set pp.enabled = '0'
             where pp.palletid = new.palletid and pp.enabled = '1';
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger pallet_comeretprint_bu for pallet_comeretprint
inactive before update position 0
as
begin
    if (old.palletid is NULL and new.palletid is NOT NULL and new.enabled = '1') then
        new.enabled = '0';
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger pallet_incomeprint_bi for pallet_incomeprint
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
         where pt.code = 'I'
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

    exception exc_k_common new.enabled;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_PALLETINCOME_PRINT (
    MANID type of R_ID,
    PALLETID type of R_ID)
returns (
    NUM1 varchar(3),
    NUM2 varchar(3),
    BARCODE type of R_BARCODE,
    ZONENAME type of R_NAME,
    EMPLNAME type of R_FULLNAME,
    DETAIL integer)
AS
declare variable pnumber type of r_barcode;
declare variable zoneid type of r_id;
begin
    if (:palletid is NULL or :palletid=0 ) then
    begin
        insert into pallet_incomeprint(manid)
        values(:manid)
        returning zoneid, number, barcode
        into :zoneid, :pnumber, :barcode;

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

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger pallet_incomeprint_bi for pallet_incomeprint
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
         where pt.code = 'I'
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

CREATE OR ALTER trigger pallet_incomeprint_ai0 for pallet_incomeprint
active after insert position 0
AS
declare variable ptid_income type of column pallet_type.id;
declare variable palletid type of column pallet.palletid;
declare variable siteid type of column site.siteid;
begin
    select w.id
      from wh_paltypeid_income w
      into :ptid_income;

    select w.siteid
      from wh_man_getsite(new.manid) w
      into :siteid;

    insert into pallet(status, barcode, number, ptypeid, siteid, objid, zoneid)
    values ('0',new.barcode,new.number,:ptid_income,:siteid,new.whid,new.zoneid)
    returning palletid
    into :palletid;

    update pallet_incomeprint pcr
       set pcr.palletid = :palletid
     where pcr.number = new.number and pcr.enabled = '0';

        exception exc_k_common new.enabled;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_PALLETINCOME_PRINT (
    MANID type of R_ID,
    PALLETID type of R_ID)
returns (
    NUM1 varchar(3),
    NUM2 varchar(3),
    BARCODE type of R_BARCODE,
    ZONENAME type of R_NAME,
    EMPLNAME type of R_FULLNAME,
    DETAIL integer)
AS
declare variable pnumber type of r_barcode;
declare variable zoneid type of r_id;
begin
    if (:palletid is NULL or :palletid=0 ) then
    begin
        insert into pallet_incomeprint(manid)
        values(:manid)
        returning zoneid, number, barcode
        into :zoneid, :pnumber, :barcode;

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

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger pallet_incomeprint_ai0 for pallet_incomeprint
active after insert position 0
AS
declare variable ptid_income type of column pallet_type.id;
declare variable palletid type of column pallet.palletid;
declare variable siteid type of column site.siteid;
begin
    select w.id
      from wh_paltypeid_income w
      into :ptid_income;

    select w.siteid
      from wh_man_getsite(new.manid) w
      into :siteid;

    insert into pallet(status, barcode, number, ptypeid, siteid, objid, zoneid)
    values ('0',new.barcode,new.number,:ptid_income,:siteid,new.whid,new.zoneid)
    returning palletid
    into :palletid;

    update pallet_incomeprint pcr
       set pcr.palletid = :palletid
     where pcr.number = new.number and pcr.enabled = '0';
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_PALLETINCOME_PRINT (
    MANID type of R_ID,
    PALLETID type of R_ID)
returns (
    NUM1 varchar(3),
    NUM2 varchar(3),
    BARCODE type of R_BARCODE,
    ZONENAME type of R_NAME,
    EMPLNAME type of R_FULLNAME,
    DETAIL integer)
AS
declare variable pnumber type of r_barcode;
declare variable zoneid type of r_id;
begin
    if (:palletid is NULL or :palletid=0 ) then
    begin
        insert into pallet_incomeprint(manid)
        values(:manid)
        returning zoneid, number, barcode
        into :zoneid, :pnumber, :barcode;

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

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger pallet_incomeprint_ai0 for pallet_incomeprint
inactive after insert position 0
AS
declare variable ptid_income type of column pallet_type.id;
declare variable palletid type of column pallet.palletid;
declare variable siteid type of column site.siteid;
begin
    select w.id
      from wh_paltypeid_income w
      into :ptid_income;

    select w.siteid
      from wh_man_getsite(new.manid) w
      into :siteid;

    insert into pallet(status, barcode, number, ptypeid, siteid, objid, zoneid)
    values ('0',new.barcode,new.number,:ptid_income,:siteid,new.whid,new.zoneid)
    returning palletid
    into :palletid;

    update pallet_incomeprint pcr
       set pcr.palletid = :palletid
     where pcr.number = new.number and pcr.enabled = '0';
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger pallet_incomeprint_ai0 for pallet_incomeprint
inactive after insert position 0
AS
declare variable ptid_income type of column pallet_type.id;
declare variable palletid type of column pallet.palletid;
declare variable siteid type of column site.siteid;
begin
    select w.id
      from wh_paltypeid_income w
      into :ptid_income;

    select w.siteid
      from wh_man_getsite(new.manid) w
      into :siteid;

    insert into pallet(status, barcode, number, ptypeid, siteid, objid, zoneid)
    values ('0',new.barcode,new.number,:ptid_income,:siteid,new.whid,new.zoneid)
    returning palletid
    into :palletid;

    update pallet_incomeprint pcr
       set pcr.palletid = :palletid
     where pcr.number = new.number and pcr.enabled = '1';
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
       set pip.palletid = new.palletid --, pip.enabled = '0'
     where pip.barcode = new.barcode and pip.enabled = '1' and pip.palletid is NULL;
  else if (:ptypecode = 'CR') then -- Паллет прихода возвратов от клиентов
    update pallet_comeretprint pip
       set pip.palletid = new.palletid --, pip.enabled = '0'
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

CREATE OR ALTER trigger pallet_incomeprint_ai0 for pallet_incomeprint
active after insert position 0
AS
declare variable ptid_income type of column pallet_type.id;
declare variable palletid type of column pallet.palletid;
declare variable siteid type of column site.siteid;
begin
    select w.id
      from wh_paltypeid_income w
      into :ptid_income;

    select w.siteid
      from wh_man_getsite(new.manid) w
      into :siteid;

    insert into pallet(status, barcode, number, ptypeid, siteid, objid, zoneid)
    values ('0',new.barcode,new.number,:ptid_income,:siteid,new.whid,new.zoneid)
    returning palletid
    into :palletid;

/*    update pallet_incomeprint pcr
       set pcr.palletid = :palletid
     where pcr.number = new.number and pcr.enabled = '1';*/
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_PALLETINCOME_PRINT (
    MANID type of R_ID,
    PALLETID type of R_ID)
returns (
    NUM1 varchar(3),
    NUM2 varchar(3),
    BARCODE type of R_BARCODE,
    ZONENAME type of R_NAME,
    EMPLNAME type of R_FULLNAME,
    DETAIL integer)
AS
declare variable pnumber type of r_barcode;
declare variable zoneid type of r_id;
begin
    if (:palletid is NULL or :palletid=0 ) then
    begin
        insert into pallet_incomeprint(manid)
        values(:manid)
        returning zoneid, number, barcode
        into :zoneid, :pnumber, :barcode;

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

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger pallet_comeretprint_ai0 for pallet_comeretprint
active after insert position 0
AS
declare variable ptid_cr type of column pallet_type.id;
declare variable palletid type of column pallet.palletid;
declare variable siteid type of column site.siteid;
begin
    select w.id
      from wh_paltypeid_comereturn w
      into :ptid_cr;

    select w.siteid
      from wh_man_getsite(new.manid) w
      into :siteid;

    insert into pallet(status, barcode, number, ptypeid, siteid, objid, zoneid)
    values ('0',new.barcode,new.number,:ptid_cr,:siteid,new.whid,new.zoneid)
    returning palletid
    into :palletid;

    /*update pallet_comeretprint pcr
       set pcr.palletid = :palletid
     where pcr.number = new.number and pcr.enabled = '0';*/
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

