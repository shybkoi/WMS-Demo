

SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_GETNEXTTASK (
    WMSID R_ID)
returns (
    TID type of R_ID,
    TNUMBER type of R_SHORTNAME,
    TSNAME type of R_NAME,
    DNUM type of DOCNUMBER,
    DDATE type of R_DATE,
    CLIENTNAME type of R_NAME,
    WHNAME type of R_NAME,
    TUID type of R_ID,
    TUNAME type of R_NAME,
    GOTOTASK type of R_FLAG)
AS
declare variable taskid_gateauto r_id;
declare variable taskid_select r_id;
declare variable taskid_loadauto r_id;
declare variable ttid_loadpallet r_id;
declare variable ttid_loadauto r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_cardocs r_id;
declare variable tbtid_loadselect r_id;
begin
    execute procedure wh_ttid_loadpallet returning_values :ttid_loadpallet;

    -- 1- ищем прив€занное задание погрузки поддона
    select t.taskid
      from wm_task t
     where t.wm_sessionid = :wmsid
       and t.status = '1'
       and t.tasktypeid = :ttid_loadpallet
      into :tid;

    -- 2 - ищем задание погрузки поддона из прив€занных заданий на погрузку документа
    if (:tid is NULL) then
    begin
        execute procedure wh_ttid_loadauto returning_values :ttid_loadauto;

        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'CARDOCS'
          into :tbtid_cardocs;
        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'LOADSELECT'
          into :tbtid_loadselect;

        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'DOCPALLETS'
          into :tbtid_docpallets;

        for
            select t.taskid
              from wm_task t
                   left join wh_taskbond tb
                        left join wm_task t1 on t1.taskid = tb.task1id
                     on tb.task2id = t.taskid and tb.taskbondtid = :tbtid_cardocs
             where t.wm_sessionid = :wmsid
               and t.status = '1'
               and t.tasktypeid = :ttid_loadauto
             order by t1.priority ascending nulls last,
                      t1.plandatetime ascending,
                      t1.begintime ascending,
                      t.priority ascending nulls last,
                      t.docid
              into :taskid_loadauto
        do
        begin
            select first(1) t.taskid
              from wh_taskbond tb
                   left join wm_task t
                        left join wh_taskbond tb2
                             left join wm_task t2 on t2.taskid = tb2.task2id
                          on tb2.task1id = t.taskid and tb2.taskbondtid = :tbtid_loadselect
                     on t.taskid = tb.task2id
             where tb.task1id = :taskid_loadauto
               and tb.taskbondtid = :tbtid_docpallets
               and t.status <> '2'
             order by t2.endtime descending nulls last, t.num ascending
               into :tid;

            if (:tid is NOT NULL) then
                break;
        end
    end

    -- ≈сли нашли - вернули
    if (:tid is NOT NULL) then
    begin
        select ti.TNUMBER,ti.TSNAME,ti.DNUM,ti.DDATE,
               ti.CLIENTNAME,ti.whname,
               ti.TUID, ti.TUNAME
          from wh_loadpalletdc_taskinfo(:tid) ti
          into :TNUMBER,:TSNAME,:DNUM,:DDATE,:CLIENTNAME,:WHNAME,:TUID,:TUNAME;

        gototask = '1';
        suspend; exit;
    end

    -- »наче ищем среди всех не прив€занных
    gototask = '0';
    for
        select t.taskid
          from WH_LOADAUTODC_LISTGATES(:wmsid) g
               left join wm_task t
                 on t.taskid = g.tid
         where g.tid is NOT NULL
         order by t.priority ascending nulls last,t.plandatetime ascending,t.begintime ascending
          into :taskid_gateauto
    do
    begin
        for
            select w.TID,w.TNUMBER,w.TSNAME,w.TID_SELECT,w.DNUM,w.DDATE,w.CLIENTNAME,w.WHNAME
              from wh_loadautodc_listpallets(:taskid_gateauto) w
                   left join wm_task t on t.taskid = w.tid_loadauto
             where w.TSTAT = '0'
--               and w.DSTAT = '2'
               and (t.status = '0' or (t.status='1' and t.wm_sessionid is NULL))
             order by w.tpriority ascending,
                   w.tend_select descending nulls last,w.tnum_select ascending
              into :tid,:tnumber,:tsname,:taskid_select,:dnum,:ddate,:clientname,:whname
        do
        begin
            tuid = NULL;
            tuname = NULL;

            select tu.tuid,tu.name
              from wm_task_transunit ttu
                   left join wh_transport_unit tu on tu.tuid = ttu.tunitid
             where ttu.taskid = :taskid_select
              into :tuid,:tuname;

            suspend;
            exit;
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_GETNEXTTASK (
    WMSID R_ID)
returns (
    TID type of R_ID,
    TNUMBER type of R_SHORTNAME,
    TSNAME type of R_NAME,
    DNUM type of DOCNUMBER,
    DDATE type of R_DATE,
    CLIENTNAME type of R_NAME,
    WHNAME type of R_NAME,
    TUID type of R_ID,
    TUNAME type of R_NAME,
    GOTOTASK type of R_FLAG)
