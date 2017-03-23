

SET TERM ^ ;

CREATE OR ALTER procedure WH_PALLETFG_BARCODEINFO (
    IBARCODE type of column pallet_finishprint.barcode)
returns (
    PAL_ID type of column PALLET.palletid,
    PAL_BARCODE type of column PALLET.barcode,
    PAL_NUM type of column PALLET.number,
    WID type of column GWARES.waresid,
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    PRODUCTDATE type of column pallet_finishprint.productdate,
    BESTBEFOREDATE type of column pallet_finishprint.bestbeforedate,
    QUANTITY type of column pallet_finishprint.quantity,
    PAL_FEATUREID type of column pallet_feature.id,
    PAL_FEATURECODE type of column pallet_feature.CODE,
    PAL_FEATURENAME type of column pallet_feature.name,
    pal_prodlinename type of column fg_prodlines.name)
AS
begin
    select pf.barcode, pf.palletid, pf.number,
           pf.waresid, g.code, g.name,
           pf.productdate, pf.quantity, pf.bestbeforedate,
           f.id, f.code, f.name, pl.name
      from pallet_finishprint pf
           left join gwares g on g.waresid = pf.waresid
           left join pallet_feature f on f.id = pf.pfid
           left join fg_prodlines pl on pl.id_prodline = pf.prodlineid
     where pf.barcode = :ibarcode and pf.enabled = '1'
      into :pal_barcode, :pal_id, :pal_num, :wid, :wcode, :wname,
           :productdate, :quantity, :bestbeforedate,
           :pal_featureid, :pal_featurecode, :pal_featurename, :pal_prodlinename;

    if (:pal_barcode is NULL) then
        select pf.barcode, pf.palletid, pf.number,
               pf.waresid, g.code, g.name,
               pf.productdate, pf.quantity, pf.bestbeforedate
          from pallet p
               left join pallet_finishprint pf
                    left join gwares g on g.waresid = pf.waresid
                 on pf.palletid = p.palletid
         where p.barcode = :ibarcode and p.status <> '2'
          into :pal_barcode, :pal_id, :pal_num, :wid, :wcode, :wname,
               :productdate, :quantity, :bestbeforedate;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYPALLET (
    PBARCODE type of R_BARCODE,
    QUANTITY type of R_DOUBLE,
    IDUSER type of R_ID,
    DTBEG type of R_DATETIME = current_timestamp,
    FEATUREID type of R_ID = null)
AS
declare variable productdate r_date;
declare variable waresid r_id;
declare variable qplan r_double;
declare variable producerid r_id;
declare variable manid r_id;
declare variable mansiteid r_id;
declare variable zoneid r_id;
declare variable whid r_id;
declare variable ttid_income r_id;
declare variable taskid r_id;
declare variable wmsid r_id;
declare variable taskwaresid r_id;
declare variable pnumber r_barcode;
declare variable ptypeid_finishgood r_id;
declare variable palletid r_id;
declare variable wlincomeid r_id;
declare variable wlotid r_id;
declare variable dtid_income r_id;
declare variable docid r_id64;
declare variable cargoid r_id;
begin
    if (:quantity is NULL) then
        exception exc_wh_wrongamount;

    select wh.zoneid, wh.whid, wh.manid
      from wh_user_infoshort(:iduser) wh
      into :zoneid, :whid, :manid;

    select pfp.productdate, pfp.waresid, pfp.quantity, pfp.producerid, pfp.number,
           coalesce(pfp.dtid_income, pl.dtid_income, p.dtid_income_print, p.dtid_income)
      from pallet_finishprint pfp
           left join fg_producer p on p.objid = pfp.producerid
           left join fg_prodlines pl on pl.id_prodline = pfp.prodlineid
     where pfp.barcode = :pbarcode and pfp.enabled = '1'
      into :productdate, :waresid, :qplan, :producerid, :pnumber, :dtid_income;

    execute procedure WH_INCOMEFG_BYPALLET_FUNDINCOME(:producerid, :whid, :waresid, :productdate, :quantity);
    select k.sid
      from k_get_user_wmsessionid(:manid, 'M') k
      into :wmsid;

    select m.siteid
      from wh_man_getsite(:manid) m
      into :mansiteid;

    execute procedure wh_ttid_incomefg
     returning_values :ttid_income;

    insert into wm_task(tasktypeid, zoneid, status, siteid)
    values(:ttid_income, :zoneid, '0', :mansiteid)
    returning taskid
    into :taskid;

    select wh.id
      from wh_paltypeid_finishgood wh
      into :ptypeid_finishgood;

    insert into pallet(ptypeid, barcode, number, siteid, zoneid, objid)
    values(:ptypeid_finishgood, :pbarcode, :pnumber, :mansiteid, :zoneid, :whid)
    returning palletid
    into :palletid;

    if (:featureid is NOT NULL) then
        execute procedure wh_pallet_feature_set(:palletid, :featureid, :manid, 'M');

    update wm_task t
       set t.wm_sessionid = :wmsid, t.begintime = :dtbeg, t.status = '1'
     where t.taskid = :taskid;

    insert into wm_task_pallet(taskid, palletid, status)
    values(:taskid, :palletid, '2');

    update or insert into wareslot(objid, zoneid, waresid, productdate, status)
    values(:whid, :zoneid, :waresid, :productdate, '1')
    matching(objid, zoneid, waresid, productdate)
    returning wlotid
    into :wlotid;

    select first(1) d.docid
      from document d
     where d.doctype = :dtid_income
       and d.fromobj = :producerid
       and d.toobj = :whid
       and d.status = 'c'
       and d.docdate = cast(:dtbeg as date)
      into :docid;

    if (:docid is NULL) then
    begin
        select k.docid
          from k_doccreate(:producerid, :whid, NULL, :dtid_income,
                           cast(:dtbeg as date), cast(:dtbeg as date),
                           NULL, NULL, null, NULL, NULL) k
          into :docid;

        update document d
           set d.status = 'c'
         where d.docid = :docid;
    end

    update or insert into wareslotincomes(docid, wlotid)
    values(:docid, :wlotid)
    matching(docid, wlotid)
    returning id
    into :wlincomeid;

    insert into wm_task_wares(taskid, waresid, status, wm_sessionid, successscan, quantity, begintime)
    values(:taskid, :waresid, '1', :wmsid, :qplan, :quantity, :dtbeg)
    returning taskwaresid
    into :taskwaresid;

    insert into wm_task_lot(palletid,  wlotid, taskwaresid, chgwli, wlincomeid, quantity)
    values(:palletid, :wlotid, :taskwaresid, '1', :wlincomeid, :quantity);

    update wm_task_wares tw
       set tw.status='2',tw.endtime = current_timestamp
     where tw.taskwaresid = :taskwaresid;

    update wm_task t
       set t.status = '2',t.docid = :docid
     where t.taskid = :taskid;

    execute procedure k_get_cargoid(:docid, :waresid)
      returning_values :cargoid;

    if (:cargoid is NULL) then
        insert into cargo(document, waresid, amount, price)
        values(:docid, :waresid, :quantity, 0.000);
    else
        update cargo cg
           set cg.amount = cg.amount + :quantity
         where cg.cargoid = :cargoid;

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_PALLETFP_INFO (
    ID type of column pallet.palletid)
