

SET TERM ^ ;

create procedure WH_TERM_INVENT_STACK_RECALCINFO (
    TASKID type of column WM_TASK.taskid,
    SITEID type of column SITE.siteid,
    CNTPAL type of column site_stack.palcurcnt
)
returns (
    PID type of column PALLET.palletid,
    PNUM type of column PALLET.number,
    PBARCODE type of column PALLET.barcode
)
as
declare variable palcurcnt type of column site_stack.siteid;
declare variable cntpalerr type of column site_stack.siteid;
declare variable cntpalskip type of column site_stack.siteid;
declare variable status type of column wm_task_pallet.status;
begin
    select ss.palcurcnt
      from site_stack ss
     where ss.siteid = :siteid
      into :palcurcnt;

    cntpalerr = :palcurcnt - :cntpal;

    if (:cntpalerr > 0) then
    for
        select p.palletid, p.number, p.barcode
          from pallet p
         where p.siteid = :siteid
         order by p.num descending
          into :pid, :pnum, :pbarcode
    do
    begin
        status = NULL;
        select tp.status
          from wm_task_pallet tp
         where tp.taskid = :taskid
           and tp.palletid = :pid
           and tp.siteid = :siteid
          into :status;

        if (:status = '2') then
        begin
            cntpalskip = :cntpalskip + 1;
            if (:cntpalskip = :cntpalerr) then
                exit;
        end

        if (:status is NULL) then
            suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_STACK_RECALCINFO (
    TASKID type of column WM_TASK.taskid,
    SITEID type of column SITE.siteid,
    CNTPAL type of column site_stack.palcurcnt
)
returns (
    PID type of column PALLET.palletid,
    PNUM type of column PALLET.number,
    PBARCODE type of column PALLET.barcode
)
as
declare variable palcurcnt type of column site_stack.siteid;
declare variable cntpalerr type of column site_stack.siteid;
declare variable cntpalskip type of column site_stack.siteid;
declare variable status type of column wm_task_pallet.status;
begin
    select ss.palcurcnt
      from site_stack ss
     where ss.siteid = :siteid
      into :palcurcnt;

    cntpalerr = :palcurcnt - :cntpal;

    if (:cntpalerr > 0) then
    for
        select p.palletid, p.number, p.barcode
          from pallet p
         where p.siteid = :siteid
         order by p.num descending
          into :pid, :pnum, :pbarcode
    do
    begin
        status = NULL;
        select tp.status
          from wm_task_pallet tp
         where tp.taskid = :taskid
           and tp.palletid = :pid
           and tp.siteid = :siteid
          into :status;

        if (:status = '2') then
        begin
            cntpalskip = :cntpalskip + 1;
            if (:cntpalskip = :cntpalerr) then
                exit;
        end

        if (:status is NULL) then
        begin
            suspend;
            exit;
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_TERM_INVENT_STACK_PALSET (
    TASKID type of column WM_TASK.TASKID,
    SITEID type of column SITE.SITEID,
    WMSESSIONID type of column WM_SESSION.SESSIONID,
    palletid type of column PALLET.palletid,
    isok type of r_flag ='1'
)
as
declare variable objid type of column OBJECT.objid;
declare variable trash_siteid type of column SITE.siteid;
declare variable manid type of column MAN.manid;
begin
  select wms.objid
    from wm_session wms
   where wms.sessionid = :wmsessionid
    into :manid;

  if (:isok = '1') then
  begin
      insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
      values( :taskid, :palletid, :siteid, '1', :manid);
  end
  else
  begin
      select t.infoid
        from wm_task t
       where t.taskid = :taskid
        into :objid;

      select k.sid
        from k_wh_get_trash(:objid) k
        into :trash_siteid;

      if (:trash_siteid is NULL) then
        exception exc_wh_wrongsite 'Корзина не найдена!';

      insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
      values( :taskid, :palletid, :siteid, '0', :manid);

      insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
      values( :taskid, :palletid, :trash_siteid, '2', :manid);
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_STACK_RECALCINFO (
    TASKID type of column WM_TASK.taskid,
    SITEID type of column SITE.siteid,
    CNTPAL type of column site_stack.palcurcnt
)
returns (
    PID type of column PALLET.palletid,
    PNUM type of column PALLET.number,
    PBARCODE type of column PALLET.barcode
)
as
declare variable palcurcnt type of column site_stack.siteid;
declare variable cntpalerr type of column site_stack.siteid;
declare variable cntpalskip type of column site_stack.siteid;
declare variable status type of column wm_task_pallet.status;
begin
    select ss.palcurcnt
      from site_stack ss
     where ss.siteid = :siteid
      into :palcurcnt;

    cntpalerr = :palcurcnt - :cntpal;

    if (:cntpalerr > 0) then
    for
        select p.palletid, p.number, p.barcode
          from pallet p
         where p.siteid = :siteid
         order by p.num descending
          into :pid, :pnum, :pbarcode
    do
    begin
        status = NULL;
        select tp.status
          from wm_task_pallet tp
         where tp.taskid = :taskid
           and tp.palletid = :pid
           and tp.siteid = :siteid
          into :status;

        if (:status = '2') then
        begin
            cntpalskip = :cntpalskip + 1;
            if (:cntpalskip = :cntpalerr) then
                exit;
        end

        if (:status is NULL) then
        begin
            suspend;
            exit;
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_STACK_RECALCINFO (
    TASKID type of column WM_TASK.TASKID,
    SITEID type of column SITE.SITEID,
    CNTPAL type of column SITE_STACK.PALCURCNT)
