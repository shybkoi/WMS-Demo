;(function($) {
    
    function load(settings, root, child, container) {
        $.getJSON(settings.url, {parentid:root}, function(response) {
            function createNode(parent) {
                var current = $("<li/>").attr("id", $.kID("liS",this.ID)).html("<a href='#'>" + this.NAME + "</a>").appendTo(parent);
                if (settings.click) current.find("a").bind("click",settings.click);
                
                if (this.classes) current.children("span").addClass(this.classes);
                if (this.expanded) current.addClass("open");
                
                if (this.HASCHILD && this.HASCHILD == '1') {
                    var branch = $("<ul/>").appendTo(current);
                    current.addClass("hasChildren");
                    createNode.call({NAME:"placeholder",ID:"placeholder"}, branch);
                }
            }
            $.each(response.data, createNode, [child]);
            $(container).treeview({add: child});
            if (settings.cb) {
                settings.cb.apply(this,$(container))
            }
        });
    }

    $.fn.SiteTree = function(settings) {
        if (!settings.url) return $.fn.treeview.apply(this, arguments);
        var container = this;
        load(settings, "0", this, container);
        var userToggle = settings.toggle;
        return $.fn.treeview.call(this, $.extend({}, settings, {
            collapsed: true,
            toggle: function() {
                var $this = $(this);
                if ($this.hasClass("hasChildren")) {
                    var childList = $this.removeClass("hasChildren").find("ul");
                    childList.empty();
                    load(settings, $.kID(this.id), childList, container);
                }
                if (userToggle) userToggle.apply(this, arguments);
            }
        }));
    };

    $.dvSiteTree = function(O){
        var O = $.extend({
            dvId: "dvSiteTree",
            url: "qSiteTreeList",
            click: false
        },O);

        var $dialog = $("#" + O.dvId);
        if ($dialog.length == 0) {
            var $dialog = $("<div/>").attr("id", O.dvId).addClass("flora treeView").css("text-align", "center")
              .dialog({
                  height: 500, width: 600, modal: true, resizable: false, draggable: true,
                  title: "Выбор местоположения", overlay: {backgroundColor: '#000', opacity: 0.5}
              });
            $dialog.html('<div class="tree">' +
            '<ul class="ulSiteTree treeview" ' +
            'style="height:420px;overflow:auto;text-align:left;background-color:white;"></ul>' +
            '</div>').find('ul.ulSiteTree').SiteTree({
              url: O.url, click: function () {
                  $("#dvSiteTree").dialog('close');
                  if (O.click) O.click.call($(this), $(this).parents("li").kID(), $(this).text());
              }
            });
            $dialog.find('ul.ulSiteTree').css('height', $dialog.innerHeight());
        }
        $dialog.dialog('open');
    };

    $.fn.inputSiteTree = function(O){
        var $this = $(this);

        var O = $.extend({
            dvId: "dvSiteTree",
            url: "qSiteTreeList",
            nullVal: 'None',
            attrVal: 'data-val'
        }, O);

        function onClick(e) {
            function siteTree(sid, sname) {
                $this.val(sname).attr('title', sname).attr(O.attrVal, sid);
            }

            $.dvSiteTree({click: siteTree, dvId: O.dvId, url: O.url});
        }

        function onRightClick(e) {
            $this.val('').removeAttr('title').attr(O.attrVal, O.nullVal);
        }

        O = $.extend({
            onClick: onClick,
            onRightClick: onRightClick
        }, O);


        $this.click(O.onClick).rightClick(O.onRightClick);
        O.onRightClick();
        return $this;
    };

})(jQuery);