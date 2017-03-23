

SET TERM ^ ;

CREATE OR ALTER procedure K_WH_INVENT_TASKPALLET (
    TASKID type of column WM_TASK.taskid)
returns (
    SID type of column SITE.siteid,
    PID type of column PALLET.palletid,
    SITEID_ROW type of column SITE.siteid,
    IS_PALLET_INVENT type of R_BOOL,
    IS_SITE_INVENT type of R_BOOL)
AS
declare variable SITEID type of column SITE.siteid;
declare variable OBJID type of column OBJECT.objid;
declare variable ZONEID type of column sitezone.zoneid;
declare variable SS_ROW type of column sitespecies.sitespeciesid;
declare variable SS_L type of column sitespecies.sitespeciesid;
declare variable ss_stack type of column sitespecies.sitespeciesid;
declare variable SSID type of column sitespecies.sitespeciesid;
begin
  select t.infoid, t.zoneid
    from wm_task t
   where t.taskid = :taskid
    into :objid, :zoneid;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'R'
    into :ss_row;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'L'
    into :ss_l;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'STACK'
    into :ss_stack;

  -- по рядам
  for
    select s.siteid
      from site s
           left join sitezone_items szi on s.siteid = szi.siteid
     where szi.zoneid = :zoneid
           and s.sitespeciesid = :ss_row
      into :siteid_row do
  begin

    for
      select sc.sid, s.sitespeciesid
        from k_site_children(:siteid_row,null,'1') sc
             left join site s on s.siteid = sc.sid
        into :sid, :ssid
    do
    begin
      --
      is_site_invent = null;
      if (ssid in (:ss_l,:ss_stack)) then
      begin

        if (
          exists (
             select *
               from wm_task_site ts
              where ts.siteid = :sid
                    and ts.taskid = :taskid
                    and ts.status = '2'
          )
       ) then
          is_site_invent = '1';
       else
         is_site_invent = '0';
      end

      -- паллеты
      pid = null;
      is_pallet_invent = null;
      for
        select p.palletid
          from pallet p
         where p.siteid = :sid
               and p.status = '1'
               and coalesce(p.objid,:objid) = :objid
               and coalesce(p.zoneid,:zoneid) = :zoneid
          into :pid do
      begin

        if (:pid is not null) then
        begin
          if (exists(
            select *
              from wm_task_pallet tp
             where tp.taskid = :taskid
                   and tp.palletid = :pid
                   and tp.siteid = :sid
                   and tp.status = '1'
          )) then
             is_pallet_invent = '1';
          else
             is_pallet_invent = null;


        end


      end 






      suspend;
    end 


  end
  -- остальные мп (Экспедиция, Ворота)
  for
    select szi.siteid
      from sitespecies ss
           left join site s
                left join sitezone_items szi on s.siteid = szi.siteid
             on s.sitespeciesid = ss.sitespeciesid
     where ss.code in ('E','GATE')
           and szi.zoneid = :zoneid
      into :siteid_row
  do
  begin
    if (
        exists (
           select ts.status
             from wm_task_site ts
            where ts.siteid = :siteid_row
                  and ts.taskid = :taskid
                  and ts.status = '2'
        )
    ) then
        is_site_invent = '1';
      else
        is_site_invent = '0';
  ---
    for
      select p.palletid
        from pallet p
       where p.siteid = :siteid_row
             and p.status = '1'
             and coalesce(p.objid,:objid) = :objid
             and coalesce(p.zoneid,:zoneid) = :zoneid
        into :pid do
    begin
      is_pallet_invent = null;
      if (:pid is not null) then
      begin
        if (exists(
            select *
              from wm_task_pallet tp
             where tp.taskid = :taskid
                   and tp.palletid = :pid
                   and tp.siteid = :siteid_row
                   and tp.status = '1'
        )) then
          is_pallet_invent = '1';



      end

      suspend;
    end
  ---
  end 
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_INVENT_GETTASKPROGRESS (
    TASKID type of R_ID)
returns (
    SITEID type of R_ID,
    SNAME type of R_NAME,
    CNT_PALLET integer,
    CNT_PALLET_ALL integer,
    CNT_SITE_ALL integer,
    CNT_SITE integer)
