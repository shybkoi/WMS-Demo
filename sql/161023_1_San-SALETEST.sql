

SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDINCOME_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
 /*$$IBE$$ declare variable docstat type of column document.status;
declare variable docbondid type of column document.docid;
declare variable docnum type of column document.number; $$IBE$$*/ 
begin /*$$IBE$$ 
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
 $$IBE$$*/ EXIT;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDMOVING_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
 /*$$IBE$$ declare variable queueid type of column R_QUEUE.queueid; $$IBE$$*/ 
begin /*$$IBE$$ 
    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');

    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    execute procedure wh_imp_fundmoving_reserve_do(:docid);

    select d.queueid
      from imp_document d
     where d.docid = :docid
      into :queueid;
    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');

 $$IBE$$*/ /*    delete from imp_document id
     where id.docid = :docid;*/
EXIT;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDSALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID,
    ACTIONCODE type of R_FLAG = 'I')
AS
 /*$$IBE$$ declare variable queueid type of column r_queue.queueid; $$IBE$$*/ 
begin /*$$IBE$$ 
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
    end
    else
    begin
        execute procedure WH_IMP_FUNDSALE_RESERVE_DO(:docid);
    end

    select d.queueid
      from imp_document d
     where d.docid = :docid
      into :queueid;
    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');
        
    execute procedure RBS_Q_CREATETASKEXPORT('Результат резервирование продажи',:docid,NULL,NULL)
      returning_values :queueid;

    delete from imp_document id
     where id.docid = :docid;
 $$IBE$$*/ EXIT;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_IMP_CARGO_CHK (
    DOCID type of column DOCUMENT.DOCID,
    DOCID_IMP type of column DOCUMENT.DOCID = NULL
)
AS
declare variable wid type of column GWARES.waresid;
declare variable wname type of column GWARES.name;
begin
    if (:docid_imp is NULL) then
        docid_imp = :docid;

     select first(1) w.waresid
      from (select ic.waresid as waresid, ic.amount as q
              from imp_cargo ic
             where ic.document = :docid_imp
             union all
            select cg.waresid as waresid, -cg.amount as q
              from cargo cg
             where cg.document = :docid) w
      group by w.waresid
      having abs(sum(w.q)) > 0.00001
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
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable docstat type of column document.status;
declare variable docbondid type of column document.docid;
declare variable docnum type of column document.number;
begin
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
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDMOVING_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable queueid type of column R_QUEUE.queueid;
begin
    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');

    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    execute procedure wh_imp_fundmoving_reserve_do(:docid);

    select d.queueid
      from imp_document d
     where d.docid = :docid
      into :queueid;
    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');

    delete from imp_document id
     where id.docid = :docid;
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
    end
    else
    begin
        execute procedure WH_IMP_FUNDSALE_RESERVE_DO(:docid);
    end

    select d.queueid
      from imp_document d
     where d.docid = :docid
      into :queueid;
    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');
        
    execute procedure RBS_Q_CREATETASKEXPORT('Результат резервирование продажи',:docid,NULL,NULL)
      returning_values :queueid;

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_FUNDMOVING_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable queueid type of column R_QUEUE.queueid;
begin
    execute procedure WH_IMP_CARGO_CHK_RESERVE(:docid, '>=');

    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    execute procedure wh_imp_fundmoving_reserve_do(:docid);

    select d.queueid
      from imp_document d
     where d.docid = :docid
      into :queueid;
    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');

    execute procedure RBS_Q_CREATETASKEXPORT('Результат перемещения резерва',:docid,NULL,NULL)
      returning_values :queueid;

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure EXP_DOC_FUNDSALE_WARESRESERVE (
    DOCID type of column DOCUMENT.DOCID,
    WARESID type of column GWARES.WARESID)
returns (
    PRDATE type of column WH_RESERVE_CHANGES.PRODUCTDATE,
    AMOUNT type of column WH_RESERVE_CHANGES.AMOUNT)
AS
begin
    for
        select rcc.productdate, sum(rcc.amount)
          from wh_reserve_client_changes rcc
         where rcc.docid = :docid
           and rcc.waresid = :waresid
         group by rcc.productdate
          into :prdate, :amount
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure RBS_Q_EXPORTXML_CARGO_INGP_U3S (
    IDS R_ID64)
returns (
    CODE R_CODE,
    NAME R_FULLNAME,
    AMOUNT R_QUANTITY,
    UNITCODE R_CODE,
    UNITNAME R_NAME,
    PRICE R_MONEY,
    DOCSUM R_MONEY,
    PRICEWNDS R_MONEY,
    DOCSUMWNDS R_MONEY,
    EXTERNALCODETAX R_CODE,
    EXTERNALCODE R_CODE25,
    EXTERNALWARESID R_CUSTOMDATA,
    SECONDARYNAME R_CUSTOMDATA,
    PRODUCT_STR RBS_BIGVARCHAR,
    SECONDARYID R_CUSTOMDATA,
    UEXTERNALID R_CUSTOMDATA)
AS
declare variable WARESID R_ID;
declare variable OBJID R_ID;
declare variable FACTOR R_QUANTITY;
declare variable UWEIGHT R_QUANTITY;
declare variable WARESTYPE R_CHOICE;
declare variable PRODUCT_STR_TMP RBS_BIGVARCHAR;
declare variable DOCTYPECODE R_CODE;
BEGIN
  FOR
     SELECT g.code, g.externalcode, g.name, SUM(COALESCE(cg.amount, 0)), u.shortname, u.fullname, COALESCE(cg.price, 0), SUM(COALESCE(cg.docsum, 0)),
            g.waresid, COALESCE(t.externalcode, ''), cg.objid,
            g.externalid, COALESCE(g.secondaryname, ''), COALESCE(g.secondaryid, ''),
            COALESCE(u.externalid, ''),
            dt.code
       FROM r_listwords(:ids, ',', 0) r
            LEFT JOIN cargo cg ON CAST(r.word AS R_ID64)=cg.document
            LEFT JOIN gwares g ON cg.waresid = g.waresid
            LEFT JOIN waresunit wu ON g.mainunitid = wu.waresunitid
            LEFT JOIN unit u ON wu.unitid =u.unitid
            LEFT JOIN rbs_gwares_gettax_bydate(g.waresid, cg.docdate) t ON 1=1
            LEFT JOIN doctype dt ON cg.doctype = dt.doctid
      --WHERE ABS(cg.amount)>0.000001
       GROUP BY g.code, g.externalcode, g.name, u.shortname, u.fullname, COALESCE(cg.price, 0),
            g.waresid, t.externalcode, cg.objid,
            g.externalid, g.secondaryname, g.secondaryid,
            u.externalid, dt.code
       INTO :code, :externalcode, :name, :amount, :unitcode, :unitname, :pricewnds, :docsumwnds,
            :waresid, :externalcodetax, :objid,
            :externalwaresid, :secondaryname, :secondaryid,
            :uexternalid, :doctypecode DO
       BEGIN
         SELECT x.text
           FROM rbs_r_xmlconvertstring(:name, NULL) x
           INTO :name;
         SELECT x.text
           FROM rbs_r_xmlconvertstring(:secondaryname, NULL) x
           INTO :secondaryname;
         secondaryname = COALESCE(:secondaryname, '');
         SELECT n.ndsfree FROM rbs_calc_waresnds(:waresid, :pricewnds, 1) n INTO :price;
         docsum = :price * :amount;
         /* собираем информацию с разбивкой по линиям */
         IF (:doctypecode = 'FUNDINCOME') THEN
           BEGIN
             product_str = '';
             FOR
               SELECT '                           <production quantity="'||p.q||'" date="'||datetostr(p.prdate,'%d.%m.%Y %H:%M:%S')||'" ttn_number="" ttn_date=""/>'
                 FROM Q_EXP_CARGO_FUNDINCOME_PRDATE(:ids, :waresid) p
                 INTO :product_str_tmp DO
               BEGIN
                 IF (product_str_tmp IS NOT NULL) THEN
                   BEGIN
                     IF (:product_str <> '') THEN product_str = product_str || '
                     ';
                     product_str = product_str || product_str_tmp;
                   END
               END
           END
         IF (:doctypecode = 'FUNDSALE') THEN
           BEGIN
             product_str = '';
             FOR
               SELECT '                           <production quantity="'||p.amount||'" date="'||datetostr(p.prdate,'%d.%m.%Y %H:%M:%S')||'" ttn_number="" ttn_date=""/>'
                 FROM EXP_DOC_FUNDSALE_WARESRESERVE(:ids, :waresid) p
                 INTO :product_str_tmp DO
               BEGIN
                 IF (product_str_tmp IS NOT NULL) THEN
                   BEGIN
                     IF (:product_str <> '') THEN product_str = product_str || '
                     ';
                     product_str = product_str || product_str_tmp;
                   END
               END
           END
         SUSPEND;
       END
END^

SET TERM ; ^



DROP PROCEDURE EXP_DOC_FUNSALE_WARESRESERVE;



SET TERM ^ ;

create or alter procedure WH_SALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable queueid type of column R_QUEUE.queueid;
declare variable waresid type of column GWARES.WARESID;
declare variable wcode type of column GWARES.code;
declare variable docid_fundsale type of column DOCUMENT.docid;
begin
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

        exception exc_wh_wrongamount 'Не верные данные по резерву у товара с кодом' || :wcode;
    end


    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    execute procedure wh_imp_fundmoving_reserve_do(:docid);

    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');

    execute procedure RBS_Q_CREATETASKEXPORT('Результат перемещения резерва',:docid,NULL,NULL)
      returning_values :queueid;

    delete from imp_document id
     where id.docid = :docid;
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

        exception exc_wh_wrongamount 'Не верные данные по резерву у товара с кодом' || :wcode;
    end


    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');

    execute procedure RBS_Q_CREATETASKEXPORT('Результат перемещения резерва',:docid,NULL,NULL)
      returning_values :queueid;

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^




SET TERM ^ ;

