

SET TERM ^ ;

create or alter procedure RBS_LOADPLAN_RETURNPLAN (
    TASKID type of column WM_TASK.TASKID)
as
declare variable OBJCODE type of column WM_CONFIG.OBJCODE;
declare variable TSTATUS type of column WM_TASK.STATUS;
declare variable TASKBONDTID type of column WH_TASKBONDTYPE.ID;
declare variable TTSELECTID type of column WM_TASKTYPE.TASKTYPEID;
begin
  select w.objcode
    from wm_config w
    into :objcode;

  select t.status
    from wm_task t
   where t.taskid = :taskid
    into :tstatus;

  if (:objcode = 'U3S') then
  begin
    -- если статус отложено
    if(:tstatus = '0') then
    begin
      select tbt.id
        from wh_taskbondtype tbt
       where tbt.code = 'CARDOCS'
        into :taskbondtid;

      select tt.tasktypeid
        from wm_tasktype tt
       where tt.code = 'SELECT'
        into :ttselectid;

      -- проверим задания на отборку привязанных документов
      if (exists(select *
                   from wh_taskbond tb
                        left join wm_task t on t.taskid = tb.task2id
                        left join wm_task t1 on t1.docid = t.docid
                  where tb.task1id = :taskid
                    and tb.taskbondtid = :taskbondtid
                    and t1.tasktypeid = :ttselectid)) then
      begin
        exception exc_k_common 'Уже есть задания на отборку товара, расформирование невозможно!';
      end
      else
      begin
        update wm_task t
           set t.status = '4'
         where t.taskid = :taskid;
      end
    end
    else
    begin
      exception exc_k_common 'Статус задания не позволяет расформирование!';
    end
  end
end^

SET TERM ; ^

