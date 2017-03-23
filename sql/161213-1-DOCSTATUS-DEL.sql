

COMMENT ON COLUMN SCHEME_MODELSTACK.X_PDIFF IS
'Сдвиг паллета по длине относительно предыдущего, сдвиг в глубину экрана';



COMMENT ON COLUMN SCHEME_MODELSTACK.Z_PDIFF IS
'Сдвиг на экране вправо';



COMMENT ON COLUMN SCHEME_MODELSTACK.Y_PDIFF IS
'Сдвиг на экране по высоте';



COMMENT ON COLUMN SCHEME_MODELSTACK.X_PDIFF IS
'Сдвиг в глубину экрана';



SET TERM ^ ;

CREATE OR ALTER procedure RBS_LOADPLAN_GETDOCS (
    DDATE type of R_DATE)
returns (
    DOCID type of R_ID64,
    NUMBER type of DOCNUMBER,
    FROMNAME type of R_NAME,
    TONAME type of R_NAME,
    STATUS type of R_STATUS)
AS
declare variable TTID type of R_ID;
declare variable DTID type of R_ID;
begin
  select tt.tasktypeid
   from wm_tasktype tt
  where tt.code = 'LOADAUTO'
   into :ttid;

  select dt.doctid
    from doctype dt
   where dt.code = 'SALE'
    into :dtid;

  for
    select d.docid, d.number, d.status,
           (select fullname from getobjectname(d.fromobj, '03')),
           (select fullname from getobjectname(d.toobj, '03'))
      from document d
           left join wm_task t on d.docid = t.docid and t.tasktypeid = :ttid
     where d.docdate = :ddate
       and t.taskid is null
       and d.doctype = :dtid
       and d.status <> 'У'
       and coalesce(d.docsubtype, '') not in ('WP', 'AM')
     order by 4
      into :docid, :number, :status, :fromname, :toname
  do
    suspend;
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

    if (:ACTIONCODE = 'D') then
    begin
        update imp_document id
           set id.status = 'У'
         where id.docid = :docid;

        delete from imp_document id
         where id.docid = :docid;
    end
    else if (:actioncode = 'I') then
    begin
        update imp_document id
           set id.status = '1'
         where id.docid = :docid;
    
        execute procedure wh_imp_doc_transfer(:docid);

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