returns (
    PID type of column PALLET.PALLETID,
    PNUM type of column PALLET.NUMBER,
    PBARCODE type of column PALLET.BARCODE)
AS
declare variable palcurcnt type of column SITE_STACK.PALCURCNT;
declare variable cntpalerr type of column SITE_STACK.PALCURCNT;
declare variable cntpalskip type of column SITE_STACK.PALCURCNT = 0;
declare variable status type of column wm_task_pallet.status;
begin
    select ss.palcurcnt
      from site_stack ss
     where ss.siteid = :siteid
      into :palcurcnt;

    cntpalerr = :palcurcnt - :cntpal;

    if (:cntpalerr > 0) then
    for
        select p.palletid, p.number, p.barcode
          from pallet p
         where p.siteid = :siteid
         order by p.num descending
          into :pid, :pnum, :pbarcode
    do
    begin
        status = NULL;
        select tp.status
          from wm_task_pallet tp
         where tp.taskid = :taskid
           and tp.palletid = :pid
           and tp.siteid = :siteid
          into :status;

        if (:status = '2') then
        begin
            cntpalskip = :cntpalskip + 1;
            if (:cntpalskip = :cntpalerr) then
                exit;
        end

        if (:status is NULL) then
        begin
            suspend;
            exit;
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_STACK_RECALCINFO (
    TASKID type of column WM_TASK.TASKID,
    SITEID type of column SITE.SITEID,
    CNTPAL type of column SITE_STACK.PALCURCNT)
returns (
    PID type of column PALLET.PALLETID,
    PNUM type of column PALLET.NUMBER,
    PBARCODE type of column PALLET.BARCODE)
AS
declare variable palcurcnt type of column SITE_STACK.PALCURCNT;
declare variable cntpalerr type of column SITE_STACK.PALCURCNT;
declare variable cntpalskip type of column SITE_STACK.PALCURCNT = 0;
declare variable status type of column wm_task_pallet.status;
begin
    select ss.palcurcnt
      from site_stack ss
     where ss.siteid = :siteid
      into :palcurcnt;

    cntpalerr = :palcurcnt - :cntpal;

    if (:cntpalerr > 0) then
    for
        select p.palletid, p.number, p.barcode
          from pallet p
         where p.siteid = :siteid
         order by p.num descending
          into :pid, :pnum, :pbarcode
    do
    begin
        status = NULL;
        select tp.status
          from wm_task_pallet tp
         where tp.taskid = :taskid
           and tp.palletid = :pid
           and tp.siteid = :siteid
          into :status;

        if (:status = '0') then
        begin
            cntpalskip = :cntpalskip + 1;
            if (:cntpalskip = :cntpalerr) then
                exit;
        end

        if (:status is NULL) then
        begin
            suspend;
            exit;
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_STACK_PALSET (
    TASKID type of column WM_TASK.TASKID,
    SITEID type of column SITE.SITEID,
    WMSESSIONID type of column WM_SESSION.SESSIONID,
    PALLETID type of column PALLET.PALLETID,
    ISOK type of R_FLAG = '1')