AS
declare variable taskid_gateauto r_id;
declare variable taskid_select r_id;
declare variable taskid_loadauto r_id;
declare variable ttid_loadpallet r_id;
declare variable ttid_loadauto r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_cardocs r_id;
declare variable tbtid_loadselect r_id;
begin
    execute procedure wh_ttid_loadpallet returning_values :ttid_loadpallet;

    -- 1- ищем прив€занное задание погрузки поддона
    select t.taskid
      from wm_task t
     where t.wm_sessionid = :wmsid
       and t.status = '1'
       and t.tasktypeid = :ttid_loadpallet
      into :tid;

    -- 2 - ищем задание погрузки поддона из прив€занных заданий на погрузку документа
    if (:tid is NULL) then
    begin
        execute procedure wh_ttid_loadauto returning_values :ttid_loadauto;

        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'CARDOCS'
          into :tbtid_cardocs;
        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'LOADSELECT'
          into :tbtid_loadselect;

        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'DOCPALLETS'
          into :tbtid_docpallets;

        for
            select t.taskid
              from wm_task t
                   left join wh_taskbond tb
                        left join wm_task t1 on t1.taskid = tb.task1id
                     on tb.task2id = t.taskid and tb.taskbondtid = :tbtid_cardocs
             where t.wm_sessionid = :wmsid
               and t.status = '1'
               and t.tasktypeid = :ttid_loadauto
             order by t1.priority ascending nulls last,
                      t1.plandatetime ascending,
                      t1.begintime ascending,
                      t.priority ascending nulls last,
                      t.docid
              into :taskid_loadauto
        do
        begin
            select first(1) t.taskid
              from wh_taskbond tb
                   left join wm_task t
                        left join wh_taskbond tb2
                             left join wm_task t2 on t2.taskid = tb2.task2id
                          on tb2.task1id = t.taskid and tb2.taskbondtid = :tbtid_loadselect
                     on t.taskid = tb.task2id
             where tb.task1id = :taskid_loadauto
               and tb.taskbondtid = :tbtid_docpallets
               and t.status <> '2'
             order by t2.endtime descending nulls last, t.num ascending
               into :tid;

            if (:tid is NOT NULL) then
                break;
        end
    end

    -- ≈сли нашли - вернули
    if (:tid is NOT NULL) then
    begin
        select ti.TNUMBER,ti.TSNAME,ti.DNUM,ti.DDATE,
               ti.CLIENTNAME,ti.whname,
               ti.TUID, ti.TUNAME
          from wh_loadpalletdc_taskinfo(:tid) ti
          into :TNUMBER,:TSNAME,:DNUM,:DDATE,:CLIENTNAME,:WHNAME,:TUID,:TUNAME;

        gototask = '1';
        suspend; exit;
    end

    -- »наче ищем среди всех не прив€занных
    gototask = '0';
    for
        select t.taskid
          from WH_LOADAUTODC_LISTGATES(:wmsid) g
               left join wm_task t
                 on t.taskid = g.tid
         where g.tid is NOT NULL
         order by t.priority ascending nulls last,
                  t.plandatetime ascending,
                  t.begintime ascending,
                  g.gname ascending
          into :taskid_gateauto
    do
    begin
        for
            select w.TID,w.TNUMBER,w.TSNAME,w.TID_SELECT,w.DNUM,w.DDATE,w.CLIENTNAME,w.WHNAME
              from wh_loadautodc_listpallets(:taskid_gateauto) w
                   left join wm_task t on t.taskid = w.tid_loadauto
             where w.TSTAT = '0'
--               and w.DSTAT = '2'
               and (t.status = '0' or (t.status='1' and t.wm_sessionid is NULL))
             order by w.tpriority ascending,
                   w.tend_select descending nulls last,w.tnum_select ascending
              into :tid,:tnumber,:tsname,:taskid_select,:dnum,:ddate,:clientname,:whname
        do
        begin
            tuid = NULL;
            tuname = NULL;

            select tu.tuid,tu.name
              from wm_task_transunit ttu
                   left join wh_transport_unit tu on tu.tuid = ttu.tunitid
             where ttu.taskid = :taskid_select
              into :tuid,:tuname;

            suspend;
            exit;
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADAUTODC_LISTGATES (
    WMSESID type of column WM_SESSION.sessionid
)
returns (
    GID type of column SITE.siteid ,
    GNAME type of column SITE.name,
    TID type of column WM_TASK.taskid,
    AID type of column T_AUTO.aid,
    ANAME type of column T_AUTO.name,
    TPLANDT type of column WM_TASK.plandatetime ,
    TPRIORITY type of column WM_TASK.priority
)
AS
declare variable objid type of column OBJECT.objid;
declare variable spid type of column sitespecies.sitespeciesid;
declare variable ttid_gateauto type of column WM_TASKTYPE.tasktypeid;
begin
    select wms.objid
      from wm_session wms
     where wms.sessionid = :wmsesid
      into :objid;

    select sp.sitespeciesid
      from sitespecies sp
     where sp.code = 'GATE'
      into :spid;

    execute procedure wh_ttid_gateauto returning_values :ttid_gateauto;

    for
        select s.siteid,s.name
          from site s
         where s.sitespeciesid = :spid
           and s.status = '1'
           and exists(select *
                        from sitezone_items szi
                             left join sitezone_employees sze on sze.zoneid = szi.zoneid
                       where szi.siteid = s.siteid
                         and sze.employeeid = :objid)
          into :gid,:gname
    do
    begin
        tid = NULL;
        aid = NULL;
        aname = NULL;

        select t.taskid,ta.aid,ta.name,t.plandatetime,t.priority
          from wm_task t
               left join t_auto ta on ta.aid = t.infoid
         where t.tasktypeid = :ttid_gateauto
           and t.status = '1'
           and t.siteid = :gid
          PLAN(T INDEX (WM_TASK_IDX_SITE,WM_TASK_S_TT), TA index (RDB$PRIMARY8))
          into :tid,:aid,:aname,:tplandt,:tpriority;

        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADAUTODC_LISTGATES (
    WMSESID type of column WM_SESSION.sessionid
)
returns (
    GID type of column SITE.siteid ,
    GNAME type of column SITE.name,
    TID type of column WM_TASK.taskid,
    AID type of column T_AUTO.aid,
    ANAME type of column T_AUTO.name,
    TPLANDT type of column WM_TASK.plandatetime,
    TPRIORITY type of column WM_TASK.priority,
    TBEGINTIME type of column WM_TASK.begintime
)
AS
declare variable objid type of column OBJECT.objid;
declare variable spid type of column sitespecies.sitespeciesid;
declare variable ttid_gateauto type of column WM_TASKTYPE.tasktypeid;
begin
    select wms.objid
      from wm_session wms
     where wms.sessionid = :wmsesid
      into :objid;

    select sp.sitespeciesid
      from sitespecies sp
     where sp.code = 'GATE'
      into :spid;

    execute procedure wh_ttid_gateauto returning_values :ttid_gateauto;

    for
        with gate as (
            select s.siteid as id,s.name as name
              from site s
             where s.sitespeciesid = :spid
               and s.status = '1'
               and exists(select *
                            from sitezone_items szi
                                 left join sitezone_employees sze on sze.zoneid = szi.zoneid
                           where szi.siteid = s.siteid
                             and sze.employeeid = :objid)
        )
        select gate.id, gate.name,
               t.taskid,ta.aid,ta.name,t.plandatetime,t.priority,t.begintime
          from gate
               left join wm_task t
                    left join t_auto ta on ta.aid = t.infoid
                 on t.tasktypeid = :ttid_gateauto and t.status = '1' and t.siteid = :gid
         order by t.priority, t.plandatetime, t.begintime
          into :gid,:gname,:tid,:aid,:aname,:tplandt,:tpriority,:tbegintime
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADAUTODC_LISTGATES (
    WMSESID type of column WM_SESSION.sessionid
)
returns (
    GID type of column SITE.siteid ,
    GNAME type of column SITE.name,
    TID type of column WM_TASK.taskid,
    AID type of column T_AUTO.aid,
    ANAME type of column T_AUTO.name,
    TPLANDT type of column WM_TASK.plandatetime,
    TPRIORITY type of column WM_TASK.priority,
    TBEGINTIME type of column WM_TASK.begintime
)
AS
declare variable objid type of column OBJECT.objid;
declare variable spid type of column sitespecies.sitespeciesid;
declare variable ttid_gateauto type of column WM_TASKTYPE.tasktypeid;
begin
    select wms.objid
      from wm_session wms
     where wms.sessionid = :wmsesid
      into :objid;

    select sp.sitespeciesid
      from sitespecies sp
     where sp.code = 'GATE'
      into :spid;

    execute procedure wh_ttid_gateauto returning_values :ttid_gateauto;

    for
        with gate as (
            select s.siteid as id,s.name as name
              from site s
             where s.sitespeciesid = :spid
               and s.status = '1'
               and exists(select *
                            from sitezone_items szi
                                 left join sitezone_employees sze on sze.zoneid = szi.zoneid
                           where szi.siteid = s.siteid
                             and sze.employeeid = :objid)
        )
        select gate.id, gate.name,
               t.taskid,ta.aid,ta.name,t.plandatetime,t.priority,t.begintime
          from gate
               left join wm_task t
                    left join t_auto ta on ta.aid = t.infoid
                 on t.tasktypeid = :ttid_gateauto and t.status = '1' and t.siteid = :gid
         order by t.priority ascending nulls last,
                  t.plandatetime ascending,
                  t.begintime ascending,
                  gate.name ascending
          into :gid,:gname,:tid,:aid,:aname,:tplandt,:tpriority,:tbegintime
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_GETNEXTTASK (
    WMSID R_ID)
