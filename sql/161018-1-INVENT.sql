

SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDINCOME_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable docstat type of column document.status;
declare variable docbondid type of column document.docid;
declare variable docnum type of column document.number;
begin
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
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_INVENT_GETTASK (
    DBEG type of R_DATE,
    DEND type of R_DATE,
    ZONEID type of R_ID)
returns (
    TASKID type of R_ID,
    STATUS type of R_STATUS,
    NUMBER type of R_NUMBER,
    PLANDATE type of R_DATE,
    TMNAME type of R_NAME,
    TMALGORITHM type of R_FLAG,
    EMPLNAME type of R_FULLNAME)
as
declare variable TASKTYPEID type of R_ID;
declare variable TASKBONDTID type of R_ID;
declare variable OBJID type of R_ID;
begin
  select tt.ttid
    from k_tasktype_by_code('INVENT','1') tt
    into :tasktypeid;

  select sz.objid
    from sitezone sz
   where sz.zoneid = :zoneid
    into :objid;

  for
    select t.taskid,t.status,t.number,t.plandatetime,
           tm.name, tm.algorithm,
           gon.fullname
      from wm_task t
           left join wm_taskmethod tm on t.taskmethodid = tm.methodid
           left join wm_session s
                left join getobjectname(s.objid,'03') gon on 1=1
             on s.sessionid = t.wm_sessionid
     where t.zoneid = :zoneid
           and t.tasktypeid = :tasktypeid
           and t.infoid = :objid
           and t.plandatetime between :dbeg and :dend
     into :taskid,:status,:number,:plandate,
          :tmname, :tmalgorithm,
          :emplname
      do
        suspend;

end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_WH_INVENT_GETTMETHOD
returns (
    METHODID type of R_ID,
    NAME type of R_NAME)
as
declare variable TTID type of R_ID;
begin
  select tt.ttid
    from k_tasktype_by_code('INVENT','1') tt
    into :ttid;

  for
    select tm.methodid, tm.name
      from wm_taskmethod tm
     where tm.tasktypeid = :ttid
      into :methodid, :name
        do

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_INVENT_ADDTASK (
    PLANDATE type of R_DATE,
    ZONEID type of R_ID,
    METHODID type of R_ID,
    WMSESID type of R_ID)
returns (
    TASKID type of R_ID)
as
declare variable TTID type of R_ID;
declare variable ALGORITHM type of R_FLAG;
declare variable OBJID type of R_ID;
declare variable INITSTATUS type of R_STATUS;
begin
  select tt.ttid , tt.ttinitst
    from k_tasktype_by_code('INVENT','1') tt
    into :ttid, :initstatus;

  select coalesce(tm.algorithm,'')
    from wm_taskmethod tm
   where tm.methodid = :methodid
    into :algorithm;

  if (:algorithm = 'A') then -- общая
  begin
    --exception exc_k_common 'Метод не доступен!';

    select sz.objid
      from sitezone sz
     where sz.zoneid = :zoneid
      into :objid;

    insert into wm_task(tasktypeid,taskmethodid,status,plandatetime,wm_sessionid,zoneid, infoid)
    values(:ttid,:methodid,:initstatus,:plandate,:wmsesid,:zoneid,:objid)
    returning taskid
    into :taskid;

  end
  else if (:algorithm = 'L') then  -- локальная
  begin
    select sz.objid
      from sitezone sz
     where sz.zoneid = :zoneid
      into :objid;

    insert into wm_task(tasktypeid,taskmethodid,status,plandatetime,wm_sessionid,zoneid, infoid)
    values(:ttid,:methodid,:initstatus,:plandate,:wmsesid,:zoneid,:objid)
    returning taskid
    into :taskid;
  end
  else
    exception exc_k_common 'Метод не обрабатывается!';


  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_WH_INVENT_TASKINFO (
    TID type of R_ID)
returns (
    TASKID type of R_ID,
    STATUS type of R_STATUS,
    NUMBER type of R_NUMBER,
    PLANDATE type of R_DATE,
    TMNAME type of R_NAME,
    TMALGORITHM type of R_FLAG,
    EMPLNAME type of R_FULLNAME,
    OBJNAME type of R_FULLNAME,
    OBJID type of R_ID)
as
begin
  select t.taskid,t.status,t.number,t.plandatetime,
         tm.name, tm.algorithm,
         gon.fullname, obj.fullname, t.infoid
    from wm_task t
         left join wm_taskmethod tm on t.taskmethodid = tm.methodid
         left join wm_session s
              left join getobjectname(s.objid,'03') gon on 1=1
           on s.sessionid = t.wm_sessionid
         left join getobjectname(t.infoid,'null') obj on 1=1
   where t.taskid = :tid
   into :taskid,:status,:number,:plandate,
        :tmname, :tmalgorithm,
        :emplname, :objname, :objid;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_WH_INVENT_GETWARES (
    TASKID type of R_ID)
returns (
    TASKWARESID type of R_ID,
    WARESID type of R_ID,
    CODE type of R_CODE,
    NAME type of R_NAME,
    WEIGHTING type of NUMBER,
    QUANTITY type of R_DOUBLE,
    SCANCOUNT type of R_DOUBLE,
    SUCCESSSCAN type of R_DOUBLE,
    SCANQUANT type of R_DOUBLE,
    LASTDATE type of R_DATETIME,
    STATUS type of R_STATUS,
    REST type of R_QUANTITY,
    INVENTQUANT type of R_QUANTITY,
    WGID type of R_ID,
    WGNAME type of R_NAME,
    WGSELCODE type of R_CODE,
    WGSELNAME type of R_NAME,
    DOCQUANT type of R_QUANTITY)
as
declare variable TRASHPALLETID type of R_ID;
declare variable TRASHSITEID type of R_ID;
declare variable OBJID type of R_ID;
begin

  select t.infoid
    from wm_task t
   where t.taskid = :taskid
    into :objid;

  select k.pid,k.sid
    from k_wh_get_trash(:objid) k
    into :trashpalletid,:trashsiteid;

  for
    select tw.taskwaresid,tw.waresid,w.code,w.name, wg.waresgrid, wg.name,
           tw.quantity,tw.scancount,tw.successscan,tw.scanquant,
           tw.lastdate,tw.status,
           coalesce(wlr.rest,0.000),
           coalesce(wr.famount, 0.000),
           wsg.code, wsg.name
      from wm_task_wares tw
           left join gwares w
                left join waresgroup wg on wg.waresgrid = w.waresgroup
                left join k_wares_selgroup wsg on w.selgroup = wsg.id
                left join waresrest wr on wr.waresunitid = w.mainunitid and wr.objid = :objid
             on tw.waresid = w.waresid
           left join wareslotrest wlr on wlr.waresid = tw.waresid and wlr.objid = :objid
     where tw.taskid = :taskid
           and tw.waresid is not null
     order by w.code asc
      into :taskwaresid,:waresid,:code,:name, :wgid, :wgname,
           :quantity,:scancount,:successscan,:scanquant,
           :lastdate,:status,
           :rest,
           :docquant,
           :wgselcode, :wgselname
  do
  begin
    select sum(tl.quantity)
      from wm_task_lot tl
     where tl.taskwaresid = :taskwaresid
           and tl.palletid <> :trashpalletid
      into :inventquant;

    suspend;
  end 


end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_RESTCONTROL_REST_DC (
    OBJID type of column OBJECT.OBJID,
    ZONEID type of column SITEZONE.ZONEID = null,
    SITEID type of column SITE.SITEID = null)
returns (
    WID type of column GWARES.WARESID,
    WNAME type of column GWARES.NAME,
    WCODE type of column GWARES.CODE,
    MUCODE type of column UNIT.SHORTNAME,
    VUCODE type of column UNIT.SHORTNAME,
    MUFACTOR type of column WARESUNIT.FACTOR,
    VUFACTOR type of column WARESUNIT.FACTOR,
    QB type of column WARESLOTITEM.AMOUNT,
    QS type of column WARESLOTITEM.AMOUNT,
    QR type of column WARESLOTITEM.AMOUNT,
    QT type of column WARESLOTITEM.AMOUNT,
    QE type of column WARESLOTITEM.AMOUNT,
    QN type of column WARESLOTITEM.AMOUNT,
    Q type of column WARESLOTITEM.AMOUNT,
    QGOOD type of column WARESLOTITEM.AMOUNT,
    QBAD type of column WARESLOTITEM.AMOUNT,
    WGID type of R_ID,
    SGID type of R_ID
)
AS
declare WINFO cursor for (
    select G.CODE, G.NAME, VWU.FACTOR, VU.SHORTNAME, MWU.FACTOR, MU.SHORTNAME, G.WARESGROUP, G.SELGROUP
    from GWARES G
    left join WARESUNIT VWU
    left join UNIT VU on VU.UNITID = VWU.UNITID on VWU.WARESUNITID = G.VIEWUNITID
    left join WARESUNIT MWU
    left join UNIT MU on MU.UNITID = MWU.UNITID on MWU.WARESUNITID = G.MAINUNITID
    where G.WARESID = :WID);
