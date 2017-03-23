

SET TERM ^ ;

CREATE OR ALTER procedure WH_DOCFREESEL_SAVE (
    WMSESID type of R_ID,
    TASKID type of R_ID,
    PALLETID type of R_ID,
    WUID type of R_ID,
    WARESLOTS varchar(1023),
    AMOUNTS varchar(1023),
    DBEG type of R_DATETIME = current_timestamp)
AS
declare variable wordwlotid varchar(1024);
declare variable wordamount varchar(1024);
declare variable amount double precision;
declare variable waresid type of r_id;
declare variable siteid type of r_id;
declare variable wlid type of r_id;
declare variable wufactor type of r_id;
declare variable twid type of r_id;
declare variable i smallint;
declare variable wlincomeid type of r_id;
declare variable pallettype type of r_flag;
declare variable reserveobjid type of column OBJECT.objid;
declare variable ptCode type of column pallet_type.code;
declare variable docid type of column document.docid;
declare variable productdate type of column WH_RESERVE.productdate;
BEGIN
  if (:dbeg is null) then dbeg = current_timestamp;

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
        exception exc_wh_wrongamount;


  amount = NULL;
  select sum(tmp.amount)
    from k_wh_siteverify_wareslot_tmp tmp
   where tmp.amount > 0.00001
    into :amount;
  if (:amount is NULL) then amount = 0.0000;

  if (:amount < 0.00001) then
        exception exc_wh_emptyamount;

  siteid = NULL;
  select p.siteid, p.pallettype, pt.code
    from pallet p
         left join pallet_type pt on pt.id = p.ptypeid
   where p.palletid = :palletid
     and p.pallettype <> '2'
    into :siteid, :pallettype, :ptCode;
  if (:siteid is NULL) then
    exception exc_wh_wrongpallet;

  select ro.objid,d.docid
    from wm_task t
         left join document d
              left join WH_GET_RESERVEOBJ(coalesce(d.throughobj, d.fromobj)) ro on 1=1
           on d.docid = t.docid
   where t.taskid = :taskid
    into :reserveobjid,:docid;

  if (:ptCode = 'CR') then
  begin
    if (exists(select *
                 from k_wh_siteverify_wareslot_tmp w
                      left join wareslot wl on wl.wlotid = w.wareslotid
                      left join wh_reserve r
                        on r.waresid = wl.waresid and r.productdate = wl.productdate and r.objid = :reserveobjid
                where w.amount - coalesce(r.amountbad,0.000) > 0.0001
    )) then
        exception exc_wh_reserve 'Не достаточно резерва';
  end
  else
  begin
    if (exists(select *
                 from k_wh_siteverify_wareslot_tmp w
                      left join wareslot wl on wl.wlotid = w.wareslotid
                      left join wh_reserve r
                        on r.waresid = wl.waresid and r.productdate = wl.productdate and r.objid = :reserveobjid
                where w.amount - coalesce(r.amountfree,0.000) > 0.0001
    )) then
        exception exc_wh_reserve 'Не достаточно резерва';
  end



  execute procedure wh_session_chkpallet(:wmsesid,:palletid,NULL);

  begin
      if (:pallettype<>'1') then
        insert into wm_task_pallet(taskid,palletid,siteid,status)
        values (:taskid,:palletid,:siteid,'1');

      select tw.taskwaresid
        from wm_task_wares tw
       where tw.taskid = :taskid
         and tw.waresid = :waresid
        into :twid;
      if (:twid is NULL) then
          insert into wm_task_wares(taskid, waresid, status, quantity, begintime, endtime, wm_sessionid)
          values(:taskid, :waresid, '2', :amount, :dbeg, current_timestamp, :wmsesid)
          returning taskwaresid
          into :twid;
      else
        update wm_task_wares tw
           set tw.begintime = coalesce(tw.begintime,:dbeg),
               tw.endtime = current_timestamp,
               tw.status = '2',tw.wm_sessionid = :wmsesid,
               tw.quantity = coalesce(tw.quantity,0.0000)+:amount
         where tw.taskwaresid = :twid;

      for
          select tmp.wareslotid,tmp.amount, wl.waresid, wl.productdate
            from k_wh_siteverify_wareslot_tmp tmp
                 left join wareslot wl on wl.wlotid = tmp.wareslotid
           where tmp.amount > 0.00001
            into :wlid,:amount,:waresid, :productdate
      do
      FOR
        select o.amount,o.wlincomeid
          from core_listwlincomes(:wlid,:palletid,-:amount) o
          into :amount,:wlincomeid
      do
      begin
          if (:ptcode = 'CR') then
              insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
              values ( :docid,:waresid, :productdate, 0.00, :reserveobjid, -:amount, :taskid);
          else
              insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
              values ( :docid,:waresid, :productdate, -:amount, :reserveobjid, 0.000, :taskid);

          -- Процедура вернет расходные количества, поэтому при приходовании знак наоборот
          insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
          values(:twid,:wlid,:palletid,:amount,'1',:wlincomeid,:wmsesid);
      end
  end
