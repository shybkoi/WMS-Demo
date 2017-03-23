

ALTER TABLE WH_RESERVE_CHANGES
ADD AMOUNTBAD R_DOUBLE;



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_changes_bi for wh_reserve_changes
active before insert position 0
as
begin
  if (not exists(select *
                   from wh_reserve_objects o
                  where o.objid = new.objid)) then
    exception exc_wh_reserve '”казанного объекта нет в списке разрешенных дл€ резервировани€!';

  if (new.id is null) then
    new.id = gen_id(gen_wh_reserve_changes_id,1);

  if (new.datetime is NULL) then
    new.datetime = current_timestamp;

  if (new.amountbad is NULL) then
    new.amountbad = 0.000;

  if (new.amount + new.amountbad < 0.00001) then
   exception exc_wh_reserve '–езервируемое количество должно быть больше нул€!';
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_changes_ai0 for wh_reserve_changes
active after insert position 0
AS
declare variable reserveid type of column wh_reserve.id;
begin
    execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
     returning_values :reserveid;

    if (:reserveid is NULL) then
        insert into wh_reserve ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
        values ( new.waresid, new.productdate, new.amount, new.objid, new.amountbad);
    else
        update wh_reserve r
           set r.amount = r.amount + new.amount,
               r.amountbad = r.amountbad + new.amountbad
         where r.id = :reserveid;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_changes_au0 for wh_reserve_changes
