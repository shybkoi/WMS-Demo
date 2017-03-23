

SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_GETNEXTTASK (
    WMSID R_ID)
returns (
    TID type of R_ID,
    TNUMBER type of R_SHORTNAME,
    TSNAME type of R_NAME,
    DNUM type of DOCNUMBER,
    DDATE type of R_DATE,
    CLIENTNAME type of R_NAME,
    WHNAME type of R_NAME,
    TUID type of R_ID,
    TUNAME type of R_NAME,
    GOTOTASK type of R_FLAG)
AS
declare variable taskid_gateauto r_id;
declare variable taskid_select r_id;
declare variable taskid_loadauto r_id;
declare variable ttid_loadpallet r_id;
declare variable ttid_loadauto r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_cardocs r_id;
declare variable tbtid_loadselect r_id;
begin
    execute procedure wh_ttid_loadpallet returning_values :ttid_loadpallet;

    -- 1- ищем прив€занное задание погрузки поддона
    select t.taskid
      from wm_task t
     where t.wm_sessionid = :wmsid
       and t.status = '1'
       and t.tasktypeid = :ttid_loadpallet
      into :tid;

    -- 2 - ищем задание погрузки поддона из прив€занных заданий на погрузку документа
    if (:tid is NULL) then
    begin
        execute procedure wh_ttid_loadauto returning_values :ttid_loadauto;

        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'CARDOCS'
          into :tbtid_cardocs;
        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'LOADSELECT'
          into :tbtid_loadselect;

        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'DOCPALLETS'
          into :tbtid_docpallets;

        for
            select t.taskid
              from wm_task t
                   left join wh_taskbond tb
                        left join wm_task t1 on t1.taskid = tb.task1id
                     on tb.task2id = t.taskid and tb.taskbondtid = :tbtid_cardocs
             where t.wm_sessionid = :wmsid
               and t.status = '1'
               and t.tasktypeid = :ttid_loadauto
             order by t1.plandatetime ascending,
                      t1.begintime ascending,
                      t.priority ascending nulls last,
                      t.docid
              into :taskid_loadauto
        do
        begin
            select first(1) t.taskid
              from wh_taskbond tb
                   left join wm_task t
                        left join wh_taskbond tb2
                             left join wm_task t2 on t2.taskid = tb2.task2id
                          on tb2.task1id = t.taskid and tb2.taskbondtid = :tbtid_loadselect
                     on t.taskid = tb.task2id
             where tb.task1id = :taskid_loadauto
               and tb.taskbondtid = :tbtid_docpallets
               and t.status <> '2'
             order by t2.endtime descending nulls last, t.num ascending
               into :tid;

            if (:tid is NOT NULL) then
                break;
        end
    end

    -- ≈сли нашли - вернули
    if (:tid is NOT NULL) then
    begin
        select ti.TNUMBER,ti.TSNAME,ti.DNUM,ti.DDATE,
               ti.CLIENTNAME,ti.whname,
               ti.TUID, ti.TUNAME
          from wh_loadpalletdc_taskinfo(:tid) ti
          into :TNUMBER,:TSNAME,:DNUM,:DDATE,:CLIENTNAME,:WHNAME,:TUID,:TUNAME;

        gototask = '1';
        suspend; exit;
    end

    -- »наче ищем среди всех не прив€занных
    gototask = '0';
    for
        select t.taskid
          from WH_LOADAUTODC_LISTGATES(:wmsid) g
               left join wm_task t
                 on t.taskid = g.tid
         where g.tid is NOT NULL
         order by t.plandatetime ascending,t.begintime ascending
          into :taskid_gateauto
    do
    begin
        for
            select w.TID,w.TNUMBER,w.TSNAME,w.TID_SELECT,w.DNUM,w.DDATE,w.CLIENTNAME,w.WHNAME
              from wh_loadautodc_listpallets(:taskid_gateauto) w
                   left join wm_task t on t.taskid = w.tid_loadauto
             where w.TSTAT = '0'
               and w.DSTAT = '2'
               and (t.status = '0' or (t.status='1' and t.wm_sessionid is NULL))
             order by w.tpriority ascending,
                   w.tend_select descending nulls last,w.tnum_select ascending
              into :tid,:tnumber,:tsname,:taskid_select,:dnum,:ddate,:clientname,:whname
        do
        begin
            tuid = NULL;
            tuname = NULL;

            select tu.tuid,tu.name
              from wm_task_transunit ttu
                   left join wh_transport_unit tu on tu.tuid = ttu.tunitid
             where ttu.taskid = :taskid_select
              into :tuid,:tuname;

            suspend;
            exit;
        end
    end
end^

SET TERM ; ^

