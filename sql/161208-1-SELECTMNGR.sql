

SET TERM ^ ;

create or alter procedure WH_SELMANAG_LISTGATEAUTO (
    WHID type of column OBJECT.objid
)
returns (
    TID type of column WM_TASK.taskid,
    GATEID type of column SITE.siteid,
    GATENAME type of column SITE.name,
    AUTOID type of column T_AUTO.aid,
    AUTONAME type of column T_AUTO.name,
    TSTAT type of column R_STATUS.code,
    TSTATNAME type of column R_STATUS.name,
    PLANDATETIME type of column WM_TASK.plandatetime,
    D type of R_SHORTNUMBER,
    DWH type of R_SHORTNUMBER,
    DWH1 type of R_SHORTNUMBER,
    DWHG type of R_SHORTNUMBER,
    CLIENT type of R_FULLNAME,
    CLIENTTITLE type of RBS_BIGVARCHAR
)
AS
declare variable ttid_gateauto type of column WM_TASKTYPE.tasktypeid;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable clientid type of column OBJECT.objid;
declare variable clientcnt type of R_SHORTNUMBER;
begin
    execute procedure wh_ttid_gateauto
     returning_values :ttid_gateauto;

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    for
        with ga as (
            select t.taskid, t.status, t.plandatetime, t.siteid, t.infoid
              from wm_task t
             where t.tasktypeid = :ttid_gateauto
               and t.status = '0'
             union distinct
            select t.taskid, t.status, t.plandatetime, t.siteid, t.infoid
              from wm_task t
             where t.tasktypeid = :ttid_gateauto
               and t.status = '1'
        )
        select ga.taskid, rs.code, rs.name, ga.plandatetime,
               s.siteid, s.name, a.aid, a.name,
               count(distinct d.docid),
               sum(iif(d.fromobj = :whid, 1, 0)),
               sum(iif(d.fromobj = :whid and d.status='1', 1, 0)),
               sum(iif(d.fromobj = :whid and d.status='g', 1, 0)),
               max(iif(d.fromobj = :whid, d.toobj, 0)),
               count(distinct iif(d.fromobj = :whid, d.toobj, NULL)),
               list((select objname from wh_get_objectname(d.toobj)))
          from ga
               left join wh_taskbond tb
                    left join wm_task t
                         left join document d on d.docid = t.docid
                      on t.taskid = tb.task2id
                 on tb.task1id = ga.taskid and tb.taskbondtid = :tbtid_cardocs
               left join site s on s.siteid = ga.siteid
               left join t_auto a on a.aid = ga.infoid
               left join r_status rs on rs.statustype = 'T' and rs.code = t.status
         where d.docid is NOT NULL
         group by ga.taskid, rs.code, rs.name, ga.plandatetime, s.siteid, s.name, a.aid, a.name
          into :tid, :tstat, :tstatname, :plandatetime, :gateid, :gatename, :autoid, :autoname,
               :d, :dwh, :dwh1, :dwhg, :clientid, :clientcnt, :clienttitle
    do
    begin
        if (:clientcnt=0) then
            client = '';
        else if (:clientcnt = 1) then
            select w.objname
              from wh_get_objectname(:clientid) w
              into :client;
        else
            client = '==='||cast(:clientcnt as varchar(10))||'===';

        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELMANAG_LISTGATEAUTO (
    WHID type of column OBJECT.objid
)
returns (
    TID type of column WM_TASK.taskid,
    GATEID type of column SITE.siteid,
    GATENAME type of column SITE.name,
    AUTOID type of column T_AUTO.aid,
    AUTONAME type of column T_AUTO.name,
    TSTAT type of column R_STATUS.code,
    TSTATNAME type of column R_STATUS.name,
    PLANDATETIME type of column WM_TASK.plandatetime,
    D type of R_SHORTNUMBER,
    DWH type of R_SHORTNUMBER,
    DWH1 type of R_SHORTNUMBER,
    DWHG type of R_SHORTNUMBER,
    CLIENT type of R_FULLNAME,
    CLIENTTITLE type of RBS_BIGVARCHAR
)
AS
declare variable ttid_gateauto type of column WM_TASKTYPE.tasktypeid;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable clientid type of column OBJECT.objid;
declare variable clientcnt type of R_SHORTNUMBER;
begin
    execute procedure wh_ttid_gateauto
     returning_values :ttid_gateauto;

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    for
        with ga as (
            select t.taskid, t.status, t.plandatetime, t.siteid, t.infoid
              from wm_task t
             where t.tasktypeid = :ttid_gateauto
               and t.status = '0'
             union distinct
            select t.taskid, t.status, t.plandatetime, t.siteid, t.infoid
              from wm_task t
             where t.tasktypeid = :ttid_gateauto
               and t.status = '1'
        )
        select ga.taskid, rs.code, rs.name, ga.plandatetime,
               s.siteid, s.name, a.aid, a.name,
               count(distinct d.docid),
               sum(iif(d.fromobj = :whid, 1, 0)),
               sum(iif(d.fromobj = :whid and d.status='1', 1, 0)),
               sum(iif(d.fromobj = :whid and d.status='g', 1, 0)),
               max(iif(d.fromobj = :whid, d.toobj, 0)),
               count(distinct iif(d.fromobj = :whid, d.toobj, NULL)),
               list(distinct (select objname from wh_get_objectname(d.toobj)))
          from ga
               left join wh_taskbond tb
                    left join wm_task t
                         left join document d on d.docid = t.docid
                      on t.taskid = tb.task2id
                 on tb.task1id = ga.taskid and tb.taskbondtid = :tbtid_cardocs
               left join site s on s.siteid = ga.siteid
               left join t_auto a on a.aid = ga.infoid
               left join r_status rs on rs.statustype = 'T' and rs.code = t.status
         where d.docid is NOT NULL
         group by ga.taskid, rs.code, rs.name, ga.plandatetime, s.siteid, s.name, a.aid, a.name
          into :tid, :tstat, :tstatname, :plandatetime, :gateid, :gatename, :autoid, :autoname,
               :d, :dwh, :dwh1, :dwhg, :clientid, :clientcnt, :clienttitle
    do
    begin
        if (:clientcnt=0) then
            client = '';
        else if (:clientcnt = 1) then
            select w.objname
              from wh_get_objectname(:clientid) w
              into :client;
        else
            client = '==='||cast(:clientcnt as varchar(10))||'===';

        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELMANAG_LISTGATEAUTO (
    WHID type of column OBJECT.objid
)
returns (
    TID type of column WM_TASK.taskid,
    GATEID type of column SITE.siteid,
    GATENAME type of column SITE.name,
    AUTOID type of column T_AUTO.aid,
    AUTONAME type of column T_AUTO.name,
    TSTAT type of column R_STATUS.code,
    TSTATNAME type of column R_STATUS.name,
    PLANDATETIME type of column WM_TASK.plandatetime,
    D type of R_SHORTNUMBER,
    DWH type of R_SHORTNUMBER,
    DWH1 type of R_SHORTNUMBER,
    DWHG type of R_SHORTNUMBER,
    CLIENT type of R_FULLNAME,
    CLIENTTITLE type of RBS_BIGVARCHAR
)
AS
declare variable ttid_gateauto type of column WM_TASKTYPE.tasktypeid;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable clientid type of column OBJECT.objid;
declare variable clientcnt type of R_SHORTNUMBER;
begin
    execute procedure wh_ttid_gateauto
     returning_values :ttid_gateauto;

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    for
        with ga as (
            select t.taskid, t.status, t.plandatetime, t.siteid, t.infoid
              from wm_task t
             where t.tasktypeid = :ttid_gateauto
               and t.status = '0'
             union distinct
            select t.taskid, t.status, t.plandatetime, t.siteid, t.infoid
              from wm_task t
             where t.tasktypeid = :ttid_gateauto
               and t.status = '1'
        )
        select ga.taskid, rs.code, rs.name, ga.plandatetime,
               s.siteid, s.name, a.aid, a.name,
               count(distinct d.docid),
               sum(iif(d.fromobj = :whid, 1, 0)),
               sum(iif(d.fromobj = :whid and d.status='1', 1, 0)),
               sum(iif(d.fromobj = :whid and d.status='g', 1, 0)),
               max(iif(d.fromobj = :whid, d.toobj, 0)),
               count(distinct iif(d.fromobj = :whid, d.toobj, NULL)),
               list(distinct (select objname from wh_get_objectname(d.toobj)))
          from ga
               left join wh_taskbond tb
                    left join wm_task t
                         left join document d on d.docid = t.docid
                      on t.taskid = tb.task2id
                 on tb.task1id = ga.taskid and tb.taskbondtid = :tbtid_cardocs
               left join site s on s.siteid = ga.siteid
               left join t_auto a on a.aid = ga.infoid
               left join r_status rs on rs.statustype = 'T' and rs.code = t.status
         where d.docid is NOT NULL
         group by ga.taskid, rs.code, rs.name, ga.plandatetime, s.siteid, s.name, a.aid, a.name
         order by s.name
          into :tid, :tstat, :tstatname, :plandatetime, :gateid, :gatename, :autoid, :autoname,
               :d, :dwh, :dwh1, :dwhg, :clientid, :clientcnt, :clienttitle
    do
    begin
        if (:clientcnt=0) then
            client = '';
        else if (:clientcnt = 1) then
            select w.objname
              from wh_get_objectname(:clientid) w
              into :client;
        else
            client = '==='||cast(:clientcnt as varchar(10))||'===';

        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELMANAG_LISTGATEAUTO (
    WHID type of column OBJECT.objid
)
returns (
    TID type of column WM_TASK.taskid,
    GATEID type of column SITE.siteid,
    GATENAME type of column SITE.name,
    AUTOID type of column T_AUTO.aid,
    AUTONAME type of column T_AUTO.name,
    TSTAT type of column R_STATUS.code,
    TSTATNAME type of column R_STATUS.name,
    PLANDATETIME type of column WM_TASK.plandatetime,
    D type of R_SHORTNUMBER,
    DWH type of R_SHORTNUMBER,
    DWH1 type of R_SHORTNUMBER,
    DWHG type of R_SHORTNUMBER,
    CLIENT type of R_FULLNAME,
    CLIENTTITLE type of RBS_BIGVARCHAR
)
AS
declare variable ttid_gateauto type of column WM_TASKTYPE.tasktypeid;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable clientid type of column OBJECT.objid;
declare variable clientcnt type of R_SHORTNUMBER;
begin
    execute procedure wh_ttid_gateauto
     returning_values :ttid_gateauto;

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    for
        with ga as (
            select t.taskid, t.status, t.plandatetime, t.siteid, t.infoid
              from wm_task t
             where t.tasktypeid = :ttid_gateauto
               and t.status = '0'
             union distinct
            select t.taskid, t.status, t.plandatetime, t.siteid, t.infoid
              from wm_task t
             where t.tasktypeid = :ttid_gateauto
               and t.status = '1'
        )
        select ga.taskid, rs.code, rs.name, ga.plandatetime,
               s.siteid, s.name, a.aid, a.name,
               count(distinct d.docid),
               sum(iif(d.fromobj = :whid, 1, 0)),
               sum(iif(d.fromobj = :whid and d.status='1', 1, 0)),
               sum(iif(d.fromobj = :whid and d.status='g', 1, 0)),
               max(iif(d.fromobj = :whid, d.toobj, 0)),
               count(distinct iif(d.fromobj = :whid, d.toobj, NULL)),
               list(distinct (select objname from wh_get_objectname(d.toobj)))
          from ga
               left join wh_taskbond tb
                    left join wm_task t
                         left join document d on d.docid = t.docid
                      on t.taskid = tb.task2id
                 on tb.task1id = ga.taskid and tb.taskbondtid = :tbtid_cardocs
               left join site s on s.siteid = ga.siteid
               left join t_auto a on a.aid = ga.infoid
               left join r_status rs on rs.statustype = 'T' and rs.code = t.status
         where d.docid is NOT NULL
         group by ga.taskid, rs.code, rs.name, ga.plandatetime, s.siteid, s.name, a.aid, a.name
         order by ga.plandatetime
          into :tid, :tstat, :tstatname, :plandatetime, :gateid, :gatename, :autoid, :autoname,
               :d, :dwh, :dwh1, :dwhg, :clientid, :clientcnt, :clienttitle
    do
    begin
        if (:clientcnt=0) then
            client = '';
        else if (:clientcnt = 1) then
            select w.objname
              from wh_get_objectname(:clientid) w
              into :client;
        else
            client = '==='||cast(:clientcnt as varchar(10))||'===';

        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELMANAG_LISTGATEAUTO (
    WHID type of column OBJECT.objid
)
returns (
    TID type of column WM_TASK.taskid,
    GATEID type of column SITE.siteid,
    GATENAME type of column SITE.name,
    AUTOID type of column T_AUTO.aid,
    AUTONAME type of column T_AUTO.name,
    TSTAT type of column R_STATUS.code,
    TSTATNAME type of column R_STATUS.name,
    PLANDATETIME type of column WM_TASK.plandatetime,
    D type of R_SHORTNUMBER,
    DWH type of R_SHORTNUMBER,
    DWH1 type of R_SHORTNUMBER,
    DWHG type of R_SHORTNUMBER,
    CLIENT type of R_FULLNAME,
    CLIENTTITLE type of RBS_BIGVARCHAR
)
AS
declare variable ttid_gateauto type of column WM_TASKTYPE.tasktypeid;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable clientid type of column OBJECT.objid;
declare variable clientcnt type of R_SHORTNUMBER;
begin
    execute procedure wh_ttid_gateauto
     returning_values :ttid_gateauto;

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    for
        with ga as (
            select t.taskid, t.status, t.plandatetime, t.siteid, t.infoid
              from wm_task t
             where t.tasktypeid = :ttid_gateauto
               and t.status = '0'
             union distinct
            select t.taskid, t.status, t.plandatetime, t.siteid, t.infoid
              from wm_task t
             where t.tasktypeid = :ttid_gateauto
               and t.status = '1'
        )
        select ga.taskid, rs.code, rs.name, ga.plandatetime,
               s.siteid, s.name, a.aid, a.name,
               count(distinct d.docid),
               sum(iif(d.fromobj = :whid, 1, 0)),
               sum(iif(d.fromobj = :whid and d.status='1', 1, 0)),
               sum(iif(d.fromobj = :whid and d.status='g', 1, 0)),
               max(iif(d.fromobj = :whid, d.toobj, 0)),
               count(distinct iif(d.fromobj = :whid, d.toobj, NULL)),
               list(distinct (select objname from wh_get_objectname(d.toobj)))
          from ga
               left join wh_taskbond tb
                    left join wm_task t
                         left join document d on d.docid = t.docid
                      on t.taskid = tb.task2id
                 on tb.task1id = ga.taskid and tb.taskbondtid = :tbtid_cardocs
               left join site s on s.siteid = ga.siteid
               left join t_auto a on a.aid = ga.infoid
               left join r_status rs on rs.statustype = 'T' and rs.code = ga.status
         where d.docid is NOT NULL
         group by ga.taskid, rs.code, rs.name, ga.plandatetime, s.siteid, s.name, a.aid, a.name
         order by ga.plandatetime
          into :tid, :tstat, :tstatname, :plandatetime, :gateid, :gatename, :autoid, :autoname,
               :d, :dwh, :dwh1, :dwhg, :clientid, :clientcnt, :clienttitle
    do
    begin
        if (:clientcnt=0) then
            client = '';
        else if (:clientcnt = 1) then
            select w.objname
              from wh_get_objectname(:clientid) w
              into :client;
        else
            client = '==='||cast(:clientcnt as varchar(10))||'===';

        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_SELMANAG_LISTGATEAUTODOCS (
    TASKID_GATEAUTO type of column WM_TASK.taskid,
    WHID type of column OBJECT.objid
)
returns (
    DOCID type of column DOCUMENT.DOCID,
    DOCDATE type of column DOCUMENT.DOCDATE,
    RDOCDATE type of column DOCUMENT.REALDOCDATE,
    DOCNUM type of column DOCUMENT.NUMBER,
    DOCSUM type of column DOCUMENT.AMOUNT,
    STAT type of column R_STATUS.CODE,
    STATNAME type of column R_STATUS.NAME,
    THROUGHNAME type of R_FULLNAME,
    TONAME type of R_FULLNAME
)
AS
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
begin
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    for
        select d.DOCID, d.DOCDATE, d.REALDOCDATE, d.number, d.amount,
               rs.code, rs.name,
               (select objname from wh_get_objectname(d.throughobj)),
               (select objname from wh_get_objectname(d.throughobj))
          from wh_taskbond tb
               left join wm_task t
                    left join document d
                         left join r_status rs on rs.statustype='O' and rs.code=d.status
                      on d.docid = t.docid
                 on t.taskid = tb.task2id
         where tb.task1id = :taskid_gateauto
           and tb.taskbondtid = :tbtid_cardocs
           and d.fromobj = :whid
          into :docid,:docdate,:docnum,:docsum,:rdocdate,:stat,:statname,:throughname,:toname
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELMANAG_LISTGATEAUTODOCS (
    TASKID_GATEAUTO type of column WM_TASK.taskid,
    WHID type of column OBJECT.objid
)
returns (
    DOCID type of column DOCUMENT.DOCID,
    DOCDATE type of column DOCUMENT.DOCDATE,
    RDOCDATE type of column DOCUMENT.REALDOCDATE,
    DOCNUM type of column DOCUMENT.NUMBER,
    DOCSUM type of column DOCUMENT.AMOUNT,
    STAT type of column R_STATUS.CODE,
    STATNAME type of column R_STATUS.NAME,
    THROUGHNAME type of R_FULLNAME,
    TONAME type of R_FULLNAME
)
AS
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
begin
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    for
        select d.DOCID, d.DOCDATE, d.REALDOCDATE, d.number, d.amount,
               rs.code, rs.name,
               (select objname from wh_get_objectname(d.throughobj)),
               (select objname from wh_get_objectname(d.toobj))
          from wh_taskbond tb
               left join wm_task t
                    left join document d
                         left join r_status rs on rs.statustype='O' and rs.code=d.status
                      on d.docid = t.docid
                 on t.taskid = tb.task2id
         where tb.task1id = :taskid_gateauto
           and tb.taskbondtid = :tbtid_cardocs
           and d.fromobj = :whid
          into :docid,:docdate,:rdocdate,:docnum,:docsum,
               :stat,:statname,:throughname,:toname
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



