

SET TERM ^ ;

create procedure WH_WARES_LISTUNITS (
    WARESID type of column GWARES.waresid
)
returns (
    WUID type of column WARESUNIT.waresunitid,
    UID type of column UNIT.unitid,
    UCODE type of column UNIT.shortname,
    UNAME type of column UNIT.fullname,
    FACTOR type of column WARESUNIT.factor,
    WUTYPE type of R_FLAG
)
as
declare variable mwuid type of column WARESUNIT.waresunitid;
declare variable vwuid type of column WARESUNIT.waresunitid;
begin
    select g.mainunitid, g.viewunitid
      from gwares g
     where g.waresid = :waresid
      into :mwuid, :vwuid;

    for
        select wu.waresunitid,wu.factor,
               u.unitid,u.shortname,u.fullname,
               case
                when wu.waresunitid = :vwuid then 'V'
                when wu.waresunitid = :mwuid then 'M'
                else ''
               end
          from waresunit wu
               left join unit u on u.unitid=wu.unitid
         where wu.waresid = :waresid
          into :wuid,:factor,
               :uid,:ucode,:uname,
               :wutype
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TTID_FUNDHANDDO
returns (
    TTID R_ID)
AS
begin
    select k.ttid
      from k_tasktype_by_code('FUNDHANDDO') k
      into :ttid;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_FUNDINCOME_WARESHANDRESERVE (
    DOCID type of column DOCUMENT.docid,
    WARESID type of column GWARES.waresid,
    Q type of R_DOUBLE,
    UID type of column K_USERS.id_user
)
as
declare variable productdate type of r_date;
declare variable whid type of r_date;
declare variable qfree type of r_double;
declare variable TTID_FUNDHANDDO type of column wm_tasktype.tasktypeid;
declare variable wmsid type of column wm_session.sessionid;
declare variable taskid type of column wm_task.taskid;
begin
    select wms.sessionid
      from k_users ku
           left join wm_session wms on wms.objid = ku.id_man
     where ku.id_user = :uid
       and wms.disconnecttime is null
       and wms.connecttime is NOT NULL
      into :wmsid;
    if (:wmsid is NULL) then
        exception exc_k_common '–абоча€ сесси€ пользовател€ не установлена!';

    select fi.productdate, coalesce(fi.qdoc,0.000) - coalesce(fi.qfund, 0.000)
      from WH_RRESERVE_FUNDINCOMEDOCWARES(:docid,:waresid) fi
      into :productdate, :qfree;

    if (:qfree is NULL or :qfree - :q < -0.0001 ) then
        exception exc_wh_wrongamount;

    select d.toobj
      from document d
     where d.docid = :docid
      into :whid;

    execute procedure WH_TTID_FUNDHANDDO
     returning_values :TTID_FUNDHANDDO;

    insert into wm_task ( TASKTYPEID, STATUS, CREATETIME, DOCID)
    values ( :ttid_fundhanddo, '0', current_timestamp, :docid)
    returning taskid
    into :taskid;

    update wm_task t
       set t.status='1',
           t.wm_sessionid=:wmsid,
           t.begintime=current_timestamp,
           t.assigntime = current_timestamp
     where t.taskid = :taskid;

    insert into wm_task_wares ( TASKID, WARESID, SCANQUANT, STATUS, BEGINTIME, ENDTIME, WM_SESSIONID, PLANDATETIME)
    values ( :taskid, :waresid, :q, '2', current_timestamp, current_timestamp, :wmsid, :productdate);

    insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, TASKID)
    values ( :docid, :waresid, :productdate, :q, :whid, :taskid);

    update wm_task t
       set t.status='2',
           t.endtime=current_timestamp
     where t.taskid = :taskid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDINCOME_WARESHANDRESERVE (
    DOCID type of column DOCUMENT.docid,
    WARESID type of column GWARES.waresid,
    Q type of R_DOUBLE,
    UID type of column K_USERS.id_user
)
as
declare variable productdate type of r_date;
declare variable whid type of column OBJECT.objid;
declare variable qfree type of r_double;
declare variable TTID_FUNDHANDDO type of column wm_tasktype.tasktypeid;
declare variable wmsid type of column wm_session.sessionid;
declare variable taskid type of column wm_task.taskid;
begin
    select wms.sessionid
      from k_users ku
           left join wm_session wms on wms.objid = ku.id_man
     where ku.id_user = :uid
       and wms.disconnecttime is null
       and wms.connecttime is NOT NULL
      into :wmsid;
    if (:wmsid is NULL) then
        exception exc_k_common '–абоча€ сесси€ пользовател€ не установлена!';

    select fi.productdate, coalesce(fi.qdoc,0.000) - coalesce(fi.qfund, 0.000)
      from WH_RRESERVE_FUNDINCOMEDOCWARES(:docid,:waresid) fi
      into :productdate, :qfree;

    if (:qfree is NULL or :qfree - :q < -0.0001 ) then
        exception exc_wh_wrongamount;

    select d.toobj
      from document d
     where d.docid = :docid
      into :whid;

    execute procedure WH_TTID_FUNDHANDDO
     returning_values :TTID_FUNDHANDDO;

    insert into wm_task ( TASKTYPEID, STATUS, CREATETIME, DOCID)
    values ( :ttid_fundhanddo, '0', current_timestamp, :docid)
    returning taskid
    into :taskid;

    update wm_task t
       set t.status='1',
           t.wm_sessionid=:wmsid,
           t.begintime=current_timestamp,
           t.assigntime = current_timestamp
     where t.taskid = :taskid;

    insert into wm_task_wares ( TASKID, WARESID, SCANQUANT, STATUS, BEGINTIME, ENDTIME, WM_SESSIONID, PLANDATETIME)
    values ( :taskid, :waresid, :q, '2', current_timestamp, current_timestamp, :wmsid, :productdate);

    insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, TASKID)
    values ( :docid, :waresid, :productdate, :q, :whid, :taskid);

    update wm_task t
       set t.status='2',
           t.endtime=current_timestamp
     where t.taskid = :taskid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_FUNDINCOMEDOCWARES (
    DOCID type of column DOCUMENT.DOCID,
    WARESID type of column GWARES.WARESID = null)
