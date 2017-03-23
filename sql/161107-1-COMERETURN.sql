

ALTER TABLE WH_OBJ_INFO
ADD CANSELECTMINUS R_FLAG;



COMMENT ON COLUMN WH_OBJ_INFO.CANSELECTMINUS IS
'Возможность отборки в минус, по умолчанию 0 - запрещена';



SET TERM ^ ;

CREATE OR ALTER procedure WH_DC_SELECT_TASKWARES_DO (
    TWID type of R_ID,
    Q type of R_QUANTITY)
AS
declare variable sitepalletid type of r_id;
declare variable objid type of r_id;
declare variable tlquantity type of r_double;
declare variable wid type of r_id;
declare variable wlid type of r_id;
declare variable amount type of r_quantity;
declare variable twq type of r_quantity;
declare variable docstat type of r_status;
declare variable twstatus type of r_status;
declare variable siteid type of r_id;
declare variable ptrashid type of r_id;
declare variable docdate type of r_date;
declare variable docid type of r_id64;
declare variable docbarcode type of r_barcode;
declare variable palletid_select type of column PALLET.palletid;
declare variable taskid type of column WM_TASK.taskid;
declare variable wm_sessionid type of column WM_SESSION.sessionid;
declare variable wlincomeid type of column WARESLOTINCOMES.id;
begin
    select tw.waresid,coalesce(tw.quantity,0.000),tw.siteid,tw.palletid,
           d.status,d.fromobj,d.docdate,tw.status,d.docid,tw.taskid,tw.wm_sessionid
      from wm_task_wares tw
           left join wm_task t
                left join document d on d.docid=t.docid
             on t.taskid=tw.taskid
           left join pallet p
                left join site s
                     left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                  on s.siteid = p.siteid
             on p.palletid = tw.palletid
     where tw.taskwaresid = :twid
      into :wid,:twq,:siteid,:sitepalletid,:docstat,:objid,:docdate,:twstatus,:docid,:taskid,:wm_sessionid;

    if (:twq < 0.00001) then
        execute procedure r_raiseerror('ERROR_ORDERAMOUNT');

    if (:q is NULL) then q = :twq;
    else if (:q - 2*:twq > 0.00001) then
        execute procedure r_raiseerror('FORBIDDENACT_FACTMOREPLAN','2*');

    if (:wid is NULL) then
        execute procedure r_raiseerror('ERROR_TASKWARES');

    if (:docstat='У') then
    begin
        execute procedure wh_doc_barcode(:docid)
         returning_values :docbarcode;
        execute procedure r_raiseerror('DOCUMENT_DELETED',:docbarcode);
    end

    if (:twstatus<>'1') then
        execute procedure r_raiseerror('ERROR_TASKWARESSTATUS');

    update wm_task_wares tw
       set tw.status='2'
     where tw.taskwaresid = :twid;

    if (:sitepalletid is NULL) then
        execute procedure k_waresslot_get_sitepallet(:siteid)
         returning_values :sitepalletid;

    --  Паллет отборки
    select tp.palletid
      from pallet_temp tp
     where tp.taskid = :taskid
      into :palletid_select;

    if (abs(:q) > 0.00001) then
    for
        select wli.wlotid,wli.amount,wli.wlincomeid
          from wareslotitem wli
               left join wareslot wl on wl.wlotid=wli.wlotid
         where wli.palletid = :sitepalletid
           and wl.waresid = :wid
           and wl.objid = :objid
           and wli.amount > 0.0001
         order by wl.productdate ascending
          into :wlid,:amount,:wlincomeid
    do
    if (abs(:q) > 0.00001) then
    begin
        if (:amount - :q > 0.00001) then
        begin
            insert into wm_task_lot(wlotid,palletid,taskwaresid,quantity,chgwli,wlincomeid,wm_sessionid)
            values (:wlid,:sitepalletid,:twid,-:q,'1',:wlincomeid,:wm_sessionid);

            if (:palletid_select is NOT NULL) then
                insert into wm_task_lot(wlotid,palletid,taskwaresid,quantity,chgwli,wlincomeid,wm_sessionid)
                values (:wlid,:palletid_select,:twid,:q,'1',:wlincomeid,:wm_sessionid);
                
            q = 0.000;
        end
        else
        begin
            insert into wm_task_lot(wlotid,palletid,taskwaresid,quantity,chgwli,wlincomeid,wm_sessionid)
            values (:wlid,:sitepalletid,:twid,-:amount,'1',:wlincomeid,:wm_sessionid);

            if (:palletid_select is NOT NULL) then
                insert into wm_task_lot(wlotid,palletid,taskwaresid,quantity,chgwli,wlincomeid,wm_sessionid)
                values (:wlid,:palletid_select,:twid,:amount,'1',:wlincomeid,:wm_sessionid);

            q = :q - :amount;
        end
    end

    if (:q > 0.00001) then
    begin
        if (not exists(select *
                         from wh_obj_info oi
                        where oi.objid = :objid
                          and coalesce(oi.canselectminus, '0') = '1')) then
            exception exc_k_common 'Отборка в минус запрещена!';

        -- Добавляем на поддон с недостачи, то есть на поддон + q штук, с недостачи -q штук
        -- Ну и списываем с поддона, то есть на поддоне ничего, а с недостачи остается -q штук
          select pid
            from k_wh_get_trash(:objid)
            into :ptrashid;
        
          if (:ptrashid is NULL) then
            execute procedure r_raiseerror('TRASH_PALLETNOTFOUND');

          wlid = NULL;
          select wl.wlotid
            from wareslot wl
           where wl.objid = :objid
             and wl.waresid = :wid
             and wl.productdate = :docdate
             and wl.docid is NULL
            into :wlid;

          if (:wlid is NULL) then
            insert into wareslot(waresid,productdate,status,objid)
            values(:wid,:docdate,'1',:objid)
            returning wlotid
            into :wlid;

          insert into wm_task_lot(wlotid,palletid,taskwaresid,quantity,chgwli,wm_sessionid)
          values(:wlid,:ptrashid,:twid,-:q,'1',:wm_sessionid);

          if (:palletid_select is NOT NULL) then
            insert into wm_task_lot(wlotid,palletid,taskwaresid,quantity,chgwli,wm_sessionid)
            values (:wlid,:palletid_select,:twid,:q,'1',:wm_sessionid);
    end

    if (:palletid_select is Null) then
        select -sum(tl.quantity)
          from wm_task_lot tl
         where tl.taskwaresid = :twid
          into :tlquantity;
    else
        select sum(tl.quantity)
          from wm_task_lot tl
         where tl.taskwaresid = :twid
           and tl.palletid = :palletid_select
          into :tlquantity;
        
    update wm_task_wares tw
       set tw.scanquant = :tlquantity,
           tw.status='2',
           tw.endtime=current_timestamp
     where tw.taskwaresid = :twid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RPALLETPRINT_FG_DATA (
    DTBEG type of R_DATETIME,
    DTEND type of R_DATETIME,
    PTCODE type of column PALLET_TYPE.code = NULL)