DROP PROCEDURE U3S_SELMANAG_LISTCLIENTDOCS;



SET TERM ^ ;

create or alter procedure K_SELMANAG_LISTGATEAUTOTASKES (
    TASKID_GATEAUTO type of column WM_TASK.taskid ,
    WHID type of column OBJECT.objid
)
returns (
    TID type of column WM_TASK.taskid,
    TSTAT type of column R_STATUS.code,
    TSTATNAME type of column R_STATUS.name,
    DOCNUM type of column DOCUMENT.number,
    TWEIGHT type of column WM_TASK.weight,
    TCAPACITY type of column WM_TASK.capacity,
    TMALGO type of column wm_taskmethod.algorithm,
    TMNAME type of column wm_taskmethod.name,
    FIO type of R_FULLNAME
)
AS
declare variable ttid_select type of column wm_tasktype.tasktypeid;
begin
    execute procedure wh_ttid_select
     returning_values :ttid_select;

    for
        select t.status,rs.name,t.taskid,t.weight,t.capacity,k.docnum,tm.algorithm,tm.name,
               (select objname from wh_get_objectname(wms.objid))
          from wh_selmanag_listgateautodocs(:taskid_gateauto,:whid) k
               left join wm_task t
                    left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                    left join r_status rs on rs.code = t.status and rs.statustype = 'T'
                    left join wm_session wms on wms.sessionid = t.wm_sessionid
                 on t.docid = k.docid
         where t.tasktypeid = :ttid_select
          into :tstat,:tstatname,:tid,:tweight,:tcapacity,:docnum,:tmalgo,:tmname,:fio
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_SELECT_TASK_MAP (
    TID R_ID)
