

SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_P_TASKINFO (
    TASKID R_ID)
returns (
    TID type of R_ID,
    TSTAT type of R_STATUS,
    SITEID type of R_ID,
    SITENAME type of R_NAME,
    PALLETID type of R_ID,
    PNUMBER type of R_BARCODE,
    PALPRODUCTDATE type of R_DATE,
    PALBESTBEFOREDATE type of R_DATE,
    PBARCODE type of R_BARCODE,
    DOCID type of R_ID64,
    DOCNUM type of DOCNUMBER,
    DOCDATE type of R_DATE,
    DOCSTAT type of R_STATUS,
    FROMID type of R_ID,
    FROMNAME type of R_NAME,
    TOID type of R_ID,
    TONAME type of R_NAME,
    WID type of R_ID,
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    VWUID type of R_ID,
    VUFACTOR type of R_DOUBLE,
    VUCODE type of R_CODE,
    MWUID type of R_ID,
    MUFACTOR type of R_DOUBLE,
    MUCODE type of R_CODE,
    QPLAN type of R_DOUBLE,
    QPALLET type of R_DOUBLE,
    CANSELECT type of R_FLAG,
    PLANPRODUCTDATE type of column WM_TASK_WARES.plandatetime
)
AS
declare variable pfeatureid type of r_id;
begin
    select t.taskid,t.status,
           d.docid,d.docdate,d.number,d.status,
           d.fromobj,(select fullname from getobjectname(d.fromobj,NULL)),
           d.toobj,(select fullname from getobjectname(d.toobj,NULL))
      from wm_task t
           left join document d on d.docid=t.docid
     where t.taskid = :taskid
      into :tid,:tstat,
           :docid,:docdate,:docnum,:docstat,
           :fromid, :fromname,
           :toid, :toname;

    select tw.quantity, s.siteid, s.name,
           p.palletid, p.number, p.barcode, p.featureid,
           g.waresid, g.code, g.name,
           vwu.waresunitid, vwu.factor, vu.shortname,
           mwu.waresunitid, mwu.factor, mu.shortname,
           tw.plandatetime
      from wm_task_wares tw
           left join site s on s.siteid = tw.siteid
           left join pallet p
             on p.palletid = tw.palletid
           left join gwares g
                left join waresunit vwu
                     left join unit vu on vu.unitid = vwu.unitid
                  on vwu.waresunitid = g.viewunitid
                left join waresunit mwu
                     left join unit mu on mu.unitid = mwu.unitid
                  on mwu.waresunitid = g.mainunitid
             on g.waresid = tw.waresid
     where tw.taskid = :taskid
       and tw.status <> '2'
      into :qplan, :siteid, :sitename,
           :palletid, :pnumber, :pbarcode, :pfeatureid,
           :wid, :wcode, :wname,
           :vwuid, :vufactor, :vucode,
           :mwuid, :mufactor, :mucode, :planproductdate;

    if (:palletid is NOT NULL) then
    begin
        select sum(wli.amount)
          from wareslotitem wli
         where wli.palletid = :palletid
          into :qpallet;

        select pfp.productdate, pfp.bestbeforedate
          from pallet_finishprint pfp
         where pfp.palletid = :palletid
          into :palproductdate, :palbestbeforedate;
    end

    /*if (:pfeatureid is NOT NULL and
        exists(select *
                 from WH_CLIENT_LISTPALLETFEATURES(:toid) pfc
                where pfc.pfid = :pfeatureid
                  and pfc.pfpriority is NOT NULL and pfc.pfpriority > 0)) then
        canselect = '1';
    else
        canselect = '0';*/

    canselect = '1';

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_P_TASKINFO (
    TASKID R_ID)
