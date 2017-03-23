

SET TERM ^ ;

CREATE OR ALTER procedure CORE_LISTWLINCOMES (
    WLOTID type of column WARESLOT.wlotid,
    PALLETID type of column PALLET.palletid,
    QUANTITY type of R_QUANTITY,
    FLAGSORT type of R_FLAG = null)
returns (
    WLINCOMEID type of column WARESLOTINCOMES.id,
    AMOUNT type of R_QUANTITY,
    DOCID type of column DOCUMENT.docid)
AS
declare variable wlamount type of r_quantity;
declare variable qsign smallint;
begin
    if (:quantity > 0.00001) then qsign = 1;
    else
    begin
        qsign = -1;
        quantity = -:quantity;
    end

    if (:flagsort is NOT NULL and :flagsort = 'N') then --Nulls сначада
    begin
        for
            select wli.amount, wli.wlincomeid, i.docid
              from wareslotitem wli
                   left join wareslotincomes i
                        left join document d on d.docid = i.docid
                     on i.id = wli.wlincomeid
             where wli.wlotid = :wlotid
               and wli.palletid = :palletid
               and -:qsign*wli.amount > 0.00001
             order by wli.wlincomeid ascending nulls last,
                   d.docdate ascending nulls last
              into :wlamount,:wlincomeid,:docid
        do
        -- Сортируем по дате прихода, если дата не установлена (излишек), то последним
        begin
            if (:quantity - :wlamount < 0.000001 ) then
            -- Если надо списать меньше, чем есть на приходе
            begin
                amount = :qsign*:quantity;
                suspend; exit;
            end
            else
            begin
                amount = :qsign*:wlamount;
                quantity = :quantity - :wlamount;
                suspend;
            end
        end
    end
    else
    begin
        for
            select wli.amount, wli.wlincomeid, i.docid
              from wareslotitem wli
                   left join wareslotincomes i
                        left join document d on d.docid = i.docid
                     on i.id = wli.wlincomeid
             where wli.wlotid = :wlotid
               and wli.palletid = :palletid
               and -:qsign*wli.amount > 0.00001
             order by wli.wlincomeid ascending nulls last, d.docdate ascending nulls last
              into :wlamount,:wlincomeid,:docid
        do
        -- Сортируем по дате прихода, если дата не установлена (излишек), то последним
        begin
            if (:quantity - :wlamount < 0.000001 ) then
            -- Если надо списать меньше, чем есть на приходе
            begin
                amount = :qsign*:quantity;
                suspend; exit;
            end
            else
            begin
                amount = :qsign*:wlamount;
                quantity = :quantity - :wlamount;
                suspend;
            end
        end
    end

    if (:quantity > 0.00001) then
    begin
        if (:qsign = -1) then
        begin
            if (not exists(select *
                             from pallet p
                                  left join site s
                                       left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                                    on s.siteid=p.siteid
                            where p.palletid = :palletid
                              and p.pallettype in ('1','N')
                              and sp.code = 'TRASH')) then
                exception exc_k_wrongamount 'Не хватает остатка для списания';
        end
        wlincomeid = NULL;
        amount = :qsign*:quantity;
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_INCOMEDOC_GETOBJECTSFUND (
    DOCID type of column DOCUMENT.docid
)
returns (
    WHID type of column OBJECT.objid,
    FUNDOBJID type of column OBJECT.objid
)
as
declare variable fromobj type of column OBJECT.objid;
declare variable throughobj type of column OBJECT.objid;
declare variable toobj type of column OBJECT.objid;
declare variable dtCode type of column DOCtype.code ;
begin
    select d.fromobj, d.throughobj, d.toobj, dt.code
      from document d
           left join doctype dt on dt.doctid = d.doctype
     where d.docid = :docid
      into :fromobj, :throughobj, :toobj, :dtcode;

    if (:dtcode in ('INCOME', 'INCOMEFG')) then
    begin
        whid = :toobj;
        fundobjid = :whid;
    end
    else if (:dtcode = 'COMERETURN') then
    begin
        whid = :toobj;
        fundobjid = :throughobj;
    end

    suspend;
end^

SET TERM ; ^



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
declare variable fundobjid type of column OBJECT.objid;
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
        select o.amount,o.wlincomeid,fo.fundobjid
          from core_listwlincomes(:wlid,:palletid,-:amount) o
               left join WH_INCOMEDOC_GETOBJECTSFUND(o.docid) fo on 1=1
          into :amount,:wlincomeid,:fundobjid
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
                values ( :waresid, :productdate, :amount, :fundobjid, 0.000, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, 0.000, :fundobjid, :amount, :taskid);
            end
        end
      end
  end
END^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEDOC_GETOBJECTSFUND (
    DOCID type of column DOCUMENT.docid
)
returns (
    WHID type of column OBJECT.objid,
    FUNDOBJID type of column OBJECT.objid
)
as
declare variable fromobj type of column OBJECT.objid;
declare variable throughobj type of column OBJECT.objid;
declare variable toobj type of column OBJECT.objid;
declare variable dtCode type of column DOCtype.code ;
begin
    select d.fromobj, d.throughobj, d.toobj, dt.code
      from document d
           left join doctype dt on dt.doctid = d.doctype
     where d.docid = :docid
      into :fromobj, :throughobj, :toobj, :dtcode;

    if (:dtcode in ('INCOME', 'INCOMEFG')) then
    begin
        whid = :toobj;
        fundobjid = :whid;
    end
    else if (:dtcode = 'COMERETURN') then
    begin
        whid = :toobj;
        fundobjid = coalesce(:throughobj, :toobj);
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEDOC_GETOBJECTSFUND (
    DOCID type of column DOCUMENT.docid
)
returns (
    WHID type of column OBJECT.objid,
    FUNDOBJID type of column OBJECT.objid
)
as
declare variable fromobj type of column OBJECT.objid;
declare variable throughobj type of column OBJECT.objid;
declare variable toobj type of column OBJECT.objid;
declare variable dtCode type of column DOCtype.code ;
begin
    select d.fromobj, d.throughobj, d.toobj, dt.code
      from document d
           left join doctype dt on dt.doctid = d.doctype
     where d.docid = :docid
      into :fromobj, :throughobj, :toobj, :dtcode;

    if (:dtcode in ('INCOME', 'INCOMEFG')) then
    begin
        whid = :toobj;
        fundobjid = :whid;
    end
    else if (:dtcode = 'COMERETURN') then
    begin
        whid = :toobj;
        fundobjid = coalesce(:throughobj, :whid);
    end

    suspend;