begin
    if (:siteid is NULL) then
    begin
        if (:zoneid is NULL or :zoneid=0) then
        begin
          for
            select wl.waresid,
                   sum(case sp.code when 'B' then wli.amount else 0.000 end),
                   sum(case sp.code when 'S' then wli.amount else 0.000 end),
                   sum(case when sp.code starting 'BUYRET' then wli.amount else 0.000 end),
                   sum(case sp.code when 'E' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype <> '1' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype = '1' then wli.amount else 0.000 end),
                   sum(case sp.calcrest when '1' then wli.amount else 0.0000 end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'GOOD' then wli.amount
                        else 0.0000
                   end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'BAD' then wli.amount
                        else 0.0000
                   end)
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join pallet_feature pf on pf.id = p.featureid
                             left join site s
                                  left join sitespecies sp
                                    on sp.sitespeciesid = s.sitespeciesid
                               on s.siteid = p.siteid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.objid = :objid
               and wl.status = '1'
             group by wl.waresid
              into :wid, :qb, :qs, :qr, :qe, :qt, :qn, :q, :qgood, :qbad
           do
           begin
                OPEN WINFO;
                FETCH WINFO INTO :wcode,:wname,:vufactor,:vucode,:mufactor,:mucode,:wgid,:sgid;
                CLOSE WINFO;
    
                suspend;
           end
        end
        else
        begin
          for
            select wl.waresid,
                   sum(case sp.code when 'B' then wli.amount else 0.000 end),
                   sum(case sp.code when 'S' then wli.amount else 0.000 end),
                   sum(case when sp.code starting 'BUYRET' then wli.amount else 0.000 end),
                   sum(case sp.code when 'E' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype <> '1' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype = '1' then wli.amount else 0.000 end),
                   sum(case sp.calcrest when '1' then wli.amount else 0.0000 end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'GOOD' then wli.amount
                        else 0.0000
                   end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'BAD' then wli.amount
                        else 0.0000
                   end)
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join pallet_feature pf on pf.id = p.featureid
                             left join site s
                                  left join sitespecies sp
                                    on sp.sitespeciesid = s.sitespeciesid
                               on s.siteid = p.siteid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.objid = :objid
               and wl.status = '1'
               and wl.zoneid = :zoneid
             group by wl.waresid
              into :wid, :qb, :qs, :qr, :qe, :qt, :qn, :q, :qgood, :qbad
           do
           begin
                OPEN WINFO;
                FETCH WINFO INTO :wcode,:wname,:vufactor,:vucode,:mufactor,:mucode,:wgid,:sgid;
                CLOSE WINFO;
    
                suspend;
           end
        end
    end
    else
    begin
         insert into wh_tbltmp_ids(id)
         with recursive tmpsite as (
             select s.siteid
               from site s
              where s.siteid = :siteid
              union all
             select s.siteid
               from tmpsite t
                    join site s on s.higher = t.siteid
         )
         select t.siteid
           from tmpsite t;

        if (:zoneid is NULL or :zoneid=0) then
        begin
          for
            select wl.waresid,
                   sum(case sp.code when 'B' then wli.amount else 0.000 end),
                   sum(case sp.code when 'S' then wli.amount else 0.000 end),
                   sum(case when sp.code starting 'BUYRET' then wli.amount else 0.000 end),
                   sum(case sp.code when 'E' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype <> '1' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype = '1' then wli.amount else 0.000 end),
                   sum(case sp.calcrest when '1' then wli.amount else 0.0000 end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'GOOD' then wli.amount
                        else 0.0000
                   end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'BAD' then wli.amount
                        else 0.0000
                   end)
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join wh_tbltmp_ids i on i.id = p.siteid
                             left join pallet_feature pf on pf.id = p.featureid
                             left join site s
                                  left join sitespecies sp
                                    on sp.sitespeciesid = s.sitespeciesid
                               on s.siteid = p.siteid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.objid = :objid
               and wl.status = '1'
               and i.id is NOT NULL
             group by wl.waresid
              into :wid, :qb, :qs, :qr, :qe, :qt, :qn, :q, :qgood, :qbad
           do
           begin
                OPEN WINFO;
                FETCH WINFO INTO :wcode,:wname,:vufactor,:vucode,:mufactor,:mucode,:wgid,:sgid;
                CLOSE WINFO;
    
                suspend;
           end
        end
        else
        begin
          for
            select wl.waresid,
                   sum(case sp.code when 'B' then wli.amount else 0.000 end),
                   sum(case sp.code when 'S' then wli.amount else 0.000 end),
                   sum(case when sp.code starting 'BUYRET' then wli.amount else 0.000 end),
                   sum(case sp.code when 'E' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype <> '1' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype = '1' then wli.amount else 0.000 end),
                   sum(case sp.calcrest when '1' then wli.amount else 0.0000 end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'GOOD' then wli.amount
                        else 0.0000
                   end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'BAD' then wli.amount
                        else 0.0000
                   end)
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join wh_tbltmp_ids i on i.id = p.siteid
                             left join pallet_feature pf on pf.id = p.featureid
                             left join site s
                                  left join sitespecies sp
                                    on sp.sitespeciesid = s.sitespeciesid
                               on s.siteid = p.siteid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.objid = :objid
               and wl.status = '1'
               and wl.zoneid = :zoneid
               and i.id is NOT NULL
             group by wl.waresid
              into :wid, :qb, :qs, :qr, :qe, :qt, :qn, :q, :qgood, :qbad
           do
           begin
                OPEN WINFO;
                FETCH WINFO INTO :wcode,:wname,:vufactor,:vucode,:mufactor,:mucode,:wgid,:sgid;
                CLOSE WINFO;
    
                suspend;
           end
        end
    end
end^

SET TERM ; ^



ALTER TABLE SITE
ADD CALCREST R_FLAG;



SET TERM ^ ;

CREATE OR ALTER procedure K_RESTCONTROL_REST_DC (
    OBJID type of column OBJECT.OBJID,
    ZONEID type of column SITEZONE.ZONEID = null,
    SITEID type of column SITE.SITEID = null)
returns (
    WID type of column GWARES.WARESID,
    WNAME type of column GWARES.NAME,
    WCODE type of column GWARES.CODE,
    MUCODE type of column UNIT.SHORTNAME,
    VUCODE type of column UNIT.SHORTNAME,
    MUFACTOR type of column WARESUNIT.FACTOR,
    VUFACTOR type of column WARESUNIT.FACTOR,
    QB type of column WARESLOTITEM.AMOUNT,
    QS type of column WARESLOTITEM.AMOUNT,
    QR type of column WARESLOTITEM.AMOUNT,
    QT type of column WARESLOTITEM.AMOUNT,
    QE type of column WARESLOTITEM.AMOUNT,
    QN type of column WARESLOTITEM.AMOUNT,
    QI type of R_QUANTITY,
    QU type of R_QUANTITY,
    QP type of R_QUANTITY,
    Q type of R_QUANTITY,
    DATETIME type of R_DATETIME,
    QGOOD type of column WARESLOTITEM.AMOUNT,
    QBAD type of column WARESLOTITEM.AMOUNT,
    WGID type of R_ID,
    SGID type of R_ID
)
AS
declare WINFO cursor for (
    select G.CODE, G.NAME, VWU.FACTOR, VU.SHORTNAME, MWU.FACTOR, MU.SHORTNAME, G.WARESGROUP, G.SELGROUP
    from GWARES G
    left join WARESUNIT VWU
    left join UNIT VU on VU.UNITID = VWU.UNITID on VWU.WARESUNITID = G.VIEWUNITID
    left join WARESUNIT MWU
    left join UNIT MU on MU.UNITID = MWU.UNITID on MWU.WARESUNITID = G.MAINUNITID
    where G.WARESID = :WID);
begin
    datetime = current_timestamp;
    if (:siteid is NULL) then
    begin
        if (:zoneid is NULL or :zoneid=0) then
        begin
          for
            select wl.waresid,
                   sum(case sp.code when 'B' then wli.amount else 0.000 end),
                   sum(case sp.code when 'S' then wli.amount else 0.000 end),
                   sum(case when sp.code starting 'BUYRET' then wli.amount else 0.000 end),
                   sum(case sp.code when 'E' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype <> '1' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype = '1' then wli.amount else 0.000 end),
                   sum(iif(coalesce(s.calcrest,sp.calcrest)='i', wli.amount, 0.000)),
                   sum(iif(sp.code in ('USER'), wli.amount, 0.000)),
                   sum(iif(pt.code='S' /*and pH.status2='1'*/, wli.amount, 0.000)),
                   sum(case sp.calcrest when '1' then wli.amount else 0.0000 end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'GOOD' then wli.amount
                        else 0.0000
                   end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'BAD' then wli.amount
                        else 0.0000
                   end)
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join pallet_feature pf on pf.id = p.featureid
                             left join site s
                                  left join sitespecies sp
                                    on sp.sitespeciesid = s.sitespeciesid
                               on s.siteid = p.siteid
                             left join pallet_type pt on pt.id = p.ptypeid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.objid = :objid
               and wl.status = '1'
             group by wl.waresid
              into :wid, :qb, :qs, :qr, :qe, :qt, :qn, :qi, :qu, :qp, :q, :qgood, :qbad
           do
           begin
                OPEN WINFO;
                FETCH WINFO INTO :wcode,:wname,:vufactor,:vucode,:mufactor,:mucode,:wgid,:sgid;
                CLOSE WINFO;
    
                suspend;
           end
        end
        else
        begin
          for
            select wl.waresid,
                   sum(case sp.code when 'B' then wli.amount else 0.000 end),
                   sum(case sp.code when 'S' then wli.amount else 0.000 end),
                   sum(case when sp.code starting 'BUYRET' then wli.amount else 0.000 end),
                   sum(case sp.code when 'E' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype <> '1' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype = '1' then wli.amount else 0.000 end),
                   sum(iif(coalesce(s.calcrest,sp.calcrest)='i', wli.amount, 0.000)),
                   sum(iif(sp.code in ('USER'), wli.amount, 0.000)),
                   sum(iif(pt.code='S' /*and pH.status2='1'*/, wli.amount, 0.000)),
                   sum(case sp.calcrest when '1' then wli.amount else 0.0000 end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'GOOD' then wli.amount
                        else 0.0000
                   end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'BAD' then wli.amount
                        else 0.0000
                   end)
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join pallet_feature pf on pf.id = p.featureid
                             left join site s
                                  left join sitespecies sp
                                    on sp.sitespeciesid = s.sitespeciesid
                               on s.siteid = p.siteid
                             left join pallet_type pt on pt.id = p.ptypeid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.objid = :objid
               and wl.status = '1'
               and wl.zoneid = :zoneid
             group by wl.waresid
              into :wid, :qb, :qs, :qr, :qe, :qt, :qn, :qi, :qu, :qp, :q, :qgood, :qbad
           do
           begin
                OPEN WINFO;
                FETCH WINFO INTO :wcode,:wname,:vufactor,:vucode,:mufactor,:mucode,:wgid,:sgid;
                CLOSE WINFO;
    
                suspend;
           end
        end
    end
    else
    begin
         insert into wh_tbltmp_ids(id)
         with recursive tmpsite as (
             select s.siteid
               from site s
              where s.siteid = :siteid
              union all
             select s.siteid
               from tmpsite t
                    join site s on s.higher = t.siteid
         )
         select t.siteid
           from tmpsite t;

        if (:zoneid is NULL or :zoneid=0) then
        begin
          for
            select wl.waresid,
                   sum(case sp.code when 'B' then wli.amount else 0.000 end),
                   sum(case sp.code when 'S' then wli.amount else 0.000 end),
                   sum(case when sp.code starting 'BUYRET' then wli.amount else 0.000 end),
                   sum(case sp.code when 'E' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype <> '1' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype = '1' then wli.amount else 0.000 end),
                   sum(iif(coalesce(s.calcrest,sp.calcrest)='i', wli.amount, 0.000)),
                   sum(iif(sp.code in ('USER'), wli.amount, 0.000)),
                   sum(iif(pt.code='S' /*and pH.status2='1'*/, wli.amount, 0.000)),
                   sum(case sp.calcrest when '1' then wli.amount else 0.0000 end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'GOOD' then wli.amount
                        else 0.0000
                   end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'BAD' then wli.amount
                        else 0.0000
                   end)
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join wh_tbltmp_ids i on i.id = p.siteid
                             left join pallet_feature pf on pf.id = p.featureid
                             left join site s
                                  left join sitespecies sp
                                    on sp.sitespeciesid = s.sitespeciesid
                               on s.siteid = p.siteid
                             left join pallet_type pt on pt.id = p.ptypeid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.objid = :objid
               and wl.status = '1'
               and i.id is NOT NULL
             group by wl.waresid
              into :wid, :qb, :qs, :qr, :qe, :qt, :qn, :qi, :qu, :qp, :q, :qgood, :qbad
           do
           begin
                OPEN WINFO;
                FETCH WINFO INTO :wcode,:wname,:vufactor,:vucode,:mufactor,:mucode,:wgid,:sgid;
                CLOSE WINFO;
    
                suspend;
           end
        end
        else
        begin
          for
            select wl.waresid,
                   sum(case sp.code when 'B' then wli.amount else 0.000 end),
                   sum(case sp.code when 'S' then wli.amount else 0.000 end),
                   sum(case when sp.code starting 'BUYRET' then wli.amount else 0.000 end),
                   sum(case sp.code when 'E' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype <> '1' then wli.amount else 0.000 end),
                   sum(case when sp.code = 'TRASH' and p.pallettype = '1' then wli.amount else 0.000 end),
                   sum(iif(coalesce(s.calcrest,sp.calcrest)='i', wli.amount, 0.000)),
                   sum(iif(sp.code in ('USER'), wli.amount, 0.000)),
                   sum(iif(pt.code='S' /*and pH.status2='1'*/, wli.amount, 0.000)),
                   sum(case sp.calcrest when '1' then wli.amount else 0.0000 end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'GOOD' then wli.amount
                        else 0.0000
                   end),
                   sum(case
                        when sp.calcrest = '1' and coalesce(pf.code,'') = 'BAD' then wli.amount
                        else 0.0000
                   end)
              from wareslot wl
                   left join wareslotitem wli
                        left join pallet p
                             left join wh_tbltmp_ids i on i.id = p.siteid
                             left join pallet_feature pf on pf.id = p.featureid
                             left join site s
                                  left join sitespecies sp
                                    on sp.sitespeciesid = s.sitespeciesid
                               on s.siteid = p.siteid
                             left join pallet_type pt on pt.id = p.ptypeid
                          on p.palletid = wli.palletid
                     on wli.wlotid = wl.wlotid
             where wl.objid = :objid
               and wl.status = '1'
               and wl.zoneid = :zoneid
               and i.id is NOT NULL
             group by wl.waresid
              into :wid, :qb, :qs, :qr, :qe, :qt, :qn, :qi, :qu, :qp, :q, :qgood, :qbad
           do
           begin
                OPEN WINFO;
                FETCH WINFO INTO :wcode,:wname,:vufactor,:vucode,:mufactor,:mucode,:wgid,:sgid;
                CLOSE WINFO;
    
                suspend;
           end
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_RESTCONTROL_REST_ALL_DC (
    OBJID R_ID64,
    ZONEID R_ID = null,
    WARESID R_ID = null)