AS
declare variable objid type of column OBJECT.objid;
declare variable trash_siteid type of column SITE.siteid;
declare variable manid type of column MAN.manid;
begin
  select wms.objid
    from wm_session wms
   where wms.sessionid = :wmsessionid
    into :manid;

  if (:isok = '1') then
  begin
      insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
      values( :taskid, :palletid, :siteid, '1', :manid);
  end
  else
  begin
      select t.infoid
        from wm_task t
       where t.taskid = :taskid
        into :objid;

      select k.sid
        from k_wh_get_trash(:objid) k
        into :trash_siteid;

      if (:trash_siteid is NULL) then
        exception exc_wh_wrongsite 'Корзина не найдена!';

      insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
      values( :taskid, :palletid, :siteid, '0', :manid);

      insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
      values( :taskid, :palletid, :trash_siteid, '2', :manid);

      update pallet p
         set p.siteid = :trash_siteid
       where p.palletid = :palletid;
  end
end^

SET TERM ; ^



CREATE TABLE TMP_TASK_SITEPALLET (
    TASKID R_ID NOT NULL,
    SITEID R_ID NOT NULL,
    PALLETID R_ID NOT NULL,
    MANID R_ID NOT NULL,
    DT R_DATETIME NOT NULL,
    STATUS R_STATUS);

ALTER TABLE TMP_TASK_SITEPALLET
ADD CONSTRAINT PK_TMP_TASK_SITEPALLET
PRIMARY KEY (TASKID,SITEID,PALLETID);



ALTER TABLE TMP_TASK_SITEPALLET
ADD CONSTRAINT FK_TMP_TASK_SITEPALLET_TID
FOREIGN KEY (TASKID)
REFERENCES WM_TASK(TASKID)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE TMP_TASK_SITEPALLET
ADD CONSTRAINT FK_TMP_TASK_SITEPALLET_PID
FOREIGN KEY (PALLETID)
REFERENCES PALLET(PALLETID)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE TMP_TASK_SITEPALLET
ADD CONSTRAINT FK_TMP_TASK_SITEPALLET_SID
FOREIGN KEY (SITEID)
REFERENCES SITE(SITEID)
ON DELETE CASCADE
ON UPDATE CASCADE;



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_STACK_PALSET (
    TASKID type of column WM_TASK.TASKID,
    SITEID type of column SITE.SITEID,
    WMSESSIONID type of column WM_SESSION.SESSIONID,
    PALLETID type of column PALLET.PALLETID,
    ISOK type of R_FLAG = '1')
AS
declare variable objid type of column OBJECT.objid;
declare variable trash_siteid type of column SITE.siteid;
declare variable manid type of column MAN.manid;
begin
  select wms.objid
    from wm_session wms
   where wms.sessionid = :wmsessionid
    into :manid;

  insert into tmp_task_sitepallet ( TASKID, SITEID, PALLETID, MANID, STATUS)
  values ( :taskid, :siteid, :palletid, :manid, iif(:isok='1', '1', '0') );

  /*if (:isok = '1') then
  begin
      insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
      values( :taskid, :palletid, :siteid, '1', :manid);
  end
  else
  begin
      select t.infoid
        from wm_task t
       where t.taskid = :taskid
        into :objid;

      select k.sid
        from k_wh_get_trash(:objid) k
        into :trash_siteid;

      if (:trash_siteid is NULL) then
        exception exc_wh_wrongsite 'Корзина не найдена!';

      insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
      values( :taskid, :palletid, :siteid, '0', :manid);

      insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
      values( :taskid, :palletid, :trash_siteid, '2', :manid);

      update pallet p
         set p.siteid = :trash_siteid
       where p.palletid = :palletid;
  end*/
