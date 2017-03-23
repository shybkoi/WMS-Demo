

SET TERM ^ ;

create procedure WH_RPALLETPRINT_FG_DATA (
    DTBEG type of R_DATETIME,
    DTEND type of R_DATETIME
)
returns (
    PNUM type of column pallet_finishprint.number,
    DT type of column pallet_finishprint.datetime,
    PLNAME type of column fg_prodlines.name,
    PRODUCER type of R_VARCHAR255,
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    PRDATE type of column pallet_finishprint.productdate,
    MANFIO type of R_VARCHAR255,
    PID type of column PALLET.palletid
)
as
begin
    for
        select pfp.datetime, pfp.palletid, pfp.number, pfp.productdate,
               g.code, g.name, pl.name,
               (select objname from wh_get_objectname(pfp.manid)),
               (select objname from wh_get_objectname(pfp.producerid))
          from pallet_finishprint pfp
               left join gwares g on g.waresid = pfp.waresid
               left join fg_prodlines pl on pl.id_prodline = pfp.prodlineid
         where pfp.datetime between :dtbeg and :dtend
          into :dt, :pid, :pnum, :prdate,
               :wcode, :wname, :plname,
               :manfio, :producer
    do
        suspend;
end^

SET TERM ; ^