active after update position 0
AS
declare variable reserveid type of column wh_reserve.id;
begin
    if (
        new.objid <> old.objid
        or
        new.waresid <> old.waresid
        or
        new.productdate <> old.productdate
    ) then
    begin
        execute procedure wh_reserve_getid(old.objid, old.waresid, old.productdate)
         returning_values :reserveid;

        if (:reserveid is NULL) then
            insert into wh_reserve ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
            values ( old.waresid, old.productdate, -old.amount, old.objid, -old.amountbad);
        else
            update wh_reserve r
               set r.amount = r.amount - old.amount,
                   r.amountbad = r.amountbad - old.amountbad
             where r.id = :reserveid;

        reserveid = NULL;
        execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
         returning_values :reserveid;

        if (:reserveid is NULL) then
            insert into wh_reserve ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
            values ( new.waresid, new.productdate, new.amount, new.objid, new.amountbad);
        else
            update wh_reserve r
               set r.amount = r.amount + new.amount,
                   r.amountbad = r.amountbad + new.amountbad
             where r.id = :reserveid;    
    end
    else if (abs(new.amount - old.amount) > 0.000001) then
    begin
        execute procedure wh_reserve_getid(new.objid, new.waresid, new.productdate)
         returning_values :reserveid;

        if (:reserveid is NULL) then
            insert into wh_reserve ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
            values ( new.waresid, new.productdate, new.amount - old.amount, new.objid, new.amountbad - old.amountbad);
        else
            update wh_reserve r
               set r.amount = r.amount + new.amount - old.amount,
                   r.amountbad = r.amountbad + new.amountbad - old.amountbad
             where r.id = :reserveid;    
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_changes_ad0 for wh_reserve_changes
active after delete position 0
AS
declare variable reserveid type of column wh_reserve.id;
begin
    execute procedure wh_reserve_getid(old.objid, old.waresid, old.productdate)
     returning_values :reserveid;

    if (:reserveid is NULL) then
        insert into wh_reserve ( WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
        values ( old.waresid, old.productdate, - old.amount, old.objid, -old.amountbad);
    else
        update wh_reserve r
           set r.amount = r.amount - old.amount,
               r.amountbad = r.amountbad - old.amountbad
         where r.id = :reserveid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_BUYRETURN_STATUSCHG (
    DOCID type of R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable TASKID type of R_ID;
declare variable ttid_comereturn type of R_ID;
declare variable TTINITST type of R_STATUS;
declare variable WARESID type of R_ID;
declare variable AMOUNT type of R_DOUBLE;
declare variable DOCSUM type of R_DOUBLE;
declare variable FROMOBJ type of R_ID;
declare variable OBJID type of R_ID;
declare variable doctid type of R_ID;
declare variable docdate type of R_DATE;
declare variable taskmethodid type of R_ID;
declare variable siteid type of R_ID;
begin
    select d.fromobj,d.toobj,d.doctype,d.docdate
      from document d
     where d.docid = :docid
      into :fromobj,:objid,:doctid,:docdate;

    if (:newstat='c') then
    begin
        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        select coalesce(tt.initstatus,'0') from wm_tasktype tt where tt.tasktypeid = :ttid_comereturn into :ttinitst;

        if (exists(select *
                     from wh_obj_info wh
                    where wh.objid = :objid
                      and wh.datestart >= :docdate
                      and wh.fromobjincome = :fromobj )) then
        begin
            select tm.methodid
              from wm_taskmethod tm
             where tm.tasktypeid = :ttid_comereturn
               and tm.algorithm = 'F'
              into :taskmethodid;

            if (:taskmethodid is NULL) then exception exc_k_wrongtasktype;

            select first(1) t.taskid
              from wm_task t
             where t.docid = :docid
               and t.tasktypeid = :ttid_comereturn
              into :taskid;

            if (:taskid is NULL) then
            begin
                siteid = NULL;
                select first(1) s.siteid
                  from sitespecies sp
                       left join site s on s.sitespeciesid = sp.sitespeciesid
                 where sp.code = 'E'
                  into :siteid;

                INSERT INTO wm_task(tasktypeid,status,docid,wm_sessionid,taskmethodid,siteid)
                VALUES(:ttid_comereturn,:ttinitst,:docid,null,:taskmethodid,:siteid)
                returning taskid
                into :taskid;
            end
            else
            begin
                update wm_task t
                   set t.taskmethodid = :taskmethodid,
                       t.wm_sessionid = NULL,
                       t.status = :ttinitst
                  where t.taskid = :taskid;
            end
        end
        else
        begin
            select first(1) szm.methodid
              from wm_taskmethod tm
                   left join sitezone_method szm
                        left join sitezone sz on sz.zoneid = szm.zoneid
                     on szm.methodid = tm.methodid
             where tm.tasktypeid = :ttid_comereturn
               and sz.objid = :objid
              into :taskmethodid;

            UPDATE or INSERT INTO wm_task(tasktypeid,status,docid,wm_sessionid,taskmethodid)
            VALUES(:ttid_comereturn,:ttinitst,:docid,null,:taskmethodid)
            matching (tasktypeid,docid)
            returning taskid
            into :taskid;
        end

        -- ≈сли повышение статуса
        if (exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.upcodes containing :newstat )) then
        begin
            for
                select cg.waresid,cg.amount,cg.docsum
                  from cargo cg
                 where cg.document = :docid
                   and cg.amount > 0.00001
                  into :waresid,:amount,:docsum
            do
                update or insert into wm_task_wares(taskid, waresid, successscan, summa, status, endtime)
                values (:taskid, :waresid, :amount, :docsum, '0', NULL)
                matching (taskid, waresid);
        end
        -- понижение статуса
        if (exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.downcodes containing :newstat))
        then
        begin
          update wm_task_wares tw
             set tw.status = '0'
           where tw.taskid = :taskid
                 and abs(coalesce(tw.successscan,0.0000)-coalesce(tw.quantity,0.00000)) > 0.000001;
        end

        execute procedure WH_CORE_SETDOCBYTASK(:docid,:ttid_comereturn);
    end
    else if (:newstat='w') then
    begin
        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        execute procedure WH_CORE_SETDOCBYTASK(:docid,:ttid_comereturn);
        execute procedure WH_COMERETURN_DOCSRENEW(:docid);

        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        if (not exists(select *
                         from wm_task t
                              left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                        where t.docid = :docid
                          and t.tasktypeid = :ttid_comereturn
                          and coalesce(tm.algorithm,'')='F' )) then
            execute procedure RBS_Q_CREATETASKEXPORT('»зменение статуса: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
             returning_values :taskid;
    end
    else if (:newstat = 'e') then
    begin
        update wareslotincomes wlin
           set wlin.status = '1'
         where wlin.docid = :docid and wlin.status = '0';


        insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
        select :docid, wl.waresid, wl.productdate, 0.000, d.throughobj, sum(tl.quantity)
          from wm_task t
               left join wm_task_wares tw
                    left join wm_task_lot tl
                         left join wareslot wl on wl.wlotid = wl.wlotid
                         left join wareslotincomes wlin
                              left join document d
                                on d.docid = wlin.docid
                           on wlin.id = tl.wlincomeid
                      on tl.taskwaresid = tw.taskwaresid
                 on tw.taskid = t.taskid
         where t.docid = :docid
         group by wl.productdate, wl.objid, wl.waresid, d.throughobj;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_BUYRETURN_STATUSCHG (
    DOCID type of R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable TASKID type of R_ID;
declare variable ttid_comereturn type of R_ID;
declare variable TTINITST type of R_STATUS;
declare variable WARESID type of R_ID;
declare variable AMOUNT type of R_DOUBLE;
declare variable DOCSUM type of R_DOUBLE;
declare variable FROMOBJ type of R_ID;
declare variable OBJID type of R_ID;
declare variable doctid type of R_ID;
declare variable docdate type of R_DATE;
declare variable taskmethodid type of R_ID;
declare variable siteid type of R_ID;
begin
    select d.fromobj,d.toobj,d.doctype,d.docdate
      from document d
     where d.docid = :docid
      into :fromobj,:objid,:doctid,:docdate;

    if (:newstat='c') then
    begin
        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        select coalesce(tt.initstatus,'0') from wm_tasktype tt where tt.tasktypeid = :ttid_comereturn into :ttinitst;

        if (exists(select *
                     from wh_obj_info wh
                    where wh.objid = :objid
                      and wh.datestart >= :docdate
                      and wh.fromobjincome = :fromobj )) then
        begin
            select tm.methodid
              from wm_taskmethod tm
             where tm.tasktypeid = :ttid_comereturn
               and tm.algorithm = 'F'
              into :taskmethodid;

            if (:taskmethodid is NULL) then exception exc_k_wrongtasktype;

            select first(1) t.taskid
              from wm_task t
             where t.docid = :docid
               and t.tasktypeid = :ttid_comereturn
              into :taskid;

            if (:taskid is NULL) then
            begin
                siteid = NULL;
                select first(1) s.siteid
                  from sitespecies sp
                       left join site s on s.sitespeciesid = sp.sitespeciesid
                 where sp.code = 'E'
                  into :siteid;

                INSERT INTO wm_task(tasktypeid,status,docid,wm_sessionid,taskmethodid,siteid)
                VALUES(:ttid_comereturn,:ttinitst,:docid,null,:taskmethodid,:siteid)
                returning taskid
                into :taskid;
            end
            else
            begin
                update wm_task t
                   set t.taskmethodid = :taskmethodid,
                       t.wm_sessionid = NULL,
                       t.status = :ttinitst
                  where t.taskid = :taskid;
            end
        end
        else
        begin
            select first(1) szm.methodid
              from wm_taskmethod tm
                   left join sitezone_method szm
                        left join sitezone sz on sz.zoneid = szm.zoneid
                     on szm.methodid = tm.methodid
             where tm.tasktypeid = :ttid_comereturn
               and sz.objid = :objid
              into :taskmethodid;

            UPDATE or INSERT INTO wm_task(tasktypeid,status,docid,wm_sessionid,taskmethodid)
            VALUES(:ttid_comereturn,:ttinitst,:docid,null,:taskmethodid)
            matching (tasktypeid,docid)
            returning taskid
            into :taskid;
        end

        -- ≈сли повышение статуса
        if (exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.upcodes containing :newstat )) then
        begin
            for
                select cg.waresid,cg.amount,cg.docsum
                  from cargo cg
                 where cg.document = :docid
                   and cg.amount > 0.00001
                  into :waresid,:amount,:docsum
            do
                update or insert into wm_task_wares(taskid, waresid, successscan, summa, status, endtime)
                values (:taskid, :waresid, :amount, :docsum, '0', NULL)
                matching (taskid, waresid);
        end
        -- понижение статуса
        if (exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.downcodes containing :newstat))
        then
        begin
          update wm_task_wares tw
             set tw.status = '0'
           where tw.taskid = :taskid
                 and abs(coalesce(tw.successscan,0.0000)-coalesce(tw.quantity,0.00000)) > 0.000001;
        end

        execute procedure WH_CORE_SETDOCBYTASK(:docid,:ttid_comereturn);
    end
    else if (:newstat='w') then
    begin
        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        execute procedure WH_CORE_SETDOCBYTASK(:docid,:ttid_comereturn);
        execute procedure WH_COMERETURN_DOCSRENEW(:docid);

        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        if (not exists(select *
                         from wm_task t
                              left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                        where t.docid = :docid
                          and t.tasktypeid = :ttid_comereturn
                          and coalesce(tm.algorithm,'')='F' )) then
            execute procedure RBS_Q_CREATETASKEXPORT('»зменение статуса: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
             returning_values :taskid;
    end
    else if (:newstat = 'e') then
    begin
        update wareslotincomes wlin
           set wlin.status = '1'
         where wlin.docid = :docid and wlin.status = '0';


        insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
        select :docid, wl.waresid, wl.productdate, 0.000, d.throughobj, sum(tl.quantity)
          from wm_task t
               left join wm_task_wares tw
                    left join wm_task_lot tl
                         left join wareslot wl on wl.wlotid = wl.wlotid
                         left join wareslotincomes wlin
                              left join document d
                                on d.docid = wlin.docid
                           on wlin.id = tl.wlincomeid
                      on tl.taskwaresid = tw.taskwaresid
                 on tw.taskid = t.taskid
         where t.docid = :docid
         group by wl.productdate, wl.objid, wl.waresid, d.throughobj
        having abs(sum(tl.quantity)) > 0.0001;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_BUYRETURN_STATUSCHG (
    DOCID type of R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable TASKID type of R_ID;
declare variable ttid_comereturn type of R_ID;
declare variable TTINITST type of R_STATUS;
declare variable WARESID type of R_ID;
declare variable AMOUNT type of R_DOUBLE;
declare variable DOCSUM type of R_DOUBLE;
declare variable FROMOBJ type of R_ID;
declare variable OBJID type of R_ID;
declare variable doctid type of R_ID;
declare variable docdate type of R_DATE;
declare variable taskmethodid type of R_ID;
declare variable siteid type of R_ID;
begin
    select d.fromobj,d.toobj,d.doctype,d.docdate
      from document d
     where d.docid = :docid
      into :fromobj,:objid,:doctid,:docdate;

    if (:newstat='c') then
    begin
        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        select coalesce(tt.initstatus,'0') from wm_tasktype tt where tt.tasktypeid = :ttid_comereturn into :ttinitst;

        if (exists(select *
                     from wh_obj_info wh
                    where wh.objid = :objid
                      and wh.datestart >= :docdate
                      and wh.fromobjincome = :fromobj )) then
        begin
            select tm.methodid
              from wm_taskmethod tm
             where tm.tasktypeid = :ttid_comereturn
               and tm.algorithm = 'F'
              into :taskmethodid;

            if (:taskmethodid is NULL) then exception exc_k_wrongtasktype;

            select first(1) t.taskid
              from wm_task t
             where t.docid = :docid
               and t.tasktypeid = :ttid_comereturn
              into :taskid;

            if (:taskid is NULL) then
            begin
                siteid = NULL;
                select first(1) s.siteid
                  from sitespecies sp
                       left join site s on s.sitespeciesid = sp.sitespeciesid
                 where sp.code = 'E'
                  into :siteid;

                INSERT INTO wm_task(tasktypeid,status,docid,wm_sessionid,taskmethodid,siteid)
                VALUES(:ttid_comereturn,:ttinitst,:docid,null,:taskmethodid,:siteid)
                returning taskid
                into :taskid;
            end
            else
            begin
                update wm_task t
                   set t.taskmethodid = :taskmethodid,
                       t.wm_sessionid = NULL,
                       t.status = :ttinitst
                  where t.taskid = :taskid;
            end
        end
        else
        begin
            select first(1) szm.methodid
              from wm_taskmethod tm
                   left join sitezone_method szm
                        left join sitezone sz on sz.zoneid = szm.zoneid
                     on szm.methodid = tm.methodid
             where tm.tasktypeid = :ttid_comereturn
               and sz.objid = :objid
              into :taskmethodid;

            UPDATE or INSERT INTO wm_task(tasktypeid,status,docid,wm_sessionid,taskmethodid)
            VALUES(:ttid_comereturn,:ttinitst,:docid,null,:taskmethodid)
            matching (tasktypeid,docid)
            returning taskid
            into :taskid;
        end

        -- ≈сли повышение статуса
        if (exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.upcodes containing :newstat )) then
        begin
            for
                select cg.waresid,cg.amount,cg.docsum
                  from cargo cg
                 where cg.document = :docid
                   and cg.amount > 0.00001
                  into :waresid,:amount,:docsum
            do
                update or insert into wm_task_wares(taskid, waresid, successscan, summa, status, endtime)
                values (:taskid, :waresid, :amount, :docsum, '0', NULL)
                matching (taskid, waresid);
        end
        -- понижение статуса
        if (exists(select *
                     from doctypestatus dts
                    where dts.doctid = :doctid
                      and dts.code = :oldstat
                      and dts.downcodes containing :newstat))
        then
        begin
          update wm_task_wares tw
             set tw.status = '0'
           where tw.taskid = :taskid
                 and abs(coalesce(tw.successscan,0.0000)-coalesce(tw.quantity,0.00000)) > 0.000001;
        end

        execute procedure WH_CORE_SETDOCBYTASK(:docid,:ttid_comereturn);
    end
    else if (:newstat='w') then
    begin
        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        execute procedure WH_CORE_SETDOCBYTASK(:docid,:ttid_comereturn);
        execute procedure WH_COMERETURN_DOCSRENEW(:docid);

        execute procedure wh_ttid_comereturn returning_values :ttid_comereturn;
        if (not exists(select *
                         from wm_task t
                              left join wm_taskmethod tm on tm.methodid = t.taskmethodid
                        where t.docid = :docid
                          and t.tasktypeid = :ttid_comereturn
                          and coalesce(tm.algorithm,'')='F' )) then
            execute procedure RBS_Q_CREATETASKEXPORT('»зменение статуса: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
             returning_values :taskid;
    end
    else if (:newstat = 'e') then
    begin
        update wareslotincomes wlin
           set wlin.status = '1'
         where wlin.docid = :docid and wlin.status = '0';


        insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, AMOUNTBAD)
        select :docid, wl.waresid, wl.productdate, 0.000, d.throughobj, sum(tl.quantity)
          from wm_task t
               left join wm_task_wares tw
                    left join wm_task_lot tl
                         left join wareslot wl on wl.wlotid = tl.wlotid
                         left join wareslotincomes wlin
                              left join document d
                                on d.docid = wlin.docid
                           on wlin.id = tl.wlincomeid
                      on tl.taskwaresid = tw.taskwaresid
                 on tw.taskid = t.taskid
         where t.docid = :docid
         group by wl.productdate, wl.objid, wl.waresid, d.throughobj
        having abs(sum(tl.quantity)) > 0.0001;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wh_reserve_bi for wh_reserve
active before insert position 0
as
declare variable wliamount type of column wareslotitem.amount;
declare variable wliamount_bad type of column wareslotitem.amount;
declare variable ramount type of column wh_reserve.amount;
declare variable ramount_bad type of column wh_reserve.amountbad;
declare variable ptypeid_cr type of column pallet_type.id;
begin
    if (new.amountbad is NULL) then
        new.amountbad = 0.000;

    if (new.amount + new.amountbad < 0.0001) then
        exception exc_wh_reserve '–езервировать можно только количество товара большее нул€!';

    if (new.amount < -0.0001 or new.amountbad < -0.0001 ) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать отрицательное количество!';


    if (new.amountsale is NULL) then
        new.amountsale = 0.000;
    
    if (new.amount - new.amountsale < -0.0000001) then
        exception exc_wh_reserve 'Ќельз€ зарезервировать меньше резерва под продажу!';

    select w.id
      from WH_PALTYPEID_COMERETURN w
      into :ptypeid_cr;

    select sum(
            case
                when p.ptypeid = :ptypeid_cr then 0.000
                else wli.amount
            end
           ),
           sum(
            case
                when p.ptypeid = :ptypeid_cr then wli.amount
                else 0.000
            end
           )
      from wareslot wl
           left join wareslotitem wli
                left join pallet p
                  on p.palletid = wli.palletid
             on wli.wlotid = wl.wlotid
     where wl.waresid = new.waresid
       and wl.productdate = new.productdate
       and wl.status = '1'
      into :wliamount, :wliamount_bad;
    if (:wliamount is NULL) then
        wliamount = 0.000;
    if (:wliamount_bad is NULL) then
        wliamount_bad = 0.000;
    
    select sum(r.amount), sum(r.amountbad)
      from wh_reserve r
     where r.waresid = new.waresid
       and r.productdate = new.productdate
      into :ramount, :ramount_bad;
    if (:ramount is NULL) then
        ramount = 0.000;
    if (:ramount_bad is NULL) then
        ramount_bad = 0.000;

    if (:wliamount - :ramount - new.amount < -0.000001) then
      exception exc_wh_reserve 'Ќельз€ зарезервировать больше остатка!';
    
    if (:wliamount_bad - :ramount_bad - new.amountbad < -0.000001) then
      exception exc_wh_reserve 'Ќельз€ зарезервировать больше остатка!';

    new.amountfree = new.amount - new.amountsale;

    if (new.id is null) then
      new.id = gen_id(gen_wh_reserve_id,1);
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_LABERPRINT_LOCWARES(
    CODE type of R_CODE,
    NAME type of R_NAME,
    BCODE type of R_BARCODE
)
returns (
    WID type of R_ID,
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    WUSEBYDATE type of R_SHORTNUMBER,
    WUBTNAME type of R_NAME,
    FACTOR type of R_MULTIPLE,
    SHORTNAME type of R_CODE,
    WGNAME type of R_NAME)
AS
 declare variable palletunitid type of r_id;
begin
  select wc.palletunitid
    from wm_config wc
    into :palletunitid;

  if (:code is NOT NULL) then
  begin
    for
       select g.waresid, g.code, g.name, g.usebydate, rc.name,
              wu.factor, u.shortname, wg.name
         from gwares g
              left join waresunit wu on g.waresid = wu.waresid and wu.unitid = :palletunitid
              left join unit u on u.unitid = wu.unitid
              left join waresgroup wg on wg.waresgrid = g.waresgroup
              left join r_choice rc on rc.chtype = 'P' and rc.code = g.ubdtype
        where g.code = :code
          and g.status = '1'
         into :wid, :wcode, :wname, :wusebydate, :wubtname,
              :factor, :shortname, :wgname
    do
      suspend;
  end
  else if (:name is NOT NULL) then
  begin
    for
       select g.waresid, g.code, g.name, g.usebydate, rc.name,
              wu.factor, u.shortname, wg.name
         from gwares g
              left join waresunit wu on g.waresid = wu.waresid and wu.unitid = :palletunitid
              left join unit u on u.unitid = wu.unitid
              left join waresgroup wg on wg.waresgrid = g.waresgroup
              left join r_choice rc on rc.chtype = 'P' and rc.code = g.ubdtype
        where g.name containing :name
          and g.status = '1'
         into :wid, :wcode, :wname, :wusebydate, :wubtname,
              :factor, :shortname, :wgname
    do
      suspend;
  end
  else if (:bcode is NOT NULL) then
  begin
    for
       select g.waresid, g.code, g.name, g.usebydate, rc.name,
              wu.factor, u.shortname, wg.name
         from waresbarcode wbc
              left join waresunit wuw
                   left join gwares g
                        left join waresunit wu
                             left join unit u on u.unitid = wu.unitid
                          on g.waresid = wu.waresid and wu.unitid = :palletunitid
                        left join waresgroup wg on wg.waresgrid = g.waresgroup
                        left join r_choice rc on rc.chtype = 'P' and rc.code = g.ubdtype
                     on g.waresid = wuw.waresid
                on wuw.waresunitid = wbc.waresunitid
        where wbc.barcode = :bcode
          and g.status = '1'
         into :wid, :wcode, :wname, :wusebydate, :wubtname,
              :factor, :shortname, :wgname
    do
      suspend;

  end
end^

SET TERM ; ^