AS
declare variable OBJID type of R_ID;
declare variable ZONEID type of R_ID;
declare variable SS_ROW type of R_ID;
declare variable SS_MX type of R_ID;
declare variable SS_L type of R_ID;
declare variable SID type of R_ID;
declare variable CNT_PALLET_TEMP integer;
declare variable CNT_PALLET_ALL_TEMP integer;
declare variable PID type of R_ID;
declare variable SITEID_ROW type of R_ID;
declare variable IS_PALLET_INVENT type of R_ID;
begin

  select t.infoid, t.zoneid
    from wm_task t
   where t.taskid = :taskid
    into :objid, :zoneid;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'R'
    into :ss_row;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'B'
    into :ss_mx;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'L'
    into :ss_l;


  for
    select tp.siteid_row, s.name,
           count(tp.pid), sum(iif(tp.is_pallet_invent is null,0,1)),        -- паллеты
           sum(iif(tp.is_site_invent is not null,1,0)), sum(iif(tp.is_site_invent ='1',1,0))
      from k_wh_invent_taskpallet(:taskid) tp
           left join site s on tp.siteid_row = s.siteid
     group by tp.siteid_row, s.name
      into :siteid, :sname,
           :cnt_pallet_all, :cnt_pallet,
           :cnt_site_all, :cnt_site

  do
  begin
    suspend;
  end
  -------------------------------
  /*
  for
    select s.siteid, s.name
      from site s
           left join sitezone_items szi on s.siteid = szi.siteid
     where szi.zoneid = :zoneid
           and s.sitespeciesid = :ss_row
      into :siteid, :sname do
  begin
    cnt_site = 0;
    cnt_site_all = 0;
    -- МП
  for
    select sc.sid
      from k_site_children(:siteid,:ss_l,'1') sc
      into :sid
    do
    begin
       -------------
      cnt_site_all = : cnt_site_all + 1;
      if (
        exists (
           select ts.status
             from wm_task_site ts
            where ts.siteid = :sid
                  and ts.taskid = :taskid
                  and ts.status = '2'
        )
      ) then
        cnt_site = :cnt_site + 1;

    end 

    cnt_pallet_all = 0;
    cnt_pallet = 0;
    -- паллеты
    for
      select sc.sid
        from k_site_children(:siteid,null,'1') sc
        into :sid
    do
    begin

      cnt_pallet_all_temp = 0;
      cnt_pallet_temp = 0;

      select count(p.palletid)
        from pallet p
       where p.siteid = :sid
             and p.status = '1'
             and coalesce(p.objid,:objid) = :objid
        into :cnt_pallet_all_temp;


      select count(distinct tp.palletid)
        from wm_task_pallet tp
       where tp.taskid = :taskid
             and tp.siteid = :sid
             and tp.status = '1'
        into :cnt_pallet_temp;

      cnt_pallet_all = :cnt_pallet_all + :cnt_pallet_all_temp;
      cnt_pallet = :cnt_pallet + :cnt_pallet_temp;

    end 



    suspend;
  end 


  -- паллеты не на стеллажах
  cnt_site = 0;
  cnt_site_all = 0;
  cnt_pallet = 0;
  cnt_pallet_temp = 0;
  for
    select s.siteid, s.name, count(distinct p.palletid), sum(iif(tp.taskpalletid is not null,1,0))
      from sitezone_items szi
           left join pallet p
                left join wm_task_pallet tp on tp.palletid = p.palletid
                                               and tp.taskid = :taskid
                                               and tp.status = '1'
                left join site s
                     left join sitespecies ss on ss.sitespeciesid = s.sitespeciesid
                  on s.siteid = p.siteid
             on p.siteid = szi.siteid
     where szi.zoneid = :zoneid
           and p.status = '1'
           and p.pallettype = '0'
           and coalesce(p.objid,:objid) = :objid
           and ss.code in ('GATE','E')
     group by 1,2
      into :siteid, :sname, :cnt_pallet_all, :cnt_pallet_temp

  do
  begin
    cnt_site_all = : cnt_site_all + 1;
      if (
        exists (
           select ts.status
             from wm_task_site ts
            where ts.siteid = :siteid
                  and ts.taskid = :taskid
                  and ts.status = '2'
        )
      ) then
        cnt_site = :cnt_site + 1;



    cnt_pallet = :cnt_pallet + :cnt_pallet_temp;
    suspend;
  end 

  */
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_TERM_INVENT_STACKDO (
    taskid type of column wm_task.taskid,
    siteid type of column site.siteid,
    wmsessionid type of column wm_session.sessionid,
    cnt1 type of column site_stack.palcurcnt

)
as
declare variable palcurcnt type of column site_stack.palcurcnt;
declare variable manid type of column man.manid;
begin
    select wms.objid
      from wm_session wms
     where wms.sessionid = :wmsessionid
      into :manid;

    select ss.palcurcnt
      from site_stack ss
     where ss.siteid = :siteid
      into :palcurcnt;

    if (:palcurcnt = :cnt1) then
    begin
        insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
        select :taskid, p.palletid, :siteid, '1', :manid
          from pallet p
         where p.siteid = :siteid
           and p.status = '1';
    end

    update wm_task t
       set t.status = '2', t.wm_sessionid = :wmsessionid
     where t.taskid = :taskid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_STACKDO (
    taskid type of column wm_task.taskid,
    siteid type of column site.siteid,
    wmsessionid type of column wm_session.sessionid,
    cnt1 type of column site_stack.palcurcnt

)
as
declare variable palcurcnt type of column site_stack.palcurcnt;
declare variable manid type of column man.manid;
begin
    select wms.objid
      from wm_session wms
     where wms.sessionid = :wmsessionid
      into :manid;

    select ss.palcurcnt
      from site_stack ss
     where ss.siteid = :siteid
      into :palcurcnt;

    if (:palcurcnt = :cnt1) then
    begin
        insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
        select :taskid, p.palletid, :siteid, '1', :manid
          from pallet p
         where p.siteid = :siteid
           and p.status = '1';
    end

    update wm_task_site ts
       set ts.status = '2'
     where ts.taskid = :taskid
       and ts.siteid = :siteid
       and ts.manid = :manid
       and ts.status = '1';
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_STACKDO (
    TASKID type of column WM_TASK.TASKID,
    SITEID type of column SITE.SITEID,
    WMSESSIONID type of column WM_SESSION.SESSIONID,
    CNT1 type of column SITE_STACK.PALCURCNT)
