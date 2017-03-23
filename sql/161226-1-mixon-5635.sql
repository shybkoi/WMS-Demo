

SET TERM ^ ;

create or alter procedure RBS_LOADPLAN_GETCOUNTS_BY_DOC (
    DOCID type of column DOCUMENT.DOCID)
returns (
    COUNTSELECT type of R_NUMBER,
    COUNSELECTDONE type of R_NUMBER)
as
declare variable TTID type of column WM_TASKTYPE.TASKTYPEID;
begin
  select tt.tasktypeid
    from wm_tasktype tt
   where tt.code = 'SELECT'
    into :ttid;

  select count(t.taskid), sum(case when t.status = '2' then 1 else 0 end)
    from wm_task t
   where t.docid = :docid
     and t.tasktypeid = :ttid
    into :countselect, :counselectdone;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_GETCOUNTS_BY_DOC (
    DOCID type of column DOCUMENT.DOCID)
returns (
    COUNTSELECT type of R_NUMBER,
    COUNSELECTDONE type of R_NUMBER,
    COUNTLOAD type of R_NUMBER,
    COUNTLOADDONE type of R_NUMBER)
as
declare variable TTID type of column WM_TASKTYPE.TASKTYPEID;
declare variable TBT_LOADSELECT type of column WH_TASKBONDTYPE.ID;
begin
  select tt.tasktypeid
    from wm_tasktype tt
   where tt.code = 'SELECT'
    into :ttid;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'LOADSELECT'
    into :tbt_LOADSELECT;

  select count(t.taskid), sum(case when t.status = '2' then 1 else 0 end),
         count(t1.taskid), sum(case when t1.status = '2' then 1 else 0 end)
    from wm_task t
         left join wh_taskbond tb on tb.task2id = t.taskid and tb.taskbondtid = :tbt_LOADSELECT
         left join wm_task t1 on t1.taskid = tb.task1id
   where t.docid = :docid
     and t.tasktypeid = :ttid
    into :countselect, :counselectdone,
         :countload, :countloaddone;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure RBS_LOADPLAN_GATESLOAD
returns (
    GATEID type of column SITE.SITEID,
    GATENAME type of column SITE.NAME,
    TASKID type of column WM_TASK.TASKID,
    AUTONAME type of column T_AUTO.NAME,
    BEGINTIME type of column WM_TASK.BEGINTIME,
    COUNTDOCS type of R_NUMBER,
    COUNTDOCSNOTUP type of R_NUMBER,
    COUNTSELECT type of R_NUMBER,
    COUNSELECTDONE type of R_NUMBER,
    COUNTLOAD type of R_NUMBER,
    COUNTLOADDONE type of R_NUMBER)
as
declare variable TTID type of column WM_TASKTYPE.TASKTYPEID;
declare variable TBTID_CARDOCS type of column WH_TASKBONDTYPE.ID;
begin
  select tt.tasktypeid
    from wm_tasktype tt
   where tt.code = 'GATEAUTO'
    into :ttid;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :tbtid_CARDOCS;

  for
    select g.gateid, g.name
      from rbs_loadplan_getgates g
      into :gateid, :gatename
  do
  begin
    select t.taskid, a.name, t.begintime
      from wm_task t
           left join t_auto a on a.aid = t.infoid
     where t.siteid = :gateid
       and t.status = '1'
       and t.tasktypeid = :ttid
      into :taskid, :autoname, :begintime;

    if(:taskid is NOT NULL) then
    begin
      select count(d.docid),sum(case when d.status = 'g' then 1 else 0 end),
             sum(c.countselect), sum(c.counselectdone),
             sum(c.countload), sum(c.countloaddone)
        from wh_taskbond tb
             left join wm_task taskdocs on taskdocs.taskid = tb.task2id
             left join document d on d.docid = taskdocs.docid
             left join rbs_loadplan_getcounts_by_doc(d.docid) c on 1=1
       where tb.task1id = :taskid
         and tb.taskbondtid = :tbtid_CARDOCS
        into :countdocs, :countdocsnotup,
             :countselect, :counselectdone,
             :countload, :countloaddone;
    end

    suspend;
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_GATESLOAD
returns (
    GATEID type of column SITE.SITEID,
    GATENAME type of column SITE.NAME,
    TASKID type of column WM_TASK.TASKID,
    AUTONAME type of column T_AUTO.NAME,
    BEGINTIME type of column WM_TASK.BEGINTIME,
    COUNTDOCS type of R_NUMBER,
    COUNTDOCSNOTUP type of R_NUMBER,
    COUNTSELECT type of R_NUMBER,
    COUNSELECTDONE type of R_NUMBER,
    COUNTLOAD type of R_NUMBER,
    COUNTLOADDONE type of R_NUMBER)