end^

SET TERM ; ^



CREATE EXCEPTION EXC_WH_WRONGSTATUS 'Не верный статус';



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_STACKDO (
    TASKID type of column WM_TASK.TASKID,
    SITEID type of column SITE.SITEID,
    WMSESSIONID type of column WM_SESSION.SESSIONID,
    CNT1 type of column SITE_STACK.PALCURCNT)
AS
declare variable palcurcnt type of column site_stack.palcurcnt;
declare variable manid type of column man.manid;
declare variable whid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable amount type of column WARESLOTITEM.amount;
declare variable trash_siteid type of column SITE.siteid;
declare variable palletid type of column PALLET.palletid;
declare variable palletnum type of column PALLET.num;
declare variable palletstatus type of column tmp_task_sitepallet.status;
declare variable dt type of column tmp_task_sitepallet.dt;
declare variable qplan type of column wareslotitem.amount;
declare variable qfact type of column wareslotitem.amount;
declare variable twqplan type of column wareslotitem.amount;
declare variable twqfact type of column wareslotitem.amount;
declare variable taskwaresid type of column WM_TASK_WARES.taskwaresid;
begin
    select wms.objid
      from wm_session wms
     where wms.sessionid = :wmsessionid
      into :manid;

    select ss.palcurcnt, ss.waresid
      from site_stack ss
     where ss.siteid = :siteid
      into :palcurcnt, :waresid;

    select t.infoid
      from wm_task t
     where t.taskid = :taskid
      into :whid;

    select k.sid
      from k_wh_get_trash(:whid) k
      into :trash_siteid;

    if (:trash_siteid is NULL) then
        exception exc_wh_wrongsite 'Корзина не найдена!';

    qplan = 0.000;
    qfact= 0.000;
    for
        select p.palletid, p.num, coalesce(t.status, '1'), coalesce(t.dt, current_timestamp)
          from pallet p
               left join tmp_task_sitepallet t
                 on t.taskid = :taskid and t.palletid = p.palletid and t.siteid = :siteid
         where p.siteid = :siteid
         order by t.status ascending --'0,1'
          into :palletid, :palletnum, :palletstatus, :dt
    do
    begin
        amount = 0.000;
        select sum(wli.amount)
          from pallet p
               left join wareslotitem wli
                    left join wareslot wl on wl.wlotid = wli.wlotid
                 on wli.palletid = p.palletid
         where p.siteid = :siteid
           and p.status = '1'
           and wl.waresid = :waresid
          into :amount;

        if (:amount is NULL) then
            amount = 0.000;

        qplan = :qplan + :amount;
        if (:palletstatus = '1') then
        begin
            insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID, LASTDATE)
            values (:taskid, :palletid, :siteid, '1', :manid, :dt);

            qfact = :qfact + :amount;
        end
        else if (:palletstatus = '0') then
        begin
            update pallet p
               set p.num = p.num - 1
             where p.siteid = :siteid and p.num between (:palletnum + 1) and :palcurcnt;
    
            update pallet p
               set p.num = :palcurcnt
             where p.palletid = :palletid;
    
            palcurcnt = :palcurcnt - 1;

            insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID, LASTDATE)
            values( :taskid, :palletid, :siteid, '0', :manid, :DT);
    
            insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID, LASTDATE)
            values( :taskid, :palletid, :trash_siteid, '2', :manid, :DT);
    
            update pallet p
               set p.siteid = :trash_siteid
             where p.palletid = :palletid;
        end
        else
        begin
            exception exc_wh_wrongstatus;
        end
    end

    taskwaresid = NULL;
    select tw.taskwaresid, tw.quantity, tw.scanquant
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.waresid = :waresid
       and tw.siteid = :siteid
      into :taskwaresid, :twqplan, :twqfact;

    -- QUANTITY - Fact
    -- SCANQUANT - Plan
    if (:taskwaresid is NULL) then
        insert into wm_task_wares ( TASKID, WARESID, QUANTITY, SCANQUANT, SITEID, STATUS, ENDTIME, WM_SESSIONID)
        values ( :taskid, :waresid, :qfact, :qplan, :siteid, '2', current_timestamp, :wmsessionid);
    else
        update wm_task_wares tw
           set tw.quantity = :qfact,
               tw.scanquant = :qplan,
               tw.status = '2',
               tw.wm_sessionid = :wmsessionid,
               tw.endtime = current_timestamp
         where tw.taskwaresid = :taskwaresid;

    select tw.taskwaresid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.waresid = :waresid
       and tw.siteid is NULL
      into :taskwaresid;

    if (:taskwaresid is NULL) then
        insert into wm_task_wares ( TASKID, WARESID, QUANTITY, SCANQUANT, SITEID, STATUS, ENDTIME, WM_SESSIONID)
        values ( :taskid, :waresid, :qfact, :qplan, NULL, '2', current_timestamp, :wmsessionid);
    else
        update wm_task_wares tw
           set tw.quantity = coalesce(tw.quantity, 0.000) - coalesce(:twqfact, 0.000) + :qfact,
               tw.scanquant = coalesce(tw.scanquant, 0.000) - coalesce(:twqplan, 0.000) + :qplan,
               tw.status = '2',
               tw.wm_sessionid = :wmsessionid,
               tw.endtime = current_timestamp
         where tw.taskwaresid = :taskwaresid;

    update wm_task_site ts
       set ts.status = '2'
     where ts.taskid = :taskid
       and ts.siteid = :siteid
       and ts.manid = :manid
       and ts.status = '1';

    delete from tmp_task_sitepallet t
     where t.taskid = :taskid
       and t.siteid = :siteid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_STACKDO (
    TASKID type of column WM_TASK.TASKID,
    SITEID type of column SITE.SITEID,
    WMSESSIONID type of column WM_SESSION.SESSIONID
)
AS
declare variable palcurcnt type of column site_stack.palcurcnt;
declare variable manid type of column man.manid;
declare variable whid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable amount type of column WARESLOTITEM.amount;
declare variable trash_siteid type of column SITE.siteid;
declare variable palletid type of column PALLET.palletid;
declare variable palletnum type of column PALLET.num;
declare variable palletstatus type of column tmp_task_sitepallet.status;
declare variable dt type of column tmp_task_sitepallet.dt;
declare variable qplan type of column wareslotitem.amount;
declare variable qfact type of column wareslotitem.amount;
declare variable twqplan type of column wareslotitem.amount;
declare variable twqfact type of column wareslotitem.amount;
declare variable taskwaresid type of column WM_TASK_WARES.taskwaresid;
begin
    select wms.objid
      from wm_session wms
     where wms.sessionid = :wmsessionid
      into :manid;

    select ss.palcurcnt, ss.waresid
      from site_stack ss
     where ss.siteid = :siteid
      into :palcurcnt, :waresid;

    select t.infoid
      from wm_task t
     where t.taskid = :taskid
      into :whid;

    select k.sid
      from k_wh_get_trash(:whid) k
      into :trash_siteid;

    if (:trash_siteid is NULL) then
        exception exc_wh_wrongsite 'Корзина не найдена!';

    qplan = 0.000;
    qfact= 0.000;
    for
        select p.palletid, p.num, coalesce(t.status, '1'), coalesce(t.dt, current_timestamp)
          from pallet p
               left join tmp_task_sitepallet t
                 on t.taskid = :taskid and t.palletid = p.palletid and t.siteid = :siteid
         where p.siteid = :siteid
         order by t.status ascending --'0,1'
          into :palletid, :palletnum, :palletstatus, :dt
    do
    begin
        amount = 0.000;
        select sum(wli.amount)
          from pallet p
               left join wareslotitem wli
                    left join wareslot wl on wl.wlotid = wli.wlotid
                 on wli.palletid = p.palletid
         where p.siteid = :siteid
           and p.status = '1'
           and wl.waresid = :waresid
          into :amount;

        if (:amount is NULL) then
            amount = 0.000;

        qplan = :qplan + :amount;
        if (:palletstatus = '1') then
        begin
            insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID, LASTDATE)
            values (:taskid, :palletid, :siteid, '1', :manid, :dt);

            qfact = :qfact + :amount;
        end
        else if (:palletstatus = '0') then
        begin
            update pallet p
               set p.num = p.num - 1
             where p.siteid = :siteid and p.num between (:palletnum + 1) and :palcurcnt;
    
            update pallet p
               set p.num = :palcurcnt
             where p.palletid = :palletid;
    
            palcurcnt = :palcurcnt - 1;

            insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID, LASTDATE)
            values( :taskid, :palletid, :siteid, '0', :manid, :DT);
    
            insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID, LASTDATE)
            values( :taskid, :palletid, :trash_siteid, '2', :manid, :DT);
    
            update pallet p
               set p.siteid = :trash_siteid
             where p.palletid = :palletid;
        end
        else
        begin
            exception exc_wh_wrongstatus;
        end
    end

    taskwaresid = NULL;
    select tw.taskwaresid, tw.quantity, tw.scanquant
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.waresid = :waresid
       and tw.siteid = :siteid
      into :taskwaresid, :twqplan, :twqfact;

    -- QUANTITY - Fact
    -- SCANQUANT - Plan
    if (:taskwaresid is NULL) then
        insert into wm_task_wares ( TASKID, WARESID, QUANTITY, SCANQUANT, SITEID, STATUS, ENDTIME, WM_SESSIONID)
        values ( :taskid, :waresid, :qfact, :qplan, :siteid, '2', current_timestamp, :wmsessionid);
    else
        update wm_task_wares tw
           set tw.quantity = :qfact,
               tw.scanquant = :qplan,
               tw.status = '2',
               tw.wm_sessionid = :wmsessionid,
               tw.endtime = current_timestamp
         where tw.taskwaresid = :taskwaresid;

    select tw.taskwaresid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.waresid = :waresid
       and tw.siteid is NULL
      into :taskwaresid;

    if (:taskwaresid is NULL) then
        insert into wm_task_wares ( TASKID, WARESID, QUANTITY, SCANQUANT, SITEID, STATUS, ENDTIME, WM_SESSIONID)
        values ( :taskid, :waresid, :qfact, :qplan, NULL, '2', current_timestamp, :wmsessionid);
    else
        update wm_task_wares tw
           set tw.quantity = coalesce(tw.quantity, 0.000) - coalesce(:twqfact, 0.000) + :qfact,
               tw.scanquant = coalesce(tw.scanquant, 0.000) - coalesce(:twqplan, 0.000) + :qplan,
               tw.status = '2',
               tw.wm_sessionid = :wmsessionid,
               tw.endtime = current_timestamp
         where tw.taskwaresid = :taskwaresid;

    update wm_task_site ts
       set ts.status = '2'
     where ts.taskid = :taskid
       and ts.siteid = :siteid
       and ts.manid = :manid
       and ts.status = '1';

    delete from tmp_task_sitepallet t
     where t.taskid = :taskid
       and t.siteid = :siteid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_JOINSITE (
    TID type of column WM_TASK.TASKID,
    SID type of column SITE.SITEID,
    WMSESID type of column WM_SESSION.SESSIONID)
