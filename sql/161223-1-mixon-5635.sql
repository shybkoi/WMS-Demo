

SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_STOPPLAN (
    TASKID type of column WM_TASK.TASKID)
as
declare variable OBJCODE type of column WM_CONFIG.OBJCODE;
declare variable TBTID_CARDOCS type of column WH_TASKBONDTYPE.ID;
declare variable PCNT type of R_SHORTNUMBER;
declare variable GATEID type of column WM_TASK.SITEID;
begin
  select w.objcode
    from wm_config w
    into :objcode;

  if (:objcode = 'U3S') then
  begin
      select t.siteid
        from wm_task t
       where t.taskid = :taskid
        into :gateid;

      if(:gateid is null) then
      begin
        exception exc_k_common '¬ы должны проставить ворота перед формированием!';
      end

      select tbt.id
        from wh_taskbondtype tbt
       where tbt.code = 'CARDOCS'
        into :tbtid_cardocs;

      with s1 as (
          select sum(iif(pu.W_PUFACTOR is NOT NULL and pu.W_PUFACTOR > 0.0001, cg.amount / pu.W_PUFACTOR, 0.000)) as q
            from wh_taskbond tb
                 left join wm_task t
                      left join cargo cg
                           left join wh_wares_getpalletunit(cg.waresid) pu on 1=1
                        on cg.document = t.docid
                   on t.taskid = tb.task2id
           where tb.task1id = :taskid
             and tb.taskbondtid = :tbtid_cardocs
           group by cg.document
      )
      select sum(ceil(s1.q))
        from s1
        into :pcnt;

      update wm_task t
         set t.status = '0', t.capacity = :pcnt
       where t.taskid = :taskid;
  end
  else
  begin
      update wm_task t
         set t.status = '0'
       where t.taskid = :taskid;
  end
end^

SET TERM ; ^