as
declare variable TTID type of column WM_TASKTYPE.TASKTYPEID;
declare variable TBTID_CARDOCS type of column WH_TASKBONDTYPE.ID;
begin
  select tt.tasktypeid
    from wm_tasktype tt
   where tt.code = 'GATEAUTO'
    into :ttid;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :tbtid_CARDOCS;

  for
    select g.gateid, g.name
      from rbs_loadplan_getgates g
      into :gateid, :gatename
  do
  begin
    taskid = null;
    select t.taskid, a.name, t.begintime
      from wm_task t
           left join t_auto a on a.aid = t.infoid
     where t.siteid = :gateid
       and t.status = '1'
       and t.tasktypeid = :ttid
      into :taskid, :autoname, :begintime;

    if(:taskid is NOT NULL) then
    begin
      select count(d.docid),sum(case when d.status = 'g' then 1 else 0 end),
             sum(c.countselect), sum(c.counselectdone),
             sum(c.countload), sum(c.countloaddone)
        from wh_taskbond tb
             left join wm_task taskdocs on taskdocs.taskid = tb.task2id
             left join document d on d.docid = taskdocs.docid
             left join rbs_loadplan_getcounts_by_doc(d.docid) c on 1=1
       where tb.task1id = :taskid
         and tb.taskbondtid = :tbtid_CARDOCS
        into :countdocs, :countdocsnotup,
             :countselect, :counselectdone,
             :countload, :countloaddone;
    end
    else
    begin
      autoname = null; begintime = null;
      countdocs = null; countdocsnotup = null;
      countselect = null; counselectdone = null;
      countload = null; countloaddone = null;
    end

    suspend;
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_GATESLOAD
returns (
    GATEID type of column SITE.SITEID,
    GATENAME type of column SITE.NAME,
    TASKID type of column WM_TASK.TASKID,
    AUTONAME type of column T_AUTO.NAME,
    BEGINTIME type of column WM_TASK.BEGINTIME,
    COUNTDOCS type of R_NUMBER,
    COUNTDOCSNOTUP type of R_NUMBER,
    COUNTSELECT type of R_NUMBER,
    COUNSELECTDONE type of R_NUMBER,
    COUNTLOAD type of R_NUMBER,
    COUNTLOADDONE type of R_NUMBER)
