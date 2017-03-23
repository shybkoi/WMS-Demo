

SET TERM ^ ;

CREATE OR ALTER procedure WH_GET_MONITORING_STACK (
    SITEID type of column SITE.SITEID)
returns (
    PALLETID type of column PALLET.PALLETID,
    PNUMBER type of column PALLET.BARCODE,
    PNUM type of column PALLET.NUMBER,
    PN type of column PALLET.NUM,
    X type of R_COORD_FLOAT,
    Y type of R_COORD_FLOAT,
    Z type of R_COORD_FLOAT)
AS
declare variable modelid type of column model_stack.modelid;
declare variable palcurcnt type of column site_stack.palcurcnt;
declare variable psize type of column model_stack.psize;
declare variable psize_dp type of R_DOUBLE;
declare variable pnum_scheme type of column scheme_modelstack.number;
begin
/*  for
   select p.palletid, p.number, p.num, sm.x_coord, sm.y_coord, sm.z_coord
     from site_stack ss
     left join pallet p on p.siteid = ss.siteid
     left join scheme_modelstack sm on sm.modelid = ss.modelid and p.num = sm.number
    where ss.siteid = :siteid and p.status = 1
     into :palletid, :pnumber, :pnum, :x, :y, :z
  do
    suspend;*/

  select ss.modelid, ss.palcurcnt, ms.psize
    from site_stack ss
         left join model_stack ms on ms.modelid = ss.modelid
   where ss.siteid = :siteid
    into :modelid, :palcurcnt, :psize;
  psize_dp = cast(:psize as r_double);

  x = :psize_dp / 2.000;
  y = :psize_dp / 2.000;
  z = :psize_dp / 2.000;

  pn = 0;
  pnum_scheme = 1;
  while (:pn < :palcurcnt) do
  begin
    pn = :pn + 1;
    select p.barcode, p.number, p.palletid
      from pallet p
     where p.siteid = :siteid
       and p.num = :pn
      into :pnumber, :pnum, :palletid;

    suspend;

    select sms.nextnumber, :x + sms.x_pdiff * :psize_dp, :y + sms.y_pdiff * :psize_dp, :z + sms.z_pdiff * :psize_dp
      from scheme_modelstack sms
     where sms.modelid = :modelid
       and sms.number = :pnum_scheme
      into :pnum_scheme, :x, :y, :z;
  end

  /*for
   select p.palletid, p.number, p.num, sm.x_coord, sm.y_coord, sm.z_coord
     from site_stack ss
          left join pallet p on p.siteid = ss.siteid
          left join scheme_modelstack sm on sm.modelid = ss.modelid and p.num = sm.number
    where ss.siteid = :siteid and p.status = 1
     into :palletid, :pnumber, :pnum, :x, :y, :z
  do
    suspend;*/
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_GET_MONITORING_STACK (
    SITEID type of column SITE.SITEID)
returns (
    PALLETID type of column PALLET.PALLETID,
    PNUMBER type of column PALLET.BARCODE,
    PNUM type of column PALLET.NUMBER,
    PN type of column PALLET.NUM,
    X type of R_COORD_FLOAT,
    Y type of R_COORD_FLOAT,
    Z type of R_COORD_FLOAT)
