

CREATE EXCEPTION EXC_WH_WRONGPRIORITY 'Не верный приоритет';



SET TERM ^ ;

create procedure U3S_SALETOSELECT_CHK (
    DOCID type of column DOCUMENT.docid
)
as
declare variable tid_gateauto type of column WM_TASK.taskid;
declare variable tid_loaddoc type of column WM_TASK.taskid;
declare variable tpriority_loaddoc type of column WM_TASK.priority;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable docnum type of column document.number;
begin
    select tf.tid_gateauto, tf.tid_loadauto, t.priority
      from WH_LOADAUTODC_GETTASKBYDOC(:docid) tf
           left join wm_task t on t.taskid = tf.tid_loadauto
      into :tid_gateauto, :tid_loaddoc, :tpriority_loaddoc;

    if (:tid_loaddoc is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку документа не найдено!';
    if (:tid_gateauto is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку авто не найдено!';

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    docnum = NULL;
    select first(1) d.number
      from wh_taskbond tb
           left join wm_task t
                left join document d on d.docid = t.docid
             on t.taskid = tb.task2id
     where tb.task1id = :tid_gateauto
       and tb.taskbondtid = :tbtid_cardocs
       and tb.task2id <> :tid_loaddoc
       and t.priority is NOT NULL
       and t.priority < :tpriority_loaddoc
      into :docnum;

    if (:tid_loaddoc is NULL) then
        exception exc_wh_wrongdocstat 'Имеются документы с более высоким приоритетом погрузки: '||:docnum;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE_PREVIEW (
    DOCID type of column DOCUMENT.DOCID)
returns (
    NUMPALLET type of R_NUMBER,
    ZONEID type of column SITEZONE.ZONEID,
    ZONENAME type of column SITEZONE.NAME,
    NUMPOS type of R_NUMBER,
    TMALGO type of column WM_TASKMETHOD.ALGORITHM,
    TMNAME type of column WM_TASKMETHOD.NAME,
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WQUANTITY type of R_DOUBLE,
    WWEIGHT type of R_DOUBLE,
    WCAPACITY type of R_DOUBLE,
    VUCODE type of column UNIT.SHORTNAME,
    VUFACTOR type of column WARESUNIT.FACTOR,
    MUCODE type of column UNIT.SHORTNAME,
    MUFACTOR type of column WARESUNIT.FACTOR,
    WSGCODE type of column K_WARES_SELGROUP.CODE,
    WSGNAME type of column K_WARES_SELGROUP.NAME,
    WSGWEIGHT type of R_DOUBLE,
    WSGCAPACITY type of R_DOUBLE,
    PRODUCTDATE type of column WARESLOT.PRODUCTDATE)
AS
begin
    execute procedure U3S_SALETOSELECT_CHK(:docid);
    execute procedure u3s_taskselect_create_prep(:docid);

    for
        select g.waresid,g.code,g.name,
               mwu.factor,mu.shortname,vwu.factor,vu.shortname,
               k.numpallet,k.num,k.amount,k.capacity,k.weight,
               tm.algorithm,tm.name,
               wsg.code,wsg.name,wsg.capacity,wsg.weight,
               k.zoneid,sz.name,k.productdate
          from k_tbltmp_select_docwares k
               left join gwares g
                    left join waresunit vwu
                         left join unit vu on vu.unitid = vwu.unitid
                      on vwu.waresunitid = g.viewunitid
                    left join waresunit mwu
                         left join unit mu on mu.unitid = mwu.unitid
                      on mwu.waresunitid = g.mainunitid
                 on g.waresid = k.waresid
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
               left join k_wares_selgroup wsg on wsg.id = k.selgroupid
               left join sitezone sz on sz.zoneid = k.zoneid
         order by k.numpallet ascending Nulls first,k.num ascending nulls first
          into :wid,:wcode,:wname,:mufactor,:mucode,:vufactor,:vucode,
               :numpallet,:numpos,:wquantity,:wcapacity,:wweight,
               :tmalgo,:tmname,:wsgcode,:wsgname,:wsgcapacity,:wsgweight,
               :zoneid,:zonename,:productdate
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable ttinitst_select type of column wm_tasktype.initstatus;
declare variable tmid_select type of column wm_taskmethod.methodid;
declare variable waresid type of column GWARES.waresid;
declare variable amount type of r_double;
declare variable numpallet type of r_number;
declare variable numpos type of r_number;
declare variable status type of r_status;
declare variable slotid type of r_id;
declare variable taskid type of r_id;
declare variable taskpalletnum type of r_number;
declare variable price type of r_double;
declare variable CAPACITY type of r_double;
declare variable WEIGHT type of r_double;
declare variable Zoneid type of r_id;
declare variable productdate type of column wm_task_wares.plandatetime;
begin
    execute procedure U3S_SALETOSELECT_CHK(:docid);
    execute procedure u3s_taskselect_create_prep(:docid);

    select k.ttid,coalesce(k.ttinitst,'0')
      from k_tasktype_by_code('SELECT',NULL) k
      into :ttid_select,:ttinitst_select;


    taskid = NULL;
    taskpalletnum = -1;
    for
        select coalesce(k.numpallet,0),k.num,k.taskmethodid,k.waresid,k.amount,k.slotid,coalesce(tm.startstatus,:ttinitst_select),k.zoneid,k.productdate
          from k_tbltmp_select_docwares k
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
         order by k.numpallet ascending nulls last,k.num ascending nulls last
          into :numpallet,:numpos,:tmid_select,:waresid,:amount,:slotid,:status,:zoneid,:productdate
    do
    begin
        if (:taskpalletnum <> :numpallet and :taskpalletnum is NOT NULL and :numpallet is NOT NULL) then
        begin
            if (:taskid is NOT NULL) then
            begin
                select sum(ww.weight),sum(ww.capacity)
                  from wm_task_wares tw
                       left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
                 where tw.taskid = :taskid
                  into :WEIGHT,:CAPACITY;
            
                update wm_task t
                   set t.weight = :weight,t.capacity = :capacity
                 where t.taskid = :taskid;
            end

            taskpalletnum = :numpallet;

            if (:zoneid = 0) then zoneid = NULL;
            insert into wm_task(tasktypeid,taskmethodid,status,docid,num,zoneid)
            values (:ttid_select,:tmid_select,:status,:docid,:numpallet,:zoneid)
            returning taskid
            into :taskid;
        end

        price = NULL;
        select round(sum(cg.docsum)/sum(cg.amount),4)
          from cargo cg
         where cg.document = :docid
           and cg.waresid = :waresid
           and cg.cargo2id is NULL
           and cg.amount > 0.0001
          into :price;
        if (:price is null) then price = 0.000;

        insert into wm_task_wares(taskid,waresid,status,quantity,siteid,num,summa,plandatetime)
        values(:taskid,:waresid,iif(:tmid_select is NOT NULL,'0',NULL),:amount,:slotid,:numpos,:price,:productdate);
    end

    if (:taskid is NOT NULL) then
    begin
        select sum(ww.weight),sum(ww.capacity)
          from wm_task_wares tw
               left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
         where tw.taskid = :taskid
          into :WEIGHT,:CAPACITY;
    
        update wm_task t
           set t.weight = :weight,t.capacity = :capacity
         where t.taskid = :taskid;
    end

    for
        select t.taskid
          from wm_task t
         where t.docid = :docid
           and t.tasktypeid = :ttid_select
           and t.taskmethodid is NULL
          into :taskid
    do
    begin
        execute procedure wh_select_clientunfund(:taskid);
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SALETOSELECT_CHK (
    DOCID type of column DOCUMENT.docid
)
as
declare variable tid_gateauto type of column WM_TASK.taskid;
declare variable tid_loaddoc type of column WM_TASK.taskid;
declare variable tpriority_loaddoc type of column WM_TASK.priority;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable docnum type of column document.number;
begin
    select tf.tid_gateauto, tf.tid_loadauto, t.priority
      from WH_LOADAUTODC_GETTASKBYDOC(:docid) tf
           left join wm_task t on t.taskid = tf.tid_loadauto
      into :tid_gateauto, :tid_loaddoc, :tpriority_loaddoc;

    if (:tid_loaddoc is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку документа не найдено!';
    if (:tid_gateauto is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку авто не найдено!';

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    docnum = NULL;
    select first(1) d.number
      from wh_taskbond tb
           left join wm_task t
                left join document d on d.docid = t.docid
             on t.taskid = tb.task2id
     where tb.task1id = :tid_gateauto
       and tb.taskbondtid = :tbtid_cardocs
       and tb.task2id <> :tid_loaddoc
       and t.priority is NOT NULL
       and t.priority < :tpriority_loaddoc
      into :docnum;

    if (:tid_loaddoc is not NULL) then
        exception exc_wh_wrongdocstat 'Имеются документы с более высоким приоритетом погрузки: '||:docnum;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE_PREP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable waresid type of column GWARES.waresid;
declare variable selgroupid type of column k_wares_selgroup.id;
declare variable maxfactor type of r_double;
declare variable amount type of r_double;
declare variable numpallet type of r_number;
declare variable numpos type of r_number;
declare variable palletunitid type of r_id;
declare variable ttid_select type of r_id;
declare variable tmid_pallet type of column wm_taskmethod.methodid;
declare variable tmid_f type of column wm_taskmethod.methodid;
declare variable objid type of r_id;
declare variable weight type of r_double;
declare variable capacity type of r_double;
declare variable zoneid type of r_id;
declare variable cntzone type of r_number;
declare variable docid_fundsale type of column DOCUMENT.docid;
declare variable productdate type of column WARESLOT.productdate;
begin
    select distinct db.doc1id
      from docbond db
     where db.doc2id = :docid
       and db.docbondtid = (select dbtid from wh_dbtid_fundsale)
      into :docid_fundsale;

    if (:docid_fundsale is NULL) then
        exception exc_wh_wrongdocstat 'Документ резерва продажи не найден!';


    select wm.palletunitid
      from wm_config wm
      into :palletunitid;

    select k.ttid
      from k_tasktype_by_code('SELECT',NULL) k
      into :ttid_select;

    select tm.methodid
      from wm_taskmethod tm
     where tm.tasktypeid = :ttid_select and tm.algorithm = 'P'
      into :tmid_pallet;

    select tm.methodid
      from wm_taskmethod tm
     where tm.tasktypeid = :ttid_select and tm.algorithm = 'F'
      into :tmid_f;

    if (:tmid_f is NULL) then
        exception exc_k_common 'Не найден метод отборки с паллета!';

    select d.fromobj
      from document d
     where d.docid = :docid
      into :objid;

    -- Зона по умолчанию
    for
        select sz.zoneid
          from sitezone sz
         where sz.objid = :objid
          into :zoneid
    do
        cntzone = :cntzone + 1;
    if (:cntzone <> 1) then zoneid = 0;

    numpallet = 0;
    numpos = 1;
    for
        with wares as(
            select rcc.waresid as waresid, rcc.productdate as productdate, sum(rcc.amount)  as amount
              from wh_reserve_client_changes rcc
             where rcc.docid = :docid_fundsale
            group by rcc.waresid, rcc.productdate
        )
        select w.waresid,w.productdate,w.amount,coalesce(g.selgroup,0),wu.factor
          from wares w
               left join gwares g on g.waresid = w.waresid
               left join waresunit wu on wu.waresid = w.waresid and wu.unitid = :palletunitid
          into :waresid,:productdate,:amount,:selgroupid,:maxfactor
    do
    begin
        -- Откидываем полные поддоны
        if (:maxfactor is NOT NULL) then
            while (:amount-:maxfactor > -0.000001) do -- and :rest - :maxfactor > -0.000001) do
            begin
                weight = NULL; capacity = NULL;
                select wc.weight,wc.capacity
                  from WM_GETWARESWEIGHTCAPACITY(:waresid,:maxfactor) wc
                  into :weight,:capacity;

                numpallet = :numpallet + 1;
                insert into k_tbltmp_select_docwares(waresid,amount,selgroupid,taskmethodid,rest,slotid,rowid,weight,capacity,numpallet,num,zoneid,productdate)
                values(:waresid,:maxfactor,:selgroupid,:tmid_pallet,NULL,NULL,NULL,:weight,:capacity,:numpallet,:numpos,:zoneid,:productdate);

                amount = :amount - :maxfactor;
            end
        
        -- Скидываем остатки
        if (:amount>0.00001) then
        begin
            weight = NULL; capacity = NULL;
            select wc.weight,wc.capacity
              from WM_GETWARESWEIGHTCAPACITY(:waresid,:amount) wc
              into :weight,:capacity;

             insert into k_tbltmp_select_docwares(waresid,amount,selgroupid,taskmethodid,rest,slotid,rowid,weight,capacity,zoneid,sitesegmentid,productdate)
             values(:waresid,:amount,:selgroupid,:tmid_f,NULL,NULL,NULL,:weight,:capacity,:zoneid,NULL,:productdate);
        end
    end

    update k_tbltmp_select_docwares sd
       set sd.numpallet = :numpallet + 1
     where sd.taskmethodid=:tmid_f
       and numpallet is NULL;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable ttinitst_select type of column wm_tasktype.initstatus;
declare variable tmid_select type of column wm_taskmethod.methodid;
declare variable waresid type of column GWARES.waresid;
declare variable amount type of r_double;
declare variable numpallet type of r_number;
declare variable numpos type of r_number;
declare variable status type of r_status;
declare variable slotid type of r_id;
declare variable taskid type of r_id;
declare variable taskpalletnum type of r_number;
declare variable price type of r_double;
declare variable CAPACITY type of r_double;
declare variable WEIGHT type of r_double;
declare variable Zoneid type of r_id;
declare variable productdate type of column wm_task_wares.plandatetime;
begin
    execute procedure U3S_SALETOSELECT_CHK(:docid);
    execute procedure u3s_taskselect_create_prep(:docid);

    select k.ttid,coalesce(k.ttinitst,'0')
      from k_tasktype_by_code('SELECT',NULL) k
      into :ttid_select,:ttinitst_select;


    taskid = NULL;
    taskpalletnum = -1;
    for
        select coalesce(k.numpallet,0),k.num,k.taskmethodid,k.waresid,k.amount,k.slotid,coalesce(tm.startstatus,:ttinitst_select),k.zoneid,k.productdate
          from k_tbltmp_select_docwares k
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
         order by k.numpallet ascending nulls last,k.num ascending nulls last
          into :numpallet,:numpos,:tmid_select,:waresid,:amount,:slotid,:status,:zoneid,:productdate
    do
    begin
        if (:taskpalletnum <> :numpallet and :taskpalletnum is NOT NULL and :numpallet is NOT NULL) then
        begin
            if (:taskid is NOT NULL) then
            begin
                select sum(ww.weight),sum(ww.capacity)
                  from wm_task_wares tw
                       left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
                 where tw.taskid = :taskid
                  into :WEIGHT,:CAPACITY;
            
                update wm_task t
                   set t.weight = :weight,t.capacity = :capacity
                 where t.taskid = :taskid;
            end

            taskpalletnum = :numpallet;

            if (:zoneid = 0) then zoneid = NULL;
            insert into wm_task(tasktypeid,taskmethodid,status,docid,num,zoneid)
            values (:ttid_select,:tmid_select,:status,:docid,:numpallet,:zoneid)
            returning taskid
            into :taskid;
        end

        price = NULL;
        select round(sum(cg.docsum)/sum(cg.amount),4)
          from cargo cg
         where cg.document = :docid
           and cg.waresid = :waresid
           and cg.cargo2id is NULL
           and cg.amount > 0.0001
          into :price;
        if (:price is null) then price = 0.000;

        insert into wm_task_wares(taskid,waresid,status,quantity,siteid,num,summa,plandatetime)
        values(:taskid,:waresid,iif(:tmid_select is NOT NULL,'0',NULL),:amount,:slotid,:numpos,:price,:productdate);
    end

    if (:taskid is NOT NULL) then
    begin
        select sum(ww.weight),sum(ww.capacity)
          from wm_task_wares tw
               left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
         where tw.taskid = :taskid
          into :WEIGHT,:CAPACITY;
    
        update wm_task t
           set t.weight = :weight,t.capacity = :capacity
         where t.taskid = :taskid;
    end

    for
        select t.taskid
          from wm_task t
         where t.docid = :docid
           and t.tasktypeid = :ttid_select
           and t.taskmethodid is NULL
          into :taskid
    do
    begin
        execute procedure wh_select_clientunfund(:taskid);
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SALETOSELECT_CHK (
    DOCID type of column DOCUMENT.docid
)
as
declare variable tid_gateauto type of column WM_TASK.taskid;
declare variable tid_loaddoc type of column WM_TASK.taskid;
declare variable tpriority_loaddoc type of column WM_TASK.priority;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable docnum type of column document.number;
begin
    select tf.tid_gateauto, tf.tid_loadauto, t.priority
      from WH_LOADAUTODC_GETTASKBYDOC(:docid) tf
           left join wm_task t on t.taskid = tf.tid_loadauto
      into :tid_gateauto, :tid_loaddoc, :tpriority_loaddoc;

    if (:tid_loaddoc is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку документа не найдено!';
    if (:tid_gateauto is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку авто не найдено!';

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    docnum = NULL;
    select first(1) d.number
      from wh_taskbond tb
           left join wm_task t
                left join document d on d.docid = t.docid
             on t.taskid = tb.task2id
     where tb.task1id = :tid_gateauto
       and tb.taskbondtid = :tbtid_cardocs
       and tb.task2id <> :tid_loaddoc
       and t.priority is NOT NULL
       and t.priority < :tpriority_loaddoc
      into :docnum;

    if (:docnum is not NULL) then
        exception exc_wh_wrongdocstat 'Имеются документы с более высоким приоритетом погрузки: '||:docnum;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE_PREP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable waresid type of column GWARES.waresid;
declare variable selgroupid type of column k_wares_selgroup.id;
declare variable maxfactor type of r_double;
declare variable amount type of r_double;
declare variable numpallet type of r_number;
declare variable numpos type of r_number;
declare variable palletunitid type of r_id;
declare variable ttid_select type of r_id;
declare variable tmid_pallet type of column wm_taskmethod.methodid;
declare variable tmid_f type of column wm_taskmethod.methodid;
declare variable objid type of r_id;
declare variable weight type of r_double;
declare variable capacity type of r_double;
declare variable zoneid type of r_id;
declare variable cntzone type of r_number;
declare variable docid_fundsale type of column DOCUMENT.docid;
declare variable productdate type of column WARESLOT.productdate;
begin
    select distinct db.doc1id
      from docbond db
     where db.doc2id = :docid
       and db.docbondtid = (select dbtid from wh_dbtid_fundsale)
      into :docid_fundsale;

    if (:docid_fundsale is NULL) then
        exception exc_wh_wrongdocstat 'Документ резерва продажи не найден!';


    select wm.palletunitid
      from wm_config wm
      into :palletunitid;

    select k.ttid
      from k_tasktype_by_code('SELECT',NULL) k
      into :ttid_select;

    select tm.methodid
      from wm_taskmethod tm
     where tm.tasktypeid = :ttid_select and tm.algorithm = 'P'
      into :tmid_pallet;

    select tm.methodid
      from wm_taskmethod tm
     where tm.tasktypeid = :ttid_select and tm.algorithm = 'F'
      into :tmid_f;

    if (:tmid_f is NULL) then
        exception exc_k_common 'Не найден метод отборки с паллета!';

    select d.fromobj
      from document d
     where d.docid = :docid
      into :objid;

    -- Зона по умолчанию
    for
        select sz.zoneid
          from sitezone sz
         where sz.objid = :objid
          into :zoneid
    do
        cntzone = :cntzone + 1;
    if (:cntzone <> 1) then zoneid = 0;

    numpallet = 0;
    numpos = 1;
    for
        with wares as(
            select rcc.waresid as waresid, rcc.productdate as productdate, sum(rcc.amount)  as amount
              from wh_reserve_client_changes rcc
             where rcc.docid = :docid_fundsale
            group by rcc.waresid, rcc.productdate
        )
        select w.waresid,w.productdate,w.amount,coalesce(g.selgroup,0),wu.factor
          from wares w
               left join gwares g on g.waresid = w.waresid
               left join waresunit wu on wu.waresid = w.waresid and wu.unitid = :palletunitid
          into :waresid,:productdate,:amount,:selgroupid,:maxfactor
    do
    begin
        -- Откидываем полные поддоны
        if (:maxfactor is NOT NULL) then
            while (:amount-:maxfactor > -0.000001) do -- and :rest - :maxfactor > -0.000001) do
            begin
                weight = NULL; capacity = NULL;
                select wc.weight,wc.capacity
                  from WM_GETWARESWEIGHTCAPACITY(:waresid,:maxfactor) wc
                  into :weight,:capacity;

                numpallet = :numpallet + 1;
                insert into k_tbltmp_select_docwares(waresid,amount,selgroupid,taskmethodid,rest,slotid,rowid,weight,capacity,numpallet,num,zoneid,productdate)
                values(:waresid,:maxfactor,:selgroupid,:tmid_pallet,NULL,NULL,NULL,:weight,:capacity,:numpallet,:numpos,:zoneid,:productdate);

                amount = :amount - :maxfactor;
            end
        
        -- Скидываем остатки
        if (:amount>0.00001) then
        begin
            weight = NULL; capacity = NULL;
            select wc.weight,wc.capacity
              from WM_GETWARESWEIGHTCAPACITY(:waresid,:amount) wc
              into :weight,:capacity;

             insert into k_tbltmp_select_docwares(waresid,amount,selgroupid,taskmethodid,rest,slotid,rowid,weight,capacity,zoneid,sitesegmentid,productdate)
             values(:waresid,:amount,:selgroupid,:tmid_f,NULL,NULL,NULL,:weight,:capacity,:zoneid,NULL,:productdate);
        end
    end

    update k_tbltmp_select_docwares sd
       set sd.numpallet = :numpallet + 1
     where sd.taskmethodid=:tmid_f
       and numpallet is NULL;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable ttinitst_select type of column wm_tasktype.initstatus;
declare variable tmid_select type of column wm_taskmethod.methodid;
declare variable waresid type of column GWARES.waresid;
declare variable amount type of r_double;
declare variable numpallet type of r_number;
declare variable numpos type of r_number;
declare variable status type of r_status;
declare variable slotid type of r_id;
declare variable taskid type of r_id;
declare variable taskpalletnum type of r_number;
declare variable price type of r_double;
declare variable CAPACITY type of r_double;
declare variable WEIGHT type of r_double;
declare variable Zoneid type of r_id;
declare variable productdate type of column wm_task_wares.plandatetime;
begin
    execute procedure U3S_SALETOSELECT_CHK(:docid);
    execute procedure u3s_taskselect_create_prep(:docid);

    select k.ttid,coalesce(k.ttinitst,'0')
      from k_tasktype_by_code('SELECT',NULL) k
      into :ttid_select,:ttinitst_select;


    taskid = NULL;
    taskpalletnum = -1;
    for
        select coalesce(k.numpallet,0),k.num,k.taskmethodid,k.waresid,k.amount,k.slotid,coalesce(tm.startstatus,:ttinitst_select),k.zoneid,k.productdate
          from k_tbltmp_select_docwares k
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
         order by k.numpallet ascending nulls last,k.num ascending nulls last
          into :numpallet,:numpos,:tmid_select,:waresid,:amount,:slotid,:status,:zoneid,:productdate
    do
    begin
        if (:taskpalletnum <> :numpallet and :taskpalletnum is NOT NULL and :numpallet is NOT NULL) then
        begin
            if (:taskid is NOT NULL) then
            begin
                select sum(ww.weight),sum(ww.capacity)
                  from wm_task_wares tw
                       left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
                 where tw.taskid = :taskid
                  into :WEIGHT,:CAPACITY;
            
                update wm_task t
                   set t.weight = :weight,t.capacity = :capacity
                 where t.taskid = :taskid;
            end

            taskpalletnum = :numpallet;

            if (:zoneid = 0) then zoneid = NULL;
            insert into wm_task(tasktypeid,taskmethodid,status,docid,num,zoneid)
            values (:ttid_select,:tmid_select,:status,:docid,:numpallet,:zoneid)
            returning taskid
            into :taskid;
        end

        price = NULL;
        select round(sum(cg.docsum)/sum(cg.amount),4)
          from cargo cg
         where cg.document = :docid
           and cg.waresid = :waresid
           and cg.cargo2id is NULL
           and cg.amount > 0.0001
          into :price;
        if (:price is null) then price = 0.000;

        insert into wm_task_wares(taskid,waresid,status,quantity,siteid,num,summa,plandatetime)
        values(:taskid,:waresid,iif(:tmid_select is NOT NULL,'0',NULL),:amount,:slotid,:numpos,:price,:productdate);
    end

    if (:taskid is NOT NULL) then
    begin
        select sum(ww.weight),sum(ww.capacity)
          from wm_task_wares tw
               left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
         where tw.taskid = :taskid
          into :WEIGHT,:CAPACITY;
    
        update wm_task t
           set t.weight = :weight,t.capacity = :capacity
         where t.taskid = :taskid;
    end

    for
        select t.taskid
          from wm_task t
         where t.docid = :docid
           and t.tasktypeid = :ttid_select
           and t.taskmethodid is NULL
          into :taskid
    do
    begin
        execute procedure wh_select_clientunfund(:taskid);
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELMANAG_LISTGATEAUTODOCS (
    TASKID_GATEAUTO type of column WM_TASK.TASKID,
    WHID type of column OBJECT.OBJID)
returns (
    TPRIORITY type of column WM_TASK.PRIORITY,
    DOCID type of column DOCUMENT.DOCID,
    DOCDATE type of column DOCUMENT.DOCDATE,
    RDOCDATE type of column DOCUMENT.REALDOCDATE,
    DOCNUM type of column DOCUMENT.NUMBER,
    DOCSUM type of column DOCUMENT.AMOUNT,
    STAT type of column R_STATUS.CODE,
    STATNAME type of column R_STATUS.NAME,
    THROUGHNAME type of R_FULLNAME,
    TONAME type of R_FULLNAME)
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
         order by t.priority ascending nulls last
          into :tpriority, :docid,:docdate,:rdocdate,:docnum,:docsum,
               :stat,:statname,:throughname,:toname
    do
    begin
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_SELMANAG_LISTGATEAUTO_TASKES (
    TASKID_GATEAUTO type of column WM_TASK.taskid = NULL
)
returns (
    taskid type of column WM_TASK.taskid,
    status type of column WM_TASK.status,
    plandatetime type of column WM_TASK.plandatetime,
    siteid type of column WM_TASK.siteid,
    infoid type of column WM_TASK.infoid,
    priority type of column WM_TASK.priority
)
as
declare variable ttid_gateauto type of column WM_TASKTYPE.tasktypeid;
begin
    execute procedure wh_ttid_gateauto
     returning_values :ttid_gateauto;

    if (:taskid_gateauto is NOT NULL) then
    begin
        for
            select t.taskid, t.status, t.plandatetime, t.siteid, t.infoid, t.priority
              from wm_task t
             where t.taskid = :taskid_gateauto
               and t.tasktypeid = :ttid_gateauto
              into :taskid, :status, :plandatetime, :siteid, :infoid, :priority
        do
            suspend;
    end
    else
    begin
        
        for
            select t.taskid, t.status, t.plandatetime, t.siteid, t.infoid, t.priority
              from wm_task t
             where t.tasktypeid = :ttid_gateauto
               and t.status = '0'
             union distinct
            select t.taskid, t.status, t.plandatetime, t.siteid, t.infoid, t.priority
              from wm_task t
             where t.tasktypeid = :ttid_gateauto
               and t.status = '1'
              into :taskid, :status, :plandatetime, :siteid, :infoid, :priority
        do
            suspend;

    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELMANAG_LISTGATEAUTO (
    WHID type of column OBJECT.OBJID,
    TASKID_GATEAUTO type of column WM_TASK.TASKID = NULL
)
returns (
    TID type of column WM_TASK.TASKID,
    GATEID type of column SITE.SITEID,
    GATENAME type of column SITE.NAME,
    AUTOID type of column T_AUTO.AID,
    AUTONAME type of column T_AUTO.NAME,
    TSTAT type of column R_STATUS.CODE,
    TSTATNAME type of column R_STATUS.NAME,
    PLANDATETIME type of column WM_TASK.PLANDATETIME,
    D type of R_SHORTNUMBER,
    DWH type of R_SHORTNUMBER,
    DWH1 type of R_SHORTNUMBER,
    DWHG type of R_SHORTNUMBER,
    CLIENT type of R_FULLNAME,
    CLIENTTITLE type of RBS_BIGVARCHAR)
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
        select ga.taskid, rs.code, rs.name, ga.plandatetime,
               s.siteid, s.name, a.aid, a.name,
               count(distinct d.docid),
               sum(iif(d.fromobj = :whid, 1, 0)),
               sum(iif(d.fromobj = :whid and d.status='1', 1, 0)),
               sum(iif(d.fromobj = :whid and d.status='g', 1, 0)),
               max(iif(d.fromobj = :whid, d.toobj, 0)),
               count(distinct iif(d.fromobj = :whid, d.toobj, NULL)),
               list(distinct (select objname from wh_get_objectname(d.toobj)))
          from WH_SELMANAG_LISTGATEAUTO_TASKES(:taskid_gateauto) ga
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

CREATE OR ALTER procedure WH_SELMANAG_LISTGATEAUTO (
    WHID type of column OBJECT.OBJID,
    TASKID_GATEAUTO type of column WM_TASK.TASKID = NULL
)
returns (
    TID type of column WM_TASK.TASKID,
    GATEID type of column SITE.SITEID,
    GATENAME type of column SITE.NAME,
    AUTOID type of column T_AUTO.AID,
    AUTONAME type of column T_AUTO.NAME,
    TSTAT type of column R_STATUS.CODE,
    TSTATNAME type of column R_STATUS.NAME,
    PLANDATETIME type of column WM_TASK.PLANDATETIME,
    D type of R_SHORTNUMBER,
    DWH type of R_SHORTNUMBER,
    DWH1 type of R_SHORTNUMBER,
    DWHG type of R_SHORTNUMBER,
    CLIENT type of R_FULLNAME,
    CLIENTTITLE type of RBS_BIGVARCHAR)
AS
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable clientid type of column OBJECT.objid;
declare variable clientcnt type of R_SHORTNUMBER;
begin
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    for
        select ga.taskid, rs.code, rs.name, ga.plandatetime,
               s.siteid, s.name, a.aid, a.name,
               count(distinct d.docid),
               sum(iif(d.fromobj = :whid, 1, 0)),
               sum(iif(d.fromobj = :whid and d.status='1', 1, 0)),
               sum(iif(d.fromobj = :whid and d.status='g', 1, 0)),
               max(iif(d.fromobj = :whid, d.toobj, 0)),
               count(distinct iif(d.fromobj = :whid, d.toobj, NULL)),
               list(distinct (select objname from wh_get_objectname(d.toobj)))
          from WH_SELMANAG_LISTGATEAUTO_TASKES(:taskid_gateauto) ga
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

CREATE OR ALTER procedure U3S_SALETOSELECT_CHK (
    DOCID type of column DOCUMENT.docid
)
RETURNS(
    tid_gateauto type of column WM_TASK.taskid,
    tid_loaddoc type of column WM_TASK.taskid
)
as
declare variable tpriority_loaddoc type of column WM_TASK.priority;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable docnum type of column document.number;
begin
    select tf.tid_gateauto, tf.tid_loadauto, t.priority
      from WH_LOADAUTODC_GETTASKBYDOC(:docid) tf
           left join wm_task t on t.taskid = tf.tid_loadauto
      into :tid_gateauto, :tid_loaddoc, :tpriority_loaddoc;

    if (:tid_loaddoc is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку документа не найдено!';
    if (:tid_gateauto is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку авто не найдено!';

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    docnum = NULL;
    select first(1) d.number
      from wh_taskbond tb
           left join wm_task t
                left join document d on d.docid = t.docid
             on t.taskid = tb.task2id
     where tb.task1id = :tid_gateauto
       and tb.taskbondtid = :tbtid_cardocs
       and tb.task2id <> :tid_loaddoc
       and t.priority is NOT NULL
       and t.priority < :tpriority_loaddoc
      into :docnum;

    if (:docnum is not NULL) then
        exception exc_wh_wrongdocstat 'Имеются документы с более высоким приоритетом погрузки: '||:docnum;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SALETOSELECT_CHK (
    DOCID type of column DOCUMENT.docid
)
as
declare variable tid_gateauto type of column WM_TASK.taskid;
declare variable tid_loaddoc type of column WM_TASK.taskid;
declare variable tpriority_loaddoc type of column WM_TASK.priority;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable docnum type of column document.number;
begin
    select tf.tid_gateauto, tf.tid_loadauto, t.priority
      from WH_LOADAUTODC_GETTASKBYDOC(:docid) tf
           left join wm_task t on t.taskid = tf.tid_loadauto
      into :tid_gateauto, :tid_loaddoc, :tpriority_loaddoc;

    if (:tid_loaddoc is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку документа не найдено!';
    if (:tid_gateauto is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку авто не найдено!';

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    docnum = NULL;
    select first(1) d.number
      from wh_taskbond tb
           left join wm_task t
                left join document d on d.docid = t.docid
             on t.taskid = tb.task2id
     where tb.task1id = :tid_gateauto
       and tb.taskbondtid = :tbtid_cardocs
       and tb.task2id <> :tid_loaddoc
       and t.priority is NOT NULL
       and t.priority < :tpriority_loaddoc
      into :docnum;

    if (:docnum is not NULL) then
        exception exc_wh_wrongdocstat 'Имеются документы с более высоким приоритетом погрузки: '||:docnum;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable ttinitst_select type of column wm_tasktype.initstatus;
declare variable tmid_select type of column wm_taskmethod.methodid;
declare variable waresid type of column GWARES.waresid;
declare variable amount type of r_double;
declare variable numpallet type of r_number;
declare variable numpos type of r_number;
declare variable status type of r_status;
declare variable slotid type of r_id;
declare variable taskid type of r_id;
declare variable taskpalletnum type of r_number;
declare variable price type of r_double;
declare variable CAPACITY type of r_double;
declare variable WEIGHT type of r_double;
declare variable Zoneid type of r_id;
declare variable productdate type of column wm_task_wares.plandatetime;
begin
    execute procedure U3S_SALETOSELECT_CHK(:docid);
    execute procedure u3s_taskselect_create_prep(:docid);

    select k.ttid,coalesce(k.ttinitst,'0')
      from k_tasktype_by_code('SELECT',NULL) k
      into :ttid_select,:ttinitst_select;


    taskid = NULL;
    taskpalletnum = -1;
    for
        select coalesce(k.numpallet,0),k.num,k.taskmethodid,k.waresid,k.amount,k.slotid,coalesce(tm.startstatus,:ttinitst_select),k.zoneid,k.productdate
          from k_tbltmp_select_docwares k
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
         order by k.numpallet ascending nulls last,k.num ascending nulls last
          into :numpallet,:numpos,:tmid_select,:waresid,:amount,:slotid,:status,:zoneid,:productdate
    do
    begin
        if (:taskpalletnum <> :numpallet and :taskpalletnum is NOT NULL and :numpallet is NOT NULL) then
        begin
            if (:taskid is NOT NULL) then
            begin
                select sum(ww.weight),sum(ww.capacity)
                  from wm_task_wares tw
                       left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
                 where tw.taskid = :taskid
                  into :WEIGHT,:CAPACITY;
            
                update wm_task t
                   set t.weight = :weight,t.capacity = :capacity
                 where t.taskid = :taskid;
            end

            taskpalletnum = :numpallet;

            if (:zoneid = 0) then zoneid = NULL;
            insert into wm_task(tasktypeid,taskmethodid,status,docid,num,zoneid)
            values (:ttid_select,:tmid_select,:status,:docid,:numpallet,:zoneid)
            returning taskid
            into :taskid;
        end

        price = NULL;
        select round(sum(cg.docsum)/sum(cg.amount),4)
          from cargo cg
         where cg.document = :docid
           and cg.waresid = :waresid
           and cg.cargo2id is NULL
           and cg.amount > 0.0001
          into :price;
        if (:price is null) then price = 0.000;

        insert into wm_task_wares(taskid,waresid,status,quantity,siteid,num,summa,plandatetime)
        values(:taskid,:waresid,iif(:tmid_select is NOT NULL,'0',NULL),:amount,:slotid,:numpos,:price,:productdate);
    end

    if (:taskid is NOT NULL) then
    begin
        select sum(ww.weight),sum(ww.capacity)
          from wm_task_wares tw
               left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
         where tw.taskid = :taskid
          into :WEIGHT,:CAPACITY;
    
        update wm_task t
           set t.weight = :weight,t.capacity = :capacity
         where t.taskid = :taskid;
    end

    for
        select t.taskid
          from wm_task t
         where t.docid = :docid
           and t.tasktypeid = :ttid_select
           and t.taskmethodid is NULL
          into :taskid
    do
    begin
        execute procedure wh_select_clientunfund(:taskid);
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE_PREVIEW (
    DOCID type of column DOCUMENT.DOCID)
returns (
    NUMPALLET type of R_NUMBER,
    ZONEID type of column SITEZONE.ZONEID,
    ZONENAME type of column SITEZONE.NAME,
    NUMPOS type of R_NUMBER,
    TMALGO type of column WM_TASKMETHOD.ALGORITHM,
    TMNAME type of column WM_TASKMETHOD.NAME,
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WQUANTITY type of R_DOUBLE,
    WWEIGHT type of R_DOUBLE,
    WCAPACITY type of R_DOUBLE,
    VUCODE type of column UNIT.SHORTNAME,
    VUFACTOR type of column WARESUNIT.FACTOR,
    MUCODE type of column UNIT.SHORTNAME,
    MUFACTOR type of column WARESUNIT.FACTOR,
    WSGCODE type of column K_WARES_SELGROUP.CODE,
    WSGNAME type of column K_WARES_SELGROUP.NAME,
    WSGWEIGHT type of R_DOUBLE,
    WSGCAPACITY type of R_DOUBLE,
    PRODUCTDATE type of column WARESLOT.PRODUCTDATE)
AS
begin
    execute procedure U3S_SALETOSELECT_CHK(:docid);
    execute procedure u3s_taskselect_create_prep(:docid);

    for
        select g.waresid,g.code,g.name,
               mwu.factor,mu.shortname,vwu.factor,vu.shortname,
               k.numpallet,k.num,k.amount,k.capacity,k.weight,
               tm.algorithm,tm.name,
               wsg.code,wsg.name,wsg.capacity,wsg.weight,
               k.zoneid,sz.name,k.productdate
          from k_tbltmp_select_docwares k
               left join gwares g
                    left join waresunit vwu
                         left join unit vu on vu.unitid = vwu.unitid
                      on vwu.waresunitid = g.viewunitid
                    left join waresunit mwu
                         left join unit mu on mu.unitid = mwu.unitid
                      on mwu.waresunitid = g.mainunitid
                 on g.waresid = k.waresid
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
               left join k_wares_selgroup wsg on wsg.id = k.selgroupid
               left join sitezone sz on sz.zoneid = k.zoneid
         order by k.numpallet ascending Nulls first,k.num ascending nulls first
          into :wid,:wcode,:wname,:mufactor,:mucode,:vufactor,:vucode,
               :numpallet,:numpos,:wquantity,:wcapacity,:wweight,
               :tmalgo,:tmname,:wsgcode,:wsgname,:wsgcapacity,:wsgweight,
               :zoneid,:zonename,:productdate
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_SELMANAGGA_DOCTOSELECT (
    DOCID type of column DOCUMENT.docid
)
AS
begin
    UPDATE DOCUMENT D
       set d.status = 'g'
     where d.docid = :docid and d.status = '1';
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELMANAGGA_DOCTOSELECT (
    ID type of column DOCUMENT.docid
)
returns(
    DOCID type of column DOCUMENT.docid,
    DSTAT type of column R_STATUS.code,
    DSTATNAME type of column R_STATUS.NAME
)
AS
begin
    UPDATE DOCUMENT D
       set d.status = 'g'
     where d.docid = :id and d.status = '1';

    select d.DOCID, d.STATUS, rs.name
      from document d
           left join r_status rs on rs.code = d.status and rs.statustype = 'O'
     where d.docid = :docid
      into :docid, :dstat, :dstatname;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SALETOSELECT_CHK (
    DOCID type of column DOCUMENT.docid
)
as
declare variable tid_gateauto type of column WM_TASK.taskid;
declare variable tid_loaddoc type of column WM_TASK.taskid;
declare variable tpriority_loaddoc type of column WM_TASK.priority;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable docnum type of column document.number;
begin
    select tf.tid_gateauto, tf.tid_loadauto, t.priority
      from WH_LOADAUTODC_GETTASKBYDOC(:docid) tf
           left join wm_task t on t.taskid = tf.tid_loadauto
      into :tid_gateauto, :tid_loaddoc, :tpriority_loaddoc;

    if (:tid_loaddoc is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку документа не найдено!';
    if (:tid_gateauto is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку авто не найдено!';

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    docnum = NULL;
    select first(1) d.number
      from wh_taskbond tb
           left join wm_task t
                left join document d on d.docid = t.docid
             on t.taskid = tb.task2id
     where tb.task1id = :tid_gateauto
       and tb.taskbondtid = :tbtid_cardocs
       and tb.task2id <> :tid_loaddoc
       and t.priority is NOT NULL
       and t.priority < :tpriority_loaddoc
       and d.status = '1'
      into :docnum;

    if (:docnum is not NULL) then
        exception exc_wh_wrongdocstat 'Имеются документы с более высоким приоритетом погрузки: '||:docnum;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SALETOSELECT_CHK (
    DOCID type of column DOCUMENT.docid
)
as
declare variable tid_gateauto type of column WM_TASK.taskid;
declare variable tid_loaddoc type of column WM_TASK.taskid;
declare variable tpriority_loaddoc type of column WM_TASK.priority;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable docnum type of column document.number;
declare variable docstat type of column document.status;
begin
    select tf.tid_gateauto, tf.tid_loadauto, t.priority
      from WH_LOADAUTODC_GETTASKBYDOC(:docid) tf
           left join wm_task t on t.taskid = tf.tid_loadauto
      into :tid_gateauto, :tid_loaddoc, :tpriority_loaddoc;

    if (:tid_loaddoc is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку документа не найдено!';
    if (:tid_gateauto is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку авто не найдено!';

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    select d.status
      from document d
     where d.docid = :docid
      into :docstat;

    docnum = NULL;
    select first(1) d.number
      from wh_taskbond tb
           left join wm_task t
                left join document d on d.docid = t.docid
             on t.taskid = tb.task2id
     where tb.task1id = :tid_gateauto
       and tb.taskbondtid = :tbtid_cardocs
       and tb.task2id <> :tid_loaddoc
       and t.priority is NOT NULL
       and t.priority < :tpriority_loaddoc
       and d.status = :docstat
      into :docnum;

    if (:docnum is not NULL) then
        exception exc_wh_wrongdocstat 'Имеются документы с более высоким приоритетом погрузки: '||:docnum;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable ttinitst_select type of column wm_tasktype.initstatus;
declare variable tmid_select type of column wm_taskmethod.methodid;
declare variable waresid type of column GWARES.waresid;
declare variable amount type of r_double;
declare variable numpallet type of r_number;
declare variable numpos type of r_number;
declare variable status type of r_status;
declare variable slotid type of r_id;
declare variable taskid type of r_id;
declare variable taskpalletnum type of r_number;
declare variable price type of r_double;
declare variable CAPACITY type of r_double;
declare variable WEIGHT type of r_double;
declare variable Zoneid type of r_id;
declare variable productdate type of column wm_task_wares.plandatetime;
begin
    execute procedure U3S_SALETOSELECT_CHK(:docid);
    execute procedure u3s_taskselect_create_prep(:docid);

    select k.ttid,coalesce(k.ttinitst,'0')
      from k_tasktype_by_code('SELECT',NULL) k
      into :ttid_select,:ttinitst_select;


    taskid = NULL;
    taskpalletnum = -1;
    for
        select coalesce(k.numpallet,0),k.num,k.taskmethodid,k.waresid,k.amount,k.slotid,coalesce(tm.startstatus,:ttinitst_select),k.zoneid,k.productdate
          from k_tbltmp_select_docwares k
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
         order by k.numpallet ascending nulls last,k.num ascending nulls last
          into :numpallet,:numpos,:tmid_select,:waresid,:amount,:slotid,:status,:zoneid,:productdate
    do
    begin
        if (:taskpalletnum <> :numpallet and :taskpalletnum is NOT NULL and :numpallet is NOT NULL) then
        begin
            if (:taskid is NOT NULL) then
            begin
                select sum(ww.weight),sum(ww.capacity)
                  from wm_task_wares tw
                       left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
                 where tw.taskid = :taskid
                  into :WEIGHT,:CAPACITY;
            
                update wm_task t
                   set t.weight = :weight,t.capacity = :capacity
                 where t.taskid = :taskid;
            end

            taskpalletnum = :numpallet;

            if (:zoneid = 0) then zoneid = NULL;
            insert into wm_task(tasktypeid,taskmethodid,status,docid,num,zoneid)
            values (:ttid_select,:tmid_select,:status,:docid,:numpallet,:zoneid)
            returning taskid
            into :taskid;
        end

        price = NULL;
        select round(sum(cg.docsum)/sum(cg.amount),4)
          from cargo cg
         where cg.document = :docid
           and cg.waresid = :waresid
           and cg.cargo2id is NULL
           and cg.amount > 0.0001
          into :price;
        if (:price is null) then price = 0.000;

        insert into wm_task_wares(taskid,waresid,status,quantity,siteid,num,summa,plandatetime)
        values(:taskid,:waresid,iif(:tmid_select is NOT NULL,'0',NULL),:amount,:slotid,:numpos,:price,:productdate);
    end

    if (:taskid is NOT NULL) then
    begin
        select sum(ww.weight),sum(ww.capacity)
          from wm_task_wares tw
               left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
         where tw.taskid = :taskid
          into :WEIGHT,:CAPACITY;
    
        update wm_task t
           set t.weight = :weight,t.capacity = :capacity
         where t.taskid = :taskid;
    end

    for
        select t.taskid
          from wm_task t
         where t.docid = :docid
           and t.tasktypeid = :ttid_select
           and t.taskmethodid is NULL
          into :taskid
    do
    begin
        execute procedure wh_select_clientunfund(:taskid);
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE_PREVIEW (
    DOCID type of column DOCUMENT.DOCID)
returns (
    NUMPALLET type of R_NUMBER,
    ZONEID type of column SITEZONE.ZONEID,
    ZONENAME type of column SITEZONE.NAME,
    NUMPOS type of R_NUMBER,
    TMALGO type of column WM_TASKMETHOD.ALGORITHM,
    TMNAME type of column WM_TASKMETHOD.NAME,
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WQUANTITY type of R_DOUBLE,
    WWEIGHT type of R_DOUBLE,
    WCAPACITY type of R_DOUBLE,
    VUCODE type of column UNIT.SHORTNAME,
    VUFACTOR type of column WARESUNIT.FACTOR,
    MUCODE type of column UNIT.SHORTNAME,
    MUFACTOR type of column WARESUNIT.FACTOR,
    WSGCODE type of column K_WARES_SELGROUP.CODE,
    WSGNAME type of column K_WARES_SELGROUP.NAME,
    WSGWEIGHT type of R_DOUBLE,
    WSGCAPACITY type of R_DOUBLE,
    PRODUCTDATE type of column WARESLOT.PRODUCTDATE)
AS
begin
    execute procedure U3S_SALETOSELECT_CHK(:docid);
    execute procedure u3s_taskselect_create_prep(:docid);

    for
        select g.waresid,g.code,g.name,
               mwu.factor,mu.shortname,vwu.factor,vu.shortname,
               k.numpallet,k.num,k.amount,k.capacity,k.weight,
               tm.algorithm,tm.name,
               wsg.code,wsg.name,wsg.capacity,wsg.weight,
               k.zoneid,sz.name,k.productdate
          from k_tbltmp_select_docwares k
               left join gwares g
                    left join waresunit vwu
                         left join unit vu on vu.unitid = vwu.unitid
                      on vwu.waresunitid = g.viewunitid
                    left join waresunit mwu
                         left join unit mu on mu.unitid = mwu.unitid
                      on mwu.waresunitid = g.mainunitid
                 on g.waresid = k.waresid
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
               left join k_wares_selgroup wsg on wsg.id = k.selgroupid
               left join sitezone sz on sz.zoneid = k.zoneid
         order by k.numpallet ascending Nulls first,k.num ascending nulls first
          into :wid,:wcode,:wname,:mufactor,:mucode,:vufactor,:vucode,
               :numpallet,:numpos,:wquantity,:wcapacity,:wweight,
               :tmalgo,:tmname,:wsgcode,:wsgname,:wsgcapacity,:wsgweight,
               :zoneid,:zonename,:productdate
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELMANAGGA_DOCTOSELECT (
    ID type of column DOCUMENT.docid
)
returns(
    DOCID type of column DOCUMENT.docid,
    DSTAT type of column R_STATUS.code,
    DSTATNAME type of column R_STATUS.NAME
)
AS
begin
    UPDATE DOCUMENT D
       set d.status = 'g'
     where d.docid = :id and d.status = '1';

    select d.DOCID, d.STATUS, rs.name
      from document d
           left join r_status rs on rs.code = d.status and rs.statustype = 'O'
     where d.docid = :docid
      into :docid, :dstat, :dstatname;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SALETOSELECT_CHK (
    DOCID type of column DOCUMENT.docid
)
as
declare variable tid_gateauto type of column WM_TASK.taskid;
declare variable tid_loaddoc type of column WM_TASK.taskid;
declare variable tpriority_loaddoc type of column WM_TASK.priority;
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable docnum type of column document.number;
begin
    select tf.tid_gateauto, tf.tid_loadauto, t.priority
      from WH_LOADAUTODC_GETTASKBYDOC(:docid) tf
           left join wm_task t on t.taskid = tf.tid_loadauto
      into :tid_gateauto, :tid_loaddoc, :tpriority_loaddoc;

    if (:tid_loaddoc is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку документа не найдено!';
    if (:tid_gateauto is NULL) then
        exception exc_wh_wrongdocstat 'Задание на погрузку авто не найдено!';

    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    docnum = NULL;
    select first(1) d.number
      from wh_taskbond tb
           left join wm_task t
                left join document d on d.docid = t.docid
             on t.taskid = tb.task2id
     where tb.task1id = :tid_gateauto
       and tb.taskbondtid = :tbtid_cardocs
       and tb.task2id <> :tid_loaddoc
       and t.priority is NOT NULL
       and t.priority < :tpriority_loaddoc
       and d.status = '1'
      into :docnum;

    if (:docnum is not NULL) then
        exception exc_wh_wrongdocstat 'Имеются документы с более высоким приоритетом погрузки: '||:docnum;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable ttinitst_select type of column wm_tasktype.initstatus;
declare variable tmid_select type of column wm_taskmethod.methodid;
declare variable waresid type of column GWARES.waresid;
declare variable amount type of r_double;
declare variable numpallet type of r_number;
declare variable numpos type of r_number;
declare variable status type of r_status;
declare variable slotid type of r_id;
declare variable taskid type of r_id;
declare variable taskpalletnum type of r_number;
declare variable price type of r_double;
declare variable CAPACITY type of r_double;
declare variable WEIGHT type of r_double;
declare variable Zoneid type of r_id;
declare variable productdate type of column wm_task_wares.plandatetime;
begin
    execute procedure U3S_SALETOSELECT_CHK(:docid);
    execute procedure u3s_taskselect_create_prep(:docid);

    select k.ttid,coalesce(k.ttinitst,'0')
      from k_tasktype_by_code('SELECT',NULL) k
      into :ttid_select,:ttinitst_select;


    taskid = NULL;
    taskpalletnum = -1;
    for
        select coalesce(k.numpallet,0),k.num,k.taskmethodid,k.waresid,k.amount,k.slotid,coalesce(tm.startstatus,:ttinitst_select),k.zoneid,k.productdate
          from k_tbltmp_select_docwares k
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
         order by k.numpallet ascending nulls last,k.num ascending nulls last
          into :numpallet,:numpos,:tmid_select,:waresid,:amount,:slotid,:status,:zoneid,:productdate
    do
    begin
        if (:taskpalletnum <> :numpallet and :taskpalletnum is NOT NULL and :numpallet is NOT NULL) then
        begin
            if (:taskid is NOT NULL) then
            begin
                select sum(ww.weight),sum(ww.capacity)
                  from wm_task_wares tw
                       left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
                 where tw.taskid = :taskid
                  into :WEIGHT,:CAPACITY;
            
                update wm_task t
                   set t.weight = :weight,t.capacity = :capacity
                 where t.taskid = :taskid;
            end

            taskpalletnum = :numpallet;

            if (:zoneid = 0) then zoneid = NULL;
            insert into wm_task(tasktypeid,taskmethodid,status,docid,num,zoneid)
            values (:ttid_select,:tmid_select,:status,:docid,:numpallet,:zoneid)
            returning taskid
            into :taskid;
        end

        price = NULL;
        select round(sum(cg.docsum)/sum(cg.amount),4)
          from cargo cg
         where cg.document = :docid
           and cg.waresid = :waresid
           and cg.cargo2id is NULL
           and cg.amount > 0.0001
          into :price;
        if (:price is null) then price = 0.000;

        insert into wm_task_wares(taskid,waresid,status,quantity,siteid,num,summa,plandatetime)
        values(:taskid,:waresid,iif(:tmid_select is NOT NULL,'0',NULL),:amount,:slotid,:numpos,:price,:productdate);
    end

    if (:taskid is NOT NULL) then
    begin
        select sum(ww.weight),sum(ww.capacity)
          from wm_task_wares tw
               left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
         where tw.taskid = :taskid
          into :WEIGHT,:CAPACITY;
    
        update wm_task t
           set t.weight = :weight,t.capacity = :capacity
         where t.taskid = :taskid;
    end

    for
        select t.taskid
          from wm_task t
         where t.docid = :docid
           and t.tasktypeid = :ttid_select
           and t.taskmethodid is NULL
          into :taskid
    do
    begin
        execute procedure wh_select_clientunfund(:taskid);
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE_PREVIEW (
    DOCID type of column DOCUMENT.DOCID)
returns (
    NUMPALLET type of R_NUMBER,
    ZONEID type of column SITEZONE.ZONEID,
    ZONENAME type of column SITEZONE.NAME,
    NUMPOS type of R_NUMBER,
    TMALGO type of column WM_TASKMETHOD.ALGORITHM,
    TMNAME type of column WM_TASKMETHOD.NAME,
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WQUANTITY type of R_DOUBLE,
    WWEIGHT type of R_DOUBLE,
    WCAPACITY type of R_DOUBLE,
    VUCODE type of column UNIT.SHORTNAME,
    VUFACTOR type of column WARESUNIT.FACTOR,
    MUCODE type of column UNIT.SHORTNAME,
    MUFACTOR type of column WARESUNIT.FACTOR,
    WSGCODE type of column K_WARES_SELGROUP.CODE,
    WSGNAME type of column K_WARES_SELGROUP.NAME,
    WSGWEIGHT type of R_DOUBLE,
    WSGCAPACITY type of R_DOUBLE,
    PRODUCTDATE type of column WARESLOT.PRODUCTDATE)
AS
begin
    execute procedure U3S_SALETOSELECT_CHK(:docid);
    execute procedure u3s_taskselect_create_prep(:docid);

    for
        select g.waresid,g.code,g.name,
               mwu.factor,mu.shortname,vwu.factor,vu.shortname,
               k.numpallet,k.num,k.amount,k.capacity,k.weight,
               tm.algorithm,tm.name,
               wsg.code,wsg.name,wsg.capacity,wsg.weight,
               k.zoneid,sz.name,k.productdate
          from k_tbltmp_select_docwares k
               left join gwares g
                    left join waresunit vwu
                         left join unit vu on vu.unitid = vwu.unitid
                      on vwu.waresunitid = g.viewunitid
                    left join waresunit mwu
                         left join unit mu on mu.unitid = mwu.unitid
                      on mwu.waresunitid = g.mainunitid
                 on g.waresid = k.waresid
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
               left join k_wares_selgroup wsg on wsg.id = k.selgroupid
               left join sitezone sz on sz.zoneid = k.zoneid
         order by k.numpallet ascending Nulls first,k.num ascending nulls first
          into :wid,:wcode,:wname,:mufactor,:mucode,:vufactor,:vucode,
               :numpallet,:numpos,:wquantity,:wcapacity,:wweight,
               :tmalgo,:tmname,:wsgcode,:wsgname,:wsgcapacity,:wsgweight,
               :zoneid,:zonename,:productdate
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELMANAGGA_DOCTOSELECT (
    ID type of column DOCUMENT.docid
)
returns(
    DOCID type of column DOCUMENT.docid,
    DSTAT type of column R_STATUS.code,
    DSTATNAME type of column R_STATUS.NAME
)
AS
begin
    UPDATE DOCUMENT D
       set d.status = 'g'
     where d.docid = :id and d.status = '1';

    select d.DOCID, d.STATUS, rs.name
      from document d
           left join r_status rs on rs.code = d.status and rs.statustype = 'O'
     where d.docid = :id
      into :docid, :dstat, :dstatname;

    suspend;
end^

SET TERM ; ^

