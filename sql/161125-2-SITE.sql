

SET TERM ^ ;

CREATE OR ALTER procedure K_SITE_LIST (
    AOBJID type of R_ID,
    ASITEID type of R_ID,
    AHIGHER type of R_ID,
    ASITETID type of R_ID,
    ASTATUS type of R_STATUS)
returns (
    OBJID type of R_ID,
    SITEID type of R_ID,
    NAME type of R_NAME,
    HIGHER type of R_ID,
    SITETID type of R_ID,
    SITETNAME type of R_NAME,
    STATUS type of R_STATUS,
    BARCODE type of R_BARCODE,
    INTERIOR char(1))
AS
declare variable sql varchar(1000);
declare variable flag char(1);
declare variable siteid_del type of column SITE.siteid;
begin

/*
    ahigher = 0  забрать все записи
    interior = 0 вложенности нет
             = 1 вложенность есть
*/

    if (:asiteid is not null) then
    begin
        select s.siteid, s.name, s.objid, s.higher, s.status, s.barcode, s.sitespeciesid, ss.name
          from site s
               left join sitespecies ss on ss.sitespeciesid = s.sitespeciesid
         where s.siteid = :asitetid
          into :siteid, :name, :objid, :higher, :status, :barcode, :sitetid, :sitetname;

        suspend;
    end
    else
    begin
        select coalesce(w.siteid_delpallets, 0)
          from wm_config w
          into :siteid_del;

        flag = '0';

        sql = 'select distinct s.siteid, s.name, s.objid, s.higher, s.status, s.barcode, s.sitespeciesid, ss.name
                 from site s
                      left join sitespecies ss on ss.sitespeciesid = s.sitespeciesid';

        if (:siteid_del is NOT NULL) then
        begin
            sql = :sql || ' where s.siteid <> ' || cast(:siteid_del as varchar(10));
            flag = '1';
        end

        if (:aobjid is not null) then
        begin
            if (:flag = '0') then
            begin
                sql = :sql || ' where s.objid = ' || cast(:aobjid as varchar(10));
                flag = '1';
            end
            else
            begin
                sql = :sql || ' and s.objid = ' || cast(:aobjid as varchar(10));
            end
        end


        if (:ahigher is null) then
            if (:flag = '0') then
            begin
                sql = :sql || ' where s.higher is null';
                flag = '1';
            end
            else
                sql = :sql || ' and s.higher is null';
        else
            if (:ahigher <> '0') then
                if (:flag = '0') then
                begin
                    sql = :sql ||  ' where s.higher = ' || cast(:ahigher as varchar(10));
                    flag = '1';
                end
                else
                    sql = :sql ||  ' and s.higher = ' || cast(:ahigher as varchar(10));

        if (:asitetid is not null) then
            if (:flag = '0') then
            begin
                sql = :sql || ' where s.sitespeciesid = ' || cast(:asitetid as varchar(10));
                flag = '1';
            end
            else
                sql = :sql || ' and s.sitespeciesid = ' || cast(:asitetid as varchar(10));

        if (:astatus is not null) then
            if (:flag = '0') then
            begin
                sql = :sql || ' where s.status = ' || :astatus;
                flag = '1';
            end
            else
                sql = :sql || ' and s.status = ' || :astatus;

        sql = :sql || ' order by ss.name';
    
        for
            execute statement :sql
            into :siteid, :name, :objid, :higher, :status, :barcode, :sitetid, :sitetname
        do
        begin
            interior = '0';

            if (exists (select s.siteid
                          from site s
                         where s.higher = :siteid ) ) then
                interior = '1';

            suspend;

         /*   if (:ahigher is not null and :ahigher <> 0) then
              for
                select sl.siteid, sl.objid, sl.higher, sl.status, sl.barcode, sl.sitetid, sl.sitetname
                  from K_SITE_LIST(:objid,null,:siteid,null,:status) sl
                  into :siteid, :objid, :higher, :status, :barcode, :sitetid, :sitetname
              do
                suspend;     */
        end
    end
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
    if (coalesce(new.ph,0) <> coalesce(old.ph,0) or coalesce(new.pw,0) <> coalesce(old.pw,0)
        or new.status <> old.status
    ) then
    begin
        delete from model_stack_ref_site_wares mssw
         where mssw.siteid = new.siteid;
        
        FLAGMODEL = '1';
    end

    if (new.status = '1'
        and (:flagmodel = '1' or coalesce(new.pl,0) <> coalesce(old.pl, 0))
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
  declare variable siteid type of column SITE.siteid ;
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
    if (coalesce(new.ph,0) <> coalesce(old.ph,0) or coalesce(new.pw,0) <> coalesce(old.pw,0)
        or new.status <> old.status
    ) then
    begin
        delete from model_stack_ref_site_wares mssw
         where mssw.siteid = new.siteid;
        
        FLAGMODEL = '1';
    end

    if (new.status = '1'
        and (:flagmodel = '1' or coalesce(new.pl,0) <> coalesce(old.pl, 0))
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

  if (exists(select *
               from wm_config w
              where w.siteid_delpallets = new.higher)) then
  begin
    for
        with recursive sr as (
            select s.siteid, s.status
              from site s
             where s.higher = new.siteid
             union all
             select s.siteid, s.status
               from sr
                    join site s on s.higher = sr.siteid
        )
        select sr.siteid
          from sr
         where sr.status <> '0'
          into :siteid
    do
        update site s
           set s.status = '0'
         where s.siteid = :siteid;
  end
END^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER trigger wm_busite for site
active before update position 4
AS
  DECLARE VARIABLE Code VARCHAR(10);
  DECLARE VARIABLE higher integer;
  DECLARE VARIABLE obj integer;
  declare variable objcode type of r_code3;
BEGIN
  IF (NEW.SiteSpeciesID <> OLD.SiteSpeciesID or NEW.siteid <> OLD.siteid or new.BARCODE is NULL) THEN BEGIN
    SELECT SiteType FROM SITESPECIES WHERE SiteSpeciesID = NEW.SiteSpeciesID
    INTO Code;

      select w.objcode
        from wm_config w
        into :objcode;
    
      if (:objcode is Not null and :objcode='DR') then NEW.BarCode = Code||NEW.SiteID;
      else NEW.BarCode = 'S'||NEW.SiteID;
  END

  IF (NEW.Higher IS NOT NULL AND C(NEW.ObjID) <> C(OLD.ObjID) AND NEW.ObjID IS NOT NULL) THEN
    begin
      -- если у родителя objid-null то дочерние могут иметь различный objid
         higher = new.higher;
         while (:higher is not null) do
           select s.higher, s.objid
             from site s
            where s.siteid = :higher
             into :higher, :obj;

      if (:obj is not null) then
        IF (NOT EXISTS(SELECT SiteID FROM SITE WHERE SiteID = NEW.Higher AND ObjID = NEW.ObjID))
          THEN EXCEPTION WM_OBJSITE_NOTVALID;
    end

  if (new.status<>'0' and
      exists(select *
               from wm_config w
              where w.siteid_delpallets = new.higher)) then
     new.status = '0';

END^

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
  declare variable siteid type of column SITE.siteid ;
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
    if (coalesce(new.ph,0) <> coalesce(old.ph,0) or coalesce(new.pw,0) <> coalesce(old.pw,0)
        or new.status <> old.status
    ) then
    begin
        delete from model_stack_ref_site_wares mssw
         where mssw.siteid = new.siteid;
        
        FLAGMODEL = '1';
    end

    if (new.status = '1'
        and (:flagmodel = '1' or coalesce(new.pl,0) <> coalesce(old.pl, 0))
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

  if ((coalesce(new.higher,0) <> coalesce(old.higher,0) or new.status<> old.status)
      and exists(select *
               from wm_config w
              where w.siteid_delpallets = new.higher)) then
  begin
    for
        with recursive sr as (
            select s.siteid, s.status
              from site s
             where s.higher = new.siteid
             union all
             select s.siteid, s.status
               from sr
                    join site s on s.higher = sr.siteid
        )
        select sr.siteid
          from sr
         where sr.status <> '0'
          into :siteid
    do
        update site s
           set s.status = '0'
         where s.siteid = :siteid;
  end
END^

SET TERM ; ^

