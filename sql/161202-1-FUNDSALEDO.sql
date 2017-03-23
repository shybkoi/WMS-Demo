

SET TERM ^ ;

CREATE OR ALTER procedure K_SUPPORT_ADD_MAN (
    FIO varchar(90),
    DOLGNNAME varchar(80),
    ZONENAME varchar(80))
returns (
    MANID integer)
AS
declare variable IO varchar(90);
declare variable F1 integer;
declare variable LASTNAME varchar(30);
declare variable SESSIONID integer;
declare variable NAME varchar(30);
declare variable FATHERNAME varchar(30);
declare variable DOLGNID integer;
declare variable DEPID type of R_ID;
declare variable KATID type of R_ID;
declare variable ZONE integer;
declare variable LOGOFFBARCODE varchar(25);
BEGIN
    --Процедура создания пользователя
    --Если пользователь заведён (соответствие по ФИО), обязательно обновляются его атрибуты (должность и зона)
    --Если DOLGNNAME пусто, создаётся умалчиваемая должность как CONFIG.DEFDOLGNNAMEPREFIX || GEN_ID(GEN_K_DEFDOLGNNAMESUFFIX,1)
    --Если ZONENAME пусто, зона устанавливается как CONFIG.DEFZONE

    fio=c(trim(fio))||' ';
    f1 = strpos(' ' ,fio);

    lastname=substr(fio,1,f1-1) ;
    io=c(trim(substr(fio,f1+1,16383-f1)))||' ';
    f1=strpos(' ',io);

    name=substr(io,1,f1-1);
    FATHERNAME=longtrim(substr(io,f1+1,16383-f1));

    if (:LASTNAME='') then LASTNAME =' ';
    if (:name='') then name = ' ';
    if (:fathername='') then fathername = ' ';

    select first 1 MANID
    from man
    where c(Trim(Trim(RLOWER(LASTNAME))||' '||Trim(RLOWER(NAME))||' '||Trim(RLOWER(FATHERNAME))))=c(Trim(RLOWER(:fio)))
      into :ManID;
    if (MANID is null) then
    begin
        ManID = GEN_ID(G_OBJID,1);
        INSERT INTO MAN (manid, LASTNAME, NAME, FATHERNAME, STATUS, SESSIONID)
        VALUES (:manid, :LASTNAME, :NAME, :FATHERNAME, '1', 1);
    end

    /*if (DOLGNNAME is not null) then
    begin
      select first 1 DolgnID
      from DOLGN D
      where D.NAME = :DOLGNNAME
        into :DolgnID;

      if (DolgnID is null) then
      begin
        DolgnID = GEN_ID(G_DolgnID,1);
        INSERT INTO DOLGN (DOLGNID, DEPID, KATID, NAME, noapply, SESSIONID)
        VALUES (:DolgnID, 2, 1, :DOLGNNAME, 0, 1);
      end
    end
    else
    begin
      DolgnID = GEN_ID(G_DolgnID,1);
      select first 1 c.DEFDOLGNNAMEPREFIX || GEN_ID(GEN_K_DEFDOLGNNAMESUFFIX,1), c.DEFDEPDOLGN, c.DEFKATDOLGN
      from CONFIG c
        into :DOLGNNAME, :DEPID, :KATID;
      INSERT INTO DOLGN (DOLGNID, DEPID, KATID, NAME, noapply, SESSIONID)
      VALUES (:DolgnID, :DEPID, :KATID, :DOLGNNAME, 0, 1);
    end */

    if (ZONENAME is not null) then
      SELECT first 1 co.zoneid FROM sitezone co
      WHERE co.name CONTAINING :zonename
      INTO :ZONE;
    else
      select first 1 c.DEFZONE
      from CONFIG c
      INTO :ZONE;

    UPDATE or insert into sitezone_employees ( ZONEID, EMPLOYEEID)
    values ( :zone, :manid )
    matching(ZONEID, EMPLOYEEID);

    UPDATE OR INSERT INTO EMPLOYEE (EMPLOYEEid, DOLGNID, nomer, BASEWORK, PROFUNION, WORKST, CURRENTZONE, SESSIONID)
    VALUES (:manid, :DolgnID, :manid, '1', '0', '0', :ZONE, 1)
    MATCHING (EMPLOYEEid);


    --SessionID = GEN_ID(G_WM_SESSIONID, 1);
    --INSERT INTO WM_SESSION (SessionID, EquipmentID, ObjID)
    --VALUES (:SessionID, 4010, :manid);

    execute procedure rbs_man_open_commonsession(:manid)
    returning_values :sessionid;

    /*
    select logoffbarcode
      from wm_config
      into :LogOffBarCode;

    select sessionid
      from wm_getsession (:LogOffBarCode,'1111')
      into :sessionid;

    select sessionid
      from wm_getsession ('U'||CAST(:manid as varchar(10)),'1111')
      into :sessionid;
    */

    suspend;