returns (
    WID type of R_ID,
    WNAME type of NAME,
    WCODE type of CODE,
    MUCODE type of R_CODE,
    VUCODE type of R_CODE,
    MUFACTOR type of R_DOUBLE,
    VUFACTOR type of R_DOUBLE,
    QB type of R_QUANTITY,
    QS type of R_QUANTITY,
    QR type of R_QUANTITY,
    QT type of R_QUANTITY,
    QE type of R_QUANTITY,
    QN type of R_QUANTITY,
    QI type of R_QUANTITY,
    QU type of R_QUANTITY,
    QP type of R_QUANTITY,
    Q type of R_QUANTITY,
    DATETIME type of R_DATETIME,
    SGCODE type of R_CODE3,
    SGNAME type of R_NAME,
    WGNAME type of R_NAME,
    WGNAMEROOT type of R_NAME,
    SLOTNAME type of R_NAME)
as
begin

  for
   select k.wid, k.wname, k.wcode, k.mucode, k.vucode, k.mufactor, k.vufactor,
          k.qb, k.qs, k.qr, k.qt, k.qe, k.qn, k.q, k.qi, k.qu, k.qp, k.datetime,
          sg.code, sg.name, wg.name, wgr.name, s.name
     from k_restcontrol_rest_dc(:objid, :zoneid, :waresid) k
          left join waresgroup wg on wg.waresgrid = k.wgid
          left join k_get_waresgroup_root(k.wgid) gr
               left join waresgroup wgr on wgr.waresgrid = gr.wgid
            on 1=1
          left join k_wares_selgroup sg on sg.id = k.sgid
          left join waressite ws
               left join site s on s.siteid = ws.siteid
            on ws.waresid = k.wid
     into :wid, :wname, :wcode, :mucode, :vucode, :mufactor, :vufactor, :qb,
          :qs, :qr, :qt, :qe, :qn, :q, :qi, :qu, :qp, :datetime,
          :sgcode, :sgname, :wgname, :wgnameroot, :slotname
  do
    suspend;

  if (:wid is null) then
  begin
    datetime = current_timestamp;
    select g.code, g.name, vwu.factor, vu.shortname, mwu.factor, mu.shortname,
           sg.code, sg.name, wg.name, wgr.name, s.name
      from gwares g
           left join waresunit vwu
                left join unit vu on vu.unitid = vwu.unitid
             on vwu.waresunitid = g.viewunitid
           left join waresunit mwu
                left join unit mu on mu.unitid = mwu.unitid
             on mwu.waresunitid = g.mainunitid
           left join waresgroup wg on wg.waresgrid = g.waresgroup
           left join k_get_waresgroup_root(g.waresgroup) gr
                left join waresgroup wgr on wgr.waresgrid = gr.wgid
             on 1=1
           left join k_wares_selgroup sg on sg.id = g.selgroup
           left join waressite ws
                left join site s on s.siteid = ws.siteid
             on ws.waresid = g.waresid
     where g.waresid = :waresid
      into :wcode, :wname, :vufactor, :vucode, :mufactor, :mucode,
           :sgcode, :sgname, :wgname, :wgnameroot, :slotname;

    qb = 0;
    qs = 0;
    qr = 0;
    qt = 0;
    qe = 0;
    qn = 0;
    qu = 0;
    q = 0;
    wid = waresid;

    suspend;
  end
end^

SET TERM ; ^



ALTER TABLE WM_TASK_SITE
ADD STATUS R_STATUS
NOT NULL ;



ALTER TABLE WM_TASK_SITE
ADD MANID R_ID;



ALTER TABLE WM_TASK_SITE
ADD BEGINTIME R_DATETIME;



ALTER TABLE WM_TASK_SITE
ADD ENDTIME R_DATETIME;



SET TERM ^ ;

create or alter procedure K_WH_INVENT_TASKPALLET (
    TASKID type of R_ID)
returns (
    SID type of R_ID,
    PID type of R_ID,
    SITEID_ROW type of R_ID,
    IS_PALLET_INVENT type of R_BOOL,
    IS_SITE_INVENT type of R_BOOL)
as
declare variable SITEID type of R_ID;
declare variable OBJID type of R_ID;
declare variable ZONEID type of R_ID;
declare variable SS_ROW type of R_ID;
declare variable SS_L type of R_ID;
declare variable SSID type of R_ID;
begin
  select t.infoid, t.zoneid
    from wm_task t
   where t.taskid = :taskid
    into :objid, :zoneid;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'R'
    into :ss_row;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'L'
    into :ss_l;
  -- по рядам
  for
    select s.siteid
      from site s
           left join sitezone_items szi on s.siteid = szi.siteid
     where szi.zoneid = :zoneid
           and s.sitespeciesid = :ss_row
      into :siteid_row do
  begin

    for
      select sc.sid, s.sitespeciesid
        from k_site_children(:siteid_row,null,'1') sc
             left join site s on s.siteid = sc.sid
        into :sid, :ssid
    do
    begin
      --
      is_site_invent = null;
      if (ssid = :ss_l) then
      begin

        if (
          exists (
             select *
               from wm_task_site ts
              where ts.siteid = :sid
                    and ts.taskid = :taskid
                    and ts.status = '2'
          )
       ) then
          is_site_invent = '1';
       else
         is_site_invent = '0';
      end

      -- паллеты
      pid = null;
      is_pallet_invent = null;
      for
        select p.palletid
          from pallet p
         where p.siteid = :sid
               and p.status = '1'
               and coalesce(p.objid,:objid) = :objid
               and coalesce(p.zoneid,:zoneid) = :zoneid
          into :pid do
      begin

        if (:pid is not null) then
        begin
          if (exists(
            select *
              from wm_task_pallet tp
             where tp.taskid = :taskid
                   and tp.palletid = :pid
                   and tp.siteid = :sid
                   and tp.status = '1'
          )) then
             is_pallet_invent = '1';
          else
             is_pallet_invent = null;


        end


      end 






      suspend;
    end 


  end
  -- остальные мп (Экспедиция, Ворота)
  for
    select szi.siteid
      from sitespecies ss
           left join site s
                left join sitezone_items szi on s.siteid = szi.siteid
             on s.sitespeciesid = ss.sitespeciesid
     where ss.code in ('E','GATE')
           and szi.zoneid = :zoneid
      into :siteid_row
  do
  begin
    if (
        exists (
           select ts.status
             from wm_task_site ts
            where ts.siteid = :siteid_row
                  and ts.taskid = :taskid
                  and ts.status = '2'
        )
    ) then
        is_site_invent = '1';
      else
        is_site_invent = '0';
  ---
    for
      select p.palletid
        from pallet p
       where p.siteid = :siteid_row
             and p.status = '1'
             and coalesce(p.objid,:objid) = :objid
             and coalesce(p.zoneid,:zoneid) = :zoneid
        into :pid do
    begin
      is_pallet_invent = null;
      if (:pid is not null) then
      begin
        if (exists(
            select *
              from wm_task_pallet tp
             where tp.taskid = :taskid
                   and tp.palletid = :pid
                   and tp.siteid = :siteid_row
                   and tp.status = '1'
        )) then
          is_pallet_invent = '1';



      end

      suspend;
    end
  ---
  end 
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_WH_INVENT_GETTASKPROGRESS (
    TASKID type of R_ID)
returns (
    SITEID type of R_ID,
    SNAME type of R_NAME,
    CNT_PALLET integer,
    CNT_PALLET_ALL integer,
    CNT_SITE_ALL integer,
    CNT_SITE integer)