AS
declare variable modelid type of column model_stack.modelid;
declare variable palcurcnt type of column site_stack.palcurcnt;
declare variable psize type of column model_stack.psize;
declare variable psize_dp type of R_DOUBLE;
declare variable pnum_scheme type of column scheme_modelstack.number;
begin
/*  for
   select p.palletid, p.number, p.num, sm.x_coord, sm.y_coord, sm.z_coord
     from site_stack ss
     left join pallet p on p.siteid = ss.siteid
     left join scheme_modelstack sm on sm.modelid = ss.modelid and p.num = sm.number
    where ss.siteid = :siteid and p.status = 1
     into :palletid, :pnumber, :pnum, :x, :y, :z
  do
    suspend;*/

  select ss.modelid, ss.palcurcnt, ms.psize
    from site_stack ss
         left join model_stack ms on ms.modelid = ss.modelid
   where ss.siteid = :siteid
    into :modelid, :palcurcnt, :psize;
  psize_dp = cast(:psize as r_double);

  x = :psize_dp / 2.000;
  y = :psize_dp / 2.000;
  z = :psize_dp / 2.000;

  pn = 0;
  pnum_scheme = 1;
  while (:pn < :palcurcnt) do
  begin
    pn = :pn + 1;
    select p.barcode, p.number, p.palletid
      from pallet p
     where p.siteid = :siteid
       and p.num = :pn
      into :pnumber, :pnum, :palletid;

    suspend;

    select sms.nextnumber, :x + sms.x_pdiff * :psize_dp, :y + sms.y_pdiff * :psize_dp, :z + sms.z_pdiff * :psize_dp
      from scheme_modelstack sms
     where sms.modelid = :modelid
       and sms.number = :pnum_scheme
      into :pnum_scheme, :z, :y, :x;
  end

  /*for
   select p.palletid, p.number, p.num, sm.x_coord, sm.y_coord, sm.z_coord
     from site_stack ss
          left join pallet p on p.siteid = ss.siteid
          left join scheme_modelstack sm on sm.modelid = ss.modelid and p.num = sm.number
    where ss.siteid = :siteid and p.status = 1
     into :palletid, :pnumber, :pnum, :x, :y, :z
  do
    suspend;*/
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_GET_MONITORING_STACK (
    SITEID type of column SITE.SITEID)
returns (
    PALLETID type of column PALLET.PALLETID,
    PNUMBER type of column PALLET.BARCODE,
    PNUM type of column PALLET.NUMBER,
    PN type of column PALLET.NUM,
    X type of R_COORD_FLOAT,
    Y type of R_COORD_FLOAT,
    Z type of R_COORD_FLOAT)
AS
declare variable modelid type of column model_stack.modelid;
declare variable palcurcnt type of column site_stack.palcurcnt;
declare variable psize type of column model_stack.psize;
declare variable psize_dp type of R_DOUBLE;
declare variable pnum_scheme type of column scheme_modelstack.number;
begin
/*  for
   select p.palletid, p.number, p.num, sm.x_coord, sm.y_coord, sm.z_coord
     from site_stack ss
     left join pallet p on p.siteid = ss.siteid
     left join scheme_modelstack sm on sm.modelid = ss.modelid and p.num = sm.number
    where ss.siteid = :siteid and p.status = 1
     into :palletid, :pnumber, :pnum, :x, :y, :z
  do
    suspend;*/

  select ss.modelid, ss.palcurcnt, ms.psize
    from site_stack ss
         left join model_stack ms on ms.modelid = ss.modelid
   where ss.siteid = :siteid
    into :modelid, :palcurcnt, :psize;
  psize_dp = cast(:psize as r_double);

  x = :psize_dp / 2.000;
  y = :psize_dp / 2.000;
  z = :psize_dp / 2.000;

  pn = 0;
  pnum_scheme = 1;
  while (:pn < :palcurcnt) do
  begin
    pn = :pn + 1;
    select p.barcode, p.number, p.palletid
      from pallet p
     where p.siteid = :siteid
       and p.num = :pn
      into :pnumber, :pnum, :palletid;

    suspend;

    select sms.nextnumber, :x + sms.x_pdiff * :psize_dp, :y + sms.y_pdiff * :psize_dp, :z + sms.z_pdiff * :psize_dp
      from scheme_modelstack sms
     where sms.modelid = :modelid
       and sms.number = :pnum_scheme
      into :pnum_scheme, :x, :y, :z;
  end

  /*for
   select p.palletid, p.number, p.num, sm.x_coord, sm.y_coord, sm.z_coord
     from site_stack ss
          left join pallet p on p.siteid = ss.siteid
          left join scheme_modelstack sm on sm.modelid = ss.modelid and p.num = sm.number
    where ss.siteid = :siteid and p.status = 1
     into :palletid, :pnumber, :pnum, :x, :y, :z
  do
    suspend;*/
end^

SET TERM ; ^

