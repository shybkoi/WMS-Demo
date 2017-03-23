

SET TERM ^ ;

create procedure WH_UTIL_TABLESCLEAR (
    TABLES type of rbs_bigvarchar
)
as
declare variable tblname type of R_DBNAME;
declare variable triggers varchar(16383);
declare variable triggername type of r_dbname;
begin
    -- Перед чисткой отключим триггеры
    select list(t.rdb$trigger_name)
      from r_listwords(:tables, ',', 0) r
           left join rdb$triggers t on t.rdb$relation_name = r.word
     where coalesce(t.rdb$trigger_inactive,0)=0
--       and t.rdb$system_flag not in (3, 4)
       and t.rdb$system_flag <> 3
      into :triggers;

    for
        select r.word
          from r_listwords(:triggers,',',0) r
          into :triggername
    do
        execute statement ('update rdb$triggers t
           set t.rdb$trigger_inactive = 1
         where t.rdb$trigger_name = :trname')
         (trname := triggername )
        WITH AUTONOMOUS TRANSACTION;

    for
        select r.word
          from r_listwords(:tables, ',', 0) r
          into :tblname
    do
    begin
        execute statement ('delete from ' || :tblname);
    end

    for
        select r.word
          from r_listwords(:triggers,',',0) r
          into :triggername
    do
        execute statement ('update rdb$triggers t
           set t.rdb$trigger_inactive = 0
         where t.rdb$trigger_name = :trname')
         (trname := triggername )
        WITH AUTONOMOUS TRANSACTION;

    when any do
    begin
        for
            select trim(r.word)
              from r_listwords(:triggers,',',0) r
              into :triggername
        do
            execute statement 'update rdb$triggers t
               set t.rdb$trigger_inactive = 0
             where t.rdb$trigger_name = ''' ||:triggername || ''''
            WITH AUTONOMOUS TRANSACTION;

        exception;
    end
end^

SET TERM ; ^