as
declare variable OBJID type of R_ID;
declare variable ZONEID type of R_ID;
declare variable SS_ROW type of R_ID;
declare variable SS_MX type of R_ID;
declare variable SS_L type of R_ID;
declare variable SID type of R_ID;
declare variable CNT_PALLET_TEMP integer;
declare variable CNT_PALLET_ALL_TEMP integer;
declare variable PID type of R_ID;
declare variable SITEID_ROW type of R_ID;
declare variable IS_PALLET_INVENT type of R_ID;
begin

  select t.infoid, t.zoneid
    from wm_task t
   where t.taskid = :taskid
    into :objid, :zoneid;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'R'
    into :ss_row;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'B'
    into :ss_mx;

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'L'
    into :ss_l;


  for
    select tp.siteid_row, s.name,
           count(tp.pid), sum(iif(tp.is_pallet_invent is null,0,1)),        -- паллеты
           sum(iif(tp.is_site_invent is not null,1,0)), sum(iif(tp.is_site_invent ='1',1,0))
      from k_wh_invent_taskpallet(:taskid) tp
           left join site s on tp.siteid_row = s.siteid
     group by tp.siteid_row, s.name
      into :siteid, :sname,
           :cnt_pallet_all, :cnt_pallet,
           :cnt_site_all, :cnt_site

  do
  begin
    suspend;
  end
  -------------------------------
  /*
  for
    select s.siteid, s.name
      from site s
           left join sitezone_items szi on s.siteid = szi.siteid
     where szi.zoneid = :zoneid
           and s.sitespeciesid = :ss_row
      into :siteid, :sname do
  begin
    cnt_site = 0;
    cnt_site_all = 0;
    -- МП
  for
    select sc.sid
      from k_site_children(:siteid,:ss_l,'1') sc
      into :sid
    do
    begin
       -------------
      cnt_site_all = : cnt_site_all + 1;
      if (
        exists (
           select ts.status
             from wm_task_site ts
            where ts.siteid = :sid
                  and ts.taskid = :taskid
                  and ts.status = '2'
        )
      ) then
        cnt_site = :cnt_site + 1;

    end 

    cnt_pallet_all = 0;
    cnt_pallet = 0;
    -- паллеты
    for
      select sc.sid
        from k_site_children(:siteid,null,'1') sc
        into :sid
    do
    begin

      cnt_pallet_all_temp = 0;
      cnt_pallet_temp = 0;

      select count(p.palletid)
        from pallet p
       where p.siteid = :sid
             and p.status = '1'
             and coalesce(p.objid,:objid) = :objid
        into :cnt_pallet_all_temp;


      select count(distinct tp.palletid)
        from wm_task_pallet tp
       where tp.taskid = :taskid
             and tp.siteid = :sid
             and tp.status = '1'
        into :cnt_pallet_temp;

      cnt_pallet_all = :cnt_pallet_all + :cnt_pallet_all_temp;
      cnt_pallet = :cnt_pallet + :cnt_pallet_temp;

    end 



    suspend;
  end 


  -- паллеты не на стеллажах
  cnt_site = 0;
  cnt_site_all = 0;
  cnt_pallet = 0;
  cnt_pallet_temp = 0;
  for
    select s.siteid, s.name, count(distinct p.palletid), sum(iif(tp.taskpalletid is not null,1,0))
      from sitezone_items szi
           left join pallet p
                left join wm_task_pallet tp on tp.palletid = p.palletid
                                               and tp.taskid = :taskid
                                               and tp.status = '1'
                left join site s
                     left join sitespecies ss on ss.sitespeciesid = s.sitespeciesid
                  on s.siteid = p.siteid
             on p.siteid = szi.siteid
     where szi.zoneid = :zoneid
           and p.status = '1'
           and p.pallettype = '0'
           and coalesce(p.objid,:objid) = :objid
           and ss.code in ('GATE','E')
     group by 1,2
      into :siteid, :sname, :cnt_pallet_all, :cnt_pallet_temp

  do
  begin
    cnt_site_all = : cnt_site_all + 1;
      if (
        exists (
           select ts.status
             from wm_task_site ts
            where ts.siteid = :siteid
                  and ts.taskid = :taskid
                  and ts.status = '2'
        )
      ) then
        cnt_site = :cnt_site + 1;



    cnt_pallet = :cnt_pallet + :cnt_pallet_temp;
    suspend;
  end 

  */
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_WH_INVENT_NOTINVENTPAL (
    TASKID type of R_ID)
returns (
    SNAME type of R_NAME,
    PNUMBER type of R_BARCODE)
as
declare variable OBJID type of R_ID;
declare variable ZONEID type of R_ID;
begin
  for
    select s.name, case
                     when (p.pallettype = '1') then 'МО'
                     when (p.pallettype = '0') then '№'||p.number
                   end
      from k_wh_invent_taskpallet(:taskid) tp
           left join site s on s.siteid = tp.sid
           left join pallet p on p.palletid = tp.pid
     where tp.pid is not null
           and tp.is_pallet_invent is null
     order by s.name asc
      into :sname, :pnumber

  do
    suspend;
end^

SET TERM ; ^



ALTER TABLE DOCTYPESTATUS
ADD APPROVEDSTATUS R_FLAG;



SET TERM ^ ;

create or alter procedure K_WH_INVENT_NOTAPPRDOCS (
    TASKID type of R_ID)
returns (
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    DOCS type of R_BLOB)
as
declare variable OBJID type of R_ID;
declare variable TMALGO type of R_FLAG;
begin

  select tm.algorithm, t.infoid
    from wm_task t
         left join wm_taskmethod tm on t.taskmethodid = tm.methodid
   where t.taskid = :taskid
    into :tmalgo, :objid;

  if (:tmalgo = 'L') then
  begin

    for
    select g.code, g.name, list(trim('O'||cast(d.docid as integer)),', ')
      from doctypestatus dts
           left join document d
                left join cargo c
                     left join wm_task_wares tw
                          left join gwares g on tw.waresid = g.waresid
                       on tw.taskid = :taskid and tw.waresid = c.waresid
                       on d.docid = c.document
                  on d.doctype = dts.doctid and d.status = dts.code
     where coalesce(dts.approvedstatus,'0') <> '1'
           and (d.fromobj = :objid or d.toobj = :objid)
           and tw.taskwaresid is not null
     group by 1,2
      into :wcode, :wname, :docs do
    begin
      suspend;
    end 

   end
   if (:tmalgo = 'A') then
   begin
     for
     select g.code,  g.name, list(trim('O'||cast(d.docid as integer)||'(')||dt.name||')',', ')
       from doctypestatus dts
            left join doctype dt on dt.doctid = dts.doctid
            left join document d
                 left join cargo c
                      left join gwares g on g.waresid = c.waresid
                   on c.document = d.docid
              on d.doctype = dts.doctid and d.status = dts.code
      where coalesce(dts.approvedstatus,'0') <> '1'
            and (d.fromobj = :objid or d.toobj = :objid)
            and d.docid is not null
      group by 1,2
       into :wcode, :wname, :docs
     do
     begin
       suspend;
     end 

   end
end^

SET TERM ; ^



ALTER TABLE PALLET
ADD CLIENTID R_ID;



SET TERM ^ ;

create or alter procedure K_WH_INVENT_TRASH (
    TASKID type of R_ID)
returns (
    PALLETID type of R_ID,
    PNUMBER type of R_BARCODE,
    PSTATUS type of R_STATUS,
    OBJID type of R_ID,
    CLIENTID type of R_ID)
as
--declare variable objid type of r_id;
declare variable TRASHPALLETID type of R_ID;
declare variable TRASHSITEID type of R_ID;
begin

  select t.infoid
    from wm_task t
   where t.taskid = :taskid
    into :objid;

  select k.pid,k.sid
    from k_wh_get_trash(:objid) k
    into :trashpalletid,:trashsiteid;

  for
    select p.palletid, p.number, p.status, p.clientid
      from wm_task_wares tw
           left join wareslot wl
                left join wareslotitem wli
                     left join pallet p on p.palletid = wli.palletid
                       on wli.wlotid = wl.wlotid
                  on tw.waresid = wl.waresid
     where tw.taskid = :taskid
           and wl.objid = :objid
           and p.siteid = :trashsiteid
           and p.palletid <> :trashpalletid
     group by 1,2,3,4
      into :palletid, :pnumber, :pstatus, :clientid do
  begin

    suspend;
  end 

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_WH_INVENT_TRASH (
    TASKID type of R_ID)
returns (
    PALLETID type of R_ID,
    PNUMBER type of R_BARCODE,
    PSTATUS type of R_STATUS,
    OBJID type of R_ID,
    CLIENTID type of R_ID)
as
--declare variable objid type of r_id;
declare variable TRASHPALLETID type of R_ID;
declare variable TRASHSITEID type of R_ID;
begin

  select t.infoid
    from wm_task t
   where t.taskid = :taskid
    into :objid;

  select k.pid,k.sid
    from k_wh_get_trash(:objid) k
    into :trashpalletid,:trashsiteid;

  for
    select p.palletid, p.number, p.status, p.clientid
      from wm_task_wares tw
           left join wareslot wl
                left join wareslotitem wli
                     left join pallet p on p.palletid = wli.palletid
                       on wli.wlotid = wl.wlotid
                  on tw.waresid = wl.waresid
     where tw.taskid = :taskid
           and wl.objid = :objid
           and p.siteid = :trashsiteid
           and p.palletid <> :trashpalletid
     group by 1,2,3,4
      into :palletid, :pnumber, :pstatus, :clientid do
  begin

    suspend;
  end 

end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_INVENT_STATUS (
    TASKID type of R_ID,
    UPDOWN integer)
as
declare variable TTID type of R_ID;
declare variable CURSTATUS type of R_STATUS;
declare variable NEXTSTATUS type of R_STATUS;
begin
  select tt.ttid
    from k_tasktype_by_code('INVENT','1') tt
    into :ttid;

  select t.status
    from wm_task t
   where t.taskid = :taskid
    into :curstatus;

  select iif(:updown=1,tts.upcodes, tts.downcodes)
    from tasktypestatus tts
   where tts.tasktypeid = :ttid
         and tts.code = :curstatus
    into :nextstatus;

  if (:nextstatus is null) then
    exception exc_k_common 'Не верный статус!';

  update wm_task t
     set t.status = :nextstatus
   where t.taskid = :taskid;


end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_SITEINFO (
    TID type of R_ID,
    SID type of R_ID)
returns (
    USERNAME type of R_FULLNAME)
as
begin
  select first(1) gon.fullname
    from wm_task_site ts
         left join getobjectname(ts.manid,'03') gon on 1=1
   where ts.taskid = :tid
         and ts.siteid = :sid
         and ts.status = '2'
   order by ts.lastdate desc
    into :username;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_CHECKTASKSITE (
    TID type of R_ID,
    WMSESID type of R_ID)
returns (
    SITEID type of R_ID)
as
declare variable MANID type of R_ID;
begin
  select s.objid
    from wm_session s
   where s.sessionid = :wmsesid
         and s.disconnecttime is null
    into :manid;

  if (:manid is null) then
   exception exc_k_common 'Пользователь не найден!';


  select ts.siteid
    from wm_task_site ts
   where ts.taskid = :tid
         and ts.status <> '2'
    into :siteid;

  suspend;
end^

SET TERM ; ^



ALTER TABLE WM_TASK_PALLET
ADD MANID R_ID;



ALTER TABLE WM_TASK_PALLET
ADD CONSTRAINT F_TASKPALLET_MAN
FOREIGN KEY (MANID)
REFERENCES MAN(MANID)
ON UPDATE CASCADE;



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_CHECKTASKPALLET (
    TID type of R_ID,
    WMSESID type of R_ID)
returns (
    PID type of R_ID,
    WID type of R_ID)
as
declare variable MANID type of R_ID;
begin
  select s.objid
    from wm_session s
   where s.sessionid = :wmsesid
         and s.disconnecttime is null
    into :manid;

  if (:manid is null) then
   exception exc_k_common 'Пользователь не найден!';

  select tw.waresid
    from wm_task_Wares tw
   where tw.taskid = :tid
         and tw.wm_sessionid = :wmsesid
         and tw.status = '1'
    into :wid;

  select tp.palletid
    from wm_task_pallet tp
   where tp.taskid = :tid
         and tp.status = 'w'
         and tp.manid = :manid
    into :pid;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_JOINSITE (
    TID type of R_ID,
    SID type of R_ID,
    WMSESID type of R_ID)
as
declare variable MANID type of R_ID;
begin
  select s.objid
    from wm_session s
   where s.sessionid = :wmsesid
         and s.disconnecttime is null
    into :manid;

  if (:manid is null) then
    exception exc_k_common 'Пользователь не найден!';

  if (exists(
    select *
      from wm_task_site ts
     where ts.taskid = :tid
           and ts.siteid = :sid
           and ts.manid <> :manid
           and ts.status = '1'
  )) then
    exception exc_k_common 'МП инвентаризируется другим сотрудником!';

  if (exists(
    select *
      from wm_task_site ts
     where ts.taskid = :tid
           and ts.siteid <> :sid
           and ts.manid = :manid
           and ts.status = '1'
  ))
  then
    exception exc_k_common 'Есть незавершенное МП!';
  else
  begin
    if (not exists(   -- проверка при работе из ПК
      select *
      from wm_task_site ts
     where ts.taskid = :tid
           and ts.siteid = :sid
           and ts.manid = :manid
           and ts.status = '1'
    )) then
      insert into wm_task_site(taskid,siteid,status,manid,begintime)
      values (:tid,:sid,'1',:manid,current_timestamp);
  end