returns (
    SPCODE type of column SITESPECIES.CODE)
AS
declare variable MANID type of column MAN.manid;
begin
  select s.objid
    from wm_session s
   where s.sessionid = :wmsesid
         and s.disconnecttime is null
    into :manid;

  if (:manid is null) then
    exception exc_k_common 'Пользователь не найден!';

  if (exists(
    select *
      from wm_task_site ts
     where ts.taskid = :tid
           and ts.siteid = :sid
           and ts.manid <> :manid
           and ts.status = '1'
  )) then
    exception exc_k_common 'МП инвентаризируется другим сотрудником!';

  if (exists(
    select *
      from wm_task_site ts
     where ts.taskid = :tid
           and ts.siteid <> :sid
           and ts.manid = :manid
           and ts.status = '1'
  ))
  then
    exception exc_k_common 'Есть незавершенное МП!';
  else
  begin
    if (not exists(   -- проверка при работе из ПК
      select *
      from wm_task_site ts
     where ts.taskid = :tid
           and ts.siteid = :sid
           and ts.manid = :manid
           and ts.status = '1'
    )) then
      insert into wm_task_site(taskid,siteid,status,manid,begintime)
      values (:tid,:sid,'1',:manid,current_timestamp);

      delete from tmp_task_sitepallet t
       where t.taskid = :tid and t.siteid = :sid;
  end

  select sp.code
    from site s
         left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
   where s.siteid = :sid
    into :spCode;

  suspend;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger tmp_task_sitepallet_bi0 for tmp_task_sitepallet
