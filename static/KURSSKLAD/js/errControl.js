//Position erorr control
// use: k.messages.js, k.formats.js

function kErrControl($el,cargoid,typecode,actions,afterWork)
{   var self = this;
    
    this.createW = function($d)
    {   $.kWaresLocate({success:function(waresid)
            {   $.getJSON('errChkIncomeWares',{cargoid:cargoid,waresid:waresid},function(JSON)
                {   if (!showErr(JSON))
                    {   $el.showConf({text:'Вы действительно хотите заменить позицию на: '+JSON.data.CODE+' - '+JSON.data.NAME+'?',
                                      confirm: function()
                                      { if ($d) $d.dialog("close");
                                        $.getJSON('errRegW',{cargoid:cargoid,waresid:waresid},function(JSON)
                                        {   if (!showErr(JSON))
                                                if (afterWork) afterWork.apply($el, arguments);
                                        });
                                      }
                                    });
                    }
                });
            } 
        });
    };
    
    this.createA = function($d)
    {   $.getJSON("errGetCargoInfo",{cargoid:cargoid},function(JSON)
        {   if (!showErr(JSON))
            {   var $dialog = $("#dvErrCreateA");
                if ($dialog.length!=0) $dialog.empty().remove();
                $dialog = $("<div/>").attr("id","dvErrCreateA").addClass("flora").css("text-align","center").dialog({height:150,width:700,modal:true,resizable:false,draggable:true,title:'Не верное количество',overlay:{backgroundColor:'#000',opacity: 0.5}});
                html = '<table style="width:100%"><thead>'+
                            '<tr><th>Код</th><th>Наименование</th><th>Количество</th><th>Цена</th><th>Сумма</th></tr>'+
                            '</thead><tbody>'+
                        '<tr>'+
                            '<td rowspan="2">'+JSON.data.CODE+'</td>'+
                            '<td rowspan="2">'+JSON.data.NAME+'</td>'+
                            '<td>'+kFloat(JSON.data.AMOUNT,3)+'</td>'+
                            '<td rowspan="2">'+kFloat(JSON.data.PRICE,2)+'</td>'+
                            '<td>'+kFloat(JSON.data.DOCSUM,4)+'</td>'+
                        '</tr>'+
                        '<tr>'+
                            '<td><input type="text" value="'+kFloat(JSON.data.AMOUNT,3)+'" size="7"></td>'+
                            '<td>'+kFloat(JSON.data.DOCSUM,4)+'</td>'+
                        '</tr></tbody><tfoot>'+
                        '<tr><th colspan="5" class="buttons">'+
                                '<button type="button"><img src="'+eng_img+'/actions/accept.png" border="0">Подтвердить</button>'+
                                '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>'+
                            '</th></tr></tfoot></table>';
                $dialog.html(html);
                $dialog.find("input").change(function()
                {   var nAm = parseFloat($(this).val());
                    var price = parseFloat($(this).parents("tr").prev().find("td").eq(3).text());
                    $(this).parents("td").next().text(kFloat(nAm*price,3));
                });
                $dialog.find("button:last").click(function(){$dialog.dialog("close")});
                $dialog.find("button:first").click(function()
                {   var $btn =$(this);
                    $btn.hide();
                    var amount = $dialog.find("input").val();
                    $.getJSON('errRegA',{cargoid:cargoid,amount:amount},function(JSON)
                    {   if (!showErr(JSON))
                        {   if (afterWork) afterWork.apply($el, arguments);
                            $dialog.dialog("close");
                            if ($d) $d.dialog("close");
                        }
                        else $btn.show();
                    });
                });
                $dialog.dialog("open");
            }
        });
    };    
    
    this.chkCargo = function(cargoid,typecode,refresh)
    {   $.getJSON('errChkCargo',{cargoid:cargoid,typecode:typecode},function(JSON)
        {   if (!showErr(JSON))
            {   if (JSON.data.length>0)
                {   var $dialog = $("#dvErrList");
                    if ($dialog.length!=0) $dialog.empty().remove();
                    $dialog = $("<div/>").attr("id","dvErrList").addClass("flora").css("text-align","center").dialog({height:275,width:700,modal:true,resizable:false,draggable:true,title:'Не отработанные ошибки',overlay:{backgroundColor:'#000',opacity: 0.5}});
                    
                    html = '<table id="tblErrList" style="width:100%"><thead>'+
                                '<tr><th>Статус</th><th>№</th><th>Время регистрации</th><th>Пользователь</th><th>Тип</th><th>Комментарий</th><th>Контрагент</th></tr>'+
                                '</thead><tbody>';
                    for (var i=0; i<JSON.data.length; i++)
                    {   html += '<tr>'+
                                    '<td>'+( (JSON.data[i].E_STATUS=='0') ? 'Новая' : 'Апелляция') +'</td>'+
                                    '<td>'+JSON.data[i].E_ID+'</td>'+
                                    '<td>'+JSON.data[i].E_REG_TIME+'</td>'+
                                    '<td>'+JSON.data[i].E_REG_USERFIO+'</td>'+
                                    '<td>'+JSON.data[i].E_TYPENAME+'</td>'+
                                    '<td>'+JSON.data[i].E_COMMENTS+'</td>'+
                                    '<td>'+JSON.data[i].E_OBJNAME+'</td>'+
                                '</tr>';
                    }
                    html += '</tbody></table>';
                    $dialog.html(html);
                    $dialog.find("table>tbody>tr").click(function()
                    {   var errid = $(this).find("td").eq(1).text();
                        var $dConf = $("#dvErrLeedConf");
                        if ($dConf.length!=0) $dConf.empty().remove();
                        $dConf = $("<div/>").attr("id","dvErrLeedConf").addClass("flora").css("text-align","center").dialog({height:75,width:300,modal:true,resizable:false,draggable:true,title:'Подтверждение',overlay:{backgroundColor:'#000',opacity: 0.5}});
                        $dConf.html('<div class="buttons"><button type="button"><img src="'+eng_img+'/actions/accept.png" border="0">Подтвердить ошибку</button>'+
                                '<button type="button"><img src="'+eng_img+'/actions/cancel.png" border="0">Отклонить ошибку</button></div>');
                        $dConf.find("button:last").click(function()
                        {   $dConf.find("button").attr("disabled","disabled");
                            $.getJSON("errIncomeTWLeed",{errorid:errid,status:'1'},function(JSON)
                            {   if (!showErr(JSON))
                                {   $dConf.dialog("close");
                                    $dialog.dialog("close");
                                    self.chkCargo(cargoid,'INCOMETW',afterWork);
                                }
                                else $dConf.find("button").removeAttr("disabled");
                            });
                        });
                        $dConf.find("button:first").click(function()
                        {   $dConf.find("button").attr("disabled","disabled");
                            $.getJSON("errIncomeTWLeed",{errorid:errid,status:'2'},function(JSON)
                            {   if (!showErr(JSON))
                                {   $dConf.dialog("close");
                                    $dialog.dialog("close");
                                    self.chkCargo(cargoid,'INCOMETW',afterWork);
                                }
                                else $dConf.find("button").removeAttr("disabled");
                            });
                        });
                        $dConf.dialog("open");
                    });
                    $dialog.dialog("open");
                }
                else if (refresh)
                {   $("#dvErrList").empty().remove();
                    refresh.apply($el, arguments);
                }
                else
                {   $.getJSON('errTypes',{actions:actions},function(JSON)
                    {   if (!showErr(JSON))
                        {   var $dialog = $("#dvErrTypes");
                            if ($dialog.length!=0) $dialog.empty().remove();
                            $dialog = $("<div/>").attr("id","dvErrTypes").addClass("flora").css("text-align","center").dialog({height:275,width:200,modal:true,resizable:false,draggable:true,title:'Выберите тип ошибки',overlay:{backgroundColor:'#000',opacity: 0.5}});
                        
                            html = '<table style="width:100%"><thead>'+'<tr><th>Тип</th></tr>'+'</thead><tbody>';
                            for (var i=0; i<JSON.data.length; i++)
                                html += '<tr code="'+JSON.data[i].CODE+'"><td>'+JSON.data[i].NAME+'</td></tr>';
                            html += '</tbody></table>'
                            $dialog.html(html);
                            $("table",$dialog).find("tbody>tr").click(function()
                            {   var code = $(this).attr("code");
                                if (code=='w') self.createW($dialog);
                                if (code=='a') self.createA($dialog);
                            });
                            $dialog.dialog("open");
                        }
                    });
                }
            }
        });
    };
    
    self.chkCargo(cargoid, 'INCOMETW');
}