create procedure UV_SELECT_TASKP_SITESET (
    taskid type of column wm_task.taskid
)
as
declare variable clientid type of r_id;
declare variable docdate type of r_date;
declare variable wdval type of r_customdata;
declare variable dbeg type of r_date;
declare variable waresid type of r_id;
declare variable taskwaresid type of r_id;
declare variable siteid type of r_id;
declare variable whid type of r_id;
declare variable palcurcnt type of r_id;
declare variable palblkcnt type of r_id;
declare variable ttid_select type of r_id;
declare variable tmid_select_p type of r_id;
declare variable pfpriority type of r_shortnumber;
declare variable flbreak type of r_shortnumber;
declare variable docid type of column DOCUMENT.DOCID;
declare variable sitesegmentid type of column uv_site_segment.siteid;
declare variable defsitesegmentid type of column uv_site_segment.siteid;
begin
    select tw.taskwaresid, tw.waresid, tw.siteid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.status <> '2'
      into :taskwaresid, :waresid, :siteid;

    if (:siteid is not NULL) then exit;

    select d.fromobj,d.toobj,d.docdate,d.docid
      from wm_task t
           left join document d on d.docid=t.docid
     where t.taskid = :taskid
      into :whid,:clientid,:docdate,:docid;

    dbeg = '01.01.2000';
    select val
      from k_get_wares_data_obj_val(NULL,'SALEPERIOD',:waresid, :clientid, :docdate)
      into :wdval;

    if (:wdval is NOT NULL) then
        dbeg = :docdate - cast(:wdval as integer);


    execute procedure wh_ttid_select
     returning_values :ttid_select;

    select w.tmid
      from wh_tmid_get(:ttid_select, 'P') w
      into :tmid_select_p;

    select u.defsitesegmentid, u.sitesegmentid
      from uv_sitesegment_bydoc(:docid, :whid) u
      into :defsitesegmentid, :sitesegmentid;
    flbreak = 0;
    for
        select distinct wh.pfpriority
          from WH_CLIENT_LISTPALLETFEATURES(:clientid) wh
         where wh.pfpriority is NOT NULL and wh.pfpriority > 0
         order by wh.pfpriority ascending
          into :pfpriority
    do
    begin
        for
            select ss.siteid,ss.palcurcnt
              from site_stack ss
             where ss.waresid = :waresid
               and ss.productdate > :dbeg
               and ss.siteid is NOT NULL
               and exists(select *
                            from uv_sitesegment_bysite(ss.siteid) ssg
                           where coalesce(ssg.SSID, :defsitesegmentid) = :sitesegmentid)
               and exists(select *
                            from pallet p
                                 left join WH_CLIENT_LISTPALLETFEATURES(:clientid) pfc
                                   on pfc.pfid = p.featureid
                           where p.siteid = ss.siteid
                             and p.objid = :whid
                             and pfc.PFPRIORITY = :pfpriority)
             order by ss.productdate ascending,
                   iif(ss.palmaxcnt=ss.palcurcnt,1,0) ascending,
                   ss.palcurcnt ascending,
                   ss.dt ascending nulls first
              into :siteid, :palcurcnt
        do
        begin
            palblkcnt = NULL;
            select count(tw.taskwaresid)
              from wm_task_wares tw
                   left join wm_task t on t.taskid = tw.taskid
             where tw.tasktypeid = :ttid_select
               and tw.status in ('0','1')
               and tw.siteid = :siteid
               and tw.waresid = :waresid
               and t.status <> '2'
               and t.taskmethodid = :tmid_select_p
               and t.taskid <> :taskid
              into :palblkcnt;
            if (:palblkcnt is not NULL) then
                palcurcnt = :palcurcnt - :palblkcnt;

            if (:palcurcnt > 0) then
            begin
                flbreak = 1;
                break;
            end
        end

        if (:flbreak = 1) then
            break;
    end

    if (:siteid is NULL) then
    begin
        for
            select ss.siteid,ss.palcurcnt
              from site_stack ss
             where ss.waresid = :waresid
               and ss.productdate > :dbeg
               and ss.siteid is NOT NULL
               and exists(select *
                            from uv_sitesegment_bysite(ss.siteid) ssg
                           where coalesce(ssg.SSID, :defsitesegmentid) = :sitesegmentid)
               and exists(select *
                            from pallet p
                           where p.siteid = ss.siteid
                             and p.objid = :whid
                             and p.featureid is NULL)
             order by ss.productdate ascending,
                   iif(ss.palmaxcnt=ss.palcurcnt,1,0) ascending,
                   ss.palcurcnt ascending,
                   ss.dt ascending nulls first
              into :siteid, :palcurcnt
        do
        begin
            palblkcnt = NULL;
            select count(tw.taskwaresid)
              from wm_task_wares tw
                   left join wm_task t on t.taskid = tw.taskid
             where tw.tasktypeid = :ttid_select
               and tw.status in ('0','1')
               and tw.siteid = :siteid
               and tw.waresid = :waresid
               and t.status <> '2'
               and t.taskmethodid = :tmid_select_p
               and t.taskid <> :taskid
              into :palblkcnt;
            if (:palblkcnt is not NULL) then
                palcurcnt = :palcurcnt - :palblkcnt;

            if (:palcurcnt > 0) then
                break;
        end
    end

    /*for
        select distinct ss.siteid,ss.palcurcnt
          from wareslot wl
               left join wareslotitem wli
                    left join pallet p
                         left join site_stack ss on ss.siteid = p.siteid
                      on p.palletid = wli.palletid
                 on wli.wlotid=wl.wlotid
         where wl.waresid = :waresid
           and wl.productdate > :dbeg
           and wl.status = '1'
           and wl.objid = :whid
           and ss.siteid is NOT NULL
         order by wl.productdate ascending,
               iif(ss.palmaxcnt=ss.palcurcnt,1,0) ascending,
               ss.palcurcnt ascending,
               ss.dt ascending nulls first
--           and ss.palcurcnt > coalesce(ss.palblkcnt,0)
          into :siteid, :palcurcnt
    do
    begin
        palblkcnt = NULL;
        select count(tw.taskwaresid)
          from wm_task_wares tw
               left join wm_task t on t.taskid = tw.taskid
         where tw.tasktypeid = :ttid_select
           and tw.status in ('0','1')
           and tw.siteid = :siteid
           and tw.waresid = :waresid
           and t.status <> '2'
           and t.taskmethodid = :tmid_select_p
           and t.taskid <> :taskid
          into :palblkcnt;
        if (:palblkcnt is not NULL) then
            palcurcnt = :palcurcnt - :palblkcnt;

        if (:palcurcnt > 0) then
            break;
    end*/

    update site_stack ss
       set ss.palblkcnt = coalesce(ss.palblkcnt,0) + 1
     where ss.siteid = :siteid;

    update wm_task_wares tw
       set tw.siteid = :siteid
     where tw.taskwaresid = :taskwaresid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_P_JOINSITE (
    TASKID R_ID)
AS
declare variable objcode type of r_code3;
begin
    select wm.objcode
      from wm_config wm
      into :objcode;

    if (:objcode = 'UV') then
    begin
        execute procedure UV_SELECT_TASKP_SITESET(:taskid);
    end
end^

SET TERM ; ^



CREATE EXCEPTION EXC_WH_DOCBONDTYPE_NOTFOUND 'Связь документов не найдена, код: ';



ALTER EXCEPTION EXC_WH_DOCBONDTYPE_NOTFOUND 'Связь документов не найдена';



SET TERM ^ ;

create procedure WH_DBTID_FUNDSALE
returns (
    DBTID type of column docbondtype.docbondtid
)
as
begin
    select dbt.docbondtid
      from docbondtype dbt
     where dbt.code = 'FUNDSALE'
      into :dbtid;

    if (:dbtid is NULL) then
        exception EXC_WH_DOCBONDTYPE_NOTFOUND;

    suspend;
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

        exception exc_wh_wrongamount 'Не верные данные по резерву у товара с кодом' || :wcode;
    end

    update imp_document id
       set id.status = '1'
     where id.docid = :docid;

    execute procedure wh_imp_doc_transfer(:docid);

    insert into docbond (DOCBONDTID, DOC1ID, DOC2ID)
    values ( (select dbtid from wh_dbtid_fundsale), :docid_fundsale, :docid);

    if (:queueid is NOT NULL) then
        execute procedure RBS_QUEUEBOND_INSERT(NULL, :queueid, :docid, NULL, 'I');

    execute procedure RBS_Q_CREATETASKEXPORT('Результат перемещения резерва',:docid,NULL,NULL)
      returning_values :queueid;

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^



SET TERM ^ ;

