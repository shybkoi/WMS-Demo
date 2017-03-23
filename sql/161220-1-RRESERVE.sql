

SET TERM ^ ;

create or alter procedure WH_RRESERVE_DOC_SUMMARY_DATA(
    DOCID type of column DOCUMENT.docid
)
returns (
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WEXTERNALCODE type of column GWARES.EXTERNALCODE,
    OBJID type of column OBJECT.OBJID,
    OBJNAME type of R_VARCHAR255,
    Q1 type of column WH_RESERVE.AMOUNT,
    Q2 type of column WH_RESERVE.AMOUNTSALE,
    QB type of column WH_RESERVE.AMOUNTBAD,
    PRDATE type of column WH_RESERVE.PRODUCTDATE)
AS
begin
    for
        with res as(
            select rc.waresid, rc.productdate, rc.objid, rc.amount as amount, rc.amountbad as amountbad, 0.000 as amountsale
              from wh_reserve_changes rc
             where rc.docid = :docid
             union all
            select rc.waresid, rc.productdate, rc.objid, 0.000 as amount, 0.000 as amountbad, rc.amount as amountsale
              from wh_reserve_client_changes rc
             where rc.docid = :docid
        )
        select g.waresid, g.code, g.name, g.externalcode,
               r.objid, (select objname from wh_get_objectname(r.objid)),
               r.amount, r.amountsale, r.productdate, r.amountbad
          from res r
               left join gwares g on g.waresid = r.waresid
         where r.amount + r.amountbad > 0.0000001
          into :wid, :wcode, :wname, :wexternalcode,
               :objid, :objname,
               :q1, :q2, :prdate, :qb
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_RRESERVE_DOC_CHANGES (
    ID type of column DOCUMENT.docid,
    OBJID type of column OBJECT.OBJID,
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of column WH_RESERVE_CHANGES.PRODUCTDATE,
    FLAG type of R_FLAG)
returns (
    DT type of column WH_RESERVE_CHANGES.DATETIME,
    AMOUNT type of column WH_RESERVE_CHANGES.AMOUNT,
    AMOUNTBAD type of column WH_RESERVE_CHANGES.AMOUNTBAD,
    DOCNUM type of column DOCUMENT.NUMBER,
    DOCDATE type of column DOCUMENT.REALDOCDATE,
    DTNAME type of column DOCTYPE.NAME,
    FROMNAME type of R_FULLNAME,
    THROUGHNAME type of R_FULLNAME,
    TONAME type of R_FULLNAME,
    DOCSTAT type of column R_STATUS.CODE,
    DOCSTATNAME type of column R_STATUS.NAME,
    TASKID type of column WM_TASK.TASKID,
    TTNAME type of column WM_TASKTYPE.NAME,
    TASKMAN type of R_FULLNAME)
AS
begin
    for
        select rc.datetime, rc.amount, rc.amountbad,
               d.number, d.realdocdate,
               (select objname from wh_get_objectname(d.fromobj)),
               (select objname from wh_get_objectname(d.throughobj)),
               (select objname from wh_get_objectname(d.toobj)),
               rs.code, rs.name, dt.name,
               t.taskid, tt.name, (select objname from wh_get_objectname(s.objid))
          from wh_reserve_changes rc
               left join wm_task t
                    left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                    left join wm_session s on s.sessionid = t.wm_sessionid
                 on t.taskid = rc.taskid
               left join document d
                    left join r_status rs on rs.code = d.status and rs.statustype = 'O'
                    left join doctype dt on dt.doctid = d.doctype
                 on d.docid = rc.docid
         where rc.docid = :id
           and rc.objid = :objid
           and rc.waresid = :waresid
           and rc.productdate = :productdate
          into :dt, :amount, :amountbad,
               :docnum, :docdate, :fromname, :throughname, :toname,
               :docstat, :docstatname, :dtname,
               :taskid, :ttname, :taskman
    do
    begin
        if (:flag is NULL) then
        begin
            suspend;
        end
        else
        begin
            if (:flag = 'B' and abs(:amountbad)>0.0001) then
                suspend;

            if (:flag = 'G' and abs(:amount)>0.0001) then
                suspend;
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_RRESERVE_DOC_CLIENTS (
    ID type of column DOCUMENT.docid,
    OBJID type of column OBJECT.OBJID,
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of column WH_RESERVE.PRODUCTDATE)
returns (
    CLIENTID type of column OBJECT.OBJID,
    CLIENTNAME type of R_FULLNAME,
    AMOUNT type of column WH_RESERVE_CLIENT.AMOUNT)
