

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
declare variable tmAlgo type of column wm_taskmethod.algorithm;
declare variable QDIFF type of R_DOUBLE;
begin
    select tw.waresid,coalesce(tw.quantity,0.000),tw.siteid,tw.palletid,
           d.status,d.fromobj,d.docdate,tw.status,d.docid,tw.taskid,tw.wm_sessionid,
           tm.algorithm
      from wm_task_wares tw
           left join wm_task t
                left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                left join document d on d.docid=t.docid
             on t.taskid=tw.taskid
           left join pallet p
                left join site s
                     left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                  on s.siteid = p.siteid
             on p.palletid = tw.palletid
     where tw.taskwaresid = :twid
      into :wid,:twq,:siteid,:sitepalletid,:docstat,:objid,:docdate,:twstatus,:docid,:taskid,:wm_sessionid,:tmalgo;

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

    qdiff  = :twq - :q;
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
        
    if (:tmalgo = 'F' and :qdiff > 0.00001
        and exists(select *
                     from wareslot wl
                          left join wareslotitem wli
                               left join pallet p
                                    left join pallet_type pt on pt.id = p.ptypeid
                                    left join site s
                                         left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                                      on s.siteid = p.siteid
                                 on p.palletid = wli.palletid
                            on wli.wlotid = wl.wlotid
                    where wl.waresid = :wid
                      and wl.status = '1'
                      and wli.amount > 0.00001
                      and wli.palletid <> :sitepalletid
                      and pt.code in ('I', 'K')
                      and sp.canselect = '1'
    )) then
    begin
        insert into wm_task_wares(taskid, waresid, status, quantity)
        values(:taskid, :wid, '0', :qdiff);

        update wm_task_wares tw
           set tw.scanquant = :tlquantity,
               tw.quantity = :tlquantity,
               tw.status='2',
               tw.endtime=current_timestamp
         where tw.taskwaresid = :twid;
    end
    else
    begin
        update wm_task_wares tw
           set tw.scanquant = :tlquantity,
               tw.status='2',
               tw.endtime=current_timestamp
         where tw.taskwaresid = :twid;
    end
end^

SET TERM ; ^



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
declare variable tmAlgo type of column wm_taskmethod.algorithm;
declare variable QDIFF type of R_DOUBLE;
declare variable plandatetime type of column wm_task_wares.plandatetime;
begin
    select tw.waresid,coalesce(tw.quantity,0.000),tw.siteid,tw.palletid,
           d.status,d.fromobj,d.docdate,tw.status,d.docid,tw.taskid,tw.wm_sessionid,
           tm.algorithm, tw.plandatetime
      from wm_task_wares tw
           left join wm_task t
                left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                left join document d on d.docid=t.docid
             on t.taskid=tw.taskid
           left join pallet p
                left join site s
                     left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                  on s.siteid = p.siteid
             on p.palletid = tw.palletid
     where tw.taskwaresid = :twid
      into :wid,:twq,:siteid,:sitepalletid,:docstat,:objid,:docdate,:twstatus,:docid,:taskid,:wm_sessionid,
           :tmalgo, :plandatetime;

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

    qdiff  = :twq - :q;
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
        
    if (:tmalgo = 'F' and :qdiff > 0.00001
        and exists(select *
                     from wareslot wl
                          left join wareslotitem wli
                               left join pallet p
                                    left join pallet_type pt on pt.id = p.ptypeid
                                    left join site s
                                         left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                                      on s.siteid = p.siteid
                                 on p.palletid = wli.palletid
                            on wli.wlotid = wl.wlotid
                    where wl.waresid = :wid
                      and wl.status = '1'
                      and wli.amount > 0.00001
                      and wli.palletid <> :sitepalletid
                      and pt.code in ('I', 'K')
                      and sp.canselect = '1'
    )) then
    begin
        insert into wm_task_wares(taskid, waresid, status, quantity, plandatetime)
        values(:taskid, :wid, '0', :qdiff, :plandatetime);

        update wm_task_wares tw
           set tw.scanquant = :tlquantity,
               tw.quantity = :tlquantity,
               tw.status='2',
               tw.endtime=current_timestamp
         where tw.taskwaresid = :twid;
    end
    else
    begin
        update wm_task_wares tw
           set tw.scanquant = :tlquantity,
               tw.status='2',
               tw.endtime=current_timestamp
         where tw.taskwaresid = :twid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TSELECTDC_TASKF_NEXTWARES (
    TASKID type of R_ID)