create procedure U3S_SELECT_TASKP_SITESET (
    taskid type of column wm_task.taskid
)
as
 /*$$IBE$$ declare variable clientid type of r_id;
declare variable docdate type of r_date;
declare variable wdval type of r_customdata;
declare variable dbeg type of r_date;
declare variable waresid type of r_id;
declare variable taskwaresid type of r_id;
declare variable siteid type of r_id;
declare variable whid type of r_id;
declare variable palcurcnt type of r_id;
declare variable palblkcnt type of r_id;
declare variable ttid_select type of r_id;
declare variable tmid_select_p type of r_id;
declare variable pfpriority type of r_shortnumber;
declare variable flbreak type of r_shortnumber;
declare variable docid type of column DOCUMENT.DOCID;
declare variable sitesegmentid type of column uv_site_segment.siteid;
declare variable defsitesegmentid type of column uv_site_segment.siteid;

declare variable dbtid_fundsale type of column docbondtype.docbondtid; $$IBE$$*/ 
begin /*$$IBE$$ 
    select tw.taskwaresid, tw.waresid, tw.siteid
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.status <> '2'
      into :taskwaresid, :waresid, :siteid;

    if (:siteid is not NULL) then exit;

    select d.fromobj,d.toobj,d.docdate,d.docid
      from wm_task t
           left join document d on d.docid=t.docid
     where t.taskid = :taskid
      into :whid,:clientid,:docdate,:docid;

    select dbt.docbondtid
      from docbondtype dbt
     where dbt.code = 'FUNDSALE'
      into :dbtid_fundsale;

    select db.doc1id
      from docbond db
     where db.doc2id = :docid
       and db.docbondtid = :dbtid_fundsale
      into :docid_fundsale;

    if (:docid_fundsale is NULL) then
        exception exc_wh_wrongdocstat 'Документ резерва продажи не найден!';

    select rcc.waresid as waresid, rcc.productdate as productdate, -rcc.amount  as amount
      from wh_reserve_client_changes rcc
     where rcc.docid = :docid_fundsale
       and rcc.waresid = :waresid
     union all
    select
      from wm_task t
           left join wm_task_wares tw
                left join site_stack
             on tw.taskid = t.taskid
     where t.docid = :docid
       and t.tasktypeid = :ttid_select
       and t.taskmethodid = :tmid
       and tw.waresid = :waresid

dbeg = '01.01.2000';
    select val
      from k_get_wares_data_obj_val(NULL,'SALEPERIOD',:waresid, :clientid, :docdate)
      into :wdval;

    if (:wdval is NOT NULL) then
        dbeg = :docdate - cast(:wdval as integer);


    execute procedure wh_ttid_select
     returning_values :ttid_select;

    select w.tmid
      from wh_tmid_get(:ttid_select, 'P') w
      into :tmid_select_p;

    select u.defsitesegmentid, u.sitesegmentid
      from uv_sitesegment_bydoc(:docid, :whid) u
      into :defsitesegmentid, :sitesegmentid;
    flbreak = 0;
    for
        select distinct wh.pfpriority
          from WH_CLIENT_LISTPALLETFEATURES(:clientid) wh
         where wh.pfpriority is NOT NULL and wh.pfpriority > 0
         order by wh.pfpriority ascending
          into :pfpriority
    do
    begin
        for
            select ss.siteid,ss.palcurcnt
              from site_stack ss
             where ss.waresid = :waresid
               and ss.productdate > :dbeg
               and ss.siteid is NOT NULL
               and exists(select *
                            from uv_sitesegment_bysite(ss.siteid) ssg
                           where coalesce(ssg.SSID, :defsitesegmentid) = :sitesegmentid)
               and exists(select *
                            from pallet p
                                 left join WH_CLIENT_LISTPALLETFEATURES(:clientid) pfc
                                   on pfc.pfid = p.featureid
                           where p.siteid = ss.siteid
                             and p.objid = :whid
                             and pfc.PFPRIORITY = :pfpriority)
             order by ss.productdate ascending,
                   iif(ss.palmaxcnt=ss.palcurcnt,1,0) ascending,
                   ss.palcurcnt ascending,
                   ss.dt ascending nulls first
              into :siteid, :palcurcnt
        do
        begin
            palblkcnt = NULL;
            select count(tw.taskwaresid)
              from wm_task_wares tw
                   left join wm_task t on t.taskid = tw.taskid
             where tw.tasktypeid = :ttid_select
               and tw.status in ('0','1')
               and tw.siteid = :siteid
               and tw.waresid = :waresid
               and t.status <> '2'
               and t.taskmethodid = :tmid_select_p
               and t.taskid <> :taskid
              into :palblkcnt;
            if (:palblkcnt is not NULL) then
                palcurcnt = :palcurcnt - :palblkcnt;

            if (:palcurcnt > 0) then
            begin
                flbreak = 1;
                break;
            end
        end

        if (:flbreak = 1) then
            break;
    end

    if (:siteid is NULL) then
    begin
        for
            select ss.siteid,ss.palcurcnt
              from site_stack ss
             where ss.waresid = :waresid
               and ss.productdate > :dbeg
               and ss.siteid is NOT NULL
               and exists(select *
                            from uv_sitesegment_bysite(ss.siteid) ssg
                           where coalesce(ssg.SSID, :defsitesegmentid) = :sitesegmentid)
               and exists(select *
                            from pallet p
                           where p.siteid = ss.siteid
                             and p.objid = :whid
                             and p.featureid is NULL)
             order by ss.productdate ascending,
                   iif(ss.palmaxcnt=ss.palcurcnt,1,0) ascending,
                   ss.palcurcnt ascending,
                   ss.dt ascending nulls first
              into :siteid, :palcurcnt
        do
        begin
            palblkcnt = NULL;
            select count(tw.taskwaresid)
              from wm_task_wares tw
                   left join wm_task t on t.taskid = tw.taskid
             where tw.tasktypeid = :ttid_select
               and tw.status in ('0','1')
               and tw.siteid = :siteid
               and tw.waresid = :waresid
               and t.status <> '2'
               and t.taskmethodid = :tmid_select_p
               and t.taskid <> :taskid
              into :palblkcnt;
            if (:palblkcnt is not NULL) then
                palcurcnt = :palcurcnt - :palblkcnt;

            if (:palcurcnt > 0) then
                break;
        end
    end

     $$IBE$$*/ /*for
        select distinct ss.siteid,ss.palcurcnt
          from wareslot wl
               left join wareslotitem wli
                    left join pallet p
                         left join site_stack ss on ss.siteid = p.siteid
                      on p.palletid = wli.palletid
                 on wli.wlotid=wl.wlotid
         where wl.waresid = :waresid
           and wl.productdate > :dbeg
           and wl.status = '1'
           and wl.objid = :whid
           and ss.siteid is NOT NULL
         order by wl.productdate ascending,
               iif(ss.palmaxcnt=ss.palcurcnt,1,0) ascending,
               ss.palcurcnt ascending,
               ss.dt ascending nulls first
--           and ss.palcurcnt > coalesce(ss.palblkcnt,0)
          into :siteid, :palcurcnt
    do
    begin
        palblkcnt = NULL;
        select count(tw.taskwaresid)
          from wm_task_wares tw
               left join wm_task t on t.taskid = tw.taskid
         where tw.tasktypeid = :ttid_select
           and tw.status in ('0','1')
           and tw.siteid = :siteid
           and tw.waresid = :waresid
           and t.status <> '2'
           and t.taskmethodid = :tmid_select_p
           and t.taskid <> :taskid
          into :palblkcnt;
        if (:palblkcnt is not NULL) then
            palcurcnt = :palcurcnt - :palblkcnt;

        if (:palcurcnt > 0) then
            break;
    end*/ /*$$IBE$$ 

    update site_stack ss
       set ss.palblkcnt = coalesce(ss.palblkcnt,0) + 1
     where ss.siteid = :siteid;

    update wm_task_wares tw
       set tw.siteid = :siteid
     where tw.taskwaresid = :taskwaresid;
 $$IBE$$*/ EXIT;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_P_JOINSITE (
    TASKID R_ID)
AS
declare variable objcode type of r_code3;
begin
    select wm.objcode
      from wm_config wm
      into :objcode;

    if (:objcode = 'UV') then
    begin
        execute procedure UV_SELECT_TASKP_SITESET(:taskid);
    end
    else if (:objcode = 'U3S') then
    begin
        execute procedure U3S_SELECT_TASKP_SITESET(:taskid);
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_P_JOINSITE (
    TASKID R_ID)
AS
declare variable objcode type of r_code3;
begin
    select wm.objcode
      from wm_config wm
      into :objcode;

    if (:objcode = 'UV') then
    begin
        execute procedure UV_SELECT_TASKP_SITESET(:taskid);
    end
    else if (:objcode = 'U3S') then
    begin
        execute procedure U3S_SELECT_TASKP_SITESET(:taskid);
    end
end^

SET TERM ; ^



ALTER TABLE K_TBLTMP_SELECT_DOCWARES
ADD PRODUCTDATE R_DATE;



SET TERM ^ ;

CREATE OR ALTER procedure WH_SALE_AFTERIMP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable queueid type of column R_QUEUE.queueid;
declare variable waresid type of column GWARES.WARESID;
declare variable wcode type of column GWARES.code;
declare variable docid_fundsale type of column DOCUMENT.docid;
begin
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

        exception exc_wh_wrongamount 'Не верные данные по резерву у товара с кодом' || :wcode;
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

    execute procedure RBS_Q_CREATETASKEXPORT('Результат перемещения резерва',:docid,NULL,NULL)
      returning_values :queueid;

    delete from imp_document id
     where id.docid = :docid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE_PREP (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable waresid type of column GWARES.waresid;
declare variable selgroupid type of column k_wares_selgroup.id;
declare variable maxfactor type of r_double;
declare variable amount type of r_double;
declare variable numpallet type of r_number;
declare variable numpos type of r_number;
declare variable palletunitid type of r_id;
declare variable ttid_select type of r_id;
declare variable tmid_pallet type of column wm_taskmethod.methodid;
declare variable tmid_f type of column wm_taskmethod.methodid;
declare variable objid type of r_id;
declare variable weight type of r_double;
declare variable capacity type of r_double;
declare variable zoneid type of r_id;
declare variable cntzone type of r_number;
declare variable docid_fundsale type of column DOCUMENT.docid;
declare variable productdate type of column WARESLOT.productdate;
begin
    select distinct db.doc1id
      from docbond db
     where db.doc2id = :docid
       and db.docbondtid = (select dbtid from wh_dbtid_fundsale)
      into :docid_fundsale;

    if (:docid_fundsale is NULL) then
        exception exc_wh_wrongdocstat 'Документ резерва продажи не найден!';


    select wm.palletunitid
      from wm_config wm
      into :palletunitid;

    select k.ttid
      from k_tasktype_by_code('SELECT',NULL) k
      into :ttid_select;

    select tm.methodid
      from wm_taskmethod tm
     where tm.tasktypeid = :ttid_select and tm.algorithm = 'P'
      into :tmid_pallet;

    select tm.methodid
      from wm_taskmethod tm
     where tm.tasktypeid = :ttid_select and tm.algorithm = 'F'
      into :tmid_f;

    if (:tmid_f is NULL) then
        exception exc_k_common 'Не найден метод отборки с паллета!';

    select d.fromobj
      from document d
     where d.docid = :docid
      into :objid;

    -- Зона по умолчанию
    for
        select sz.zoneid
          from sitezone sz
         where sz.objid = :objid
          into :zoneid
    do
        cntzone = :cntzone + 1;
    if (:cntzone <> 1) then zoneid = 0;

    numpallet = 0;
    numpos = 1;
    for
        with wares as(
            select rcc.waresid as waresid, rcc.productdate as productdate, sum(rcc.amount)  as amount
              from wh_reserve_client_changes rcc
             where rcc.docid = :docid_fundsale
            group by rcc.waresid, rcc.productdate
        )
        select w.waresid,w.productdate,w.amount,coalesce(g.selgroup,0),wu.factor
          from wares w
               left join gwares g on g.waresid = w.waresid
               left join waresunit wu on wu.waresid = w.waresid and wu.unitid = :palletunitid
          into :waresid,:productdate,:amount,:selgroupid,:maxfactor
    do
    begin
        -- Откидываем полные поддоны
        if (:maxfactor is NOT NULL) then
            while (:amount-:maxfactor > -0.000001) do -- and :rest - :maxfactor > -0.000001) do
            begin
                weight = NULL; capacity = NULL;
                select wc.weight,wc.capacity
                  from WM_GETWARESWEIGHTCAPACITY(:waresid,:maxfactor) wc
                  into :weight,:capacity;

                numpallet = :numpallet + 1;
                insert into k_tbltmp_select_docwares(waresid,amount,selgroupid,taskmethodid,rest,slotid,rowid,weight,capacity,numpallet,num,zoneid,productdate)
                values(:waresid,:maxfactor,:selgroupid,:tmid_pallet,NULL,NULL,NULL,:weight,:capacity,:numpallet,:numpos,:zoneid,:productdate);

                amount = :amount - :maxfactor;
            end
        
        -- Скидываем остатки
        if (:amount>0.00001) then
        begin
            weight = NULL; capacity = NULL;
            select wc.weight,wc.capacity
              from WM_GETWARESWEIGHTCAPACITY(:waresid,:amount) wc
              into :weight,:capacity;

             insert into k_tbltmp_select_docwares(waresid,amount,selgroupid,taskmethodid,rest,slotid,rowid,weight,capacity,zoneid,sitesegmentid,productdate)
             values(:waresid,:amount,:selgroupid,:tmid_f,NULL,NULL,NULL,:weight,:capacity,:zoneid,NULL,:productdate);
        end
    end

    update k_tbltmp_select_docwares sd
       set sd.numpallet = :numpallet + 1
     where sd.taskmethodid=:tmid_f
       and numpallet is NULL;