active before insert position 0
AS
begin
    if (new.dt is NULL) then
        new.dt = current_timestamp;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_STACK_PALSET (
    TASKID type of column WM_TASK.TASKID,
    SITEID type of column SITE.SITEID,
    WMSESSIONID type of column WM_SESSION.SESSIONID,
    PALLETID type of column PALLET.PALLETID,
    ISOK type of R_FLAG = '1')
AS
declare variable objid type of column OBJECT.objid;
declare variable trash_siteid type of column SITE.siteid;
declare variable manid type of column MAN.manid;
begin
  select wms.objid
    from wm_session wms
   where wms.sessionid = :wmsessionid
    into :manid;

  insert into tmp_task_sitepallet ( TASKID, SITEID, PALLETID, MANID, STATUS)
  values ( :taskid, :siteid, :palletid, :manid, iif(:isok='1', '1', '0') );

  /*if (:isok = '1') then
  begin
      insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
      values( :taskid, :palletid, :siteid, '1', :manid);
  end
  else
  begin
      select t.infoid
        from wm_task t
       where t.taskid = :taskid
        into :objid;

      select k.sid
        from k_wh_get_trash(:objid) k
        into :trash_siteid;

      if (:trash_siteid is NULL) then
        exception exc_wh_wrongsite 'Корзина не найдена!';

      insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
      values( :taskid, :palletid, :siteid, '0', :manid);

      insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
      values( :taskid, :palletid, :trash_siteid, '2', :manid);

      update pallet p
         set p.siteid = :trash_siteid
       where p.palletid = :palletid;
  end*/
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_STACK_RECALCINFO (
    TASKID type of column WM_TASK.TASKID,
    SITEID type of column SITE.SITEID,
    CNTPAL type of column SITE_STACK.PALCURCNT)
