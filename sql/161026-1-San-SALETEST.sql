

SET TERM ^ ;

create or alter procedure U3S_TSELECTDC_TASKF_NEXTWARES (
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
            select tw.taskwaresid,tw.waresid
              from wm_task_wares tw
             where tw.taskid = :taskid
               and tw.status = '0'
              into :twid,:wid
        do
        begin
            palid = NULL;
            siteid = NULL;
            rowid = NULL;

            select first(1) p.palletid,s.siteid
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join site s
                                  left join site_options so on so.siteid = s.siteid
                                  left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                               on s.siteid = p.siteid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.objid = :objid
               and wl.waresid = :wid
               and wl.status = '1'
               and wli.amount > 0.0001
               and coalesce(sp.calcrest,'0') = '1'
               and coalesce(sp.canselect,'0') = '1'
               and so.optionid = :siteoptionid_notfillpal
             order by wl.productdate ascending,s.name ascending
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
    select first(1) tw.taskwaresid,tw.waresid,tw.status,tw.quantity,tw.siteid,tw.plandatetime
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.status = '1'
     order by tw.num ascending
      into :twid,:wid,:twstat,:qo,:siteid,:planproductdate;

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
            select tw.taskwaresid,tw.waresid
              from wm_task_wares tw
             where tw.taskid = :taskid
               and tw.status = '0'
              into :twid,:wid
        do
        begin
            palid = NULL;
            siteid = NULL;
            rowid = NULL;

            select first(1) p.palletid,s.siteid
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
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

create procedure U3S_SELECTF_TWPALLETS (
    twid type of column wm_task_wares.taskwaresid
)
returns (
    sid type of column SITE.siteid,
    sname type of column SITE.name,
    pcnt type of R_SHORTNUMBER,
    pq type of R_DOUBLE
)
as
declare variable wid type of column GWARES.waresid;
declare variable planproductdate type of column WARESLOT.productdate;
declare variable objid type of column OBJECT.objid;
declare variable siteoptionid_notfillpal type of column SITEOPTION.id;
begin
    select tw.waresid,tw.plandatetime, d.fromobj
      from wm_task_wares tw
           left join wm_task t
                left join document d on d.docid = t.docid
             on t.taskid = tw.taskid
     where tw.taskwaresid = :twid
      into :wid,:planproductdate,:objid;
    
    execute procedure WH_SITEOPTIONID_NOTFILLPAL
     returning_values :siteoptionid_notfillpal;
    for
        select s.siteid, min(s.name), count(distinct p.palletid), sum(wli.amount)
          from wareslot wl
               left join wareslotitem wli
                    left join pallet p
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
           and coalesce(sp.calcrest,'0') = '1'
           and so.optionid = :siteoptionid_notfillpal
         group by s.siteid
         order by 4 ascending
          into :sid, :sname, :pcnt, :pq
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_DC_SELECT_TASKWARESINFO (
    TASKWARESID type of R_ID)
returns (
    TWID type of R_ID,
    TID type of R_ID,
    WID type of R_ID,
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    QO type of R_QUANTITY,
    QS type of R_QUANTITY,
    QREFILL type of R_QUANTITY,
    TWSTAT type of R_STATUS,
    VUID type of R_ID,
    VUFACTOR type of R_MULTIPLE,
    VUCODE type of R_CODE,
    MUID type of R_ID,
    MUFACTOR type of R_MULTIPLE,
    MUCODE type of R_CODE,
    SITEID type of R_ID,
    SITENAME type of R_NAME,
    TWPALLETID type of R_ID,
    TWPALLETNUM type of R_BARCODE,
    FS type of R_FLAG,
    TWPLANDT type of column wm_task_wares.plandatetime )
AS
begin
    for
        select first(1) tw.taskwaresid,tw.taskid,tw.waresid,tw.status,tw.quantity,tw.scanquant,tw.siteid,
               g.code,g.name,vwu.waresunitid,vu.shortname,vwu.factor,mwu.waresunitid,mu.shortname,mwu.factor,
               s.name,p.palletid,p.number, tw.plandatetime
          from wm_task_wares tw
               left join gwares g
                    left join waresunit vwu
                         left join unit vu on vu.unitid = vwu.unitid
                      on vwu.waresunitid = g.viewunitid
                    left join waresunit mwu
                         left join unit mu on mu.unitid = mwu.unitid
                      on mwu.waresunitid = g.mainunitid
                 on g.waresid = tw.waresid
               left join site s on s.siteid = tw.siteid
               left join pallet p on p.palletid = tw.palletid
         where tw.taskwaresid = :taskwaresid
          into :twid,:tid,:wid,:twstat,:qo,:qs,:siteid,
               :wcode,:wname,:vuid,:vucode,:vufactor,:muid,:mucode,:mufactor,:sitename,
               :twpalletid,:twpalletnum,:twplandt
    do
    begin
        qrefill = NULL;
        select first(1) tw.scanquant
          from wm_taskwares_bond b
               left join wm_taskwares_bondtype bt on bt.id = b.typeid
               left join wm_task_wares tw on tw.taskwaresid = b.id2
         where b.id1 = :twid
           and bt.code = 'REFILLSLOT'
           and tw.status = '2'
         order by tw.endtime descending
          into :qrefill;
        if (:qrefill is NULL) then qrefill = 0.000;

        select wso.selaccept
          from wm_task t
               left join document d
                    left join wares_select_options wso on wso.objid = d.fromobj
                 on d.docid = t.docid
         where t.taskid = :tid
           and wso.waresid = :wid
          into :fs;

        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SELECTF_TWPALLETS (
    twid type of column wm_task_wares.taskwaresid
)
returns (
    sid type of column SITE.siteid,
    sname type of column SITE.name,
    pcnt type of R_SHORTNUMBER,
    pq type of R_DOUBLE
)
as
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
           and coalesce(sp.calcrest,'0') = '1'
         group by s.siteid
         order by 4 ascending
          into :sid, :sname, :pcnt, :pq
    do
        suspend;
end^

SET TERM ; ^



update RDB$RELATION_FIELDS set
RDB$FIELD_SOURCE = 'R_DOUBLE'
where (RDB$FIELD_NAME = 'PALLETCOUNT') and
(RDB$RELATION_NAME = 'SITE')
;



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

