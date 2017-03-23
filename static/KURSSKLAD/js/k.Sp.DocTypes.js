;(function($) {

    function loadDocTypes(settings, root, child, container) {
        $.getJSON(settings.url, {id:root}, function(response) {
            function createNode(parent) {
                var current = $("<li/>").attr("id", "liDT"+this.DOCTID).html("<a href='#'>" + this.NAME + "</a>").appendTo(parent);
                current.find("a").bind("click",settings.DocTypeClick);
                
                if (this.classes) current.children("span").addClass(this.classes);
                if (this.expanded) current.addClass("open");
                
                if (this.HASCHILDREN && this.HASCHILDREN=='1') {
                    var branch = $("<ul/>").appendTo(current);
                    current.addClass("hasChildren");
                    createNode.call({
                        text:"placeholder",
                        id:"placeholder",
                        children:[]
                    }, branch);
                }
            }
            $.each(response.data, createNode, [child]);
            $(container).treeDocTypes({add: child});
        });
    };

    $.fn.treeDocTypes = function(settings) {   
        if (!settings.url) return $.fn.treeview.apply(this, arguments);
        var container = this;    
        loadDocTypes(settings, "0", this, container);
        var userToggle = settings.toggle;
        return $.fn.treeview.call(this, $.extend({}, settings, {
            collapsed: true,
            toggle: function() {
                var $this = $(this);
                if ($this.hasClass("hasChildren")) {
                    var childList = $this.removeClass("hasChildren").find("ul");
                    childList.empty();
                    loadDocTypes(settings, this.id.substring("liDT".length), childList, container);
                }
                if (userToggle) userToggle.apply(this, arguments);
            }
        }));
    };

    $.SpDocTypes = function(options)
    {   var options = $.extend({title:'Выбор типа документа', // Заголовок
                                afterSelect: false, // Select function
                                divId: 'dvSpDocType'
                               },options);
        
        var $dialog = $("#"+options.divId);
        if ($dialog.length==0)
        {   var $dialog = $("<div/>")
                .attr("id",options.divId)
                .addClass("flora")
                .css({"text-align":"left",
                      "float":"left",
                      "position":"relative",
                      "overflow":"auto"
                    })
                .dialog({height:350,width:350,modal:true,resizable:false,draggable:true,title:options.title,overlay:{backgroundColor:'#000',opacity: 0.5}})
                .treeDocTypes({ url:"DocTypes",
                                DocTypeClick:function()
                                {   $("#"+options.divId).dialog("close");
                                    options.DocTypeClick.call(this,$(this).parents("li").attr("id").substring("liDT".length),$(this).text());
                                }
                             });
        }
        $dialog.dialog("open");
    };
    
    
    $.fn.cmbSpDocTypes = function(options)
    {   var options = $.extend({withoutFilter: "null",
                                onChange: false,
                                request: 'docTypes',
                                requestParam: {},
                                addCode: false,
                                addWsetId: false,
                                addInitStatus: false,
                                addPriceCode: false,
                                funcOptAttr: false
                               },options);
        var $cmb = $(this);

        function restrict(data) {
            return ((options.docmanager)?' restrict='+data.DOCMANAGEREDITDISABLE+' ':'');
        }
        function optAttr(data){
            return ((options.funcOptAttr) ? options.funcOptAttr(data) : '');
        }

        $.getJSON(options.request,options.requestParam,function(JSON)
        {   var html = '';
            if (options.withoutFilter) html = '<option value="'+options.withoutFilter+'">Без фильтра</option>';
            
            if (JSON.data.length){
                for (var i=0; i<JSON.data.length; i++) {html += '<option value="'+JSON.data[i].DOCTID+'"'+
                                                                         restrict(JSON.data[i])+
                                                                         optAttr(JSON.data[i])+
                                                                         ((options.addCode)?' code="'+JSON.data[i].CODE+'"':'')+
                                                                         ((options.addWsetId)?' wsetid="'+JSON.data[i].WSETID+'"':'')+
                                                                         ((options.addPriceCode)?' pricecode="'+JSON.data[i].PRICECODE+'"':'')+
                                                                         ((options.addInitStatus)?' initstatus="'+JSON.data[i].FIRSTSTATUS+'"':'')+'>'+JSON.data[i].NAME+'</option>';}
                $cmb.html(html);
                if (options.onChange) {
                    if (typeof options.onChange == 'function')    $cmb.change(options.onChange).change();
                }
            }
            else {
                alert('Нет ни одного типа документов!');
            }
        });
    };
    

    $.fn.cmbSpDocTypeStatuses = function(doctid)
    {   var $cmb = $(this);
        $.getJSON(options.request,function(JSON)
        {   var html = '';
            if (options.withoutFilter) html = '<option value="'+options.withoutFilter+'">Без фильтра</option>';
            
            for (var i=0; i<JSON.data.length; i++) {html += '<option value="'+JSON.data[i].DOCTID+'">'+JSON.data[i].NAME+'</option>';}
            $cmb.html(html);
            if (options.onChange)
            {   if (typeof options.onChange == 'function')    $cmb.change(options.onChange);
                
            }   
        });
    };
    
})(jQuery);