returns (
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    PRODUCTDATE type of R_DATE,
    QDOC type of column CARGO.AMOUNT,
    QFUND type of column WH_RESERVE_CHANGES.AMOUNT,
    VUF type of column WARESUNIT.FACTOR,
    VUC type of column UNIT.SHORTNAME,
    MUF type of column WARESUNIT.FACTOR,
    MUC type of column UNIT.SHORTNAME)
AS
begin
    if (:waresid is NULL) then
    begin
        for
            with wdata as (
                select cast(d.realdocdate as r_date) as productdate, cg.waresid as waresid, cg.amount as qdoc, 0.000 as qfund
                  from document d
                       left join cargo cg on cg.document = d.docid
                 where d.docid = :docid
                   and cg.cargoid is NOT NULL
                 union all
                select rcc.productdate as productdate, rcc.waresid as waresid, 0.000 as qdoc, rcc.amount as qfund
                  from wh_reserve_changes rcc
                 where rcc.docid = :docid
            ),
            wgroup as(
                select productdate, waresid, sum(qdoc) as qdoc, sum(qfund) as qfund
                  from wdata
                group by productdate, waresid
            )
            select wgroup.productdate, wgroup.qdoc, wgroup.qfund,
                   g.waresid, g.code, g.name,
                   vwu.factor, vu.shortname, mwu.factor, mu.shortname
              from wgroup
                   left join gwares g
                        left join waresunit vwu
                             left join unit vu on vu.unitid = vwu.unitid
                          on vwu.waresunitid = g.viewunitid
                        left join waresunit mwu
                             left join unit mu on mu.unitid = mwu.unitid
                          on mwu.waresunitid = g.mainunitid
                     on g.waresid = wgroup.waresid
              into :productdate, :qdoc, :qfund,
                   :wid, :wcode, :wname,
                   :vuf, :vuc, :muf, :muc
        do
            suspend;
    end
    else
    begin
        for
            with wdata as (
                select cast(d.realdocdate as r_date) as productdate, cg.waresid as waresid, cg.amount as qdoc, 0.000 as qfund
                  from document d
                       left join cargo cg on cg.document = d.docid
                 where d.docid = :docid
                   and cg.waresid = :waresid
                 union all
                select rcc.productdate as productdate, rcc.waresid as waresid, 0.000 as qdoc, rcc.amount as qfund
                  from wh_reserve_changes rcc
                 where rcc.docid = :docid
                   and rcc.waresid = :waresid
            ),
            wgroup as(
                select productdate, waresid, sum(qdoc) as qdoc, sum(qfund) as qfund
                  from wdata
                group by productdate, waresid
            )
            select wgroup.productdate, wgroup.qdoc, wgroup.qfund,
                   g.waresid, g.code, g.name,
                   vwu.factor, vu.shortname, mwu.factor, mu.shortname
              from wgroup
                   left join gwares g
                        left join waresunit vwu
                             left join unit vu on vu.unitid = vwu.unitid
                          on vwu.waresunitid = g.viewunitid
                        left join waresunit mwu
                             left join unit mu on mu.unitid = mwu.unitid
                          on mwu.waresunitid = g.mainunitid
                     on g.waresid = wgroup.waresid
              into :productdate, :qdoc, :qfund,
                   :wid, :wcode, :wname,
                   :vuf, :vuc, :muf, :muc
        do
            suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDINCOME_WARESHANDRESERVE (
    DOCID type of column DOCUMENT.docid,
    WARESID type of column GWARES.waresid,
    Q type of R_DOUBLE,
    UID type of column K_USERS.id_user
)
as
declare variable productdate type of r_date;
declare variable whid type of column OBJECT.objid;
declare variable qfree type of r_double;
declare variable TTID_FUNDHANDDO type of column wm_tasktype.tasktypeid;
declare variable wmsid type of column wm_session.sessionid;
declare variable taskid type of column wm_task.taskid;
begin
    select wms.sessionid
      from k_users ku
           left join wm_session wms on wms.objid = ku.id_man
     where ku.id_user = :uid
       and wms.disconnecttime is null
       and wms.connecttime is NOT NULL
      into :wmsid;
    if (:wmsid is NULL) then
        exception exc_k_common '–абоча€ сесси€ пользовател€ не установлена!';

    select fi.productdate, coalesce(fi.qdoc,0.000) - coalesce(fi.qfund, 0.000)
      from WH_RRESERVE_FUNDINCOMEDOCWARES(:docid,:waresid) fi
      into :productdate, :qfree;

    if (:qfree is NULL or :qfree - :q < -0.0001 ) then
        exception exc_wh_wrongamount;

    select d.toobj
      from document d
     where d.docid = :docid
      into :whid;

    execute procedure WH_TTID_FUNDHANDDO
     returning_values :TTID_FUNDHANDDO;

    insert into wm_task ( TASKTYPEID, STATUS, CREATETIME, DOCID)
    values ( :ttid_fundhanddo, '0', current_timestamp, :docid)
    returning taskid
    into :taskid;

    update wm_task t
       set t.status='1',
           t.wm_sessionid=:wmsid,
           t.begintime=current_timestamp,
           t.assigntime = current_timestamp
     where t.taskid = :taskid;

    insert into wm_task_wares ( TASKID, WARESID, SCANQUANT, STATUS, BEGINTIME, ENDTIME, WM_SESSIONID, PLANDATETIME)
    values ( :taskid, :waresid, :q, '2', current_timestamp, current_timestamp, :wmsid, :productdate);

    insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, TASKID)
    values ( :docid, :waresid, :productdate, :q, :whid, :taskid);

    update wm_task t
       set t.status='2',
           t.endtime=current_timestamp
     where t.taskid = :taskid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDINCOME_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
