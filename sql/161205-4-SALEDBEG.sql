SET TERM ^ ;

CREATE OR ALTER trigger k_wares_data_obj_bi for k_wares_data_obj
active before insert position 0
as
begin
  new.lastdate = 'NOW';
  if (new.id_wares_data_obj is null) then
    new.id_wares_data_obj = gen_id(gen_k_wares_data_obj_id,1);

  if (new.dbeg is NULL) then
    new.dbeg = '01.01.2001';

  if (new.dend is NULL) then
    new.dend = '31.12.2099';
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARES_SALEDBEG (
    WARESID type of column GWARES.WARESID,
    CLIENTID type of column OBJECT.OBJID = null,
    ACTUALDATE type of R_DATE = current_date)
returns (
    DBEG type of R_DATE)
AS
declare variable wdVAL type of R_CUSTOMDATA;
declare variable ubdays type of r_double;
begin
    dbeg = '01.01.2000';

    if (:clientid is NOT NULL) then
    begin
        select val
          from k_get_wares_data_obj_val(NULL,'SALEPERIOD',:waresid, :clientid, :actualdate)
          into :wdval;
        
        if (:wdval is NOT NULL) then
        begin
            select cast(rcI.data as double precision)*g.incometerm
              from gwares g
                   left join r_choice rcI on rcI.chtype='P' and rcI.code=g.incometermtype
             where g.waresid = :waresid
              into :ubdays;

            dbeg = :actualdate - ceil(:ubdays * cast(:wdval as r_double) /  100.00);
        end
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARES_SALEDBEG (
    WARESID type of column GWARES.WARESID,
    CLIENTID type of column OBJECT.OBJID = null,
    ACTUALDATE type of R_DATE = current_date)
returns (
    DBEG type of R_DATE)
AS
declare variable wdVAL type of R_CUSTOMDATA;
declare variable ubdays type of r_double;
begin
    dbeg = '01.01.2000';

    if (:clientid is NOT NULL) then
    begin
        select val
          from k_get_wares_data_obj_val(NULL,'SALEPERIOD',:waresid, :clientid, :actualdate)
          into :wdval;
        
        if (:wdval is NOT NULL) then
        begin
            select cast(rcI.data as double precision)*g.incometerm
              from gwares g
                   left join r_choice rcI on rcI.chtype='P' and rcI.code=g.incometermtype
             where g.waresid = :waresid
              into :ubdays;

            dbeg = dateadd(- floor(:ubdays * cast(:wdval as r_double) /  100.00) day to :actualdate);
        end
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARES_SALEDBEG (
    WARESID type of column GWARES.WARESID,
    CLIENTID type of column OBJECT.OBJID = null,
    ACTUALDATE type of R_DATE = current_date)
returns (
    DBEG type of R_DATE)
AS
declare variable wdVAL type of R_CUSTOMDATA;
declare variable ubdays type of r_double;
begin
    dbeg = '01.01.2000';

    if (:clientid is NOT NULL) then
    begin
        select val
          from k_get_wares_data_obj_val(NULL,'SALEPERIOD',:waresid, :clientid, :actualdate)
          into :wdval;
        
        if (:wdval is NOT NULL) then
        begin
            select cast(rcI.data as double precision)*g.usebydate
              from gwares g
                   left join r_choice rcI on rcI.chtype='P' and rcI.code=g.ubdtype
             where g.waresid = :waresid
              into :ubdays;

            dbeg = dateadd(- floor(:ubdays * cast(:wdval as r_double) /  100.00) day to :actualdate);
        end
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARES_SALEDBEG (
    WARESID type of column GWARES.WARESID,
    CLIENTID type of column OBJECT.OBJID = null,
    ACTUALDATE type of R_DATE = current_date)
returns (
    DBEG type of R_DATE)
AS
declare variable wdVAL type of R_CUSTOMDATA;
declare variable ubdays type of r_double;
begin
    dbeg = '01.01.2000';

    if (:clientid is NOT NULL) then
    begin
        select val
          from k_get_wares_data_obj_val(NULL,'SALEPERIOD',:waresid, :clientid, :actualdate)
          into :wdval;
        
        if (:wdval is NOT NULL) then
        begin
            select cast(rcI.data as double precision)*g.usebydate
              from gwares g
                   left join r_choice rcI on rcI.chtype='P' and rcI.code=g.ubdtype
             where g.waresid = :waresid
              into :ubdays;

            dbeg = dateadd(- floor(:ubdays * cast(:wdval as r_double) /  100.00)+1 day to :actualdate);
        end
    end

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_WARES_SALEDBEG (
    WARESID type of column GWARES.WARESID,
    CLIENTID type of column OBJECT.OBJID = null,
    ACTUALDATE type of R_DATE = current_date)
returns (
    DBEG type of R_DATE)
AS
declare variable wdVAL type of R_CUSTOMDATA;
declare variable ubdays type of r_double;
begin
    dbeg = '01.01.2000';

    if (:clientid is NOT NULL) then
    begin
        select val
          from k_get_wares_data_obj_val(NULL,'SALEPERIOD',:waresid, :clientid, :actualdate)
          into :wdval;
        
        if (:wdval is NOT NULL) then
        begin
            select cast(rcI.data as double precision)*g.usebydate
              from gwares g
                   left join r_choice rcI on rcI.chtype='P' and rcI.code=g.ubdtype
             where g.waresid = :waresid
              into :ubdays;

            dbeg = dateadd(-floor(:ubdays * cast(:wdval as r_double) / 100.00)+1 day to :actualdate);
        end
    end

    suspend;
end^

SET TERM ; ^