end^

SET TERM ; ^



ALTER TABLE WM_TASK_WARES
ADD PLANDATETIME R_DATETIME;



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE (
    DOCID type of column DOCUMENT.DOCID)
AS
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable ttinitst_select type of column wm_tasktype.initstatus;
declare variable tmid_select type of column wm_taskmethod.methodid;
declare variable waresid type of column GWARES.waresid;
declare variable amount type of r_double;
declare variable numpallet type of r_number;
declare variable numpos type of r_number;
declare variable status type of r_status;
declare variable slotid type of r_id;
declare variable taskid type of r_id;
declare variable taskpalletnum type of r_number;
declare variable price type of r_double;
declare variable CAPACITY type of r_double;
declare variable WEIGHT type of r_double;
declare variable Zoneid type of r_id;
declare variable productdate type of column wm_task_wares.plandatetime;
begin
    execute procedure u3s_taskselect_create_prep(:docid);

    select k.ttid,coalesce(k.ttinitst,'0')
      from k_tasktype_by_code('SELECT',NULL) k
      into :ttid_select,:ttinitst_select;


    taskid = NULL;
    taskpalletnum = -1;
    for
        select coalesce(k.numpallet,0),k.num,k.taskmethodid,k.waresid,k.amount,k.slotid,coalesce(tm.startstatus,:ttinitst_select),k.zoneid,k.productdate
          from k_tbltmp_select_docwares k
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
         order by k.numpallet ascending nulls last,k.num ascending nulls last
          into :numpallet,:numpos,:tmid_select,:waresid,:amount,:slotid,:status,:zoneid,:productdate
    do
    begin
        if (:taskpalletnum <> :numpallet and :taskpalletnum is NOT NULL and :numpallet is NOT NULL) then
        begin
            if (:taskid is NOT NULL) then
            begin
                select sum(ww.weight),sum(ww.capacity)
                  from wm_task_wares tw
                       left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
                 where tw.taskid = :taskid
                  into :WEIGHT,:CAPACITY;
            
                update wm_task t
                   set t.weight = :weight,t.capacity = :capacity
                 where t.taskid = :taskid;
            end

            taskpalletnum = :numpallet;

            if (:zoneid = 0) then zoneid = NULL;
            insert into wm_task(tasktypeid,taskmethodid,status,docid,num,zoneid)
            values (:ttid_select,:tmid_select,:status,:docid,:numpallet,:zoneid)
            returning taskid
            into :taskid;
        end

        price = NULL;
        select round(sum(cg.docsum)/sum(cg.amount),4)
          from cargo cg
         where cg.document = :docid
           and cg.waresid = :waresid
           and cg.cargo2id is NULL
           and cg.amount > 0.0001
          into :price;
        if (:price is null) then price = 0.000;

        insert into wm_task_wares(taskid,waresid,status,quantity,siteid,num,summa,plandatetime)
        values(:taskid,:waresid,iif(:tmid_select is NOT NULL,'0',NULL),:amount,:slotid,:numpos,:price,:productdate);
    end

    if (:taskid is NOT NULL) then
    begin
        select sum(ww.weight),sum(ww.capacity)
          from wm_task_wares tw
               left join wm_getwaresweightcapacity(tw.waresid,tw.quantity) ww on 1=1
         where tw.taskid = :taskid
          into :WEIGHT,:CAPACITY;
    
        update wm_task t
           set t.weight = :weight,t.capacity = :capacity
         where t.taskid = :taskid;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_TASKSELECT_CREATE_PREVIEW (
    DOCID type of column DOCUMENT.DOCID)
returns (
    NUMPALLET type of R_NUMBER,
    ZONEID type of column SITEZONE.ZONEID,
    ZONENAME type of column SITEZONE.NAME,
    NUMPOS type of R_NUMBER,
    TMALGO type of column WM_TASKMETHOD.ALGORITHM,
    TMNAME type of column WM_TASKMETHOD.NAME,
    WID type of column GWARES.WARESID,
    WCODE type of column GWARES.CODE,
    WNAME type of column GWARES.NAME,
    WQUANTITY type of R_DOUBLE,
    WWEIGHT type of R_DOUBLE,
    WCAPACITY type of R_DOUBLE,
    VUCODE type of column UNIT.SHORTNAME,
    VUFACTOR type of column WARESUNIT.FACTOR,
    MUCODE type of column UNIT.SHORTNAME,
    MUFACTOR type of column WARESUNIT.FACTOR,
    WSGCODE type of column K_WARES_SELGROUP.CODE,
    WSGNAME type of column K_WARES_SELGROUP.NAME,
    WSGWEIGHT type of R_DOUBLE,
    WSGCAPACITY type of R_DOUBLE,
    productdate type of column WARESLOT.productdate)
AS
begin
    execute procedure u3s_taskselect_create_prep(:docid);

    for
        select g.waresid,g.code,g.name,
               mwu.factor,mu.shortname,vwu.factor,vu.shortname,
               k.numpallet,k.num,k.amount,k.capacity,k.weight,
               tm.algorithm,tm.name,
               wsg.code,wsg.name,wsg.capacity,wsg.weight,
               k.zoneid,sz.name,k.productdate
          from k_tbltmp_select_docwares k
               left join gwares g
                    left join waresunit vwu
                         left join unit vu on vu.unitid = vwu.unitid
                      on vwu.waresunitid = g.viewunitid
                    left join waresunit mwu
                         left join unit mu on mu.unitid = mwu.unitid
                      on mwu.waresunitid = g.mainunitid
                 on g.waresid = k.waresid
               left join wm_taskmethod tm on tm.methodid = k.taskmethodid
               left join k_wares_selgroup wsg on wsg.id = k.selgroupid
               left join sitezone sz on sz.zoneid = k.zoneid
         order by k.numpallet ascending Nulls first,k.num ascending nulls first
          into :wid,:wcode,:wname,:mufactor,:mucode,:vufactor,:vucode,
               :numpallet,:numpos,:wquantity,:wcapacity,:wweight,
               :tmalgo,:tmname,:wsgcode,:wsgname,:wsgcapacity,:wsgweight,
               :zoneid,:zonename,:productdate
    do
        suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SELECT_TASKP_SITESET (
    TASKID type of column WM_TASK.TASKID)
AS
declare variable waresid type of r_id;
declare variable taskwaresid type of r_id;
declare variable siteid type of r_id;
declare variable whid type of r_id;
declare variable palcurcnt type of r_id;
declare variable palblkcnt type of r_id;
declare variable ttid_select type of r_id;
declare variable tmid_select_p type of r_id;
declare variable pfpriority type of r_shortnumber;
declare variable flbreak type of r_shortnumber;
declare variable docid type of column DOCUMENT.DOCID;
declare variable sitesegmentid type of column uv_site_segment.siteid;
declare variable defsitesegmentid type of column uv_site_segment.siteid;

declare variable dbtid_fundsale type of column docbondtype.docbondtid;
declare variable productdate type of column WARESLOT.productdate;
begin
    select tw.taskwaresid, tw.waresid, tw.siteid, tw.plandatetime
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.status <> '2'
      into :taskwaresid, :waresid, :siteid, :productdate;

    if (:siteid is not NULL) then exit;

    select d.fromobj, d.docid, t.tasktypeid, t.taskmethodid
      from wm_task t
           left join document d on d.docid=t.docid
     where t.taskid = :taskid
      into :whid, :docid, :ttid_select, :tmid_select_p;

    flbreak = 0;
    for
        select ss.siteid,ss.palcurcnt
          from site_stack ss
         where ss.waresid = :waresid
           and ss.productdate = :productdate
           and ss.siteid is NOT NULL
         order by iif(ss.palmaxcnt=ss.palcurcnt,1,0) ascending,
               ss.palcurcnt ascending,
               ss.dt ascending nulls first
          into :siteid, :palcurcnt
    do
    begin
        palblkcnt = NULL;
        select count(tw.taskwaresid)
          from wm_task_wares tw
               left join wm_task t on t.taskid = tw.taskid
         where tw.tasktypeid = :ttid_select
           and tw.status in ('0','1')
           and tw.siteid = :siteid
           and tw.waresid = :waresid
           and t.status <> '2'
           and t.taskmethodid = :tmid_select_p
           and t.taskid <> :taskid
          into :palblkcnt;
        if (:palblkcnt is not NULL) then
            palcurcnt = :palcurcnt - :palblkcnt;

        if (:palcurcnt > 0) then
        begin
            flbreak = 1;
            break;
        end
    end

    update site_stack ss
       set ss.palblkcnt = coalesce(ss.palblkcnt,0) + 1
     where ss.siteid = :siteid;

    update wm_task_wares tw
       set tw.siteid = :siteid
     where tw.taskwaresid = :taskwaresid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SELECT_TASKP_SITESET (
    TASKID type of column WM_TASK.TASKID)