returns (
    TID type of R_ID,
    TSTAT type of R_STATUS,
    SITEID type of R_ID,
    SITENAME type of R_NAME,
    PALLETID type of R_ID,
    PNUMBER type of R_BARCODE,
    PALPRODUCTDATE type of R_DATE,
    PALBESTBEFOREDATE type of R_DATE,
    PBARCODE type of R_BARCODE,
    DOCID type of R_ID64,
    DOCNUM type of DOCNUMBER,
    DOCDATE type of R_DATE,
    DOCSTAT type of R_STATUS,
    FROMID type of R_ID,
    FROMNAME type of R_NAME,
    TOID type of R_ID,
    TONAME type of R_NAME,
    WID type of R_ID,
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    VWUID type of R_ID,
    VUFACTOR type of R_DOUBLE,
    VUCODE type of R_CODE,
    MWUID type of R_ID,
    MUFACTOR type of R_DOUBLE,
    MUCODE type of R_CODE,
    QPLAN type of R_DOUBLE,
    QPALLET type of R_DOUBLE,
    CANSELECT type of R_FLAG,
    PLANPRODUCTDATE type of column WM_TASK_WARES.plandatetime
)
AS
declare variable pfeatureid type of r_id;
begin
    select t.taskid,t.status,
           d.docid,d.docdate,d.number,d.status,
           d.fromobj,(select fullname from getobjectname(d.fromobj,NULL)),
           d.toobj,(select fullname from getobjectname(d.toobj,NULL))
      from wm_task t
           left join document d on d.docid=t.docid
     where t.taskid = :taskid
      into :tid,:tstat,
           :docid,:docdate,:docnum,:docstat,
           :fromid, :fromname,
           :toid, :toname;

    select tw.quantity, s.siteid, s.name,
           p.palletid, p.number, p.barcode, p.featureid,
           g.waresid, g.code, g.name,
           vwu.waresunitid, vwu.factor, vu.shortname,
           mwu.waresunitid, mwu.factor, mu.shortname,
           tw.plandatetime
      from wm_task_wares tw
           left join site s on s.siteid = tw.siteid
           left join pallet p
             on p.palletid = tw.palletid
           left join gwares g
                left join waresunit vwu
                     left join unit vu on vu.unitid = vwu.unitid
                  on vwu.waresunitid = g.viewunitid
                left join waresunit mwu
                     left join unit mu on mu.unitid = mwu.unitid
                  on mwu.waresunitid = g.mainunitid
             on g.waresid = tw.waresid
     where tw.taskid = :taskid
       and tw.status <> '2'
      into :qplan, :siteid, :sitename,
           :palletid, :pnumber, :pbarcode, :pfeatureid,
           :wid, :wcode, :wname,
           :vwuid, :vufactor, :vucode,
           :mwuid, :mufactor, :mucode, :planproductdate;

    if (:palletid is NOT NULL) then
    begin
        select sum(wli.amount)
          from wareslotitem wli
         where wli.palletid = :palletid
          into :qpallet;

        select pfp.productdate, pfp.bestbeforedate
          from pallet_finishprint pfp
         where pfp.palletid = :palletid
          into :palproductdate, :palbestbeforedate;
    end

    /*if (:pfeatureid is NOT NULL and
        exists(select *
                 from WH_CLIENT_LISTPALLETFEATURES(:toid) pfc
                where pfc.pfid = :pfeatureid
                  and pfc.pfpriority is NOT NULL and pfc.pfpriority > 0)) then
        canselect = '1';
    else
        canselect = '0';*/

    canselect = '1';

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_SELECTDC_P_PALLETLIST (
    TASKID type of column WM_TASK.taskid
)
returns (
    PNUM type of column PALLET.number,
    SNAME type of column SITE.name
)
as
declare variable whid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable ProductDate type of column WM_TASK_WARES.plandatetime;
declare variable qorder type of column WM_TASK_WARES.quantity;
begin
    select tw.waresid, tw.plandatetime, d.whid, tw.quantity
      from wm_task_wares tw
           left join wm_task t
                left join wh_doc_getobjects(t.docid) d on 1=1
             on t.taskid = tw.taskid
     where tw.taskid = :taskid
       and tw.status <> '2'
      into :waresid, :productdate, :whid, :qorder;

    if (:waresid is NOT NULL) then
        for
            with wl as (
                select wli.palletid as palletid, sum(wli.amount) as wliamount
                  from wareslot wl
                       left join wareslotitem wli on wli.wlotid = wl.wlotid
                 where wl.waresid = :waresid
                   and wl.status = '1'
                   and wl.objid = :whid
                   and wl.productdate = :productdate
                 group by wli.palletid
                having abs(sum(wli.amount) - :qorder) < 0.0001
            )
            select p.number, s.name
              from wl
                   left join pallet p
                        left join pallet_type pt on pt.id=p.ptypeid
                        left join site s on s.siteid = p.siteid
                     on p.palletid = wl.palletid
             where pt.code = 'FP'
              into :pnum, :sname
        do
            suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_P_PALLETLIST (
    TASKID type of column WM_TASK.taskid
)
returns (
    PNUM type of column PALLET.number,
    SNAME type of column SITE.name
)
as
declare variable whid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable ProductDate type of column WM_TASK_WARES.plandatetime;
declare variable qorder type of column WM_TASK_WARES.quantity;
begin
    select tw.waresid, tw.plandatetime, d.whid, tw.quantity
      from wm_task_wares tw
           left join wm_task t
                left join wh_doc_getobjects(t.docid) d on 1=1
             on t.taskid = tw.taskid
     where tw.taskid = :taskid
       and tw.status <> '2'
      into :waresid, :productdate, :whid, :qorder;

    if (:waresid is NOT NULL) then
        for
            with wl as (
                select wli.palletid as palletid, sum(wli.amount) as wliamount
                  from wareslot wl
                       left join wareslotitem wli on wli.wlotid = wl.wlotid
                 where wl.waresid = :waresid
                   and wl.status = '1'
                   and wl.objid = :whid
                   and wl.productdate = :productdate
                 group by wli.palletid
                having abs(sum(wli.amount) - :qorder) < 0.0001
            )
            select p.number, s.name
              from wl
                   left join pallet p
                        left join pallet_type pt on pt.id=p.ptypeid
                        left join site s
                             left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                          on s.siteid = p.siteid
                     on p.palletid = wl.palletid
             where pt.code = 'FP'
               and sp.code <> 'STACK'
              into :pnum, :sname
        do
            suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_SELECTDC_P_HANDPALLETSET (
    TASKID type of column WM_TASK.taskid,
    PALLETID type of column PALLET.palletid
)
as
declare variable taskwaresid type of column WM_TASK_WARES.taskwaresid;
declare variable waresid type of column GWARES.waresid;
declare variable PRODUCTDATE type of column WM_TASK_WARES.plandatetime;
declare variable WHID type of column OBJECT.objid;
declare variable QORDER type of column WM_TASK_WARES.quantity;
declare variable ptid_fp type of column PALLET_TYPE.id;
declare variable qpalletwares type of column WARESLOTITEM.amount;
declare variable qpalletfull type of column WARESLOTITEM.amount;
begin
    select tw.taskwaresid, tw.waresid, tw.plandatetime, d.whid, tw.quantity
      from wm_task_wares tw
           left join wm_task t
                left join wh_doc_getobjects(t.docid) d on 1=1
             on t.taskid = tw.taskid
     where tw.taskid = :taskid
       and tw.status <> '2'
      into :taskwaresid, :waresid, :productdate, :whid, :qorder;

    if (:waresid is NULL) then
        exception exc_wh_wrongtaskwaresstat 'Не найдена активная позиция в задании';

    select p.id
      from wh_paltypeid_finishgood p
      into :ptid_fp;

    if (not exists(select *
                     from pallet p
                          left join pallet_finishprint pfp on pfp.palletid = p.palletid
                    where p.palletid = :palletid
                      and p.status = '1'
                      and p.pallettype = :ptid_fp
                      and pfp.productdate = :productdate
                      and pfp.waresid = :waresid
    )) then
        exception exc_wh_wrongpallet;

    select sum(iif(wl.waresid = :waresid and wl.objid = :whid and wl.productdate = :productdate, wli.amount, 0.000)),
           sum(wli.amount)
      from wareslotitem wli
           left join wareslot wl
             on wl.wlotid = wli.wlotid
     where wli.palletid = :palletid
      into :qpalletwares, :qpalletfull;
    if (:qpalletwares is NULL) then
        qpalletwares = 0.000;
    if (:qpalletfull is NULL) then
        qpalletfull = 0.000;

    if (abs(:qorder - :qpalletwares) > 0.0001) then
    begin
        exception exc_wh_wrongamount 'Доступное количество товара на паллете отличается от заказанного';
    end

    if (abs(:qpalletfull - :qpalletwares) > 0.0001) then
    begin
        exception exc_wh_wrongamount 'На паллете есть не подходящие остатки!';
    end

    update wm_task_wares tw
       set tw.palletid = :palletid
     where tw.taskwaresid = :taskwaresid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_P_HANDPALLETSET (
    TASKID type of column WM_TASK.taskid,
    PALLETID type of column PALLET.palletid
)
as
declare variable taskwaresid type of column WM_TASK_WARES.taskwaresid;
declare variable waresid type of column GWARES.waresid;
declare variable PRODUCTDATE type of column WM_TASK_WARES.plandatetime;
declare variable WHID type of column OBJECT.objid;
declare variable QORDER type of column WM_TASK_WARES.quantity;
declare variable ptid_fp type of column PALLET_TYPE.id;
declare variable qpalletwares type of column WARESLOTITEM.amount;
declare variable qpalletfull type of column WARESLOTITEM.amount;
begin
    select tw.taskwaresid, tw.waresid, tw.plandatetime, d.whid, tw.quantity
      from wm_task_wares tw
           left join wm_task t
                left join wh_doc_getobjects(t.docid) d on 1=1
             on t.taskid = tw.taskid
     where tw.taskid = :taskid
       and tw.status <> '2'
      into :taskwaresid, :waresid, :productdate, :whid, :qorder;

    if (:waresid is NULL) then
        exception exc_wh_wrongtaskwaresstat 'Не найдена активная позиция в задании';

    select p.id
      from wh_paltypeid_finishgood p
      into :ptid_fp;

    if (not exists(select *
                     from pallet p
                          left join pallet_finishprint pfp on pfp.palletid = p.palletid
                    where p.palletid = :palletid
                      and p.status = '1'
                      and p.ptypeid = :ptid_fp
                      and pfp.productdate = :productdate
                      and pfp.waresid = :waresid
    )) then
        exception exc_wh_wrongpallet;

    select sum(iif(wl.waresid = :waresid and wl.objid = :whid and wl.productdate = :productdate, wli.amount, 0.000)),
           sum(wli.amount)
      from wareslotitem wli
           left join wareslot wl
             on wl.wlotid = wli.wlotid
     where wli.palletid = :palletid
      into :qpalletwares, :qpalletfull;
    if (:qpalletwares is NULL) then
        qpalletwares = 0.000;
    if (:qpalletfull is NULL) then
        qpalletfull = 0.000;

    if (abs(:qorder - :qpalletwares) > 0.0001) then
    begin
        exception exc_wh_wrongamount 'Доступное количество товара на паллете отличается от заказанного';
    end

    if (abs(:qpalletfull - :qpalletwares) > 0.0001) then
    begin
        exception exc_wh_wrongamount 'На паллете есть не подходящие остатки!';
    end

    update wm_task_wares tw
       set tw.palletid = :palletid
     where tw.taskwaresid = :taskwaresid;
end^

SET TERM ; ^



COMMENT ON COLUMN WM_TASK.TMPFLAGS IS
'U - Неоходимо добавление единицы транспортировки
E - Пустой результат выполнения (к примеру, отборка в ноль)';