AS
declare variable palcurcnt type of column site_stack.palcurcnt;
declare variable manid type of column man.manid;
declare variable waresid type of column GWARES.waresid;
declare variable amount type of column WARESLOTITEM.amount;
begin
    select wms.objid
      from wm_session wms
     where wms.sessionid = :wmsessionid
      into :manid;

    select ss.palcurcnt
      from site_stack ss
     where ss.siteid = :siteid
      into :palcurcnt;

    if (:palcurcnt = :cnt1) then
    begin
        insert into wm_task_pallet ( TASKID, PALLETID, SITEID, STATUS, MANID)
        select :taskid, p.palletid, :siteid, '1', :manid
          from pallet p
         where p.siteid = :siteid
           and p.status = '1';

        select ss.waresid
          from site_stack ss
         where ss.siteid = :siteid
          into :waresid;

        select sum(wli.amount)
          from pallet p
               left join wareslotitem wli
                    left join wareslot wl on wl.wlotid = wli.wlotid
                 on wli.palletid = p.palletid
         where p.siteid = :siteid
           and p.status = '1'
           and wl.waresid = :waresid
          into :amount;

         -- QUANTITY - Fact
         -- SCANQUANT - Plan
         insert into wm_task_wares ( TASKID, WARESID, QUANTITY, SCANQUANT, SITEID, STATUS, ENDTIME, WM_SESSIONID)
         values ( :taskid, :waresid, :amount, :amount, :siteid, '2', current_timestamp, :wmsessionid);
    end

    update wm_task_site ts
       set ts.status = '2'
     where ts.taskid = :taskid
       and ts.siteid = :siteid
       and ts.manid = :manid
       and ts.status = '1';
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_INVENT_GETTASKPROGRESS (
    TASKID type of R_ID)
returns (
    SITEID type of R_ID,
    SNAME type of R_NAME,
    CNT_PALLET integer,
    CNT_PALLET_ALL integer,
    CNT_SITE_ALL integer,
    CNT_SITE integer)