returns (
    TID type of R_ID,
    TNUMBER type of R_SHORTNAME,
    TSNAME type of R_NAME,
    DNUM type of DOCNUMBER,
    DDATE type of R_DATE,
    CLIENTNAME type of R_NAME,
    WHNAME type of R_NAME,
    TUID type of R_ID,
    TUNAME type of R_NAME,
    GOTOTASK type of R_FLAG)
AS
declare variable taskid_gateauto r_id;
declare variable taskid_select r_id;
declare variable taskid_loadauto r_id;
declare variable ttid_loadpallet r_id;
declare variable ttid_loadauto r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_cardocs r_id;
declare variable tbtid_loadselect r_id;
begin
    execute procedure wh_ttid_loadpallet returning_values :ttid_loadpallet;

    -- 1- ищем прив€занное задание погрузки поддона
    select t.taskid
      from wm_task t
     where t.wm_sessionid = :wmsid
       and t.status = '1'
       and t.tasktypeid = :ttid_loadpallet
      into :tid;

    -- 2 - ищем задание погрузки поддона из прив€занных заданий на погрузку документа
    if (:tid is NULL) then
    begin
        execute procedure wh_ttid_loadauto returning_values :ttid_loadauto;

        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'CARDOCS'
          into :tbtid_cardocs;
        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'LOADSELECT'
          into :tbtid_loadselect;

        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'DOCPALLETS'
          into :tbtid_docpallets;

        for
            select t.taskid
              from wm_task t
                   left join wh_taskbond tb
                        left join wm_task t1 on t1.taskid = tb.task1id
                     on tb.task2id = t.taskid and tb.taskbondtid = :tbtid_cardocs
             where t.wm_sessionid = :wmsid
               and t.status = '1'
               and t.tasktypeid = :ttid_loadauto
             order by t1.priority ascending nulls last,
                      t1.plandatetime ascending,
                      t1.begintime ascending,
                      t.priority ascending nulls last,
                      t.docid
              into :taskid_loadauto
        do
        begin
            select first(1) t.taskid
              from wh_taskbond tb
                   left join wm_task t
                        left join wh_taskbond tb2
                             left join wm_task t2 on t2.taskid = tb2.task2id
                          on tb2.task1id = t.taskid and tb2.taskbondtid = :tbtid_loadselect
                     on t.taskid = tb.task2id
             where tb.task1id = :taskid_loadauto
               and tb.taskbondtid = :tbtid_docpallets
               and t.status <> '2'
             order by t2.endtime descending nulls last, t.num ascending
               into :tid;

            if (:tid is NOT NULL) then
                break;
        end
    end

    -- ≈сли нашли - вернули
    if (:tid is NOT NULL) then
    begin
        select ti.TNUMBER,ti.TSNAME,ti.DNUM,ti.DDATE,
               ti.CLIENTNAME,ti.whname,
               ti.TUID, ti.TUNAME
          from wh_loadpalletdc_taskinfo(:tid) ti
          into :TNUMBER,:TSNAME,:DNUM,:DDATE,:CLIENTNAME,:WHNAME,:TUID,:TUNAME;

        gototask = '1';
        suspend; exit;
    end

    -- »наче ищем среди всех не прив€занных
    gototask = '0';
    for
        select g.tid
          from WH_LOADAUTODC_LISTGATES(:wmsid) g
          into :taskid_gateauto
    do
    begin
        for
            select w.TID,w.TNUMBER,w.TSNAME,w.TID_SELECT,w.DNUM,w.DDATE,w.CLIENTNAME,w.WHNAME
              from wh_loadautodc_listpallets(:taskid_gateauto) w
                   left join wm_task t on t.taskid = w.tid_loadauto
             where w.TSTAT = '0'
--               and w.DSTAT = '2'
               and (t.status = '0' or (t.status='1' and t.wm_sessionid is NULL))
             order by w.tpriority ascending,
                   w.tend_select descending nulls last,w.tnum_select ascending
              into :tid,:tnumber,:tsname,:taskid_select,:dnum,:ddate,:clientname,:whname
        do
        begin
            tuid = NULL;
            tuname = NULL;

            select tu.tuid,tu.name
              from wm_task_transunit ttu
                   left join wh_transport_unit tu on tu.tuid = ttu.tunitid
             where ttu.taskid = :taskid_select
              into :tuid,:tuname;

            suspend;
            exit;
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_LISTGATES (
    WMSESID R_ID)
returns (
    GID R_ID,
    GNAME R_NAME,
    TID R_ID,
    AID R_ID,
    ANAME R_NAME,
    TPLANDT R_DATETIME)
AS
declare variable tbtid_cardocs r_id;
BEGIN
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    For
        select w.GID,w.GNAME,w.TID,w.AID,w.ANAME,w.TPLANDT
          from wh_loadautodc_listgates(:wmsesid) w
         where exists(select *
                        from wh_taskbond tb
                             left join wm_task t on t.taskid = tb.task2id
                       where tb.task1id = w.tid
                         and tb.taskbondtid = :tbtid_cardocs
                         and t.status = '0'
                         and t.wm_sessionid is NULL)
          into :GID,:GNAME,:TID,:AID,:ANAME,:TPLANDT
    do
        suspend;