returns (
    PAL_ID type of column PALLET.palletid,
    PAL_NUM type of column PALLET.number,
    PAL_BARCODE type of column PALLET.barcode,
    PAL_STAT type of column PALLET.status,
    PAL_SID type of column SITE.siteid,
    PAL_SCURCNT type of column site_stack.palcurcnt,
    PAL_SMAXCNT type of column site_stack.palmaxcnt,
    PAL_SNAME type of column SITE.name,
    PAL_SPCODE type of column sitespecies.code,
    PAL_OBJID type of column OBJECT.objid,
    PAL_TCANMOVE type of column pallet_type.canmove,
    PAL_TCODE type of column pallet_type.code,
    PAL_N type of column pallet.num,
    PAL_FEATUREID type of column pallet_feature.id,
    PAL_FEATURECODE type of column pallet_feature.code,
    PAL_FEATURENAME type of column pallet_feature.name,
    PAL_PRODLINENAME type of column fg_prodlines.name,
    WID type of column GWARES.waresid,
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    PRODUCTDATE type of column pallet_finishprint.productdate,
    BESTBEFOREDATE type of column pallet_finishprint.bestbeforedate,
    WQPLAN type of column pallet_finishprint.quantity,
    WQ type of column wareslotitem.amount,
    PRODUCERID type of column fg_producer.objid,
    PRODUCERNAME type of r_varchar255,
    VUFACTOR type of column waresunit.factor,
    VUCODE type of column UNIT.shortname,
    MUFACTOR type of column waresunit.factor,
    MUCODE type of column UNIT.shortname,
    WSID type of column SITE.siteid,
    WSNAME type of column SITE.name,
    REC_SID type of column SITE.siteid,
    REC_SNAME type of column SITE.name)