AS
 /*$$IBE$$ declare variable OBJID type of R_ID;
declare variable ZONEID type of R_ID;
declare variable SS_ROW type of R_ID;
declare variable SS_MX type of R_ID;
declare variable SS_L type of R_ID;
declare variable SID type of R_ID;
declare variable CNT_PALLET_TEMP integer;
declare variable CNT_PALLET_ALL_TEMP integer;
declare variable PID type of R_ID;
declare variable SITEID_ROW type of R_ID;
declare variable IS_PALLET_INVENT type of R_ID; $$IBE$$*/ 
begin /*$$IBE$$ 

  select t.infoid, t.zoneid
    from wm_task t
   where t.taskid = :taskid
    into :objid, :zoneid;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'R'
    into :ss_row;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'B'
    into :ss_mx;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'L'
    into :ss_l;


  for
    select tp.siteid_row, s.name,
           count(tp.pid), sum(iif(tp.is_pallet_invent is null,0,1)),        -- паллеты
           sum(iif(tp.is_site_invent is not null,1,0)), sum(iif(tp.is_site_invent ='1',1,0))
      from k_wh_invent_taskpallet(:taskid) tp
           left join site s on tp.siteid_row = s.siteid
     group by tp.siteid_row, s.name
      into :siteid, :sname,
           :cnt_pallet_all, :cnt_pallet,
           :cnt_site_all, :cnt_site

  do
  begin
    suspend;
  end
  -------------------------------
   $$IBE$$*/ /*
  for
    select s.siteid, s.name
      from site s
           left join sitezone_items szi on s.siteid = szi.siteid
     where szi.zoneid = :zoneid
           and s.sitespeciesid = :ss_row
      into :siteid, :sname do
  begin
    cnt_site = 0;
    cnt_site_all = 0;
    -- МП
  for
    select sc.sid
      from k_site_children(:siteid,:ss_l,'1') sc
      into :sid
    do
    begin
       -------------
      cnt_site_all = : cnt_site_all + 1;
      if (
        exists (
           select ts.status
             from wm_task_site ts
            where ts.siteid = :sid
                  and ts.taskid = :taskid
                  and ts.status = '2'
        )
      ) then
        cnt_site = :cnt_site + 1;

    end 

    cnt_pallet_all = 0;
    cnt_pallet = 0;
    -- паллеты
    for
      select sc.sid
        from k_site_children(:siteid,null,'1') sc
        into :sid
    do
    begin

      cnt_pallet_all_temp = 0;
      cnt_pallet_temp = 0;

      select count(p.palletid)
        from pallet p
       where p.siteid = :sid
             and p.status = '1'
             and coalesce(p.objid,:objid) = :objid
        into :cnt_pallet_all_temp;


      select count(distinct tp.palletid)
        from wm_task_pallet tp
       where tp.taskid = :taskid
             and tp.siteid = :sid
             and tp.status = '1'
        into :cnt_pallet_temp;

      cnt_pallet_all = :cnt_pallet_all + :cnt_pallet_all_temp;
      cnt_pallet = :cnt_pallet + :cnt_pallet_temp;

    end 



    suspend;
  end 


  -- паллеты не на стеллажах
  cnt_site = 0;
  cnt_site_all = 0;
  cnt_pallet = 0;
  cnt_pallet_temp = 0;
  for
    select s.siteid, s.name, count(distinct p.palletid), sum(iif(tp.taskpalletid is not null,1,0))
      from sitezone_items szi
           left join pallet p
                left join wm_task_pallet tp on tp.palletid = p.palletid
                                               and tp.taskid = :taskid
                                               and tp.status = '1'
                left join site s
                     left join sitespecies ss on ss.sitespeciesid = s.sitespeciesid
                  on s.siteid = p.siteid
             on p.siteid = szi.siteid
     where szi.zoneid = :zoneid
           and p.status = '1'
           and p.pallettype = '0'
           and coalesce(p.objid,:objid) = :objid
           and ss.code in ('GATE','E')
     group by 1,2
      into :siteid, :sname, :cnt_pallet_all, :cnt_pallet_temp

  do
  begin
    cnt_site_all = : cnt_site_all + 1;
      if (
        exists (
           select ts.status
             from wm_task_site ts
            where ts.siteid = :siteid
                  and ts.taskid = :taskid
                  and ts.status = '2'
        )
      ) then
        cnt_site = :cnt_site + 1;



    cnt_pallet = :cnt_pallet + :cnt_pallet_temp;
    suspend;
  end 

  */
SUSPEND;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_INVENT_NOTINVENTPAL (
    TASKID type of R_ID)
returns (
    SNAME type of R_NAME,
    PNUMBER type of R_BARCODE)
AS
 /*$$IBE$$ declare variable OBJID type of R_ID;
declare variable ZONEID type of R_ID; $$IBE$$*/ 
begin /*$$IBE$$ 
  for
    select s.name, case
                     when (p.pallettype = '1') then 'МО'
                     when (p.pallettype = '0') then '№'||p.number
                   end
      from k_wh_invent_taskpallet(:taskid) tp
           left join site s on s.siteid = tp.sid
           left join pallet p on p.palletid = tp.pid
     where tp.pid is not null
           and tp.is_pallet_invent is null
     order by s.name asc
      into :sname, :pnumber

  do
    suspend;
 $$IBE$$*/ SUSPEND;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_INVENT_TASKPALLET (
    TASKID type of column WM_TASK.TASKID)
returns (
    SID type of column SITE.SITEID,
    PID type of column PALLET.PALLETID,
    SITEID_ROW type of column SITE.SITEID,
    cnt_site_all type of R_NUMBER,
    cnt_site_inv type of R_NUMBER,
    cnt_pal_all type of R_NUMBER,
    cnt_pal_inv type of R_NUMBER)
