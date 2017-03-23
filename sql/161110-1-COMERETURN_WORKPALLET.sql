

SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_SUMMARY_DATA
returns (
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    OBJID type of column OBJECT.OBJID,
    OBJNAME type of R_VARCHAR255,
    Q1 type of column WH_RESERVE.AMOUNT,
    Q2 type of column WH_RESERVE.AMOUNTSALE,
    QB type of column WH_RESERVE.amountbad,
    PRDATE type of column WH_RESERVE.PRODUCTDATE)
AS
begin
    for
        select g.waresid, g.code, g.name,
               r.objid, (select objname from wh_get_objectname(r.objid)),
               r.amount, r.amountsale, r.productdate, r.amountbad
          from wh_reserve r
               left join gwares g on g.waresid = r.waresid
         where r.amount > 0.0000001
          into :wid, :wcode, :wname,
               :objid, :objname,
               :q1, :q2, :prdate, :qb
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_SUMMARY_DATA
returns (
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    OBJID type of column OBJECT.OBJID,
    OBJNAME type of R_VARCHAR255,
    Q1 type of column WH_RESERVE.AMOUNT,
    Q2 type of column WH_RESERVE.AMOUNTSALE,
    QB type of column WH_RESERVE.amountbad,
    PRDATE type of column WH_RESERVE.PRODUCTDATE)
AS
begin
    for
        select g.waresid, g.code, g.name,
               r.objid, (select objname from wh_get_objectname(r.objid)),
               r.amount, r.amountsale, r.productdate, r.amountbad
          from wh_reserve r
               left join gwares g on g.waresid = r.waresid
         where r.amount + r.amountbad > 0.0000001
          into :wid, :wcode, :wname,
               :objid, :objname,
               :q1, :q2, :prdate, :qb
    do
        suspend;
end^

SET TERM ; ^



ALTER TABLE WH_RESERVE_CHANGES
ADD TASKID R_ID;



ALTER TABLE WH_RESERVE_CHANGES
ADD CONSTRAINT FK_WH_RESERVE_CHANGES_TASKID
FOREIGN KEY (TASKID)
REFERENCES WM_TASK(TASKID)
ON DELETE CASCADE
ON UPDATE CASCADE;



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_WORKPALLET_SAVE (
    WMSESID type of R_ID,
    PALLETID type of R_ID,
    WUID type of R_ID,
    WARESLOTS varchar(1023),
    AMOUNTS varchar(1023),
    NEWPALLETID type of R_ID,
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
  select p.siteid, iif(pt.code='CR', '1', '0')
    from pallet p
         left join pallet_type pt on pt.id = p.ptypeid
   where p.palletid = :palletid
     and p.pallettype <> '2'
    into :siteid, :ispalletcr;
  if (:siteid is NULL) then
        exception exc_k_common 'Не верный тип поддона - отправителя!';
  execute procedure wh_session_chkpallet(:wmsesid,:palletid,NULL);

  SELECT tt.tasktypeid
    FROM wm_tasktype tt
   where tt.code = 'WORKPALLET'
    into :ttid;

  select p.siteid,p.objid,iif(pt.code='CR', '1', '0')
    from pallet p
         left join pallet_type pt on pt.id = p.ptypeid
   where p.palletid = :newpalletid
     and p.pallettype <> '2'
    into :newsiteid,:newobjid,:isnewpalletcr;
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
    
      if (:ispalletcr <> :isnewpalletcr) then
      begin
        for
          select wl.productdate,sum(tmp.amount),wl.objid
            from k_wh_siteverify_wareslot_tmp tmp
                 left join wareslot wl on wl.wlotid = tmp.wareslotid
           where tmp.amount > 0.00001
           group by wl.productdate, wl.objid
            into :productdate, :amount, :whid
        do
        begin
            if (:ispalletcr = '1') then
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, 0.000, :whid, -:amount, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, -:amount, :whid, 0.000, :taskid);
            end
        end
      end

      for
          select tmp.wareslotid,tmp.amount
            from k_wh_siteverify_wareslot_tmp tmp
           where tmp.amount > 0.00001
            into :wlid,:amount
      do
      FOR
        select o.amount,o.wlincomeid
          from core_listwlincomes(:wlid,:palletid,-:amount) o
          into :amount,:wlincomeid
      do
      begin
          -- Процедура вернет расходные количества, поэтому при приходовании знак наоборот
          insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
          values(:twid,:wlid,:palletid,:amount,'1',:wlincomeid,:wmsesid);

          insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
          values(:twid,:wlid,:newpalletid,-:amount,'1',:wlincomeid,:wmsesid);
      end

      if (:ispalletcr <> :isnewpalletcr) then
      begin
        for
          select wl.productdate,sum(tmp.amount)
            from k_wh_siteverify_wareslot_tmp tmp
                 left join wareslot wl on wl.wlotid = tmp.wareslotid
           where tmp.amount > 0.00001
           group by wl.productdate
            into :productdate, :amount
        do
        begin
            if (:ispalletcr = '1') then
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, :amount, :whid, 0.000, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, 0.000, :whid, :amount, :taskid);
            end
        end
      end
  end
END^

SET TERM ; ^