END^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADAUTODC_LISTGATES (
    WMSESID type of column WM_SESSION.sessionid
)
returns (
    GID type of column SITE.siteid ,
    GNAME type of column SITE.name,
    TID type of column WM_TASK.taskid,
    AID type of column T_AUTO.aid,
    ANAME type of column T_AUTO.name,
    TPLANDT type of column WM_TASK.plandatetime,
    TPRIORITY type of column WM_TASK.priority,
    TBEGINTIME type of column WM_TASK.begintime
)
AS
declare variable objid type of column OBJECT.objid;
declare variable spid type of column sitespecies.sitespeciesid;
declare variable ttid_gateauto type of column WM_TASKTYPE.tasktypeid;
begin
    select wms.objid
      from wm_session wms
     where wms.sessionid = :wmsesid
      into :objid;

    select sp.sitespeciesid
      from sitespecies sp
     where sp.code = 'GATE'
      into :spid;

    execute procedure wh_ttid_gateauto returning_values :ttid_gateauto;

    for
        with gate as (
            select s.siteid as id,s.name as name
              from site s
             where s.sitespeciesid = :spid
               and s.status = '1'
               and exists(select *
                            from sitezone_items szi
                                 left join sitezone_employees sze on sze.zoneid = szi.zoneid
                           where szi.siteid = s.siteid
                             and sze.employeeid = :objid)
        )
        select gate.id, gate.name,
               t.taskid,ta.aid,ta.name,t.plandatetime,t.priority,t.begintime
          from gate
               left join wm_task t
                    left join t_auto ta on ta.aid = t.infoid
                 on t.tasktypeid = :ttid_gateauto and t.status = '1' and t.siteid = :gid
         where t.taskid is NOT NULL
         order by t.priority ascending nulls last,
                  t.plandatetime ascending,
                  t.begintime ascending,
                  gate.name ascending
          into :gid,:gname,:tid,:aid,:aname,:tplandt,:tpriority,:tbegintime
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_LISTGATES (
    WMSESID R_ID)
returns (
    GID R_ID,
    GNAME R_NAME,
    TID R_ID,
    AID R_ID,
    ANAME R_NAME,
    TPLANDT R_DATETIME)
AS
declare variable tbtid_cardocs r_id;
BEGIN
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    For
        select w.GID,w.GNAME,w.TID,w.AID,w.ANAME,w.TPLANDT
          from wh_loadautodc_listgates(:wmsesid) w
         where exists(select *
                        from wh_taskbond tb
                             left join wm_task t on t.taskid = tb.task2id
                       where tb.task1id = w.tid
                         and tb.taskbondtid = :tbtid_cardocs
                         and t.status = '0'
                         and t.wm_sessionid is NULL)
          into :GID,:GNAME,:TID,:AID,:ANAME,:TPLANDT
    do
        suspend;

END^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_GETNEXTTASK (
    WMSID R_ID)
returns (
    TID type of R_ID,
    TNUMBER type of R_SHORTNAME,
    TSNAME type of R_NAME,
    DNUM type of DOCNUMBER,
    DDATE type of R_DATE,
    CLIENTNAME type of R_NAME,
    WHNAME type of R_NAME,
    TUID type of R_ID,
    TUNAME type of R_NAME,
    GOTOTASK type of R_FLAG)
AS
declare variable taskid_gateauto r_id;
declare variable taskid_select r_id;
declare variable taskid_loadauto r_id;
declare variable ttid_loadpallet r_id;
declare variable ttid_loadauto r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_cardocs r_id;
declare variable tbtid_loadselect r_id;
begin
    execute procedure wh_ttid_loadpallet returning_values :ttid_loadpallet;

    -- 1- ищем прив€занное задание погрузки поддона
    select t.taskid
      from wm_task t
     where t.wm_sessionid = :wmsid
       and t.status = '1'
       and t.tasktypeid = :ttid_loadpallet
      into :tid;

    -- 2 - ищем задание погрузки поддона из прив€занных заданий на погрузку документа
    if (:tid is NULL) then
    begin
        execute procedure wh_ttid_loadauto returning_values :ttid_loadauto;

        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'CARDOCS'
          into :tbtid_cardocs;
        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'LOADSELECT'
          into :tbtid_loadselect;

        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'DOCPALLETS'
          into :tbtid_docpallets;

        for
            select t.taskid
              from wm_task t
                   left join wh_taskbond tb
                        left join wm_task t1 on t1.taskid = tb.task1id
                     on tb.task2id = t.taskid and tb.taskbondtid = :tbtid_cardocs
             where t.wm_sessionid = :wmsid
               and t.status = '1'
               and t.tasktypeid = :ttid_loadauto
             order by t1.priority ascending nulls last,
                      t1.plandatetime ascending,
                      t1.begintime ascending,
                      t.priority ascending nulls last,
                      t.docid
              into :taskid_loadauto
        do
        begin
            select first(1) t.taskid
              from wh_taskbond tb
                   left join wm_task t
                        left join wh_taskbond tb2
                             left join wm_task t2 on t2.taskid = tb2.task2id
                          on tb2.task1id = t.taskid and tb2.taskbondtid = :tbtid_loadselect
                     on t.taskid = tb.task2id
             where tb.task1id = :taskid_loadauto
               and tb.taskbondtid = :tbtid_docpallets
               and t.status <> '2'
             order by t2.endtime descending nulls last, t.num ascending
               into :tid;

            if (:tid is NOT NULL) then
                break;
        end
    end

    -- ≈сли нашли - вернули
    if (:tid is NOT NULL) then
    begin
        select ti.TNUMBER,ti.TSNAME,ti.DNUM,ti.DDATE,
               ti.CLIENTNAME,ti.whname,
               ti.TUID, ti.TUNAME
          from wh_loadpalletdc_taskinfo(:tid) ti
          into :TNUMBER,:TSNAME,:DNUM,:DDATE,:CLIENTNAME,:WHNAME,:TUID,:TUNAME;

        gototask = '1';
        suspend; exit;
    end

    -- »наче ищем среди всех не прив€занных
    gototask = '0';
    for
        select g.tid
          from WH_LOADAUTODC_LISTGATES(:wmsid) g
          into :taskid_gateauto
    do
    begin
        for
            select w.TID,w.TNUMBER,w.TSNAME,w.TID_SELECT,w.DNUM,w.DDATE,w.CLIENTNAME,w.WHNAME
              from wh_loadautodc_listpallets(:taskid_gateauto) w
                   left join wm_task t on t.taskid = w.tid_loadauto
             where w.TSTAT = '0'