COMMENT ON COLUMN WM_TASK.TMPFLAGS IS
'U - Неоходимо добавление единицы транспортировки
E - Пустой результат выполнения (к примеру, отборка в ноль)
A - автоматическое дейтвие (для отборки - автоматическая погрузка)';



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
begin
    -- Чтобы сгенерить задания на погрузку поддонов в авто машина должна стоять на воротах
    if (not exists(select *
                     from wm_task t
                    where t.taskid = :tid_gateauto
                      and t.status = '1')) then exit;
    
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
        select d.docid,d.status,t.taskid, ts.taskid,ts.status
          from wh_taskbond tb
               left join wm_task t
                    left join document d
                         left join wm_task ts
                           on ts.docid = d.docid
                              and ts.tasktypeid = :ttid_Select
                              and ts.taskmethodid is NOT NULL
                              and coalesce(t.tmpflags,'') not containing 'E' -- Пустое задание на отборку
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
             insert into wm_task(tasktypeid,docid,status)
             values(:ttid_loadpallet,:docid,'0')
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



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADAUTODC_LISTPALLETS (
    TASKID R_ID)
returns (
    DOCID type of R_ID64,
    DNUM type of DOCNUMBER,
    DDATE type of R_DATE,
    DSTAT type of R_STATUS,
    CLIENTNAME type of R_NAME,
    WHNAME type of R_NAME,
    TID type of R_ID,
    TSTAT type of R_STATUS,
    TPRIORITY type of R_NUMBER,
    TNUMBER type of R_SHORTNAME,
    TSNAME type of R_NAME,
    TID_SELECT type of R_ID,
    TNUM_SELECT type of R_NUMBER,
    TUID type of R_ID,
    TUNAME type of R_NAME,
    TUTYPESHORT type of R_SHORTNAME,
    TUSTAT type of R_STATUS,
    TID_LOADAUTO type of R_ID,
    TEND_SELECT type of R_DATETIME)
AS
declare variable ttid_loadauto r_id;
declare variable ttid_loadpallet r_id;
declare variable ttid_select r_id;

declare variable tbtid_CARDOCS r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_loadselect r_id;
begin
  execute procedure wh_ttid_loadauto returning_values :ttid_loadauto;
  execute procedure wh_ttid_loadpallet returning_values :ttid_loadpallet;
  execute procedure wh_ttid_select returning_values :ttid_select;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'CARDOCS'
    into :tbtid_CARDOCS;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'DOCPALLETS'
    into :tbtid_docpallets;

  select tbt.id
    from wh_taskbondtype tbt
   where tbt.code = 'LOADSELECT'
    into :tbtid_loadselect;

  for
    select d.docid,d.number,d.docdate,d.status,
           (select fullname from getobjectname(d.toobj,NULL)),
           (select fullname from getobjectname(d.fromobj,NULL)),
           t.taskid,t.priority
      from wh_taskbond tb
           left join wm_task t
                left join document d on d.docid = t.docid
             on tb.task2id = t.taskid
     where tb.taskbondtid = :tbtid_cardocs
       and tb.task1id = :taskid
       and t.tasktypeid = :ttid_loadauto
     order by t.priority,5,d.docid
      into :docid, :dnum, :ddate, :dstat, :clientname, :whname, :tid_loadauto, :tpriority
  do
  begin
    tid_select = NULL;
/*    tid = NULL;
    tstat = NULL;
    tnumber = NULL;*/


    for
        select iif(ps.palletid is NOT NULL, p.number, (select numpallet from wh_selectdc_getnumpallet(t.taskid))),
               iif(ps.palletid is NOT NULL, sp.name, s.name), t.taskid, t.num, t.endtime,
               t1.status,t1.taskid
          from wm_task t
               left join pallet_select ps
                    left join pallet p
                         left join site sp on sp.siteid = p.siteid
                      on p.palletid = ps.palletid
                 on ps.taskid = t.taskid
               left join site s on s.siteid = t.siteid
               left join wh_taskbond tb
                    left join wm_task t1 on t1.taskid = tb.task1id and t1.tasktypeid = :ttid_loadpallet
                 on tb.task2id = t.taskid and tb.taskbondtid = :tbtid_loadselect
         where t.docid = :docid
           and t.tasktypeid = :ttid_select
           and t.taskmethodid is NOT NULL
           and coalesce(t.tmpflags,'') not containing 'E'
         order by t1.num, t.endtime descending, t.num asc
          into :tnumber,:tsname,:tid_select,:tnum_select,:tend_select,:tstat,:tid
    do
    begin
        tuid = NULL;
        tuname = NULL;
        tutypeshort = NULL;
        select tu.name,tu.tuid,tut.shortname
          from wm_task_transunit ttu
               left join WH_TRANSPORT_UNIT tu
                         left join wh_transport_unit_type tut on tut.tutid = tu.tutid
                    on tu.tuid = ttu.tunitid
         where ttu.taskid = :tid_select
          into :tuname,:tuid,:tutypeshort;
        tustat = NULL;
        if (:tuid is NOT NULL) then 
        begin
          if (exists(select *
                       from wm_task_transunit ttu
                      where ttu.taskid = :tid
                        and ttu.tunitid = :tuid)) then
            tustat = '2';
          else
            tustat = '0';
        end

        suspend;
    end

    if (:tid_select is NULL) then
    begin
        tnumber = NULL;
        tsname = NULL;
        tnum_select = NULL;
        tend_select = NULL;
        tstat = NULL;
        tid = NULL;
        tustat = NULL;
        suspend;
    end

/*    for
        select t.status,t.taskid
          from wh_taskbond tb
               left join wm_task t on t.taskid = tb.task2id
         where tb.task1id = :tid_loadauto
           and tb.taskbondtid = :tbtid_docpallets
           and t.tasktypeid = :ttid_loadpallet
         order by t.num
          into :tstat,:tid
    do
    begin
        tnumber = NULL;
        tsname = NULL;
        tid_select = NULL;

        select iif(ps.palletid is NOT NULL, p.number, (select numpallet from wh_selectdc_getnumpallet(t.taskid))),
               iif(ps.palletid is NOT NULL, sp.name, s.name), t.taskid, t.num, t.endtime
          from wh_taskbond tb
               left join wm_task t
                    left join pallet_select ps
                         left join pallet p
                              left join site sp on sp.siteid = p.siteid
                           on p.palletid = ps.palletid
                      on ps.taskid = t.taskid
                    left join site s on s.siteid = t.siteid
                 on t.taskid = tb.task2id
         where tb.task1id = :tid
           and tb.taskbondtid = :tbtid_loadselect
           and t.tasktypeid = :ttid_select
           and t.taskmethodid is NOT NULL
          into :tnumber,:tsname,:tid_select,:tnum_select,:tend_select;

        tuid = NULL;
        tuname = NULL;
        tutypeshort = NULL;
        select tu.name,tu.tuid,tut.shortname
          from wm_task_transunit ttu
               left join WH_TRANSPORT_UNIT tu
                         left join wh_transport_unit_type tut on tut.tutid = tu.tutid
                    on tu.tuid = ttu.tunitid
         where ttu.taskid = :tid_select
          into :tuname,:tuid,:tutypeshort;
        tustat = NULL;
        if (:tuid is NOT NULL) then 
        begin
          if (exists(select *
                       from wm_task_transunit ttu
                      where ttu.taskid = :tid
                        and ttu.tunitid = :tuid)) then
            tustat = '2';
          else
            tustat = '0';
        end

        suspend;
    end

    if (:tid is NULL) then
        suspend;*/
  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_TASKEND (
    TID_LOADPALLET R_ID)