returns (
    TWID type of R_ID,
    WID type of R_ID,
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    QO type of R_QUANTITY,
    TWSTAT type of R_STATUS,
    VUFACTOR type of R_MULTIPLE,
    VUCODE type of R_CODE,
    MUFACTOR type of R_MULTIPLE,
    MUCODE type of R_CODE,
    SITEID type of R_ID,
    SITENAME type of R_NAME,
    PALID type of R_ID,
    PALNUM type of R_SHORTNAME)
AS
declare variable objid type of r_id;
declare variable rowid type of r_id;
declare variable sprowid type of r_id;
declare variable directIndex type of r_bool;
declare variable num type of r_number;
declare variable siteoptionid_notfillpal type of column siteoption.code;
declare variable planproductdate type of column wareslot.productdate;
begin
    select first(1) tw.taskwaresid,tw.waresid,tw.status,tw.quantity,tw.siteid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.status = '1'
     order by tw.num ascending
      into :twid,:wid,:twstat,:qo,:siteid;

    if (:twid is NULL) then
    begin
        select d.fromobj
          from wm_task t
               left join document d on d.docid = t.docid
         where t.taskid = :taskid
          into :objid;

        select sp.sitespeciesid
          from sitespecies sp
         where sp.code = 'R'
          into :sprowid;

        execute procedure WH_SITEOPTIONID_NOTFILLPAL
         returning_values :siteoptionid_notfillpal;

        for
            select tw.taskwaresid,tw.waresid,tw.plandatetime
              from wm_task_wares tw
             where tw.taskid = :taskid
               and tw.status = '0'
              into :twid,:wid,:planproductdate
        do
        begin
            palid = NULL;
            siteid = NULL;
            rowid = NULL;

            select first(1) p.palletid,s.siteid
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join pallet_type pt on pt.id = p.ptypeid
                             left join site s
                                  left join site_options so on so.siteid = s.siteid
                                  left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                               on s.siteid = p.siteid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.objid = :objid
               and wl.waresid = :wid
               and wl.productdate = :planproductdate
               and wl.status = '1'
               and wli.amount > 0.0001
               and pt.code in ('FP', 'I')
               and coalesce(sp.calcrest,'0') = '1'
               and coalesce(sp.canselect,'0') = '1'
               and so.optionid = :siteoptionid_notfillpal
             order by wli.amount ascending
              into :palid,:siteid;

            if (:siteid is NOT NULL) then
            begin
                select k.sid
                  from k_site_parent(:siteid,:sprowid) k
                  into :rowid;

                insert into k_tbltmp_select_reformtaskwares(taskwaresid,palletid,siteid,rowid)
                values(:twid,:palid,:siteid,:rowid);
            end
        end

        if (:twid is NOT NULL) then
        begin
            twid = NULL;
            rowid = NULL;
            directIndex = NULL;
    
            select first(1) r.rowid,szi.directindex
              from (select distinct k.rowid as rowid
                      from k_tbltmp_select_reformtaskwares k) r
                   left join sitezone_items szi on szi.siteid = r.rowid
             order by r.rowid nulls last
              into :rowid,:directindex;
    
            if (coalesce(:directindex,'0')='0') then
                select first(1) k.taskwaresid,k.palletid,k.siteid
                  from k_tbltmp_select_reformtaskwares k
                       left join site s on s.siteid = k.siteid
                 where k.rowid = :rowid
                 order by s.name ascending
                  into :twid,:palid,:siteid;
            else
                select first(1) k.taskwaresid,k.palletid,k.siteid
                  from k_tbltmp_select_reformtaskwares k
                       left join site s on s.siteid = k.siteid
                 where k.rowid = :rowid
                 order by s.name descending
                  into :twid,:palid,:siteid;

            select max(tw.num)
              from wm_task_wares tw
             where tw.taskid = :taskid
               and tw.status = '2'
              into :num;

            if (:num is NULL) then num = 1;
            else num  = :num + 1;

            update wm_task_wares tw
               set tw.num = :num,tw.palletid = :palid, tw.siteid = :siteid
             where tw.taskwaresid = :twid;
        end
    end

    if (:twid is NOT NULL) then
    begin
      select g.code,g.name,vu.shortname,vwu.factor,mu.shortname,mwu.factor,
             p.palletid,p.number,s.siteid,s.name,tw.quantity
        from wm_task_wares tw
             left join gwares g
                  left join waresunit mwu
                       left join unit mu on mu.unitid = mwu.unitid
                    on mwu.waresunitid=g.mainunitid
                  left join waresunit vwu
                       left join unit vu on vu.unitid = vwu.unitid
                    on vwu.waresunitid=g.viewunitid
               on g.waresid = tw.waresid
             left join pallet p on p.palletid = tw.palletid
             left join site s on s.siteid = tw.siteid
       where tw.taskwaresid = :twid
        into :wcode,:wname,:vucode,:vufactor,:mucode,:mufactor,
             :palid,:palnum,:siteid,:sitename,:qo;

      suspend;
    end
    else
    begin
        for
          select tw.taskwaresid,tw.status,
                 g.code,g.name,vu.shortname,vwu.factor,mu.shortname,mwu.factor,tw.quantity
            from wm_task_wares tw
                 left join gwares g
                      left join waresunit mwu
                           left join unit mu on mu.unitid = mwu.unitid
                        on mwu.waresunitid=g.mainunitid
                      left join waresunit vwu
                           left join unit vu on vu.unitid = vwu.unitid
                        on vwu.waresunitid=g.viewunitid
                   on g.waresid = tw.waresid
           where tw.taskid = :taskid
             and tw.status = '0'
            into :twid,:twstat,:wcode,:wname,:vucode,:vufactor,:mucode,:mufactor,:qo
       do
        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SELECTF_TWPALLETS (
    TWID type of column WM_TASK_WARES.TASKWARESID)