AS
begin
    select p.palletid, p.number, p.barcode, p.status, p.objid,
           s.siteid, s.name, sp.code, pt.code, p.num,
           case
                when coalesce(p.num,0) < coalesce(ss.palcurcnt,0) then '0'
                else pt.canmove
           end, ss.palcurcnt, ss.palmaxcnt, pf.id, pf.code, pf.name
      from pallet p
           left join site s on s.siteid=p.siteid
           left join sitespecies sp on sp.sitespeciesid=s.sitespeciesid
           left join pallet_type pt on pt.id = p.ptypeid
           left join site_stack ss on ss.siteid = p.siteid
           left join pallet_feature pf on pf.id = p.featureid
     where p.palletid = :id
      into :pal_id, :pal_num, :pal_barcode, :pal_stat, :pal_objid,
           :pal_sid, :pal_sname, :pal_spcode, :pal_tcode, :pal_n, :pal_tcanmove,
           :pal_scurcnt, :pal_smaxcnt,
           :pal_featureid, :pal_featurecode, :pal_featurename;

    select pf.waresid, g.code, g.name,
           pf.productdate, pf.quantity, pf.bestbeforedate,
           pf.producerid,
           vwu.factor, vu.shortname, mwu.factor, mu.shortname,
           pl.name
      from pallet_finishprint pf
           left join fg_prodlines pl on pl.id_prodline = pf.prodlineid
           left join gwares g
                left join waresunit vwu
                     left join unit vu on vu.unitid = vwu.unitid
                  on vwu.waresunitid = g.viewunitid
                left join waresunit mwu
                     left join unit mu on mu.unitid = mwu.unitid
                  on mwu.waresunitid = g.mainunitid
             on g.waresid = pf.waresid
     where pf.palletid = :id
      into :wid, :wcode, :wname,
           :productdate, :wqplan, :bestbeforedate,
           :producerid,
           :vufactor, :vucode, :mufactor, :mucode,
           :pal_prodlinename;

    select fullname
      from getobjectname(:producerid,'03')
      into :producername;

    select sum(wli.amount)
      from wareslotitem wli
     where wli.palletid = :pal_id
      into :wq;

    select wso.siteid, s.name
      from wares_select_options wso
           left join site s on s.siteid = wso.siteid
     where wso.objid = :pal_objid and wso.waresid = :wid
      into :wsid, :wsname;

    if (:pal_spcode <> 'STACK') then
    begin
        select first(1) ss.siteid, s.name
          from site_stack ss
               left join site s on s.siteid = ss.siteid
         where ss.waresid = :wid
           and ss.productdate = :productdate
           and ss.bestbeforedate = :bestbeforedate
           and coalesce(ss.palcurcnt,0) < coalesce(ss.palmaxcnt, 0)
           and ss.palfeatureid = :pal_featureid
          into :rec_sid, :rec_sname;

        if (:rec_sid is NULL) then
        begin
            select first(1) sw.siteid, s.name
              from MODEL_STACK_REF_WARESID w
                   left join MODEL_STACK_REF_SITE_WARES sw
                        left join site_stack ss on ss.siteid = sw.siteid
                        left join site s on s.siteid = sw.siteid
                     on sw.waresid = w.waresid and sw.modelid = w.modelid
             where w.waresid = :wid
               and ss.waresid is NULL
             order by w.priority ascending, sw.palletcount descending, s.name ascending
              into :rec_sid, :rec_sname;
        end
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_STACKWARES_LISTAVAIL (
    SID type of R_ID,
    WID type of R_ID)
returns (
    MODELID R_ID,
    MODELNAME R_NAME)
AS
begin
    select first(1) ms.modelid, ms.name
      from model_stack_ref_site_wares sw
           left join model_stack ms on ms.modelid = sw.modelid
     where sw.siteid = :sid
       and sw.waresid = :wid
     order by sw.palletcount descending
      into :modelid, :modelname;

    if (:modelid is NOT NULL) then
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_STACKMODEL_INFO (
    ID type of column model_stack.modelid
)
returns (
    STACKMODELID type of column model_stack.modelid,
    STACKMODELNAME type of column model_stack.name
)
as
begin
    select ms.modelid, ms.name
      from model_stack ms
     where ms.modelid = :id
      into :stackmodelid, :stackmodelname;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_FGPRODLINE_INFO (
    ID type of column fg_prodlines.id_prodline
)
returns (
    PRODLINEID type of column fg_prodlines.id_prodline,
    PRODLINENAME type of column fg_prodlines.name
)
as
begin
    select p.id_prodline, p.name
      from fg_prodlines p
     where p.id_prodline = :id
      into :prodlineid, :prodlinename;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_FGPRODLINE_PRODUCER_LIST (
    ID type of column fg_prodlines.id_prodline
)
returns (
    OBJID type of R_ID,
    CODE type of R_CODE25,
    OBJFULLNAME type of R_FULLNAME)
AS
declare variable producers type of column fg_prodlines.listproducers;
begin
    select pl.listproducers
      from fg_prodlines pl
     where pl.id_prodline = :id
      into :producers;

    for
        select p.objid, p.code,  gon.fullname
          from r_listwords(:producers, ',', 0) r
               left join fg_producer p
                    left join getobjectname(p.objid, '3') gon on 1 = 1
                 on p.objid = cast(r.word as r_id)
          into :objid, :code, :objfullname
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FGPRODLINE_PRODUCER_LIST (
    ID type of column fg_prodlines.id_prodline
)
returns (
    OBJID type of R_ID,
    CODE type of R_CODE25,
    OBJFULLNAME type of R_FULLNAME)
AS
declare variable producers type of column fg_prodlines.listproducers;
begin
    select pl.listproducers
      from fg_prodlines pl
     where pl.id_prodline = :id
      into :producers;

    for
        select p.objid, p.code,  gon.fullname
          from r_listwords(:producers, ',', 0) r
               left join fg_producer p
                    left join getobjectname(p.objid, '3') gon on 1 = 1
                 on p.objid = cast(r.word as r_id)
         where p.objid is NOT NULL
          into :objid, :code, :objfullname
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FGPRODLINE_INFO (
    ID type of column fg_prodlines.id_prodline
)
returns (
    PRODLINEID type of column fg_prodlines.id_prodline,
    PRODLINENAME type of column fg_prodlines.name,
    PRODLINECHGDATE type of column fg_prodlines.chgdate
)
as
begin
    select p.id_prodline, p.name, p.chgdate
      from fg_prodlines p
     where p.id_prodline = :id
      into :prodlineid, :prodlinename, :prodlinechgdate;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_FGPRODUCER_INFO (
    ID type of column fg_producer.objid
)
returns (
    PRODUCERID type of column fg_producer.objid,
    PRODUCERNAME type of r_varchar255
)
as
begin
    select p.objid, (select objname from wh_get_objectname(p.objid))
      from fg_producer p
     where p.objid = :id
      into :PRODUCERid, :PRODUCERname;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYSTACK (
    TASKID type of R_ID,
    STACKID type of R_ID,
    WARESID type of R_ID,
    MODELID type of R_ID,
    LINEID type of R_ID,
    PRODUCERID type of R_ID,
    PCNT type of R_NUMBER,
    PQ type of R_DOUBLE,
    PRODUCTDATE type of R_DATE,
    BESTBEFOREDATE type of R_DATE,
    IDUSER type of R_ID,
    DTBEG type of R_DATETIME = current_timestamp)