--declare variable objid type of column OBJECT.objid;
begin
/*   select d.toobj
     from document d
    where d.docid = :docid
     into :objid;

   insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
   select :docid, ir.waresid, ir.productdate, ir.amount, :objid
     from imp_reserve ir
    where ir.docid = :docid;*/

   insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
   with w as(
       select d.docid as docid, cg.waresid as waresid, cast(d.realdocdate as r_date) as productdate, cg.amount as amount, d.toobj as whid
         from document d
              left join cargo cg on cg.document = d.docid
        where d.docid = :docid
          and cg.cargoid is NOT NULL
        union
       select rc.docid as docid, rc.waresid as waresid, rc.productdate as productdate, -rc.amount as amount, rc.objid as whid
         from wh_reserve_changes rc
        where rc.docid = :docid
    )
   select w.docid, w.waresid, w.productdate, sum(w.amount), w.whid
     from w
    group by w.docid, w.waresid, w.productdate, w.whid
   having abs(sum(w.amount)) > 0.0001;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDINCOME_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I')
AS
declare variable docstat type of column document.status;
declare variable docbondid type of column document.docid;
declare variable docnum type of column document.number;
begin
    if (not exists(select *
                     from imp_document id
                          left join doctype dt on id.doctype = dt.doctid
                    where id.docid = :docid
                      and dt.code = 'FUNDINCOME')) then
        exception exc_wh_wrongdoctype;

    select id.docbondid, id.number
      from imp_document id
     where id.docid = :docid
      into :docbondid, :docnum;

    if (:docbondid is NOT NULL) then
    begin
        update imp_document id
           set id.docid = :docbondid
         where id.docid = :docid;

        docid = :docbondid;
    end

    select d.status
      from document d
     where d.docid = :docid
      into :docstat;

    if (:actioncode = 'I') then
    begin
        if (:docstat = 'w') then
        begin
            execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid);
            execute procedure WH_IMP_CARGO_CHK(:docid);
    
            execute procedure wh_imp_fundincome_reserve_do(:docid);
    
            update document d
               set d.status = 'e', d.number = :docnum
             where d.docid = :docid;
    
            delete from imp_document id
             where id.docid = :docid;
        end
        else
        begin
            exception exc_wh_wrongdocstat;
        end
    end
    else if (:actioncode = 'D') then
    begin
        if (:docstat = 'e') then
        begin
            execute procedure WH_DOC_RESERVE_LVL1_CANC(:docid);

            update document d
               set d.status = 'w', d.number = :docnum
             where d.docid = :docid;
    
            delete from imp_document id
             where id.docid = :docid;
        end
        else
        begin
            exception exc_wh_wrongdocstat;
        end
    end
    else
    begin
        exception exc_wh_wrongdocstat 'wrong ACTIONCODE';
    end
end^

SET TERM ; ^