returns (
    PID type of column PALLET.PALLETID,
    PNUM type of column PALLET.NUMBER,
    PBARCODE type of column PALLET.BARCODE)
AS
declare variable palcurcnt type of column SITE_STACK.PALCURCNT;
declare variable cntpalerr type of column SITE_STACK.PALCURCNT;
declare variable cntpalskip type of column SITE_STACK.PALCURCNT = 0;
declare variable status type of column wm_task_pallet.status;
begin
    select ss.palcurcnt
      from site_stack ss
     where ss.siteid = :siteid
      into :palcurcnt;

    cntpalerr = :palcurcnt - :cntpal;

    if (:cntpalerr > 0) then
    for
        select p.palletid, p.number, p.barcode
          from pallet p
         where p.siteid = :siteid
         order by p.num descending
          into :pid, :pnum, :pbarcode
    do
    begin
        status = NULL;
        select tp.status
          from tmp_task_sitepallet tp
         where tp.taskid = :taskid
           and tp.palletid = :pid
           and tp.siteid = :siteid
          into :status;

        if (:status = '0') then
        begin
            cntpalskip = :cntpalskip + 1;
            if (:cntpalskip = :cntpalerr) then
                exit;
        end

        if (:status is NULL) then
        begin
            suspend;
            exit;
        end
    end
end^

SET TERM ; ^