END^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYPALLET_FUNDINCOME (
    PRODUCERID type of column OBJECT.OBJID,
    WHID type of column OBJECT.OBJID,
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of R_DATE,
    QUANTITY type of R_QUANTITY,
    DST type of column DOCSUBTYPE.CODE = null,
    FLAGS type of WH_FLAGS = NULL
)
returns (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable dtid_fundincome type of column doctype.doctid;
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
               and (:dst is NULL or d.docsubtype = :dst)
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
               and (:dst is NULL or d.docsubtype = :dst)
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
                               NULL, NULL, :singularityname, NULL, :dst) k
              into :docid;

            if (:singularityid is NOT NULL) then
                insert into document_wgsingularity(docid, singularityid)
                values(:docid, :singularityid);
    
            update document d
               set d.status = 'c'
             where d.docid = :docid;
        end
        else if (:docstat <> 'c' and (:flags is NULL or :flags containing 'S') ) then
        begin
            exception exc_wh_reserve 'Не верный статус документа прихода резерва!';
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

        suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDSALE_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable objid type of column OBJECT.objid;
declare variable clientid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable icamount type of column IMP_CARGO.amount;
declare variable productdate type of column WARESLOT.productdate;
declare variable iramount type of column IMP_RESERVE.amount;
declare variable realdocdate type of column DOCUMENT.realdocdate;
declare variable saledbeg type of R_DATE;
declare variable errmes type of rbs_bigvarchar;
declare variable excmes type of r_exceptionusermes;
declare variable errcnt type of r_shortnumber;
declare variable pufactor type of column WARESUNIT.factor;
declare variable flag type of R_FLAG;
begin
   select gor.objid, d.toobj, d.realdocdate
     from imp_document d
          left join wh_get_reserveobj(coalesce(d.throughobj, d.fromobj)) gor on 1=1
    where d.docid = :docid
     into :objid, :clientid, :realdocdate;

   for
    select ic.waresid, ic.amount
      from imp_cargo ic
     where ic.document = :docid
       and ic.amount > 0.000001
      into :waresid, :icamount
   do
   begin
        for
            select ir.productdate, ir.amount
              from imp_reserve ir
             where ir.docid = :docid
               and ir.waresid = :waresid
              into :productdate, :iramount
        do
        if (exists(select *
                     from wh_reserve r
                    where r.objid = :objid
                      and r.waresid = :waresid
                      and r.productdate = :productdate
                      and r.amountfree - :iramount > -0.0001)) then
        begin
           insert into wh_tmp_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
           values(:docid, :waresid, :productdate, :iramount, :objid, :clientid);
    
           icamount = :icamount - :iramount;
        end
        else
        begin
           icamount = 0.000;
           break;
        end

        if (:icamount > 0.0000001) then
        begin
            pufactor = NULL;
            select w.W_PUFACTOR
              from wh_wares_getpalletunit(:waresid) w
              into :pufactor;
            if (:pufactor < 0.0001) then
                pufactor = NULL;

            select w.dbeg
              from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
              into :saledbeg;
            
            if (:pufactor is NOT NULL) then
            begin
                flag = NULL;
                while (:flag is NULL) do
                begin
                    if (:icamount - :pufactor > -0.0001) then
                    begin
                        iramount = NULL;
                        select first(1) r.amountfree, r.productdate
                          from wh_reserve r
                         where r.objid = :objid
                           and r.waresid = :waresid
                           and r.productdate > :saledbeg
                           and r.amountfree - :pufactor > -0.0001
                         order by r.productdate ascending
                          into :iramount, :productdate;
                        
                        if (:iramount is NOT NULL and :iramount > 0.00001) then
                        begin
                            insert into wh_tmp_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
                            values(:docid, :waresid, :productdate, :pufactor, :objid, :clientid);
    
                            icamount = :icamount - :pufactor;
                        end
                        else
                        begin
                            flag = '1';
                        end
                    end
                    else
                    begin
                        for
                            select mod(r.amountfree, :pufactor), r.productdate
                              from wh_reserve r
                             where r.objid = :objid
                               and r.waresid = :waresid
                               and r.productdate > :saledbeg
                               and r.amountfree > 0.0000001
                               and mod(r.amountfree, :pufactor) > 0.0001
                             order by r.productdate ascending
                              into :iramount, :productdate
                        do
                        begin
                           if (:iramount - :icamount > 0.0000001) then
                                iramount = :icamount;
                
                           insert into wh_tmp_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
                           values(:docid, :waresid, :productdate, :iramount, :objid, :clientid);
                    
                           icamount = :icamount - :iramount;

                           if (:icamount < 0.0000001) then
                            break;
                        end
                    end

                    if (:icamount < 0.0001) then
                        flag = 1;
                end
            end

            if (:icamount > 0.0001) then
            begin
                for
                    select r.amountfree, r.productdate
                      from wh_reserve r
                     where r.objid = :objid
                       and r.waresid = :waresid
                       and r.productdate > :saledbeg
                       and r.amountfree > 0.0000001
                     order by r.productdate ascending
                      into :iramount, :productdate
                do
                begin
                   if (:iramount - :icamount > 0.0000001) then
                        iramount = :icamount;
        
                   insert into wh_tmp_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
                   values(:docid, :waresid, :productdate, :iramount, :objid, :clientid);
            
                   icamount = :icamount - :iramount;
        
                   if (:icamount < 0.0000001) then
                    break;
                end
            end
        end
   end

   with chg1 as (
       select w.waresid as waresid, w.amount as amount
         from wh_tmp_reserve_client_changes w
        where w.docid = :docid
        union all
       select ic.waresid as waresid, -ic.amount as amount
         from imp_cargo ic
        where ic.document = :docid
   ),
   chg2 as (
    select chg1.waresid as waresid, sum(chg1.amount) as amount
      from chg1
     group by chg1.waresid
    having abs(sum(chg1.amount)) > 0.0001
   )
   select list(distinct g.externalcode || '->' || g.code), count(distinct g.waresid)
     from chg2
          left join gwares g on g.waresid = chg2.waresid
     into :errmes, :errcnt;

   if (:errcnt is NOT NULL and :errcnt > 0) then
   begin
        errmes = 'Невозможно зарезервировать в нужном количестве товары: '||:errmes;
        execute procedure WH_TEXT_TO_EXCMES(:errmes)
         returning_values :excmes;
        exception exc_wh_wrongamount :excmes;
   end
   else
   begin
        insert into wh_reserve_client_changes ( OBJID, WARESID, PRODUCTDATE, CLIENTID, AMOUNT, DOCID)
        select t.objid, t.waresid,  t.productdate, t.clientid, t.amount, t.docid
          from wh_tmp_reserve_client_changes t;
   end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDSALE_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable objid type of column OBJECT.objid;