returns (
    TWID type of R_ID,
    WID type of R_ID,
    BTIME type of R_DATETIME,
    ETIME type of R_DATETIME,
    NUM type of R_NUMBER,
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    QO type of R_QUANTITY,
    QF type of R_QUANTITY,
    TWSTAT type of R_STATUS,
    VUFACTOR type of R_MULTIPLE,
    VUCODE type of R_CODE,
    MUFACTOR type of R_MULTIPLE,
    MUCODE type of R_CODE,
    WMSESID type of R_ID,
    OBJNAME type of R_FULLNAME,
    PLANDATETIME type of column WM_TASK_WARES.plandatetime)
AS
declare variable DOCID type of column DOCUMENT.docid;
declare variable WLOTID type of column WARESLOT.wlotid;
declare variable PALLETID type of column PALLET.palletid;
declare variable QCANC R_DOUBLE;
declare variable QSEL R_DOUBLE;
declare variable QFTW R_DOUBLE;
begin
    select t.docid
      from wm_task t
     where t.taskid = :tid
      into :docid;

    insert into rbs_tmp_taskwareslot(taskwaresid,palletid,wlotid,quantity)
    select tw.taskwaresid,tl.palletid,tl.wlotid,-sum(tl.quantity)
      from wm_task_wares tw
           left join wm_task_lot tl on tl.taskwaresid=tw.taskwaresid
     where tw.taskid = :tid
       and tw.status = '2'
       and coalesce(tl.quantity,0.000)<0.0001
     group by tw.taskwaresid,tl.palletid,tl.wlotid;

    for
        select tl.wlotid,tl.palletid,sum(tl.quantity)
          from wm_task t
               left join wm_tasktype tt on tt.tasktypeid=t.tasktypeid
               left join wm_task_wares tw
                    left join wm_task_lot tl on tl.taskwaresid = tw.taskwaresid
                 on tw.taskid = t.taskid
         where t.docid = :docid
           and t.ownertask = :tid
           and tt.code = 'SELECTCANC'
         group by tl.wlotid,tl.palletid
          into :wlotid,:palletid,:qcanc
    do
    begin
       for
        select r.taskwaresid,r.quantity
          from rbs_tmp_taskwareslot r
         where r.wlotid = :wlotid
           and r.palletid = :palletid
           and r.quantity > 0.00001
          into :twid,:qsel
       do
       if (abs(:qcanc)>0.00001) then
       begin
            if (:qsel<:qcanc) then
            begin
                qcanc = :qcanc - :qsel;
                delete from rbs_tmp_taskwareslot r
                 where r.taskwaresid = :twid and r.palletid = :palletid and r.wlotid = :wlotid;
            end
            else
            begin
                update rbs_tmp_taskwareslot r
                   set r.quantity = :qsel - :qcanc
                 where r.taskwaresid = :twid and r.palletid = :palletid and r.wlotid = :wlotid;
                qcanc = 0.000;
            end
       end
    end

    for
        select tw.taskwaresid,min(tw.waresid),min(tw.num),min(coalesce(tw.status,'0')),
               min(tw.wm_sessionid),min(tw.begintime),max(tw.endtime),
               sum(tw.quantity),sum(tw.scanquant),
               sum(case
                 when coalesce(tw.status,'0') in ('0','1') then tw.scanquant
                 else r.quantity
               end)
          from wm_task_wares tw
               left join rbs_tmp_taskwareslot r on r.taskwaresid=tw.taskwaresid
         where tw.taskid = :tid
           and (coalesce(tw.status,'0') <> '2' or r.taskwaresid is NOT NULL)
         group by tw.taskwaresid
         order by 3
          into :twid,:wid,:num,:twstat,:wmsesid,:btime,:etime,:qo,:qftw,:qf
    do
    begin
        if (:qftw is NULL) then qftw = 0.000;
        if (:qf is NULL) then qf = 0.000;

        if (:twstat='2' and abs(:qftw-:qf)>0.0001) then qo = :qf;

        select g.code,g.name,vu.shortname,vwu.factor,mu.shortname,mwu.factor
          from gwares g
               left join waresunit mwu
                    left join unit mu on mu.unitid = mwu.unitid
                 on mwu.waresunitid=g.mainunitid
               left join waresunit vwu
                    left join unit vu on vu.unitid = vwu.unitid
                 on vwu.waresunitid=g.viewunitid
         where g.waresid = :wid
          into :wcode,:wname,:vucode,:vufactor,:mucode,:mufactor;

        select (select fullname from getobjectname(wms.objid,'03'))
          from wm_session wms
         where wms.sessionid = :wmsesid
          into :objname;

        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_SELECT_TASK_MAP_EX (
    TID type of column WM_TASK.taskid
)
returns (
    TWID type of column wm_task_wares.taskwaresid,
    WID type of column gwares.waresid,
    BTIME type of column wm_task_wares.begintime,
    ETIME type of column wm_task_wares.endtime,
    PlanDateTime type of column wm_task_wares.plandatetime,
    NUM type of column wm_task_wares.num,
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    QO type of R_QUANTITY,
    QF type of R_QUANTITY,
    QR type of R_QUANTITY,
    TWSTAT type of column WM_TASK_WARES.status,
    VUFACTOR type of column WARESUNIT.factor,
    VUCODE type of column UNIT.shortname,
    MUFACTOR type of column WARESUNIT.factor,
    MUCODE type of column UNIT.shortname,
    WMSESID type of column WM_SESSION.sessionid,
    OBJNAME type of R_FULLNAME)