end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_JOINPALLET (
    TID type of R_ID,
    PID type of R_ID,
    WMSESID type of R_ID)
as
declare variable MANID type of R_ID;
declare variable SITEID type of R_ID;
declare variable WORKSITEID type of R_ID;
declare variable SSCODE type of R_CODE;
declare variable PSITEID type of R_ID;
declare variable SS_L type of R_ID;
begin
  select s.objid
    from wm_session s
   where s.sessionid = :wmsesid
         and s.disconnecttime is null
    into :manid;

  if (:manid is null) then
    exception exc_k_common 'Пользователь не найден!';

  select p.siteid
    from pallet p
   where p.palletid = :pid
    into :siteid;

  if (:siteid is null) then
    exception exc_k_common 'Не найдено МП!';

  select ss.sitespeciesid
    from sitespecies ss
   where ss.code = 'L'
    into :ss_l;

  select ts.siteid, ss.code
    from wm_task_site ts
         left join site s
              left join sitespecies ss on ss.sitespeciesid = s.sitespeciesid
           on s.siteid = ts.siteid
   where ts.taskid = :tid
         and ts.manid = :manid
         and ts.status = '1'
    into :worksiteid, :sscode;

  if (exists(
    select *
      from wm_task_pallet tp
     where tp.taskid = :tid
           and tp.palletid = :pid
           and tp.manid <> :manid
           and tp.status = 'w'
  )) then
    exception exc_k_common 'Паллет инвентаризируется другим сотрудником!';

  if (:worksiteid is null) then
    exception exc_k_common 'Не найдено МП инвентаризации!';

  if (:sscode in ('GATE','E')) then
  begin
    if (not exists(
      select *
        from pallet p
       where p.palletid = :pid
             and p.siteid = :worksiteid
    )) then
      exception exc_k_common 'Поддон не числится на инвентаризируемом МП!';
  end 
  else if (:sscode = 'L') then
  begin
    select sp.sid
      from k_site_parent(:siteid,:ss_l) sp
      into :psiteid;

    if (:worksiteid <> :psiteid) then
      exception exc_k_common 'Поддон не числится на инвентаризируемом МП!';
  end 

  if (exists(
    select *
      from wm_task_pallet tp
     where tp.taskid = :tid
           --and tp.siteid = :siteid
           and tp.palletid <> :pid
           and tp.manid = :manid
           and tp.status = 'w'
  )) then
    exception exc_k_common 'Завершите привязанный паллет!';
  else
  begin
    if (not exists(
      select *
      from wm_task_pallet tp
     where tp.taskid = :tid
           and tp.siteid = :siteid
           and tp.palletid = :pid
           and tp.manid = :manid
           and tp.status = 'w'
    )) then
      insert into wm_task_pallet(taskid,siteid,palletid,status,manid)
      values (:tid,:siteid,:pid,'w',:manid);
  end 



end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_HSITE (
    TID type of R_ID,
    SID type of R_ID)
returns (
    SITEID type of R_ID)
as
declare variable RACK_ID type of R_ID;
declare variable RACK_SPID type of R_ID;
declare variable ZONEID type of R_ID;
begin
   select sp.sitespeciesid
    from sitespecies sp
   where sp.code = 'L'
    into :rack_spid;

  select k.sid
    from k_site_parent(:sid,:rack_spid) k
    into :rack_id;

  select t.zoneid
    from wm_task t
   where t.taskid = :tid
    into :zoneid;

  if (not exists(
    select *
      from sitezone_items szi
     where szi.siteid = :sid
           and szi.zoneid = :zoneid
  )) then
    exception exc_k_common 'МП не относится к зоне инвентаризации!';

  if (:rack_id is not null) then
    siteid = :rack_id;
  else if (exists(
    select *
      from site s
           left join sitespecies ss on s.sitespeciesid = ss.sitespeciesid
     where s.siteid = :sid
           and ss.code in ('GATE','E')
  )) then
    siteid = :sid;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_GETTASK (
    WMSESID type of R_ID)
returns (
    TASKID type of R_ID,
    ALGORITHM type of R_FLAG,
    PLANDATETIME type of R_DATETIME)
as
declare variable TTID type of R_ID;
declare variable TMID type of R_ID;
declare variable OBJID type of R_ID;
begin
  select tt.ttid
    from k_tasktype_by_code('INVENT','1') tt
    into :ttid;

  select s.objid
    from k_wh_sessionzoneobj(:wmsesid) s
    into :objid;

  if (:objid is null) then
    exception exc_k_common 'Не найден объект!';

  -- полная инвентаризация
  algorithm = 'A';

  select tm.methodid
    from wm_taskmethod tm
   where tm.tasktypeid = :ttid
         and tm.algorithm = :algorithm
    into :tmid;

  if (:tmid is not null) then
  begin

    select first(1) t.taskid
      from wm_task t
     where t.tasktypeid = :ttid
           and t.taskmethodid = :tmid
           and t.infoid = :objid
           and t.plandatetime <= current_date -- нельзя начать раньше запланированной даты
           and t.status = '1'
     order by t.plandatetime asc
      into :taskid;

    if (:taskid is not null) then
    begin
      suspend;
      exit;
    end 
  end 

  -- локальная инвентаризация
  algorithm = 'L';

  select tm.methodid
    from wm_taskmethod tm
   where tm.tasktypeid = :ttid
         and tm.algorithm = 'L'
    into :tmid;

  for
    select t.taskid, t.plandatetime
      from wm_task t
     where t.tasktypeid = :ttid
           and t.taskmethodid = :tmid
           and t.infoid = :objid
           and t.plandatetime <= current_date -- нельзя начать раньше запланированной даты
           and t.status = '1'
     order by t.plandatetime asc
      into :taskid, :plandatetime
  do
  begin

    suspend;
  end 

end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_LISTPALLET (
    TID type of R_ID,
    SID type of R_ID,
    WMSESID type of R_ID)
returns (
    SITEID type of R_ID,
    SNAME type of R_NAME,
    PALLETID type of R_ID,
    PTYPE type of R_FLAG,
    PNUMBER type of R_BARCODE,
    TPSTATUS type of R_STATUS)
as
declare variable MANID type of R_ID;
declare variable SSCODE type of R_CODE;
declare variable OBJID type of R_ID;
declare variable ZONEID type of R_ID;
begin
  /*
  select sp.sitespeciesid
    from sitespecies sp
   where sp.code = 'L'
    into :rack_spid;

  select k.sid
    from k_site_parent(:sid,:rack_spid) k
    into :rack_id;
  */
  select t.infoid, t.zoneid
    from wm_task t
   where t.taskid = :tid
    into :objid, :zoneid;

  select wms.objid
    from wm_session wms
   where wms.sessionid = :wmsesid
    into :manid;

  select ss.code, s.siteid, s.name
    from site s
         left join sitespecies ss on ss.sitespeciesid = s.sitespeciesid
   where s.siteid = :sid
    into :sscode, :siteid, :sname;

  if (:sscode in ('E','GATE')) then
  begin
    for
      select p.palletid, p.pallettype, p.number
        from pallet p
       where p.siteid = :sid
             and p.status = '1'
             and p.objid = :objid
        into :palletid, :ptype, :pnumber do
    begin
      tpstatus = null;

      select first(1) tp.status
        from wm_task_pallet tp
       where tp.taskid = :tid
             and tp.palletid = :palletid
       order by tp.taskpalletid desc   -- не хорошо
          into :tpstatus;

       suspend;
    end 
  end 
  else if (:sscode = 'L') then
  begin
    -- стеллаж
    for
      select s.siteid, s.name, p.palletid, p.pallettype, p.number
        from site s
             left join pallet p on s.siteid = p.siteid and p.status = '1'
       where s.higher = :sid
       order by s.z_coord descending,s.name descending
        into :siteid, :sname, :palletid, :ptype, :pnumber
    do
    begin
      tpstatus = null;

      if (:palletid is not null) then
      begin
        select first(1) tp.status
          from wm_task_pallet tp
         where tp.taskid = :tid
               and tp.palletid = :palletid
         order by tp.taskpalletid desc   -- не хорошо
          into :tpstatus;

      end 


      suspend;


    end 

  end 
  else
  begin
    exception exc_k_common 'Неверное МП!';
  end 
  --suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_PALLETWARES (
    PALLETID type of R_ID,
    WMSESID type of R_ID)
returns (
    WID type of R_ID,
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    AMOUNT type of R_QUANTITY,
    VUFACTOR type of R_MULTIPLE,
    VUCODE type of R_CODE,
    MUFACTOR type of R_MULTIPLE,
    MUCODE type of R_CODE,
    TWSTAT type of R_STATUS)
as
declare variable TASKID type of R_ID;
begin

    for
        select wl.waresid,sum(wli.amount)
          from wareslotitem wli
               left join wareslot wl on wl.wlotid=wli.wlotid
         where wli.palletid = :palletid
           and wli.amount > 0.00001
         group by wl.waresid
          into :wid,:amount
    do
    begin
        select g.code,g.name,
               vwu.factor,vu.shortname,mwu.factor,mu.shortname
          from gwares g
               left join waresunit vwu
                    left join unit vu on vu.unitid = vwu.unitid
                 on vwu.waresunitid = g.viewunitid
               left join waresunit mwu
                    left join unit mu on mu.unitid = mwu.unitid
                 on mwu.waresunitid = g.mainunitid
          where g.waresid = :wid
           into :wcode,:wname,:vufactor,:vucode,:mufactor,:mucode;

        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_PALWARESADD (
    WMSESID type of R_ID,
    PALLETID type of R_ID,
    WUID type of R_ID,
    PRODUCTDATE type of R_DATE,
    AMOUNT type of R_QUANTITY,
    TASKID type of R_ID)
