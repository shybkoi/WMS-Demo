

SET TERM ^ ;

create procedure WH_INCOMEDC_QLINES (
    DOCID type of column DOCUMENT.docid
)
returns (
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    WEXTERNALCODE type of column GWARES.externalcode,
    LINENUM type of column fg_prodlines.number,
    LINENAME type of column fg_prodlines.name,
    Q type of column WM_TASK_LOT.quantity,
    QP type of R_NUMBER,
    QM type of column WM_TASK_LOT.quantity
)
as
begin
    for
        with pq as (
            select tl.palletid as palletid, sum(tl.quantity) as q
              from wm_task t
                   left join wm_task_wares tw
                        left join wm_task_lot tl on tl.taskwaresid = tw.taskwaresid
                     on tw.taskid = t.taskid
             where t.docid = :docid
             group by tl.palletid
        ),
        wlq as (
            select pfp.waresid, pfp.prodlineid,
                   sum(iif (abs(pfp.quantity - pq.q) < 0.001, 1, 0)) as qp,
                   sum(iif (abs(pfp.quantity - pq.q) < 0.001, 0, pq.q)) as qm,
                   sum(pq.q) as q
              from pq
                   left join pallet_finishprint pfp on pfp.palletid = pq.palletid
             group by pfp.waresid, pfp.prodlineid
        )
        select g.code, g.name, g.externalcode,
               pl.number, pl.name,
               wlq.qp, wlq.qm, wlq.q
          from wlq
               left join gwares g on g.waresid = wlq.waresid
               left join fg_prodlines pl on pl.id_prodline = wlq.prodlineid
          into :wcode, :wname, :wexternalcode,
               :linenum, :linename,
               :qp, :qm, :q
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEDC_QLINES (
    DOCID type of column DOCUMENT.docid
)
returns (
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    WEXTERNALCODE type of column GWARES.externalcode,
    LINENUM type of column fg_prodlines.number,
    LINENAME type of column fg_prodlines.name,
    Q type of column WM_TASK_LOT.quantity,
    QP type of R_NUMBER,
    QM type of column WM_TASK_LOT.quantity,
    PUF type of column WARESUNIT.factor
)
as
begin
    for
        with pq as (
            select tl.palletid as palletid, sum(tl.quantity) as q
              from wm_task t
                   left join wm_task_wares tw
                        left join wm_task_lot tl on tl.taskwaresid = tw.taskwaresid
                     on tw.taskid = t.taskid
             where t.docid = :docid
             group by tl.palletid
        ),
        wlq as (
            select pfp.waresid, pfp.prodlineid,
                   sum(iif (abs(pfp.quantity - pq.q) < 0.001, 1, 0)) as qp,
                   sum(iif (abs(pfp.quantity - pq.q) < 0.001, 0, pq.q)) as qm,
                   sum(pq.q) as q
              from pq
                   left join pallet_finishprint pfp on pfp.palletid = pq.palletid
             group by pfp.waresid, pfp.prodlineid
        )
        select g.code, g.name, g.externalcode,
               pl.number, pl.name,
               wlq.qp, wlq.qm, wlq.q,
               pu.W_PUFACTOR
          from wlq
               left join gwares g
                    left join wh_wares_getpalletunit(g.waresid) pu on 1=1
                 on g.waresid = wlq.waresid
               left join fg_prodlines pl on pl.id_prodline = wlq.prodlineid
          into :wcode, :wname, :wexternalcode,
               :linenum, :linename,
               :qp, :qm, :q, :puf
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEDC_QLINES (
    DOCID type of column DOCUMENT.docid
)
returns (
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    WEXTERNALCODE type of column GWARES.externalcode,
    LINENUM type of column fg_prodlines.number,
    LINENAME type of column fg_prodlines.name,
    Q type of column WM_TASK_LOT.quantity,
    QP type of R_NUMBER,
    QM type of column WM_TASK_LOT.quantity,
    PUF type of column WARESUNIT.factor,
    PRODUCTDATE type of column WARESLOT.productdate
)
as
begin
    for
        with pq as (
            select tl.palletid as palletid, sum(tl.quantity) as q, wl.productdate as productdate
              from wm_task t
                   left join wm_task_wares tw
                        left join wm_task_lot tl
                             left join wareslot wl on wl.wlotid = tl.wlotid
                          on tl.taskwaresid = tw.taskwaresid
                     on tw.taskid = t.taskid
             where t.docid = :docid
             group by tl.palletid, wl.productdate
        ),
        wlq as (
            select pfp.waresid, pfp.prodlineid, pq.productdate,
                   sum(iif (abs(pfp.quantity - pq.q) < 0.001, 1, 0)) as qp,
                   sum(iif (abs(pfp.quantity - pq.q) < 0.001, 0, pq.q)) as qm,
                   sum(pq.q) as q
              from pq
                   left join pallet_finishprint pfp on pfp.palletid = pq.palletid
             group by pfp.waresid, pfp.prodlineid, pq.productdate
        )
        select g.code, g.name, g.externalcode,
               pl.number, pl.name,
               wlq.qp, wlq.qm, wlq.q,
               pu.W_PUFACTOR, wlq.productdate
          from wlq
               left join gwares g
                    left join wh_wares_getpalletunit(g.waresid) pu on 1=1
                 on g.waresid = wlq.waresid
               left join fg_prodlines pl on pl.id_prodline = wlq.prodlineid
          into :wcode, :wname, :wexternalcode,
               :linenum, :linename,
               :qp, :qm, :q, :puf, :productdate
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure WH_INCOMEDC_RQLINES_INFO (
    ID type of R_ID64)
