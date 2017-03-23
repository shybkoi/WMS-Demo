

CREATE TABLE WARESGROUP_SINGULARITY (
    ID R_ID NOT NULL,
    NAME R_NAME NOT NULL,
    EGAISNEED R_FLAG NOT NULL);

ALTER TABLE WARESGROUP_SINGULARITY
ADD CONSTRAINT PK_WARESGROUP_SINGULARITY
PRIMARY KEY (ID);

CREATE SEQUENCE GEN_WARESGROUP_SINGULARITY_ID;

SET TERM ^ ;

create trigger waresgroup_singularity_bi for waresgroup_singularity
active before insert position 0
as
begin
  if (new.id is null) then
    new.id = gen_id(gen_waresgroup_singularity_id,1);
end^

SET TERM ; ^



ALTER TABLE WARESGROUP
ADD SINGULARITYID R_ID;



ALTER TABLE WARESGROUP
ADD CONSTRAINT FK_WARESGROUP_SINGULARITY
FOREIGN KEY (SINGULARITYID)
REFERENCES WARESGROUP_SINGULARITY(ID)
ON DELETE SET NULL
ON UPDATE SET NULL;



ALTER TABLE WARESGROUP DROP CONSTRAINT FK_WARESGROUP_SINGULARITY;

ALTER TABLE WARESGROUP
ADD CONSTRAINT FK_WARESGROUP_SINGULARITY
FOREIGN KEY (SINGULARITYID)
REFERENCES WARESGROUP_SINGULARITY(ID)
ON DELETE SET NULL
ON UPDATE CASCADE
USING INDEX FK_WARESGROUP_SINGULARITY;



CREATE EXCEPTION EXC_WH_WRONGDOCSTAT 'Ќе верный статус документа';



SET TERM ^ ;

create procedure WH_IMP_CARGO_CHK_RESERVE (
    DOCID type of column DOCUMENT.docid
)
as
declare variable wid type of column GWARES.waresid;
declare variable wname type of column GWARES.name;
begin
     select first(1) w.waresid
      from (select cg.waresid as waresid, cg.amount as q
              from imp_cargo cg
             where cg.document = :docid
             union all
            select ir.waresid as waresid, -ir.amount as q
              from imp_reserve ir
             where ir.docid = :docid) w
      group by w.waresid
      having abs(sum(w.q)) < 0.00001
       into :wid;

     if (:wid is NOT NULL) then
     begin
        select g.name
          from gwares g
         where g.waresid = :wid
          into :wname;

        exception exc_wh_reserve :wname || ': в файле количества по документу и по резерву не совпадают!';
     end
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_FUNDINCOME_AFTERIMP (
    DOCID type of column DOCUMENT.docid
)
as
declare variable docstat type of column document.status;
begin
    select d.status
      from document d
     where d.docid = :docid
      into :docstat;

    if (:docstat = 'w') then
    begin
        execute procedure WH_IMP_CARGO_CHK_RESERVE (:docid);
    end
    else
    begin
        exception exc_wh_wrongdocstat;
    end
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_IMP_CARGO_CHK (
    DOCID type of column DOCUMENT.docid
)
as
declare variable wid type of column GWARES.waresid;
declare variable wname type of column GWARES.name;
begin
     select first(1) w.waresid
      from (select ic.waresid as waresid, ic.amount as q
              from imp_cargo ic
             where ic.document = :docid
             union all
            select cg.waresid as waresid, -cg.amount as q
              from cargo cg
             where cg.document = :docid) w
      group by w.waresid
      having abs(sum(w.q)) < 0.00001
       into :wid;

     if (:wid is NOT NULL) then
     begin
        select g.name
          from gwares g
         where g.waresid = :wid
          into :wname;

        exception exc_wh_reserve :wname || ': количества в файле не совпадает с количеством по документу!';
     end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDINCOME_AFTERIMP (
    DOCID type of column DOCUMENT.docid
)
as
declare variable docstat type of column document.status;
begin
    select d.status
      from document d
     where d.docid = :docid
      into :docstat;

    if (:docstat = 'w') then
    begin
        execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid);
        execute procedure WH_IMP_CARGO_CHK(:docid);

        execute procedure wh_imp_fundincome_reserve_do(:docid);

        update document d
           set d.status = 'e'
         where d.docid = :docid;
    end
    else
    begin
        exception exc_wh_wrongdocstat;
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_U3S_FUNDINCOME_STATUSCHG (
    DOCID type of column DOCUMENT.docid,
    OLDSTAT type of column R_STATUS.code,
    NEWSTAT type of column R_STATUS.code)
