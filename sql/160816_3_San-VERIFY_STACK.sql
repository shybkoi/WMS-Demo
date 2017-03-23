

SET TERM ^ ;

create procedure WH_VERIFY_STACK_PALLETLIST (
    SITEID type of column SITE.siteid
)
returns (
    PALLETID type of column pallet.palletid,
    PNUM type of column pallet.num,
    PNUMBER type of column pallet.number
)
as
begin
    for
        select p.palletid, p.num, p.number
          from pallet p
         where p.siteid = :siteid
          into :palletid, :pnum, :pnumber
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_VERIFY_STACK_INFO (
    siteid type of column SITE.siteid
)
returns (
    STACKID type of column SITE.siteid,
    WID type of column GWARES.waresid,
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    PRODUCTDATE type of R_DATE,
    BESTBEFOREDATE type of R_DATE,
    CURCNT type of R_NUMBER,
    MAXCNT type of R_NUMBER,
    MODELID type of column model_stack.modelid,
    MODELNAME type of column model_stack.name
)
as
begin
    select ss.siteid, ss.palmaxcnt, ss.palcurcnt,
           ss.productdate, ss.bestbeforedate,
           g.waresid, g.code, g.name,
           ms.modelid, ms.name
      from site_stack ss
           left join gwares g
             on g.waresid = ss.waresid
           left join model_stack ms
             on ms.modelid = ss.modelid
     where ss.siteid = :siteid
      into :stackid, :maxcnt, :curcnt,
           :productdate, :bestbeforedate,
           :wid, :wcode, :wname,
           :modelid, :modelname;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_VERIFY_STACK_INFO (
    siteid type of column SITE.siteid
)
returns (
    STACKID type of column SITE.siteid,
    STACKNAME type of column SITE.name,
    WID type of column GWARES.waresid,
    WCODE type of column GWARES.code,
    WNAME type of column GWARES.name,
    PRODUCTDATE type of R_DATE,
    BESTBEFOREDATE type of R_DATE,
    CURCNT type of R_NUMBER,
    MAXCNT type of R_NUMBER,
    MODELID type of column model_stack.modelid,
    MODELNAME type of column model_stack.name
)
as
begin
    select s.siteid, s.name,
           ss.palmaxcnt, ss.palcurcnt,
           ss.productdate, ss.bestbeforedate,
           g.waresid, g.code, g.name,
           ms.modelid, ms.name
      from site s
           left join site_stack ss
                left join gwares g
                  on g.waresid = ss.waresid
                left join model_stack ms
                  on ms.modelid = ss.modelid
             on ss.siteid = s.siteid
     where s.siteid = :siteid
      into :stackid, :stackname,
           :maxcnt, :curcnt,
           :productdate, :bestbeforedate,
           :wid, :wcode, :wname,
           :modelid, :modelname;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_VERIFY_STACK_PALLETLIST (
    SITEID type of column SITE.siteid
)
returns (
    PALLETID type of column pallet.palletid,
    PNUM type of column pallet.num,
    PNUMBER type of column pallet.number,
    PQ type of column WARESLOTITEM.amount
)
as
begin
    for
        select p.palletid, p.num, p.number
          from pallet p
         where p.siteid = :siteid
           and p.status = '1'
         order by p.num descending
          into :palletid, :pnum, :pnumber
    do
    begin
        pq = NULL;

        select sum(wli.amount)
          from wareslotitem wli
         where wli.palletid = :palletid
          into :pq;

        suspend;
    end
end^

SET TERM ; ^