AS
declare variable waresid type of r_id;
declare variable taskwaresid type of r_id;
declare variable siteid type of r_id;
declare variable whid type of r_id;
declare variable palcurcnt type of r_id;
declare variable palblkcnt type of r_id;
declare variable ttid_select type of r_id;
declare variable tmid_select_p type of r_id;
declare variable flbreak type of r_shortnumber;
declare variable docid type of column DOCUMENT.DOCID;
declare variable sitesegmentid type of column uv_site_segment.siteid;
declare variable defsitesegmentid type of column uv_site_segment.siteid;

declare variable dbtid_fundsale type of column docbondtype.docbondtid;
declare variable productdate type of column WARESLOT.productdate;
begin
    select tw.taskwaresid, tw.waresid, tw.siteid, tw.plandatetime
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.status <> '2'
      into :taskwaresid, :waresid, :siteid, :productdate;

    if (:siteid is not NULL) then exit;

    select d.fromobj, d.docid, t.tasktypeid, t.taskmethodid
      from wm_task t
           left join document d on d.docid=t.docid
     where t.taskid = :taskid
      into :whid, :docid, :ttid_select, :tmid_select_p;

    flbreak = 0;
    for
        select ss.siteid,ss.palcurcnt
          from site_stack ss
         where ss.waresid = :waresid
           and ss.productdate = :productdate
           and ss.siteid is NOT NULL
         order by iif(ss.palmaxcnt=ss.palcurcnt,1,0) ascending,
               ss.palcurcnt ascending,
               ss.dt ascending nulls first
          into :siteid, :palcurcnt
    do
    begin
        palblkcnt = NULL;
        select count(tw.taskwaresid)
          from wm_task_wares tw
               left join wm_task t on t.taskid = tw.taskid
         where tw.tasktypeid = :ttid_select
           and tw.status in ('0','1')
           and tw.siteid = :siteid
           and tw.waresid = :waresid
           and t.status <> '2'
           and t.taskmethodid = :tmid_select_p
           and t.taskid <> :taskid
          into :palblkcnt;
        if (:palblkcnt is not NULL) then
            palcurcnt = :palcurcnt - :palblkcnt;

        if (:palcurcnt > 0) then
        begin
            flbreak = 1;
            break;
        end
    end

    update site_stack ss
       set ss.palblkcnt = coalesce(ss.palblkcnt,0) + 1
     where ss.siteid = :siteid;

    update wm_task_wares tw
       set tw.siteid = :siteid
     where tw.taskwaresid = :taskwaresid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SELECT_TASKP_SITESET (
    TASKID type of column WM_TASK.TASKID)
AS
declare variable waresid type of r_id;
declare variable taskwaresid type of r_id;
declare variable siteid type of r_id;
declare variable whid type of r_id;
declare variable palcurcnt type of r_id;
declare variable palblkcnt type of r_id;
declare variable ttid_select type of r_id;
declare variable tmid_select_p type of r_id;
declare variable flbreak type of r_shortnumber;
declare variable docid type of column DOCUMENT.DOCID;
declare variable sitesegmentid type of column uv_site_segment.siteid;
declare variable defsitesegmentid type of column uv_site_segment.siteid;

declare variable dbtid_fundsale type of column docbondtype.docbondtid;
declare variable productdate type of column WARESLOT.productdate;
begin
    select tw.taskwaresid, tw.waresid, tw.siteid, tw.plandatetime
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.status <> '2'
      into :taskwaresid, :waresid, :siteid, :productdate;

    if (:siteid is not NULL) then exit;

    select d.fromobj, t.tasktypeid, t.taskmethodid
      from wm_task t
           left join document d on d.docid=t.docid
     where t.taskid = :taskid
      into :whid, :ttid_select, :tmid_select_p;

    flbreak = 0;
    for
        select ss.siteid,ss.palcurcnt
          from site_stack ss
         where ss.waresid = :waresid
           and ss.productdate = :productdate
           and ss.siteid is NOT NULL
         order by iif(ss.palmaxcnt=ss.palcurcnt,1,0) ascending,
               ss.palcurcnt ascending,
               ss.dt ascending nulls first
          into :siteid, :palcurcnt
    do
    begin
        palblkcnt = NULL;
        select count(tw.taskwaresid)
          from wm_task_wares tw
               left join wm_task t on t.taskid = tw.taskid
         where tw.tasktypeid = :ttid_select
           and tw.status in ('0','1')
           and tw.siteid = :siteid
           and tw.waresid = :waresid
           and t.status <> '2'
           and t.taskmethodid = :tmid_select_p
           and t.taskid <> :taskid
          into :palblkcnt;
        if (:palblkcnt is not NULL) then
            palcurcnt = :palcurcnt - :palblkcnt;

        if (:palcurcnt > 0) then
        begin
            flbreak = 1;
            break;
        end
    end

    update site_stack ss
       set ss.palblkcnt = coalesce(ss.palblkcnt,0) + 1
     where ss.siteid = :siteid;

    update wm_task_wares tw
       set tw.siteid = :siteid
     where tw.taskwaresid = :taskwaresid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure U3S_SELECT_TASKP_SITESET (
    TASKID type of column WM_TASK.TASKID)
AS
declare variable waresid type of column GWARES.waresid;
declare variable taskwaresid type of column wm_task_wares.taskwaresid;
declare variable siteid type of column SITE.siteid;
declare variable palcurcnt type of column site_stack.palcurcnt;
declare variable palblkcnt type of column site_stack.palblkcnt;
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable tmid_select_p type of column wm_taskmethod.methodid;
declare variable productdate type of column WARESLOT.productdate;
begin
    select tw.taskwaresid, tw.waresid, tw.siteid, tw.plandatetime
      from wm_task_wares tw
     where tw.taskid = :taskid
       and tw.status <> '2'
      into :taskwaresid, :waresid, :siteid, :productdate;

    if (:siteid is not NULL) then exit;

    select t.tasktypeid, t.taskmethodid
      from wm_task t
     where t.taskid = :taskid
      into :ttid_select, :tmid_select_p;

    for
        select ss.siteid,ss.palcurcnt
          from site_stack ss
         where ss.waresid = :waresid
           and ss.productdate = :productdate
           and ss.siteid is NOT NULL
         order by iif(ss.palmaxcnt=ss.palcurcnt,1,0) ascending,
               ss.palcurcnt ascending,
               ss.dt ascending nulls first
          into :siteid, :palcurcnt
    do
    begin
        palblkcnt = NULL;
        select count(tw.taskwaresid)
          from wm_task_wares tw
               left join wm_task t on t.taskid = tw.taskid
         where tw.tasktypeid = :ttid_select
           and tw.status in ('0','1')
           and tw.siteid = :siteid
           and tw.waresid = :waresid
           and t.status <> '2'
           and t.taskmethodid = :tmid_select_p
           and t.taskid <> :taskid
          into :palblkcnt;
        if (:palblkcnt is not NULL) then
            palcurcnt = :palcurcnt - :palblkcnt;

        if (:palcurcnt > 0) then
        begin
            break;
        end
    end

    update site_stack ss
       set ss.palblkcnt = coalesce(ss.palblkcnt,0) + 1
     where ss.siteid = :siteid;

    update wm_task_wares tw
       set tw.siteid = :siteid
     where tw.taskwaresid = :taskwaresid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_P_JOINSITE (
    TASKID R_ID)
AS
declare variable objcode type of r_code3;
begin
    select wm.objcode
      from wm_config wm
      into :objcode;

    if (:objcode = 'UV') then
    begin
        execute procedure UV_SELECT_TASKP_SITESET(:taskid);
    end
    else if (:objcode = 'U3S') then
    begin
        execute procedure U3S_SELECT_TASKP_SITESET(:taskid);
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_P_TASKINFO (
    TASKID R_ID)
returns (
    TID type of R_ID,
    TSTAT type of R_STATUS,
    SITEID type of R_ID,
    SITENAME type of R_NAME,
    PALLETID type of R_ID,
    PNUMBER type of R_BARCODE,
    PALPRODUCTDATE type of R_DATE,
    PALBESTBEFOREDATE type of R_DATE,
    PBARCODE type of R_BARCODE,
    DOCID type of R_ID64,
    DOCNUM type of DOCNUMBER,
    DOCDATE type of R_DATE,
    DOCSTAT type of R_STATUS,
    FROMID type of R_ID,
    FROMNAME type of R_NAME,
    TOID type of R_ID,
    TONAME type of R_NAME,
    WID type of R_ID,
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    VWUID type of R_ID,
    VUFACTOR type of R_DOUBLE,
    VUCODE type of R_CODE,
    MWUID type of R_ID,
    MUFACTOR type of R_DOUBLE,
    MUCODE type of R_CODE,
    QPLAN type of R_DOUBLE,
    QPALLET type of R_DOUBLE,
    CANSELECT type of R_FLAG)