as
declare variable TTID type of column WM_TASKTYPE.TASKTYPEID;
declare variable TBTID_CARDOCS type of column WH_TASKBONDTYPE.ID;
begin
  select tt.tasktypeid
    from wm_tasktype tt
   where tt.code = 'GATEAUTO'
    into :ttid;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :tbtid_CARDOCS;

  for
    select g.gateid, g.name
      from rbs_loadplan_getgates g
      into :gateid, :gatename
  do
  begin
    taskid = null;
    for
    select t.taskid, a.name, t.begintime,count(d.docid),sum(case when d.status = 'g' then 1 else 0 end),
             sum(c.countselect), sum(c.counselectdone),
             sum(c.countload), sum(c.countloaddone)
      from wm_task t
           left join t_auto a on a.aid = t.infoid
           left join wh_taskbond tb on tb.task1id = t.taskid and tb.taskbondtid = :tbtid_CARDOCS
             left join wm_task taskdocs on taskdocs.taskid = tb.task2id
             left join document d on d.docid = taskdocs.docid
             left join rbs_loadplan_getcounts_by_doc(d.docid) c on 1=1
     where t.siteid = :gateid
       and t.status = '1'
       and t.tasktypeid = :ttid
     group by 1,2,3
      into :taskid, :autoname, :begintime,:countdocs, :countdocsnotup,
             :countselect, :counselectdone,
             :countload, :countloaddone
             do

    /*if(:taskid is NOT NULL) then
    begin
      select count(d.docid),sum(case when d.status = 'g' then 1 else 0 end),
             sum(c.countselect), sum(c.counselectdone),
             sum(c.countload), sum(c.countloaddone)
        from wh_taskbond tb
             left join wm_task taskdocs on taskdocs.taskid = tb.task2id
             left join document d on d.docid = taskdocs.docid
             left join rbs_loadplan_getcounts_by_doc(d.docid) c on 1=1
       where tb.task1id = :taskid
         and tb.taskbondtid = :tbtid_CARDOCS
        into :countdocs, :countdocsnotup,
             :countselect, :counselectdone,
             :countload, :countloaddone;
    end
    else
    begin
      autoname = null; begintime = null;
      countdocs = null; countdocsnotup = null;
      countselect = null; counselectdone = null;
      countload = null; countloaddone = null;
    end */

    suspend;
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_GATESLOAD
returns (
    GATEID type of column SITE.SITEID,
    GATENAME type of column SITE.NAME,
    TASKID type of column WM_TASK.TASKID,
    AUTONAME type of column T_AUTO.NAME,
    BEGINTIME type of column WM_TASK.BEGINTIME,
    COUNTDOCS type of R_NUMBER,
    COUNTDOCSNOTUP type of R_NUMBER,
    COUNTSELECT type of R_NUMBER,
    COUNSELECTDONE type of R_NUMBER,
    COUNTLOAD type of R_NUMBER,
    COUNTLOADDONE type of R_NUMBER)
as
declare variable TTID type of column WM_TASKTYPE.TASKTYPEID;
declare variable TBTID_CARDOCS type of column WH_TASKBONDTYPE.ID;
begin
  select tt.tasktypeid
    from wm_tasktype tt
   where tt.code = 'GATEAUTO'
    into :ttid;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :tbtid_CARDOCS;


    for
    select  g.gateid, g.name,t.taskid, a.name, t.begintime,count(d.docid),sum(case when d.status = 'g' then 1 else 0 end),
             sum(c.countselect), sum(c.counselectdone),
             sum(c.countload), sum(c.countloaddone)
      from rbs_loadplan_getgates g left join wm_task t on t.siteid = g.gateid and t.status = '1' and t.tasktypeid = :ttid
           left join t_auto a on a.aid = t.infoid
           left join wh_taskbond tb on tb.task1id = t.taskid and tb.taskbondtid = :tbtid_CARDOCS
             left join wm_task taskdocs on taskdocs.taskid = tb.task2id
             left join document d on d.docid = taskdocs.docid
             left join rbs_loadplan_getcounts_by_doc(d.docid) c on 1=1
     group by 1,2,3,4,5
      into :gateid, :gatename,:taskid, :autoname, :begintime,:countdocs, :countdocsnotup,
             :countselect, :counselectdone,
             :countload, :countloaddone
             do

    /*if(:taskid is NOT NULL) then
    begin
      select count(d.docid),sum(case when d.status = 'g' then 1 else 0 end),
             sum(c.countselect), sum(c.counselectdone),
             sum(c.countload), sum(c.countloaddone)
        from wh_taskbond tb
             left join wm_task taskdocs on taskdocs.taskid = tb.task2id
             left join document d on d.docid = taskdocs.docid
             left join rbs_loadplan_getcounts_by_doc(d.docid) c on 1=1
       where tb.task1id = :taskid
         and tb.taskbondtid = :tbtid_CARDOCS
        into :countdocs, :countdocsnotup,
             :countselect, :counselectdone,
             :countload, :countloaddone;
    end
    else
    begin
      autoname = null; begintime = null;
      countdocs = null; countdocsnotup = null;
      countselect = null; counselectdone = null;
      countload = null; countloaddone = null;
    end */

    suspend;
  --end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_GATESLOAD