returns (
    SID type of column SITE.SITEID,
    SNAME type of column SITE.NAME,
    PCNT type of R_SHORTNUMBER,
    PQ type of R_DOUBLE)
AS
declare variable wid type of column GWARES.waresid;
declare variable planproductdate type of column WARESLOT.productdate;
declare variable objid type of column OBJECT.objid;
begin
    select tw.waresid,tw.plandatetime, d.fromobj
      from wm_task_wares tw
           left join wm_task t
                left join document d on d.docid = t.docid
             on t.taskid = tw.taskid
     where tw.taskwaresid = :twid
      into :wid,:planproductdate,:objid;
    for
        select s.siteid, min(s.name), count(distinct p.palletid), sum(wli.amount)
          from wareslot wl
               left join wareslotitem wli
                    left join pallet p
                         left join pallet_type pt on pt.id = p.ptypeid
                         left join site s
                              left join site_options so on so.siteid = s.siteid
                              left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                           on s.siteid = p.siteid
                      on p.palletid = wli.palletid
                 on wli.wlotid = wl.wlotid
         where wl.objid = :objid
           and wl.waresid = :wid
           and wl.productdate = :planproductdate
           and wl.status = '1'
           and pt.code in ('FP', 'I')
           and wli.amount > 0.0001
           and coalesce(sp.calcrest,'0') = '1'
         group by s.siteid
         order by 4 ascending
          into :sid, :sname, :pcnt, :pq
    do
        suspend;
end^