AS
declare variable fromobj type of r_id;
begin
    select d.fromobj
      from wm_task t
           left join document d on d.docid = t.docid
     where t.taskid = :tid
      into :fromobj;

    for
        select k.TWID,k.WID,k.BTIME,k.ETIME,k.NUM,k.PlanDateTime,
               k.WCODE,k.WNAME,k.QO,k.QF,wr.rest,
               k.TWSTAT,k.VUFACTOR,k.VUCODE,k.MUFACTOR,k.MUCODE,k.WMSESID,k.OBJNAME
          from k_wh_select_task_map(:tid) k
               left join k_rest_wareslot_obj(:fromobj, k.wid) wr on 1=1
          into :TWID,:WID,:BTIME,:ETIME,:NUM,:PlanDateTime,
               :WCODE,:WNAME,:QO,:QF,:QR,
               :TWSTAT,:VUFACTOR,:VUCODE,:MUFACTOR,:MUCODE,:WMSESID,:OBJNAME
    do
     suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_SELECT_TASK_MAP (
    TID R_ID)
returns (
    TWID type of R_ID,
    WID type of R_ID,
    BTIME type of R_DATETIME,
    ETIME type of R_DATETIME,
    NUM type of R_NUMBER,
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    QO type of R_QUANTITY,
    QF type of R_QUANTITY,
    TWSTAT type of R_STATUS,
    VUFACTOR type of R_MULTIPLE,
    VUCODE type of R_CODE,
    MUFACTOR type of R_MULTIPLE,
    MUCODE type of R_CODE,
    WMSESID type of R_ID,
    OBJNAME type of R_FULLNAME,
    PLANDATETIME type of column WM_TASK_WARES.plandatetime)
