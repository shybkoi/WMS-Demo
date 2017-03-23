

SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_GETNUMPALLET (
    TASKID type of column WM_TASK.taskid)
returns (
    NUMPALLET type of R_SHORTNAME)
AS
begin
    /*select O.Code||'-'||T.Num
      from wm_task t
           left join document d
                left join object o on o.objid = d.toobj
             on d.docid = t.docid
     where t.taskid = :taskid
      into :numpallet;*/

    NUMPALLET = 'T'||cast(:taskid as varchar(10));

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARES_GETPALLETUNIT (
    WARESID type of column GWARES.waresid
)
returns (
    W_PWUID type of column WARESUNIT.waresunitid,
    W_PUID type of column UNIT.unitid,
    W_PUCODE type of column UNIT.shortname,
    W_PUFACTOR type of column WARESUNIT.factor
)
AS
begin
    select wu.factor,wu.waresunitid,u.shortname,u.unitid
      from wm_config wm
           left join waresunit wu
                left join unit u on u.unitid = wu.unitid
             on wu.waresid = :waresid and wu.unitid = wm.palletunitid
      into :w_pufactor, :w_pwuid, :w_pucode, :w_puid;


    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_STOPPLAN (
    TASKID type of column WM_TASK.taskid)
AS
declare variable objcode type of column WM_CONFIG.objcode;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable pcnt type of r_shortnumber;
begin
  select w.objcode
    from wm_config w
    into :objcode;

  if (:objcode = 'U3S') then
  begin
      select tbt.id
        from wh_taskbondtype tbt
       where tbt.code = 'CARDOCS'
        into :tbtid_cardocs;

      with s1 as (
          select sum(iif(pu.W_PUFACTOR is NOT NULL and pu.W_PUFACTOR > 0.0001, cg.amount / pu.W_PUFACTOR, 0.000)) as q
            from wh_taskbond tb
                 left join wm_task t
                      left join cargo cg
                           left join wh_wares_getpalletunit(cg.waresid) pu on 1=1
                        on cg.document = t.docid
                   on t.taskid = tb.task2id
           where tb.task1id = :taskid
             and tb.taskbondtid = :tbtid_cardocs
           group by cg.document
      )
      select sum(ceil(s1.q))
        from s1
        into :pcnt;

      update wm_task t
         set t.status = '0', t.capacity = :pcnt
       where t.taskid = :taskid;
  end
  else
  begin
      update wm_task t
         set t.status = '0'
       where t.taskid = :taskid;
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_TASKINFO (
    TASKID type of column WM_TASK.TASKID)
returns (
    TID type of column WM_TASK.TASKID,
    TSTAT type of column R_STATUS.CODE,
    TCAPACITY type of column WM_TASK.capacity,
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
    select t.taskid,t.siteid, t.status,
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
      into :tid,:siteid,:tstat,
           :docid,:docdate,:docnum,:docstat,:algorithm,
           :fromid, :fromname,
           :throughid, :throughname,
           :toid, :toname,
           :infoid,:sname,:infotypecode,:plandt,:infoname;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_TASKINFO (
    TASKID type of column WM_TASK.TASKID)
returns (
    TID type of column WM_TASK.TASKID,
    TSTAT type of column R_STATUS.CODE,
    TCAPACITY type of column WM_TASK.capacity,
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
    select t.taskid,t.siteid, t.status,t.capacity,
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
      into :tid,:siteid,:tstat,:tcapacity,
           :docid,:docdate,:docnum,:docstat,:algorithm,
           :fromid, :fromname,
           :throughid, :throughname,
           :toid, :toname,
           :infoid,:sname,:infotypecode,:plandt,:infoname;

    suspend;
end^

SET TERM ; ^