AS
declare variable i type of R_NUMBER;
declare variable WHID type of R_ID;
declare variable ZONEID type of R_ID;
declare variable MANID type of R_ID;
declare variable PNUMBER type of R_BARCODE;
declare variable PBARCODE type of R_BARCODE;
declare variable wmsid r_id;
declare variable taskwaresid r_id;
declare variable ptypeid_finishgood r_id;
declare variable palletid r_id;
declare variable wlincomeid r_id;
declare variable wlotid r_id;
declare variable docid r_id64;
declare variable cargoid r_id;
begin
  if (:pq is NULL) then
      exception exc_wh_wrongamount;

  if (not exists(select *
                   from site s
                        left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                  where s.siteid = :stackid
                    and sp.code = 'STACK')) then
      exception exc_wh_wrongsitetype;

  execute procedure WH_INCOMEFG_BYPALLET_FUNDINCOME(:producerid, :whid, :waresid, :productdate, :pq*:pcnt);

  select t.docid
    from wm_task t
   where t.taskid = :taskid
    into :docid;

  select wh.zoneid, wh.whid, wh.manid
    from wh_user_infoshort(:iduser) wh
    into :zoneid, :whid, :manid;

  select k.sid
    from k_get_user_wmsessionid(:manid, 'M') k
    into :wmsid;

  select wh.id
    from wh_paltypeid_finishgood wh
    into :ptypeid_finishgood;

  update or insert into wareslot(objid, zoneid, waresid, productdate, status)
  values(:whid, :zoneid, :waresid, :productdate, '1')
  matching(objid, zoneid, waresid, productdate)
  returning wlotid
  into :wlotid;

  update or insert into wareslotincomes(docid, wlotid)
  values(:docid, :wlotid)
  matching(docid, wlotid)
  returning id
  into :wlincomeid;


  insert into site_stack(siteid, modelid, waresid, productdate, bestbeforedate)
  values( :stackid, :modelid, :waresid, :productdate, :bestbeforedate);

  i = 0;

  while (i < :pcnt) do
  begin
    insert into pallet_finishprint (manid, prodlineid, waresid, productdate, quantity, bestbeforedate, producerid)
    values (:manid, :lineid, :waresid, :productdate, :pq, :bestbeforedate, :producerid)
    returning number, barcode
    into :pnumber, :pbarcode;

    insert into pallet(ptypeid, barcode, number, siteid, zoneid, objid, status)
    values(:ptypeid_finishgood, :pbarcode, :pnumber, :stackid, :zoneid, :whid, '0')
    returning palletid
    into :palletid;

    insert into wm_task_pallet(taskid, palletid, status)
    values(:taskid, :palletid, '2');

    select tw.taskwaresid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.waresid = :waresid
      into :taskwaresid;

    if (:taskwaresid is Null) then
        insert into wm_task_wares(taskid, waresid, status, wm_sessionid, successscan, quantity, begintime)
        values(:taskid, :waresid, '1', :wmsid, :pq, :pq, :dtbeg)
        returning taskwaresid
        into :taskwaresid;
    else
        update wm_task_wares tw
           set tw.status='2',
               tw.successscan = coalesce(tw.successscan,0.000) + :pq,
               tw.quantity = coalesce(tw.quantity,0.000) + :pq,
               tw.begintime = :dtbeg,
               tw.endtime = current_timestamp,
               tw.wm_sessionid = :wmsid
         where tw.taskwaresid = :taskwaresid;

    insert into wm_task_lot(palletid,  wlotid, taskwaresid, chgwli, wlincomeid, quantity, wm_sessionid)
    values(:palletid, :wlotid, :taskwaresid, '1', :wlincomeid, :pq, :wmsid);

    execute procedure k_get_cargoid(:docid, :waresid)
      returning_values :cargoid;

    if (:cargoid is NULL) then
        insert into cargo(document, waresid, amount, price)
        values(:docid, :waresid, :pq, 0.000);
    else
        update cargo cg
           set cg.amount = cg.amount + :pq
         where cg.cargoid = :cargoid;
    
    i = :i + 1;
  end
end^

SET TERM ; ^



CREATE TABLE SITEOPTION (
    ID R_ID NOT NULL,
    CODE R_CODE NOT NULL,
    NAME R_NAME NOT NULL,
    WITHCHILDREN R_FLAG NOT NULL);

ALTER TABLE SITEOPTION
ADD CONSTRAINT PK_SITEOPTION
PRIMARY KEY (ID);

