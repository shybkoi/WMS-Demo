

SET TERM ^ ;

create procedure WH_SPWARES_STACKMODEL_LIST (
    WID type of column GWARES.waresid
)
returns (
    MODELID type of column model_stack.modelid,
    MODELNAME type of column model_stack.name,
    PRIORITY type of column MODEL_STACK_REF_WARESID.priority
)
as
begin
    for
        select ms.modelid, ms.name, w.priority
          from model_stack ms
               left join MODEL_STACK_REF_WARESID w on w.modelid = ms.modelid and w.waresid = :wid
          into :modelid, :modelname, :priority
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_SPWARES_STACKMODEL_SET (
    WID type of column GWARES.waresid,
    MODELID type of column model_stack.modelid,
    PRIORITY type of column MODEL_STACK_REF_WARESID.priority
)
as
begin
    if (:priority is NULL or :priority = 0) then
        delete from MODEL_STACK_REF_WARESID w
         where w.modelid = :modelid and w.waresid = :wid;
    else
        update or insert into MODEL_STACK_REF_WARESID ( MODELID, WARESID, PRIORITY)
        values ( :modelid, :wid, :priority)
        matching (MODELID, WARESID);
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SPWARES_STACKMODEL_SET (
    WID type of column GWARES.waresid,
    MODELID type of column model_stack.modelid,
    PRIORITY type of column MODEL_STACK_REF_WARESID.priority
)
returns(
    r type of r_flag
)
as
begin
    if (:priority is NULL or :priority = 0) then
    begin
        delete from MODEL_STACK_REF_WARESID w
         where w.modelid = :modelid and w.waresid = :wid;

        r = 'D';
    end
    else
    begin
        update or insert into MODEL_STACK_REF_WARESID ( MODELID, WARESID, PRIORITY)
        values ( :modelid, :wid, :priority)
        matching (MODELID, WARESID);

        r = 'S';
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SPWARES_STACKMODEL_LIST (
    WID type of column GWARES.waresid
)
returns (
    MODELID type of column model_stack.modelid,
    MODELNAME type of column model_stack.name,
    PRIORITY type of column MODEL_STACK_REF_WARESID.priority
)
as
begin
    for
        select ms.modelid, ms.name, coalesce(w.priority, 0)
          from model_stack ms
               left join MODEL_STACK_REF_WARESID w on w.modelid = ms.modelid and w.waresid = :wid
          into :modelid, :modelname, :priority
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger model_stack_ref_waresid_bi for model_stack_ref_waresid
active before insert position 0
as
begin
    if (new.priority is NULL) then
        new.priority = 1;

    if (exists(select *
                 from MODEL_STACK_REF_WARESID w
                where w.waresid = new.waresid
                  and w.priority = new.priority )) then
        exception exc_k_common 'Ќельз€ двум модел€м задать одинаковый приоритет!';
end^

SET TERM ; ^