AS
declare variable queueid type of column r_queue.queueid;
begin
    if (:newstat = 'w') then
         execute procedure RBS_Q_CREATETASKEXPORT('FUNDINCOME_STATUSCHG: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
          returning_values :queueid;
end^

SET TERM ; ^



CREATE TABLE DOCUMENT_WGSINGULARITY (
    DOCID R_ID64 NOT NULL,
    SINGULARITYID R_ID NOT NULL);

ALTER TABLE DOCUMENT_WGSINGULARITY
ADD CONSTRAINT PK_DOCUMENT_WGSINGULARITY
PRIMARY KEY (DOCID);



ALTER TABLE DOCUMENT_WGSINGULARITY
ADD CONSTRAINT FK_DOCUMENT_WGSINGULARITY_DOCID
FOREIGN KEY (DOCID)
REFERENCES DOCUMENT(DOCID)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE DOCUMENT_WGSINGULARITY
ADD CONSTRAINT FK_DOCUMENT_WGSINGULARITY_SID
FOREIGN KEY (SINGULARITYID)
REFERENCES WARESGROUP_SINGULARITY(ID)
ON DELETE CASCADE
ON UPDATE CASCADE;



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYPALLET_FUNDINCOME (
    PRODUCERID type of column OBJECT.OBJID,
    WHID type of column OBJECT.OBJID,
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of R_DATE,
    QUANTITY type of R_QUANTITY)
AS
declare variable dtid_fundincome type of column doctype.doctid;
declare variable docid type of column DOCUMENT.docid;
declare variable docstat type of column r_status.code;
declare variable cargoid type of column cargo.cargoid;
declare variable singularityid type of column waresgroup_singularity.id;
declare variable singularityname type of column waresgroup_singularity.name = NULL;
begin
    execute procedure wh_dtid_fundincome('0')
     returning_values :dtid_fundincome;

    if (:dtid_fundincome is NOT NULL) then
    begin
        with recursive wgf as(
            select wg.waresgrid, wg.higher, wg.singularityid
              from gwares g
                   left join waresgroup wg
                     on wg.waresgrid = g.waresgroup
             where g.waresid = :waresid
             union all
            select wg.waresgrid, wg.higher, wg.singularityid
              from wgf
                   join waresgroup wg on wg.waresgrid = wgf.higher
             where wg.singularityid is NULL
        )
        select first(1) wgf.singularityid
          from wgf
         where wgf.singularityid is NOT NULL
          into :singularityid;

        if (:singularityid is NULL) then
        begin
            select first(1) d.docid, d.status
              from document d
                   left join document_wgsingularity ds on ds.docid = d.docid
             where d.doctype = :dtid_fundincome
               and d.fromobj = :producerid
               and d.toobj = :whid
               and d.realdocdate = :productdate
               and ds.singularityid is NULL
              into :docid, :docstat;
        end
        else
        begin
            select first(1) d.docid, d.status
              from document d
                   left join document_wgsingularity ds on ds.docid = d.docid
             where d.doctype = :dtid_fundincome
               and d.fromobj = :producerid
               and d.toobj = :whid
               and d.realdocdate = :productdate
               and ds.singularityid = :singularityid
              into :docid, :docstat;
        end

        if (:docid is NULL) then
        begin                               
            if (:singularityid is NOT NULL) then
                select wsg.name
                  from waresgroup_singularity wsg
                 where wsg.id = :singularityid
                  into :singularityname;

            select k.docid
              from k_doccreate(:producerid, :whid, NULL, :dtid_fundincome,
                               current_date, :productdate,
                               NULL, NULL, :singularityname, NULL, NULL) k
              into :docid;

            if (:singularityid is NOT NULL) then
                insert into document_wgsingularity(docid, singularityid)
                values(:docid, :singularityid);
    
            update document d
               set d.status = 'c'
             where d.docid = :docid;
        end
        else if (:docstat <> 'c') then
        begin
            exception exc_wh_reserve 'Ќе верный статус документа прихода резерва!';
        end

        execute procedure k_get_cargoid(:docid, :waresid)
          returning_values :cargoid;

        if (:cargoid is NULL) then
            insert into cargo(document, waresid, amount, price)
            values(:docid, :waresid, :quantity, 0.000);
        else
            update cargo cg
               set cg.amount = cg.amount + :quantity
             where cg.cargoid = :cargoid;

    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure K_U3S_FUNDINCOME_STATUSCHG (
    DOCID type of column DOCUMENT.DOCID,
    OLDSTAT type of column R_STATUS.CODE,
    NEWSTAT type of column R_STATUS.CODE)
AS
declare variable queueid type of column r_queue.queueid;
declare variable egaisneed type of column waresgroup_singularity.egaisneed;
declare variable whid type of column OBJECT.objid;
declare variable realdocdate type of column DOCUMENT.realdocdate;
begin
    if (:newstat = 'w') then
    begin
        select wsg.egaisneed
          from document_wgsingularity ds
               left join waresgroup_singularity wsg
                 on wsg.id = ds.singularityid
         where ds.docid = :docid
          into :egaisneed;

        if (:egaisneed is NULL or :egaisneed = '1') then
        begin
         execute procedure RBS_Q_CREATETASKEXPORT('FUNDINCOME_STATUSCHG: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
          returning_values :queueid;
        end
        else
        begin
            select d.toobj, d.realdocdate
              from document d
             where d.docid = :docid
              into :whid, :realdocdate;

           insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           select :docid, cg.waresid, :realdocdate, cg.amount, :whid
             from cargo cg
            where cg.document = :docid;
       end
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDINCOME_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable objid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable productdate type of column WARESLOT.productdate;
declare variable amount type of column WH_RESERVE.amount;
begin
   select d.toobj
     from document d
    where d.docid = :docid
     into :objid;

   insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
   select :docid, ir.waresid, ir.productdate, ir.amount, :objid
     from imp_reserve ir
    where ir.docid = :docid;

   delete from imp_reserve ir
    where ir.docid = :docid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDINCOME_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable objid type of column OBJECT.objid;
begin
   select d.toobj
     from document d
    where d.docid = :docid
     into :objid;

   insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
   select :docid, ir.waresid, ir.productdate, ir.amount, :objid
     from imp_reserve ir
    where ir.docid = :docid;

   delete from imp_reserve ir
    where ir.docid = :docid;
end^

SET TERM ; ^