CREATE SEQUENCE GEN_SITEOPTION_ID;

SET TERM ^ ;

create trigger siteoption_bi for siteoption
active before insert position 0
as
begin
  if (new.id is null) then
    new.id = gen_id(gen_siteoption_id,1);
end^

SET TERM ; ^



CREATE TABLE SITE_OPTIONS (
    SITEID R_ID NOT NULL,
    OPTIONID R_ID NOT NULL);

ALTER TABLE SITE_OPTIONS
ADD CONSTRAINT PK_SITE_OPTIONS
PRIMARY KEY (SITEID,OPTIONID);



ALTER TABLE SITE_OPTIONS
ADD CONSTRAINT FK_SITE_OPTIONS_SITEID
FOREIGN KEY (SITEID)
REFERENCES SITE(SITEID)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE SITE_OPTIONS
ADD CONSTRAINT FK_SITE_OPTIONS_OPTIONID
FOREIGN KEY (OPTIONID)
REFERENCES SITEOPTION(ID)
ON DELETE CASCADE
ON UPDATE CASCADE;



CREATE UNIQUE INDEX SITEOPTION_IDX_CODE
ON SITEOPTION (CODE);



SET TERM ^ ;

CREATE trigger site_options_ai0 for site_options
active after insert position 0
AS
begin
    if (exists(select *
                 from siteoption so
                where so.id = new.optionid
                  and so.withchildren = '1'
    )) then
    begin
        insert into site_options ( SITEID, OPTIONID)
        select s.siteid, new.optionid
          from site s
         where s.higher = new.siteid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE trigger site_options_ad0 for site_options
active after delete position 0
AS
declare variable siteid type of column site.siteid;
begin
    if (exists(select *
                 from siteoption so
                where so.id = old.optionid
                  and so.withchildren = '1'
    )) then
    begin
        for
            select s.siteid
              from site s
             where s.higher = old.siteid
              into :siteid
        do
            delete from site_options sos
             where sos.siteid = :siteid and sos.optionid = old.optionid;
    end
end^

SET TERM ; ^



ALTER TABLE SITE_CSS
ADD BLOCKSIZE R_SHORTNUMBER;

CREATE GLOBAL TEMPORARY TABLE WH_TBLTMP_SITE (
    SITEID         R_ID /* R_ID = INTEGER */,
    HIGHER         R_ID /* R_ID = INTEGER */,
    OBJID          R_ID /* R_ID = INTEGER */,
    SITESPECIESID  R_ID /* R_ID = INTEGER */,
    NAME           R_NAME /* R_NAME = VARCHAR(80) */,
    SLENGTH        R_DIMENSION /* R_DIMENSION = DOUBLE PRECISION CHECK(VALUE > 0 OR VALUE IS NULL) */,
    SWIDTH         R_DIMENSION /* R_DIMENSION = DOUBLE PRECISION CHECK(VALUE > 0 OR VALUE IS NULL) */,
    SHEIGHT        R_DIMENSION /* R_DIMENSION = DOUBLE PRECISION CHECK(VALUE > 0 OR VALUE IS NULL) */,
    X              R_COORD_INT /* R_COORD_INT = INTEGER */,
    Y              R_COORD_INT /* R_COORD_INT = INTEGER */,
    Z              R_COORD_INT /* R_COORD_INT = INTEGER */,
    VIEWNAME       R_FULLNAME /* R_FULLNAME = VARCHAR(255) */,
    CLASSNAME      R_NAME /* R_NAME = VARCHAR(80) */,
    SUBTYPE        R_FLAG /* R_FLAG = CHAR(1) */,
    PALLETVOLUME   R_DOUBLE /* R_DOUBLE = DOUBLE PRECISION */
) ON COMMIT DELETE ROWS;



SET TERM ^ ;

create or alter procedure WH_UTIL_SITENAME_SPLIT (
    SITENAME R_NAME,
    SEPARATOR varchar(1),
    ERRSYMBOL varchar(1) = null)
returns (
    ROWNAME R_NAME,
    RACKNAME varchar(3),
    SBNAME varchar(2),
    SBNAME2 varchar(1))
as
declare variable WORD type of R_NAME;
declare variable I type of R_SHORTNUMBER = 1;
begin
    for
        select r.word
          from r_listwords(:sitename, :separator, 0) r
          into :word
    do
    begin
        if (:i = 1) then
            rowname = :word;
        else if (:i = 2) then
        begin
            if (strlen(:word) > 3) then
            begin
                if (:errsymbol is NOT NULL) then
                    rackname = :errsymbol;
                else
                    exception exc_k_common :sitename;
            end
            else
            begin
                rackname = :word;
            end
        end
        else if (:i = 3) then
        begin
            if (strlen(:word) > 2) then
            begin
                if (:errsymbol is NOT NULL) then
                    sbname = :errsymbol;
                else
                    exception exc_k_common :sitename;
            end
            else
            begin
                sbname = :word;
            end
        end
        else
        begin
            if (strlen(:word) > 1) then
            begin
                if (:errsymbol is NOT NULL) then
                    sbname2 = :errsymbol;
                else
                    exception exc_k_common :sitename;
            end
            else
            begin
                sbname2 = :word;
            end
        end

        i = :i + 1;
    end

    if (:rackname is NOT NULL) then
        rackname = padleft(:rackname, 3, '0');
    if (:sbname is NOT NULL) then
        sbname = padleft(:sbname, 2, '0');
    if (:sbname2 is NOT NULL) then
        sbname2 = padleft(:sbname2, 1, '0');

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_UTIL_SITENAME_RIGHT (
    INAME R_NAME,
    SEPSYM R_FLAG = '-')