AS
declare variable tid_loadauto r_id;
declare variable tid_gateauto r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_CARDOCS r_id;
declare variable tpriority r_number;
declare variable palid_select r_id;
declare variable tbtid_loadselect r_id;
declare variable wlotid r_id;
declare variable wlincomeid r_id;
declare variable waresid r_id;
declare variable taskwaresid r_id;
declare variable wmsessionid r_id;
declare variable amount r_double;
declare variable docid r_id64;
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable taskid_select type of column wm_task.taskid;
begin
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'DOCPALLETS'
      into :tbtid_docpallets;

    select t.taskid,t.priority,t.docid
      from wh_taskbond tb
           left join wm_task t on t.taskid = tb.task1id
     where tb.task2id = :tid_loadpallet
       and tb.taskbondtid = :tbtid_docpallets
      into :tid_loadauto,:tpriority,:docid;

    if (:tpriority is NOT NULL) then
    begin
        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'CARDOCS'
          into :tbtid_CARDOCS;
    
        select t.taskid
          from wh_taskbond tb
               left join wm_task t on t.taskid = tb.task1id
         where tb.task2id = :tid_loadauto
           and tb.taskbondtid = :tbtid_cardocs
          into :tid_gateauto;

        if (exists(select *
                     from wh_taskbond tb
                          left join wm_task t
                               left join wh_taskbond tb2
                                    left join wm_task t2 on t2.taskid = tb2.task2id
                                 on tb2.task1id = t.taskid and tb2.taskbondtid = :tbtid_docpallets
                            on t.taskid = tb.task2id
                    where tb.task1id = :tid_gateauto
                      and tb.taskbondtid = :tbtid_cardocs
                      and t.priority is NOT NULL and t.priority < :tpriority
                      and t2.taskid is NOT NULL and t2.status <> '2' )) then
            exception exc_k_common 'Подождите, есть поддоны, которые должны быть загружены раньше вашего!';

    end

    -- Возможно нужно списать остатки
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'LOADSELECT'
      into :tbtid_loadselect;

    select ps.palletid, t.taskid
      from wh_taskbond tb
           left join wm_task t
                left join pallet_select ps on ps.taskid = t.taskid
             on t.taskid = tb.task2id
     where tb.task1id = :tid_loadpallet
       and tb.taskbondtid = :tbtid_loadselect
      into :palid_select, :taskid_select;

    execute procedure WH_SELECT_CLIENTUNFUND(:taskid_select);

    if (:palid_select is NOT NULL) then
    begin
        select t.wm_sessionid
          from wm_task t
         where t.taskid = :tid_loadpallet
          into :wmsessionid;

        for
            select wli.wlotid,wli.wlincomeid,sum(wli.amount)
              from wareslotitem wli
             where wli.palletid = :palid_select
             group by wli.wlotid, wli.wlincomeid
             order by wli.wlotid, wli.wlincomeid nulls last
              into :wlotid, :wlincomeid, :amount
        do
        begin
            waresid = NULL;
            select wl.waresid
              from wareslot wl
             where wl.wlotid = :wlotid
              into :waresid;

            taskwaresid = NULL;
            select tw.taskwaresid
              from wm_task_wares tw
             where tw.taskid = :tid_loadpallet
               and tw.waresid = :waresid
              into :taskwaresid;
            if (:taskwaresid is NULL) then
                insert into wm_task_wares(taskid, waresid, status, wm_sessionid, begintime)
                values(:tid_loadpallet, :waresid, '1', :wmsessionid, current_timestamp)
                returning taskwaresid
                into :taskwaresid;

            insert into wm_task_lot(taskwaresid, wlotid, palletid, wlincomeid,  quantity, chgwli)
            values(:taskwaresid, :wlotid, :palid_select, :wlincomeid, -:amount, '1');

            update wm_task_wares tw
               set tw.status = '2',
                   tw.endtime = current_timestamp,
                   tw.quantity = coalesce(tw.quantity,0.000) + :amount
              where tw.taskwaresid = :taskwaresid;
        end
    end

    -- Закрываем само задание на погрузку паллета в автомобиль
    UPDATE wm_task t
       set t.status = '2',t.endtime = current_timestamp
     where t.taskid = :tid_loadpallet;

    -- Закрыть задание на погрузку документа в машину
    if (not exists(select *
                     from wh_taskbond tb
                          left join wm_task t on t.taskid = tb.task2id
                    where tb.task1id = :tid_loadauto
                      and tb.taskbondtid = :tbtid_docpallets
                      and coalesce(t.status,'0') <> '2')) then
    begin
        execute procedure wh_ttid_select
         returning_values :ttid_select;

        if (not exists(select *
                         from wm_task t
                        where t.docid = :docid
                          and t.taskmethodid is NOT NULL
                          and coalesce(t.tmpflags,'') not containing 'E'
                          and t.tasktypeid = :ttid_select
                          and coalesce(t.status,'0') <> '2')) then
        UPDATE wm_task t
           set t.status = '2',t.endtime = current_timestamp
         where t.taskid = :tid_loadauto;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_SELECT_TSTCHG (
    TASKID type of R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable ttcode type of r_code;
declare variable ttid type of r_id;
declare variable docid type of r_id64;
declare variable wmsid type of r_id;
declare variable tid_loadpallet type of r_id;
declare variable tid_gateauto type of r_id;
declare variable tflags type of wh_flags;
begin
    select tt.code,tt.tasktypeid,t.docid,t.tmpflags,t.wm_sessionid
      from wm_task t
           left join wm_tasktype tt on tt.tasktypeid=t.tasktypeid
     where t.taskid = :taskid
      into :ttcode,:ttid,:docid,:tflags,:wmsid;

    if (:ttcode <> 'SELECT') then
        exception exc_k_wrongtasktype;

    if (:newstat = '2') then
    begin
        if (not exists(select *
                         from wm_task t
                        where t.docid = :docid
                          and t.tasktypeid = :ttid
                          and t.taskmethodid is NOT NULL
                          and t.status <> '2')) then
            update document d
               set d.status = '2'
             where d.docid = :docid;

        select t.tid_gateauto
          from WH_LOADAUTODC_GETTASKBYDOC(:docid) t
          into :tid_gateauto;
        if (:tid_gateauto is NOT NULL) then
            execute procedure wh_loadpalletdc_createtaskes(:tid_gateauto);

        if ((:tflags is NOT NULL and :tflags containing 'A')
/*            or
            not exists(select *
                         from wm_task_wares tw
                              left join wm_task_lot tl on tl.taskwaresid = tw.taskwaresid
                        where tw.taskid = :taskid
                          and tl.palletid is NOT NULL)*/
        ) then
        begin
            select tb.task1id
              from wh_taskbond tb
                   left join wh_taskbondtype tbt on tbt.id = tb.taskbondtid
                   left join wm_task t on t.taskid = tb.task1id
             where tb.task2id = :taskid
               and tbt.code = 'LOADSELECT'
               and coalesce(t.status,'0') <> '2'
              into :tid_loadpallet;

            if (:tid_loadpallet is NOT NULL) then
            begin
                update wm_task t
                   set t.wm_sessionid = null, t.status = '0'
                 where t.taskid = :tid_loadpallet
                   and coalesce(t.wm_sessionid,0) <> :wmsid;
                execute procedure K_SESSION_JOIN_TASK(:tid_loadpallet, :wmsid);
                execute procedure wh_loadpalletdc_taskend(:tid_loadpallet);
            end
        end
    end
end^

SET TERM ; ^

CREATE UNIQUE INDEX WM_TASKTYPE_IDX_CODE
ON WM_TASKTYPE (CODE);



SET TERM ^ ;

create or alter procedure WH_LOADPALLETDC_SELECT_CHKLOAD (
    TASKID_SELECT type of column WM_TASK.taskid
)
AS
declare variable docid type of column DOCUMENT.DOCID;
declare variable docnum type of column DOCUMENT.NUMBER;
declare variable ttid_loadauto type of column WM_TASKTYPE.tasktypeid;
declare variable taskid_loadauto type of column WM_TASK.taskid;
declare variable taskpriority_loadauto type of column WM_TASK.priority;
declare variable taskid_gateauto type of column WM_TASK.taskid;
declare variable taskstat_gateauto type of column WM_TASK.status;
declare variable tbtid_CARDOCS type of column wh_taskbondtype.id;
begin
    select t.docid
      from wm_task t
     where t.taskid = :taskid_select
      into :docid;

    execute procedure wh_ttid_loadauto
     returning_values :ttid_loadauto;

    select t.taskid, t.priority
      from wm_task t
     where t.docid = :docid
       and t.tasktypeid = :ttid_loadauto
      into :taskid_loadauto, :taskpriority_loadauto;

    if (:taskid_loadauto is NULL) then
        exception exc_wh_tasknotfound 'У документа не найдено задание на погрузку';

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_CARDOCS;

    select t.taskid, t.status
      from wh_taskbond tb
           left join wm_task t on t.taskid = tb.task1id
     where tb.task2id = :taskid_loadauto
       and tb.taskbondtid = :tbtid_cardocs
      into :taskid_gateauto, :taskstat_gateauto;

    if (:taskid_gateauto is NULL) then
        exception exc_wh_tasknotfound 'Погрузка авто не найдена';

    if (:taskstat_gateauto <> '1') then
        exception exc_wh_tasknotfound 'Погрузка авто должна выполняться';

    select d.number
      from wh_taskbond tb
           left join wm_task t
                left join document d on d.docid = t.docid
             on t.taskid = tb.task2id
     where tb.task1id = :taskid_gateauto
       and tb.taskbondtid = :tbtid_cardocs
       and t.priority < :taskpriority_loadauto
       and t.status <> '2'
      into :docnum;

    if (:docnum is NOT NULL) then
        exception exc_wh_wrongdocstat 'Имеются документы с более высоким приоритетом погрузки: '||:docnum;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_SELECT_CHKLOAD (
    TASKID_SELECT type of column WM_TASK.taskid,
    AUTOID type of column T_AUTO.aid
)
AS
declare variable docid type of column DOCUMENT.DOCID;
declare variable docnum type of column DOCUMENT.NUMBER;
declare variable ttid_loadauto type of column WM_TASKTYPE.tasktypeid;
declare variable taskid_loadauto type of column WM_TASK.taskid;
declare variable taskpriority_loadauto type of column WM_TASK.priority;
declare variable taskid_gateauto type of column WM_TASK.taskid;
declare variable taskstat_gateauto type of column WM_TASK.status;
declare variable tbtid_CARDOCS type of column wh_taskbondtype.id;
declare variable taskautoid type of column WM_TASK.infoid;
begin
    select t.docid
      from wm_task t
     where t.taskid = :taskid_select
      into :docid;

    execute procedure wh_ttid_loadauto
     returning_values :ttid_loadauto;

    select t.taskid, t.priority
      from wm_task t
     where t.docid = :docid
       and t.tasktypeid = :ttid_loadauto
      into :taskid_loadauto, :taskpriority_loadauto;

    if (:taskid_loadauto is NULL) then
        exception exc_wh_tasknotfound 'У документа не найдено задание на погрузку';

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_CARDOCS;

    select t.taskid, t.status, t.infoid
      from wh_taskbond tb
           left join wm_task t on t.taskid = tb.task1id
     where tb.task2id = :taskid_loadauto
       and tb.taskbondtid = :tbtid_cardocs
      into :taskid_gateauto, :taskstat_gateauto, :taskautoid;

    if (:taskid_gateauto is NULL) then
        exception exc_wh_tasknotfound 'Погрузка авто не найдена';

    if (:taskstat_gateauto <> '1') then
        exception exc_wh_tasknotfound 'Погрузка авто должна выполняться';

    if (:taskautoid is NULL or :autoid is NULL or :autoid <> :taskautoid ) then
        exception exc_wh_wrongbarcode 'Не верный ШК автомобиля';

    select d.number
      from wh_taskbond tb
           left join wm_task t
                left join document d on d.docid = t.docid
             on t.taskid = tb.task2id
     where tb.task1id = :taskid_gateauto
       and tb.taskbondtid = :tbtid_cardocs
       and t.priority < :taskpriority_loadauto
       and t.status <> '2'
      into :docnum;

    if (:docnum is NOT NULL) then
        exception exc_wh_wrongdocstat 'Имеются документы с более высоким приоритетом погрузки: '||:docnum;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_SELECT_CHKLOAD (
    TASKID_SELECT type of column WM_TASK.taskid,
    AUTOID type of column T_AUTO.aid
)
AS
declare variable docid type of column DOCUMENT.DOCID;
declare variable docnum type of column DOCUMENT.NUMBER;
declare variable ttid_loadauto type of column WM_TASKTYPE.tasktypeid;
declare variable taskid_loadauto type of column WM_TASK.taskid;
declare variable taskpriority_loadauto type of column WM_TASK.priority;
declare variable taskid_gateauto type of column WM_TASK.taskid;
declare variable taskstat_gateauto type of column WM_TASK.status;
declare variable tbtid_CARDOCS type of column wh_taskbondtype.id;
declare variable taskautoid type of column WM_TASK.infoid;
begin
    select t.docid
      from wm_task t
     where t.taskid = :taskid_select
      into :docid;

    execute procedure wh_ttid_loadauto
     returning_values :ttid_loadauto;

    select t.taskid, t.priority
      from wm_task t
     where t.docid = :docid
       and t.tasktypeid = :ttid_loadauto
      into :taskid_loadauto, :taskpriority_loadauto;

    if (:taskid_loadauto is NULL) then
        exception exc_wh_tasknotfound 'У документа не найдено задание на погрузку';

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_CARDOCS;

    select t.taskid, t.status, t.infoid
      from wh_taskbond tb
           left join wm_task t on t.taskid = tb.task1id
     where tb.task2id = :taskid_loadauto
       and tb.taskbondtid = :tbtid_cardocs
      into :taskid_gateauto, :taskstat_gateauto, :taskautoid;

    if (:taskid_gateauto is NULL) then
        exception exc_wh_tasknotfound 'Погрузка авто не найдена';

    if (:taskstat_gateauto <> '1') then
        exception exc_wh_tasknotfound 'Погрузка авто должна выполняться';

    if (:taskautoid is NULL or :autoid is NULL or :autoid <> :taskautoid ) then
        exception exc_wh_wrongbarcode 'Не верный автомобиль';

    select d.number
      from wh_taskbond tb
           left join wm_task t
                left join document d on d.docid = t.docid
             on t.taskid = tb.task2id
     where tb.task1id = :taskid_gateauto
       and tb.taskbondtid = :tbtid_cardocs
       and t.priority < :taskpriority_loadauto
       and t.status <> '2'
      into :docnum;

    if (:docnum is NOT NULL) then
        exception exc_wh_wrongdocstat 'Имеются документы с более высоким приоритетом погрузки: '||:docnum;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_SELECT_CHKLOAD (
    TASKID_SELECT type of column WM_TASK.taskid,
    AUTOID type of column T_AUTO.aid
)
RETURNS(
    GATEID type of column SITE.siteid
)
AS
declare variable docid type of column DOCUMENT.DOCID;
declare variable docnum type of column DOCUMENT.NUMBER;
declare variable ttid_loadauto type of column WM_TASKTYPE.tasktypeid;
declare variable taskid_loadauto type of column WM_TASK.taskid;
declare variable taskpriority_loadauto type of column WM_TASK.priority;
declare variable taskid_gateauto type of column WM_TASK.taskid;
declare variable taskstat_gateauto type of column WM_TASK.status;
declare variable tbtid_CARDOCS type of column wh_taskbondtype.id;
declare variable taskautoid type of column WM_TASK.infoid;
begin
    select t.docid
      from wm_task t
     where t.taskid = :taskid_select
      into :docid;

    execute procedure wh_ttid_loadauto
     returning_values :ttid_loadauto;

    select t.taskid, t.priority
      from wm_task t
     where t.docid = :docid
       and t.tasktypeid = :ttid_loadauto
      into :taskid_loadauto, :taskpriority_loadauto;

    if (:taskid_loadauto is NULL) then
        exception exc_wh_tasknotfound 'У документа не найдено задание на погрузку';

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_CARDOCS;

    select t.taskid, t.status, t.infoid, t.siteid
      from wh_taskbond tb
           left join wm_task t on t.taskid = tb.task1id
     where tb.task2id = :taskid_loadauto
       and tb.taskbondtid = :tbtid_cardocs
      into :taskid_gateauto, :taskstat_gateauto, :taskautoid, :gateid;

    if (:taskid_gateauto is NULL) then
        exception exc_wh_tasknotfound 'Погрузка авто не найдена';

    if (:taskstat_gateauto <> '1') then
        exception exc_wh_tasknotfound 'Погрузка авто должна выполняться';

    if (:taskautoid is NULL or :autoid is NULL or :autoid <> :taskautoid ) then
        exception exc_wh_wrongbarcode 'Не верный автомобиль';

    select d.number
      from wh_taskbond tb
           left join wm_task t
                left join document d on d.docid = t.docid
             on t.taskid = tb.task2id
     where tb.task1id = :taskid_gateauto
       and tb.taskbondtid = :tbtid_cardocs
       and t.priority < :taskpriority_loadauto
       and t.status <> '2'
      into :docnum;

    if (:docnum is NOT NULL) then
        exception exc_wh_wrongdocstat 'Имеются документы с более высоким приоритетом погрузки: '||:docnum;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_DC_SELECT_SETTASKSITE (
    TASKID type of R_ID,
    BARCODE type of R_BARCODE)
AS
declare variable availablesiteid r_id;
declare variable flag type of r_flag;
declare variable sitestatus type of r_status;
declare variable siteid type of r_id;
declare variable stellagid type of r_id;
declare variable spcode type of r_code;
declare variable palletid_select type of r_id;
declare variable autoid type of r_id;
declare variable autostat type of r_status;
BEGIN

    select s.siteid, s.status, sp.code
      from site s
           left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
     where s.barcode = :barcode
       and sp.code in ('B','R','E','GATE','S')
      into :siteid,:sitestatus,:spcode;
    if (:siteid is NULL) then
    begin
        select t.aid, t.status
          from t_auto t
         where t.barcode = :barcode
          into :autoid, :autostat;

        if (:autoid is NOT NULL) then
        begin
            if (:autostat = '0') then
                exception exc_k_wrongsite 'Не активный транспорт!';
            else
            begin
                execute procedure WH_LOADPALLETDC_SELECT_CHKLOAD(:taskid, :autoid)
                 returning_values :siteid;

                /*select t.siteid, s.status
                  from wh_dc_select_tasklistsite(:taskid) t
                       left join wh_taskinfotype tit on tit.id = t.infotypeid
                       left join site s on s.siteid = t.siteid
                 where t.infoid = :autoid
                   and tit.code = 'AUTO'
                  into :siteid, :sitestatus;*/

                if (:siteid is NULL) then
                    exception exc_wh_wrongbarcode;
                else
                    flag = '1';
            end
        end
        else
        begin
            exception exc_wh_wrongbarcode;
        end
    end

    if (:sitestatus='0') then
        exception exc_k_wrongsite 'Не активное МП!';

    if (:flag is NULL or :flag = '0') then
    begin
        if (:spcode='E') then
        begin
            flag = '1';
        end
        else if (:spcode = 'S') then
        begin
            flag = '1';
            stellagid = NULL;
            select sid
              from k_site_parent(:siteid,(select sp.sitespeciesid from sitespecies sp where sp.code = 'L'))
              into :stellagid;
    
            if (:stellagid is NULL) then
                exception exc_k_wrongsite 'У МО нет стеллажа!';
            else
                siteid = :stellagid;
        end
        else
        begin
            flag = '0';
            for
                select k.siteid
                  from wh_dc_select_tasklistsite(:taskid) k
                  into :availablesiteid
            do
            if (:availablesiteid=:siteid) then
            begin
                flag = '1';
                break;
            end
        end
    end

    if (:flag='1' or :availablesiteid is NULL ) then
    begin
        -- Если МП в допустимых или это первый поддон
      update wm_task t
         set t.siteid = :siteid
       where t.taskid = :taskid;

      select ps.palletid
        from pallet_select ps
       where ps.taskid = :taskid
        into :palletid_select;
      if (:palletid_select is NOT NULL) then
      begin
        insert into wm_task_pallet(taskid, palletid, status, siteid)
        values(:taskid, :palletid_select, '2', :siteid);

        update pallet p
           set p.siteid = :siteid
         where p.palletid = :palletid_select;
      end
    end
    else
       exception exc_k_wrongsite 'МП должно быть в списке!';

    if (:autoid is NOT NULL) then
        update wm_task t
           set t.tmpflags = coalesce(t.tmpflags,'')||'A'
         where t.taskid = :taskid;
END^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_P_EMPTY (
    TASKID R_ID)
AS
declare variable taskwaresid r_id;
declare variable siteid r_id;
begin
    for
        select tw.taskwaresid, tw.siteid
          from wm_task_wares tw
         where tw.taskid = :taskid
           and tw.status <> '2'
          into :taskwaresid, :siteid
    do
    begin
        update wm_task_wares tw
           set tw.status = '2', tw.siteid = NULL, tw.palletid = NULL
         where tw.taskwaresid = :taskwaresid;

        if (:siteid is NOT NULL) then
            update site_stack ss
               set ss.palblkcnt = coalesce(ss.palblkcnt,1) - 1
             where ss.siteid = :siteid;
    end

    update wm_task t
       set t.status = '5'
     where t.taskid = :taskid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_TASKEND (
    TASKID type of column wm_task.taskid
)
returns (
    NEXTSTEP R_FLAG)
AS
declare variable palletid_select type of column PALLET.palletid;
declare variable palletid_income type of column PALLET.palletid;
declare variable paltypeid_select type of column PALLET_TYPE.id;
declare variable paltypeid_temp type of column PALLET_TYPE.id;
declare variable paltypeid type of column PALLET_TYPE.id;
declare variable palnum type of column PALLET.number;
declare variable tid_loadpal type of column WM_TASK.taskid;
declare variable tid_loaddoc type of column WM_TASK.taskid;
declare variable pbarcode type of column PALLET.number;
declare variable pnumber type of column PALLET.number;
declare variable talgo type of column wm_taskmethod.methodid;
declare variable tsiteid type of column SITE.siteid;
declare variable docid type of column DOCUMENT.docid;
declare variable tmpflags type of column WM_TASK.tmpflags;
declare variable ttid_loaddoc type of column wm_tasktype.tasktypeid;
begin
    if (not exists(select *
                     from wm_task_wares tw
                    where tw.taskid = :taskid
                      and coalesce(tw.scanquant,0.000) > 0.0001)) then
    begin
        NEXTSTEP = 'E';

        select t.docid, coalesce(t.tmpflags,'')||'E'
          from wm_task t
         where t.taskid = :taskid
          into :docid, :tmpflags;

        execute procedure wh_ttid_loadauto
         returning_values :ttid_loaddoc;

        select t.taskid
          from wm_task t
         where t.docid = :docid
           and t.tasktypeid = :ttid_loaddoc
          into :tid_loaddoc;

        if (:tid_loaddoc is NOT NULL) then
        begin
            for
                select tb.task1id
                  from wh_taskbond tb
                       left join wh_taskbondtype tbt on tbt.id = tb.taskbondtid
                 where tb.task2id = :taskid
                  into :tid_loadpal
            do
            begin
                delete from wh_taskbond tb
                 where tb.task1id = :tid_loadpal and tb.task2id = :taskid;
    
                delete from wh_taskbond tb
                 where tb.task1id = :tid_loaddoc and tb.task2id = :tid_loadpal;

                delete from wm_task t where t.taskid = :tid_loadpal;
            end
        end
--            execute procedure K_SESSION_JOIN_TASK(:tid_loadpal, :wmsesid);
--            execute procedure wh_loadpalletdc_taskend(:tid_loadpal);
    end
    else
    begin
        select pt.palletid
          from pallet_temp pt
         where pt.taskid = :taskid
          into :palletid_select;
        
        select pts.id
          from wh_paltypeid_temp pts
          into :paltypeid_temp;
        
        select pts.id
          from wh_paltypeid_select pts
          into :paltypeid_select;
        
        select p.ptypeid
          from pallet p
         where p.palletid = :palletid_select
          into :paltypeid;
        
        if (:paltypeid = :paltypeid_temp) then
        begin
           update pallet p
              set p.ptypeid = :paltypeid_select
            where p.palletid = :palletid_select;
        
        
           update or insert into pallet_select(palletid, taskid)
           values(:palletid_select, :taskid)
           matching(palletid);
        
           if (exists(select *
                        from wm_task t
                             left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                       where t.taskid = :taskid
                         and tm.algorithm = 'P')) then
           begin
               select distinct p.barcode, p.number, p.palletid
                 from wm_task_wares tw
                      left join pallet p on p.palletid = tw.palletid
                where tw.taskid = :taskid
                 into :pbarcode, :pnumber, :palletid_income;

               update pallet p
                  set p.barcode = :pbarcode, p.number = :pnumber
                where p.palletid = :palletid_select;

               update pallet p
                  set p.status = '2'
                where p.palletid = :palletid_income;

               NEXTSTEP = 'M';
           end
           else
               NEXTSTEP = 'P';
        end
        else if (:paltypeid = :paltypeid_select) then
        begin
            
            select tm.algorithm, t.siteid
              from wm_task t
                   left join wm_taskmethod tm on tm.methodid = t.taskmethodid
             where t.taskid = :taskid
              into :talgo, :tsiteid;

           if (:talgo is NOT NULL and :talgo='P') then
           begin
               if (:tsiteid is NOT NULL) then
                   NEXTSTEP = 'E';
               else
                   NEXTSTEP = 'M';
           end
           else
           begin
               select case
                        when ps.printdatetime is NULL then 'P'
                        when ps.printdatetime is NOT NULL and ps.stickdatetime is NULL then 'S'
                        else ''
                      end
                 from pallet_select ps
                where ps.palletid = :palletid_select
                 into :nextstep;
    
               if (:nextstep = '') then
               begin
                if (exists(select *
                            from wm_task_pallet tp
                           where tp.taskid = :taskid
                             and tp.palletid = :palletid_select)) then
                    nextstep = 'E';
                 else
                    nextstep = 'M';
               end
           end
        end
        else
        begin
            select p.number
              from pallet p
             where p.palletid = :palletid_select
              into :palnum;
            execute procedure r_raiseerror('PALLET_ERRORTYPE',:palnum);
        end
    end

    if (:nextstep='E') then
        update wm_task t
           set t.status = '2', t.tmpflags = coalesce(:tmpflags, t.tmpflags)
         where t.taskid = :taskid;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_TASKEND (
    TASKID type of column wm_task.taskid
)
returns (
    NEXTSTEP R_FLAG)
AS
declare variable palletid_select type of column PALLET.palletid;
declare variable palletid_income type of column PALLET.palletid;
declare variable paltypeid_select type of column PALLET_TYPE.id;
declare variable paltypeid_temp type of column PALLET_TYPE.id;
declare variable paltypeid type of column PALLET_TYPE.id;
declare variable palnum type of column PALLET.number;
declare variable tid_loadpal type of column WM_TASK.taskid;
declare variable tid_loaddoc type of column WM_TASK.taskid;
declare variable pbarcode type of column PALLET.number;
declare variable pnumber type of column PALLET.number;
declare variable talgo type of column wm_taskmethod.methodid;
declare variable tsiteid type of column SITE.siteid;
declare variable docid type of column DOCUMENT.docid;
declare variable tmpflags type of column WM_TASK.tmpflags;
declare variable ttid_loaddoc type of column wm_tasktype.tasktypeid;
begin
    if (not exists(select *
                     from wm_task_wares tw
                    where tw.taskid = :taskid
                      and coalesce(tw.scanquant,0.000) > 0.0001)) then
    begin
        NEXTSTEP = 'E';

        select t.docid, coalesce(t.tmpflags,'')||'E'
          from wm_task t
         where t.taskid = :taskid
          into :docid, :tmpflags;

        execute procedure wh_ttid_loadauto
         returning_values :ttid_loaddoc;

        select t.taskid
          from wm_task t
         where t.docid = :docid
           and t.tasktypeid = :ttid_loaddoc
          into :tid_loaddoc;

        if (:tid_loaddoc is NOT NULL) then
        begin
            for
                select tb.task1id
                  from wh_taskbond tb
                       left join wh_taskbondtype tbt on tbt.id = tb.taskbondtid
                 where tb.task2id = :taskid
                   and tbt.code = 'LOADSELECT'
                  into :tid_loadpal
            do
            begin
                delete from wh_taskbond tb
                 where tb.task1id = :tid_loadpal and tb.task2id = :taskid;
    
                delete from wh_taskbond tb
                 where tb.task1id = :tid_loaddoc and tb.task2id = :tid_loadpal;

                delete from wm_task t where t.taskid = :tid_loadpal;
            end
        end
--            execute procedure K_SESSION_JOIN_TASK(:tid_loadpal, :wmsesid);
--            execute procedure wh_loadpalletdc_taskend(:tid_loadpal);
    end
    else
    begin
        select pt.palletid
          from pallet_temp pt
         where pt.taskid = :taskid
          into :palletid_select;
        
        select pts.id
          from wh_paltypeid_temp pts
          into :paltypeid_temp;
        
        select pts.id
          from wh_paltypeid_select pts
          into :paltypeid_select;
        
        select p.ptypeid
          from pallet p
         where p.palletid = :palletid_select
          into :paltypeid;
        
        if (:paltypeid = :paltypeid_temp) then
        begin
           update pallet p
              set p.ptypeid = :paltypeid_select
            where p.palletid = :palletid_select;
        
        
           update or insert into pallet_select(palletid, taskid)
           values(:palletid_select, :taskid)
           matching(palletid);
        
           if (exists(select *
                        from wm_task t
                             left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                       where t.taskid = :taskid
                         and tm.algorithm = 'P')) then
           begin
               select distinct p.barcode, p.number, p.palletid
                 from wm_task_wares tw
                      left join pallet p on p.palletid = tw.palletid
                where tw.taskid = :taskid
                 into :pbarcode, :pnumber, :palletid_income;

               update pallet p
                  set p.barcode = :pbarcode, p.number = :pnumber
                where p.palletid = :palletid_select;

               update pallet p
                  set p.status = '2'
                where p.palletid = :palletid_income;

               NEXTSTEP = 'M';
           end
           else
               NEXTSTEP = 'P';
        end
        else if (:paltypeid = :paltypeid_select) then
        begin
            
            select tm.algorithm, t.siteid
              from wm_task t
                   left join wm_taskmethod tm on tm.methodid = t.taskmethodid
             where t.taskid = :taskid
              into :talgo, :tsiteid;

           if (:talgo is NOT NULL and :talgo='P') then
           begin
               if (:tsiteid is NOT NULL) then
                   NEXTSTEP = 'E';
               else
                   NEXTSTEP = 'M';
           end
           else
           begin
               select case
                        when ps.printdatetime is NULL then 'P'
                        when ps.printdatetime is NOT NULL and ps.stickdatetime is NULL then 'S'
                        else ''
                      end
                 from pallet_select ps
                where ps.palletid = :palletid_select
                 into :nextstep;
    
               if (:nextstep = '') then
               begin
                if (exists(select *
                            from wm_task_pallet tp
                           where tp.taskid = :taskid
                             and tp.palletid = :palletid_select)) then
                    nextstep = 'E';
                 else
                    nextstep = 'M';
               end
           end
        end
        else
        begin
            select p.number
              from pallet p
             where p.palletid = :palletid_select
              into :palnum;
            execute procedure r_raiseerror('PALLET_ERRORTYPE',:palnum);
        end
    end

    if (:nextstep='E') then
        update wm_task t
           set t.status = '2', t.tmpflags = coalesce(:tmpflags, t.tmpflags)
         where t.taskid = :taskid;

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
begin
    -- Чтобы сгенерить задания на погрузку поддонов в авто машина должна стоять на воротах
    if (not exists(select *
                     from wm_task t
                    where t.taskid = :tid_gateauto
                      and t.status = '1')) then exit;
    
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
        select d.docid,d.status,t.taskid, ts.taskid,ts.status
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
             insert into wm_task(tasktypeid,docid,status)
             values(:ttid_loadpallet,:docid,'0')
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



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_SELECT_TSTCHG (
    TASKID type of R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable ttcode type of r_code;
declare variable ttid type of r_id;
declare variable docid type of r_id64;
declare variable wmsid type of r_id;
declare variable tid_loadpallet type of r_id;
declare variable tid_gateauto type of r_id;
declare variable tflags type of wh_flags;
begin
    select tt.code,tt.tasktypeid,t.docid,t.tmpflags,t.wm_sessionid
      from wm_task t
           left join wm_tasktype tt on tt.tasktypeid=t.tasktypeid
     where t.taskid = :taskid
      into :ttcode,:ttid,:docid,:tflags,:wmsid;

    if (:ttcode <> 'SELECT') then
        exception exc_k_wrongtasktype;

    if (:newstat = '2') then
    begin
        if (not exists(select *
                         from wm_task t
                        where t.docid = :docid
                          and t.tasktypeid = :ttid
                          and t.taskmethodid is NOT NULL
                          and t.status <> '2')) then
            update document d
               set d.status = '2'
             where d.docid = :docid;

        select t.tid_gateauto
          from WH_LOADAUTODC_GETTASKBYDOC(:docid) t
          into :tid_gateauto;
        if (:tid_gateauto is NOT NULL) then
            execute procedure wh_loadpalletdc_createtaskes(:tid_gateauto);

        if ((:tflags is NOT NULL and :tflags containing 'A')
/*            or
            not exists(select *
                         from wm_task_wares tw
                              left join wm_task_lot tl on tl.taskwaresid = tw.taskwaresid
                        where tw.taskid = :taskid
                          and tl.palletid is NOT NULL)*/
        ) then
        begin
            select tb.task1id
              from wh_taskbond tb
                   left join wh_taskbondtype tbt on tbt.id = tb.taskbondtid
                   left join wm_task t on t.taskid = tb.task1id
             where tb.task2id = :taskid
               and tbt.code = 'LOADSELECT'
               and coalesce(t.status,'0') <> '2'
              into :tid_loadpallet;

            if (:tid_loadpallet is NOT NULL) then
            begin
                update wm_task t
                   set t.wm_sessionid = null, t.status = '0'
                 where t.taskid = :tid_loadpallet
                   and coalesce(t.wm_sessionid,0) <> :wmsid;
                execute procedure K_SESSION_JOIN_TASK(:tid_loadpallet, :wmsid);
                execute procedure wh_loadpalletdc_taskend(:tid_loadpallet);
            end
        end

        if (:tflags is NOT NULL and :tflags containing 'E') then
            execute procedure wh_select_clientunfund(:taskid);
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_TASKEND (
    TASKID type of column wm_task.taskid
)
returns (
    NEXTSTEP R_FLAG)
AS
declare variable palletid_select type of column PALLET.palletid;
declare variable palletid_income type of column PALLET.palletid;
declare variable paltypeid_select type of column PALLET_TYPE.id;
declare variable paltypeid_temp type of column PALLET_TYPE.id;
declare variable paltypeid type of column PALLET_TYPE.id;
declare variable palnum type of column PALLET.number;
declare variable tid_loadpal type of column WM_TASK.taskid;
declare variable tid_loaddoc type of column WM_TASK.taskid;
declare variable pbarcode type of column PALLET.number;
declare variable pnumber type of column PALLET.number;
declare variable talgo type of column wm_taskmethod.algorithm;
declare variable tsiteid type of column SITE.siteid;
declare variable docid type of column DOCUMENT.docid;
declare variable tmpflags type of column WM_TASK.tmpflags;
declare variable ttid_loaddoc type of column wm_tasktype.tasktypeid;
begin
    if (not exists(select *
                     from wm_task_wares tw
                    where tw.taskid = :taskid
                      and coalesce(tw.scanquant,0.000) > 0.0001)) then
    begin
        NEXTSTEP = 'E';

        select t.docid, coalesce(t.tmpflags,'')||'E'
          from wm_task t
         where t.taskid = :taskid
          into :docid, :tmpflags;

        execute procedure wh_ttid_loadauto
         returning_values :ttid_loaddoc;

        select t.taskid
          from wm_task t
         where t.docid = :docid
           and t.tasktypeid = :ttid_loaddoc
          into :tid_loaddoc;

        if (:tid_loaddoc is NOT NULL) then
        begin
            for
                select tb.task1id
                  from wh_taskbond tb
                       left join wh_taskbondtype tbt on tbt.id = tb.taskbondtid
                 where tb.task2id = :taskid
                   and tbt.code = 'LOADSELECT'
                  into :tid_loadpal
            do
            begin
                delete from wh_taskbond tb
                 where tb.task1id = :tid_loadpal and tb.task2id = :taskid;
    
                delete from wh_taskbond tb
                 where tb.task1id = :tid_loaddoc and tb.task2id = :tid_loadpal;

                delete from wm_task t where t.taskid = :tid_loadpal;
            end
        end
--            execute procedure K_SESSION_JOIN_TASK(:tid_loadpal, :wmsesid);
--            execute procedure wh_loadpalletdc_taskend(:tid_loadpal);
    end
    else
    begin
        select pt.palletid
          from pallet_temp pt
         where pt.taskid = :taskid
          into :palletid_select;
        
        select pts.id
          from wh_paltypeid_temp pts
          into :paltypeid_temp;
        
        select pts.id
          from wh_paltypeid_select pts
          into :paltypeid_select;
        
        select p.ptypeid
          from pallet p
         where p.palletid = :palletid_select
          into :paltypeid;
        
        if (:paltypeid = :paltypeid_temp) then
        begin
           update pallet p
              set p.ptypeid = :paltypeid_select
            where p.palletid = :palletid_select;
        
        
           update or insert into pallet_select(palletid, taskid)
           values(:palletid_select, :taskid)
           matching(palletid);
        
           if (exists(select *
                        from wm_task t
                             left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                       where t.taskid = :taskid
                         and tm.algorithm = 'P')) then
           begin
               select distinct p.barcode, p.number, p.palletid
                 from wm_task_wares tw
                      left join pallet p on p.palletid = tw.palletid
                where tw.taskid = :taskid
                 into :pbarcode, :pnumber, :palletid_income;

               update pallet p
                  set p.barcode = :pbarcode, p.number = :pnumber
                where p.palletid = :palletid_select;

               update pallet p
                  set p.status = '2'
                where p.palletid = :palletid_income;

               NEXTSTEP = 'M';
           end
           else
               NEXTSTEP = 'P';
        end
        else if (:paltypeid = :paltypeid_select) then
        begin
            
            select tm.algorithm, t.siteid
              from wm_task t
                   left join wm_taskmethod tm on tm.methodid = t.taskmethodid
             where t.taskid = :taskid
              into :talgo, :tsiteid;

           if (:talgo is NOT NULL and :talgo='P') then
           begin
               if (:tsiteid is NOT NULL) then
                   NEXTSTEP = 'E';
               else
                   NEXTSTEP = 'M';
           end
           else
           begin
               select case
                        when ps.printdatetime is NULL then 'P'
                        when ps.printdatetime is NOT NULL and ps.stickdatetime is NULL then 'S'
                        else ''
                      end
                 from pallet_select ps
                where ps.palletid = :palletid_select
                 into :nextstep;
    
               if (:nextstep = '') then
               begin
                if (exists(select *
                            from wm_task_pallet tp
                           where tp.taskid = :taskid
                             and tp.palletid = :palletid_select)) then
                    nextstep = 'E';
                 else
                    nextstep = 'M';
               end
           end
        end
        else
        begin
            select p.number
              from pallet p
             where p.palletid = :palletid_select
              into :palnum;
            execute procedure r_raiseerror('PALLET_ERRORTYPE',:palnum);
        end
    end

    if (:nextstep='E') then
        update wm_task t
           set t.status = '2', t.tmpflags = coalesce(:tmpflags, t.tmpflags)
         where t.taskid = :taskid;

    suspend;
end^

SET TERM ; ^

