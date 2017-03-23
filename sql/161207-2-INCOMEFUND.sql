

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
declare variable docsubtype type of column DOCSUBTYPE.code;
begin
    if (:newstat = 'w') then
    begin
        if (:oldstat = 'e') then
            exit;

        select d.toobj, d.realdocdate, d.docsubtype
          from document d
         where d.docid = :docid
          into :whid, :realdocdate, :docsubtype;

        select wsg.egaisneed
          from document_wgsingularity ds
               left join waresgroup_singularity wsg
                 on wsg.id = ds.singularityid
         where ds.docid = :docid
          into :egaisneed;

        if ((docsubtype is NULL or :docsubtype <> '-1C') and (:egaisneed is NULL or :egaisneed = '1')) then
        begin
         execute procedure RBS_Q_CREATETASKEXPORT('FUNDINCOME_STATUSCHG: '||:oldstat||'-->'||:newstat,:docid,NULL,NULL)
          returning_values :queueid;
        end
        else
        begin
           /*insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           select :docid, cg.waresid, :realdocdate, cg.amount, :whid
             from cargo cg
            where cg.document = :docid;*/

           insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
           with w as(
               select d.docid as docid, cg.waresid as waresid, cast(d.realdocdate as r_date) as productdate, cg.amount as amount, d.toobj as whid
                 from document d
                      left join cargo cg on cg.document = d.docid
                where d.docid = :docid
                  and cg.cargoid is NOT NULL
                union
               select rc.docid as docid, rc.waresid as waresid, rc.productdate as productdate, -rc.amount as amount, rc.objid as whid
                 from wh_reserve_changes rc
                where rc.docid = :docid
            )
           select w.docid, w.waresid, w.productdate, sum(w.amount), w.whid
             from w
            group by w.docid, w.waresid, w.productdate, w.whid
           having abs(sum(w.amount)) > 0.0001;


           update document d
              set d.status = 'e'
            where d.docid = :docid;
       end
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_INCOMEFG_BYPALLET_FUNDINCOME (
    PRODUCERID type of column OBJECT.OBJID,
    WHID type of column OBJECT.OBJID,
    WARESID type of column GWARES.WARESID,
    PRODUCTDATE type of R_DATE,
    QUANTITY type of R_QUANTITY,
    DST type of column DOCSUBTYPE.CODE = null,
    FLAGS type of WH_FLAGS = null)
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
        else if (:docstat <> 'c') then
        begin
            if (coalesce(:dst,'') = '-1C') then
                update document d
                   set d.status = 'c'
                 where d.docid = :docid;
            else if (:flags is NULL or :flags containing 'S') then
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

        suspend;
    end
end^

SET TERM ; ^