returns (
    ONAME R_NAME)
as
begin
    select w.rowname ||
           iif(w.rackname is NOT NULL, :sepsym || w.rackname, '') ||
           iif(w.sbname is NOT NULL, :sepsym || w.sbname, '') ||
           iif(w.sbname2 is NOT NULL, :sepsym || w.sbname2, '')
      from wh_util_sitename_split(:iname, :sepsym) w
      into :oname;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_PALTYPEID_VIRTUAL
returns (
    ID type of R_ID,
    CODE type of R_CODE,
    NAME type of R_NAME)
as
begin
    select pt.id, pt.code, pt.name
      from pallet_type pt
     where pt.code = 'V'
      into :id, :code, :name;

    if (:id is NULL) then
        execute procedure r_raiseerror('PALLETTYPE_NOTFOUND','V');

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_UTIL_RACK_REFORM (
    RACKID R_ID,
    SLOTS R_VARCHAR255,
    STORAGES R_VARCHAR255,
    FLAGS varchar(10) = 'SB')
as
declare variable RACKNAME type of R_NAME;
declare variable SNAME type of R_NAME;
declare variable SNAME_OLD type of R_NAME;
declare variable SNAME_NEW type of R_NAME;
declare variable SNUM type of R_NUMBER;
declare variable STORAGESPID type of R_ID;
declare variable SLOTSPID type of R_ID;
declare variable ZCOORD type of R_NUMBER;
declare variable XCOORD type of R_NUMBER;
declare variable Z type of R_NUMBER;
declare variable SNMIN type of R_NUMBER;
declare variable SNMAX type of R_NUMBER;
declare variable SHEIGHT type of R_NUMBER;
declare variable SWIDTH type of R_NUMBER;
declare variable CNT type of R_NUMBER;
declare variable RACKNAMELENGTH type of R_NUMBER;
declare variable SITEID_DEL type of R_ID;
declare variable SITEID type of R_ID;
declare variable SPID type of R_ID;
declare variable OBJID type of R_ID;
declare variable RACKHEIGHT type of R_ID;
declare variable PALLETVOLUME type of R_DOUBLE;
declare variable SITESPID type of R_ID;
declare variable HIGHER type of R_ID;
declare variable RACKW type of R_DOUBLE;
declare variable RACKL type of R_DOUBLE;
declare variable PTID_VIRTUAL type of R_ID;
declare variable SEPSYM type of R_FLAG = '-';
declare variable BSIZE type of R_SHORTNUMBER = 6;
declare variable WITHCHILD type of R_CODE3;
declare variable DIRECTINDEX type of R_FLAG;
declare variable ZONEID type of R_ID;
begin
    select wmc.siteid_delpallets
      from wm_config wmc
      into :siteid_del;

    select s.name, s.objid, s.swidth, s.slength
      from site s
     where s.siteid = :rackid
      into :rackname, :objid, :rackw, :rackl;

    with recursive t as (
    select siteid,s.higher,1 AS lvl
      from site s
     where s.siteid = :rackid
    union all
    select siteid, s.higher, (t.lvl + 1) as lvl
      from site s
      join t on t.higher = s.siteid)
    select first(1) sc.blocksize
      from t
           join site_css sc on sc.siteid = t.siteid
      into :bsize;
    if (:bsize is NULL) then bsize = 6;


    with recursive t as (
    select siteid,s.higher
      from site s
     where s.siteid = :rackid
    union all
    select siteid, s.higher
      from site s
      join t on t.higher = s.siteid)
    select first(1) t.higher
      from t
     where t.higher = :siteid_del
      into :higher;
    if (:higher is not null) then
      exception exc_k_common 'Невозможно изменить! Данный стеллаж находиться в удаленных МП';

    select sp.sitespeciesid
      from sitespecies sp
     where sp.code = 'S'
      into :slotspid;

    if (:flags containing 'S') then
    begin
        insert into wh_tbltmp_site(name, SITESPECIESID, SHEIGHT, SLENGTH, SWIDTH)
        select :rackname || :sepsym || r.word, :slotspid, :bsize, :rackl, :rackl
          from r_listwords(:slots,',',0) r;
    end
    else
    begin
        insert into wh_tbltmp_site(name, SITESPECIESID, SHEIGHT, SLENGTH, SWIDTH)
        select s.name, s.sitespeciesid, :bsize, :rackl, :rackw
          from site s
         where s.higher = :rackid
           and s.sitespeciesid = :slotspid;
    end

    select sp.sitespeciesid
      from sitespecies sp
     where sp.code = 'B'
      into :storagespid;
    if (:flags containing 'B') then
    begin
        insert into wh_tbltmp_site(name, SITESPECIESID, SHEIGHT, SLENGTH, SWIDTH)
        select :rackname || '-' || r.word, :storagespid, :bsize, :bsize, :bsize
          from r_listwords(:storages,',',0) r;
    end
    else
    begin
        insert into wh_tbltmp_site(name, SITESPECIESID, SHEIGHT, SLENGTH, SWIDTH)
        select s.name, s.sitespeciesid, :bsize, :bsize, :bsize
          from site s
         where s.higher = :rackid
           and s.sitespeciesid = :storagespid;
    end

    if (not exists(select * from wh_tbltmp_site) and :rackid is NOT NULL) then
    begin
        if (:siteid_del is NOT NULL) then
            update site s
               set s.higher = :siteid_del, s.status = '0'
             where s.siteid = :rackid;
        else
            delete from site s
             where s.siteid = :rackid;

        exit;
    end

    racknamelength = strlen(:rackname);
    zcoord = 1;
    for
        select s.name, rn.sbname, s.sheight, s.swidth
          from wh_tbltmp_site s
               left join wh_util_sitename_split(s.name, :sepsym) rn on 1=1
         order by cast(rn.sbname as r_number) ascending, cast(rn.sbname2 as r_number) ascending
          into :sname, :snum, :sheight, :swidth
    do
    begin
        
        snmin = floor(cast(:snum-1  as double precision)/ 10) * 10 + 1;
        snmax = ceil(cast(:snum as double precision) / 10) * 10;

        cnt = NULL;
        select count(distinct rn.sbname)
          from wh_tbltmp_site st
               left join wh_util_sitename_split(st.name, :sepsym) rn on 1=1
         where cast(rn.sbname as r_number) between :snmin and :snmax
          into :cnt;
        sheight = :sheight / :cnt;
        palletvolume = round(1.0000 / :cnt, 6);

        cnt = NULL; xcoord = NULL; z=NULL;
        select count(distinct st.name),max(st.x + st.swidth),min(st.z)
          from wh_tbltmp_site st
               left join wh_util_sitename_split(st.name, :sepsym) rn on 1=1
         where cast(rn.sbname as r_number) = :snum
          into :cnt, :xcoord, :z;
        swidth = :swidth / :cnt;
        palletvolume = round(:palletvolume / :cnt, 6);

        update wh_tbltmp_site st
           set st.sheight = :sheight,
               st.swidth = :swidth,
               st.z = coalesce(:z,:zcoord),
               st.x = coalesce(:xcoord,1)
