;(function(jQuery){
    
    jQuery.kObjLocate = function(options)
    {   // defaults
        var options = jQuery.extend({title:'Поиск контрагента', // Заголовок
                                     action: 'listObjects', 
                                     statuses: false, // Выбирать ли статус контрагента из списка и собственно список статусов '01с'
                                     afterSel: false, // Function after 
                                     closeAfter: true, // Close after select
                                     data: false, // Дополнительные параметры для передачи
                                     dvId:"dvObjLocate", // Идентификатор диалога
                                     destroyDvIfExists:false, // перпестьраивать диалог, если существует
                                     eventClose: false,
                                     minLength: 1,
                                     submitAfterShow: false
                                    },options);
        
        
        var $dialog = $("#"+options.dvId);
        if ($dialog.length && options.destroyDvIfExists) {
            $dialog.dialog("destroy").remove();
            $dialog = $("#"+options.dvId);
        }
        
        if ($dialog.length==0){   
            var selectHtml = '';
            if (options.statuses) {   
                selectHtml = '<select name="status">';
                for (var symbol in options.statuses) {   
                    if  (symbol=='0') selectHtml += '<option value="'+symbol+'">Не активный</option>';
                    if  (symbol=='1') selectHtml += '<option value="'+symbol+'">Активный</option>';
                    if  (symbol=='c') selectHtml += '<option value="'+symbol+'">Видимый</option>';
                }    
                selectHtml += '</select> ';
            }
            
            var $dialog = $("<div/>").attr("id",options.dvId).addClass("flora").css("text-align","center").dialog({height:400,width:400,modal:true,resizable:false,draggable:true,title:options.title,overlay:{backgroundColor:'#000',opacity: 0.5}});
            $dialog.html('<form class="buttons" style="height:10%">'+ selectHtml+
                                '<input type="text" style="width:100px" value=""> </input>'+'<button type="submit"><img src="'+eng_img+'/actions/magnifier.png" border="0">Искать</button>'+
                          '</form>'+
                          '<div style="height:90%"></div>');
            
            $("form",$dialog).unbind("submit").bind("submit",function() {   
                var incname = $(this).find("input").val();
                if (incname.length < options.minLength)  { showMes('Ошибка','Ничего не написано!'); return false; }
                $("div:last",$dialog).empty();
                var data;
                if (options.data) data = options.data;
                else data = {};
                data.incname = incname;
                if ( $(this).find("select").length>0 ) data.statuses = $(this).find("select>option:selected").val();
                $.getJSON(options.action,data,function(JSON) {   
                    var html = '<table><thead><tr><th>Наименование</th></tr></thead><tbody>';
                    for (var i=0; i<JSON.data.length; i++)
                        html += '<tr objid="'+kInt(JSON.data[i].OBJID)+'"><td class="text">'+JSON.data[i].NAME+'</td></tr>';
                    html += '</tbody><tfoot><tr><th>Итого: '+JSON.data.length+'</th></tr></tfoot></table>';
                    $("div:last",$dialog).html(html).find("table").kTblScroll().tablesorter()
                        .find("tbody>tr").click(function() {   
                            var $tr = $(this);
                            var objid = $tr.attr("objid");
                            var text = $tr.find("td:first").text();
                            if (options.afterSel) options.afterSel(objid,text);
                            if (options.closeAfter) $dialog.dialog("close");
                        });
                });
                return false;
            }).find("input").unbind("focus").focus(function(){$(this).select();});
        }
        if (options.eventClose) $dialog.bind("dialogclose",options.eventClose);
        $dialog.dialog("open");
        if(options.submitAfterShow) $dialog.find("form").submit();
        $dialog.find("input").focus();
        
        return $dialog;
    };    
    
    jQuery.fn.kObjLocate = function(options)
    {   // defaults
        var self = this.attr("readonly","readonly");
        
        var options = jQuery.extend({title:'Поиск контрагента', // Заголовок
                                     hiddenName: false, // Id Hidden Element
                                     action: 'listObjects', 
                                     statuses: false, // Выбирать ли статус контрагента из списка и собственно список статусов '01с'
                                     inputTitle: 'Кликните правой или левой кнопкой мыши для выбора контрагента',
                                     buttons: false,
                                     data: false, // Дополнительные параметры для передачи
                                     dvId:"dvObjLocateFn", // Идентификатор диалога
                                     destroyDvIfExists:false,
                                     eventClose: false,
                                     minLength: 1,
                                     submitAfterShow: false
                                    },options);
        
        var buttons = options.buttons ? jQuery.extend({locateBtnTitle: 'Выбор контрагента',deleteBtnTitle: 'Очиситить контрагента',},options.buttons) : false;
        
        // Добавим hiffen - элемент
        var $hidden = false;
        var $form = self.parents("form");
        if (options.hiddenName && $form.length>0){
            $hidden = $form.find("input:hidden[name="+options.hiddenName+"]");
            if ($hidden.length==0) $hidden = $('<input/>').attr("type","hidden").attr("name",options.hiddenName).val("null").appendTo($form);
            else $hidden.val("null");
        }
        
        // Функция очистки
        self.clear = function() {
            self.$i().val("").removeAttr("title");
            if ($hidden && $hidden.length>0) $hidden.val("null");        
        };
        
        self.$i = function(){
            if (self.is("input")) return self;
            else return self.find("input:first");
        };
        
        var destroyDvIfExists = true;
        // Функция поиска
        self.locate = function(){
            $.kObjLocate({title:options.title,
                          action: options.action, 
                          statuses: options.statuses,
                          afterSel: function(objid,objname) {
                            self.$i().val(objname).attr("title",objname);
                            if ($hidden && $hidden.length>0) $hidden.val(objid);
                          },
                          closeAfter: true,
                          dvId:options.dvId,
                          data:options.data,
                          minLength: options.minLength,
                          submitAfterShow: options.submitAfterShow,
                          destroyDvIfExists:(options.destroyDvIfExists===true ? true : (options.destroyDvIfExists ? destroyDvIfExists : false)),
                          eventClose:function(){self.focus();}
                         });
            destroyDvIfExists = false;
        };
        
        // Если выбран режим с кнопками
        if (buttons) {
            if (!self.hasClass("buttons")) self.addClass("buttons");
            self.html('<input type="text" readonly style="width:66%;border:1px solid gray;">'+
                      '<button type="button" style="width:15%;" title="'+buttons.locateBtnTitle+'"><img src="'+eng_img+'/actions/magnifier.png" border="0"></button>'+
                      '<button type="button" style="width:15%" title="'+buttons.deleteBtnTitle+'"><img src="'+eng_img+'/actions/application.png" border="0"></button>');
            
            self.find("button:first").unbind("click").bind("click",self.locate);
            self.find("button:last").unbind("click").bind("click",self.clear).click();
        } //Если простой input
        else {
            if ($("#ulObjLocate").length==0)
            {   $(document.body).append('<ul id="ulObjLocate" class="contextMenu">'+
                                            '<li class="locate"><a href="#locate">Искать</a></li>'+
                                            '<li class="clear"><a href="#clear">Очистить</a></li>'+
                                        '</ul>');
                $("#ulObjLocate>li.locate>a").css("background-image","url("+eng_img+"/actions/magnifier.png)");
                $("#ulObjLocate>li.clear>a").css("background-image","url("+eng_img+"/actions/application.png)");
            }
            
            var $i;
            if (self.is("input")) $i = self;
            else $i = self.html('<input type="text" readonly style="width:96%;">').find("input:first");
            $i.contextMenu({menu:'ulObjLocate'},function(action){   if (action=='locate') self.locate();
                if (action=='clear') self.clear();
            });
        }
        
        
        self.$i().click(self.locate);
        self.clear();
        return self;
    };    
})(jQuery);
