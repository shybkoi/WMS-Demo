

SET TERM ^ ;

create or alter procedure K_U3S_INCOME_STATUSCHG (
    DOCID R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable TASKID type of R_ID;
declare variable TASKTYPEID type of R_ID;
declare variable TASKMETHODID type of R_ID;
declare variable TTINITST type of R_STATUS;
declare variable DOCDATE type of R_DATE;
declare variable FROMOBJ type of R_ID;
declare variable SITEID type of R_ID;
declare variable OBJID type of R_ID;
begin
    if (:newstat = 'c') then
    begin
        SELECT ttid,ttinitst
          FROM k_tasktype_by_code('INCOMEFG','1')
          into :tasktypeid,:ttinitst;

        select d.fromobj, d.toobj, d.realdocdate
          from document d
         where d.docid = :docid
          into :fromobj, :objid, :docdate;

        if (exists(select *
                     from wh_obj_info wh
                    where wh.objid = :objid
                      and wh.datestart >= :docdate
                      and coalesce(wh.fromobjincome,0) = coalesce(:fromobj,0) )) then
        begin
            select tm.methodid
              from wm_taskmethod tm
             where tm.tasktypeid = :tasktypeid
               and tm.algorithm = 'F'
              into :taskmethodid;

            if (:taskmethodid is NULL) then
                exception exc_k_wrongtasktype 'Не найден метод с кодом F у типа задания приемка от поставщика!';

            select first(1) t.taskid
              from wm_task t
             where t.docid = :docid
               and t.tasktypeid = :tasktypeid
              into :taskid;

            if (:taskid is NULL) then
            begin
                siteid = NULL;
                select first(1) s.siteid
                  from sitespecies sp
                       left join site s on s.sitespeciesid = sp.sitespeciesid
                 where sp.code = 'E'
                  into :siteid;

                INSERT INTO wm_task(tasktypeid,status,docid,wm_sessionid,taskmethodid,siteid)
                VALUES(:tasktypeid,:ttinitst,:docid,null,:taskmethodid,:siteid)
                returning taskid
                into :taskid;
            end
            else
            begin
                update wm_task t
                   set t.taskmethodid = :taskmethodid,
                       t.wm_sessionid = NULL,
                       t.status = :ttinitst
                  where t.taskid = :taskid;
            end
        end
    end
    else if (:newstat = 'w') then
    begin
         taskid = NULL;
         for
            select t.taskid
              from wm_task t
                   left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                   left join wm_taskmethod tm on tm.methodid = t.taskmethodid
             where t.docid = :docid
               and tt.code = 'INCOMEFG'
               and tm.algorithm = 'F'
              into :taskid
         do
            update wm_task t
               set t.status = '2',t.endtime = current_timestamp
             where t.taskid = :taskid and t.status <> '2';

        execute procedure wh_core_setdocbytasklot(:docid);
/*        execute procedure RBS_Q_CREATETASKEXPORT('K_UV_INCOMEFG_STATUSCHG: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
         returning_values :docid;*/

    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_U3S_INCOMEFG_STATUSCHG (
    DOCID R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable TASKID type of R_ID;
begin
    if (:newstat = 'w') then
    begin
         taskid = NULL;
         for
            select t.taskid
              from wm_task t
                   left join wm_tasktype tt on tt.tasktypeid = t.tasktypeid
                   left join wm_taskmethod tm on tm.methodid = t.taskmethodid
             where t.docid = :docid
               and tt.code = 'INCOMEFG'
               and tm.algorithm = 'F'
              into :taskid
         do
            update wm_task t
               set t.status = '2',t.endtime = current_timestamp
             where t.taskid = :taskid and t.status <> '2';

        execute procedure uv_intara_create(:docid);
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SITESTACK_INFO (
    ID type of column SITE.siteid)
returns (
    S_ID type of column SITE.siteid,
    S_NAME type of column SITE.siteid,
    S_STAT type of column SITE.status,
    S_MODELID type of column model_stack.modelid,
    S_MODELNAME type of column model_stack.name,
    S_PALID type of column PALLET.palletid,
    S_PALNUM type of column PALLET.number,
    S_PALBARCODE type of column PALLET.barcode,
    S_WID type of column GWARES.waresid,
    S_WCODE type of column GWARES.code,
    S_WNAME type of column GWARES.name,
    S_WVUFACTOR type of column WARESUNIT.factor,
    S_WVUCODE type of column UNIT.shortname,
    S_WMUFACTOR type of column WARESUNIT.factor,
    S_WMUCODE type of column UNIT.shortname,
    S_WPRODUCTDATE type of column SITE_STACK.productdate,
    S_WBESTBEFOREDATE type of column SITE_STACK.bestbeforedate,
    S_PALMAXCNT type of column SITE_STACK.palmaxcnt,
    S_PALCURCNT type of column SITE_STACK.palcurcnt)
AS
begin
    select s.siteid,s.status,s.name,
           ms.modelid, ms.name,
           st.productdate, st.bestbeforedate,
           st.palmaxcnt, st.palcurcnt,
           g.waresid, g.code, g.name,
           vwu.factor, vu.shortname, mwu.factor, mu.shortname,
           p.palletid, p.number, p.barcode
      from site s
           left join site_stack st on s.siteid = st.siteid
           left join model_stack ms on ms.modelid = st.modelid
           left join gwares g
                left join waresunit vwu
                     left join unit vu on vu.unitid = vwu.unitid
                  on vwu.waresunitid = g.viewunitid
                left join waresunit mwu
                     left join unit mu on mu.unitid = mwu.unitid
                  on mwu.waresunitid = g.mainunitid
             on g.waresid = st.waresid
            left join pallet p on p.palletid = st.palletid
     where s.siteid = :id
      into :s_id,:s_stat,:s_name,
           :s_modelid, s_modelname,
           :s_wproductdate, :s_wbestbeforedate,
           :s_palmaxcnt, :s_palcurcnt,
           :s_wid, :s_wcode, :s_wname,
           :s_wvufactor, :s_wvucode, :s_wmufactor, :s_wmucode,
           :s_palid, :s_palnum, :s_palbarcode;

    suspend;
end^

SET TERM ; ^



DROP PROCEDURE WH_VERIFY_STACK_INFO;



SET TERM ^ ;

CREATE OR ALTER procedure WH_SITESTACK_INFO (
    ID type of column SITE.siteid)
returns (
    S_ID type of column SITE.siteid,
    S_NAME type of column SITE.siteid,
    S_STAT type of column SITE.status,
    S_MODELID type of column model_stack.modelid,
    S_MODELNAME type of column model_stack.name,
    S_PALID type of column PALLET.palletid,
    S_PALNUM type of column PALLET.number,
    S_PALBARCODE type of column PALLET.barcode,
    S_SPCODE type of column sitespecies.code,
    S_WID type of column GWARES.waresid,
    S_WCODE type of column GWARES.code,
    S_WNAME type of column GWARES.name,
    S_WVUFACTOR type of column WARESUNIT.factor,
    S_WVUCODE type of column UNIT.shortname,
    S_WMUFACTOR type of column WARESUNIT.factor,
    S_WMUCODE type of column UNIT.shortname,
    S_WPRODUCTDATE type of column SITE_STACK.productdate,
    S_WBESTBEFOREDATE type of column SITE_STACK.bestbeforedate,
    S_PALMAXCNT type of column SITE_STACK.palmaxcnt,
    S_PALCURCNT type of column SITE_STACK.palcurcnt)
AS
begin
    select s.siteid,s.status,s.name,sp.code,
           ms.modelid, ms.name,
           st.productdate, st.bestbeforedate,
           st.palmaxcnt, st.palcurcnt,
           g.waresid, g.code, g.name,
           vwu.factor, vu.shortname, mwu.factor, mu.shortname,
           p.palletid, p.number, p.barcode
      from site s
           left join site_stack st on s.siteid = st.siteid
           left join model_stack ms on ms.modelid = st.modelid
           left join gwares g
                left join waresunit vwu
                     left join unit vu on vu.unitid = vwu.unitid
                  on vwu.waresunitid = g.viewunitid
                left join waresunit mwu
                     left join unit mu on mu.unitid = mwu.unitid
                  on mwu.waresunitid = g.mainunitid
             on g.waresid = st.waresid
            left join pallet p on p.palletid = st.palletid
            left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
     where s.siteid = :id
      into :s_id,:s_stat,:s_name,:s_spcode,
           :s_modelid, s_modelname,
           :s_wproductdate, :s_wbestbeforedate,
           :s_palmaxcnt, :s_palcurcnt,
           :s_wid, :s_wcode, :s_wname,
           :s_wvufactor, :s_wvucode, :s_wmufactor, :s_wmucode,
           :s_palid, :s_palnum, :s_palbarcode;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SITESTACK_INFO (
    ID type of column SITE.siteid)
returns (
    S_ID type of column SITE.siteid,
    S_NAME type of column SITE.siteid,
    S_STAT type of column SITE.status,
    S_MODELID type of column model_stack.modelid,
    S_MODELNAME type of column model_stack.name,
    S_PALID type of column PALLET.palletid,
    S_PALNUM type of column PALLET.number,
    S_PALBARCODE type of column PALLET.barcode,
    S_SPCODE type of column sitespecies.code,
    S_PL type of column site.pl,
    S_PW type of column site.pw,
    S_PH type of column site.ph,
    S_WID type of column GWARES.waresid,
    S_WCODE type of column GWARES.code,
    S_WNAME type of column GWARES.name,
    S_WVUFACTOR type of column WARESUNIT.factor,
    S_WVUCODE type of column UNIT.shortname,
    S_WMUFACTOR type of column WARESUNIT.factor,
    S_WMUCODE type of column UNIT.shortname,
    S_WPRODUCTDATE type of column SITE_STACK.productdate,
    S_WBESTBEFOREDATE type of column SITE_STACK.bestbeforedate,
    S_PALMAXCNT type of column SITE_STACK.palmaxcnt,
    S_PALCURCNT type of column SITE_STACK.palcurcnt)
AS
begin
    select s.siteid,s.status,s.name,sp.code,
           s.pl, s.pw, s.ph, 
           ms.modelid, ms.name,
           st.productdate, st.bestbeforedate,
           st.palmaxcnt, st.palcurcnt,
           g.waresid, g.code, g.name,
           vwu.factor, vu.shortname, mwu.factor, mu.shortname,
           p.palletid, p.number, p.barcode
      from site s
           left join site_stack st on s.siteid = st.siteid
           left join model_stack ms on ms.modelid = st.modelid
           left join gwares g
                left join waresunit vwu
                     left join unit vu on vu.unitid = vwu.unitid
                  on vwu.waresunitid = g.viewunitid
                left join waresunit mwu
                     left join unit mu on mu.unitid = mwu.unitid
                  on mwu.waresunitid = g.mainunitid
             on g.waresid = st.waresid
            left join pallet p on p.palletid = st.palletid
            left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
     where s.siteid = :id
      into :s_id,:s_stat,:s_name,:s_spcode,
           :s_pl, :s_pw, :s_ph,
           :s_modelid, s_modelname,
           :s_wproductdate, :s_wbestbeforedate,
           :s_palmaxcnt, :s_palcurcnt,
           :s_wid, :s_wcode, :s_wname,
           :s_wvufactor, :s_wvucode, :s_wmufactor, :s_wmucode,
           :s_palid, :s_palnum, :s_palbarcode;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SITESTACK_INFO (
    ID type of column SITE.siteid)
returns (
    S_ID type of column SITE.siteid,
    S_NAME type of column SITE.NAME,
    S_STAT type of column SITE.status,
    S_MODELID type of column model_stack.modelid,
    S_MODELNAME type of column model_stack.name,
    S_PALID type of column PALLET.palletid,
    S_PALNUM type of column PALLET.number,
    S_PALBARCODE type of column PALLET.barcode,
    S_SPCODE type of column sitespecies.code,
    S_PL type of column site.pl,
    S_PW type of column site.pw,
    S_PH type of column site.ph,
    S_WID type of column GWARES.waresid,
    S_WCODE type of column GWARES.code,
    S_WNAME type of column GWARES.name,
    S_WVUFACTOR type of column WARESUNIT.factor,
    S_WVUCODE type of column UNIT.shortname,
    S_WMUFACTOR type of column WARESUNIT.factor,
    S_WMUCODE type of column UNIT.shortname,
    S_WPRODUCTDATE type of column SITE_STACK.productdate,
    S_WBESTBEFOREDATE type of column SITE_STACK.bestbeforedate,
    S_PALMAXCNT type of column SITE_STACK.palmaxcnt,
    S_PALCURCNT type of column SITE_STACK.palcurcnt)
AS
begin
    select s.siteid,s.status,s.name,sp.code,
           s.pl, s.pw, s.ph, 
           ms.modelid, ms.name,
           st.productdate, st.bestbeforedate,
           st.palmaxcnt, st.palcurcnt,
           g.waresid, g.code, g.name,
           vwu.factor, vu.shortname, mwu.factor, mu.shortname,
           p.palletid, p.number, p.barcode
      from site s
           left join site_stack st on s.siteid = st.siteid
           left join model_stack ms on ms.modelid = st.modelid
           left join gwares g
                left join waresunit vwu
                     left join unit vu on vu.unitid = vwu.unitid
                  on vwu.waresunitid = g.viewunitid
                left join waresunit mwu
                     left join unit mu on mu.unitid = mwu.unitid
                  on mwu.waresunitid = g.mainunitid
             on g.waresid = st.waresid
            left join pallet p on p.palletid = st.palletid
            left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
     where s.siteid = :id
      into :s_id,:s_stat,:s_name,:s_spcode,
           :s_pl, :s_pw, :s_ph,
           :s_modelid, s_modelname,
           :s_wproductdate, :s_wbestbeforedate,
           :s_palmaxcnt, :s_palcurcnt,
           :s_wid, :s_wcode, :s_wname,
           :s_wvufactor, :s_wvucode, :s_wmufactor, :s_wmucode,
           :s_palid, :s_palnum, :s_palbarcode;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SITESTACK_INFO (
    ID type of column SITE.siteid)
returns (
    S_ID type of column SITE.siteid,
    S_NAME type of column SITE.NAME,
    S_STAT type of column SITE.status,
    S_MODELID type of column model_stack.modelid,
    S_MODELNAME type of column model_stack.name,
    S_PALID type of column PALLET.palletid,
    S_PALNUM type of column PALLET.number,
    S_PALBARCODE type of column PALLET.barcode,
    S_SPCODE type of column sitespecies.code,
    S_SPNAME type of column sitespecies.NAME,
    S_PL type of column site.pl,
    S_PW type of column site.pw,
    S_PH type of column site.ph,
    S_WID type of column GWARES.waresid,
    S_WCODE type of column GWARES.code,
    S_WNAME type of column GWARES.name,
    S_WVUFACTOR type of column WARESUNIT.factor,
    S_WVUCODE type of column UNIT.shortname,
    S_WMUFACTOR type of column WARESUNIT.factor,
    S_WMUCODE type of column UNIT.shortname,
    S_WPRODUCTDATE type of column SITE_STACK.productdate,
    S_WBESTBEFOREDATE type of column SITE_STACK.bestbeforedate,
    S_PALMAXCNT type of column SITE_STACK.palmaxcnt,
    S_PALCURCNT type of column SITE_STACK.palcurcnt)
AS
begin
    select s.siteid,s.status,s.name,
           sp.code, sp.name,
           s.pl, s.pw, s.ph, 
           ms.modelid, ms.name,
           st.productdate, st.bestbeforedate,
           st.palmaxcnt, st.palcurcnt,
           g.waresid, g.code, g.name,
           vwu.factor, vu.shortname, mwu.factor, mu.shortname,
           p.palletid, p.number, p.barcode
      from site s
           left join site_stack st on s.siteid = st.siteid
           left join model_stack ms on ms.modelid = st.modelid
           left join gwares g
                left join waresunit vwu
                     left join unit vu on vu.unitid = vwu.unitid
                  on vwu.waresunitid = g.viewunitid
                left join waresunit mwu
                     left join unit mu on mu.unitid = mwu.unitid
                  on mwu.waresunitid = g.mainunitid
             on g.waresid = st.waresid
            left join pallet p on p.palletid = st.palletid
            left join sitespecies sp on sp.sitespeciesid = s.sitespeciesid
     where s.siteid = :id
      into :s_id,:s_stat,:s_name,
           :s_spcode, :s_spname,
           :s_pl, :s_pw, :s_ph,
           :s_modelid, s_modelname,
           :s_wproductdate, :s_wbestbeforedate,
           :s_palmaxcnt, :s_palcurcnt,
           :s_wid, :s_wcode, :s_wname,
           :s_wvufactor, :s_wvucode, :s_wmufactor, :s_wmucode,
           :s_palid, :s_palnum, :s_palbarcode;

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_MODELSTACK_LWHSET (
    SITEID type of column SITE.siteid,
    PL type of column SITE.PL,
    PW type of column SITE.PW,
    PH type of column SITE.PH
)
as
begin
    UPDATE SITE S
       set s.pl = :pl,
           s.pw = :pw,
           s.ph = :ph
     where s.siteid = :siteid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger t_ausite for site
active after update position 0
AS
  DECLARE VARIABLE I INTEGER;
  DECLARE VARIABLE CHILDSPECIES INTEGER;
  DECLARE VARIABLE CHILDCOUNT SMALLINT;
  DECLARE VARIABLE SITETYPE CHAR(1);

  declare variable FLAGMODEL type of R_FLAG = '0';
  declare variable modelid type of column MODEL_STACK.modelid;
  declare variable waresid type of column GWARES.waresid;
  declare variable palletcount type of column MODEL_STACK_REF_SITE_WARES.palletcount;
BEGIN
  IF (C(OLD.ObjID) != C(NEW.ObjID)) THEN
    UPDATE SITE SET ObjID = NEW.ObjID
    WHERE Higher = NEW.SiteID AND C(ObjID) = C(OLD.ObjID);
  IF (OLD.SiteSpeciesID != NEW.SiteSpeciesID) THEN
  BEGIN
    SELECT ChildSpecies, ChildCount, SiteType FROM SITESPECIES
      WHERE SiteSpeciesID = NEW.SiteSpeciesID
    INTO ChildSpecies, ChildCount, SiteType;
    DELETE FROM SITE WHERE Higher = NEW.SiteID;
    /* создаем вложенные местоположения */
    IF (ChildSpecies IS NOT NULL) THEN BEGIN
      I = 1;
      WHILE (I <= ChildCount) DO BEGIN
        INSERT INTO SITE (SiteSpeciesID, Higher, Name, Status, ObjID)
        VALUES (:ChildSpecies, NEW.SiteID, '', '1', NEW.ObjID);
        I = I + 1;
      END
    END
    /* виртуальный паллет для места отборки */
    IF (SiteType = 'S') THEN BEGIN
      IF (NOT EXISTS(SELECT PalletID FROM PALLET WHERE PalletType = '1' AND SiteID = NEW.SiteID))
      THEN
        INSERT INTO PALLET(PalletType, Status, SiteID, PTypeId)
        VALUES ('1', '1', NEW.SiteID, 2);
    END
    ELSE
      DELETE FROM PALLET WHERE SiteID = NEW.SiteID AND PalletType = '1';
  END

  if (exists(select *
                from sitespecies sp
               where sp.sitespeciesid = new.sitespeciesid
                 and sp.code = 'STACK')) then
  begin
    if (coalesce(new.ph,0) <> coalesce(old.ph,0) or coalesce(new.pw,0) <> coalesce(old.pw,0)) then
    begin
        delete from model_stack_ref_site_wares mssw
         where mssw.siteid = new.siteid;
        
        FLAGMODEL = '1';
    end

    if (
        (:flagmodel = '1' or coalesce(new.pl,0) <> coalesce(old.pl, 0))
         and coalesce(new.pl, 0) > 0
         and coalesce(new.pw, 0) > 0
         and coalesce(new.ph, 0) > 0
    ) then
    begin
        for
            select distinct w.modelid
              from model_stack_ref_waresid w
              into :modelid
        do
        if (exists(select *
                     from model_stack ms
                    where ms.modelid = :modelid
                      and ms.pw = new.pw
                      and ms.ph >= new.ph)) then
        begin
            delete from tmp_scheme_modelstack;
            execute procedure wh_tmp_scheme_modelstack_fill(:modelid, new.pl);
            
            select max(t.palnum)
              from tmp_scheme_modelstack t
             where t.pl = new.pl
              into :palletcount;

            for
                select w.waresid
                  from model_stack_ref_waresid w
                 where w.modelid = :modelid
                  into :waresid
            do
                update or insert into MODEL_STACK_REF_SITE_WARES ( MODELID, SITEID, WARESID, PALLETCOUNT)
                values ( :modelid, new.siteid, :waresid, :palletcount)
                matching( MODELID, SITEID, WARESID);
        end
    end
  end
END^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_MODELSTACK_LWHSET (
    SITEID type of column SITE.siteid,
    PL type of column SITE.PL,
    PW type of column SITE.PW,
    PH type of column SITE.PH
)
as
begin
    if (not exists(select *
                     from model_stack ms
                    where ms.pw = :pw )) then
        exception exc_k_common 'Нет моделей с указанной шириной!';

    UPDATE SITE S
       set s.pl = :pl,
           s.pw = :pw,
           s.ph = :ph
     where s.siteid = :siteid;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_MODELSTAK_SETWARESMODELS (
    WID type of column GWARES.waresid,
    MODELS type of rbs_bigvarchar,
    PRIORITIES type of rbs_bigvarchar
)
as
declare variable i type of r_shortnumber;
declare variable pr_old type of column MODEL_STACK_REF_WARESID.priority;
declare variable pr_new type of column MODEL_STACK_REF_WARESID.priority;
declare variable modelid type of column model_stack.modelid;
begin
  I = 0;
  FOR
    select r.word, coalesce(sw.priority, 0)
      from r_listwords(:models, ',', 0) r
           left join MODEL_STACK_REF_WARESID sw on sw.waresid = :wid and sw.modelid = cast(r.word as r_id)
      into :modelid, :pr_old
  do
  begin
    I = :I + 1;
    pr_new = WORDNUM(:priorities,:I,';','0');

    if (:pr_new <> :pr_old) then
    begin
        if (:pr_new = 0) then
            delete from MODEL_STACK_REF_WARESID sw
             where sw.waresid = :wid and sw.modelid = :modelid;
        else
            update or insert into MODEL_STACK_REF_WARESID ( MODELID, WARESID, PRIORITY)
            values ( :modelid, :wid, :pr_new)
            matching (modelid, waresid);
    end

  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_MODELSTAK_SETWARESMODELS (
    WID type of column GWARES.waresid,
    MODELS type of rbs_bigvarchar,
    PRIORITIES type of rbs_bigvarchar
)
as
declare variable i type of r_shortnumber;
declare variable pr_old type of column MODEL_STACK_REF_WARESID.priority;
declare variable pr_new type of column MODEL_STACK_REF_WARESID.priority;
declare variable modelid type of column model_stack.modelid;
begin
  I = 0;
  FOR
    select r.word, coalesce(sw.priority, 0)
      from r_listwords(:models, ';', 0) r
           left join MODEL_STACK_REF_WARESID sw on sw.waresid = :wid and sw.modelid = cast(r.word as r_id)
      into :modelid, :pr_old
  do
  begin
    I = :I + 1;
    pr_new = WORDNUM(:priorities,:I,';','0');

    if (:pr_new <> :pr_old) then
    begin
        if (:pr_new = 0) then
            delete from MODEL_STACK_REF_WARESID sw
             where sw.waresid = :wid and sw.modelid = :modelid;
        else
            update or insert into MODEL_STACK_REF_WARESID ( MODELID, WARESID, PRIORITY)
            values ( :modelid, :wid, :pr_new)
            matching (modelid, waresid);
    end

  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_TMP_SCHEME_MODELSTACK_FILL (
    MODELID type of column MODEL_STACK.MODELID,
    STACK_PL_MAX type of R_SHORTNUMBER)
AS
declare variable model_scheme_pl type of column scheme_modelstack.pl;
declare variable pnum type of column scheme_modelstack.number;
declare variable pnumnext type of column scheme_modelstack.nextnumber;
begin
    DELETE FROM TMP_SCHEME_MODELSTACK WHERE 1=1;
    model_scheme_pl = 1;
    pnumnext = 1;
    pnum = 0;
    while (:model_scheme_pl <= :stack_pl_max) do
    begin
        pnum = :pnum + 1;

        insert into TMP_SCHEME_MODELSTACK ( PALNUM, PL)
        values ( :pnum, :model_scheme_pl);

        select sms.nextnumber, :model_scheme_pl + sms.pl
          from scheme_modelstack sms
         where sms.number = :pnumnext
           and sms.modelid = :modelid
          into :pnumnext, :model_scheme_pl;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_MODELSTAK_SETWARESMODELS (
    WID type of column GWARES.waresid,
    MODELS type of rbs_bigvarchar,
    PRIORITIES type of rbs_bigvarchar
)
as
declare variable i type of r_shortnumber;
declare variable pr_old type of column MODEL_STACK_REF_WARESID.priority;
declare variable pr_new type of column MODEL_STACK_REF_WARESID.priority;
declare variable modelid type of column model_stack.modelid;
begin
  I = 0;
  FOR
    select r.word, coalesce(sw.priority, 0)
      from r_listwords(:models, ';', 0) r
           left join MODEL_STACK_REF_WARESID sw on sw.waresid = :wid and sw.modelid = cast(r.word as r_id)
      into :modelid, :pr_old
  do
  begin
    I = :I + 1;
    pr_new = WORDNUM(:priorities,:I,';','0');

    if (:pr_new <> :pr_old) then
    begin
        if (:pr_new = 0) then
            delete from MODEL_STACK_REF_WARESID sw
             where sw.waresid = :wid and sw.modelid = :modelid;
        else
            update or insert into MODEL_STACK_REF_WARESID ( MODELID, WARESID, PRIORITY)
            values ( :modelid, :wid, :pr_new)
            matching (modelid, waresid);
    end

  end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger model_stack_ref_waresid_ai for model_stack_ref_waresid
active after insert position 0
as
declare variable model_pw type of column model_stack.pw;
declare variable model_ph type of column model_stack.ph;
declare variable spid_stack type of column sitespecies.sitespeciesid;
declare variable stack_pl_max type of column site.pl;
declare variable palletcount type of column model_stack_ref_site_wares.palletcount;
declare variable stackid type of column site.siteid;
begin
    select ms.pw, ms.ph
      from model_stack ms
     where ms.modelid = new.modelid
      into :model_pw, :model_ph;

    select sp.sitespeciesid
      from sitespecies sp
     where sp.code = 'STACK'
      into :spid_stack;


    select max(s.pl)
      from site s
     where s.sitespeciesid = :spid_stack
       and s.pw = :model_pw
       and s.pl is NOT NULL and s.pl > 0
       and s.ph >= :model_ph
      into :stack_pl_max;

    if (:stack_pl_max is Null or :stack_pl_max = 0) then
    begin
        exit;
    end

    execute procedure WH_TMP_SCHEME_MODELSTACK_FILL(new.modelid, :stack_pl_max);
    /*model_scheme_pl = 1;
    pnumnext = 1;
    pnum = 0;
    while (:model_scheme_pl <= :stack_pl_max) do
    begin
        pnum = :pnum + 1;

        insert into TMP_SCHEME_MODELSTACK ( PALNUM, PL)
        values ( :pnum, :model_scheme_pl);

        select sms.nextnumber, :model_scheme_pl + sms.pl
          from scheme_modelstack sms
         where sms.number = :pnumnext
           and sms.modelid = new.modelid
          into :pnumnext, :model_scheme_pl;
    end*/

    for
        select s.siteid, max(t.palnum)
          from site s
               left join TMP_SCHEME_MODELSTACK t on t.pl = s.pl
         where s.sitespeciesid = :spid_stack
           and s.pw = :model_pw
           and s.ph >= :model_ph
         group by s.siteid
          into :stackid, :palletcount
    do
    begin
        update or insert into MODEL_STACK_REF_SITE_WARES ( MODELID, SITEID, WARESID, PALLETCOUNT)
        values ( new.modelid, :stackid, new.waresid, :palletcount)
        matching( MODELID, SITEID, WARESID);
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_MODELSTAK_SETWARESMODELS (
    WID type of column GWARES.waresid,
    MODELS type of rbs_bigvarchar,
    PRIORITIES type of rbs_bigvarchar
)
as
declare variable i type of r_shortnumber;
declare variable pr_old type of column MODEL_STACK_REF_WARESID.priority;
declare variable pr_new type of column MODEL_STACK_REF_WARESID.priority;
declare variable modelid type of column model_stack.modelid;
begin
  I = 0;
  FOR
    select r.word, coalesce(sw.priority, 0)
      from r_listwords(:models, ';', 0) r
           left join MODEL_STACK_REF_WARESID sw on sw.waresid = :wid and sw.modelid = cast(r.word as r_id)
      into :modelid, :pr_old
  do
  begin
    I = :I + 1;
    pr_new = WORDNUM(:priorities,:I,';','0');

    if (:pr_new <> :pr_old) then
    begin
        if (:pr_new = 0) then
            delete from MODEL_STACK_REF_WARESID sw
             where sw.waresid = :wid and sw.modelid = :modelid;
        else
            update or insert into MODEL_STACK_REF_WARESID ( MODELID, WARESID, PRIORITY)
            values ( :modelid, :wid, :pr_new)
            matching (modelid, waresid);
    end

  end
end^

SET TERM ; ^