--               st.palletvolume = :palletvolume
         where st.name = :sname;

        if (:z is NULL) then
            zcoord  = :zcoord + :sheight;
    end

    rackheight = :zcoord - 1;

    -- Стандартизируем названия старых местоположений
    for
        select s.siteid, s.name
          from site s
         where s.higher = :rackid
          into :siteid, :sname_old
    do
    begin
        select oname
          from wh_util_sitename_right(:sname_old, :sepsym)
          into :sname_new;

        update site s
           set s.name = :sname_new
         where s.siteid = :siteid
           and s.name <> :sname_new;
    end

    -- Стандартизируем названия новых местоположений
    for
        select s.name
          from wh_tbltmp_site s
         where s.higher = :rackid
          into :sname_old
    do
    begin
        select oname
          from wh_util_sitename_right(:sname_old, :sepsym)
          into :sname_new;

        update wh_tbltmp_site s
           set s.name = :sname_new
         where s.name = :sname_old
           and s.name <> :sname_new;
    end

    -- Удаляем не нужные старые местоположения
    for
        select s.siteid--, substring(s.name from :racknamelength+2)
          from site s
         where s.higher = :rackid
           and not exists(select *
                            from wh_tbltmp_site st
                           where st.name = s.name)
          into :siteid--, :snum
    do
    begin
        if (:siteid_del is NULL) then
            delete from site s
             where s.siteid = :siteid;
        else
            update site s
               set s.higher = :siteid_del, s.status = '0'
             where s.siteid = :siteid;
    end


    -- Изменяем старые и добавляем новые
    select id
      from wh_paltypeid_virtual
      into :ptid_virtual;

    for
        select st.name, st.sheight, st.z, st.swidth, st.x, st.sitespeciesid, st.palletvolume
          from wh_tbltmp_site st
          into :sname, :sheight, :zcoord, :swidth, :xcoord, :spid, :palletvolume
    do
    begin
        siteid = Null;
        select s.siteid,s.sitespeciesid
          from site s
         where s.name = :sname
           and s.higher = :rackid
          into :siteid,:sitespid;

        if (:siteid is NULL) then
        begin
            with recursive t as (
                select s.siteid, s.name, s.higher, s.sitespeciesid
                  from site s
                 where s.name = :sname
                 union all
                 select t.siteid, t.name, s.higher, t.sitespeciesid
                   from site s
                        join t on t.higher = s.siteid
            )
            select first(1) t.siteid, t.sitespeciesid
              from t
             where t.higher = :siteid_del
               and t.name = :sname
              into :siteid,:sitespid;