AS
--declare variable SITEID type of column SITE.siteid;
declare variable OBJID type of column OBJECT.objid;
declare variable ZONEID type of column sitezone.zoneid;
declare variable SS_ROW type of column sitespecies.sitespeciesid;
declare variable SS_L type of column sitespecies.sitespeciesid;
declare variable ss_stack type of column sitespecies.sitespeciesid;
declare variable SSID type of column sitespecies.sitespeciesid;
begin
  select t.infoid, t.zoneid
    from wm_task t
   where t.taskid = :taskid
    into :objid, :zoneid;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'R'
    into :ss_row;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'L'
    into :ss_l;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'STACK'
    into :ss_stack;

  -- по рядам
  for
    select s.siteid
      from site s
           left join sitezone_items szi on s.siteid = szi.siteid
     where szi.zoneid = :zoneid
           and s.sitespeciesid = :ss_row
      into :siteid_row do
  begin
    cnt_site_all = 0;
    cnt_site_inv = 0;

    cnt_pal_all = 0;
    cnt_pal_inv = 0;

    for
      select sc.sid, s.sitespeciesid
        from k_site_children(:siteid_row,null,'1') sc
             left join site s on s.siteid = sc.sid
        into :sid, :ssid
    do
    begin
      if (ssid in (:ss_l,:ss_stack)) then
      begin
        cnt_site_all = :cnt_site_all + 1;
        if (exists (select *
                      from wm_task_site ts
                     where ts.siteid = :sid
                       and ts.taskid = :taskid
                       and ts.status = '2')) then
            cnt_site_inv = :cnt_site_inv + 1;
      end

      -- паллеты
      for
        select p.palletid
          from pallet p
         where p.siteid = :sid
               and p.status = '1'
               and coalesce(p.objid,:objid) = :objid
               and coalesce(p.zoneid,:zoneid) = :zoneid
          into :pid do
      begin
          cnt_pal_all = :cnt_pal_all + 1;
          if (exists(select *
                       from wm_task_pallet tp
                      where tp.taskid = :taskid
                           and tp.palletid = :pid
                   and tp.siteid = :sid
                   and tp.status = '1'
          )) then
             cnt_pal_inv = :cnt_pal_inv + 1;
      end 

      suspend;
    end 
  end
  -- остальные мп (Экспедиция, Ворота)
  for
    select szi.siteid
      from sitespecies ss
           left join site s
                left join sitezone_items szi on s.siteid = szi.siteid
             on s.sitespeciesid = ss.sitespeciesid
     where ss.code in ('E','GATE')
       and szi.zoneid = :zoneid
      into :siteid_row
  do
  begin
    cnt_site_all = 1;
    cnt_site_inv = 0;

    if (
        exists (
           select ts.status
             from wm_task_site ts
            where ts.siteid = :siteid_row
                  and ts.taskid = :taskid
                  and ts.status = '2'
        )
    ) then
        cnt_site_inv = 1;

    cnt_pal_all = 0;
    cnt_pal_inv = 0;

    for
      select p.palletid
        from pallet p
       where p.siteid = :siteid_row
             and p.status = '1'
             and coalesce(p.objid,:objid) = :objid
             and coalesce(p.zoneid,:zoneid) = :zoneid
        into :pid do
    begin
      cnt_pal_all = :cnt_pal_all + 1;

      if (exists(select *
                   from wm_task_pallet tp
                  where tp.taskid = :taskid
                    and tp.palletid = :pid
                    and tp.siteid = :siteid_row
                    and tp.status = '1')) then
          cnt_pal_inv = :cnt_pal_inv + 1;
    end

    suspend;
  ---
  end 
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_INVENT_GETTASKPROGRESS (
    TASKID type of R_ID)
returns (
    SITEID type of R_ID,
    SNAME type of R_NAME,
    CNT_PALLET integer,
    CNT_PALLET_ALL integer,
    CNT_SITE_ALL integer,
    CNT_SITE integer)
AS
declare variable OBJID type of R_ID;
declare variable ZONEID type of R_ID;
declare variable SS_ROW type of R_ID;
declare variable SS_MX type of R_ID;
declare variable SS_L type of R_ID;
declare variable SID type of R_ID;
declare variable CNT_PALLET_TEMP integer;
declare variable CNT_PALLET_ALL_TEMP integer;
declare variable PID type of R_ID;
declare variable SITEID_ROW type of R_ID;
declare variable IS_PALLET_INVENT type of R_ID;
begin

  select t.infoid, t.zoneid
    from wm_task t
   where t.taskid = :taskid
    into :objid, :zoneid;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'R'
    into :ss_row;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'B'
    into :ss_mx;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'L'
    into :ss_l;


  for
    select tp.siteid_row, s.name,
           sum(tp.cnt_pal_all), sum(tp.cnt_pal_inv),        -- паллеты
           sum(tp.cnt_site_all), sum(tp.cnt_site_inv)
      from k_wh_invent_taskpallet(:taskid) tp
           left join site s on tp.siteid_row = s.siteid
     group by tp.siteid_row, s.name
      into :siteid, :sname,
           :cnt_pallet_all, :cnt_pallet,
           :cnt_site_all, :cnt_site

  do
  begin
    suspend;
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_INVENT_GETTASKPROGRESS (
    TASKID type of R_ID)