AS
--declare variable reserveid type of column wh_reserve.id;
begin
    /*select r.id
      from wh_reserve r
     where r.objid = :objid
       and r.productdate = :productdate
       and r.waresid = :waresid
      into :reserveid;*/

--    if (:reserveid is NOT NULL) then
    for
        select rcc.clientid, sum(rcc.amount)
          from wh_reserve_client_changes rcc
         where rcc.docid = :id
           and rcc.objid = :objid
           and rcc.waresid = :waresid
           and rcc.productdate = :productdate
         group by rcc.clientid
          into :clientid, :amount
    do
    begin
        clientname = NULL;
        select w.objname
          from wh_get_objectname(:clientid) w
          into :clientname;

        suspend;
    end

    /*for
        select rc.clientid, rc.amount,
               (select objname from wh_get_objectname(rc.clientid))
          from wh_reserve_client rc
         where rc.reserveid = :reserveid
          into :clientid, :amount, :clientname
    do
    begin
        suspend;
    end*/
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_RRESERVE_DOC_CLIENT_CHANGES (
    ID type of column DOCUMENT.docid,
    OBJID type of column OBJECT.OBJID,
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of column WH_RESERVE_CHANGES.PRODUCTDATE,
    CLIENTID type of column OBJECT.OBJID)
returns (
    DT type of column WH_RESERVE_CHANGES.DATETIME,
    AMOUNT type of column WH_RESERVE_CHANGES.AMOUNT,
    DOCNUM type of column DOCUMENT.NUMBER,
    DOCDATE type of column DOCUMENT.REALDOCDATE,
    DTNAME type of column DOCTYPE.NAME,
    FROMNAME type of R_FULLNAME,
    THROUGHNAME type of R_FULLNAME,
    TONAME type of R_FULLNAME,
    DOCSTAT type of column R_STATUS.CODE,
    DOCSTATNAME type of column R_STATUS.NAME)
AS
begin
    for
        select rc.datetime, rc.amount, --rc.amountbad,
               d.number, d.realdocdate,
               (select objname from wh_get_objectname(d.fromobj)),
               (select objname from wh_get_objectname(d.throughobj)),
               (select objname from wh_get_objectname(d.toobj)),
               rs.code, rs.name, dt.name --,
--               t.taskid, tt.name, (select objname from wh_get_objectname(s.objid))
          from wh_reserve_client_changes rc
/*               left join wm_task t
                    left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                    left join wm_session s on s.sessionid = t.wm_sessionid
                 on t.taskid = rc.taskid*/
               left join document d
                    left join r_status rs on rs.code = d.status and rs.statustype = 'O'
                    left join doctype dt on dt.doctid = d.doctype
                 on d.docid = rc.docid
         where rc.docid = :id
           and rc.objid = :objid
           and rc.waresid = :waresid
           and rc.productdate = :productdate
           and rc.clientid = :clientid
          into :dt, :amount, --:amountbad,
               :docnum, :docdate, :fromname, :throughname, :toname,
               :docstat, :docstatname, :dtname --,
--               :taskid, :ttname, :taskman
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RRESERVE_DOC_SUMMARY_DATA(
    DOCID type of column DOCUMENT.docid
)
returns (
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WEXTERNALCODE type of column GWARES.EXTERNALCODE,
    OBJID type of column OBJECT.OBJID,
    OBJNAME type of R_VARCHAR255,
    Q1 type of column WH_RESERVE.AMOUNT,
    Q2 type of column WH_RESERVE.AMOUNTSALE,
    QB type of column WH_RESERVE.AMOUNTBAD,
    PRDATE type of column WH_RESERVE.PRODUCTDATE)
AS
begin
    for
        with res as(
            select rc.waresid, rc.productdate, rc.objid, rc.amount as amount, rc.amountbad as amountbad, 0.000 as amountsale
              from wh_reserve_changes rc
             where rc.docid = :docid
             union all
            select rc.waresid, rc.productdate, rc.objid, 0.000 as amount, 0.000 as amountbad, rc.amount as amountsale
              from wh_reserve_client_changes rc
             where rc.docid = :docid
        )
        select g.waresid, g.code, g.name, g.externalcode,
               r.objid, (select objname from wh_get_objectname(r.objid)),
               r.amount, r.amountsale, r.productdate, r.amountbad
          from res r
               left join gwares g on g.waresid = r.waresid
          into :wid, :wcode, :wname, :wexternalcode,
               :objid, :objname,
               :q1, :q2, :prdate, :qb
    do
        suspend;
end^

SET TERM ; ^