--               and w.DSTAT = '2'
               and (t.status = '0' or (t.status='1' and t.wm_sessionid is NULL))
             order by w.tpriority ascending,
                   w.tend_select descending nulls last,w.tnum_select ascending
              into :tid,:tnumber,:tsname,:taskid_select,:dnum,:ddate,:clientname,:whname
        do
        begin
            tuid = NULL;
            tuname = NULL;

            select tu.tuid,tu.name
              from wm_task_transunit ttu
                   left join wh_transport_unit tu on tu.tuid = ttu.tunitid
             where ttu.taskid = :taskid_select
              into :tuid,:tuname;

            suspend;
            exit;
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADAUTODC_LISTGATES (
    WMSESID type of column WM_SESSION.SESSIONID)
returns (
    GID type of column SITE.SITEID,
    GNAME type of column SITE.NAME,
    TID type of column WM_TASK.TASKID,
    AID type of column T_AUTO.AID,
    ANAME type of column T_AUTO.NAME,
    TPLANDT type of column WM_TASK.PLANDATETIME,
    TPRIORITY type of column WM_TASK.PRIORITY,
    TBEGINTIME type of column WM_TASK.BEGINTIME)
AS
declare variable objid type of column OBJECT.objid;
declare variable spid type of column sitespecies.sitespeciesid;
declare variable ttid_gateauto type of column WM_TASKTYPE.tasktypeid;
begin
    select wms.objid
      from wm_session wms
     where wms.sessionid = :wmsesid
      into :objid;

    select sp.sitespeciesid
      from sitespecies sp
     where sp.code = 'GATE'
      into :spid;

    execute procedure wh_ttid_gateauto returning_values :ttid_gateauto;

    for
        with gate as (
            select s.siteid as id,s.name as name
              from site s
             where s.sitespeciesid = :spid
               and s.status = '1'
               and exists(select *
                            from sitezone_items szi
                                 left join sitezone_employees sze on sze.zoneid = szi.zoneid
                           where szi.siteid = s.siteid
                             and sze.employeeid = :objid)
        )
        select gate.id, gate.name,
               t.taskid,ta.aid,ta.name,t.plandatetime,t.priority,t.begintime
          from gate
               left join wm_task t
                    left join t_auto ta on ta.aid = t.infoid
                 on t.tasktypeid = :ttid_gateauto and t.status = '1' and t.siteid = gate.id
         where t.taskid is NOT NULL
         order by t.priority ascending nulls last,
                  t.plandatetime ascending,
                  t.begintime ascending,
                  gate.name ascending
          into :gid,:gname,:tid,:aid,:aname,:tplandt,:tpriority,:tbegintime
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



DROP PROCEDURE WH_LOADAUTODC_PALLETCANC;




SET TERM ^ ;

CREATE OR ALTER procedure K_WH_TASKINFO (
    TASKID type of column WM_TASK.TASKID)
returns (
    TID type of column WM_TASK.TASKID,
    TSTAT type of column R_STATUS.CODE,
    TCAPACITY type of column WM_TASK.CAPACITY,
    TPRIORITY type of column WM_TASK.priority,
    SITEID type of column SITE.SITEID,
    SNAME type of column SITE.NAME,
    DOCID type of column DOCUMENT.DOCID,
    DOCNUM type of column DOCUMENT.NUMBER,
    DOCDATE type of R_DATE,
    DOCSTAT type of column R_STATUS.CODE,
    ALGORITHM type of column WM_TASKMETHOD.ALGORITHM,
    FROMID type of column OBJECT.OBJID,
    FROMNAME type of R_FULLNAME,
    THROUGHID type of column OBJECT.OBJID,
    THROUGHNAME type of R_FULLNAME,
    TOID type of column OBJECT.OBJID,
    TONAME type of R_FULLNAME,
    INFOID type of column WM_TASK.INFOID,
    INFOTYPECODE type of column WH_TASKINFOTYPE.CODE,
    INFONAME varchar(1023),
    PLANDT type of column WM_TASK.PLANDATETIME)
AS
begin
    select t.taskid,t.siteid, t.status,t.capacity,t.priority,
           d.docid,d.docdate,d.number,d.status,tm.algorithm,
           d.fromobj,(select fullname from getobjectname(d.fromobj,NULL)),
           d.throughobj,(select fullname from getobjectname(d.throughobj,NULL)),
           d.toobj,(select fullname from getobjectname(d.toobj,NULL)),
           t.infoid,s.name,tit.code,t.plandatetime,ig.info
      from wm_task t
           left join wm_taskmethod tm on tm.methodid=t.taskmethodid
           left join document d on d.docid=t.docid
           left join site s on s.siteid = t.siteid
           left join wh_taskinfotype tit on tit.id = t.typeinfoid
           left join wh_id_getinfo(t.infoid,t.typeinfoid) ig on 1=1
     where t.taskid = :taskid
      into :tid,:siteid,:tstat,:tcapacity,:tpriority,
           :docid,:docdate,:docnum,:docstat,:algorithm,
           :fromid, :fromname,
           :throughid, :throughname,
           :toid, :toname,
           :infoid,:sname,:infotypecode,:plandt,:infoname;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_TASKPRIORITY_SET (
    TASKID type of column wm_task.taskid,
    PRIORITY type of column wm_task.priority
)
as
begin
    if (exists(select *
                 from wm_task t
                where t.taskid = :taskid
                  and t.status = '2' )) then
        exception exc_wh_wrongstatus '—татус задани€ не позвол€ет изменение приоритета';


    if (:priority < 0.0000001) then
        priority = NULL;

    update wm_task t
       set t.priority = :priority
     where t.taskid = :taskid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_LISTGATES (
    WMSESID type of column WM_SESSION.sessionid
)
returns (
    GID type of column SITE.siteid,
    GNAME type of column SITE.name,
    TID type of column WM_TASK.taskid,
    AID type of column T_AUTO.aid,
    ANAME type of column T_AUTO.name ,
    TPLANDT type of column WM_TASK.plandatetime,
    TPRIORITY type of column WM_TASK.priority
)
AS
declare variable tbtid_cardocs r_id;
BEGIN
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    For
        select w.GID,w.GNAME,w.TID,w.AID,w.ANAME,w.TPLANDT,w.tpriority
          from wh_loadautodc_listgates(:wmsesid) w
         where exists(select *
                        from wh_taskbond tb
                             left join wm_task t on t.taskid = tb.task2id
                       where tb.task1id = w.tid
                         and tb.taskbondtid = :tbtid_cardocs
                         and t.status = '0'
                         and t.wm_sessionid is NULL)
          into :GID,:GNAME,:TID,:AID,:ANAME,:TPLANDT,:tpriority
    do
        suspend;