returns (
    SITEID type of R_ID,
    SNAME type of R_NAME,
    CNT_PALLET integer,
    CNT_PALLET_ALL integer,
    CNT_SITE_ALL integer,
    CNT_SITE integer)
AS
begin
  for
    select tp.siteid_row, s.name,
           sum(tp.cnt_pal_all), sum(tp.cnt_pal_inv),        -- паллеты
           sum(tp.cnt_site_all), sum(tp.cnt_site_inv)
      from k_wh_invent_taskpallet(:taskid) tp
           left join site s on tp.siteid_row = s.siteid
     group by tp.siteid_row, s.name
      into :siteid, :sname,
           :cnt_pallet_all, :cnt_pallet,
           :cnt_site_all, :cnt_site
  do
  begin
    suspend;
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_INVENT_TASKPALLET (
    TASKID type of column WM_TASK.TASKID)
returns (
    SID type of column SITE.SITEID,
    PID type of column PALLET.PALLETID,
    SITEID_ROW type of column SITE.SITEID,
    cnt_site_all type of R_NUMBER,
    cnt_site_inv type of R_NUMBER,
    cnt_pal_all type of R_NUMBER,
    cnt_pal_inv type of R_NUMBER)
AS
--declare variable SITEID type of column SITE.siteid;
declare variable OBJID type of column OBJECT.objid;
declare variable ZONEID type of column sitezone.zoneid;
declare variable SS_ROW type of column sitespecies.sitespeciesid;
declare variable SS_L type of column sitespecies.sitespeciesid;
declare variable ss_stack type of column sitespecies.sitespeciesid;
declare variable SSID type of column sitespecies.sitespeciesid;
begin
  select t.infoid, t.zoneid
    from wm_task t
   where t.taskid = :taskid
    into :objid, :zoneid;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'R'
    into :ss_row;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'L'
    into :ss_l;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'STACK'
    into :ss_stack;

  -- по рядам
  for
    select s.siteid
      from site s
           left join sitezone_items szi on s.siteid = szi.siteid
     where szi.zoneid = :zoneid
           and s.sitespeciesid = :ss_row
           and s.siteid = 103
      into :siteid_row do
  begin
    cnt_site_all = 0;
    cnt_site_inv = 0;

    cnt_pal_all = 0;
    cnt_pal_inv = 0;

    for
      select sc.sid, s.sitespeciesid
        from k_site_children(:siteid_row,null,'1') sc
             left join site s on s.siteid = sc.sid
        into :sid, :ssid
    do
    begin
      if (ssid in (:ss_l,:ss_stack)) then
      begin
        cnt_site_all = :cnt_site_all + 1;
        if (exists (select *
                      from wm_task_site ts
                     where ts.siteid = :sid
                       and ts.taskid = :taskid
                       and ts.status = '2')) then
            cnt_site_inv = :cnt_site_inv + 1;
      end

      -- паллеты
      for
        select p.palletid
          from pallet p
         where p.siteid = :sid
               and p.status = '1'
               and coalesce(p.objid,:objid) = :objid
               and coalesce(p.zoneid,:zoneid) = :zoneid
          into :pid do
      begin
          cnt_pal_all = :cnt_pal_all + 1;
          if (exists(select *
                       from wm_task_pallet tp
                      where tp.taskid = :taskid
                           and tp.palletid = :pid
                   and tp.siteid = :sid
                   and tp.status = '1'
          )) then
             cnt_pal_inv = :cnt_pal_inv + 1;
      end 

      suspend;
    end 
  end
  -- остальные мп (Экспедиция, Ворота)
  for
    select szi.siteid
      from sitespecies ss
           left join site s
                left join sitezone_items szi on s.siteid = szi.siteid
             on s.sitespeciesid = ss.sitespeciesid
     where ss.code in ('E','GATE')
       and szi.zoneid = :zoneid
      into :siteid_row
  do
  begin
    cnt_site_all = 1;
    cnt_site_inv = 0;

    if (
        exists (
           select ts.status
             from wm_task_site ts
            where ts.siteid = :siteid_row
                  and ts.taskid = :taskid
                  and ts.status = '2'
        )
    ) then
        cnt_site_inv = 1;

    cnt_pal_all = 0;
    cnt_pal_inv = 0;

    for
      select p.palletid
        from pallet p
       where p.siteid = :siteid_row
             and p.status = '1'
             and coalesce(p.objid,:objid) = :objid
             and coalesce(p.zoneid,:zoneid) = :zoneid
        into :pid do
    begin
      cnt_pal_all = :cnt_pal_all + 1;

      if (exists(select *
                   from wm_task_pallet tp
                  where tp.taskid = :taskid
                    and tp.palletid = :pid
                    and tp.siteid = :siteid_row
                    and tp.status = '1')) then
          cnt_pal_inv = :cnt_pal_inv + 1;
    end

    suspend;
  ---
  end 
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_INVENT_TASKPALLET (
    TASKID type of column WM_TASK.TASKID)
