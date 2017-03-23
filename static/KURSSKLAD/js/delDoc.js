// Удаление документа
function kDelDoc($tr,docid,statuses,afterDel)
{   var self = this;
    
    this.ddErrShowText = function(text)
    {   if (typeof window['errShowText'] == 'function') errShowText(text);
        else 
        {   if (typeof window['showMes'] == 'function') showMes("Внимание",text);
            else alert(text);
        }
    }
    
    this.errShow = function(JSON)
    {   if (JSON)
        {   if (JSON.errMes) 
            {   self.ddErrShowText(JSON.errMes); 
                return true;
            }
            else
            if (JSON.data && JSON.data.ERRMES)
            {   self.ddErrShowText(JSON.data.ERRMES); 
                return true;
            }
        }
        return false;
    }      

    this.NullTo = function(expr,to) 
    {   res = (!expr || expr=='None') ? to : expr;
        return res;
    }
        
    this.dttod = function(dt)
    {   if (typeof window['kDate'] == 'function') return kDate(dt);
        else return (!dt || dt=='None') ? '&nbsp;' : dt.split(' ')[0];
    }
    
    $.getJSON("delDocInfo",{docid:docid},function(JSON)
    {   if (JSON.length>0)
        {   if (statuses.indexOf(JSON[0].STATUS)>-1)
            {   var $dialog = $("#dvDelDoc");
                if ($dialog.length!=0) $dialog.empty().remove();
                $dialog = $("<div/>").attr("id","dvDelDoc").addClass("flora").css("text-align","center").dialog({height:275,width:350,modal:true,resizable:false,draggable:true,title:'Удаление документа',overlay:{backgroundColor:'#000',opacity: 0.5}});
                $dialog.html('От кого: <b><u>'+self.NullTo(JSON[0].FROMNAME,'&nbsp;')+'</u></b><br><br>'+
                             'Кому: <b><u>'+self.NullTo(JSON[0].TONAME,'&nbsp;')+'</u></b><br><br>'+
                             'Подтип документа: <b><u>'+self.NullTo(JSON[0].DSTNAME,'Не задан')+'</u></b><br><br>'+
                             'Номер: <b><u>'+self.NullTo(JSON[0].NUMBER,'&nbsp;')+'</u></b><br><br>'+
                             'Дата: <b><u>'+self.dttod(JSON[0].DOCDATE)+'</u></b><br><br>'+
                             'Дата документа: <b><u>'+self.dttod(JSON[0].REALDOCDATE)+'</u></b><br><br>'+
                             'Причина удаления: <select id="dvDelDocReason"></select><br><br>'+
                             '<div class="buttons"><button type="submit" id="dvDelDocCancel"><img src="'+eng_img+'/actions/cancel.png" border="0">Отменить</button>&nbsp;&nbsp;&nbsp;'+
                             '<button type="submit" id="dvDelDocSubmit"><img src="'+eng_img+'/actions/accept.png" border="0">Подтвердить</button></div>');
                
                $.getJSON("delDocReasons",{docid:docid},function(JSON)
                {   if (!self.errShow(JSON))
                        {   var html  = '';
                            var len = JSON.length;
                            for (var i = 0; i < len; i++) 
                                html += '<option value="'+JSON[i].CODE+'">'+JSON[i].NAME+'</option>';
                            $("#dvDelDocReason").html(html);
                        }
                });
                
                $("#dvDelDocCancel").bind("click",function(){$dialog.dialog("close");});
                $("#dvDelDocSubmit").unbind("click").bind("click",function()
                {   if($("#dvDelDocReason>option:selected").length==0){self.ddErrShowText("Не выбрана причина!"); return;}               
                    $("#dvDelDocSubmit").hide();
                    $.getJSON("delDocDo",{docid:docid,reason:$("#dvDelDocReason>option:selected").val()},function(JSON)
                    {   if (!self.errShow(JSON))
                        {   $dialog.dialog("close");
                            var $tbl = $tr.parents("table");
                            $tr.remove();
                            $tbl.trigger("update");
                            if( typeof $.fn.kTblScroll == 'function') $tbl.kTblScroll();
                            if (afterDel) afterDel.apply($tbl,arguments);
                        }
                        $("#dvDelDocSubmit").show();
                    });
                });
            }
            else self.ddErrShowText("Статус документа не позволяет удаление!");
        }
        else this.ddErrShowText("Ошибка запроса!");
    });
}