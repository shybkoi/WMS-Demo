

SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_FUNDSALE_RESERVE_DO (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable OBJID type of column OBJECT.OBJID;
declare variable CLIENTID type of column OBJECT.OBJID;
declare variable WARESID type of column GWARES.WARESID;
declare variable ICAMOUNT type of column IMP_CARGO.AMOUNT;
declare variable PRODUCTDATE type of column WARESLOT.PRODUCTDATE;
declare variable IRAMOUNT type of column IMP_RESERVE.AMOUNT;
declare variable REALDOCDATE type of column DOCUMENT.REALDOCDATE;
declare variable SALEDBEG type of R_DATE;
declare variable ERRMES type of RBS_BIGVARCHAR;
declare variable EXCMES type of R_EXCEPTIONUSERMES;
declare variable ERRCNT type of R_SHORTNUMBER;
declare variable PUFACTOR type of column WARESUNIT.FACTOR;
declare variable RAMOUNT type of column IMP_RESERVE.AMOUNT;
declare variable FLAG type of R_FLAG;
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
                        select first(1) r.amountfree - coalesce(t.amount, 0), r.productdate
                          from wh_reserve r
                               left join WH_IMP_FUNDSALE_RESERVE_DO_TMP(r.waresid, r.objid, r.productdate) t on 1=1
                         where r.objid = :objid
                           and r.waresid = :waresid
                           and r.productdate > :saledbeg
--                           and r.amountfree - :pufactor > -0.0001
                           and r.amountfree - coalesce(t.amount, 0) - :pufactor > -0.0001
                         order by r.productdate ascending
                          into :iramount, :productdate;
                        
                        if (:iramount is NOT NULL and :iramount > 0.00001) then
                        begin
                            ramount = minvalue(:iramount, :icamount);
                            ramount = :ramount - mod(:ramount, :pufactor);

                            insert into wh_tmp_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
                            values(:docid, :waresid, :productdate, :ramount, :objid, :clientid);
    
                            icamount = :icamount - :ramount;
                        end
                        else
                        begin
                            flag = '1';
                        end
                    end
                    else
                    begin
                        for
                            select mod(r.amountfree - coalesce(t.amount, 0.000), :pufactor), r.productdate
                              from wh_reserve r
                                   left join WH_IMP_FUNDSALE_RESERVE_DO_TMP(r.waresid, r.objid, r.productdate) t on 1=1
                             where r.objid = :objid
                               and r.waresid = :waresid
                               and r.productdate > :saledbeg
                               and r.amountfree > 0.0000001
                               and mod(r.amountfree - coalesce(t.amount, 0.000), :pufactor) > 0.0001
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
                        flag = 1;
                    end

                    --if (:icamount < 0.0001) then
                    --  flag = 1;
                end
            end

            if (:icamount > 0.0001) then
            begin
                for
                    select r.amountfree - coalesce(t.amount, 0.000), r.productdate
                      from wh_reserve r
                           left join WH_IMP_FUNDSALE_RESERVE_DO_TMP(r.waresid, r.objid, r.productdate) t on 1=1
                     where r.objid = :objid
                       and r.waresid = :waresid
                       and r.productdate > :saledbeg
                       and r.amountfree - coalesce(t.amount, 0.000) > 0.0000001
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
         group by t.objid, t.waresid,  t.productdate, t.clientid, t.docid
        having abs(sum(t.amount)) > 0.0001;
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
    if (not exists(select *
                     from imp_document id
                          left join doctype dt on id.doctype = dt.doctid
                    where id.docid = :docid
                      and dt.code = 'FUNDSALE')) then
        exception exc_wh_wrongdoctype;

    if (:actioncode = 'D') then
    begin
        if (not exists(select *
                         from document d
                        where d.docid = :docid)) then
        begin
            delete from imp_document id
             where id.docid = :docid;

            exit;
        end

        if (exists(select *
                     from docbond db
                          left join docbondtype dbt on dbt.docbondtid = db.docbondtid
                    where db.doc1id = :docid
                      and dbt.code = 'FUNDSALE')) then
            exception exc_wh_wrongdocstat 'Сначала нужно отменить документ продажи!';
        
    end


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



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDMOVING_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I')
AS
declare variable QUEUEID type of column R_QUEUE.QUEUEID;
declare variable TOOBJ type of column IMP_DOCUMENT.TOOBJ;
begin
    if (not exists(select *
                     from imp_document id
                          left join doctype dt on id.doctype = dt.doctid
                    where id.docid = :docid
                      and dt.code = 'FUNDMOVING')) then
        exception exc_wh_wrongdoctype;

    if (:actioncode = 'I') then
    begin
        execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');
    
        update imp_document id
           set id.status = '1'
         where id.docid = :docid;
    
        execute procedure wh_imp_doc_transfer(:docid);
    
        execute procedure wh_imp_fundmoving_reserve_do(:docid);
    
        select d.queueid, d.toobj
          from imp_document d
         where d.docid = :docid
          into :queueid, :toobj;
        if (:queueid is NOT NULL) then
            execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');

        if (not exists (select *
                          from wh_reserve_objects ro
                         where ro.objid = :toobj
                           and ro.fundmoving_not_export = '1')) then
          execute procedure RBS_Q_CREATETASKEXPORT('Результат перемещения резерва',:docid,NULL,NULL)
           returning_values :queueid;
    
        delete from imp_document id
         where id.docid = :docid;
    end
    else if (:actioncode = 'D') then
    begin
        execute procedure WH_DOC_RESERVE_LVL1_CANC(:docid);

        delete from cargo cg
         where cg.document = :docid;

        update document d
           set d.status = 'У'
         where d.docid = :docid;

        delete from imp_document id
         where id.docid = :docid;
    end

end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDINCOME_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I')
AS
declare variable docstat type of column document.status;
declare variable docbondid type of column document.docid;
declare variable docnum type of column document.number;
begin
    if (not exists(select *
                     from imp_document id
                          left join doctype dt on id.doctype = dt.doctid
                    where id.docid = :docid
                      and dt.code = 'FUNDINCOME')) then
        exception exc_wh_wrongdoctype;

    select id.docbondid, id.number
      from imp_document id
     where id.docid = :docid
      into :docbondid, :docnum;

    if (:docbondid is NOT NULL) then
    begin
        update imp_document id
           set id.docid = :docbondid
         where id.docid = :docid;

        docid = :docbondid;
    end

    select d.status
      from document d
     where d.docid = :docid
      into :docstat;

    if (:actioncode = 'I') then
    begin
        if (:docstat = 'w') then
        begin
            execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid);
            execute procedure WH_IMP_CARGO_CHK(:docid);
    
            execute procedure wh_imp_fundincome_reserve_do(:docid);
    
            update document d
               set d.status = 'e', d.number = :docnum
             where d.docid = :docid;
    
            delete from imp_document id
             where id.docid = :docid;
        end
        else
        begin
            exception exc_wh_wrongdocstat;
        end
    end
    else if (:actioncode = 'D') then
    begin
        if (:docstat = 'e') then
        begin
            execute procedure WH_DOC_RESERVE_LVL1_CANC(:docid);

            update document d
               set d.status = 'w', d.number = :docnum
             where d.docid = :docid;
    
            delete from imp_document id
             where id.docid = :docid;
        end
        else
        begin
            exception exc_wh_wrongdocstat;
        end
    end
    else
    begin
        exception exc_wh_wrongdocstat 'wrong ACTIONCODE';
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable queueid type of column R_QUEUE.queueid;
declare variable waresid type of column GWARES.WARESID;
declare variable wcode type of column GWARES.code;
declare variable docid_fundsale type of column DOCUMENT.docid;
begin
    if (not exists(select *
                     from imp_document id
                          left join doctype dt on id.doctype = dt.doctid
                    where id.docid = :docid
                      and dt.code = 'SALE')) then
        exception exc_wh_wrongdoctype;

    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '=');

    select d.queueid, d.docbondid
      from imp_document d
     where d.docid = :docid
      into :queueid, :docid_fundsale;

    select first(1) u.waresid
      from (select ir.waresid as waresid, ir.productdate as productdate, ir.amount as amount
              from imp_reserve ir
             where ir.docid = :docid
             union all
            select rcc.waresid as waresid, rcc.productdate as productdate, -rcc.amount  as amount
              from wh_reserve_client_changes rcc
             where rcc.docid = :docid_fundsale) u
     group by u.waresid, u.productdate
    having abs(sum(u.amount)) > 0.0001
      into :waresid;

    if (:waresid is NOT NULL) then
    begin
        select g.code
          from gwares g
         where g.waresid = :waresid
          into :wcode;

        exception exc_wh_wrongamount 'Не верные данные по резерву у товара с кодом ' || :wcode;
    end

    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    update or insert into docbond (DOCBONDTID, DOC1ID, DOC2ID)
    values ( (select dbtid from wh_dbtid_fundsale), :docid_fundsale, :docid)
    matching (DOCBONDTID, DOC1ID, DOC2ID);

    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^