declare variable clientid type of column OBJECT.objid;
declare variable waresid type of column GWARES.waresid;
declare variable icamount type of column IMP_CARGO.amount;
declare variable productdate type of column WARESLOT.productdate;
declare variable iramount type of column IMP_RESERVE.amount;
declare variable realdocdate type of column DOCUMENT.realdocdate;
declare variable saledbeg type of R_DATE;
declare variable errmes type of rbs_bigvarchar;
declare variable excmes type of r_exceptionusermes;
declare variable errcnt type of r_shortnumber;
declare variable pufactor type of column WARESUNIT.factor;
declare variable flag type of R_FLAG;
begin
   select gor.objid, d.toobj, d.realdocdate
     from imp_document d
          left join wh_get_reserveobj(coalesce(d.throughobj, d.fromobj)) gor on 1=1
    where d.docid = :docid
     into :objid, :clientid, :realdocdate;

   for
    select ic.waresid, ic.amount
      from imp_cargo ic
     where ic.document = :docid
       and ic.amount > 0.000001
      into :waresid, :icamount
   do
   begin
        for
            select ir.productdate, ir.amount
              from imp_reserve ir
             where ir.docid = :docid
               and ir.waresid = :waresid
              into :productdate, :iramount
        do
        if (exists(select *
                     from wh_reserve r
                    where r.objid = :objid
                      and r.waresid = :waresid
                      and r.productdate = :productdate
                      and r.amountfree - :iramount > -0.0001)) then
        begin
           insert into wh_tmp_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
           values(:docid, :waresid, :productdate, :iramount, :objid, :clientid);
    
           icamount = :icamount - :iramount;
        end
        else
        begin
           icamount = 0.000;
           break;
        end

        if (:icamount > 0.0000001) then
        begin
            pufactor = NULL;
            select w.W_PUFACTOR
              from wh_wares_getpalletunit(:waresid) w
              into :pufactor;
            if (:pufactor < 0.0001) then
                pufactor = NULL;

            select w.dbeg
              from wh_wares_saledbeg(:waresid, :clientid, :realdocdate) w
              into :saledbeg;
            
            if (:pufactor is NOT NULL) then
            begin
                flag = NULL;
                while (:flag is NULL) do
                begin
                    if (:icamount - :pufactor > -0.0001) then
                    begin
                        iramount = NULL;
                        select first(1) r.amountfree, r.productdate
                          from wh_reserve r
                         where r.objid = :objid
                           and r.waresid = :waresid
                           and r.productdate > :saledbeg
                           and r.amountfree - :pufactor > -0.0001
                         order by r.productdate ascending
                          into :iramount, :productdate;
                        
                        if (:iramount is NOT NULL and :iramount > 0.00001) then
                        begin
                            insert into wh_tmp_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
                            values(:docid, :waresid, :productdate, :pufactor, :objid, :clientid);
    
                            icamount = :icamount - :pufactor;
                        end
                        else
                        begin
                            flag = '1';
                        end
                    end
                    else
                    begin
                        for
                            select mod(r.amountfree, :pufactor), r.productdate
                              from wh_reserve r
                             where r.objid = :objid
                               and r.waresid = :waresid
                               and r.productdate > :saledbeg
                               and r.amountfree > 0.0000001
                               and mod(r.amountfree, :pufactor) > 0.0001
                             order by r.productdate ascending
                              into :iramount, :productdate
                        do
                        begin
                           if (:iramount - :icamount > 0.0000001) then
                                iramount = :icamount;
                
                           insert into wh_tmp_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
                           values(:docid, :waresid, :productdate, :iramount, :objid, :clientid);
                    
                           icamount = :icamount - :iramount;

                           if (:icamount < 0.0000001) then
                            break;
                        end
                    end

                    if (:icamount < 0.0001) then
                        flag = 1;
                end
            end

            if (:icamount > 0.0001) then
            begin
                for
                    select r.amountfree, r.productdate
                      from wh_reserve r
                     where r.objid = :objid
                       and r.waresid = :waresid
                       and r.productdate > :saledbeg
                       and r.amountfree > 0.0000001
                     order by r.productdate ascending
                      into :iramount, :productdate
                do
                begin
                   if (:iramount - :icamount > 0.0000001) then
                        iramount = :icamount;
        
                   insert into wh_tmp_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
                   values(:docid, :waresid, :productdate, :iramount, :objid, :clientid);
            
                   icamount = :icamount - :iramount;
        
                   if (:icamount < 0.0000001) then
                    break;
                end
            end
        end
   end

   with chg1 as (
       select w.waresid as waresid, w.amount as amount
         from wh_tmp_reserve_client_changes w
        where w.docid = :docid
        union all
       select ic.waresid as waresid, -ic.amount as amount
         from imp_cargo ic
        where ic.document = :docid
   ),
   chg2 as (
    select chg1.waresid as waresid, sum(chg1.amount) as amount
      from chg1
     group by chg1.waresid
    having abs(sum(chg1.amount)) > 0.0001
   )
   select list(distinct g.externalcode || '->' || g.code), count(distinct g.waresid)
     from chg2
          left join gwares g on g.waresid = chg2.waresid
     into :errmes, :errcnt;

   if (:errcnt is NOT NULL and :errcnt > 0) then
   begin
        errmes = 'Невозможно зарезервировать в нужном количестве товары: '||:errmes;
        execute procedure WH_TEXT_TO_EXCMES(:errmes)
         returning_values :excmes;
        exception exc_wh_wrongamount :excmes;
   end
   else
   begin
        insert into wh_reserve_client_changes ( OBJID, WARESID, PRODUCTDATE, CLIENTID, AMOUNT, DOCID)
        select t.objid, t.waresid,  t.productdate, t.clientid, sum(t.amount), t.docid
          from wh_tmp_reserve_client_changes t
         group by t.objid, t.waresid,  t.productdate, t.clientid, t.docid;
   end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDSALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I')
AS
declare variable queueid type of column r_queue.queueid;
begin
    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');
    execute procedure WH_IMP_FUNDSALE_RESERVE_CANC(:docid);

    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    if (:ACTIONCODE = 'D') then
    begin
        delete from imp_cargo ic
         where ic.document = :docid;

        delete from imp_document id
         where id.docid = :docid;
    end
    else if (:actioncode = 'I') then
    begin
        execute procedure WH_IMP_FUNDSALE_RESERVE_DO(:docid);

        select d.queueid
          from imp_document d
         where d.docid = :docid
          into :queueid;
        if (:queueid is NOT NULL) then
            execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');

        execute procedure RBS_Q_CREATETASKEXPORT('Результат резервирования продажи',:docid,NULL,NULL)
          returning_values :queueid;
    
        delete from imp_document id
         where id.docid = :docid;
    end
    else
    begin
        exception exc_wh_wrongdocstat 'wrong ACTIONCODE';
    end
end^

SET TERM ; ^