END^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_DOCFREESEL_SAVE (
    WMSESID type of R_ID,
    TASKID type of R_ID,
    PALLETID type of R_ID,
    WUID type of R_ID,
    WARESLOTS varchar(1023),
    AMOUNTS varchar(1023),
    DBEG type of R_DATETIME = current_timestamp)
AS
declare variable wordwlotid varchar(1024);
declare variable wordamount varchar(1024);
declare variable amount double precision;
declare variable waresid type of r_id;
declare variable siteid type of r_id;
declare variable wlid type of r_id;
declare variable wufactor type of r_id;
declare variable twid type of r_id;
declare variable i smallint;
declare variable wlincomeid type of r_id;
declare variable pallettype type of r_flag;
declare variable reserveobjid type of column OBJECT.objid;
declare variable ptCode type of column pallet_type.code;
declare variable docid type of column document.docid;
declare variable productdate type of column WH_RESERVE.productdate;
BEGIN
  if (:dbeg is null) then dbeg = current_timestamp;

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
        exception exc_wh_wrongamount;


  amount = NULL;
  select sum(tmp.amount)
    from k_wh_siteverify_wareslot_tmp tmp
   where tmp.amount > 0.00001
    into :amount;
  if (:amount is NULL) then amount = 0.0000;

  if (:amount < 0.00001) then
        exception exc_wh_emptyamount;

  siteid = NULL;
  select p.siteid, p.pallettype, pt.code
    from pallet p
         left join pallet_type pt on pt.id = p.ptypeid
   where p.palletid = :palletid
     and p.pallettype <> '2'
    into :siteid, :pallettype, :ptCode;
  if (:siteid is NULL) then
    exception exc_wh_wrongpallet;

  select ro.objid,d.docid
    from wm_task t
         left join document d
              left join WH_GET_RESERVEOBJ(coalesce(d.throughobj, d.fromobj)) ro on 1=1
           on d.docid = t.docid
   where t.taskid = :taskid
    into :reserveobjid,:docid;

  if (:ptCode = 'CR') then
  begin
    if (exists(select *
                 from k_wh_siteverify_wareslot_tmp w
                      left join wareslot wl on wl.wlotid = w.wareslotid
                      left join wh_reserve r
                        on r.waresid = wl.waresid and r.productdate = wl.productdate and r.objid = :reserveobjid
                where w.amount - coalesce(r.amountbad,0.000) > 0.0001
    )) then
        exception exc_wh_reserve 'Не достаточно резерва';
  end
  else
  begin
    if (exists(select *
                 from k_wh_siteverify_wareslot_tmp w
                      left join wareslot wl on wl.wlotid = w.wareslotid
                      left join wh_reserve r
                        on r.waresid = wl.waresid and r.productdate = wl.productdate and r.objid = :reserveobjid
                where w.amount - coalesce(r.amountfree,0.000) > 0.0001
    )) then
        exception exc_wh_reserve 'Не достаточно резерва';
  end



  execute procedure wh_session_chkpallet(:wmsesid,:palletid,NULL);

  begin
      if (:pallettype<>'1') then
        insert into wm_task_pallet(taskid,palletid,siteid,status)
        values (:taskid,:palletid,:siteid,'1');

      select tw.taskwaresid
        from wm_task_wares tw
       where tw.taskid = :taskid
         and tw.waresid = :waresid
        into :twid;
      if (:twid is NULL) then
          insert into wm_task_wares(taskid, waresid, status, quantity, begintime, endtime, wm_sessionid)
          values(:taskid, :waresid, '2', :amount, :dbeg, current_timestamp, :wmsesid)
          returning taskwaresid
          into :twid;
      else
        update wm_task_wares tw
           set tw.begintime = coalesce(tw.begintime,:dbeg),
               tw.endtime = current_timestamp,
               tw.status = '2',tw.wm_sessionid = :wmsesid,
               tw.quantity = coalesce(tw.quantity,0.0000)+:amount
         where tw.taskwaresid = :twid;

      for
          select tmp.wareslotid,tmp.amount, wl.waresid, wl.productdate
            from k_wh_siteverify_wareslot_tmp tmp
                 left join wareslot wl on wl.wlotid = tmp.wareslotid
           where tmp.amount > 0.00001
            into :wlid,:amount,:waresid, :productdate
      do
      FOR
        select o.amount,o.wlincomeid
          from core_listwlincomes(:wlid,:palletid,-:amount) o
          into :amount,:wlincomeid
      do
      begin
          if (:ptcode = 'CR') then
              insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
              values ( :docid,:waresid, :productdate, 0.00, :reserveobjid, :amount, :taskid);
          else
              insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
              values ( :docid,:waresid, :productdate, :amount, :reserveobjid, 0.000, :taskid);

          -- Процедура вернет расходные количества, поэтому при приходовании знак наоборот
          insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
          values(:twid,:wlid,:palletid,:amount,'1',:wlincomeid,:wmsesid);
      end
  end
