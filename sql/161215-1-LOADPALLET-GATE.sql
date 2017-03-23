

SET TERM ^ ;

CREATE OR ALTER procedure RBS_TASKVIEW_LISTTASK (
    TTID_IN type of R_ID,
    TBEG_IN type of R_DATETIME,
    TEND_IN type of R_DATETIME,
    MANID_IN type of R_ID,
    DOCID_IN type of R_ID64,
    TSTATUS_IN char(1))
returns (
    TID type of R_ID,
    DOCID type of R_ID64,
    TSTAT type of R_STATUS,
    TSTATNAME type of R_NAME,
    TTID type of R_ID,
    TTCODE type of R_CODE,
    TTNAME type of R_NAME,
    TMID type of R_ID,
    TMALGORITHM type of R_FLAG,
    TMNAME type of R_NAME,
    CREATETIME type of R_DATETIME,
    ENDTIME type of R_DATETIME,
    BEGINTIME type of R_DATETIME,
    MANID type of R_ID,
    MANFIO type of R_FULLNAME,
    SITENAME type of column SITE.name
)
AS
declare variable wmsesid type of r_id;
begin
    if (:manid_in is not null) then
    begin
      select wms.sessionid
        from wm_session wms
       where wms.objid = :manid_in
             and wms.disconnecttime is null
        into :wmsesid;
    end 
    --docid = :adocid;

    for
        select t.taskid,t.status,rs.name,
               tt.tasktypeid,tt.code,tt.name,
               tm.methodid,tm.algorithm,tm.name,
               t.createtime,t.endtime,t.begintime,
               wms.objid,m.fullname,
               t.docid, s.name
          from wm_task t
               left join document d on d.docid = t.docid
               left join wm_tasktype tt on tt.tasktypeid=t.tasktypeid
               left join wm_taskmethod tm on tm.methodid=t.taskmethodid
               left join wm_session wms
                    left join getobjectname(wms.objid,NULL) m on 1=1
                 on wms.sessionid=t.wm_sessionid
               left join r_status rs on rs.statustype='T' and rs.code=t.status
               left join site s on s.siteid = t.siteid
         where (t.docid = :docid_in or :docid_in is null)
                and ((t.begintime < :tend_in and t.endtime > :tbeg_in) or (:tbeg_in is null and :tend_in is null))
                and (t.tasktypeid  = :ttid_in or :ttid_in is null)
                and (t.wm_sessionid  = :wmsesid or :manid_in is null)
                and (t.status = :tstatus_in or :tstatus_in is null )
                --and d.status <> 'У'
          into :tid,:tstat,:tstatname,
               :ttid,:ttcode,:ttname,
               :tmid,:tmalgorithm,:tmname,
               :createtime,:endtime,:begintime,
               :manid,:manfio,
               :docid, :sitename
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_CREATETASKES (
    TID_GATEAUTO R_ID)
AS
declare variable docstatus type of r_status;
declare variable docid type of r_id64;
declare variable tid_loadauto type of r_id;
declare variable tid_select type of r_id;
declare variable tid_loadpallet type of r_id;
declare variable tbtid_CARDOCS r_id;
declare variable tbtid_loadselect type of r_id;
declare variable tbtid_docpallets type of r_id;
declare variable ttid_Select type of r_id;
declare variable ttid_loadpallet type of r_id;
declare variable taskstat_select type of r_status;
declare variable gateautostatus type of r_status;
declare variable gateid type of column SITE.siteid;
begin
    -- Чтобы сгенерить задания на погрузку поддонов в авто машина должна стоять на воротах
    select t.status, t.siteid
      from wm_task t
     where t.taskid = :tid_gateauto
      into :gateautostatus, :gateid;

    if (:gateautostatus is NULL or :gateautostatus <> '1' ) then
        exit;

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_CARDOCS;

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'LOADSELECT'
      into :tbtid_loadselect;

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'DOCPALLETS'
      into :tbtid_docpallets;

    execute procedure wh_ttid_select returning_values :ttid_Select;
    execute procedure wh_ttid_loadpallet returning_values :ttid_loadpallet;

    for
        select d.docid, d.status, t.taskid, ts.taskid, ts.status
          from wh_taskbond tb
               left join wm_task t
                    left join document d
                         left join wm_task ts
                           on ts.docid = d.docid
                              and ts.tasktypeid = :ttid_Select
                              and ts.taskmethodid is NOT NULL
                              and coalesce(ts.tmpflags,'') not containing 'E' -- Пустое задание на отборку
                      on d.docid = t.docid
                 on t.taskid = tb.task2id
         where tb.task1id = :tid_gateauto
           and tb.taskbondtid = :tbtid_cardocs
         order by t.priority ascending nulls last, ts.endtime ascending nulls last
          into :docid,:docstatus, :tid_loadauto, :tid_select, :taskstat_select
    do
    begin
      if (:tid_select is NULL and :docstatus in ('2','e')) then
      begin
        update wm_task t
           set t.status = '2',t.wm_sessionid = NULL
         where t.taskid = :tid_loadauto and t.status <> '2';
      end
      else
      if (:taskstat_select is NULL or :taskstat_select <> '2') then
      begin
        exit;
      end
      else
      begin
          if (not exists(select *
                                from wh_taskbond tb
                                     left join wm_task t2 on t2.taskid = tb.task1id
                               where tb.task2id = :tid_select
                                 and tb.taskbondtid = :tbtid_loadselect
                                 and t2.tasktypeid = :ttid_loadpallet)) then
          begin
             insert into wm_task(tasktypeid,docid,status,siteid)
             values(:ttid_loadpallet,:docid,'0',:gateid)
             returning taskid
             into :tid_loadpallet;
    
             insert into wh_taskbond(task1id,task2id,taskbondtid)
             values(:tid_loadauto,:tid_loadpallet,:tbtid_docpallets);
    
             insert into wh_taskbond(task1id,task2id,taskbondtid)
             values(:tid_loadpallet,:tid_select,:tbtid_loadselect);
         end
      end
    end
end^

SET TERM ; ^

