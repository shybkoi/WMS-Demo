

SET TERM ^ ;

CREATE OR ALTER procedure K_AUTO_DOWN (
    AID type of column T_AUTO.AID)
AS
declare variable ttid_gateauto type of column WM_TASKTYPE.tasktypeid;
begin
    execute procedure wh_ttid_gateauto
     returning_values :ttid_gateauto;

    if (exists(select *
                 from wm_task t
                where t.tasktypeid = :ttid_gateauto
                  and t.status <> '2'
                  and t.infoid = :aid)) then
        exception exc_wh_wrongstatus '” авто есть не завершенное задание на погрузку!';

    update t_auto ta
       set ta.status = '0'
     where ta.aid = :aid and ta.status <> '0';
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_AUTO_DOWN (
    AID type of column T_AUTO.AID)
AS
declare variable ttid_gateauto type of column WM_TASKTYPE.tasktypeid;
begin
    execute procedure wh_ttid_gateauto
     returning_values :ttid_gateauto;

    if (exists(select *
                 from wm_task t
                where t.tasktypeid = :ttid_gateauto
                  and t.status in ('4','0','1')
                  and t.infoid = :aid
                PLAN (T INDEX (WM_TASK_IDX_INFOID, WM_TASK_S_TT))
                )) then
        exception exc_wh_wrongstatus '” авто есть не завершенное задание на погрузку!';

    update t_auto ta
       set ta.status = '0'
     where ta.aid = :aid and ta.status <> '0';
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_AUTO_DELAUTO (
    AID type of column T_AUTO.AID)
returns (
    STAT type of column T_AUTO.STATUS)
AS
declare variable titid type of column wh_taskinfotype.id;
begin
    select tit.id
      from wh_taskinfotype tit
     where tit.code = 'AUTO'
      into :titid;

    if (exists(select *
                 from wm_task t
                where t.infoid = :aid
                  and t.typeinfoid = :titid)) then
        exception exc_wh_wrongstatus '” авто есть задани€ на погрузку, удаление не возможно!';
    else
    begin
      delete from t_auto a
       where a.aid = :aid;

      stat = 'D';
    end

    suspend;
end^

SET TERM ; ^