END^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_DOCFREESEL_TASK_FUNDINFO (
    TASKID type of column WM_TASK.taskid
)
returns (
    DOCID type of column DOCUMENT.docid,
    FUNDOBJID type of column OBJECT.objid
)
as
begin
  select ro.objid,d.docid
    from wm_task t
         left join document d
              left join WH_GET_RESERVEOBJ(coalesce(d.throughobj, d.fromobj)) ro on 1=1
           on d.docid = t.docid
   where t.taskid = :taskid
    into :fundobjid,:docid;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_DOCFREESEL_SAVE (
    WMSESID type of R_ID,
    TASKID type of R_ID,
    PALLETID type of R_ID,
    WUID type of R_ID,
    WARESLOTS varchar(1023),
    AMOUNTS varchar(1023),
    DBEG type of R_DATETIME = current_timestamp)
AS
declare variable wordwlotid varchar(1024);
declare variable wordamount varchar(1024);
declare variable amount double precision;
declare variable waresid type of r_id;
declare variable siteid type of r_id;
declare variable wlid type of r_id;
declare variable wufactor type of r_id;
declare variable twid type of r_id;
declare variable i smallint;
declare variable wlincomeid type of r_id;
declare variable pallettype type of r_flag;
declare variable reserveobjid type of column OBJECT.objid;
declare variable ptCode type of column pallet_type.code;
declare variable docid type of column document.docid;
declare variable productdate type of column WH_RESERVE.productdate;
BEGIN
  if (:dbeg is null) then dbeg = current_timestamp;

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
        exception exc_wh_wrongamount;


  amount = NULL;
  select sum(tmp.amount)
    from k_wh_siteverify_wareslot_tmp tmp
   where tmp.amount > 0.00001
    into :amount;
  if (:amount is NULL) then amount = 0.0000;

  if (:amount < 0.00001) then
        exception exc_wh_emptyamount;

  siteid = NULL;
  select p.siteid, p.pallettype, pt.code
    from pallet p
         left join pallet_type pt on pt.id = p.ptypeid
   where p.palletid = :palletid
     and p.pallettype <> '2'
    into :siteid, :pallettype, :ptCode;
  if (:siteid is NULL) then
    exception exc_wh_wrongpallet;

  select t.fundobjid,t.docid
    from WH_DOCFREESEL_TASK_FUNDINFO(:taskid) t
    into :reserveobjid,:docid;

  if (:ptCode = 'CR') then
  begin
    if (exists(select *
                 from k_wh_siteverify_wareslot_tmp w
                      left join wareslot wl on wl.wlotid = w.wareslotid
                      left join wh_reserve r
                        on r.waresid = wl.waresid and r.productdate = wl.productdate and r.objid = :reserveobjid
                where w.amount - coalesce(r.amountbad,0.000) > 0.0001
    )) then
        exception exc_wh_reserve 'Не достаточно резерва';
  end
  else
  begin
    if (exists(select *
                 from k_wh_siteverify_wareslot_tmp w
                      left join wareslot wl on wl.wlotid = w.wareslotid
                      left join wh_reserve r
                        on r.waresid = wl.waresid and r.productdate = wl.productdate and r.objid = :reserveobjid
                where w.amount - coalesce(r.amountfree,0.000) > 0.0001
    )) then
        exception exc_wh_reserve 'Не достаточно резерва';
  end



  execute procedure wh_session_chkpallet(:wmsesid,:palletid,NULL);

  begin
      if (:pallettype<>'1') then
        insert into wm_task_pallet(taskid,palletid,siteid,status)
        values (:taskid,:palletid,:siteid,'1');

      select tw.taskwaresid
        from wm_task_wares tw
       where tw.taskid = :taskid
         and tw.waresid = :waresid
        into :twid;
      if (:twid is NULL) then
          insert into wm_task_wares(taskid, waresid, status, quantity, begintime, endtime, wm_sessionid)
          values(:taskid, :waresid, '2', :amount, :dbeg, current_timestamp, :wmsesid)
          returning taskwaresid
          into :twid;
      else
        update wm_task_wares tw
           set tw.begintime = coalesce(tw.begintime,:dbeg),
               tw.endtime = current_timestamp,
               tw.status = '2',tw.wm_sessionid = :wmsesid,
               tw.quantity = coalesce(tw.quantity,0.0000)+:amount
         where tw.taskwaresid = :twid;

      for
          select tmp.wareslotid,tmp.amount, wl.waresid, wl.productdate
            from k_wh_siteverify_wareslot_tmp tmp
                 left join wareslot wl on wl.wlotid = tmp.wareslotid
           where tmp.amount > 0.00001
            into :wlid,:amount,:waresid, :productdate
      do
      FOR
        select o.amount,o.wlincomeid
          from core_listwlincomes(:wlid,:palletid,-:amount) o
          into :amount,:wlincomeid
      do
      begin
          if (:ptcode = 'CR') then
              insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
              values ( :docid,:waresid, :productdate, 0.00, :reserveobjid, :amount, :taskid);
          else
              insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
              values ( :docid,:waresid, :productdate, :amount, :reserveobjid, 0.000, :taskid);

          -- Процедура вернет расходные количества, поэтому при приходовании знак наоборот
          insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
          values(:twid,:wlid,:palletid,:amount,'1',:wlincomeid,:wmsesid);
      end
  end