end^

SET TERM ; ^



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
declare variable fundobjid type of column OBJECT.objid;
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
        select o.amount,o.wlincomeid,fo.fundobjid
          from core_listwlincomes(:wlid,:palletid,-:amount) o
               left join WH_INCOMEDOC_GETOBJECTSFUND(o.docid) fo on 1=1
          into :amount,:wlincomeid,:fundobjid
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
                values ( :waresid, :productdate, :amount, :fundobjid, 0.000, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, 0.000, :fundobjid, :amount, :taskid);
            end
        end
      end
  end
END^

SET TERM ; ^



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
        select o.amount,o.wlincomeid,fo.fundobjid
          from core_listwlincomes(:wlid,:palletid,-:amount) o
               left join WH_INCOMEDOC_GETOBJECTSFUND(o.docid) fo on 1=1
          into :amount,:wlincomeid,:fundobjid
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
                values ( :waresid, :productdate, :amount, :fundobjid, 0.000, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, 0.000, :fundobjid, :amount, :taskid);
            end
        end
      end
  end
END^

SET TERM ; ^



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
          select tmp.wareslotid,tmp.amount
            from k_wh_siteverify_wareslot_tmp tmp
           where tmp.amount > 0.00001
            into :wlid,:amount
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
                values ( :waresid, :productdate, 0.000, :fundobjid, -:amount, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, -:amount, :fundobjid, 0.000, :taskid);
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
                values ( :waresid, :productdate, :amount, :fundobjid, 0.000, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, 0.000, :fundobjid, :amount, :taskid);
            end
          end
      end
  end
END^

SET TERM ; ^



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
          select tmp.wareslotid,tmp.amount
            from k_wh_siteverify_wareslot_tmp tmp
           where tmp.amount > 0.00001
            into :wlid,:amount
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
                values ( :waresid, :productdate, 0.000, :fundobjid, -:amount, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, -:amount, :fundobjid, 0.000, :taskid);
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
                values ( :waresid, :productdate, :amount, :fundobjid, 0.000, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, 0.000, :fundobjid, :amount, :taskid);
            end
          end
      end
  end
END^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEDOC_GETOBJECTSFUND (
    DOCID type of column DOCUMENT.DOCID)
returns (
    WHID type of column OBJECT.OBJID,
    FUNDOBJID type of column OBJECT.OBJID)
AS
declare variable fromobj type of column OBJECT.objid;
declare variable throughobj type of column OBJECT.objid;
declare variable toobj type of column OBJECT.objid;
declare variable dtCode type of column DOCtype.code ;
begin
    select d.fromobj, d.throughobj, d.toobj, dt.code
      from document d
           left join doctype dt on dt.doctid = d.doctype
     where d.docid = :docid
      into :fromobj, :throughobj, :toobj, :dtcode;

    if (:dtcode in ('INCOME', 'INCOMEFG')) then
    begin
        whid = :toobj;
        fundobjid = :whid;
    end
    else if (:dtcode = 'BUYRETURN') then
    begin
        whid = :toobj;
        fundobjid = coalesce(:throughobj, :whid);
    end

    suspend;
end^

SET TERM ; ^



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
          select tmp.wareslotid,tmp.amount
            from k_wh_siteverify_wareslot_tmp tmp
           where tmp.amount > 0.00001
            into :wlid,:amount
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
                values ( :waresid, :productdate, 0.000, :fundobjid, -:amount, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, -:amount, :fundobjid, 0.000, :taskid);
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
                values ( :waresid, :productdate, :amount, :fundobjid, 0.000, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, 0.000, :fundobjid, :amount, :taskid);
            end
          end
      end
  end
END^

SET TERM ; ^



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
                values ( :waresid, :productdate, 0.000, :fundobjid, -:amount, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, -:amount, :fundobjid, 0.000, :taskid);
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
                values ( :waresid, :productdate, :amount, :fundobjid, 0.000, :taskid);
            end
            else
            begin
                insert into wh_reserve_changes ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
                values ( :waresid, :productdate, 0.000, :fundobjid, :amount, :taskid);
            end
          end
      end
  end
END^

SET TERM ; ^



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

CREATE OR ALTER trigger wh_reserve_changes_bi for wh_reserve_changes
active before insert position 0
as
begin
  if (not exists(select *
                   from wh_reserve_objects o
                  where o.objid = new.objid)) then
    exception exc_wh_reserve 'Указанного объекта нет в списке разрешенных для резервирования!';

  if (new.id is null) then
    new.id = gen_id(gen_wh_reserve_changes_id,1);

  if (new.datetime is NULL) then
    new.datetime = current_timestamp;

  if (new.amountbad is NULL) then
    new.amountbad = 0.000;

  if (abs(new.amount + new.amountbad) < 0.00001) then
   exception exc_wh_reserve 'Резервируемое количество должно быть не нулевым!';
end^

SET TERM ; ^



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