AS
declare variable DOCID type of column DOCUMENT.docid;
declare variable WLOTID type of column WARESLOT.wlotid;
declare variable PALLETID type of column PALLET.palletid;
declare variable QCANC R_DOUBLE;
declare variable QSEL R_DOUBLE;
declare variable QFTW R_DOUBLE;
begin
    select t.docid
      from wm_task t
     where t.taskid = :tid
      into :docid;

    insert into rbs_tmp_taskwareslot(taskwaresid,palletid,wlotid,quantity)
    select tw.taskwaresid,tl.palletid,tl.wlotid,-sum(tl.quantity)
      from wm_task_wares tw
           left join wm_task_lot tl on tl.taskwaresid=tw.taskwaresid
     where tw.taskid = :tid
       and tw.status = '2'
       and coalesce(tl.quantity,0.000)<0.0001
     group by tw.taskwaresid,tl.palletid,tl.wlotid;

    for
        select tl.wlotid,tl.palletid,sum(tl.quantity)
          from wm_task t
               left join wm_tasktype tt on tt.tasktypeid=t.tasktypeid
               left join wm_task_wares tw
                    left join wm_task_lot tl on tl.taskwaresid = tw.taskwaresid
                 on tw.taskid = t.taskid
         where t.docid = :docid
           and t.ownertask = :tid
           and tt.code = 'SELECTCANC'
         group by tl.wlotid,tl.palletid
          into :wlotid,:palletid,:qcanc
    do
    begin
       for
        select r.taskwaresid,r.quantity
          from rbs_tmp_taskwareslot r
         where r.wlotid = :wlotid
           and r.palletid = :palletid
           and r.quantity > 0.00001
          into :twid,:qsel
       do
       if (abs(:qcanc)>0.00001) then
       begin
            if (:qsel<:qcanc) then
            begin
                qcanc = :qcanc - :qsel;
                delete from rbs_tmp_taskwareslot r
                 where r.taskwaresid = :twid and r.palletid = :palletid and r.wlotid = :wlotid;
            end
            else
            begin
                update rbs_tmp_taskwareslot r
                   set r.quantity = :qsel - :qcanc
                 where r.taskwaresid = :twid and r.palletid = :palletid and r.wlotid = :wlotid;
                qcanc = 0.000;
            end
       end
    end

    for
        select tw.taskwaresid,min(tw.waresid),min(tw.num),min(coalesce(tw.status,'0')),
               min(tw.wm_sessionid),min(tw.begintime),max(tw.endtime),max(tw.plandatetime),
               sum(tw.quantity),sum(tw.scanquant),
               sum(case
                 when coalesce(tw.status,'0') in ('0','1') then tw.scanquant
                 else r.quantity
               end)
          from wm_task_wares tw
               left join rbs_tmp_taskwareslot r on r.taskwaresid=tw.taskwaresid
         where tw.taskid = :tid
           and (coalesce(tw.status,'0') <> '2' or r.taskwaresid is NOT NULL)
         group by tw.taskwaresid
         order by 3
          into :twid,:wid,:num,:twstat,:wmsesid,:btime,:etime,:plandatetime,:qo,:qftw,:qf
    do
    begin
        if (:qftw is NULL) then qftw = 0.000;
        if (:qf is NULL) then qf = 0.000;

        if (:twstat='2' and abs(:qftw-:qf)>0.0001) then qo = :qf;

        select g.code,g.name,vu.shortname,vwu.factor,mu.shortname,mwu.factor
          from gwares g
               left join waresunit mwu
                    left join unit mu on mu.unitid = mwu.unitid
                 on mwu.waresunitid=g.mainunitid
               left join waresunit vwu
                    left join unit vu on vu.unitid = vwu.unitid
                 on vwu.waresunitid=g.viewunitid
         where g.waresid = :wid
          into :wcode,:wname,:vucode,:vufactor,:mucode,:mufactor;

        select (select fullname from getobjectname(wms.objid,'03'))
          from wm_session wms
         where wms.sessionid = :wmsesid
          into :objname;

        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_SELECT_TASK_MAP_EX (
    TID type of column WM_TASK.taskid
)
returns (
    TWID type of column wm_task_wares.taskwaresid,
    WID type of column gwares.waresid,
    BTIME type of column wm_task_wares.begintime,
    ETIME type of column wm_task_wares.endtime,
    PlanDateTime type of column wm_task_wares.plandatetime,
    NUM type of column wm_task_wares.num,
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    QO type of R_QUANTITY,
    QF type of R_QUANTITY,
    QR type of R_QUANTITY,
    TWSTAT type of column WM_TASK_WARES.status,
    VUFACTOR type of column WARESUNIT.factor,
    VUCODE type of column UNIT.shortname,
    MUFACTOR type of column WARESUNIT.factor,
    MUCODE type of column UNIT.shortname,
    WMSESID type of column WM_SESSION.sessionid,
    OBJNAME type of R_FULLNAME)