END^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_DOCFREESEL_PALWARLOTS (
    TASKID type of column WM_TASK.taskid,
    PALLETID type of column PALLET.palletid,
    WARESID type of column GWARES.waresid)
returns (
    WLOTID type of column WARESLOT.wlotid,
    PRODUCTDATE type of R_DATE,
    WLNUMBER type of column WARESLOT.wlnumber,
    AMOUNT type of column WARESLOTITEM.amount,
    RESERVE type of column WH_RESERVE.amount
)
AS
declare variable reserveobjid type of column OBJECT.objid;
begin
  select t.fundobjid
    from WH_DOCFREESEL_TASK_FUNDINFO(:taskid) t
    into :reserveobjid;

  For
    select wl.wlotid,min(wl.productdate),min(wl.wlnumber),sum(wli.amount)
      from wareslotitem wli
           left join wareslot wl on wl.wlotid = wli.wlotid
     where wli.palletid = :palletid
       and wl.waresid = :waresid
     group by wl.wlotid
      into :wlotid,:productdate,:wlnumber,:amount
  do
    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_DOCFREESEL_PALWARLOTS (
    TASKID type of column WM_TASK.taskid,
    PALLETID type of column PALLET.palletid,
    WARESID type of column GWARES.waresid)
returns (
    WLOTID type of column WARESLOT.wlotid,
    PRODUCTDATE type of R_DATE,
    WLNUMBER type of column WARESLOT.wlnumber,
    AMOUNT type of column WARESLOTITEM.amount,
    RESERVE type of column WH_RESERVE.amount
)
AS
declare variable reserveobjid type of column OBJECT.objid;
declare variable ptCode type of column PALLET_TYPE.code;
begin
  select t.fundobjid
    from WH_DOCFREESEL_TASK_FUNDINFO(:taskid) t
    into :reserveobjid;

  select pt.code
    from pallet p
         left join pallet_type pt on pt.id = p.ptypeid
   where p.palletid = :palletid
    into :ptCode;

  For
    select wl.wlotid,min(wl.productdate),min(wl.wlnumber),sum(wli.amount),
           min(iif(:ptCode='CR', r.amountbad, r.amountfree))
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