END^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_LOADAUTODC_PSELECT_INFO (
    PALLETID type of column PALLET.palletid
)
returns (
    TID_SELECT type of column WM_TASK.taskid,
    TSTAT_SELECT type of column R_STATUS.code,
    TID_LOADPALLET type of column WM_TASK.taskid,
    TSTAT_LOADPALLET type of column R_STATUS.CODE,
    TID_LOADDOC type of column WM_TASK.taskid,
    TID_GATEAUTO type of column WM_TASK.taskid,
    GID type of column SITE.siteid,
    GNAME type of column SITE.name,
    TNUMBER type of R_SHORTNAME,
    TSNAME type of R_NAME,
    DNUM type of column DOCUMENT.number,
    DDATE type of R_DATE,
    CLIENTNAME type of R_FULLNAME,
    TUID type of column wh_transport_unit.tuid,
    TUNAME type of column wh_transport_unit.name,
    TUSTAT_TASK type of R_STATUS,
    AID type of column T_AUTO.aid,
    ANAME type of column T_AUTO.name,
    TSTAT_GATEAUTO type of column R_STATUS.CODE
)
AS
declare variable tbtid_loadselect r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_CARDOCS r_id;
declare variable ttid_select r_id;
begin
    select ps.taskid
      from pallet_select ps
     where ps.palletid = :palletid
      into :tid_select;

  if (:tid_select is NULL) then
    exception exc_k_wrongtasktype;

  execute procedure wh_ttid_select returning_values :ttid_select;

  select s.name,t.status,
         (select numpallet from wh_selectdc_getnumpallet(t.taskid)),
         d.number,d.docdate,(select fullname from getobjectname(d.toobj,NULL))
    from wm_task t
         left join site s on s.siteid = t.siteid
         left join document d on d.docid = t.docid
   where t.taskid = :tid_select
     and t.tasktypeid = :ttid_select
    into :tsname,:tstat_select,
         :tnumber,:dnum,:ddate,:clientname;

  if (:tstat_select <> '2') then
    exception exc_k_wrongtaskstat;

  select tu.tuid,tu.name
    from wm_task_transunit ttu
         left join wh_transport_unit tu on tu.tuid = ttu.tunitid
   where ttu.taskid = :tid_select
    into :tuid,:tuname;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'LOADSELECT'
    into :tbtid_loadselect;

  select t.taskid,t.status
    from wh_taskbond tb
         left join wm_task t on t.taskid = tb.task1id
   where tb.task2id = :tid_select
     and tb.taskbondtid = :tbtid_loadselect
    into :tid_loadpallet,:tstat_loadpallet;

  if (exists(select *
               from wm_task_transunit ttu
              where ttu.taskid = :tid_loadpallet
                and ttu.tunitid = :tuid
                and ttu.status = 'a')) then
     tustat_task = '2';
  else
     tustat_task = '0';


  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'DOCPALLETS'
    into :tbtid_docpallets;

  select ta.aid,ta.name,t.taskid
    from wh_taskbond tb
         left join wm_task t
              left join t_auto ta on ta.aid = t.infoid
           on t.taskid = tb.task1id
   where tb.task2id = :tid_loadpallet
     and tb.taskbondtid = :tbtid_docpallets
    into :aid,:aname,:tid_loaddoc;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :tbtid_CARDOCS;

  select t.taskid,t.status,s.siteid,s.name
    from wh_taskbond tb
         left join wm_task t
              left join site s on s.siteid = t.siteid
           on t.taskid = tb.task1id
   where tb.task2id = :tid_loaddoc
     and tb.taskbondtid = :tbtid_CARDOCS
    into :tid_gateauto,:tstat_gateauto,:gid,:gname;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADAUTODC_PSELECT_INFO (
    PALLETID type of column PALLET.palletid
)
returns (
    TID_SELECT type of column WM_TASK.taskid,
    TSTAT_SELECT type of column R_STATUS.code,
    TID_LOADPALLET type of column WM_TASK.taskid,
    TSTAT_LOADPALLET type of column R_STATUS.CODE,
    TID_LOADDOC type of column WM_TASK.taskid,
    TID_GATEAUTO type of column WM_TASK.taskid,
    GID type of column SITE.siteid,
    GNAME type of column SITE.name,
    PNUMBER type of column PALLET.number,
    TSNAME type of R_NAME,
    DNUM type of column DOCUMENT.number,
    DDATE type of R_DATE,
    CLIENTNAME type of R_FULLNAME,
    TUID type of column wh_transport_unit.tuid,
    TUNAME type of column wh_transport_unit.name,
    TUSTAT_TASK type of R_STATUS,
    AID type of column T_AUTO.aid,
    ANAME type of column T_AUTO.name,
    TSTAT_GATEAUTO type of column R_STATUS.CODE
)
AS
declare variable tbtid_loadselect r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_CARDOCS r_id;
declare variable ttid_select r_id;
begin
    select ps.taskid
      from pallet_select ps
     where ps.palletid = :palletid
      into :tid_select;

  if (:tid_select is NULL) then
    exception exc_k_wrongtasktype;

  execute procedure wh_ttid_select returning_values :ttid_select;

  select s.name,t.status,
         d.number,d.docdate,(select fullname from getobjectname(d.toobj,NULL))
    from wm_task t
         left join site s on s.siteid = t.siteid
         left join document d on d.docid = t.docid
   where t.taskid = :tid_select
     and t.tasktypeid = :ttid_select
    into :tsname,:tstat_select,
         :dnum,:ddate,:clientname;

  if (:tstat_select <> '2') then
    exception exc_k_wrongtaskstat;

  select tu.tuid,tu.name
    from wm_task_transunit ttu
         left join wh_transport_unit tu on tu.tuid = ttu.tunitid
   where ttu.taskid = :tid_select
    into :tuid,:tuname;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'LOADSELECT'
    into :tbtid_loadselect;

  select t.taskid,t.status
    from wh_taskbond tb
         left join wm_task t on t.taskid = tb.task1id
   where tb.task2id = :tid_select
     and tb.taskbondtid = :tbtid_loadselect
    into :tid_loadpallet,:tstat_loadpallet;

  if (exists(select *
               from wm_task_transunit ttu
              where ttu.taskid = :tid_loadpallet
                and ttu.tunitid = :tuid
                and ttu.status = 'a')) then
     tustat_task = '2';
  else
     tustat_task = '0';


  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'DOCPALLETS'
    into :tbtid_docpallets;

  select ta.aid,ta.name,t.taskid
    from wh_taskbond tb
         left join wm_task t
              left join t_auto ta on ta.aid = t.infoid
           on t.taskid = tb.task1id
   where tb.task2id = :tid_loadpallet
     and tb.taskbondtid = :tbtid_docpallets
    into :aid,:aname,:tid_loaddoc;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :tbtid_CARDOCS;

  select t.taskid,t.status,s.siteid,s.name
    from wh_taskbond tb
         left join wm_task t
              left join site s on s.siteid = t.siteid
           on t.taskid = tb.task1id
   where tb.task2id = :tid_loaddoc
     and tb.taskbondtid = :tbtid_CARDOCS
    into :tid_gateauto,:tstat_gateauto,:gid,:gname;

  select p.number
    from pallet p
   where p.palletid = :palletid
    into :pnumber;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADAUTODC_PSELECT_INFO (
    PALLETID type of column PALLET.palletid
)
returns (
    TID_SELECT type of column WM_TASK.taskid,
    TSTAT_SELECT type of column R_STATUS.code,
    TID_LOADPALLET type of column WM_TASK.taskid,
    TSTAT_LOADPALLET type of column R_STATUS.CODE,
    TID_LOADDOC type of column WM_TASK.taskid,
    TID_GATEAUTO type of column WM_TASK.taskid,
    GID type of column SITE.siteid,
    GNAME type of column SITE.name,
    PNUMBER type of column PALLET.number,
    SNAME type of column SITE.name,
    DNUM type of column DOCUMENT.number,
    DDATE type of R_DATE,
    CLIENTNAME type of R_FULLNAME,
    TUID type of column wh_transport_unit.tuid,
    TUNAME type of column wh_transport_unit.name,
    TUSTAT_TASK type of R_STATUS,
    AID type of column T_AUTO.aid,
    ANAME type of column T_AUTO.name,
    TSTAT_GATEAUTO type of column R_STATUS.CODE
)
AS
declare variable tbtid_loadselect r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_CARDOCS r_id;
declare variable ttid_select r_id;
begin
    select ps.taskid
      from pallet_select ps
     where ps.palletid = :palletid
      into :tid_select;

  if (:tid_select is NULL) then
    exception exc_k_wrongtasktype;

  execute procedure wh_ttid_select returning_values :ttid_select;

  select t.status,d.number,d.docdate,(select fullname from getobjectname(d.toobj,NULL))
    from wm_task t
         left join document d on d.docid = t.docid
   where t.taskid = :tid_select
     and t.tasktypeid = :ttid_select
    into :tstat_select,:dnum,:ddate,:clientname;

  if (:tstat_select <> '2') then
    exception exc_k_wrongtaskstat;

  select tu.tuid,tu.name
    from wm_task_transunit ttu
         left join wh_transport_unit tu on tu.tuid = ttu.tunitid
   where ttu.taskid = :tid_select
    into :tuid,:tuname;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'LOADSELECT'
    into :tbtid_loadselect;

  select t.taskid,t.status
    from wh_taskbond tb
         left join wm_task t on t.taskid = tb.task1id
   where tb.task2id = :tid_select
     and tb.taskbondtid = :tbtid_loadselect
    into :tid_loadpallet,:tstat_loadpallet;

  if (exists(select *
               from wm_task_transunit ttu
              where ttu.taskid = :tid_loadpallet
                and ttu.tunitid = :tuid
                and ttu.status = 'a')) then
     tustat_task = '2';
  else
     tustat_task = '0';


  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'DOCPALLETS'
    into :tbtid_docpallets;

  select ta.aid,ta.name,t.taskid
    from wh_taskbond tb
         left join wm_task t
              left join t_auto ta on ta.aid = t.infoid
           on t.taskid = tb.task1id
   where tb.task2id = :tid_loadpallet
     and tb.taskbondtid = :tbtid_docpallets
    into :aid,:aname,:tid_loaddoc;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :tbtid_CARDOCS;

  select t.taskid,t.status,s.siteid,s.name
    from wh_taskbond tb
         left join wm_task t
              left join site s on s.siteid = t.siteid
           on t.taskid = tb.task1id
   where tb.task2id = :tid_loaddoc
     and tb.taskbondtid = :tbtid_CARDOCS
    into :tid_gateauto,:tstat_gateauto,:gid,:gname;

  select p.number, s.name
    from pallet p
         left join site s on s.siteid = p.siteid
   where p.palletid = :palletid
    into :pnumber, :sname;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADAUTODC_PSELECT_INFO (
    PALLETID type of column PALLET.palletid
)
returns (
    TID_SELECT type of column WM_TASK.taskid,
    TSTAT_SELECT type of column R_STATUS.code,
    TID_LOADPALLET type of column WM_TASK.taskid,
    TSTAT_LOADPALLET type of column R_STATUS.CODE,
    TID_LOADDOC type of column WM_TASK.taskid,
    TID_GATEAUTO type of column WM_TASK.taskid,
    GID type of column SITE.siteid,
    GNAME type of column SITE.name,
    PNUMBER type of column PALLET.number,
    SNAME type of column SITE.name,
    DNUM type of column DOCUMENT.number,
    DDATE type of R_DATE,
    CLIENTNAME type of R_FULLNAME,
    TUID type of column wh_transport_unit.tuid,
    TUNAME type of column wh_transport_unit.name,
    TUSTAT_TASK type of R_STATUS,
    AID type of column T_AUTO.aid,
    ANAME type of column T_AUTO.name,
    TSTAT_GATEAUTO type of column R_STATUS.CODE,
    PLANDATETIME type of column WM_TASK.plandatetime,
    MANLOAD type of R_FULLNAME,
    MANSELECT type of R_FULLNAME,
    MANLOADDOC type of R_FULLNAME
)
AS
declare variable tbtid_loadselect r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_CARDOCS r_id;
declare variable ttid_select r_id;
begin
    select ps.taskid
      from pallet_select ps
     where ps.palletid = :palletid
      into :tid_select;

  if (:tid_select is NULL) then
    exception exc_k_wrongtasktype;

  execute procedure wh_ttid_select returning_values :ttid_select;

  select t.status,d.number,d.docdate,(select fullname from getobjectname(d.toobj,NULL)),
         (select objname from wh_get_objectname(wms.sessionid))
    from wm_task t
         left join wm_session wms on wms.sessionid = t.wm_sessionid
         left join document d on d.docid = t.docid
   where t.taskid = :tid_select
     and t.tasktypeid = :ttid_select
    into :tstat_select,:dnum,:ddate,:clientname,:manselect;

  if (:tstat_select <> '2') then
    exception exc_k_wrongtaskstat;

  select tu.tuid,tu.name
    from wm_task_transunit ttu
         left join wh_transport_unit tu on tu.tuid = ttu.tunitid
   where ttu.taskid = :tid_select
    into :tuid,:tuname;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'LOADSELECT'
    into :tbtid_loadselect;

  select t.taskid,t.status, (select objname from wh_get_objectname(wms.objid))
    from wh_taskbond tb
         left join wm_task t
              left join wm_session wms on wms.sessionid = t.wm_sessionid
           on t.taskid = tb.task1id
   where tb.task2id = :tid_select
     and tb.taskbondtid = :tbtid_loadselect
    into :tid_loadpallet, :tstat_loadpallet, :manload;

  if (exists(select *
               from wm_task_transunit ttu
              where ttu.taskid = :tid_loadpallet
                and ttu.tunitid = :tuid
                and ttu.status = 'a')) then
     tustat_task = '2';
  else
     tustat_task = '0';


  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'DOCPALLETS'
    into :tbtid_docpallets;

  select ta.aid,ta.name,t.taskid,
         (select objname from wh_get_objectname(wms.objid))
    from wh_taskbond tb
         left join wm_task t
              left join wm_session wms on wms.sessionid = t.wm_sessionid
              left join t_auto ta on ta.aid = t.infoid
           on t.taskid = tb.task1id
   where tb.task2id = :tid_loadpallet
     and tb.taskbondtid = :tbtid_docpallets
    into :aid,:aname,:tid_loaddoc,:manloaddoc;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :tbtid_CARDOCS;

  select t.taskid,t.status,s.siteid,s.name,t.plandatetime
    from wh_taskbond tb
         left join wm_task t
              left join site s on s.siteid = t.siteid
           on t.taskid = tb.task1id
   where tb.task2id = :tid_loaddoc
     and tb.taskbondtid = :tbtid_CARDOCS
    into :tid_gateauto,:tstat_gateauto,:gid,:gname,:plandatetime;

  select p.number, s.name
    from pallet p
         left join site s on s.siteid = p.siteid
   where p.palletid = :palletid
    into :pnumber, :sname;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADAUTODC_PSELECT_INFO (
    PALLETID type of column PALLET.palletid
)
returns (
    TID_SELECT type of column WM_TASK.taskid,
    TSTAT_SELECT type of column R_STATUS.code,
    TID_LOADPALLET type of column WM_TASK.taskid,
    TSTAT_LOADPALLET type of column R_STATUS.CODE,
    TID_LOADDOC type of column WM_TASK.taskid,
    TID_GATEAUTO type of column WM_TASK.taskid,
    GID type of column SITE.siteid,
    GNAME type of column SITE.name,
    PNUMBER type of column PALLET.number,
    SNAME type of column SITE.name,
    DNUM type of column DOCUMENT.number,
    DDATE type of R_DATE,
    CLIENTNAME type of R_FULLNAME,
    TUID type of column wh_transport_unit.tuid,
    TUNAME type of column wh_transport_unit.name,
    TUSTAT_TASK type of R_STATUS,
    AID type of column T_AUTO.aid,
    ANAME type of column T_AUTO.name,
    TSTAT_GATEAUTO type of column R_STATUS.CODE,
    PLANDATETIME type of column WM_TASK.plandatetime,
    MANLOAD type of R_FULLNAME,
    MANSELECT type of R_FULLNAME,
    MANLOADDOC type of R_FULLNAME
)
AS
declare variable tbtid_loadselect r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_CARDOCS r_id;
declare variable ttid_select r_id;
begin
    select ps.taskid
      from pallet_select ps
     where ps.palletid = :palletid
      into :tid_select;

  if (:tid_select is NULL) then
    exception exc_k_wrongtasktype;

  execute procedure wh_ttid_select returning_values :ttid_select;

  select t.status,d.number,d.docdate,(select fullname from getobjectname(d.toobj,NULL)),
         (select objname from wh_get_objectname(wms.objid))
    from wm_task t
         left join wm_session wms on wms.sessionid = t.wm_sessionid
         left join document d on d.docid = t.docid
   where t.taskid = :tid_select
     and t.tasktypeid = :ttid_select
    into :tstat_select,:dnum,:ddate,:clientname,:manselect;

  if (:tstat_select <> '2') then
    exception exc_k_wrongtaskstat;

  select tu.tuid,tu.name
    from wm_task_transunit ttu
         left join wh_transport_unit tu on tu.tuid = ttu.tunitid
   where ttu.taskid = :tid_select
    into :tuid,:tuname;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'LOADSELECT'
    into :tbtid_loadselect;

  select t.taskid,t.status, (select objname from wh_get_objectname(wms.objid))
    from wh_taskbond tb
         left join wm_task t
              left join wm_session wms on wms.sessionid = t.wm_sessionid
           on t.taskid = tb.task1id
   where tb.task2id = :tid_select
     and tb.taskbondtid = :tbtid_loadselect
    into :tid_loadpallet, :tstat_loadpallet, :manload;

  if (exists(select *
               from wm_task_transunit ttu
              where ttu.taskid = :tid_loadpallet
                and ttu.tunitid = :tuid
                and ttu.status = 'a')) then
     tustat_task = '2';
  else
     tustat_task = '0';


  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'DOCPALLETS'
    into :tbtid_docpallets;

  select ta.aid,ta.name,t.taskid,
         (select objname from wh_get_objectname(wms.objid))
    from wh_taskbond tb
         left join wm_task t
              left join wm_session wms on wms.sessionid = t.wm_sessionid
              left join t_auto ta on ta.aid = t.infoid
           on t.taskid = tb.task1id
   where tb.task2id = :tid_loadpallet
     and tb.taskbondtid = :tbtid_docpallets
    into :aid,:aname,:tid_loaddoc,:manloaddoc;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :tbtid_CARDOCS;

  select t.taskid,t.status,s.siteid,s.name,t.plandatetime
    from wh_taskbond tb
         left join wm_task t
              left join site s on s.siteid = t.siteid
           on t.taskid = tb.task1id
   where tb.task2id = :tid_loaddoc
     and tb.taskbondtid = :tbtid_CARDOCS
    into :tid_gateauto,:tstat_gateauto,:gid,:gname,:plandatetime;

  select p.number, s.name
    from pallet p
         left join site s on s.siteid = p.siteid
   where p.palletid = :palletid
    into :pnumber, :sname;

  suspend;
end^

SET TERM ; ^



DROP PROCEDURE WH_LOADAUTODC_TASKSELINFO;