AS
declare variable fromobj type of r_id;
begin
    select d.fromobj
      from wm_task t
           left join document d on d.docid = t.docid
     where t.taskid = :tid
      into :fromobj;

    for
        select k.TWID,k.WID,k.BTIME,k.ETIME,k.NUM,k.PlanDateTime,
               k.WCODE,k.WNAME,k.QO,k.QF,wr.rest,
               k.TWSTAT,k.VUFACTOR,k.VUCODE,k.MUFACTOR,k.MUCODE,k.WMSESID,k.OBJNAME
          from k_wh_select_task_map(:tid) k
               left join k_rest_wareslot_obj(:fromobj, k.wid) wr on 1=1
          into :TWID,:WID,:BTIME,:ETIME,:NUM,:PlanDateTime,
               :WCODE,:WNAME,:QO,:QF,:QR,
               :TWSTAT,:VUFACTOR,:VUCODE,:MUFACTOR,:MUCODE,:WMSESID,:OBJNAME
    do
     suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_SELECT_DOC_MAP_EX (
    DOCID type of column DOCUMENT.docid)
returns (
    TID type of column WM_TASK.taskid,
    WID type of column GWARES.waresid,
    BTIME type of column wm_task_wares.begintime,
    ETIME type of column wm_task_wares.endtime,
    PLANDATETIME type of column wm_task_wares.plandatetime,
    NUM type of column wm_task_wares.num,
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    VUFACTOR type of column WARESUNIT.factor,
    VUCODE type of column UNIT.shortname,
    MUFACTOR type of column WARESUNIT.factor,
    MUCODE type of column UNIT.shortname,
    QO type of R_QUANTITY,
    QF type of R_QUANTITY,
    QR type of R_QUANTITY,
    TWSTAT type of column WM_TASK_WARES.status,
    WMSESID type of column WM_SESSION.sessionid,
    OBJNAME type of R_FULLNAME)
AS
declare variable docstatus type of column r_status.code;
declare variable ttid type of column wm_tasktype.tasktypeid;
begin
    select d.status
      from document d
     where d.docid = :docid
      into :docstatus;

    execute procedure wh_ttid_select
     returning_values :ttid;

    if (:docstatus in ('g','2')) then
    begin
        for
            select t.taskid,g.waresid,g.code,g.name,tw.num,coalesce(tw.status,'0'),
                   vwu.factor,vu.shortname,mwu.factor,mu.shortname,
                   tw.begintime,tw.endtime,tw.plandatetime,
                   coalesce(tw.quantity,0.000),coalesce(tw.scanquant,0.000),wr.rest,
                   wms.sessionid,(select fullname from getobjectname(wms.objid,'03'))
              from wm_task t
                   left join wm_task_wares tw
                        left join gwares g
                             left join waresunit mwu
                                  left join unit mu on mu.unitid=mwu.unitid
                               on mwu.waresunitid=g.mainunitid
                             left join waresunit vwu
                                  left join unit vu on vu.unitid=vwu.unitid
                               on vwu.waresunitid=g.viewunitid
                          on g.waresid=tw.waresid
                        left join wm_session wms on wms.sessionid=tw.wm_sessionid
                        left join k_rest_wareslot(tw.waresid) wr on 1=1
                     on tw.taskid=t.taskid
             where t.docid = :docid
               and t.tasktypeid = :ttid
               and tw.tasktypeid = :ttid
             order by tw.taskid,tw.num
              into :tid,:wid,:wcode,:wname,:num,:twstat,
                   :vufactor,:vucode,:mufactor,:mucode, 
                   :btime,:etime,:plandatetime,
                   :qo,:qf,:qr,
                   :wmsesid,:objname
        do
            suspend;
    end
    else
    begin
        num = 0;
        twstat = '0';
        tid = null;
        btime = null;
        etime = null;
        wmsesid = null;
        objname = null;

        for
            select g.waresid,g.code,g.name,
                   vwu.factor,vu.shortname,mwu.factor,mu.shortname,
                   coalesce(cg.amount,0.000),0.000,wr.rest
              from cargo cg
                   left join gwares g
                        left join waresunit mwu
                             left join unit mu on mu.unitid=mwu.unitid
                          on mwu.waresunitid=g.mainunitid
                        left join waresunit vwu
                             left join unit vu on vu.unitid=vwu.unitid
                          on vwu.waresunitid=g.viewunitid
                     on g.waresid=cg.waresid
                   left join k_rest_wareslot(cg.waresid) wr on 1=1
             where cg.document = :docid
              into :wid,:wcode,:wname,
                   :vufactor,:vucode,:mufactor,:mucode,
                   :qo,:qf,:qr
        do
        begin
            num = :num + 1;
            suspend;
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_SELECT_DOC_MAP_EX (
    DOCID type of column DOCUMENT.docid)