as
declare variable WUFACTOR type of R_DOUBLE;
declare variable WARESID type of R_ID;
declare variable PTRASHID type of R_ID;
declare variable WLOTID type of R_ID;
declare variable TWID type of R_ID;
declare variable SESZONEOBJID type of R_ID;
declare variable QPALLETWARES type of R_DOUBLE;
declare variable DOCID type of R_ID64;
declare variable WLINCOMEID type of R_ID64;
declare variable NEEDTASKEND type of R_FLAG;
begin
  -- Предварительные проверки и установки
  if (:amount is NULL or :amount<0.00001 ) then exit;

  -- Объект, к которому привязан пользователь, чтобы его остатками работать
  select objid
    from k_wh_sessionzoneobj(:wmsesid)
    into :seszoneobjid;

  select wu.factor,wu.waresid
    from waresunit wu
   where wu.waresunitid = :wuid
    into :wufactor,:waresid;

  amount = :amount * :wufactor;

  -- Найдем поддон недостачу, все равно что-то с него надо убрать, из неоткуда при выверке взяться не может
  select pid
    from K_WH_GET_TRASH(:seszoneobjid)
    into :ptrashid;
  if (:ptrashid is NULL) then
    exception exc_ur_common 'Не найден поддон НЕДОСТАЧА!';


  -- попробуем найти партию
  select first(1) wl.wlotid
    from wareslot wl
   where wl.waresid = :waresid
     and wl.productdate = :productdate
     and wl.objid = :seszoneobjid
    into :wlotid;

  -- Если такой партии нет, то создадим
  if (:wlotid is NULL) then
    insert into wareslot(waresid,objid,status,productdate)
    values(:waresid,:seszoneobjid,'1',:productdate)
    returning wlotid
    into :wlotid;

  -- Работаем с позицией задания
  --qpalletwares = NULL;
  --execute procedure wh_tverify_taskcreatewares(:taskid,:waresid,:dbeg);
  select tw.taskwaresid --,tw.quantity
    from wm_task_wares tw
   where tw.taskid = :taskid
         and tw.waresid = :waresid
         and tw.status = '1'
    into :twid; --,:qpalletwares;

  if (:twid is NULL) then
  begin
    insert into wm_task_wares(taskid,waresid,scanquant,status)
    values (:taskid,:waresid,0.000,'1')
    returning taskwaresid
    into :twid;
  end

  -- Теперь наоборот сначала с недостачи
  FOR
    select o.amount,o.wlincomeid
      from core_listwlincomes(:wlotid,:ptrashid,-:amount,'N') o
      into :amount,:wlincomeid
  do
  begin
      -- Процедура вернет расходные количества, поэтому при приходовании знак наоборот
      insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
      values(:twid,:wlotid,:ptrashid,:amount,'2',:wlincomeid,:wmsesid);

      insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
      values(:twid,:wlotid,:palletid,-:amount,'2',:wlincomeid,:wmsesid);
  end

  -- Списываем с НЕДОСТАЧИ
--  insert into wm_task_lot(wlotid,palletid,taskwaresid,quantity,wm_sessionid,chgwli)
--  values (:wlotid,:ptrashid,:twid,-:amount,:wmsesid,'1');

  -- Добавляем на поддон
--  insert into wm_task_lot(wlotid,palletid,taskwaresid,quantity,wm_sessionid,chgwli)
--  values (:wlotid,:palletid,:twid,:amount,:wmsesid,'1');

  update wm_task_wares tw
     set tw.status = '1'
   where tw.taskwaresid = :twid;

end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_MOVEPAL (
    TASKID type of R_ID,
    PALLETID type of R_ID,
    SITEID type of R_ID,
    WMSESID type of R_ID)
as
declare variable TTID type of R_ID;
declare variable SID type of R_ID;
declare variable PZONEID type of R_ID;
declare variable PALLETTYPE type of R_FLAG;
declare variable MANID type of R_ID;
begin
   select s.objid
     from wm_session s
    where s.sessionid = :wmsesid
          and s.disconnecttime is null
     into :manid;

   if (:manid is null) then
     exception exc_k_common 'Сотрудник не найден!';

    select p.siteid,p.pallettype,p.zoneid
      from pallet p
     where p.palletid = :palletid
      into :sid,:pallettype,:pzoneid;

    if (:pallettype='1') then
        exception exc_k_common 'Нельзя перемещать виртуальный поддон!';

    if (:sid<>:siteid) then
    begin
        if (not exists(select *
                         from sitezone_items szi
                        where szi.zoneid = :pzoneid
                          and szi.siteid = :siteid)) then
            exception exc_k_wrongsite 'МП не включено в зону поддона!';

        execute procedure wh_session_chksite(:wmsesid,:siteid,'');

        if (exists(select *
                     from pallet p
                    where p.siteid = :siteid and p.pallettype = '1')) then
            exception exc_k_wrongsite 'Нельзя перемещать на МП с виртуальным поддоном!';

        insert into wm_task_pallet(taskid, palletid, siteid, status, manid)
        values (:taskid, :palletid, :sid, '0', :manid);
    
        insert into wm_task_pallet(taskid, palletid, siteid, status, manid)
        values (:taskid, :palletid, :siteid, '2', :manid);

        update wm_task_pallet tp
           set tp.status = '1'
         where tp.taskid = :taskid
               and tp.palletid = :palletid
               and tp.status = 'w';
    
        update pallet p
           set p.siteid = :siteid
         where p.palletid = :palletid;
    end
    else
    begin
        --insert into wm_task_pallet(taskid, palletid, siteid, status, manid)
        --values (:taskid, :palletid, :sid, '1', :manid);
        exception exc_k_common 'МП поддона не изменилось!';
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_NOPALLET (
    TID type of R_ID,
    PID type of R_ID,
    WMSESID type of R_ID)
as
declare variable OBJID type of R_ID;
declare variable TRASH_SITEID type of R_ID;
declare variable SITEID type of R_ID;
declare variable MANID type of R_ID;
begin
  select t.infoid
    from wm_task t
   where t.taskid = :tid
    into :objid;

  select s.objid
    from wm_session s
   where s.sessionid = :wmsesid
         and s.disconnecttime is null
    into :manid;

  if (:manid is null) then
   exception exc_k_common 'Пользователь не найден!';

  select t.sid
    from k_wh_get_trash(:objid) t
    into :trash_siteid;

  if (:trash_siteid is null) then
    exception exc_k_common 'МП "Корзина" не найдена!';

  if (exists (
    select *
      from pallet p
     where p.palletid = :pid
           and p.pallettype = '1'
  )) then
    exception exc_k_common 'Запрещено перемещать виртуальный паллет!';
  /*
  if (exists(
    select *
      from wm_task_pallet tp
     where tp.taskid = :tid
           and tp.palletid = :pid
           --and tp.status
  )) then
    exception exc_k_common 'Паллет был найден!';
  */
  update wm_task_pallet tp
     set tp.status = '1'
   where tp.taskid = :tid
         and tp.palletid = :pid
         and tp.status = 'w';

  select p.siteid
    from pallet p
   where p.palletid = :pid
    into :siteid;

  update pallet p
     set p.siteid = :trash_siteid
   where p.palletid = :pid;

  insert into wm_task_pallet(palletid, siteid, status, taskid, manid)
  values (:pid, :siteid, '2', :tid, :manid);

  --suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_LISTPALLET (
    TID type of R_ID,
    SID type of R_ID,
    WMSESID type of R_ID)
returns (
    SITEID type of R_ID,
    SNAME type of R_NAME,
    PALLETID type of R_ID,
    PTYPE type of R_FLAG,
    PNUMBER type of R_BARCODE,
    TPSTATUS type of R_STATUS)
as
declare variable MANID type of R_ID;
declare variable SSCODE type of R_CODE;
declare variable OBJID type of R_ID;
declare variable ZONEID type of R_ID;
begin
  /*
  select sp.sitespeciesid
    from sitespecies sp
   where sp.code = 'L'
    into :rack_spid;

  select k.sid
    from k_site_parent(:sid,:rack_spid) k
    into :rack_id;
  */
  select t.infoid, t.zoneid
    from wm_task t
   where t.taskid = :tid
    into :objid, :zoneid;

  select wms.objid
    from wm_session wms
   where wms.sessionid = :wmsesid
    into :manid;

  select ss.code, s.siteid, s.name
    from site s
         left join sitespecies ss on ss.sitespeciesid = s.sitespeciesid
   where s.siteid = :sid
    into :sscode, :siteid, :sname;

  if (:sscode in ('E','GATE')) then
  begin
    for
      select p.palletid, p.pallettype, p.number
        from pallet p
       where p.siteid = :sid
             and p.status = '1'
             and p.objid = :objid
        into :palletid, :ptype, :pnumber do
    begin
      tpstatus = null;

      select first(1) tp.status
        from wm_task_pallet tp
       where tp.taskid = :tid
             and tp.palletid = :palletid
       order by tp.taskpalletid desc   -- не хорошо
          into :tpstatus;

       suspend;
    end 
  end 
  else if (:sscode = 'L') then
  begin
    -- стеллаж
    for
      select s.siteid, s.name, p.palletid, p.pallettype, p.number
        from site s
             left join pallet p on s.siteid = p.siteid and p.status = '1'
       where s.higher = :sid
       order by s.z_coord descending,s.name descending
        into :siteid, :sname, :palletid, :ptype, :pnumber
    do
    begin
      tpstatus = null;

      if (:palletid is not null) then
      begin
        select first(1) tp.status
          from wm_task_pallet tp
         where tp.taskid = :tid
               and tp.palletid = :palletid
         order by tp.taskpalletid desc   -- не хорошо
          into :tpstatus;

      end 


      suspend;


    end 

  end 
  else
  begin
    exception exc_k_common 'Неверное МП!';
  end 
  --suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_ADDPALLET (
    TASKID type of R_ID,
    SITEID type of R_ID,
    PALLETID type of R_ID,
    WMSESID type of R_ID)
as
declare variable MANID type of R_ID;
begin
  select s.objid
    from wm_session s
   where s.sessionid = :wmsesid
         and s.disconnecttime is null
    into :manid;

  if (:manid is null) then
   exception exc_k_common 'Пользователь не найден!';

  update pallet p
     set p.siteid = :siteid
   where p.palletid = :palletid;

  insert into wm_task_pallet(palletid, siteid, status, taskid, manid)
  values (:palletid, :siteid, '2', :taskid, :manid);

  insert into wm_task_pallet(palletid, siteid, status, taskid, manid)
  values (:palletid, :siteid, 'w', :taskid, :manid);

  --suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_ENDPALLET (
    TID type of R_ID,
    PID type of R_ID,
    WMSESID type of R_ID)
as
declare variable MANID type of R_ID;
begin
  select s.objid
    from wm_session s
   where s.sessionid = :wmsesid
         and s.disconnecttime is null
    into :manid;

  if (:manid is null) then
    exception exc_k_common 'Сотрудник не найден!';

  if (exists(
    select *
      from wm_task_pallet tp
     where tp.taskid = :tid
           and tp.palletid <> :pid
           and tp.status = 'w'
           and tp.manid = :manid
  )) then
    exception exc_k_common 'Есть незавершенные паллеты!';

  update wm_task_pallet tp
     set tp.status = '1'
   where tp.taskid = :tid
         and tp.palletid = :pid
         and tp.manid = :manid
         and tp.status = 'w';

end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_ENDSITE (
    TID type of R_ID,
    SID type of R_ID,
    WMSESID type of R_ID)
as
declare variable MANID type of R_ID;
begin
  select s.objid
    from wm_session s
   where s.sessionid = :wmsesid
         and s.disconnecttime is null
    into :manid;

  if (:manid is null) then
    exception exc_k_common 'Сотрудник не найден!';

  if (not exists(
    select *
      from wm_task_site ts
     where ts.siteid = :sid
           and ts.taskid = :tid
           and ts.status <> '2'
           and ts.manid = :manid
  )) then
    exception exc_k_common 'Произошла ошибка!';

  if (exists(
    select *
      from wm_task_pallet tp
     where tp.taskid = :tid
           and tp.siteid = :sid
           and tp.status = 'w'
           and tp.manid = :manid
  )) then
    exception exc_k_common 'Есть незавершенные паллеты!';

  update wm_task_site ts
     set ts.status = '2',
         ts.endtime = current_timestamp
   where ts.taskid = :tid
         and ts.siteid = :sid
         and ts.manid = :manid;