returns (
    GATEID type of column SITE.SITEID,
    GATENAME type of column SITE.NAME,
    TASKID type of column WM_TASK.TASKID,
    AUTONAME type of column T_AUTO.NAME,
    BEGINTIME type of column WM_TASK.BEGINTIME,
    COUNTDOCS type of R_NUMBER,
    COUNTDOCSNOTUP type of R_NUMBER,
    COUNTSELECT type of R_NUMBER,
    COUNSELECTDONE type of R_NUMBER,
    COUNTLOAD type of R_NUMBER,
    COUNTLOADDONE type of R_NUMBER)
as
declare variable TTID type of column WM_TASKTYPE.TASKTYPEID;
declare variable TBTID_CARDOCS type of column WH_TASKBONDTYPE.ID;
begin
  select tt.tasktypeid
    from wm_tasktype tt
   where tt.code = 'GATEAUTO'
    into :ttid;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :tbtid_CARDOCS;

  for
    select g.gateid, g.name,t.taskid, a.name, t.begintime,
           count(d.docid),sum(case when d.status = 'g' then 1 else 0 end),
           sum(c.countselect), sum(c.counselectdone),
           sum(c.countload), sum(c.countloaddone)
      from rbs_loadplan_getgates g left join wm_task t on t.siteid = g.gateid
                                                      and t.status = '1'
                                                      and t.tasktypeid = :ttid
           left join t_auto a on a.aid = t.infoid
           left join wh_taskbond tb on tb.task1id = t.taskid
                                   and tb.taskbondtid = :tbtid_CARDOCS
           left join wm_task taskdocs on taskdocs.taskid = tb.task2id
           left join document d on d.docid = taskdocs.docid
           left join rbs_loadplan_getcounts_by_doc(d.docid) c on 1=1
     group by 1,2,3,4,5
      into :gateid, :gatename,:taskid, :autoname, :begintime,
           :countdocs, :countdocsnotup,
           :countselect, :counselectdone,
           :countload, :countloaddone
  do
     suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_GATESLOAD
returns (
    GATEID type of column SITE.SITEID,
    GATENAME type of column SITE.NAME,
    TASKID type of column WM_TASK.TASKID,
    AUTONAME type of column T_AUTO.NAME,
    BEGINTIME type of column WM_TASK.BEGINTIME,
    COUNTDOCS type of R_NUMBER,
    COUNTDOCSNOTUP type of R_NUMBER,
    COUNTSELECT type of R_NUMBER,
    COUNSELECTDONE type of R_NUMBER,
    COUNTLOAD type of R_NUMBER,
    COUNTLOADDONE type of R_NUMBER)
as
declare variable TTID type of column WM_TASKTYPE.TASKTYPEID;
declare variable TBTID_CARDOCS type of column WH_TASKBONDTYPE.ID;
begin
  select tt.tasktypeid
    from wm_tasktype tt
   where tt.code = 'GATEAUTO'
    into :ttid;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :tbtid_CARDOCS;

  for
    select g.gateid, g.name, t.taskid, a.name, t.begintime,
           count(d.docid), sum(case when d.status = 'g' then 1 else 0 end),
           sum(c.countselect), sum(c.counselectdone),
           sum(c.countload), sum(c.countloaddone)
      from rbs_loadplan_getgates g left join wm_task t on t.siteid = g.gateid
                                                      and t.status = '1'
                                                      and t.tasktypeid = :ttid
           left join t_auto a on a.aid = t.infoid
           left join wh_taskbond tb on tb.task1id = t.taskid
                                   and tb.taskbondtid = :tbtid_CARDOCS
           left join wm_task taskdocs on taskdocs.taskid = tb.task2id
           left join document d on d.docid = taskdocs.docid
           left join rbs_loadplan_getcounts_by_doc(d.docid) c on 1=1
     group by 1,2,3,4,5
     order by 2
      into :gateid, :gatename,:taskid, :autoname, :begintime,
           :countdocs, :countdocsnotup,
           :countselect, :counselectdone,
           :countload, :countloaddone
  do
     suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_GATESLOAD
