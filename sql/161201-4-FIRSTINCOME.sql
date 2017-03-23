

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
declare variable WUBDAYS type of R_QUANTITY;
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

  if (:bestbeforedate is NULL) then
  begin
    select cast(rcU.data as double precision)*g.usebydate
      from gwares g
           left join r_choice rcU on rcU.chtype='P' and rcU.code=g.ubdtype
     where g.waresid = :waresid
      into :wubdays;

    if (:wubdays is NULL) then
        exception exc_wh_wrongdate;

    bestbeforedate = dateadd(cast(:wubdays as integer) DAY to :productdate);
  end
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