/*            select s.siteid,s.sitespeciesid
              from site s
             where s.higher = :siteid_del
               and s.name = :sname
              into :siteid,:sitespid;*/
        end

        if (:siteid is NULL) then
        begin
            select s.siteid, s.sitespeciesid
              from site s
                   left join wh_util_sitename_right(s.name) sr on 1=1
             where s.higher = :siteid_del
               and sr.oname = :sname
              into :siteid,:sitespid;
        end

        if (:siteid is NULL) then
        begin
            insert into site(higher, name, status, sitespeciesid, x_coord, y_coord, z_coord, sheight, slength, swidth, objid)
            select :rackid, st.name, '1', st.sitespeciesid, st.x, st.y, st.z, st.sheight, st.slength, st.swidth, :objid
              from wh_tbltmp_site st
             where st.name = :sname;

        end
        else
        begin
            if (:sitespid = :spid) then
            begin
                update site s
                   set s.sheight = :sheight,
                       s.z_coord = :zcoord,
                       s.swidth = :swidth,
                       s.x_coord = :xcoord,
                       s.sitespeciesid = :spid,
                       s.higher = :rackid,
--                       s.palletvolume = :palletvolume,
                       s.status = '1',
                       s.name = :sname
                 where s.siteid = :siteid;
            end
            else if (not exists(select *
                                  from pallet p
                                       left join wareslotitem wli on wli.palletid = p.palletid
                                 where p.siteid = :siteid
                                   and wli.amount is NOT NULL)) then
            begin
                if (:spid = :slotspid) then
                begin
                    update pallet p
                       set p.siteid = :siteid, p.number = NULL, p.barcode = 'V'||:siteid
                     where p.siteid = :siteid_del and p.number = '(' || :sname || ')' and p.ptypeid = :ptid_virtual;
                end
                else if (:sitespid = :slotspid) then
                begin
                    update pallet p
                       set p.siteid = :siteid_del, p.number = '(' || :sname || ')'
                     where p.siteid = :siteid and p.ptypeid = :ptid_virtual;
                end

                update site s
                   set s.sheight = :sheight,
                       s.z_coord = :zcoord,
                       s.swidth = :swidth,
                       s.x_coord = :xcoord,
                       s.sitespeciesid = :spid,
                       s.name = :sname,
                       s.higher = :rackid,
--                       s.palletvolume = :palletvolume,
                       s.status = '1'
                 where s.siteid = :siteid;
            end
            else
            begin
                exception exc_wh_wrongpallet 'Нельзя поменять тип местоположения: '||:siteid;
            end
        end
    end

    update site s
       set s.sheight = :rackheight
     where s.siteid = :rackid;

    -- Привяжем зоны
    for
        select szi.withchild, szi.zoneid, szi.directindex
          from sitezone_items szi
         where szi.siteid = :rackid
          into :withchild, :zoneid, :directindex
    do
      insert into sitezone_items(siteid,zoneid,withchild,directindex)
      select s.siteid,:zoneid,:withchild,:directindex
        from site s
             left join sitespecies ss on ss.sitespeciesid = s.sitespeciesid
       where s.higher = :rackid
         and (
             (coalesce(ss.multizone, '0') = '1' and Substr(:withchild, 2, 1) in ('0', '1'))
          or (coalesce(ss.multizone, '0') = '0' and Substr(:withchild, 2, 1) in ('0', '2'))
         )
         and not exists(select * from sitezone_items szi where szi.zoneid = :zoneid and szi.siteid = s.siteid);

    delete from wh_tbltmp_site where 1=1;
end^

SET TERM ; ^



CREATE UNIQUE INDEX SITE_IDX_NAME
ON SITE (NAME);



SET TERM ^ ;

CREATE OR ALTER procedure WH_FIRSTINCOMEFG_SITEBYTEXT (
    TEXT type of R_NAME)
returns (
    SID type of column SITE.siteid,
    SNAME type of column SITE.NAME,
    SPCODE type of column sitespecies.code)
AS
declare variable higher type of column SITE.higher;
begin
    select s.siteid, s.name, sp.code, s.higher
      from site s
           left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
     where s.barcode = :text
      into :sid, :sname, :spcode, :higher;

    if (:sid is NULL) then
        select s.siteid, s.name, sp.code, s.higher
          from site s
               left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
         where s.name = :text
          into :sid, :sname, :spcode, :higher;

    if (:sid is NOT NULL) then
    begin
        if (:spcode in ('S', 'STACK')) then
        begin
            suspend;
        end
        else if (:spcode = 'B') then
        begin
            for
                select s.siteid, s.name, sp.code
                  from site s
                       left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                 where s.higher = :higher
                  into :sid, :sname, :spcode
            do
                suspend;
        end
    end


    /*for
        select s.siteid, s.name, sp.code
          from site s
               left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
         where s.barcode = :text
           and sp.code in ('S', 'STACK')
         union distinct
        select s.siteid, s.name, sp.code
          from site s
               left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
         where s.name = :text
           and sp.code in ('S', 'STACK')
         union distinct
        select distinct s.siteid, s.name, sp.code
          from pallet p
               left join site s
                    left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                 on s.siteid = p.siteid
         where p.barcode = :text
           and sp.code = 'STACK'
         union distinct
        select distinct s.siteid, s.name, sp.code
          from pallet p
               left join site s
                    left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
                 on s.siteid = p.siteid
         where p.number = :text
           and sp.code = 'STACK'
          into :sid, :sname, :spcode
    do
        suspend;
   */
end^

SET TERM ; ^