returns (
    GATEID type of column SITE.SITEID,
    GATENAME type of column SITE.NAME,
    TASKID type of column WM_TASK.TASKID,
    AUTONAME type of column T_AUTO.NAME,
    BEGINTIME type of column WM_TASK.BEGINTIME,
    COUNTDOCS type of R_NUMBER,
    COUNTDOCSNOTUP type of R_NUMBER,
    COUNTSELECT type of R_NUMBER,
    COUNSELECTDONE type of R_NUMBER,
    COUNTLOAD type of R_NUMBER,
    COUNTLOADDONE type of R_NUMBER)
as
declare variable TTID type of column WM_TASKTYPE.TASKTYPEID;
declare variable TBTID_CARDOCS type of column WH_TASKBONDTYPE.ID;
begin
  select tt.tasktypeid
    from wm_tasktype tt
   where tt.code = 'GATEAUTO'
    into :ttid;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :tbtid_CARDOCS;

  for
    select g.gateid, g.name, t.taskid, a.name, t.begintime,
           count(d.docid), sum(case when d.status = '1' then 1 else 0 end),
           sum(c.countselect), sum(c.counselectdone),
           sum(c.countload), sum(c.countloaddone)
      from rbs_loadplan_getgates g left join wm_task t on t.siteid = g.gateid
                                                      and t.status = '1'
                                                      and t.tasktypeid = :ttid
           left join t_auto a on a.aid = t.infoid
           left join wh_taskbond tb on tb.task1id = t.taskid
                                   and tb.taskbondtid = :tbtid_CARDOCS
           left join wm_task taskdocs on taskdocs.taskid = tb.task2id
           left join document d on d.docid = taskdocs.docid
           left join rbs_loadplan_getcounts_by_doc(d.docid) c on 1=1
     group by 1,2,3,4,5
     order by 2
      into :gateid, :gatename,:taskid, :autoname, :begintime,
           :countdocs, :countdocsnotup,
           :countselect, :counselectdone,
           :countload, :countloaddone
  do
     suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_GATESLOAD
returns (
    GATEID type of column SITE.SITEID,
    GATENAME type of column SITE.NAME,
    TASKID type of column WM_TASK.TASKID,
    AUTONAME type of column T_AUTO.NAME,
    BEGINTIME type of column WM_TASK.BEGINTIME,
    COUNTDOCS type of R_NUMBER,
    COUNTDOCSNOTUP type of R_NUMBER,
    COUNTSELECT type of R_NUMBER,
    COUNSELECTDONE type of R_NUMBER,
    COUNTLOAD type of R_NUMBER,
    COUNTLOADDONE type of R_NUMBER)
as
declare variable TTID type of column WM_TASKTYPE.TASKTYPEID;
declare variable TBTID_CARDOCS type of column WH_TASKBONDTYPE.ID;
begin
  execute procedure wh_ttid_gateauto returning_values :ttid;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :tbtid_CARDOCS;

  for
    select g.gateid, g.name, t.taskid, a.name, t.begintime,
           count(d.docid), sum(case when d.status = '1' then 1 else 0 end),
           sum(c.countselect), sum(c.counselectdone),
           sum(c.countload), sum(c.countloaddone)
      from rbs_loadplan_getgates g left join wm_task t on t.siteid = g.gateid
                                                      and t.status = '1'
                                                      and t.tasktypeid = :ttid
           left join t_auto a on a.aid = t.infoid
           left join wh_taskbond tb on tb.task1id = t.taskid
                                   and tb.taskbondtid = :tbtid_CARDOCS
           left join wm_task taskdocs on taskdocs.taskid = tb.task2id
           left join document d on d.docid = taskdocs.docid
           left join rbs_loadplan_getcounts_by_doc(d.docid) c on 1=1
     group by 1,2,3,4,5
     order by 2
      into :gateid, :gatename,:taskid, :autoname, :begintime,
           :countdocs, :countdocsnotup,
           :countselect, :counselectdone,
           :countload, :countloaddone
  do
     suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TBTID_CARDOCS