end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_TRASHREST (
    TASKID type of R_ID,
    WID type of R_ID)
returns (
    TRASHNAME type of R_NAME,
    TRASHREST type of R_QUANTITY)
as
declare variable OBJID type of R_ID;
declare variable TRASHPALLETID type of R_ID;
declare variable ZONEID type of R_ID;
declare variable TRASHSITEID type of R_ID;
begin
  trashrest = 0.0;
  select t.infoid, t.zoneid, gt.sid, gt.pid
    from wm_task t
         left join k_wh_get_trash(t.infoid) gt on 1=1
   where t.taskid = :taskid
    into :objid, :zoneid, :trashsiteid, :trashpalletid;

  select s.name, sum(wli.amount)
    from wareslot wl
         left join wareslotitem wli
              left join pallet p
                   left join site s
                        left join sitezone_items szi on s.siteid = szi.siteid
                     on s.siteid = p.siteid
                on p.palletid = wli.palletid
           on wl.wlotid = wli.wlotid
   where wl.waresid = :wid
         and wli.amount > 0.0001
         and szi.zoneid = :zoneid
         and p.siteid = :trashsiteid
   group by 1
    into :trashname, :trashrest;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_CHECKTASKWARES (
    TASKID type of R_ID,
    WMSESID type of R_ID)
returns (
    WARESID type of R_ID)
as
begin
  select tw.waresid
    from wm_task_Wares tw
   where tw.taskid = :taskid
         and tw.wm_sessionid = :wmsesid
         and tw.status = '1'
    into :waresid;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_L_JOINPAL (
    TID type of R_ID,
    PID type of R_ID,
    WMSESID type of R_ID)
as
declare variable MANID type of R_ID;
declare variable SITEID type of R_ID;
declare variable WID type of R_ID;
declare variable ZONEID type of R_ID;
begin
  select s.objid
    from wm_session s
   where s.sessionid = :wmsesid
         and s.disconnecttime is null
    into :manid;

  if (:manid is null) then
    exception exc_k_common 'Пользователь не найден!';

  select t.zoneid
    from wm_task t
   where t.taskid = :tid
    into :zoneid;
  /*
  select tw.waresid
    from wm_task_wares tw
   where tw.taskid = :tid
         and tw.wm_sessionid = :wmsesid
         and tw.status = '1'
    into :wid;

  if (not exists(
    select *
      from wh_term_invent_tasklwares(:tid,:wid) tlw
     where tlw.palletid = :pid
  )) then
    exception exc_k_common 'Товар на паллете не найден!';
  */
  select p.siteid
    from pallet p
   where p.palletid = :pid
    into :siteid;

  if (not exists(
    select *
      from sitezone_items szi
     where szi.siteid = :siteid
           and szi.zoneid = :zoneid
  )) then
    exception exc_k_common 'Неверная зона паллета!';

  if (exists(
    select *
      from wm_task_pallet tp
     where tp.taskid = :tid
           and tp.palletid <> :pid
           and tp.manid = :manid
           and tp.status = 'w'
  )) then
    exception exc_k_common 'Завершите привязанный паллет!';
  else
  begin
    if (not exists(
      select *
      from wm_task_pallet tp
     where tp.taskid = :tid
           and tp.siteid = :siteid
           and tp.palletid = :pid
           and tp.manid = :manid
           and tp.status = 'w'
    )) then
      insert into wm_task_pallet(taskid,siteid,palletid,status,manid)
      values (:tid,:siteid,:pid,'w',:manid);
  end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_JOINWARES (
    TASKID type of R_ID,
    WARESID type of R_ID,
    WMSESID type of R_ID)
as
declare variable MANID type of R_ID;
declare variable TW_WID type of R_ID;
declare variable TW_STATUS type of R_STATUS;
declare variable TW_WMSESID type of R_ID;
begin
  select s.objid
    from wm_session s
   where s.sessionid = :wmsesid
         and s.disconnecttime is null
    into :manid;

  if (:manid is null) then
    exception exc_k_common 'Пользователь не найден!';

  if (exists(
    select *
      from wm_task t
     where t.taskid = :taskid
           and t.status = '2'
  )) then
    exception exc_k_common 'Задание завершено!';

  select tw.waresid, tw.status, tw.wm_sessionid
    from wm_task_Wares tw
   where tw.taskid = :taskid
         and tw.waresid = :waresid
    into :tw_wid, :tw_status, :tw_wmsesid;

  if (:tw_wid is null) then
    exception exc_k_common 'Товар не найден в задании!';

  if (:tw_status = '1' and :tw_wmsesid <> :wmsesid) then
    exception exc_k_common 'Товар инвентаризируется другим сотрудником!';

  if (exists(
    select *
      from wm_task_Wares tw
     where tw.wm_sessionid = :wmsesid
           and tw.waresid <> :waresid
           and tw.taskid = :taskid
           and tw.status = '1'
  )) then
    exception exc_k_common 'Уже есть привязанный товар!';
  else
  begin
    update wm_task_wares tw
       set tw.status = '1',
           tw.wm_sessionid = :wmsesid
     where tw.waresid = :waresid
           and tw.taskid = :taskid;
  end 


  --suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_WH_INVENT_GETWARES (
    TASKID type of R_ID)
returns (
    TASKWARESID type of R_ID,
    WARESID type of R_ID,
    CODE type of R_CODE,
    NAME type of R_NAME,
    WEIGHTING type of NUMBER,
    QUANTITY type of R_DOUBLE,
    SCANCOUNT type of R_DOUBLE,
    SUCCESSSCAN type of R_DOUBLE,
    SCANQUANT type of R_DOUBLE,
    LASTDATE type of R_DATETIME,
    STATUS type of R_STATUS,
    REST type of R_QUANTITY,
    INVENTQUANT type of R_QUANTITY,
    WGID type of R_ID,
    WGNAME type of R_NAME,
    WGSELCODE type of R_CODE,
    WGSELNAME type of R_NAME,
    DOCQUANT type of R_QUANTITY)
as
declare variable TRASHPALLETID type of R_ID;
declare variable TRASHSITEID type of R_ID;
declare variable OBJID type of R_ID;
begin

  select t.infoid
    from wm_task t
   where t.taskid = :taskid
    into :objid;

  select k.pid,k.sid
    from k_wh_get_trash(:objid) k
    into :trashpalletid,:trashsiteid;

  for
    select tw.taskwaresid,tw.waresid,w.code,w.name, wg.waresgrid, wg.name,
           tw.quantity,tw.scancount,tw.successscan,tw.scanquant,
           tw.lastdate,tw.status,
           coalesce(wlr.rest,0.000),
           coalesce(wr.famount, 0.000),
           wsg.code, wsg.name
      from wm_task_wares tw
           left join gwares w
                left join waresgroup wg on wg.waresgrid = w.waresgroup
                left join k_wares_selgroup wsg on w.selgroup = wsg.id
                left join waresrest wr on wr.waresunitid = w.mainunitid and wr.objid = :objid
             on tw.waresid = w.waresid
           left join wareslotrest wlr on wlr.waresid = tw.waresid and wlr.objid = :objid
     where tw.taskid = :taskid
           and tw.waresid is not null
     order by w.code asc
      into :taskwaresid,:waresid,:code,:name, :wgid, :wgname,
           :quantity,:scancount,:successscan,:scanquant,
           :lastdate,:status,
           :rest,
           :docquant,
           :wgselcode, :wgselname
  do
  begin
    select sum(tl.quantity)
      from wm_task_lot tl
     where tl.taskwaresid = :taskwaresid
           and tl.palletid <> :trashpalletid
      into :inventquant;

    suspend;
  end 


end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_TASKLWARES (
    TASKID type of R_ID,
    WARESID type of R_ID)
returns (
    PALLETID type of R_ID,
    PNUMBER type of R_BARCODE,
    SNAME type of R_NAME,
    IS_INVENT smallint,
    CLIENTID type of R_ID)
as
declare variable OBJID type of R_ID;
declare variable ZONEID type of R_ID;
declare variable TRASHSITEID type of R_ID;
declare variable TRASHPALLETID type of R_ID;
begin
  select t.infoid, t.zoneid
    from wm_task t
   where t.taskid = :taskid
    into :objid, :zoneid;

  select gt.sid, gt.pid
    from k_wh_get_trash(:objid) gt
    into :trashsiteid, :trashpalletid;

  for
    select wli.palletid, p.number, s.name, p.clientid
      from wareslot wl
           left join wareslotitem wli
                left join pallet p
                     left join site s
                          left join sitezone_items szi on s.siteid = szi.siteid
                       on s.siteid = p.siteid
                  on p.palletid = wli.palletid
             on wl.wlotid = wli.wlotid
     where wl.waresid = :waresid
           and wli.amount > 0.0001
           --and p.objid = :objid
           and szi.zoneid = :zoneid
           and p.siteid <> :trashsiteid
      into :palletid, :pnumber, :sname, :clientid do
  begin
    is_invent = 0;
    if (exists(
      select *
        from wm_task_pallet tp
       where tp.taskid = :taskid
             and tp.palletid = :palletid
             and tp.status = '1'

    )) then
      is_invent = 1;
    suspend;
  end 

end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_ENDWARES (
    TID type of R_ID,
    WID type of R_ID,
    WMSESID type of R_ID)
as
begin
  if (exists(
    select *
      from WH_TERM_INVENT_TASKLWARES(:tid,:wid) tlw
     where tlw.is_invent = 0
  )) then
    exception exc_k_common 'Есть незавершенные паллеты!';


  update wm_task_wares tw
     set tw.status = '2'
   where tw.taskid = :tid
         and tw.waresid = :wid
         and tw.wm_sessionid = :wmsesid;


  --suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_TERM_INVENT_CORRECTPALWARES (
    WMSESID type of R_ID,
    PALLETID type of R_ID,
    WUID type of R_ID,
    WARESLOTS varchar(1023),
    AMOUNTS varchar(1023),
    TID type of R_ID)
