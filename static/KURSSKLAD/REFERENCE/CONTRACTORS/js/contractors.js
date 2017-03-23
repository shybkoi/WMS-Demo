include(eng_js+'/options.js');
$(function(){
    function GetContractors(getfile){
        var stext = $('#stext').val();
        var status = $('#status').val();
        var statusname = $('#status option:selected').text();
        Block('Загрузка контрагентов...',1);
        $.getJSON('GetContractors',{getfile:getfile, stext:stext, status:status, statusname:statusname},function(data){
            if (!showErr(data)){
                if(getfile){if(data.ext_data.linkfile) location.href = data.ext_data.linkfile;}
                else{
                    var table = QHTable({tid:'contractors',
                             thead:['№','Ст.','Код','Наименование','ИНН','Код ОКПО','СН','БИК','ОГРН','Дата регистрации', 'Руководитель', 'Телефон руководителя'],
                             theadtitle:['','статус контрагента','код контрагента','наименование контрагента','Идентификационный номер налогоплательщика','Код Общеукраинский классификатор предприятий и организаций','№ свидетельства налогоплательщика','Банковский идентификационный код','Основной государственный регистрационный номер','Дата регистрации', 'Руководитель', 'Телефон реководителя'],
                             tbodytitle:['','STATUSNAME','','','','','','','','','','',],
                             tbody:['Num','STATUS','CODE','NAME','INN','OKPO','KPP','BIK','OGRP','REGDATE', 'CHIEF', 'PHONECHIEF'],
                             tclass:['Num','<img>ObjectStatus', 'Code', 'Name','INN','OKPO','KPP','BIK','OGRP','RegDate', 'Chief', 'PhoneChief'],
                             trid:['C','COMPID'],
                             data:data,
                            });
                    $('#div-contractors').html(table).QHxscroll();
                    ContractorsInit();
                }
            }
            UnBlock();
        });
    }
    function ContractorsInit(){
        $('#contractors').QHTableInit({width: '100%',
                            height: '300',
                            ts:['i','t'],
                            sc :'kScrollableToDown',
                            cm: CMContractors,
                        });
    }
    function CMContractors(id){
        $("#"+id).contextMenu({menu: 'cm-contractors'},
            function(action, el, pos){
                if (action=='add'){ AddContractor(false, 'dlg-addcontractors');}
                if (action=='edit'){ AddContractor(el.attr('id').split('-')[1], 'dlg-addcontractors');}
                if (action=='delete'){ DeleteContractor(el.attr('id').split('-')[1]);}
                if (action=='reload'){ GetContractors();}
                if (action=='excel'){ GetContractors(1);}
                if (action=='req'){ GetReq(el);}
                if (action=='bond'){ Bond(el);}
                if (action=='palfeature'){ palfeature(el);}
        });
    }
    function AddContractor(compid, dlgclass){
        dlg = $('#'+dlgclass);
        if(!dlg.length){
            QHCreateDialog(dlgclass, null, sp_forms+'/AddContractor.html', {height: 490,
                  width: 810,
                  title: "Добавление контрагента",
                  }, function(){
                    $('input.RegDate',$('#'+dlgclass)).QHDatePicker({value:getToday()});
                    $('input.Date1,input.Date2',$('#'+dlgclass)).QHDatePicker();
                    $('a.edit',$('#'+dlgclass)).QHbind('click', function(){EditAddress(dlgclass, $(this));});
                    $('button.accounts',$('#'+dlgclass)).QHbind('click', function(){Accounts(dlgclass);});
                    $('button.groups',$('#'+dlgclass)).QHbind('click', Groups);
                    $('button.brands',$('#'+dlgclass)).QHbind('click', function(){Brands(dlgclass);});
                    $('button.typeactivity',$('#'+dlgclass)).QHbind('click', TypeActivity);
                    $('button.save',$('#'+dlgclass)).QHbind('click', function(){ContractorAddEdit(dlgclass);});
                    $('a.copy',$('#'+dlgclass)).QHbind('click', function(){CopyAddress(dlgclass, $(this));});
                    $('a.delete',$('#'+dlgclass)).QHbind('click', function(){DelAddress($(this), dlgclass);});
                    $('input.Higher',$('#'+dlgclass)).kObjLocate({hiddenName:'higherobj',dvId:"dvHigherObj",title:'Объект',destroyDvIfExists:true});
                    AddContractorDlg(compid, dlgclass);});
        }
        else{
            AddContractorDlg(compid, dlgclass);
        }
    }
    function ContractorAddEdit(dlgclass){
        var dlg = $('#'+dlgclass);
        var contid = dlg.attr('compid');
        var name = dlg.find('input.Name').val();
        var code = dlg.find('input.Code').val();
        var adress = dlg.find('input.Address').attr('id');
        var realadress = dlg.find('input.RealAddress').attr('id');
        var inn = dlg.find('input.INN').val();
        var innone = (dlg.find('input.INNONE:checked').length==1)?'1':'0';
        var okpo = dlg.find('input.OKPO').val();
        var okpoone = (dlg.find('input.OKPOONE:checked').length==1)?'1':'0';
        var bik = dlg.find('input.BIK').val();
        var bikone = (dlg.find('input.BIKONE:checked').length==1)?'1':'0';
        var chief = dlg.find('input.Chief').val();
        var phonechief = dlg.find('input.PhoneChief').val();
        var mainacc = dlg.find('input.MainAcc').val();
        var phonema = dlg.find('input.PhoneMA').val();
        var ogrp = dlg.find('input.OGRP').val();
        var ogrpone = (dlg.find('input.OGRPONE:checked').length==1)?'1':'0';
        var regdate = dlg.find('input.RegDate').val();
        var status = dlg.find('input.Status').val();
        var higher = dlg.find('input[name="higherobj"]').val()=='null'?'':dlg.find('input[name="higherobj"]').val();
        var descript = dlg.find('textarea.Descript').val();
        var date1 = dlg.find('input.Date1').val();
        var date2 = dlg.find('input.Date2').val();
        var kpp = dlg.find('input.KPP').val();
        var isbank = ($('input.Bank:checked',dlg).length == 1)?'1':'0';
        $.getJSON('ajaxAddEditContractor',{
            contid: contid,
            name: name,
            code: code,
            adress: adress,
            realadress: realadress,
            inn: inn,
            innone: innone,
            okpo: okpo,
            okpoone: okpoone,
            bik: bik,
            bikone: bikone,
            chief: chief,
            phonechief: phonechief,
            mainacc: mainacc,
            phonema: phonema,
            ogrp: ogrp,
            ogrpone: ogrpone,
            regdate: regdate,
            status: status,
            higher: higher,
            descript: descript,
            date1: date1,
            date2: date2,
            kpp: kpp,
            isbank: isbank},
            function(data){
                if(data.data.MES!='')
                    alert(data.data.MES);
                else
                {
                    if(dlgclass == 'dlg-add-bank'){
                        var acc = $('#dlg-accounts');
                        if(!contid){
                            $('select.Bank', acc).append('<option selected="selected" value="'+data.data.COMPID+'">'+name+'</option>');
                        }
                        else{
                            $('select.Bank option:selected', acc).text(name);
                        }
                    }
                    else{
                        if(!contid){
                            $('#stext').val(name);
                            $('#status').val(status);
                        }
                        GetContractors();
                    }
                    dlg.dialog('close');
                }
        });
    }
    function AddContractorDlg(compid, dlgclass){
        var dlg = $('#'+dlgclass);
        $('input.Bank',dlg).removeAttr('disabled');
        if(compid){
            dlg.attr('compid', compid);
            $('button.accounts, button.groups, button.brands, button.typeactivity', dlg).removeAttr('disabled');
            if(dlgclass == 'dlg-add-bank'){
                $('button.accounts, button.groups, button.brands, button.typeactivity', dlg).attr('disabled','disabled');
            }
            $.ajax({url: 'ajaxGetContractor',
                data: {compid: compid},
                dataType: 'json',
                async: false,
                success: function(res){
                    PrepareUpdate(res, dlgclass);
                }
            });
        }
        else{
            $('#'+dlgclass).removeAttr('compid');
            $('button.accounts, button.groups, button.brands, button.typeactivity', dlg).attr('disabled','disabled');
            PrepareUpdate(false, dlgclass);
        }
        if(dlgclass == 'dlg-add-bank')
            $('input.Bank',dlg).attr('checked','checked').attr('disabled','disabled');
        var dlg = $('#'+dlgclass);
        dlg.QHdialogOH();
    }
    function PrepareUpdate(res, dlgclass){
        var dlg = $('#'+dlgclass);
        var upd = (res)?true:false;
        dlg.find('input').removeAttr('checked');
        dlg.find('input.Name').val(((upd)?res.data.NAME:''));
        dlg.find('input.Code').val(((upd)?res.data.CODE:''));
        dlg.find('input.Address').attr('id',((upd)?res.data.ADDRESS:'')).val('');
        if(upd)
            if(res.data.ADDRESS!='')
                GetAddress(res.data.ADDRESS, 'Address', dlgclass);
        dlg.find('input.RealAddress').attr('id',((upd)?res.data.REALADDRESS:'')).val('');
        if(upd)
            if(res.data.REALADDRESS!='')
                GetAddress(res.data.REALADDRESS, 'RealAddress', dlgclass);
        dlg.find('input.INN').val(((upd)?res.data.INN:''));
        if(upd){
            if(res.data.INNONE == '1')
                dlg.find('input.INNONE').attr('checked','checked');
            else
                dlg.find('input.INNONE').removeAttr('checked');
        }
        dlg.find('input.OKPO').val(((upd)?res.data.OKPO:''));
        //var okpoone = (dlg.find('input.OKPOONE:checked').length==1)?'1':'0';
        if(upd)
        if(res.data.OKPOONE == '1')
            dlg.find('input.OKPOONE').attr('checked','checked');
        else
            dlg.find('input.OKPOONE').removeAttr('checked');
        dlg.find('input.BIK').val(((upd)?res.data.BIK:''));
        //var bikone = (dlg.find('input.BIKONE:checked').length==1)?'1':'0';
        if(upd){
            if(res.data.BIKONE == '1')
                dlg.find('input.BIKONE').attr('checked','checked');
            else
                dlg.find('input.BIKONE').removeAttr('checked');
        }
        dlg.find('input.Chief').val(((upd)?res.data.CHIEF:''));
        dlg.find('input.PhoneChief').val(((upd)?res.data.PHONECHIEF:''));
        dlg.find('input.MainAcc').val(((upd)?res.data.MAINACC:''));
        dlg.find('input.PhoneMA').val(((upd)?res.data.PHONEMA:''));
        dlg.find('input.OGRP').val(((upd)?res.data.OGRP:''));
        //var ogrpone = (dlg.find('input.OGRPONE:checked').length==1)?'1':'0';
        if(upd){
            if(upd && res.data.OGRPONE == '1')
                dlg.find('input.OGRPONE').attr('checked','checked');
            else
                dlg.find('input.OGRPONE').removeAttr('checked');
        }
        dlg.find('input.RegDate').val(((upd)?res.data.REGDATE:''));
        dlg.find('input.Status').val(((upd)?res.data.STATUS:''));
        dlg.find('input.Higher').val(((upd)?res.data.HIGHERNAME:''));
        dlg.find('[name="higherobj"]').val(((upd)?res.data.HIGHER:'null'));
        dlg.find('textarea.Descript').val(((upd)?res.data.DESCRIPT:''));
        dlg.find('textarea.Descript').val(((upd)?res.data.DESCRIPT:''));
        //var date1 = dlg.find('input.Date1').val();
        //var date2 = dlg.find('input.Date2').val();
        dlg.find('input.KPP').val(((upd)?res.data.KPP:''));
    }
    function EditAddress(dlgclass, th){
        var aclass = th.closest('div').find('input').attr('class');
        var addressid = th.closest('div').find('input').attr('id');
        dlg = $('#dlg-editaddress-'+dlgclass);
        if(!dlg.length){
            QHCreateDialog('dlg-editaddress-'+dlgclass, null, sp_forms+'/EditAddress.html', {height: 260,
                  width: 610,
                  title: "Изменение адреса",
                  }, function(){
                    $('select.Countryid,select.State,select.Rayon,select.City,select.Street',$('#dlg-editaddress-'+dlgclass)).jec({blinkingCursor: true, blinkingCursorInterval: 500, acceptedKeys: [[32, 126], [191, 382], [1040, 1106]]});
                    EditAddressDlg(aclass, addressid, dlgclass);});
        }
        else{
            EditAddressDlg(aclass, addressid, dlgclass);
        }
    }
    function EditAddressDlg(aclass, addressid, dlgclass){
        var dlg = $('#dlg-editaddress-'+dlgclass);
        var mode = (addressid=='' || addressid==undefined)?'i':'u';
        var data = {};
        var country = '';
        var reg = '';
        var ci = '';
        var ray = '';
        var st = '';
        if(mode == 'u')
        {
            data = GetAddressFull(addressid, aclass, dlgclass);
            dlg.find('input.PostIndex').val(data.PostIndex);
            dlg.find('input.OKATO').val(data.OKTO);
            dlg.find('input.StateCode').val(data.StateCode);
            dlg.find('input.House').val(data.House);
            dlg.find('input.Building').val(data.Building);
            dlg.find('input.Room').val(data.Room);
            country = data.CountryId;
            reg = data.State;
            ci = data.City;
            ray = data.Rayon;
            st = data.Street;
        }
        else{
            dlg.find('input.PostIndex').val('');
            dlg.find('input.OKATO').val('');
            dlg.find('input.StateCode').val('');
            dlg.find('input.House').val('');
            dlg.find('input.Building').val('');
            dlg.find('input.Room').val('');
        }
        $.ajax({url:'ajaxCountrySel',
                data:{},
                dataType: 'json',
                ajax: false,
                success:function(res){
            var select = dlg.find('select.Countryid');
            select.find('option').not('.jecEditableOption').remove()
            for(var i=0;i<res.data.length;++i)
            {
                select.append('<option value="'+
                              res.data[i].COUNTRYID+'" '
                              +((res.data[i].FULLNAME == 'Украина' && country == '')?'selected':'')+'>'+
                              res.data[i].FULLNAME+'</option>')
            }
            if(mode == 'u')
                select.val(country);
            select.unbind('change').change(function(){
                var option = $(this).find('option:selected');
                $.ajax({url:'ajaxRegionSel',
                        data:{country: option.val()},
                        dataType:'json',
                        ajax: false,
                        success: function(res){
                            var region = dlg.find('select.State');
                            region.find('option').not('.jecEditableOption').remove();
                            for(var i=0;i<res.data.length;++i)
                            {
                                region.append('<option value="'+
                                res.data[i].STATE+'">'+
                                res.data[i].STATE+'</option>');
                            }
                            if(mode == 'u')
                                region.val(reg);
                                //region.find('option[value="'+reg+'"]').attr('selected','selected');
                            else
                                region.find('option').eq(1).attr('selected','selected');
                            region.unbind('change').change(function(){
                                var city = dlg.find('select.City');
                                $.ajax({url:'ajaxCitySel',
                                        data:{state: region.find('option:selected').val()},
                                        dataType: 'json',
                                        ajax: false,
                                        success: function(res){
                                            city.find('option').not('.jecEditableOption').remove();
                                            for(var i=0;i<res.data.length;++i)
                                            {
                                                city.append('<option value="'+
                                                             res.data[i].CITY+'">'+
                                                             res.data[i].CITY+'</option>');
                                            }
                                            if(mode == 'u')
                                                city.val(ci);
                                            else
                                                city.find('option').eq(1).attr('selected','selected');
                                            city.unbind('change').change(function(){
                                                var rayon = dlg.find('select.Rayon');
                                                $.ajax({url:'ajaxRayonSel',
                                                        data:{state: city.find('option:selected').val()},
                                                        dataType: 'json',
                                                        ajax: false,
                                                        success: function(res){
                                                            rayon.find('option').not('.jecEditableOption').remove();
                                                            for(var i=0;i<res.data.length;++i)
                                                            {
                                                                rayon.append('<option value="'+
                                                                             res.data[i].RAYON+'">'+
                                                                             res.data[i].RAYON+'</option>');
                                                            }
                                                            if(mode == 'u')
                                                                rayon.val(ray);
                                                            else
                                                                rayon.find('option').eq(1).attr('selected','selected');
                                                            rayon.unbind('change').change(function(){
                                                                var street = dlg.find('select.Street');
                                                                $.ajax({url:'ajaxStreetSel',
                                                                        data:{street: rayon.find('option:selected').val()},
                                                                        dataType: 'json',
                                                                        ajax: false,
                                                                        success: function(res){
                                                                            street.find('option').not('.jecEditableOption').remove();
                                                                            for(var i=0;i<res.data.length;++i)
                                                                            {
                                                                                street.append('<option value="'+
                                                                                             res.data[i].STREET+'">'+
                                                                                             res.data[i].STREET+'</option>');
                                                                            }
                                                                            if(mode == 'u')
                                                                                street.val(st);
                                                                            else
                                                                                street.find('option').eq(1).attr('selected','selected');
                                                                        }})
                                                            }).change();
                                                        }})
                                            }).change();
                                        }})
                            }).change();
                        }})
            }).change();
        }});
        dlg.find('button.save').unbind('click').click(function(){
            AddEditAddress(dlg, mode, aclass, dlgclass);
        });
        dlg.QHdialogOH();
    }
    function AddEditAddress(dlg, mode, aclass, dlgclass){
        //console.log('aclass='+aclass+' dlgclass='+dlgclass);
        var PostIndex = dlg.find('input.PostIndex').val();
        var OKATO = dlg.find('input.OKATO').val();
        var Countryid = dlg.find('select.Countryid').val();
        var State = dlg.find('select.State').val();
        var StateCode = dlg.find('input.StateCode').val();
        var City = dlg.find('select.City').val();
        var Rayon = dlg.find('select.Rayon').val();
        var Street = dlg.find('select.Street').val();
        var House = dlg.find('input.House').val();
        var Building = dlg.find('input.Building').val();
        var Room = dlg.find('input.Room').val();
        $.getJSON('ajaxAddEditAddress',
                  {AddId:$('#'+dlgclass).find('input.'+aclass).attr('id'),
                  PostIndex: PostIndex,
                  OKATO: OKATO,
                  Countryid: Countryid,
                  State: State,
                  StateCode: StateCode,
                  City: City,
                  Rayon: Rayon,
                  Street: Street,
                  House: House,
                  Building: Building,
                  Room: Room,
                  mode: mode},
                  function(res){
            GetAddress(res.data.NEWADDID, aclass, dlgclass);
            dlg.dialog('close');
        });
    }
    function GetAddress(addr, aclass, dlgclass){
        $.ajax({url: 'ajaxGetAddress',
                data: {addr: addr, mode: 'str'},
                dataType: 'json',
                async: false,
                success: function(res1){
                    $('#'+dlgclass)
                        .find('input.'+aclass)
                        .attr('id', addr)
                        .attr('value',res1.data.STRING);
                }});
    }
    function GetAddressFull(addr, aclass, dlgclass){
        var lst = {};
        $.ajax({url: 'ajaxGetAddress',
            data: {addr: addr, mode: 'full'},
            dataType: 'json',
            async: false,
            success: function(res){
                var dlg = $('#dlg-editaddress-'+dlgclass);
                lst = {
                    'CountryId' : res.data.COUNTRYID,
                    'PostIndex' : res.data.POSTINDEX,
                    'OKATO' : res.data.OKATO,
                    'State' : res.data.STATE,
                    'StateCode' : res.data.STATECODE,
                    'City' : res.data.CITY,
                    'Rayon' : res.data.RAYON,
                    'Street' : res.data.STREET,
                    'House' : res.data.HOUSE,
                    'Building' : res.data.BUILDING,
                    'Room' : res.data.ROOM
                }
            }});
        return lst;
    }
    function CopyAddress(dlgclass, th){
        var fromclass = th.closest('div').find('input').attr('class');
        var addressid = th.closest('div').find('input').attr('id');
        var destclass = (fromclass == 'Address')?'RealAddress':'Address';
        var toaddressid = $('input.'+destclass).attr('id');
        if(addressid=='')
            return;
        $.ajax({url: 'ajaxCopyAddress',
            data: {fromid: addressid, toid: toaddressid},
            dataType: 'json',
            async: false,
            success: function(res){
                GetAddress(res.data.RESULT, destclass, dlgclass);
            }});
    }
    function DelAddress(th, dlgclass){
        var aclass = th.closest('div').find('input').attr('class');
        var addressid = th.closest('div').find('input').attr('id');
        if(addressid == '')
            return;
        if(confirm('Вы действительно хотите удалить адрес?')){
            $.ajax({url: 'ajaxDelAddress',
                data: {addr: addressid},
                dataType: 'json',
                async: false,
                success: function(res){
                    $('input.'+aclass,'#'+dlgclass).val('').removeAttr('id');
                }
            });
        }
    }
    function Accounts(dlgclass){
        var compid = $('#contractors').rfGetFocus().split('-')[1];
        dlg = $('#dlg-accounts');
        if(!dlg.length){
            QHCreateDialog('dlg-accounts', null, sp_forms+'/Accounts.html', {height: 460,
                  width: 600,
                  title: "Банковские счета контрагента",
                  }, function(){
                    $('div.actions a.edit, div.actions a.add',$('#dlg-accounts')).QHbind('click', function(){EditAccount(dlgclass, $(this));});
                    $('div.actions a.delete',$('#dlg-accounts')).QHbind('click', DelAccount);
                    $('input.OpenDate, input.CloseDate',$('#dlg-accounts')).QHDatePicker({value:getToday()});
                    AccountsDlg(compid);});
        }
        else{
            AccountsDlg(compid);
        }
    }
    function AccountsDlg(compid,getfile){
        var dlg = $('#dlg-accounts');
        $.getJSON('GetBankAccounts',{compid:compid, getfile:getfile},function(data){
            if(!showErr(data)){
                var table = QHTable({tid:'bankaccounts',
                         thead:['№','Банк','Основной','Дата открытия','Дата закрытия','Номер счета','Тип'],
                         theadtitle:['№','Банк','Основной','Дата открытия','Дата закрытия','Номер счета','Тип'],
                         tbodytitle:['','','','','','','',],
                         tbody:['Num','BANK','MAIN','OPENDATE','CLOSEDATE','BANKACCOUNT','BATYPE'],
                         tclass:['Num','Name','<img>Main', 'OpenDate', 'CloseDate','BankAccount','BAType'],
                         trid:['BA','BANKACCID'],
                         data:data,
                        });
                $('div.table',dlg).html(table).QHxscroll();
                AccountsInit();
                $('div.form-edit',dlg).hide();
                dlg.QHdialogOH();
            }
        });
    }
    function AccountsInit(){
        $('#bankaccounts').QHTableInit({width: '100%',
                            height: '200',
                            ts:['i','t','t','l','l','t','t'],
                        });
    }
    function EditAccount(dlgclass, th){
        var aclass = th.attr('class');
        var accid = (aclass == 'add'?null:$('#bankaccounts').rfGetFocus().split('-')[1]);
        var dlg = $('#dlg-accounts');
        $('select.Contractor option', dlg).remove();
        $('select.Contractor', dlg).attr('disabled','disabled').append('<option value="'+
                                           $('#contractors').rfGetFocus().split('-')[1]+'">'+
                                           $('#'+dlgclass+' input.Name').val()+'</option>');
        $.ajax({url: 'ajaxGetBanks',
            data: {},
            dataType: 'json',
            async: false,
            success: function(res){
                $('select.Bank option',dlg).remove();
                for(var i=0;i<res.data.length;++i){
                    $('select.Bank',dlg).append('<option value="'+
                                           res.data[i].COMPID+'">'+
                                           res.data[i].NAME+'</option>');
                }
            }
        });
        $.ajax({url: 'ajaxGetBAType',
            data: {},
            dataType: 'json',
            async: false,
            success: function(res){
                $('select.BAType option',dlg).remove();
                for(var i=0;i<res.data.length;++i){
                    $('select.BAType',dlg).append('<option value="'+
                                           res.data[i].CODE+'">'+
                                           res.data[i].NAME+'</option>');
                }
            }
        });
        $('button.save', dlg).QHbind('click', function(){AddEditAccount(accid, dlgclass);});
        $('div.Bank a.add, div.Bank a.edit', dlg).QHbind('click', function(){AddEditBank($(this));});
        if(accid){
            //console.log('edit')
            $.ajax({url: 'ajaxGetAccountById',
                data: {id: accid},
                dataType: 'json',
                async: false,
                success: function(res){
                    $('input.BankAccount',dlg).val(res.data.BANKACCOUNT);
                    $('select.Bank',dlg).val(res.data.BANK);
                    $('select.BAType',dlg).val(res.data.BATYPE);
                    $('input.OpenDate',dlg).val(res.data.OPENDATE);
                    $('input.CloseDate',dlg).val(res.data.CLOSEDATE);
                    if(res.data.MAIN == '1')
                        $('input.Main',dlg).attr('checked','checked');
                    else $('input.Main',dlg).removeAttr('checked');
                }
            });
        }
        else{
            //console.log('add');
            $('input.BankAccount',dlg).val('');
            $('input.OpenDate',dlg).val('');
            $('input.CloseDate',dlg).val('');
            $('input.Main',dlg).removeAttr('checked');
        }
        $('div.form-edit',dlg).show();
    }
    function AddEditBank(th){
        var dlg = $('#dlg-accounts');
        //alert(th.attr('class'))
        var compid = (th.attr('class')=='add')?false:$('select.Bank', dlg).val();
        var dlgclass = 'dlg-add-bank';
        AddContractor(compid, dlgclass)
    }
    function AddEditAccount(accid, dlgclass){
        var dlg = $('#dlg-accounts');
        $.getJSON('ajaxAddEditAccount',
                  {accid:accid,
                   Contractor:$('select.Contractor',dlg).val(),
                   Bank:$('select.Bank',dlg).val(),
                   Main:$('input.Main:checked',dlg).length,
                   OpenDate:$('input.OpenDate',dlg).val(),
                   CloseDate:$('input.CloseDate',dlg).val(),
                   BankAccount:$('input.BankAccount',dlg).val(),
                   BAType:$('select.BAType',dlg).val()},
            function(res){
                Accounts(dlgclass);
            }
        );
    }
    function DelAccount(dlgclass){
        if(confirm('Вы действительно хотите удалить счет ?')){
            accid = $('#dlg-accounts table#bankaccounts').rf$GetFocus().attr('id').split('-')[1];
            $.getJSON('ajaxDelAccount',{accid:accid}, function(res){
                if(res.data.OK == 'OK')
                    Accounts(dlgclass);
            }
        );
        }
    }
    function Groups(){
        var compid = $('#contractors').rfGetFocus().split('-')[1];
        dlg = $('#dlg-groups');
        if(!dlg.length){
            QHCreateDialog('dlg-groups', null, sp_forms+'/Groups.html', {height: 430,
                  width: 600,
                  title: "Вхождение в группы",
                  }, function(){
                    $('div.actions a.edit, div.actions a.add',$('#dlg-groups')).QHbind('click', EditGroup);
                    $('a.inobjcat, a.allinobjcat',$('#dlg-groups')).QHbind('click', InObjCat);
                    $('a.outobjcat, a.alloutobjcat',$('#dlg-groups')).QHbind('click', OutObjCat);
                    GroupsDlg(compid);});
        }
        else{
            GroupsDlg(compid);
        }
    }
    function GroupsDlg(compid){
        var dlg = $('#dlg-groups');
        $.getJSON('GetCategories',{compid:compid},function(data){
            if(!showErr(data)){
                var table = QHTable({tid:'category',
                         thead:['№','Группа'],
                         theadtitle:['№','Группа'],
                         tbodytitle:['',''],
                         tbody:['Num','NAME'],
                         tclass:['Num','Name'],
                         trid:['CATEGORY','CATID'],
                         data:data,
                        });
                $('div.category',dlg).html(table).QHxscroll();
                table = $('<table/>').attr('id','objcat')
                    .append($('<thead/>').append($('<tr/>')
                        .append($('<th/>').append('№'))
                        .append($('<th/>').append('Наименование'))
                    ))
                    .append($('<tbody/>'));
                var oc = 0;
                for(var i = 0;i<data.data.length;i++){
                    if(data.data[i]['OBJCATID'])
                        table.find('tbody').append($('<tr/>').attr('id','OBJCAT-'+data.data[i]['OBJCATID'])
                            .append($('<td/>').append(++oc))
                            .append($('<td/>').append(data.data[i]['NAME']))
                        );
                }
                $('div.objcat',dlg).html(table).QHxscroll();
                dlg.QHdialogOH();
                GroupsInit();
            }
        });
    }
    function GroupsInit(){
        $('#category').QHTableInit({width: '100%',
                            height: '300',
                            ts:['i','t'],
                        });
        $('#objcat').QHTableInit({width: '100%',
                            height: '300',
                            ts:['i','t'],
                        });
    }
    function EditGroup(){
        var aclass = $(this).attr('class');
        var catid = aclass=='add'?null:$('#category').rfGetFocus().split('-')[1];
        dlg = $('#dlg-editgroup');
        if(!dlg.length){
            QHCreateDialog('dlg-editgroup', null, sp_forms+'/EditGroup.html', {height: 290,
                  width: 400,
                  title: "Добавить/изменить группу",
                  }, function(){
                    $('div.actions a.edit, div.actions a.add',$('#dlg-editgroup')).QHbind('click', EditGroup);
                    EditGroupDlg(catid);});
        }
        else{
            EditGroupDlg(catid);
        }

    }
    function GetMultiSelectValue(){
        var results = '';
        $('div.multiSelectOptions :checked').each(function()
        {
            results = results + $(this).val() + ',';
        });
        results = results.substr(0,(results.length-1));
        return results;
    }
    function EditGroupDlg(catid){
        var dlg = $('#dlg-editgroup');
        $('select.Higher option', dlg).remove();
        $.ajax({url: 'ajaxGetTopCat',
            data: {},
            dataType: 'json',
            async: false,
            success: function(res){
                $('select.Higher', dlg).append('<option value="null"></option>');
                for(var i=0;i<res.data.length;++i){
                    $('select.Higher', dlg).append('<option value="'+
                            res.data[i].CATID+'">'+
                            res.data[i].NAME+'</option>');
                }
            }
        });
        var select = $('div.multiSelectOptions label');
        if(!select.length){
            $('select.ObjTypes option', dlg).remove();
            $.ajax({url: 'ajaxGetContType',
                data: {},
                dataType: 'json',
                async: false,
                success: function(res){
                    for(var i=0;i<res.data.length;++i){
                        $('select.ObjTypes', dlg).append('<option value="'+"'"+
                                res.data[i].CODE+"'"+'">'+
                                res.data[i].NAME+'</option>');
                    }
                }
            });
            $('select.ObjTypes', dlg).multiSelect({selectAll: false, selectAllText: 'Выбрать все', noneSelected:'Выберите типы', oneOrMoreSelected: 'Отмечено - %'});
        }
        $('div.multiSelectOptions :checkbox').attr('checked', false);
        $('INPUT.multiSelect').val('Выберите типы');
        if(!catid){
            $('input.Name',dlg).val('');
            $('input.Code',dlg).val('');
            $('input.ForOwner',dlg).attr('checked',false);
            dlg.QHdialogOH();
        }
        else{
            $.getJSON('GetCategoryInfo',{catid:catid},function(data){
                if(!showErr(data)){
                    $('input.Name',dlg).val(data.data.NAME);
                    $('input.Code',dlg).val(data.data.CODE);
                    $('select.Higher',dlg).val(data.data.HIGHER);
                    $('input.ForOwner',dlg).attr('checked',(data.data.FOROWNER == '1'?true:false));
                    var objs = data.data.OBJTYPES.split(',');
                    for(var i = 0; i<objs.length; i++)
                    {
                        $('div.multiSelectOptions :checkbox[value="'+objs[i]+'"]').attr('checked', true);
                    }
                    $('INPUT.multiSelect').val('Отмечено - '+$('div.multiSelectOptions :checked').length);
                    dlg.QHdialogOH();
                }
            });
        }
        $('button.save',dlg).QHbind('click', function(){GroupAddEdit(catid);});
    }
    function GroupAddEdit(catid){
        var dlg = $('#dlg-editgroup');
        $.getJSON('ajaxCategoryAddEdit',
                 {catid   : catid,
                  Name    : $('input.Name',dlg).val(),
                  Code    : $('input.Code',dlg).val(),
                  Higher  : $('select.Higher',dlg).val(),
                  ObjTypes: GetMultiSelectValue(),
                  ForOwner: $('input.ForOwner:checked',dlg).length},
                  function(data){
                    GroupsDlg($('#contractors').rfGetFocus().split('-')[1]);
                    dlg.dialog('close');
                  }
        );
    }
    function InObjCat(){
        var compid = $('#contractors').rfGetFocus().split('-')[1];
        var catid = $('#category').rfGetFocus().split('-')[1];
        var mass = ($(this).attr('class') == 'inobjcat')?false:true;
        var mes = (mass)?'во все группы':('в группу "'+$('#category').rf$GetFocus().find('td:eq(1)').text())+'"';
        if(confirm('Вы действительно хотите добавить '+mes+'?')){
            $.getJSON('ajaxInObjCat',
                 {catid: (mass)?'all':catid,
                  compid: compid},
                  function(data){
                    if(data.data.MES!='')
                        alert(data.data.MES);
                    GroupsDlg($('#contractors').rfGetFocus().split('-')[1]);
                  }
            );
        }
    }
    function OutObjCat(){
        var compid = $('#contractors').rfGetFocus().split('-')[1];
        var objcatid = $('#objcat').rfGetFocus().split('-')[1];
        var mass = ($(this).attr('class') == 'outobjcat')?false:true;
        var mes = (mass)?'из всех групп':('из группы "'+$('#objcat').rf$GetFocus().find('td:eq(1)').text())+'"';
        if(confirm('Вы действительно хотите удалить '+mes+'?')){
            $.getJSON('ajaxOutObjCat',
                 {objcatid: (mass)?'all':objcatid,
                  compid  : compid},
                  function(data){
                    if(data.data.MES!='')
                        alert(data.data.MES);
                    GroupsDlg($('#contractors').rfGetFocus().split('-')[1]);
                  }
            );
        }
    }
    function Brands(dlgclass){
        var compid = $('#contractors').rfGetFocus().split('-')[1];
        dlg = $('#dlg-brands');
        if(!dlg.length){
            QHCreateDialog('dlg-brands', null, sp_forms+'/Brands.html', {height: 430,
                  width: 600,
                  title: "Торговые марки контрагента",
                  }, function(){
                    $('div.actions a.edit, div.actions a.add',$('#dlg-brands')).QHbind('click', function(){EditBrand(dlgclass, $(this));});
                    $('div.actions a.delete',$('#dlg-brands')).QHbind('click', function(){DelBrand(dlgclass);});
                    BrandsDlg(compid);});
        }
        else{
            BrandsDlg(compid);
        }
    }
    function BrandsDlg(compid,getfile){
        var dlg = $('#dlg-brands');
        $.getJSON('GetBrands',{compid:compid, getfile:getfile},function(data){
            if(!showErr(data)){
                var table = QHTable({tid:'brands',
                         thead:['№','Наименование','Основная торговая марка'],
                         theadtitle:['№','Наименование','Основная торговая марка'],
                         tbodytitle:['','',''],
                         tbody:['Num','NAME','HIGHERNAME'],
                         tclass:['Num','Name','HigherName'],
                         trid:['BRAND','BRANDID'],
                         data:data,
                        });
                $('div.table',dlg).html(table).QHxscroll();
                BrandsInit();
                $('div.form-edit',dlg).hide();
                dlg.QHdialogOH();
            }
        });
    }
    function BrandsInit(){
        $('#brands').QHTableInit({width: '100%',
                            height: '200',
                            ts:['i','t','t'],
                        });
    }
    function EditBrand(dlgclass, th){
        var aclass = th.attr('class');
        var brandid = (aclass == 'add'?null:$('#brands').rfGetFocus().split('-')[1]);
        var compid = $('#contractors').rfGetFocus().split('-')[1];
        var dlg = $('#dlg-brands');
        $('select.Higher option', dlg).remove();
        $('select.Contractor option', dlg).remove();
        $('select.Contractor', dlg).attr('disabled','disabled').append('<option value="'+
                                           $('#contractors').rfGetFocus().split('-')[1]+'">'+
                                           $('#'+dlgclass+' input.Name').val()+'</option>');
        $('select.Higher', dlg).append('<option value="null"></option>');
        $.ajax({url: 'ajaxGetMainBrands',
                data: {objid: compid},
                dataType: 'json',
                async: false,
                success: function(res){
                    for(var i=0;i<res.data.length;++i)
                        if(res.data[i].BRANDID != brandid)
                            $('select.Higher', dlg).append('<option value="'+
                                                        res.data[i].BRANDID+'">'+
                                                        res.data[i].NAME+'</option>');
                }
            });
        if(brandid){
            $.ajax({url: 'ajaxGetBrandInfo',
                data: {brand: brandid, objid: compid},
                dataType: 'json',
                async: false,
                success: function(res){
                    $('input.Name', dlg).val(res.data.NAME);
                    $('select.Higher', dlg).val(res.data.HIGHER);
                }
            });
        }
        else{
            $('input.Name', dlg).val('');
            $('select.Higher', dlg).val('null');
        }
        $('button.save', dlg).QHbind('click', function(){AddEditBrand(brandid, dlgclass)});
        $('div.form-edit',dlg).show();
    }
    function AddEditBrand(brandid, dlgclass){
        var compid = $('#contractors').rfGetFocus().split('-')[1];
        var dlg = $('#dlg-brands');
        $.getJSON('ajaxBrandAddEdit',
            {brandid   : brandid,
             Name      : $('input.Name', dlg).val(),
             Higher    : $('select.Higher', dlg).val(),
             Contractor: $('select.Contractor', dlg).val()},
            function(data){
                Brands(dlgclass);
        });
    }
    function DelBrand(dlgclass){
        if(confirm('Вы действительно хотите удалить торговую марку "'+$('#brands').rf$GetFocus().find('td:eq(1)').text()+'"?')){
            var brand = $('#brands').rfGetFocus().split('-')[1];
            $.getJSON('ajaxBrandDel',{brand:brand},function(res){
                    if(res.data.MES =='')
                        Brands(dlgclass);
                    else
                        alert(res.data.MES);
            });
        }
    }
    function TypeActivity(){
        var compid = $('#contractors').rfGetFocus().split('-')[1];
        dlg = $('#dlg-typeactivity');
        if(!dlg.length){
            QHCreateDialog('dlg-typeactivity', null, sp_forms+'/TypeActivity.html', {height: 430,
                  width: 600,
                  title: "Виды деятельности",
                  }, function(){
                    $('div.actions a.edit, div.actions a.add',$('#dlg-typeactivity')).QHbind('click', EditTypeActivity);
                    $('div.actions a.delete',$('#dlg-typeactivity')).QHbind('click', DelTypeActivity);
                    $('input.LicDate1, input.LicDate2',$('#dlg-typeactivity')).QHDatePicker({value:getToday()});
                    TypeActivityDlg(compid);});
        }
        else{
            TypeActivityDlg(compid);
        }
    }
    function TypeActivityDlg(compid,getfile){
        var dlg = $('#dlg-typeactivity');
        $.getJSON('GetTypeActivity',{compid:compid, getfile:getfile},function(data){
            if(!showErr(data)){
                var table = QHTable({tid:'typeactivity',
                         thead:['№','Серия','Номер','Рег.номер','Дата с','Дата по'],
                         theadtitle:['№','Серия','Номер','Рег.номер','Дата с','Дата по'],
                         tbodytitle:['','','','','',''],
                         tbody:['Num','LICSERIAL','LICNUMBER','REGNUMBER','LICDATE1','LICDATE2'],
                         tclass:['Num','LicSerial','LicNumber','RegNumber','LicDate1','LicDate2'],
                         trid:['ACT','OBJACTTYPEID'],
                         data:data,
                        });
                $('div.table',dlg).html(table).QHxscroll();
                TypeActivityInit();
                $('div.form-edit',dlg).hide();
                dlg.QHdialogOH();
            }
        });
    }
    function TypeActivityInit(){
        $('#typeactivity').QHTableInit({width: '100%',
                            height: '200',
                            ts:['i','t','t'],
                        });
    }
    function EditTypeActivity(){
        var aclass = $(this).attr('class');
        var taid = (aclass == 'add'?null:$('#typeactivity').rfGetFocus().split('-')[1]);
        var dlg = $('#dlg-typeactivity');
        $('select.ActivityType option', dlg).remove();
        $.ajax({url: 'ajaxActTypeSel',
                data: {},
                dataType: 'json',
                async: false,
                success: function(res){
                    for(var i=0;i<res.data.length;++i)
                        $('select.ActivityType', dlg).append('<option value="'+
                                                        res.data[i].ACTTID+'">'+
                                                        res.data[i].NAME+'</option>');
                }
            });
        $('select.LicAgencyid option', dlg).remove();
        $.ajax({url: 'ajaxGetAgency',
                data: {},
                dataType: 'json',
                async: false,
                success: function(res){
                    for(var i=0;i<res.data.length;++i)
                        $('select.LicAgencyid', dlg).append('<option value="'+
                                                        res.data[i].AGENCYID+'">'+
                                                        res.data[i].NAME+'</option>');
                }
            });

        if(taid){
            $.ajax({url: 'ajaxGetObjAct',
                data: {taid: taid},
                dataType: 'json',
                async: false,
                success: function(res){
                    $('select.ActivityType', dlg).val(res.data.ACTTID);
                    $('input.LicSerial', dlg).val(res.data.LICSERIAL);
                    $('input.LicNumber', dlg).val(res.data.LICNUMBER);
                    $('input.RegNumber', dlg).val(res.data.REGNUMBER);
                    $('input.LicDate1', dlg).val(res.data.LICDATE1);
                    $('input.LicDate2', dlg).val(res.data.LICDATE2);
                    $('select.LicAgencyid', dlg).val(res.data.LICAGENCYID);
                    $('textarea.LicConditions', dlg).val(res.data.LICCONDITIONS);
                    $('textarea.Notes', dlg).val(res.data.NOTES);
                }
            });
        }
        else{
            $('input.LicSerial', dlg).val('');
            $('input.LicNumber', dlg).val('');
            $('input.RegNumber', dlg).val('');
            $('input.LicDate1', dlg).val(getToday());
            $('input.LicDate2', dlg).val(getToday());
            $('textarea.LicConditions', dlg).val('');
            $('textarea.Notes', dlg).val('');
        }
        $('div.form-edit',dlg).show();
        $('button.save',dlg).QHbind('click', function(){TypeActivityAddEdit(taid);});
        $('div.agency a.add',dlg).QHbind('click', Agency);
    }
    function DelTypeActivity(){
        if(confirm('Вы действительно хотите удалить позицию ?')){
            var taid = $('#typeactivity').rfGetFocus().split('-')[1];
            $.getJSON('ajaxObjActTypeDel',{taid:taid},function(res){
                if(res.data.OK == 'OK')
                    TypeActivity();
            });
        }
    }
    function TypeActivityAddEdit(taid){
        var dlg = $('#dlg-typeactivity');
        var objid = $('#contractors').rfGetFocus().split('-')[1];
        var actid = $('select.ActivityType', dlg).val();
        var licserial = $('input.LicSerial', dlg).val();
        var licnumber = $('input.LicNumber', dlg).val();
        var regnumber = $('input.RegNumber', dlg).val();
        var licdate1 = $('input.LicDate1', dlg).val();
        var licdate2 = $('input.LicDate2', dlg).val();
        var licagencyid = $('select.LicAgencyid', dlg).val();
        var licconditions = $('textarea.LicConditions', dlg).val();
        var notes = $('textarea.Notes', dlg).val();
        var licpicture = $('input.LicPicture', dlg).val();
        $.getJSON('ajaxObjActTypeAddEdit',
                  {taid         : taid,
                   objid        : objid,
                   actid        : actid,
                   licserial    : licserial,
                   licnumber    : licnumber,
                   regnumber    : regnumber,
                   licdate1     : licdate1,
                   licdate2     : licdate2,
                   licagencyid  : licagencyid,
                   licconditions: licconditions,
                   notes        : notes,
                   licpicture   : licpicture},
                  function(data){
            TypeActivity();
        });
    }
    function Agency(){
        dlg = $('#dlg-agency');
        if(!dlg.length){
            QHCreateDialog('dlg-agency', null, sp_forms+'/Agency.html', {height: 150,
                  width: 470,
                  title: "Добавить выдавший орган",
                  }, function(){
                    AgencyDlg();});
        }
        else{
            AgencyDlg();
        }
    }
    function AgencyDlg(){
        dlg = $('#dlg-agency');
        $('button.save', dlg).QHbind('click', AgencyAdd);
        dlg.QHdialogOH();
    }
    function AgencyAdd(){
        var Name = $('input.Name', dlg).val();
        var ShortName = $('input.ShortName', dlg).val();
        var Code = $('input.Code', dlg).val();
        $.getJSON('ajaxAgencyAdd',
                  {Name: Name,
                   ShortName: ShortName,
                   Code: Code},
                  function(res){
            $('#dlg-typeactivity select.LicAgencyid').append('<option value="'+ res.data.AGENCYID +'" selected="selected">'+Name+'</option>');
            dlg.dialog('close');
        });
    }
    function GetReq(row){
        $.getJSON('ajaxGetReq',{compid: row.attr('id').split('-')[1]},function(res){
            $('td.INN', row).text(res.data.INN);
            $('td.OKPO', row).text(res.data.OKPO);
            $('td.KPP', row).text(res.data.KPP);
            $('td.BIK', row).text(res.data.BIK);
            $('td.OGRP', row).text(res.data.OGRP);
            $('td.RegDate', row).text(res.data.REGDATE);
            $('td.Chief', row).text(res.data.CHIEF);
            $('td.PhoneChief', row).text(res.data.PHONECHIEF);
        });
    }
    function SetDefaultParams(){
        $('#idgo').QHbind('click',GetContractors);
        $('#stext').unbind("keydown").bind('keydown',function(e){if(e.keyCode==13)GetContractors();});
        $('#addContractors').unbind('click').click(function(){
            AddContractor(false, 'dlg-addcontractors');
        });
    }
    function Start(){
        SetDefaultParams();
    }
    Start();
    function Bond(el){
        if($('#dvBond').length) {$('#dvBond').dialog('destroy').remove();}
        $.getJSON('getBonds', {objid: el.attr('id').split('-')[1]}, function(data){
            var html = '<table><thead><tr><th>Объект</th><th>Тип связи</th></tr></thead><tbody>';
            for(var i=0;i<data.data.length;++i){
                html += '<tr objbondid="'+data.data[i].OBJBONDID+'" objbonttype="'+data.data[i].OBJBONDTID+'"><td>'+data.data[i].NAME+'</td><td>'+data.data[i].TYPENAME+'</td></tr>';
            }
            html+='</tbody><tfoot><tr><th colspan=2><a href="#" class="add"><img src="'+eng_img+'/actions/add.png"></a><a href="#" class="del"><img src="'+eng_img+'/actions/delete.png"></a></th></tr></tfoot>'
            $('<div/>')
                .attr('id', 'dvBond')
                .addClass("flora").css("text-align","center")
                .append(html)
                .dialog({width: 300, height: 300, title: 'Связи',
                         closeOnEscape:false,autoOpen:true,
                         resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"}})
                .find('table')
                    .kTblScroll()
                    .rowFocus()
                    .find('a.add').click(function(){
                        if($('#addBond').length) {$('#addBond').dialog('destroy').remove();}
                        var html = 'Объект <input type="text" class="obj1id"/><br><br>\
                                    Тип связи <select class="bondtype">';
                        $.ajax({url:'getBondType', success: function(data){
                            for(var i=0;i<data.data.length;++i)
                                html += '<option value="'+data.data[i].OBJBONDTID+'">'+data.data[i].NAME+'</option>';
                        }, dataType: 'json', async: false});
                        html += '</select><br><br>'+
                            '<div class="buttons" style="width:100%;text-align:center;">'+
                                '<button type="button" class="dvAddBondOk"><img src="'+eng_img+'/actions/accept.png" border="0">Добавить</button>&nbsp;&nbsp;&nbsp;'+
                                '<button type="submit" style="display:none;"></button>&nbsp;&nbsp;&nbsp;'+
                                '<button type="button" class="dvDocConfCanc"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
                            '</div>';
                        $('<form/>')
                            .addClass("flora").css("text-align","right")
                            .attr('id', 'addBond')
                            .html(html)
                            .dialog({width: 300, height: 150, title: 'Добавление связи',
                                     closeOnEscape:false,autoOpen:true,
                                     resizable:false,draggable:false,modal:true,overlay:{opacity:0.5,background:"black"}})
                            .find('.obj1id').kObjLocate({hiddenName:'obj1id',dvId:"dvObj1",title:'Объект',destroyDvIfExists:true}).end()
                            .find('.dvAddBondOk').click(function(){$('#addBond').submit();}).end()
                            .find('.dvDocConfCanc').click(function(){$('#addBond').dialog('close');}).end()
                            .submit(function(){
                                var obj1id = $(this).find('[name="obj1id"]').val();
                                if(obj1id == 'null'){alert('Введите объкт!');return false;}
                                $.blockUI({message:'<h2>..сохранение..</h2>'});
                                $.getJSON('addBond',{obj1id:el.attr('id').split('-')[1], obj2id:obj1id, type:$(this).find('select').val()}, function(data){
                                    if(!showErr(data)){
                                        $('#dvBond table').append(
                                            '<tr objbondid="'+data.data.OBJBONDID+'" objbonttype="'+$('#addBond').find('select').val()+'"><td>'+$('#addBond').find('.obj1id').val()+'</td><td>'+$('#addBond').find('option:selected').text()+'</td></tr>'
                                        ).kTblScroll().rowFocus();
                                        $('#addBond').dialog('close');
                                        $.unblockUI();
                                    }
                                })
                                return false;
                            });
                    }).end()
                    .find('a.del').click(function(){
                        var row = $('#dvBond table').rf$GetFocus();
                        if(row.length){
                            var id = row.attr('objbondid');
                            if(confirm('Вы действительно хотите удалить данную связь ?')){
                                $.blockUI({message:'<h2>..удаление..</h2>'});
                                $.getJSON('delBond',{id: id},function(data){
                                    if(!showErr(data)){
                                        $('#dvBond table').rf$GetFocus().remove();
                                        $('#dvBond table').kTblScroll().rowFocus();
                                        $.unblockUI();
                                    }
                                })
                            }
                        }
                    });
        });
    }

  function palfeature(el){
    $.getJSON('getPalletFeatures', {objid: el.attr('id').split('-')[1]}, function (json) {
      function dvReCreate(json){
        if (showErr(json)) return;
        var html = '<table><thead><tr><th>Наименование</th><th>Приоритет</th></tr></thead><tbody>';
        for (var i = 0; i < json.data.length; i++) {
          var r = json.data[i];
          html += '<tr pfid="' + r.PFID + '">' +
            '<td class="text">' + r.PFNAME + '</td>' +
            '<td><input type="text" name="pf' + r.PFID + '" value="' + kInt(r.PFPRIORITY) + '" /></td>' +
            '</tr>';
        }
        html += '</tbody><tfoot><tr><th colspan="2" class="buttons">' +
          '<button type="submit"><img src="' + eng_img + '/actions/save.png">Сохранить</button>' +
          '<button type="button"><img src="' + eng_img + '/actions/cancel.png">Отменить</button>' +
          '</th></tr></tfoot></table>';

        $('#frmPalFeatures').html(html).find('table').kTblScroll();
        $('#frmPalFeatures').find('input').css('width', '30px').kInputInt();
      }

      var $d = $('#frmPalFeatures');
      if (!$d.length){
        $d = $('<form/>').attr('id', 'frmPalFeatures').attr('clientid', json.ext_data.OBJID)
          .submit(function () {
            var p = $(this).kFormSubmitParam();
            p['OBJID'] = $(this).attr('clientid');
            $.getJSON('setPalletFeatures', p, dvReCreate);
            return false;
          })
          .addClass("flora").css("text-align", "center")
          .dialog({width: 300, height: 300, title: 'Характеристики паллетов',
            closeOnEscape: false, autoOpen: true,
            resizable: false, draggable: false, modal: true, overlay: {opacity: 0.5, background: "black"}})
      }
      else {
        $d.attr('clientid', json.ext_data.OBJID).dialog('open')
      }
      dvReCreate(json);
    });
  }
});