returns (
    TID type of column WM_TASK.taskid,
    WID type of column GWARES.waresid,
    BTIME type of column wm_task_wares.begintime,
    ETIME type of column wm_task_wares.endtime,
    PLANDATETIME type of column wm_task_wares.plandatetime,
    NUM type of column wm_task_wares.num,
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    VUFACTOR type of column WARESUNIT.factor,
    VUCODE type of column UNIT.shortname,
    MUFACTOR type of column WARESUNIT.factor,
    MUCODE type of column UNIT.shortname,
    QO type of R_QUANTITY,
    QF type of R_QUANTITY,
    QR type of R_QUANTITY,
    TWSTAT type of column WM_TASK_WARES.status,
    WMSESID type of column WM_SESSION.sessionid,
    OBJNAME type of R_FULLNAME)
AS
declare variable docstatus type of column r_status.code;
declare variable ttid type of column wm_tasktype.tasktypeid;
begin
    select d.status
      from document d
     where d.docid = :docid
      into :docstatus;

    execute procedure wh_ttid_select
     returning_values :ttid;

    if (:docstatus in ('g','2','e')) then
    begin
        for
            select t.taskid,g.waresid,g.code,g.name,tw.num,coalesce(tw.status,'0'),
                   vwu.factor,vu.shortname,mwu.factor,mu.shortname,
                   tw.begintime,tw.endtime,tw.plandatetime,
                   coalesce(tw.quantity,0.000),coalesce(tw.scanquant,0.000),wr.rest,
                   wms.sessionid,(select fullname from getobjectname(wms.objid,'03'))
              from wm_task t
                   left join wm_task_wares tw
                        left join gwares g
                             left join waresunit mwu
                                  left join unit mu on mu.unitid=mwu.unitid
                               on mwu.waresunitid=g.mainunitid
                             left join waresunit vwu
                                  left join unit vu on vu.unitid=vwu.unitid
                               on vwu.waresunitid=g.viewunitid
                          on g.waresid=tw.waresid
                        left join wm_session wms on wms.sessionid=tw.wm_sessionid
                        left join k_rest_wareslot(tw.waresid) wr on 1=1
                     on tw.taskid=t.taskid
             where t.docid = :docid
               and t.tasktypeid = :ttid
               and tw.tasktypeid = :ttid
             order by tw.taskid,tw.num
              into :tid,:wid,:wcode,:wname,:num,:twstat,
                   :vufactor,:vucode,:mufactor,:mucode, 
                   :btime,:etime,:plandatetime,
                   :qo,:qf,:qr,
                   :wmsesid,:objname
        do
            suspend;
    end
    else
    begin
        num = 0;
        twstat = '0';
        tid = null;
        btime = null;
        etime = null;
        wmsesid = null;
        objname = null;

        for
            select g.waresid,g.code,g.name,
                   vwu.factor,vu.shortname,mwu.factor,mu.shortname,
                   coalesce(cg.amount,0.000),0.000,wr.rest
              from cargo cg
                   left join gwares g
                        left join waresunit mwu
                             left join unit mu on mu.unitid=mwu.unitid
                          on mwu.waresunitid=g.mainunitid
                        left join waresunit vwu
                             left join unit vu on vu.unitid=vwu.unitid
                          on vwu.waresunitid=g.viewunitid
                     on g.waresid=cg.waresid
                   left join k_rest_wareslot(cg.waresid) wr on 1=1
             where cg.document = :docid
              into :wid,:wcode,:wname,
                   :vufactor,:vucode,:mufactor,:mucode,
                   :qo,:qf,:qr
        do
        begin
            num = :num + 1;
            suspend;
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELMANAG_LISTGATEAUTODOCS (
    TASKID_GATEAUTO type of column WM_TASK.taskid,
    WHID type of column OBJECT.objid
)
returns (
    TPRIORITY type of column WM_TASK.priority,
    DOCID type of column DOCUMENT.DOCID,
    DOCDATE type of column DOCUMENT.DOCDATE,
    RDOCDATE type of column DOCUMENT.REALDOCDATE,
    DOCNUM type of column DOCUMENT.NUMBER,
    DOCSUM type of column DOCUMENT.AMOUNT,
    STAT type of column R_STATUS.CODE,
    STATNAME type of column R_STATUS.NAME,
    THROUGHNAME type of R_FULLNAME,
    TONAME type of R_FULLNAME
)
AS
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
begin
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    for
        select t.priority, d.DOCID, d.DOCDATE, d.REALDOCDATE, d.number, d.amount,
               rs.code, rs.name,
               (select objname from wh_get_objectname(d.throughobj)),
               (select objname from wh_get_objectname(d.toobj))
          from wh_taskbond tb
               left join wm_task t
                    left join document d
                         left join r_status rs on rs.statustype='O' and rs.code=d.status
                      on d.docid = t.docid
                 on t.taskid = tb.task2id
         where tb.task1id = :taskid_gateauto
           and tb.taskbondtid = :tbtid_cardocs
           and d.fromobj = :whid
          into :tpriority, :docid,:docdate,:rdocdate,:docnum,:docsum,
               :stat,:statname,:throughname,:toname
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_SELMNGRGA_LISTTASKES (
    FROMID type of column OBJECT.objid,
    TOID type of column OBJECT.objid,
    DBEG type of R_DATETIME,
    DEND type of R_DATETIME,
    TASKID_GATEAUTO type of column wm_task.taskid,
    DOCID type of column DOCUMENT.docid
)
returns (
    TID type of column WM_TASK.taskid,
    TSTAT type of column R_STATUS.CODE,
    TSTATNAME type of column R_STATUS.NAME,
    TMALGO type of column wm_taskmethod.algorithm,
    TMNAME type of column WM_TASKMETHOD.name,
    TONAME type of R_FULLNAME,
    THROUGHNAME type of R_FULLNAME,
    DOCNUM type of column DOCUMENT.number,
    RDDATE type of R_DATE,
    FIO type of R_FULLNAME,
    WEIGHT type of R_DOUBLE,
    CAPACITY type of R_DOUBLE)