as
declare variable WORDWLOTID varchar(1023);
declare variable WORDAMOUNT varchar(1023);
declare variable AMOUNT double precision;
declare variable QDIFF double precision;
declare variable WARESID type of R_ID;
declare variable PTRASHID type of R_ID;
declare variable WLID type of R_ID;
declare variable WUFACTOR type of R_ID;
declare variable TWID type of R_ID;
declare variable WLAMOUNT type of R_QUANTITY;
declare variable I smallint;
declare variable WLINCOMEID type of R_ID;
declare variable PTYPE type of R_FLAG;
declare variable ZONEID type of R_ID;
declare variable OBJID type of R_ID;
declare variable SITEID type of R_ID;
BEGIN
  if (exists(
    select *
      from pallet p
     where p.palletid = :palletid
           and p.clientid is not null
  )) then
    exception exc_k_common 'Мультипаллет запрещен к правке!';

  select p.pallettype,p.zoneid,p.objid,p.siteid
    from pallet p
   where p.palletid = :palletid
    into :ptype,:zoneid,:objid,:siteid;

  if (:ptype = '1' and (:zoneid is NULL or :objid is NULL)) then
    select szi.zoneid,sz.objid
      from sitezone_items szi
           left join sitezone sz on sz.zoneid = szi.zoneid
     where szi.siteid = :siteid
      into :zoneid,:objid;

  select wu.factor,wu.waresid
    from waresunit wu
   where wu.waresunitid = :wuid
    into :wufactor,:waresid;

  I = 0;
  FOR
    select r.word
      from r_listwords(:wareslots, ';', 0) r
      into :wordwlotid
  do
  begin
    I = :I + 1;
    wordamount = WORDNUM(:amounts,:I,';','0');

    if (:wordamount is NULL or trim(:wordamount)='') then
        amount = 0.0000;
    else
        amount = cast(:wordamount as double precision);

    amount = :amount * :wufactor;
    if (:amount > 0.0000001) then
        insert into k_wh_siteverify_wareslot_tmp(wareslotid,amount)
        values (cast(:wordwlotid as integer),:amount);
  end


  select pid
    from k_wh_get_trash(:objid)
    into :ptrashid;

  if (:ptrashid is NULL) then
    exception exc_ur_common 'Не найден поддон НЕДОСТАЧА!';

  -- WM_TASK_WARES->QUANTITY : Кол-во, которое было на поддоне
  -- WM_TASK_WARES->SCANQUANT : Кол-во, которое стало на поддоне
  -- WM_TASK_WARES->PALLETID : Поддон

  --qpalletwares = NULL;

  select tw.taskwaresid --,tw.quantity
    from wm_task_wares tw
   where tw.taskid = :tid
         and tw.waresid = :waresid
         --and tw.status = '1'
    into :twid;  --,:qpalletwares;

  if (:twid is null) then
  begin
    insert into wm_task_wares(taskid,waresid,scanquant,status)
    values (:tid,:waresid,0.000,'1')
    returning taskwaresid
    into :twid;
  end 

  /*
  if (:qpalletwares is NULL) then
  begin
      select sum(wli.amount)
        from wareslotitem wli
             left join wareslot wl on wl.wlotid = wli.wlotid
       where wli.palletid = :palletid
         and wl.waresid = :waresid
         and coalesce(wl.objid,:objid) = :objid
         and coalesce(wl.zoneid,:zoneid) = :zoneid
        into :qpalletwares;
    
      update wm_task_wares tw
         set tw.quantity = coalesce(:qpalletwares,0.0000)
       where tw.taskwaresid = :twid;
  end
  */
  -- 1
  -- Сбрасываем не нужные партии в корзину на поддон Недостача
  for
    select wl.wlotid,sum(wli.amount)
      from wareslotitem wli
           left join wareslot wl on wl.wlotid = wli.wlotid
     where wli.palletid = :palletid
       and wl.waresid = :waresid
       and coalesce(wl.objid,:objid) = :objid
       and coalesce(wl.zoneid,:zoneid) = :zoneid
       and not exists(select *
                        from k_wh_siteverify_wareslot_tmp k
                       where k.wareslotid = wl.wlotid
                         and k.amount > 0.000001)
     group by wl.wlotid,wl.productdate
    having sum(wli.amount)>0.00001
      into :wlid,:wlamount
  do
  FOR
    select o.amount,o.wlincomeid
      from core_listwlincomes(:wlid,:palletid,-:wlamount) o
      into :amount,:wlincomeid
  do
  begin
      -- Процедура вернет расходные количества, поэтому при приходовании знак наоборот
      insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
      values(:twid,:wlid,:palletid,:amount,'1',:wlincomeid,:wmsesid);

      insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
      values(:twid,:wlid,:ptrashid,-:amount,'1',:wlincomeid,:wmsesid);
  end

  -- 2
  -- Обрабатываем все партии, которые остались на поддоне
  for
    select k.wareslotid,k.amount
      from k_wh_siteverify_wareslot_tmp k
     where k.amount > 0.000001
      into :wlid,:amount
  do
  begin
    wlamount = NULL;
    select sum(wli.amount)
      from wareslotitem wli
     where wli.wlotid = :wlid and wli.palletid = :palletid
      into :wlamount;
    if (:wlamount is NULL) then wlamount = 0.000;

    qdiff = :amount - :wlamount;
    if (abs(:qdiff)>0.00001) then
    begin
        if (:qdiff < -0.00001) then -- если уменьшилось количество в партии
        begin
          -- Сначала списываем с поддона, а потом ложим на недостачу
          FOR
            select o.amount,o.wlincomeid
              from core_listwlincomes(:wlid,:palletid,:qdiff,'N') o
              into :amount,:wlincomeid
          do
          begin
              -- Процедура вернет расходные количества, поэтому при приходовании знак наоборот
              insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
              values(:twid,:wlid,:palletid,:amount,'2',:wlincomeid,:wmsesid);
        
              insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
              values(:twid,:wlid,:ptrashid,-:amount,'2',:wlincomeid,:wmsesid);
          end
        end
        else
        begin
          -- Теперь наоборот сначала с недостачи
          FOR
            select o.amount,o.wlincomeid
              from core_listwlincomes(:wlid,:ptrashid,-:qdiff,'N') o
              into :amount,:wlincomeid
          do
          begin
              -- Процедура вернет расходные количества, поэтому при приходовании знак наоборот
              insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
              values(:twid,:wlid,:ptrashid,:amount,'2',:wlincomeid,:wmsesid);
        
              insert into wm_task_lot(taskwaresid,wlotid,palletid,quantity,chgwli,wlincomeid,wm_sessionid)
              values(:twid,:wlid,:palletid,-:amount,'2',:wlincomeid,:wmsesid);
          end

        end
    end
  end
  /*
  qpalletwares = NULL;
  select sum(tl.quantity)
    from wm_task_lot tl
   where tl.palletid = :palletid
     and tl.taskwaresid = :twid
    into :qpalletwares;
  if (:qpalletwares is NULL) then qpalletwares = 0.000;
  */
  update wm_task_wares tw
     set tw.status = '1'
   where tw.taskwaresid = :twid;


END^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_HSITE (
    TID type of column WM_TASK.taskid,
    SID type of column SITE.siteid)
returns (
    SITEID type of column SITE.siteid)
AS
declare variable RACK_ID type of column SITE.siteid;
declare variable RACK_SPID type of column SITE.siteid;
declare variable ZONEID type of column SITEZONE.zoneid;
declare variable spCode type of column sitespecies.code ;
begin
    select sp.code
      from site s
           left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
     where s.siteid = :sid
      into :spCode;

    if (:spcode = 'STACK') then
    begin
        siteid = :sid;
        suspend;
        exit;
    end

  select sp.sitespeciesid
    from sitespecies sp
   where sp.code = 'L'
    into :rack_spid;

  select k.sid
    from k_site_parent(:sid,:rack_spid) k
    into :rack_id;

  select t.zoneid
    from wm_task t
   where t.taskid = :tid
    into :zoneid;

  if (not exists(
    select *
      from sitezone_items szi
     where szi.siteid = :sid
           and szi.zoneid = :zoneid
  )) then
    exception exc_k_common 'МП не относится к зоне инвентаризации!';

  if (:rack_id is not null) then
    siteid = :rack_id;
  else if (exists(
    select *
      from site s
           left join sitespecies ss on s.sitespeciesid = ss.sitespeciesid
     where s.siteid = :sid
           and ss.code in ('GATE','E')
  )) then
    siteid = :sid;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_LISTPALLET (
    TID type of R_ID,
    SID type of R_ID,
    WMSESID type of R_ID)
returns (
    SITEID type of R_ID,
    SNAME type of R_NAME,
    PALLETID type of R_ID,
    PTYPE type of R_FLAG,
    PNUMBER type of R_BARCODE,
    TPSTATUS type of R_STATUS)
AS
declare variable MANID type of R_ID;
declare variable SSCODE type of R_CODE;
declare variable OBJID type of R_ID;
declare variable ZONEID type of R_ID;
begin
  /*
  select sp.sitespeciesid
    from sitespecies sp
   where sp.code = 'L'
    into :rack_spid;

  select k.sid
    from k_site_parent(:sid,:rack_spid) k
    into :rack_id;
  */
  select t.infoid, t.zoneid
    from wm_task t
   where t.taskid = :tid
    into :objid, :zoneid;

  select wms.objid
    from wm_session wms
   where wms.sessionid = :wmsesid
    into :manid;

  select ss.code, s.siteid, s.name
    from site s
         left join sitespecies ss on ss.sitespeciesid = s.sitespeciesid
   where s.siteid = :sid
    into :sscode, :siteid, :sname;

  if (:sscode in ('E','GATE','STACK')) then
  begin
    for
      select p.palletid, p.pallettype, p.number
        from pallet p
       where p.siteid = :sid
             and p.status = '1'
             and p.objid = :objid
        into :palletid, :ptype, :pnumber do
    begin
      tpstatus = null;

      select first(1) tp.status
        from wm_task_pallet tp
       where tp.taskid = :tid
             and tp.palletid = :palletid
       order by tp.taskpalletid desc   -- не хорошо
          into :tpstatus;

       suspend;
    end 
  end 
  else if (:sscode = 'L') then
  begin
    -- стеллаж
    for
      select s.siteid, s.name, p.palletid, p.pallettype, p.number
        from site s
             left join pallet p on s.siteid = p.siteid and p.status = '1'
       where s.higher = :sid
       order by s.z_coord descending,s.name descending
        into :siteid, :sname, :palletid, :ptype, :pnumber
    do
    begin
      tpstatus = null;

      if (:palletid is not null) then
      begin
        select first(1) tp.status
          from wm_task_pallet tp
         where tp.taskid = :tid
               and tp.palletid = :palletid
         order by tp.taskpalletid desc   -- не хорошо
          into :tpstatus;

      end 


      suspend;


    end 

  end 
  else
  begin
    exception exc_k_common 'Неверное МП!';
  end 
  --suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TERM_INVENT_JOINSITE (
    TID type of column wm_task.taskid,
    SID type of column SITE.siteid,
    WMSESID type of column WM_SESSION.sessionid)
RETURNS(
    SPCODE type of column sitespecies.code
)
AS
declare variable MANID type of column MAN.manid;
begin
  select s.objid
    from wm_session s
   where s.sessionid = :wmsesid
         and s.disconnecttime is null
    into :manid;

  if (:manid is null) then
    exception exc_k_common 'Пользователь не найден!';

  if (exists(
    select *
      from wm_task_site ts
     where ts.taskid = :tid
           and ts.siteid = :sid
           and ts.manid <> :manid
           and ts.status = '1'
  )) then
    exception exc_k_common 'МП инвентаризируется другим сотрудником!';

  if (exists(
    select *
      from wm_task_site ts
     where ts.taskid = :tid
           and ts.siteid <> :sid
           and ts.manid = :manid
           and ts.status = '1'
  ))
  then
    exception exc_k_common 'Есть незавершенное МП!';
  else
  begin
    if (not exists(   -- проверка при работе из ПК
      select *
      from wm_task_site ts
     where ts.taskid = :tid
           and ts.siteid = :sid
           and ts.manid = :manid
           and ts.status = '1'
    )) then
      insert into wm_task_site(taskid,siteid,status,manid,begintime)
      values (:tid,:sid,'1',:manid,current_timestamp);
  end

  select sp.code
    from site s
         left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
   where s.siteid = :sid
    into :spCode;

  suspend;

end^

SET TERM ; ^