returns (
    ID type of column WH_TASKBONDTYPE.ID)
as
begin
  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :id;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_GATESLOAD
returns (
    GATEID type of column SITE.SITEID,
    GATENAME type of column SITE.NAME,
    TASKID type of column WM_TASK.TASKID,
    AUTONAME type of column T_AUTO.NAME,
    BEGINTIME type of column WM_TASK.BEGINTIME,
    COUNTDOCS type of R_NUMBER,
    COUNTDOCSNOTUP type of R_NUMBER,
    COUNTSELECT type of R_NUMBER,
    COUNSELECTDONE type of R_NUMBER,
    COUNTLOAD type of R_NUMBER,
    COUNTLOADDONE type of R_NUMBER)
as
declare variable TTID type of column WM_TASKTYPE.TASKTYPEID;
declare variable TBTID_CARDOCS type of column WH_TASKBONDTYPE.ID;
begin
  execute procedure wh_ttid_gateauto returning_values :ttid;

  execute procedure wh_tbtid_cardocs returning_values :tbtid_CARDOCS;

  for
    select g.gateid, g.name, t.taskid, a.name, t.begintime,
           count(d.docid), sum(case when d.status = '1' then 1 else 0 end),
           sum(c.countselect), sum(c.counselectdone),
           sum(c.countload), sum(c.countloaddone)
      from rbs_loadplan_getgates g left join wm_task t on t.siteid = g.gateid
                                                      and t.status = '1'
                                                      and t.tasktypeid = :ttid
           left join t_auto a on a.aid = t.infoid
           left join wh_taskbond tb on tb.task1id = t.taskid
                                   and tb.taskbondtid = :tbtid_CARDOCS
           left join wm_task taskdocs on taskdocs.taskid = tb.task2id
           left join document d on d.docid = taskdocs.docid
           left join rbs_loadplan_getcounts_by_doc(d.docid) c on 1=1
     group by 1,2,3,4,5
     order by 2
      into :gateid, :gatename,:taskid, :autoname, :begintime,
           :countdocs, :countdocsnotup,
           :countselect, :counselectdone,
           :countload, :countloaddone
  do
     suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TBTID_LOADSELECT
returns (
    ID type of column WH_TASKBONDTYPE.ID)
as
begin
  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'LOADSELECT'
    into :id;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_GETCOUNTS_BY_DOC (
    DOCID type of column DOCUMENT.DOCID)
returns (
    COUNTSELECT type of R_NUMBER,
    COUNSELECTDONE type of R_NUMBER,
    COUNTLOAD type of R_NUMBER,
    COUNTLOADDONE type of R_NUMBER)
as
declare variable TTID type of column WM_TASKTYPE.TASKTYPEID;
declare variable TBT_LOADSELECT type of column WH_TASKBONDTYPE.ID;
begin
  execute procedure wh_ttid_select returning_values :ttid;

  execute procedure wh_tbtid_loadselect returning_values :tbt_LOADSELECT;

  select count(t.taskid), sum(case when t.status = '2' then 1 else 0 end),
         count(t1.taskid), sum(case when t1.status = '2' then 1 else 0 end)
    from wm_task t
         left join wh_taskbond tb on tb.task2id = t.taskid and tb.taskbondtid = :tbt_LOADSELECT
         left join wm_task t1 on t1.taskid = tb.task1id
   where t.docid = :docid
     and t.tasktypeid = :ttid
    into :countselect, :counselectdone,
         :countload, :countloaddone;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_GATESLOAD