returns (
    PNUM type of column PALLET_FINISHPRINT.NUMBER,
    DT type of column PALLET_FINISHPRINT.DATETIME,
    PLNAME type of column FG_PRODLINES.NAME,
    PRODUCER type of R_VARCHAR255,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    PRDATE type of column PALLET_FINISHPRINT.PRODUCTDATE,
    MANFIO type of R_VARCHAR255,
    PID type of column PALLET.PALLETID)
AS
begin
    if (:ptcode = 'FP') then
    begin
        for
            select pfp.datetime, pfp.palletid, pfp.number, pfp.productdate,
                   g.code, g.name, pl.name,
                   (select objname from wh_get_objectname(pfp.manid)),
                   (select objname from wh_get_objectname(pfp.producerid))
              from pallet_finishprint pfp
                   left join gwares g on g.waresid = pfp.waresid
                   left join fg_prodlines pl on pl.id_prodline = pfp.prodlineid
             where pfp.datetime between :dtbeg and :dtend
              into :dt, :pid, :pnum, :prdate,
                   :wcode, :wname, :plname,
                   :manfio, :producer
        do
            suspend;
    end
    else if (:ptcode = 'CR') then
    begin
        for
            select p.datetime, p.palletid, p.number,
                   (select objname from wh_get_objectname(p.manid))
              from pallet_comeretprint p
             where p.datetime between :dtbeg and :dtend
              into :dt, :pid, :pnum, :manfio
        do
            suspend;
    end
    else
        exception exc_wh_wrongpallet;