returns (
    SID type of column SITE.SITEID,
    PID type of column PALLET.PALLETID,
    SITEID_ROW type of column SITE.SITEID,
    cnt_site_all type of R_NUMBER,
    cnt_site_inv type of R_NUMBER,
    cnt_pal_all type of R_NUMBER,
    cnt_pal_inv type of R_NUMBER)
AS
--declare variable SITEID type of column SITE.siteid;
declare variable OBJID type of column OBJECT.objid;
declare variable ZONEID type of column sitezone.zoneid;
declare variable SS_ROW type of column sitespecies.sitespeciesid;
declare variable SS_L type of column sitespecies.sitespeciesid;
declare variable ss_stack type of column sitespecies.sitespeciesid;
declare variable SSID type of column sitespecies.sitespeciesid;
begin
  select t.infoid, t.zoneid
    from wm_task t
   where t.taskid = :taskid
    into :objid, :zoneid;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'R'
    into :ss_row;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'L'
    into :ss_l;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'STACK'
    into :ss_stack;

  -- по рядам
  for
    select s.siteid
      from site s
           left join sitezone_items szi on s.siteid = szi.siteid
     where szi.zoneid = :zoneid
           and s.sitespeciesid = :ss_row
           and s.siteid = 103
      into :siteid_row do
  begin
    cnt_site_all = 0;
    cnt_site_inv = 0;

    cnt_pal_all = 0;
    cnt_pal_inv = 0;

    for
      select sc.sid, s.sitespeciesid
        from k_site_children(:siteid_row,null,'1') sc
             left join site s on s.siteid = sc.sid
        into :sid, :ssid
    do
    begin
      if (ssid in (:ss_l,:ss_stack)) then
      begin
        cnt_site_all = :cnt_site_all + 1;
        if (exists (select *
                      from wm_task_site ts
                     where ts.siteid = :sid
                       and ts.taskid = :taskid
                       and ts.status = '2')) then
            cnt_site_inv = :cnt_site_inv + 1;
      end

      -- паллеты
      for
        select p.palletid
          from pallet p
         where p.siteid = :sid
               and p.status = '1'
               and coalesce(p.objid,:objid) = :objid
               and coalesce(p.zoneid,:zoneid) = :zoneid
          into :pid do
      begin
          cnt_pal_all = :cnt_pal_all + 1;
          if (exists(select *
                       from wm_task_pallet tp
                      where tp.taskid = :taskid
                           and tp.palletid = :pid
                   and tp.siteid = :sid
                   and tp.status = '1'
          )) then
             cnt_pal_inv = :cnt_pal_inv + 1;
      end 
    end 
    suspend;
  end
  -- остальные мп (Экспедиция, Ворота)
  for
    select szi.siteid
      from sitespecies ss
           left join site s
                left join sitezone_items szi on s.siteid = szi.siteid
             on s.sitespeciesid = ss.sitespeciesid
     where ss.code in ('E','GATE')
       and szi.zoneid = :zoneid
      into :siteid_row
  do
  begin
    cnt_site_all = 1;
    cnt_site_inv = 0;

    if (
        exists (
           select ts.status
             from wm_task_site ts
            where ts.siteid = :siteid_row
                  and ts.taskid = :taskid
                  and ts.status = '2'
        )
    ) then
        cnt_site_inv = 1;

    cnt_pal_all = 0;
    cnt_pal_inv = 0;

    for
      select p.palletid
        from pallet p
       where p.siteid = :siteid_row
             and p.status = '1'
             and coalesce(p.objid,:objid) = :objid
             and coalesce(p.zoneid,:zoneid) = :zoneid
        into :pid do
    begin
      cnt_pal_all = :cnt_pal_all + 1;

      if (exists(select *
                   from wm_task_pallet tp
                  where tp.taskid = :taskid
                    and tp.palletid = :pid
                    and tp.siteid = :siteid_row
                    and tp.status = '1')) then
          cnt_pal_inv = :cnt_pal_inv + 1;
    end

    suspend;
  ---
  end 
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_INVENT_TASKPALLET (
    TASKID type of column WM_TASK.TASKID)