returns (
    GATEID type of column SITE.SITEID,
    GATENAME type of column SITE.NAME,
    TASKID type of column WM_TASK.TASKID,
    AUTONAME type of column T_AUTO.NAME,
    DIFF type of R_NUMBER,
    BEGINTIME type of column WM_TASK.BEGINTIME,
    COUNTDOCS type of R_NUMBER,
    COUNTDOCSNOTUP type of R_NUMBER,
    COUNTSELECT type of R_NUMBER,
    COUNSELECTDONE type of R_NUMBER,
    COUNTLOAD type of R_NUMBER,
    COUNTLOADDONE type of R_NUMBER)
as
declare variable TTID type of column WM_TASKTYPE.TASKTYPEID;
declare variable TBTID_CARDOCS type of column WH_TASKBONDTYPE.ID;
begin
  execute procedure wh_ttid_gateauto returning_values :ttid;

  execute procedure wh_tbtid_cardocs returning_values :tbtid_CARDOCS;

  for
    select g.gateid, g.name, t.taskid, a.name, t.begintime, current_timestamp - t.begintime,
           count(d.docid), sum(case when d.status = '1' then 1 else 0 end),
           sum(c.countselect), sum(c.counselectdone),
           sum(c.countload), sum(c.countloaddone)
      from rbs_loadplan_getgates g left join wm_task t on t.siteid = g.gateid
                                                      and t.status = '1'
                                                      and t.tasktypeid = :ttid
           left join t_auto a on a.aid = t.infoid
           left join wh_taskbond tb on tb.task1id = t.taskid
                                   and tb.taskbondtid = :tbtid_CARDOCS
           left join wm_task taskdocs on taskdocs.taskid = tb.task2id
           left join document d on d.docid = taskdocs.docid
           left join rbs_loadplan_getcounts_by_doc(d.docid) c on 1=1
     group by 1,2,3,4,5,6
     order by 2
      into :gateid, :gatename,:taskid, :autoname, :begintime, :diff,
           :countdocs, :countdocsnotup,
           :countselect, :counselectdone,
           :countload, :countloaddone
  do
     suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_GATESLOAD
returns (
    GATEID type of column SITE.SITEID,
    GATENAME type of column SITE.NAME,
    TASKID type of column WM_TASK.TASKID,
    AUTONAME type of column T_AUTO.NAME,
    DIFFTIME type of R_DOUBLE,
    BEGINTIME type of column WM_TASK.BEGINTIME,
    COUNTDOCS type of R_NUMBER,
    COUNTDOCSNOTUP type of R_NUMBER,
    COUNTSELECT type of R_NUMBER,
    COUNSELECTDONE type of R_NUMBER,
    COUNTLOAD type of R_NUMBER,
    COUNTLOADDONE type of R_NUMBER)
as
declare variable TTID type of column WM_TASKTYPE.TASKTYPEID;
declare variable TBTID_CARDOCS type of column WH_TASKBONDTYPE.ID;
begin
  execute procedure wh_ttid_gateauto returning_values :ttid;

  execute procedure wh_tbtid_cardocs returning_values :tbtid_CARDOCS;

  for
    select g.gateid, g.name, t.taskid, a.name, t.begintime, current_timestamp - t.begintime,
           count(d.docid), sum(case when d.status = '1' then 1 else 0 end),
           sum(c.countselect), sum(c.counselectdone),
           sum(c.countload), sum(c.countloaddone)
      from rbs_loadplan_getgates g left join wm_task t on t.siteid = g.gateid
                                                      and t.status = '1'
                                                      and t.tasktypeid = :ttid
           left join t_auto a on a.aid = t.infoid
           left join wh_taskbond tb on tb.task1id = t.taskid
                                   and tb.taskbondtid = :tbtid_CARDOCS
           left join wm_task taskdocs on taskdocs.taskid = tb.task2id
           left join document d on d.docid = taskdocs.docid
           left join rbs_loadplan_getcounts_by_doc(d.docid) c on 1=1
     group by 1,2,3,4,5,6
     order by 2
      into :gateid, :gatename,:taskid, :autoname, :begintime, :difftime,
           :countdocs, :countdocsnotup,
           :countselect, :counselectdone,
           :countload, :countloaddone
  do
     suspend;
end^

SET TERM ; ^

