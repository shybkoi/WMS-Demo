

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

create or alter procedure K_U3S_COMERETURN_TSTCHG (
    TASKID type of R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable TTCODE type of R_CODE;
declare variable TTID type of R_ID;
declare variable DOCID type of R_ID64;
begin
    select tt.code,tt.tasktypeid,t.docid
      from wm_task t
           left join wm_tasktype tt on tt.tasktypeid=t.tasktypeid
           left join wm_taskmethod tm on tm.methodid=t.taskmethodid
     where t.taskid = :taskid
      into :ttcode,:ttid,:docid;

    if (:ttcode <> 'COMERETURN') then
        exception exc_k_wrongtasktype;

    if (:newstat = '2') then
        if (not exists(select *
                         from wm_task t
                        where t.docid = :docid
                          and t.tasktypeid = :ttid
                          and t.status <> '2'
                          and t.status <> 'E')) then
    begin
        update document d
           set d.status = 'w'
         where d.docid = :docid and d.status <> 'w';
    end
end^

SET TERM ; ^



ALTER TABLE DOCTYPEOBJ
ADD ISOBJRESERVE R_FLAG;



SET TERM ^ ;

create procedure WH_DOCMNGR_DTOBJLIST (
    DOCTID type of column DOCTYPE.doctid,
    WMSESSIONID type of column WM_SESSION.sessionid
)
returns (
    numobj type of column DOCTYPEOBJ.numobj,
    objid type of column DOCTYPEOBJ.objid,
    canchoice type of column DOCTYPEOBJ.canchoice,
    objname type of R_FULLNAME,
    REQUIRED type of column DOCTYPEOBJ.required,
    ISOBJZONE type of column DOCTYPEOBJ.isobjzone,
    CAPTION type of column DOCTYPEOBJ.caption,
    ISOBJRESERVE type of column DOCTYPEOBJ.isobjreserve
)
as
declare variable currentobjid type of column SITEZONE.objid;
begin
    select sz.objid
      from wm_session s
           left join employee e
                left join sitezone sz on sz.zoneid=e.currentzone
             on s.objid=e.employeeid
     where s.sessionid=:wmsessionid
      into :currentobjid;

    for
        select dto.numobj,
               case
                when dto.ISOBJZONE is NULL then dto.objid
                else :currentobjid end as OBJID,
               dto.canchoice,
               gon.fullname as objname, dto.REQUIRED, dto.ISOBJZONE, dto.CAPTION, dto.isobjreserve
          from doctypeobj dto
               left join GETOBJECTNAME(case when dto.ISOBJZONE is NULL then dto.objid else :currentobjid end, NULL) gon on 1=1
         where dto.doctid = :doctid
           and dto.numobj in ('0','1','2')
          into :numobj, :objid, :canchoice, :objname, :REQUIRED, :ISOBJZONE, :CAPTION, :ISOBJRESERVE
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_DOCMNGR_OBJRESERVELIST (
    INCNAME type of R_NAME = NULL
)
returns (
    OBJID type of R_ID,
    NAME type of R_FULLNAME
)
AS
begin
    if (:incname is NULL) then
    begin
        for
            select ro.objid, n.objname
              from wh_reserve_objects ro
                   left join wh_get_objectname(ro.objid) n on 1=1
              into :objid, :name
        do
            suspend;
    end
    else
    begin
        for
            select ro.objid, n.objname
              from wh_reserve_objects ro
                   left join wh_get_objectname(ro.objid) n on 1=1
             where n.objname containing :incname
              into :objid, :name
        do
            suspend;
    end
end^

SET TERM ; ^



CREATE EXCEPTION EXC_WH_WRONGWMSESSION 'Не верная сессия пользователя';



SET TERM ^ ;

create procedure WH_COMERETURN_TWJOIN (
    TASKID type of column WM_TASK.taskid,
    WARESID type of column GWARES.waresid,
    WMSESSIONID type of column WM_SESSION.sessionid
)
as
declare variable twid type of column wm_task_wares.taskwaresid;
declare variable twsid type of column wm_task_wares.sessionid;
begin
    select tw.taskwaresid, tw.wm_sessionid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.waresid = :waresid
      into :twid, :twsid;

    if (:twid is NULL) then
        exception EXC_WH_WARESNOTFOUNDINTASK;

    if (:twsid is NOT NULL and :twsid <> :wmsessionid) then
        exception exc_wh_wrongwmsession;

    update wm_task_wares tw
       set tw.begintime = coalesce(tw.begintime, current_timestamp),
           tw.wm_sessionid = coalesce(tw.wm_sessionid, :wmsessionid)
     where tw.taskwaresid = :twid;
end^

SET TERM ; ^