end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_RPALLETPRINT_RC_DATA (
    DTBEG type of R_DATETIME,
    DTEND type of R_DATETIME
)
returns (
    PNUM type of column PALLET_FINISHPRINT.NUMBER,
    DT type of column PALLET_FINISHPRINT.DATETIME,
    MANFIO type of R_VARCHAR255,
    PID type of column PALLET.PALLETID)
AS
begin
    for
        select p.datetime, p.palletid, p.number,
               (select objname from wh_get_objectname(p.manid))
          from pallet_comeretprint p
         where p.datetime between :dtbeg and :dtend
          into :dt, :pid, :pnum, :manfio
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RPALLETPRINT_FG_DATA (
    DTBEG type of R_DATETIME,
    DTEND type of R_DATETIME,
    PTCODE type of column PALLET_TYPE.code = NULL)
returns (
    PNUM type of column PALLET_FINISHPRINT.NUMBER,
    DT type of column PALLET_FINISHPRINT.DATETIME,
    PLNAME type of column FG_PRODLINES.NAME,
    PRODUCER type of R_VARCHAR255,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    PRDATE type of column PALLET_FINISHPRINT.PRODUCTDATE,
    MANFIO type of R_VARCHAR255,
    PID type of column PALLET.PALLETID)
AS
begin
    for
        select pfp.datetime, pfp.palletid, pfp.number, pfp.productdate,
               g.code, g.name, pl.name,
               (select objname from wh_get_objectname(pfp.manid)),
               (select objname from wh_get_objectname(pfp.producerid))
          from pallet_finishprint pfp
               left join gwares g on g.waresid = pfp.waresid
               left join fg_prodlines pl on pl.id_prodline = pfp.prodlineid
         where pfp.datetime between :dtbeg and :dtend
          into :dt, :pid, :pnum, :prdate,
               :wcode, :wname, :plname,
               :manfio, :producer
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_RPALLETPRINT_FG_DATA (
    DTBEG type of R_DATETIME,
    DTEND type of R_DATETIME
)
returns (
    PNUM type of column PALLET_FINISHPRINT.NUMBER,
    DT type of column PALLET_FINISHPRINT.DATETIME,
    PLNAME type of column FG_PRODLINES.NAME,
    PRODUCER type of R_VARCHAR255,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    PRDATE type of column PALLET_FINISHPRINT.PRODUCTDATE,
    MANFIO type of R_VARCHAR255,
    PID type of column PALLET.PALLETID)
AS
begin
    for
        select pfp.datetime, pfp.palletid, pfp.number, pfp.productdate,
               g.code, g.name, pl.name,
               (select objname from wh_get_objectname(pfp.manid)),
               (select objname from wh_get_objectname(pfp.producerid))
          from pallet_finishprint pfp
               left join gwares g on g.waresid = pfp.waresid
               left join fg_prodlines pl on pl.id_prodline = pfp.prodlineid
         where pfp.datetime between :dtbeg and :dtend
          into :dt, :pid, :pnum, :prdate,
               :wcode, :wname, :plname,
               :manfio, :producer
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_RPALLETPRINT_CR_DATA (
    DTBEG type of R_DATETIME,
    DTEND type of R_DATETIME
)
returns (
    PNUM type of column PALLET_FINISHPRINT.NUMBER,
    DT type of column PALLET_FINISHPRINT.DATETIME,
    MANFIO type of R_VARCHAR255,
    PID type of column PALLET.PALLETID)
AS
begin
    for
        select p.datetime, p.palletid, p.number,
               (select objname from wh_get_objectname(p.manid))
          from pallet_comeretprint p
         where p.datetime between :dtbeg and :dtend
          into :dt, :pid, :pnum, :manfio
    do
        suspend;
end^

SET TERM ; ^



DROP PROCEDURE WH_RPALLETPRINT_RC_DATA;

