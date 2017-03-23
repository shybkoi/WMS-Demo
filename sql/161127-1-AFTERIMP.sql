

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
        if (:oldstat = 'e') then
            exit;

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

           update document d
              set d.status = 'e'
            where d.docid = :docid;
       end
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