AS
declare variable pfeatureid type of r_id;
begin
    select t.taskid,t.status,
           d.docid,d.docdate,d.number,d.status,
           d.fromobj,(select fullname from getobjectname(d.fromobj,NULL)),
           d.toobj,(select fullname from getobjectname(d.toobj,NULL))
      from wm_task t
           left join document d on d.docid=t.docid
     where t.taskid = :taskid
      into :tid,:tstat,
           :docid,:docdate,:docnum,:docstat,
           :fromid, :fromname,
           :toid, :toname;

    select tw.quantity, s.siteid, s.name,
           p.palletid, p.number, p.barcode, p.featureid,
           g.waresid, g.code, g.name,
           vwu.waresunitid, vwu.factor, vu.shortname,
           mwu.waresunitid, mwu.factor, mu.shortname
      from wm_task_wares tw
           left join site s on s.siteid = tw.siteid
           left join pallet p
             on p.palletid = tw.palletid
           left join gwares g
                left join waresunit vwu
                     left join unit vu on vu.unitid = vwu.unitid
                  on vwu.waresunitid = g.viewunitid
                left join waresunit mwu
                     left join unit mu on mu.unitid = mwu.unitid
                  on mwu.waresunitid = g.mainunitid
             on g.waresid = tw.waresid
     where tw.taskid = :taskid
       and tw.status <> '2'
      into :qplan, :siteid, :sitename,
           :palletid, :pnumber, :pbarcode, :pfeatureid,
           :wid, :wcode, :wname,
           :vwuid, :vufactor, :vucode,
           :mwuid, :mufactor, :mucode;

    if (:palletid is NOT NULL) then
    begin
        select sum(wli.amount)
          from wareslotitem wli
         where wli.palletid = :palletid
          into :qpallet;

        select pfp.productdate, pfp.bestbeforedate
          from pallet_finishprint pfp
         where pfp.palletid = :palletid
          into :palproductdate, :palbestbeforedate;
    end

    /*if (:pfeatureid is NOT NULL and
        exists(select *
                 from WH_CLIENT_LISTPALLETFEATURES(:toid) pfc
                where pfc.pfid = :pfeatureid
                  and pfc.pfpriority is NOT NULL and pfc.pfpriority > 0)) then
        canselect = '1';
    else
        canselect = '0';*/

    canselect = '1';

    suspend;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECTDC_P_SCANPALLET (
    ID type of R_ID,
    BARCODE type of R_BARCODE)
AS
declare variable PALLETID R_ID;
declare variable PALLETID_TASK R_ID;
declare variable psiteid R_ID;
declare variable wlincomeid R_ID;
declare variable wlotid R_ID;
declare variable amount R_DOUBLE;
declare variable quantity R_DOUBLE;
declare variable taskwaresid R_DOUBLE;
declare variable palletid_temp R_ID;
declare variable palletmanid R_ID;
declare variable employeeid R_ID;
declare variable wmsid R_ID;
declare variable waresid R_ID;
declare variable clientid R_ID;
declare variable pfeatureid R_ID;
begin

    select wms.objid,t.wm_sessionid, d.toobj
      from wm_task t
           left join document d
             on d.docid = t.docid
           left join wm_session wms
             on wms.sessionid = t.wm_sessionid
     where t.taskid = :id
      into :employeeid, :wmsid, :clientid;

    select p.palletid,p.siteid,p.featureid
      from pallet p
     where p.barcode = :barcode
      into :palletid, :psiteid, :pfeatureid;
    if (:palletid is NULL) then
        exception exc_wh_wrongbarcode;

/*    if (:pfeatureid is NUll or
        not exists(select *
                     from WH_CLIENT_LISTPALLETFEATURES(:clientid) wh
                    where wh.PFID = :pfeatureid
                      and wh.pfpriority is NOT NULL
                      and wh.pfpriority > 0)) then
        exception exc_wh_wrongbarcode 'Характеристика паллета запрещает его отборку этому клиенту!';*/

    select first(1) tw.palletid, tw.taskwaresid, tw.waresid
      from wm_task_wares tw
     where tw.taskid = :id
       and tw.status <> '2'
      into :palletid_task, :taskwaresid, :waresid;
    if (:palletid_task is NULL or :palletid_task <> :palletid) then
        exception exc_wh_wrongbarcode;
    if (not exists(select *
                     from pallet_finishprint pfp
                    where pfp.palletid = :palletid
                      and pfp.waresid = :waresid )) then
        execute procedure r_raiseerror('WARES_NOTFOUND');


    select pt.manid, pt.palletid
      from pallet_temp pt
     where pt.taskid = :id
      into :palletmanid, :palletid_temp;

    amount = 0.000;
    for
        select wli.amount, wli.wlotid, wli.wlincomeid
          from wareslotitem wli
         where wli.palletid = :palletid_task
         order by wli.wlincomeid
          into :quantity, :wlotid, :wlincomeid
    do
    begin
        if (:palletid_temp is NULL) then
            insert into pallet_temp(manid, taskid)
            values(:employeeid, :id)
            returning palletid
            into :palletid_temp;
        else if (:employeeid <> :palletmanid) then
            update pallet_temp pt
               set pt.manid = :employeeid
             where pt.taskid = :id and pt.palletid = :palletid_temp;

        insert into wm_task_lot(taskwaresid, palletid, quantity, wlotid, wlincomeid, chgwli)
        values(:taskwaresid, :palletid_task, -:quantity, :wlotid, :wlincomeid, '1');

        insert into wm_task_lot(taskwaresid, palletid, quantity, wlotid, wlincomeid, chgwli)
        values(:taskwaresid, :palletid_temp, :quantity, :wlotid, :wlincomeid, '1');

        amount = :amount + :quantity;
    end

    update wm_task_wares tw
       set tw.scanquant = :amount,
           tw.status = '2',
           tw.endtime = current_timestamp,
           tw.wm_sessionid = :wmsid
     where tw.taskwaresid = :taskwaresid;

    update site_stack ss
       set ss.palblkcnt = coalesce(ss.palblkcnt,0) - 1
     where ss.siteid = :psiteid;
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure U3S_SELECTDC_TASKENDLISTWARPAL (
    TASKID R_ID)
returns (
    WCODE type of R_CODE,
    WNAME type of R_NAME,
    AMOUNT type of R_DOUBLE)
AS
declare variable docid type of r_id64;
declare variable ttid_gateauto type of r_id;
declare variable ttid_loadauto type of r_id;
declare variable tid_loadauto type of r_id;
declare variable tid_gateauto type of r_id;
declare variable tbtid_cardocs type of r_id;
begin
    select t.docid
      from wm_task t
     where t.taskid = :taskid
      into :docid;

    execute procedure wh_ttid_gateauto returning_values :ttid_gateauto;
    execute procedure wh_ttid_loadauto returning_values :ttid_loadauto;

    select t.taskid
      from wm_task t
     where t.docid = :docid
       and t.tasktypeid = :ttid_loadauto
      into :tid_loadauto;

    if (:tid_loadauto is NOT NULL) then
    begin
        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'CARDOCS'
          into :tbtid_cardocs;

        select t.taskid
          from wh_taskbond tb
               left join wm_task t on t.taskid = tb.task1id
         where tb.task2id = :tid_loadauto
           and tb.taskbondtid = :tbtid_cardocs
           and t.tasktypeid = :ttid_gateauto
           and t.status = '1'
          into :tid_gateauto;

        for
            select g.code, g.name, sum(cg.amount)
              from wh_taskbond tb
                   left join wm_task t
                        left join wh_idx_listcargo(t.docid) cg
                             left join gwares g on g.waresid = cg.waresid
                          on 1=1
                     on t.taskid = tb.task2id
             where tb.task1id = :tid_gateauto
               and tb.taskbondtid = :tbtid_cardocs
               and t.tasktypeid = :ttid_loadauto
               and coalesce(g.pa,'1') = '0'
             group by g.code, g.name
              into :wcode, :wname, :amount
        do
            suspend;
    end
end^

SET TERM ; ^



SET TERM ^ ;

