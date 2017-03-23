

SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECT_CLIENTUNFUND (
    TASKID type of column WM_TASK.TASKID)
AS
declare variable clientid type of column OBJECT.objid;
declare variable fundobjid type of column OBJECT.objid;
declare variable docid type of column DOCUMENT.docid ;
declare variable tmid type of column wm_taskmethod.methodid;
begin
   select gor.objid, d.toobj, d.docid, t.taskmethodid
     from wm_task t
          left join document d
               left join wh_get_reserveobj(coalesce(d.throughobj, d.fromobj)) gor on 1=1
            on d.docid = t.docid
    where t.taskid = :taskid
     into :fundobjid, :clientid, :docid, :tmid;

   insert into wh_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
   select :docid, tw.waresid, tw.plandatetime, -tw.quantity, :fundobjid, :clientid
     from wm_task_wares tw
    where tw.taskid = :taskid;

   if (:tmid is NOT NULL) then
       insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
       select :docid, tw.waresid, tw.plandatetime, -tw.scanquant, :fundobjid
         from wm_task_wares tw
        where tw.taskid = :taskid
          and coalesce(tw.scanquant, 0.000) > 0.0001;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECT_CLIENTUNFUND (
    TASKID type of column WM_TASK.TASKID)
AS
declare variable clientid type of column OBJECT.objid;
declare variable fundobjid type of column OBJECT.objid;
declare variable docid type of column DOCUMENT.docid ;
declare variable tmid type of column wm_taskmethod.methodid;
begin
   select gor.objid, d.toobj, d.docid, t.taskmethodid
     from wm_task t
          left join document d
               left join wh_get_reserveobj(coalesce(d.throughobj, d.fromobj)) gor on 1=1
            on d.docid = t.docid
    where t.taskid = :taskid
     into :fundobjid, :clientid, :docid, :tmid;

   insert into wh_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
   select :docid, tw.waresid, tw.plandatetime, -tw.quantity, :fundobjid, :clientid
     from wm_task_wares tw
    where tw.taskid = :taskid;

   if (:tmid is NOT NULL) then
       insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, TASKID)
       select :docid, tw.waresid, tw.plandatetime, -tw.scanquant, :fundobjid, :taskid
         from wm_task_wares tw
        where tw.taskid = :taskid
          and coalesce(tw.scanquant, 0.000) > 0.0001;
end^

SET TERM ; ^


