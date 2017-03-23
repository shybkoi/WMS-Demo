

ALTER TABLE FG_PRODLINES
ADD DOCSUBTYPE R_CODE3;



ALTER TABLE FG_PRODLINES ALTER DOCSUBTYPE TO FUNDINCOMESUBTYPE;



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYPALLET_FUNDINCOME (
    PRODUCERID type of column OBJECT.OBJID,
    WHID type of column OBJECT.OBJID,
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of R_DATE,
    QUANTITY type of R_QUANTITY,
    DST type of column DOCSUBTYPE.code = NULL)
returns (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable dtid_fundincome type of column doctype.doctid;
declare variable docstat type of column r_status.code;
declare variable cargoid type of column cargo.cargoid;
declare variable singularityid type of column waresgroup_singularity.id;
declare variable singularityname type of column waresgroup_singularity.name = NULL;
begin
    execute procedure wh_dtid_fundincome('0')
     returning_values :dtid_fundincome;

    if (:dtid_fundincome is NOT NULL) then
    begin
        with recursive wgf as(
            select wg.waresgrid, wg.higher, wg.singularityid
              from gwares g
                   left join waresgroup wg
                     on wg.waresgrid = g.waresgroup
             where g.waresid = :waresid
             union all
            select wg.waresgrid, wg.higher, wg.singularityid
              from wgf
                   join waresgroup wg on wg.waresgrid = wgf.higher
             where wg.singularityid is NULL
        )
        select first(1) wgf.singularityid
          from wgf
         where wgf.singularityid is NOT NULL
          into :singularityid;

        if (:singularityid is NULL) then
        begin
            select first(1) d.docid, d.status
              from document d
                   left join document_wgsingularity ds on ds.docid = d.docid
             where d.doctype = :dtid_fundincome
               and d.fromobj = :producerid
               and d.toobj = :whid
               and d.realdocdate = :productdate
               and ds.singularityid is NULL
               and (:dst is NULL or d.docsubtype = :dst)
              into :docid, :docstat;
        end
        else
        begin
            select first(1) d.docid, d.status
              from document d
                   left join document_wgsingularity ds on ds.docid = d.docid
             where d.doctype = :dtid_fundincome
               and d.fromobj = :producerid
               and d.toobj = :whid
               and d.realdocdate = :productdate
               and ds.singularityid = :singularityid
               and (:dst is NULL or d.docsubtype = :dst)
              into :docid, :docstat;
        end

        if (:docid is NULL) then
        begin                               
            if (:singularityid is NOT NULL) then
                select wsg.name
                  from waresgroup_singularity wsg
                 where wsg.id = :singularityid
                  into :singularityname;

            select k.docid
              from k_doccreate(:producerid, :whid, NULL, :dtid_fundincome,
                               current_date, :productdate,
                               NULL, NULL, :singularityname, NULL, :dst) k
              into :docid;

            if (:singularityid is NOT NULL) then
                insert into document_wgsingularity(docid, singularityid)
                values(:docid, :singularityid);
    
            update document d
               set d.status = 'c'
             where d.docid = :docid;
        end
        else if (:docstat <> 'c') then
        begin
            exception exc_wh_reserve 'Ќе верный статус документа прихода резерва!';
        end

        execute procedure k_get_cargoid(:docid, :waresid)
          returning_values :cargoid;

        if (:cargoid is NULL) then
            insert into cargo(document, waresid, amount, price)
            values(:docid, :waresid, :quantity, 0.000);
        else
            update cargo cg
               set cg.amount = cg.amount + :quantity
             where cg.cargoid = :cargoid;

        suspend;
    end
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
declare variable docid type of column DOCUMENT.docid;
declare variable cargoid type of column cargo.cargoid;
declare variable docid_fundincome type of column DOCUMENT.docid;
declare variable fundincomesubtype type of column docsubtype.code;
begin
    if (:quantity is NULL) then
        exception exc_wh_wrongamount;

    select wh.zoneid, wh.whid, wh.manid
      from wh_user_infoshort(:iduser) wh
      into :zoneid, :whid, :manid;

    select pfp.productdate, pfp.waresid, pfp.quantity, pfp.producerid, pfp.number,
           coalesce(pfp.dtid_income, pl.dtid_income, p.dtid_income_print, p.dtid_income),
           pl.fundincomesubtype
      from pallet_finishprint pfp
           left join fg_producer p on p.objid = pfp.producerid
           left join fg_prodlines pl on pl.id_prodline = pfp.prodlineid
     where pfp.barcode = :pbarcode and pfp.enabled = '1'
      into :productdate, :waresid, :qplan, :producerid, :pnumber, :dtid_income, :fundincomesubtype;

    execute procedure WH_INCOMEFG_BYPALLET_FUNDINCOME(:producerid, :whid, :waresid, :productdate, :quantity, :fundincomesubtype)
     returning_values :docid_fundincome;

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

    update or insert into docbond ( DOCBONDTID, DOC1ID, DOC2ID)
    values ( (select dbt.docbondtid from docbondtype dbt where dbt.code = 'FUNDINCOME'), :docid_fundincome, :docid)
    matching (DOCBONDTID, DOC1ID, DOC2ID);

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

CREATE OR ALTER procedure WH_INCOMEFG_BYSTACK (
    TASKID type of column WM_TASK.TASKID,
    STACKID type of column SITE.SITEID,
    WARESID type of column GWARES.WARESID,
    MODELID type of column MODEL_STACK.MODELID,
    LINEID type of column FG_PRODLINES.ID_PRODLINE,
    PRODUCERID type of column OBJECT.OBJID,
    PCNT type of R_NUMBER,
    PQ type of R_DOUBLE,
    PRODUCTDATE type of R_DATE,
    BESTBEFOREDATE type of R_DATE,
    IDUSER type of R_ID,
    DTBEG type of R_DATETIME = current_timestamp)
AS
declare variable i type of R_NUMBER;
declare variable WHID type of column OBJECT.objid;
declare variable ZONEID type of column SITEZONE.zoneid;
declare variable MANID type of column MAN.manid;
declare variable PNUMBER type of column PALLET.number;
declare variable PBARCODE type of column PALLET.barcode;
declare variable wmsid type of column WM_SESSION.sessionid;
declare variable taskwaresid type of column wm_task_wares.taskwaresid;
declare variable ptypeid_finishgood type of column pallet_type.id;
declare variable palletid type of column PALLET.palletid;
declare variable wlincomeid type of column wareslotincomes.id;
declare variable wlotid type of column WARESLOT.wlotid;
declare variable docid type of column DOCUMENT.docid;
declare variable docid_fundincome type of column DOCUMENT.docid;
declare variable cargoid type of column CARGO.cargoid;
declare variable spCode type of column sitespecies.code;
declare variable fundincomesubtype type of column DOCSUBTYPE.code;
begin
  if (:pq is NULL) then
      exception exc_wh_wrongamount;

  select sp.code
    from site s
         left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
   where s.siteid = :stackid
    into :spCode;


  if (:spcode not in ('STACK', 'B')) then
      exception exc_wh_wrongsitetype;

  select t.docid
    from wm_task t
   where t.taskid = :taskid
    into :docid;

  select wh.zoneid, wh.whid, wh.manid
    from wh_user_infoshort(:iduser) wh
    into :zoneid, :whid, :manid;

  select pl.fundincomesubtype
    from fg_prodlines pl
   where pl.id_prodline = :lineid
    into :fundincomesubtype;

  execute procedure WH_INCOMEFG_BYPALLET_FUNDINCOME(:producerid, :whid, :waresid, :productdate, :pq*:pcnt, :fundincomesubtype)
   returning_values :docid_fundincome;

  update or insert into docbond ( DOCBONDTID, DOC1ID, DOC2ID)
  values ( (select dbt.docbondtid from docbondtype dbt where dbt.code = 'FUNDINCOME'), :docid_fundincome, :docid)
  matching (DOCBONDTID, DOC1ID, DOC2ID);


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


  if (:spcode = 'STACK') then
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



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_FUNDINCOME_STATUSCHG (
    DOCID type of column DOCUMENT.DOCID,
    OLDSTAT type of column R_STATUS.CODE,
    NEWSTAT type of column R_STATUS.CODE)
AS
declare variable queueid type of column r_queue.queueid;
declare variable egaisneed type of column waresgroup_singularity.egaisneed;
declare variable whid type of column OBJECT.objid;
declare variable realdocdate type of column DOCUMENT.realdocdate;
declare variable docsubtype type of column DOCSUBTYPE.code;
begin
    if (:newstat = 'w') then
    begin
        if (:oldstat = 'e') then
            exit;

        select d.toobj, d.realdocdate, d.docsubtype
          from document d
         where d.docid = :docid
          into :whid, :realdocdate, :docsubtype;

        select wsg.egaisneed
          from document_wgsingularity ds
               left join waresgroup_singularity wsg
                 on wsg.id = ds.singularityid
         where ds.docid = :docid
          into :egaisneed;

        if ((docsubtype is NULL or :docsubtype <> '-EG') and (:egaisneed is NULL or :egaisneed = '1')) then
        begin
         execute procedure RBS_Q_CREATETASKEXPORT('FUNDINCOME_STATUSCHG: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
          returning_values :queueid;
        end
        else
        begin
           insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           select :docid, cg.waresid, :realdocdate, cg.amount, :whid
             from cargo cg
            where cg.document = :docid;

           update document d
              set d.status = 'e'
            where d.docid = :docid;
       end
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_FUNDINCOME_STATUSCHG (
    DOCID type of column DOCUMENT.DOCID,
    OLDSTAT type of column R_STATUS.CODE,
    NEWSTAT type of column R_STATUS.CODE)
AS
declare variable queueid type of column r_queue.queueid;
declare variable egaisneed type of column waresgroup_singularity.egaisneed;
declare variable whid type of column OBJECT.objid;
declare variable realdocdate type of column DOCUMENT.realdocdate;
declare variable docsubtype type of column DOCSUBTYPE.code;
begin
    if (:newstat = 'w') then
    begin
        if (:oldstat = 'e') then
            exit;

        select d.toobj, d.realdocdate, d.docsubtype
          from document d
         where d.docid = :docid
          into :whid, :realdocdate, :docsubtype;

        select wsg.egaisneed
          from document_wgsingularity ds
               left join waresgroup_singularity wsg
                 on wsg.id = ds.singularityid
         where ds.docid = :docid
          into :egaisneed;

        if ((docsubtype is NULL or :docsubtype <> '-1C') and (:egaisneed is NULL or :egaisneed = '1')) then
        begin
         execute procedure RBS_Q_CREATETASKEXPORT('FUNDINCOME_STATUSCHG: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
          returning_values :queueid;
        end
        else
        begin
           insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           select :docid, cg.waresid, :realdocdate, cg.amount, :whid
             from cargo cg
            where cg.document = :docid;

           update document d
              set d.status = 'e'
            where d.docid = :docid;
       end
    end
end^

SET TERM ; ^