create or alter procedure K_U3S_SELECT_TSTCHG (
    TASKID type of R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable ttcode type of r_code;
declare variable ttid type of r_id;
declare variable docid type of r_id64;
declare variable wmsid type of r_id;
declare variable tid_loadpallet type of r_id;
declare variable tid_gateauto type of r_id;
declare variable tflags type of wh_flags;
begin
    select tt.code,tt.tasktypeid,t.docid,t.tmpflags,t.wm_sessionid
      from wm_task t
           left join wm_tasktype tt on tt.tasktypeid=t.tasktypeid
     where t.taskid = :taskid
      into :ttcode,:ttid,:docid,:tflags,:wmsid;

    if (:ttcode <> 'SELECT') then
        exception exc_k_wrongtasktype;

    if (:newstat = '2') then
    begin
        if (not exists(select *
                         from wm_task t
                        where t.docid = :docid
                          and t.tasktypeid = :ttid
                          and t.taskmethodid is NOT NULL
                          and t.status <> '2')) then
            update document d
               set d.status = '2'
             where d.docid = :docid;

        select t.tid_gateauto
          from WH_LOADAUTODC_GETTASKBYDOC(:docid) t
          into :tid_gateauto;
        if (:tid_gateauto is NOT NULL) then
            execute procedure wh_loadpalletdc_createtaskes(:tid_gateauto);

        if ((:tflags is NOT NULL and :tflags containing 'A')
            or
            not exists(select *
                         from wm_task_wares tw
                              left join wm_task_lot tl on tl.taskwaresid = tw.taskwaresid
                        where tw.taskid = :taskid
                          and tl.palletid is NOT NULL)
        ) then
        begin
            select tb.task1id
              from wh_taskbond tb
                   left join wh_taskbondtype tbt on tbt.id = tb.taskbondtid
                   left join wm_task t on t.taskid = tb.task1id
             where tb.task2id = :taskid
               and tbt.code = 'LOADSELECT'
               and coalesce(t.status,'0') <> '2'
              into :tid_loadpallet;

            if (:tid_loadpallet is NOT NULL) then
            begin
                update wm_task t
                   set t.wm_sessionid = null, t.status = '0'
                 where t.taskid = :tid_loadpallet
                   and coalesce(t.wm_sessionid,0) <> :wmsid;
                execute procedure K_SESSION_JOIN_TASK(:tid_loadpallet, :wmsid);
                execute procedure wh_loadpalletdc_taskend(:tid_loadpallet);
            end
        end
    end
end^

SET TERM ; ^



SET TERM ^ ;

create procedure WH_SELECT_CLIENTUNFUND (
    taskid type of column wm_task.taskid
)
as
declare variable whid type of column OBJECT.objid ;
declare variable clientid type of column OBJECT.objid ;
declare variable docid type of column DOCUMENT.docid ;
begin
   select d.fromobj, d.toobj, d.docid
     from wm_task t
          left join document d on d.docid = t.docid
    where t.taskid = :taskid
     into :whid, :clientid, :docid;

   insert into wh_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
   select :docid, tw.waresid, tw.plandatetime, tw.quantity, :whid, :clientid
     from wm_task_wares tw
    where tw.taskid = :taskid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_TASKEND (
    TID_LOADPALLET R_ID)
AS
declare variable tid_loadauto r_id;
declare variable tid_gateauto r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_CARDOCS r_id;
declare variable tpriority r_number;
declare variable palid_select r_id;
declare variable tbtid_loadselect r_id;
declare variable wlotid r_id;
declare variable wlincomeid r_id;
declare variable waresid r_id;
declare variable taskwaresid r_id;
declare variable wmsessionid r_id;
declare variable amount r_double;
declare variable docid r_id64;
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable taskid_select type of column wm_task.taskid;
begin
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'DOCPALLETS'
      into :tbtid_docpallets;

    select t.taskid,t.priority,t.docid
      from wh_taskbond tb
           left join wm_task t on t.taskid = tb.task1id
     where tb.task2id = :tid_loadpallet
       and tb.taskbondtid = :tbtid_docpallets
      into :tid_loadauto,:tpriority,:docid;

    if (:tpriority is NOT NULL) then
    begin
        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'CARDOCS'
          into :tbtid_CARDOCS;
    
        select t.taskid
          from wh_taskbond tb
               left join wm_task t on t.taskid = tb.task1id
         where tb.task2id = :tid_loadauto
           and tb.taskbondtid = :tbtid_cardocs
          into :tid_gateauto;

        if (exists(select *
                     from wh_taskbond tb
                          left join wm_task t
                               left join wh_taskbond tb2
                                    left join wm_task t2 on t2.taskid = tb2.task2id
                                 on tb2.task1id = t.taskid and tb2.taskbondtid = :tbtid_docpallets
                            on t.taskid = tb.task2id
                    where tb.task1id = :tid_gateauto
                      and tb.taskbondtid = :tbtid_cardocs
                      and t.priority is NOT NULL and t.priority < :tpriority
                      and t2.taskid is NOT NULL and t2.status <> '2' )) then
            exception exc_k_common 'Подождите, есть поддоны, которые должны быть загружены раньше вашего!';

    end

    -- Возможно нужно списать остатки
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'LOADSELECT'
      into :tbtid_loadselect;

    select ps.palletid, t.taskid
      from wh_taskbond tb
           left join wm_task t
                left join pallet_select ps on ps.taskid = t.taskid
             on t.taskid = tb.task2id
     where tb.task1id = :tid_loadpallet
       and tb.taskbondtid = :tbtid_loadselect
      into :palid_select, :taskid_select;

    if (:palid_select is NOT NULL) then
    begin
        execute procedure WH_SELECT_CLIENTUNFUND(:taskid_select);

        select t.wm_sessionid
          from wm_task t
         where t.taskid = :tid_loadpallet
          into :wmsessionid;

        for
            select wli.wlotid,wli.wlincomeid,sum(wli.amount)
              from wareslotitem wli
             where wli.palletid = :palid_select
             group by wli.wlotid, wli.wlincomeid
             order by wli.wlotid, wli.wlincomeid nulls last
              into :wlotid, :wlincomeid, :amount
        do
        begin
            waresid = NULL;
            select wl.waresid
              from wareslot wl
             where wl.wlotid = :wlotid
              into :waresid;

            taskwaresid = NULL;
            select tw.taskwaresid
              from wm_task_wares tw
             where tw.taskid = :tid_loadpallet
               and tw.waresid = :waresid
              into :taskwaresid;
            if (:taskwaresid is NULL) then
                insert into wm_task_wares(taskid, waresid, status, wm_sessionid, begintime)
                values(:tid_loadpallet, :waresid, '1', :wmsessionid, current_timestamp)
                returning taskwaresid
                into :taskwaresid;

            insert into wm_task_lot(taskwaresid, wlotid, palletid, wlincomeid,  quantity, chgwli)
            values(:taskwaresid, :wlotid, :palid_select, :wlincomeid, -:amount, '1');

            update wm_task_wares tw
               set tw.status = '2',
                   tw.endtime = current_timestamp,
                   tw.quantity = coalesce(tw.quantity,0.000) + :amount
              where tw.taskwaresid = :taskwaresid;
        end
    end

    -- Закрываем само задание на погрузку паллета в автомобиль
    UPDATE wm_task t
       set t.status = '2',t.endtime = current_timestamp
     where t.taskid = :tid_loadpallet;

    -- Закрыть задание на погрузку документа в машину
    if (not exists(select *
                     from wh_taskbond tb
                          left join wm_task t on t.taskid = tb.task2id
                    where tb.task1id = :tid_loadauto
                      and tb.taskbondtid = :tbtid_docpallets
                      and coalesce(t.status,'0') <> '2')) then
    begin
        execute procedure wh_ttid_select
         returning_values :ttid_select;

        if (not exists(select *
                         from wm_task t
                        where t.docid = :docid
                          and t.taskmethodid is NOT NULL
                          and t.tasktypeid = :ttid_select
                          and coalesce(t.status,'0') <> '2')) then
        UPDATE wm_task t
           set t.status = '2',t.endtime = current_timestamp
         where t.taskid = :tid_loadauto;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECT_CLIENTUNFUND (
    taskid type of column wm_task.taskid
)
as
declare variable whid type of column OBJECT.objid ;
declare variable clientid type of column OBJECT.objid ;
declare variable docid type of column DOCUMENT.docid ;
begin
   select d.fromobj, d.toobj, d.docid
     from wm_task t
          left join document d on d.docid = t.docid
    where t.taskid = :taskid
     into :whid, :clientid, :docid;

   insert into wh_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
   select :docid, tw.waresid, tw.plandatetime, -tw.quantity, :whid, :clientid
     from wm_task_wares tw
    where tw.taskid = :taskid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_TASKEND (
    TID_LOADPALLET R_ID)
AS
declare variable tid_loadauto r_id;
declare variable tid_gateauto r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_CARDOCS r_id;
declare variable tpriority r_number;
declare variable palid_select r_id;
declare variable tbtid_loadselect r_id;
declare variable wlotid r_id;
declare variable wlincomeid r_id;
declare variable waresid r_id;
declare variable taskwaresid r_id;
declare variable wmsessionid r_id;
declare variable amount r_double;
declare variable docid r_id64;
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable taskid_select type of column wm_task.taskid;
begin
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'DOCPALLETS'
      into :tbtid_docpallets;

    select t.taskid,t.priority,t.docid
      from wh_taskbond tb
           left join wm_task t on t.taskid = tb.task1id
     where tb.task2id = :tid_loadpallet
       and tb.taskbondtid = :tbtid_docpallets
      into :tid_loadauto,:tpriority,:docid;

    if (:tpriority is NOT NULL) then
    begin
        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'CARDOCS'
          into :tbtid_CARDOCS;
    
        select t.taskid
          from wh_taskbond tb
               left join wm_task t on t.taskid = tb.task1id
         where tb.task2id = :tid_loadauto
           and tb.taskbondtid = :tbtid_cardocs
          into :tid_gateauto;

        if (exists(select *
                     from wh_taskbond tb
                          left join wm_task t
                               left join wh_taskbond tb2
                                    left join wm_task t2 on t2.taskid = tb2.task2id
                                 on tb2.task1id = t.taskid and tb2.taskbondtid = :tbtid_docpallets
                            on t.taskid = tb.task2id
                    where tb.task1id = :tid_gateauto
                      and tb.taskbondtid = :tbtid_cardocs
                      and t.priority is NOT NULL and t.priority < :tpriority
                      and t2.taskid is NOT NULL and t2.status <> '2' )) then
            exception exc_k_common 'Подождите, есть поддоны, которые должны быть загружены раньше вашего!';

    end

    -- Возможно нужно списать остатки
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'LOADSELECT'
      into :tbtid_loadselect;

    select ps.palletid, t.taskid
      from wh_taskbond tb
           left join wm_task t
                left join pallet_select ps on ps.taskid = t.taskid
             on t.taskid = tb.task2id
     where tb.task1id = :tid_loadpallet
       and tb.taskbondtid = :tbtid_loadselect
      into :palid_select, :taskid_select;

    if (:palid_select is NOT NULL) then
    begin
        execute procedure WH_SELECT_CLIENTUNFUND(:taskid_select);

        select t.wm_sessionid
          from wm_task t
         where t.taskid = :tid_loadpallet
          into :wmsessionid;

        for
            select wli.wlotid,wli.wlincomeid,sum(wli.amount)
              from wareslotitem wli
             where wli.palletid = :palid_select
             group by wli.wlotid, wli.wlincomeid
             order by wli.wlotid, wli.wlincomeid nulls last
              into :wlotid, :wlincomeid, :amount
        do
        begin
            waresid = NULL;
            select wl.waresid
              from wareslot wl
             where wl.wlotid = :wlotid
              into :waresid;

            taskwaresid = NULL;
            select tw.taskwaresid
              from wm_task_wares tw
             where tw.taskid = :tid_loadpallet
               and tw.waresid = :waresid
              into :taskwaresid;
            if (:taskwaresid is NULL) then
                insert into wm_task_wares(taskid, waresid, status, wm_sessionid, begintime)
                values(:tid_loadpallet, :waresid, '1', :wmsessionid, current_timestamp)
                returning taskwaresid
                into :taskwaresid;

            insert into wm_task_lot(taskwaresid, wlotid, palletid, wlincomeid,  quantity, chgwli)
            values(:taskwaresid, :wlotid, :palid_select, :wlincomeid, -:amount, '1');

            update wm_task_wares tw
               set tw.status = '2',
                   tw.endtime = current_timestamp,
                   tw.quantity = coalesce(tw.quantity,0.000) + :amount
              where tw.taskwaresid = :taskwaresid;
        end
    end

    -- Закрываем само задание на погрузку паллета в автомобиль
    UPDATE wm_task t
       set t.status = '2',t.endtime = current_timestamp
     where t.taskid = :tid_loadpallet;

    -- Закрыть задание на погрузку документа в машину
    if (not exists(select *
                     from wh_taskbond tb
                          left join wm_task t on t.taskid = tb.task2id
                    where tb.task1id = :tid_loadauto
                      and tb.taskbondtid = :tbtid_docpallets
                      and coalesce(t.status,'0') <> '2')) then
    begin
        execute procedure wh_ttid_select
         returning_values :ttid_select;

        if (not exists(select *
                         from wm_task t
                        where t.docid = :docid
                          and t.taskmethodid is NOT NULL
                          and t.tasktypeid = :ttid_select
                          and coalesce(t.status,'0') <> '2')) then
        UPDATE wm_task t
           set t.status = '2',t.endtime = current_timestamp
         where t.taskid = :tid_loadauto;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECT_CLIENTUNFUND (
    taskid type of column wm_task.taskid
)
as
declare variable clientid type of column OBJECT.objid;
declare variable fundobjid type of column OBJECT.objid;
declare variable docid type of column DOCUMENT.docid ;
begin
   select gor.objid, d.toobj, d.docid
     from wm_task t
          left join document d
               left join wh_get_reserveobj(coalesce(d.throughobj, d.fromobj)) gor on 1=1
            on d.docid = t.docid
    where t.taskid = :taskid
     into :fundobjid, :clientid, :docid;

   insert into wh_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
   select :docid, tw.waresid, tw.plandatetime, -tw.quantity, :fundobjid, :clientid
     from wm_task_wares tw
    where tw.taskid = :taskid;

   insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
   select :docid, tw.waresid, tw.plandatetime, -tw.quantity, :fundobjid
     from wm_task_wares tw
    where tw.taskid = :taskid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_LOADPALLETDC_TASKEND (
    TID_LOADPALLET R_ID)
AS
declare variable tid_loadauto r_id;
declare variable tid_gateauto r_id;
declare variable tbtid_docpallets r_id;
declare variable tbtid_CARDOCS r_id;
declare variable tpriority r_number;
declare variable palid_select r_id;
declare variable tbtid_loadselect r_id;
declare variable wlotid r_id;
declare variable wlincomeid r_id;
declare variable waresid r_id;
declare variable taskwaresid r_id;
declare variable wmsessionid r_id;
declare variable amount r_double;
declare variable docid r_id64;
declare variable ttid_select type of column wm_tasktype.tasktypeid;
declare variable taskid_select type of column wm_task.taskid;
begin
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'DOCPALLETS'
      into :tbtid_docpallets;

    select t.taskid,t.priority,t.docid
      from wh_taskbond tb
           left join wm_task t on t.taskid = tb.task1id
     where tb.task2id = :tid_loadpallet
       and tb.taskbondtid = :tbtid_docpallets
      into :tid_loadauto,:tpriority,:docid;

    if (:tpriority is NOT NULL) then
    begin
        select tbt.id
          from wh_taskbondtype tbt
         where tbt.code = 'CARDOCS'
          into :tbtid_CARDOCS;
    
        select t.taskid
          from wh_taskbond tb
               left join wm_task t on t.taskid = tb.task1id
         where tb.task2id = :tid_loadauto
           and tb.taskbondtid = :tbtid_cardocs
          into :tid_gateauto;

        if (exists(select *
                     from wh_taskbond tb
                          left join wm_task t
                               left join wh_taskbond tb2
                                    left join wm_task t2 on t2.taskid = tb2.task2id
                                 on tb2.task1id = t.taskid and tb2.taskbondtid = :tbtid_docpallets
                            on t.taskid = tb.task2id
                    where tb.task1id = :tid_gateauto
                      and tb.taskbondtid = :tbtid_cardocs
                      and t.priority is NOT NULL and t.priority < :tpriority
                      and t2.taskid is NOT NULL and t2.status <> '2' )) then
            exception exc_k_common 'Подождите, есть поддоны, которые должны быть загружены раньше вашего!';

    end

    -- Возможно нужно списать остатки
    select tbt.id
      from wh_taskbondtype tbt
     where tbt.code = 'LOADSELECT'
      into :tbtid_loadselect;

    select ps.palletid, t.taskid
      from wh_taskbond tb
           left join wm_task t
                left join pallet_select ps on ps.taskid = t.taskid
             on t.taskid = tb.task2id
     where tb.task1id = :tid_loadpallet
       and tb.taskbondtid = :tbtid_loadselect
      into :palid_select, :taskid_select;

    if (:palid_select is NOT NULL) then
    begin
        execute procedure WH_SELECT_CLIENTUNFUND(:taskid_select);

        select t.wm_sessionid
          from wm_task t
         where t.taskid = :tid_loadpallet
          into :wmsessionid;

        for
            select wli.wlotid,wli.wlincomeid,sum(wli.amount)
              from wareslotitem wli
             where wli.palletid = :palid_select
             group by wli.wlotid, wli.wlincomeid
             order by wli.wlotid, wli.wlincomeid nulls last
              into :wlotid, :wlincomeid, :amount
        do
        begin
            waresid = NULL;
            select wl.waresid
              from wareslot wl
             where wl.wlotid = :wlotid
              into :waresid;

            taskwaresid = NULL;
            select tw.taskwaresid
              from wm_task_wares tw
             where tw.taskid = :tid_loadpallet
               and tw.waresid = :waresid
              into :taskwaresid;
            if (:taskwaresid is NULL) then
                insert into wm_task_wares(taskid, waresid, status, wm_sessionid, begintime)
                values(:tid_loadpallet, :waresid, '1', :wmsessionid, current_timestamp)
                returning taskwaresid
                into :taskwaresid;

            insert into wm_task_lot(taskwaresid, wlotid, palletid, wlincomeid,  quantity, chgwli)
            values(:taskwaresid, :wlotid, :palid_select, :wlincomeid, -:amount, '1');

            update wm_task_wares tw
               set tw.status = '2',
                   tw.endtime = current_timestamp,
                   tw.quantity = coalesce(tw.quantity,0.000) + :amount
              where tw.taskwaresid = :taskwaresid;
        end
    end

    -- Закрываем само задание на погрузку паллета в автомобиль
    UPDATE wm_task t
       set t.status = '2',t.endtime = current_timestamp
     where t.taskid = :tid_loadpallet;

    -- Закрыть задание на погрузку документа в машину
    if (not exists(select *
                     from wh_taskbond tb
                          left join wm_task t on t.taskid = tb.task2id
                    where tb.task1id = :tid_loadauto
                      and tb.taskbondtid = :tbtid_docpallets
                      and coalesce(t.status,'0') <> '2')) then
    begin
        execute procedure wh_ttid_select
         returning_values :ttid_select;

        if (not exists(select *
                         from wm_task t
                        where t.docid = :docid
                          and t.taskmethodid is NOT NULL
                          and t.tasktypeid = :ttid_select
                          and coalesce(t.status,'0') <> '2')) then
        UPDATE wm_task t
           set t.status = '2',t.endtime = current_timestamp
         where t.taskid = :tid_loadauto;
    end
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECT_CLIENTUNFUND (
    taskid type of column wm_task.taskid
)
as
declare variable clientid type of column OBJECT.objid;
declare variable fundobjid type of column OBJECT.objid;
declare variable docid type of column DOCUMENT.docid ;
begin
   select gor.objid, d.toobj, d.docid
     from wm_task t
          left join document d
               left join wh_get_reserveobj(coalesce(d.throughobj, d.fromobj)) gor on 1=1
            on d.docid = t.docid
    where t.taskid = :taskid
     into :fundobjid, :clientid, :docid;

/*   insert into wh_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
   select :docid, tw.waresid, tw.plandatetime, -tw.quantity, :fundobjid, :clientid
     from wm_task_wares tw
    where tw.taskid = :taskid;*/

   insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
   select :docid, tw.waresid, tw.plandatetime, -tw.quantity, :fundobjid
     from wm_task_wares tw
    where tw.taskid = :taskid;
end^

SET TERM ; ^



SET TERM ^ ;

CREATE OR ALTER procedure WH_SELECT_CLIENTUNFUND (
    taskid type of column wm_task.taskid
)
as
declare variable clientid type of column OBJECT.objid;
declare variable fundobjid type of column OBJECT.objid;
declare variable docid type of column DOCUMENT.docid ;
begin
   select gor.objid, d.toobj, d.docid
     from wm_task t
          left join document d
               left join wh_get_reserveobj(coalesce(d.throughobj, d.fromobj)) gor on 1=1
            on d.docid = t.docid
    where t.taskid = :taskid
     into :fundobjid, :clientid, :docid;

   insert into wh_reserve_client_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID, CLIENTID)
   select :docid, tw.waresid, tw.plandatetime, -tw.quantity, :fundobjid, :clientid
     from wm_task_wares tw
    where tw.taskid = :taskid;

   insert into wh_reserve_changes ( DOCID, WARESID, PRODUCTDATE, AMOUNT, OBJID)
   select :docid, tw.waresid, tw.plandatetime, -tw.quantity, :fundobjid
     from wm_task_wares tw
    where tw.taskid = :taskid;
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

        exception exc_wh_wrongamount 'Не верные данные по резерву у товара с кодом' || :wcode;
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



SET TERM ^ ;

create or alter procedure K_U3S_LOADAUTO_TSTCHG (
    TASKID type of R_ID64,
    OLDSTAT type of R_STATUS,
    NEWSTAT type of R_STATUS)
AS
declare variable TTCODE type of R_CODE;
declare variable DOCID type of R_ID64;
declare variable TMALGO type of R_FLAG;
begin
    select tt.code, t.docid
      from wm_task t
           left join wm_tasktype tt on tt.tasktypeid=t.tasktypeid
     where t.taskid = :taskid
      into :ttcode, :docid;

    if (:ttcode <> 'LOADAUTO') then
        exception exc_k_wrongtasktype;

    if (:oldstat = '2') then
    begin
        if (:newstat <> :oldstat) then
            exception exc_k_common 'Попытка произвести не санкционированную операцию!';
    end

    if (:newstat = '2') then
        update document d
           set d.status = 'e',d.docdate = current_timestamp
         where d.docid = :docid;

end^

SET TERM ; ^