returns (
    SID type of column SITE.SITEID,
    PID type of column PALLET.PALLETID,
    SITEID_ROW type of column SITE.SITEID,
    cnt_site_all type of R_NUMBER,
    cnt_site_inv type of R_NUMBER,
    cnt_pal_all type of R_NUMBER,
    cnt_pal_inv type of R_NUMBER)
AS
--declare variable SITEID type of column SITE.siteid;
declare variable OBJID type of column OBJECT.objid;
declare variable ZONEID type of column sitezone.zoneid;
declare variable SS_ROW type of column sitespecies.sitespeciesid;
declare variable SS_L type of column sitespecies.sitespeciesid;
declare variable ss_stack type of column sitespecies.sitespeciesid;
declare variable SSID type of column sitespecies.sitespeciesid;
begin
  select t.infoid, t.zoneid
    from wm_task t
   where t.taskid = :taskid
    into :objid, :zoneid;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'R'
    into :ss_row;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'L'
    into :ss_l;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'STACK'
    into :ss_stack;

  -- по рядам
  for
    select s.siteid
      from site s
           left join sitezone_items szi on s.siteid = szi.siteid
     where szi.zoneid = :zoneid
           and s.sitespeciesid = :ss_row
      into :siteid_row do
  begin
    cnt_site_all = 0;
    cnt_site_inv = 0;

    cnt_pal_all = 0;
    cnt_pal_inv = 0;

    for
      select sc.sid, s.sitespeciesid
        from k_site_children(:siteid_row,null,'1') sc
             left join site s on s.siteid = sc.sid
        into :sid, :ssid
    do
    begin
      if (ssid in (:ss_l,:ss_stack)) then
      begin
        cnt_site_all = :cnt_site_all + 1;
        if (exists (select *
                      from wm_task_site ts
                     where ts.siteid = :sid
                       and ts.taskid = :taskid
                       and ts.status = '2')) then
            cnt_site_inv = :cnt_site_inv + 1;
      end

      -- паллеты
      for
        select p.palletid
          from pallet p
         where p.siteid = :sid
               and p.status = '1'
               and coalesce(p.objid,:objid) = :objid
               and coalesce(p.zoneid,:zoneid) = :zoneid
          into :pid do
      begin
          cnt_pal_all = :cnt_pal_all + 1;
          if (exists(select *
                       from wm_task_pallet tp
                      where tp.taskid = :taskid
                           and tp.palletid = :pid
                   and tp.siteid = :sid
                   and tp.status = '1'
          )) then
             cnt_pal_inv = :cnt_pal_inv + 1;
      end 
    end 
    suspend;
  end
  -- остальные мп (Экспедиция, Ворота)
  for
    select szi.siteid
      from sitespecies ss
           left join site s
                left join sitezone_items szi on s.siteid = szi.siteid
             on s.sitespeciesid = ss.sitespeciesid
     where ss.code in ('E','GATE')
       and szi.zoneid = :zoneid
      into :siteid_row
  do
  begin
    cnt_site_all = 1;
    cnt_site_inv = 0;

    if (
        exists (
           select ts.status
             from wm_task_site ts
            where ts.siteid = :siteid_row
                  and ts.taskid = :taskid
                  and ts.status = '2'
        )
    ) then
        cnt_site_inv = 1;

    cnt_pal_all = 0;
    cnt_pal_inv = 0;

    for
      select p.palletid
        from pallet p
       where p.siteid = :siteid_row
             and p.status = '1'
             and coalesce(p.objid,:objid) = :objid
             and coalesce(p.zoneid,:zoneid) = :zoneid
        into :pid do
    begin
      cnt_pal_all = :cnt_pal_all + 1;

      if (exists(select *
                   from wm_task_pallet tp
                  where tp.taskid = :taskid
                    and tp.palletid = :pid
                    and tp.siteid = :siteid_row
                    and tp.status = '1')) then
          cnt_pal_inv = :cnt_pal_inv + 1;
    end

    suspend;
  ---
  end 
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_INVENT_GETTASKPROGRESS (
    TASKID type of R_ID)
returns (
    SITEID type of R_ID,
    SNAME type of R_NAME,
    CNT_PALLET integer,
    CNT_PALLET_ALL integer,
    CNT_SITE_ALL integer,
    CNT_SITE integer)
AS
begin
  for
    select tp.siteid_row, s.name,
           sum(tp.cnt_pal_all), sum(tp.cnt_pal_inv),        -- паллеты
           sum(tp.cnt_site_all), sum(tp.cnt_site_inv)
      from k_wh_invent_taskpallet(:taskid) tp
           left join site s on tp.siteid_row = s.siteid
     group by tp.siteid_row, s.name
      into :siteid, :sname,
           :cnt_pallet_all, :cnt_pallet,
           :cnt_site_all, :cnt_site
  do
  begin
    suspend;
  end
end^

SET TERM ; ^

