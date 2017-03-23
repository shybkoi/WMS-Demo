

SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_PRINTPALLET (
    PRINTERID R_ID,
    STACKID R_ID,
    PALLETID R_ID,
    IDUSER R_ID)
AS
declare variable PrinterName type of R_NAME;
declare variable QUETASKID type of R_ID;
declare variable MANID type of R_ID;
declare variable rule varchar(60);
declare variable userfio varchar(255);
declare variable params varchar(8192);
declare variable tasktypeid R_ID;
begin
  select Name
    from WM_PRINTERS
   where printerid = :printerid
    into :PrinterName;
  if (PrinterName is null) then
    exception exc_ur_common 'Не найден принтер с таким штрих-кодом.';

  select QuetaskID from WM_CONFIG into :QUETASKID;

  execute procedure wh_ttid_incomefg
   returning_values :tasktypeid;

  execute procedure WM_GETPARAMVALUE(:tasktypeid, null,  null,  'REPORTS')
  returning_values Rule;
  select Name
    from R_REPORT
   where ReportID = :Rule
    into Rule;

  select ku.id_man, ku.fio
    from k_users ku
   where ku.id_user = :iduser
    into :manid, :userfio;
  if (:palletid is NULL) then palletid = 0;

  if (:palletid is NOT NULL and :palletid>0) then
  begin
    params = '<params><ProdLineID value="None"/>
            <WaresID value="None"/>
            <ManID value="' || cast(:manid as varchar(10)) || '"/>
            <ProducerID value="None"/>
            <PrDate value="None"/>
            <PFID value="None"/>
            <PalletID value="'||cast(:palletid as varchar(10))||'"/>
            <printer value="'||:PrinterName||'"/>
            <PrintAfterDone value="1"/></params>';

     execute procedure WM_CREATEQUEUETASK(:QUETASKID,:RULE,:userfio,:PARAMS)
      returning_values :tasktypeid;
  end
  else
  begin
    for
        select p.p_id
          from wh_incomefg_stacklistpallets(:stackid) p
          into :palletid
    do
    begin
        params = '<params><ProdLineID value="None"/>
                <WaresID value="None"/>
                <ManID value="' || cast(:manid as varchar(10)) || '"/>
                <ProducerID value="None"/>
                <PrDate value="None"/>
                <PFID value="None"/>
                <PalletID value="'||cast(:palletid as varchar(10))||'"/>
                <printer value="'||:PrinterName||'"/>
                <PrintAfterDone value="1"/></params>';
    
         execute procedure WM_CREATEQUEUETASK(:QUETASKID,:RULE,:userfio,:PARAMS)
          returning_values :tasktypeid;
    end
  end
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_PALLET_BYNUMBER (
    PALNUMBER type of column PALLET.number
)
returns (
    PALLETID type of column PALLET.palletid
)
as
begin
    select p.palletid
      from pallet p
     where p.number = :palnumber
       and p.status <> '2'
      into :palletid;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_PALLET_REPRINT (
    palletid type of column PALLET.palletid,
    printerid type of column wm_printers.printerid,
    wmsid type of column WM_SESSION.sessionid
)
as
declare variable ptCode type of column pallet_type.code;
declare variable id_user type of column K_USERS.id_user;
begin
    select pt.code
      from pallet p
           left join pallet_type pt on pt.id = p.ptypeid
     where p.palletid = :palletid
      into :ptCode;

    if (:ptcode = 'I') then
        execute procedure WH_INCOME_PRINTPALLET ('INCOME', :wmsid, :palletid, :printerid, 1);
    else if (:ptcode = 'CR') then
        execute procedure WH_INCOME_PRINTPALLET ('COMERETURN', :wmsid, :palletid, :printerid, 1);
    else if (:ptCode = 'FP') then
    begin
        select ku.id_user
          from wm_session wms
               left join k_users ku on ku.id_man = wms.objid
         where wms.sessionid = :wmsid
          into :id_user;
        execute procedure WH_INCOMEFG_PRINTPALLET (:printerid, NULL, :palletid, :id_user);
    end
end^

SET TERM ; ^