SET TERM ; ^



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
declare variable tmAlgo type of column wm_taskmethod.algorithm;
declare variable QDIFF type of R_DOUBLE;
declare variable plandatetime type of column wm_task_wares.plandatetime;
begin
    select tw.waresid,coalesce(tw.quantity,0.000),tw.siteid,tw.palletid,
           d.status,d.fromobj,d.docdate,tw.status,d.docid,tw.taskid,tw.wm_sessionid,
           tm.algorithm, tw.plandatetime
      from wm_task_wares tw
           left join wm_task t
                left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                left join document d on d.docid=t.docid
             on t.taskid=tw.taskid
           left join pallet p
                left join site s
                     left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                  on s.siteid = p.siteid
             on p.palletid = tw.palletid
     where tw.taskwaresid = :twid
      into :wid,:twq,:siteid,:sitepalletid,:docstat,:objid,:docdate,:twstatus,:docid,:taskid,:wm_sessionid,
           :tmalgo, :plandatetime;

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

    qdiff  = :twq - :q;
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
        
    if (:tmalgo = 'F' and :qdiff > 0.00001
        /*and exists(select *
                     from wareslot wl
                          left join wareslotitem wli
                               left join pallet p
                                    left join pallet_type pt on pt.id = p.ptypeid
                                    left join site s
                                         left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                                      on s.siteid = p.siteid
                                 on p.palletid = wli.palletid
                            on wli.wlotid = wl.wlotid
                    where wl.waresid = :wid
                      and wl.status = '1'
                      and wli.amount > 0.00001
                      and wli.palletid <> :sitepalletid
                      and pt.code in ('I', 'K', 'FP')
                      and sp.canselect = '1')*/
    ) then
    begin
        insert into wm_task_wares(taskid, waresid, status, quantity, plandatetime)
        values(:taskid, :wid, '0', :qdiff, :plandatetime);

        update wm_task_wares tw
           set tw.scanquant = :tlquantity,
               tw.quantity = :tlquantity,
               tw.status='2',
               tw.endtime=current_timestamp
         where tw.taskwaresid = :twid;
    end
    else
    begin
        update wm_task_wares tw
           set tw.scanquant = :tlquantity,
               tw.status='2',
               tw.endtime=current_timestamp
         where tw.taskwaresid = :twid;
    end
end^

SET TERM ; ^



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
declare variable tmAlgo type of column wm_taskmethod.algorithm;
declare variable QDIFF type of R_DOUBLE;
declare variable plandatetime type of column wm_task_wares.plandatetime;
declare variable twsumma type of column wm_task_wares.summa;
begin
    select tw.waresid,coalesce(tw.quantity,0.000),tw.siteid,tw.palletid,
           d.status,d.fromobj,d.docdate,tw.status,d.docid,tw.taskid,tw.wm_sessionid,
           tm.algorithm, tw.plandatetime, tw.summa
      from wm_task_wares tw
           left join wm_task t
                left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                left join document d on d.docid=t.docid
             on t.taskid=tw.taskid
           left join pallet p
                left join site s
                     left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                  on s.siteid = p.siteid
             on p.palletid = tw.palletid
     where tw.taskwaresid = :twid
      into :wid,:twq,:siteid,:sitepalletid,:docstat,:objid,:docdate,:twstatus,:docid,:taskid,:wm_sessionid,
           :tmalgo, :plandatetime, :twsumma;

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

    qdiff  = :twq - :q;
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
        
    if (:tmalgo = 'F' and :qdiff > 0.00001
        /*and exists(select *
                     from wareslot wl
                          left join wareslotitem wli
                               left join pallet p
                                    left join pallet_type pt on pt.id = p.ptypeid
                                    left join site s
                                         left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                                      on s.siteid = p.siteid
                                 on p.palletid = wli.palletid
                            on wli.wlotid = wl.wlotid
                    where wl.waresid = :wid
                      and wl.status = '1'
                      and wli.amount > 0.00001
                      and wli.palletid <> :sitepalletid
                      and pt.code in ('I', 'K', 'FP')
                      and sp.canselect = '1')*/
    ) then
    begin
        insert into wm_task_wares(taskid, waresid, status, summa, quantity, plandatetime)
        values(:taskid, :wid, '0', :twsumma, :qdiff, :plandatetime);

        update wm_task_wares tw
           set tw.scanquant = :tlquantity,
               tw.quantity = :tlquantity,
               tw.status='2',
               tw.endtime=current_timestamp
         where tw.taskwaresid = :twid;
    end
    else
    begin
        update wm_task_wares tw
           set tw.scanquant = :tlquantity,
               tw.status='2',
               tw.endtime=current_timestamp
         where tw.taskwaresid = :twid;
    end
end^

SET TERM ; ^