CREATE OR ALTER procedure WH_DOCFREESEL_TASKWARES_PALCANC (
    TASKID type of column WM_TASK.taskid,
    WARESID type of column GWARES.waresid,
    PALLETID type of column PALLET.palletid,
    WLOTID type of column WARESLOT.wlotid,
    WMSESID type of column wm_session.sessionid
)
AS
declare variable docid type of column DOCUMENT.docid;
declare variable twid type of column WM_TASK_WARES.taskwaresid;
declare variable productdate type of R_DATE;
declare variable wlincomeid type of column WARESLOTINCOMES.id;
declare variable quantity r_double;
declare variable qsum r_double;
declare variable reserveobjid type of column OBJECT.objid;
declare variable ptCode type of column PALLET_TYPE.code;
begin
     select tw.taskwaresid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.waresid = :waresid
      into :twid;

    qsum = 0.0000;
    for
        select tl.wlincomeid,sum(-tl.quantity)
          from wm_task_lot tl
         where tl.taskwaresid = :twid
           and tl.wlotid = :wlotid
           and tl.palletid = :palletid
         group by tl.wlincomeid
        having abs(sum(-tl.quantity))>0.0001
          into :wlincomeid,:quantity
     do
     begin
        insert into wm_task_lot(taskwaresid,wlotid,palletid,wlincomeid,chgwli,quantity,wm_sessionid)
        values (:twid,:wlotid,:palletid,:wlincomeid,'1',:quantity,:wmsesid);
        qsum = :qsum + :quantity;
     end

     select wl.productdate
       from wareslot wl
      where wl.wlotid = :wlotid
       into :productdate;

     select t.fundobjid,t.docid
       from WH_DOCFREESEL_TASK_FUNDINFO(:taskid) t
       into :reserveobjid,:docid;

     select pt.code
       from pallet p
            left join pallet_type pt on pt.id = p.ptypeid
      where p.palletid = :palletid
       into :ptCode;

     if (:ptcode = 'CR') then
         insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
         values ( :docid,:waresid, :productdate, 0.00, :reserveobjid, :qsum, :taskid);
     else
         insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD, TASKID)
         values ( :docid,:waresid, :productdate, :qsum, :reserveobjid, 0.000, :taskid);

     update wm_task_wares tw
        set tw.quantity = tw.quantity - :qsum,
            tw.endtime = current_timestamp,tw.status = '2',tw.wm_sessionid = :wmsesid
      where tw.taskwaresid = :twid;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_U3S_DOCFREESEL_TSTCHG (
    TASKID type of R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable TTCODE type of R_CODE;
declare variable DOCID type of R_ID64;
begin
    select tt.code,t.docid
      from wm_task t
           left join wm_tasktype tt on tt.tasktypeid=t.tasktypeid
           left join wm_taskmethod tm on tm.methodid = t.taskmethodid
     where t.taskid = :taskid
      into :ttcode,:docid;

    if (:ttcode <> 'DOCFREESEL') then
        exception exc_k_wrongtasktype;

    if (:newstat = '2' and :oldstat<>'2') then
    begin
        update document d
           set d.status = '2'
         where d.docid = :docid and d.status<>'2';
    end
end^

SET TERM ; ^