AS
declare variable dtid_sale type of column DOCTYPE.doctid;
declare variable ttid_select type of column WM_TASKTYPE.tasktypeid;
begin
    execute procedure wh_dtid_sale
     returning_values :dtid_sale;

    execute procedure wh_ttid_select
     returning_values :ttid_select;

    if (:docid is NOT NULL) then
    begin
        for
            select d.realdocdate,d.number,
                   t.taskid,t.status,rs.name,
                   tm.algorithm,tm.name,
                   t.weight,t.capacity,
                   (select fullname from getobjectname(wms.objid,'03')),
                   (select fullname from getobjectname(d.toobj,NULL)),
                   (select fullname from getobjectname(d.throughobj,NULL))
              from document d
                   left join wm_task t
                        left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                        left join r_status rs on rs.code = t.status and rs.statustype = 'T'
                        left join wm_session wms on wms.sessionid = t.wm_sessionid
                     on t.docid = d.docid
             where d.docid = :docid
               and d.fromobj = :fromid
               and d.status = 'g'
               and t.tasktypeid = :ttid_select
               and t.taskmethodid is NOT NULL
               and t.status <> '2'
              into :rddate,:docnum,:tid,:tstat,:tstatname,:tmalgo,:tmname,
                   :weight,:capacity,:fio,:toname,:throughname
        do
            suspend;
    end
    else if (:taskid_gateauto is NOT NULL) then
    begin
        for
            select w.rdocdate, w.docnum,
                   t.taskid,t.status,rs.name,
                   tm.algorithm,tm.name,
                   t.weight,t.capacity,
                   (select fullname from getobjectname(wms.objid,'03')),
                   w.throughname, w.toname
              from WH_SELMANAG_LISTGATEAUTODOCS(:taskid_gateauto, :fromid) w
                   left join wm_task t
                        left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                        left join r_status rs on rs.code = t.status and rs.statustype = 'T'
                        left join wm_session wms on wms.sessionid = t.wm_sessionid
                     on t.docid = w.docid
             where t.tasktypeid = :ttid_select
               and t.taskmethodid is NOT NULL
               and t.status <> '2'
              into :rddate,:docnum,:tid,:tstat,:tstatname,:tmalgo,:tmname,
                   :weight,:capacity,:fio,:toname,:throughname
        do
            suspend;
    end
    else if (:toid is NOT NULL) then
        for
            select d.realdocdate,d.number,
                   t.taskid,t.status,rs.name,
                   tm.algorithm,tm.name,
                   t.weight,t.capacity,
                   (select fullname from getobjectname(wms.objid,'03')),
                   (select fullname from getobjectname(d.toobj,NULL)),
                   (select fullname from getobjectname(d.throughobj,NULL))
              from document d
                   left join wm_task t
                        left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                        left join r_status rs on rs.code = t.status and rs.statustype = 'T'
                        left join wm_session wms on wms.sessionid = t.wm_sessionid
                     on t.docid = d.docid
             where d.doctype = :dtid_sale
               and d.realdocdate between :dbeg and :dend
               and d.status = 'g'
               and d.fromobj = :fromid
               and d.toobj=:toid
               and t.tasktypeid = :ttid_select
               and t.taskmethodid is NOT NULL
               and t.status <> '2'
              into :rddate,:docnum,:tid,:tstat,:tstatname,:tmalgo,:tmname,
                   :weight,:capacity,:fio,:toname,:throughname
        do
            suspend;
    else
        for
            select d.realdocdate,d.number,
                   t.taskid,t.status,rs.name,
                   tm.algorithm,tm.name,
                   t.weight,t.capacity,
                   (select fullname from getobjectname(wms.objid,'03')),
                   (select fullname from getobjectname(d.toobj,NULL)),
                   (select fullname from getobjectname(d.throughobj,NULL))
              from document d
                   left join wm_task t
                        left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                        left join r_status rs on rs.code = t.status and rs.statustype = 'T'
                        left join wm_session wms on wms.sessionid = t.wm_sessionid
                     on t.docid = d.docid
             where d.doctype = :dtid_sale
               and d.realdocdate between :dbeg and :dend
               and d.status = 'g'
               and d.fromobj = :fromid
               and t.tasktypeid = :ttid_select
               and t.taskmethodid is NOT NULL
               and t.status <> '2'
              into :rddate,:docnum,:tid,:tstat,:tstatname,:tmalgo,:tmname,
                   :weight,:capacity,:fio,:toname,:throughname
        do
            suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_TASKGATEAUTO_INFO (
    TASKID_GATEAUTO type of column WM_TASK.taskid
)
returns (
    PLANDATETIME type of column WM_TASK.plandatetime,
    GATENAME type of column SITE.name,
    AUTONAME type of column T_AUTO.name
)
as
begin
    select t.plandatetime, s.name, ta.name
      from wm_task t
           left join site s on s.siteid = t.siteid
           left join t_auto ta on ta.aid = t.infoid
     where t.taskid = :taskid_gateauto
      into :plandatetime, :gatename, :autoname;

    suspend;
end^

SET TERM ; ^

