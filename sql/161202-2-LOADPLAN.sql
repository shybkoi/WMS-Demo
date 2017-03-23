

SET TERM ^ ;

create procedure WH_LOADPLAN_FUNDSALE (
    taskid_gateauto type of column WM_TASK.taskid
)
returns(
    wid type of column GWARES.waresid,
    wcode type of column GWARES.CODE,
    wname type of column GWARES.NAME,
    wexternalcode type of column GWARES.externalcode,
    amount type of column wh_reserve_client_changes.amount,
    productdate type of column wh_reserve_client_changes.productdate,
    docnums type of RBS_BIGVARCHAR
)
as
declare variable tbtid_cardocs type of column wh_taskbondtype.id;
declare variable dbtid_fundsale type of column DOCBONDTYPE.docbondtid;
begin
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'CARDOCS'
      into :tbtid_cardocs;

    execute procedure wh_dbtid_fundsale
     returning_values :dbtid_fundsale;

    for
        with doc as(
            select distinct d.docid, d.number
              from wh_taskbond tb
                   left join wm_task t
                        left join docbond db
                             left join document d on d.docid = db.doc1id
                          on db.doc2id = t.docid
                     on t.taskid = tb.task2id
             where tb.task1id = :taskid_gateauto
               and tb.taskbondtid = :tbtid_cardocs
               and db.docbondtid = :dbtid_fundsale
        )
        select g.waresid, rcc.productdate,
               sum(rcc.amount), list(distinct doc.number),
               max(g.code), max(g.name), max(g.externalcode)
          from doc
               left join wh_reserve_client_changes rcc
                    left join gwares g on g.waresid = rcc.waresid
                 on rcc.docid = doc.docid
         group by g.waresid, rcc.productdate
        having sum(rcc.amount) > 0.0001
          into :wid, :productdate,
               :amount, :docnums,
               :wcode, :wname, :wexternalcode
    do
        suspend;
end^

SET TERM ; ^