returns (
    DOCNUM type of DOCNUMBER,
    DOCDATE type of R_DATETIME,
    FROMOBJNAME type of R_NAME,
    TOOBJNAME type of R_NAME,
    DTPRINTNAME type of R_NAME
)
AS
begin
  DTPRINTNAME = 'Отчет о приходе готовой продукции в разрезе линий производства';

  select d.number, d.realdocdate,
         (select objname from wh_get_objectname(d.fromobj)),
         (select objname from wh_get_objectname(d.toobj))
    from document d
   where d.docid = :id
    into :docnum, :docdate, :fromobjname, :toobjname;

  suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_INCOMEDC_RQLINES (
    DOCID type of column DOCUMENT.docid
)
returns (
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    WEXTERNALCODE type of column GWARES.externalcode,
    LINENUM type of column fg_prodlines.number,
    LINENAME type of column fg_prodlines.name,
    Q type of column WM_TASK_LOT.quantity,
    QP type of R_NUMBER,
    QM type of column WM_TASK_LOT.quantity,
    PUF type of column WARESUNIT.factor,
    PRODUCTDATE type of column WARESLOT.productdate
)
as
begin
    for
        with pq as (
            select tl.palletid as palletid, sum(tl.quantity) as q, wl.productdate as productdate
              from wm_task t
                   left join wm_task_wares tw
                        left join wm_task_lot tl
                             left join wareslot wl on wl.wlotid = tl.wlotid
                          on tl.taskwaresid = tw.taskwaresid
                     on tw.taskid = t.taskid
             where t.docid = :docid
             group by tl.palletid, wl.productdate
        ),
        wlq as (
            select pfp.waresid, pfp.prodlineid, pq.productdate,
                   sum(iif (abs(pfp.quantity - pq.q) < 0.001, 1, 0)) as qp,
                   sum(iif (abs(pfp.quantity - pq.q) < 0.001, 0, pq.q)) as qm,
                   sum(pq.q) as q
              from pq
                   left join pallet_finishprint pfp on pfp.palletid = pq.palletid
             group by pfp.waresid, pfp.prodlineid, pq.productdate
        )
        select g.code, g.name, g.externalcode,
               pl.number, pl.name,
               wlq.qp, wlq.qm, wlq.q,
               pu.W_PUFACTOR, wlq.productdate
          from wlq
               left join gwares g
                    left join wh_wares_getpalletunit(g.waresid) pu on 1=1
                 on g.waresid = wlq.waresid
               left join fg_prodlines pl on pl.id_prodline = wlq.prodlineid
          into :wcode, :wname, :wexternalcode,
               :linenum, :linename,
               :qp, :qm, :q, :puf, :productdate
    do
        suspend;
end^

SET TERM ; ^



DROP PROCEDURE WH_INCOMEDC_QLINES;

