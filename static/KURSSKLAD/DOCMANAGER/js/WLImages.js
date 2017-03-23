(function($){
    var dialogOptions = {
        closeOnEscape:false,
        autoOpen:true,
        resizable:false,
        draggable:false,
        modal:true,
        overlay:{opacity:0.5,background:"black"}
    }
    $.WLImages = function(options){
        var o = $.extend({
            wls: '',
            width: 900,
            height: 500,
            linkType: 'scan'
        }, options);
        var html = '<div style="width:50%;float:left;"><div style="height:50%;width:100%;float:left;" class="dvWl"></div><div style="height:50%;width:100%;float:left;" class="dvImg"></div></div><div style="width:50%;float:left;" class="dvImgPlace"></div>';
        if ($("#dvImages").length) $("#dvImages").dialog("destroy").remove();
        $("<div/>")
            .attr("id","dvImages").addClass("flora")
            .dialog($.extend({
                        height: o.height,
                        width: o.width,
                        title:'�����������'
                    }, dialogOptions))
            .html(html);
        $.blockUI({message: '<h1>�������� ������</h1>'});
        $.getJSON('getWLs', {wls: o.wls}, function(response){
            if(!showErr(response)){
                var html = '<table id="wlTbl"><thead><tr><th colspan=4>������</th></tr><tr><th>�����</th><th>���</th><th>� ������</th><th>���� ������</th></tr><thead><tbody>';
                for(var i in response.data){
                    var r = response.data[i];
                    html += '<tr wlot="'+r.WLOTID+'">\
                                <td class="text">'+r.WNAME+'</td>\
                                <td>'+r.WCODE+'</td>\
                                <td>'+r.WLNUMBER+'</td>\
                                <td>'+kDate(r.PRODUCTDATE)+'</td>\
                            </tr>';
                }
                html += '</tbody></table>';
                $('#dvImages .dvWl').html(html)
                    .height($('#dvImages').innerHeight()/2)
                    .find('table')
                        .kTblScroll()
                        .rowFocus({rfFocusCallBack: wlCallback});
            }
            $.unblockUI();
        })
    }
    
    function wlCallback(){
        var tr = $(this);
        $.blockUI({message: '<h1>�������� ������</h1>'});
        $.getJSON('getImagesByWL', {wlotid: tr.attr('wlot')}, function(response){
            if(!showErr(response)){
                var html = '<table id="imgTbl"><thead><tr><th colspan=2>�����������</th><tr><th>���</th><th>���</th></tr><thead><tbody>';
                for(var i in response.data){
                    html += imgTr(response.data[i]);
                }
                html += '</tbody><tfoot><tr><th colspan=2>\
                        <a href="javascript:void(0);" title="�������� �����������"><img src="'+eng_img+'/actions/add.png" border="0"></a>\
                        <a href="javascript:void(0);" title="������� �����������"><img src="'+eng_img+'/actions/delete.png" border="0"></a>\
                        </th></tr></tfoot></table>';
                $('#dvImages .dvImg').html(html)
                    .height($('#dvImages').innerHeight()/2)
                    .find('table')
                        .kTblScroll('100%')
                        .rowFocus({rfFocusCallBack: imgCallback})
                        .find('a')
                            .eq(0).click(addImg).end()
                            .eq(1).click(delImg).end();
            }
            $.unblockUI();
        });
    }
    function imgTr(r){
        return '<tr img="'+r.IMAGEID+'" imgwl="'+r.IMGWLID+'" itid="'+r.ITTYPE+'" path="'+ r.IPATH+'">\
                    <td class="text">'+r.INAME+'</td>\
                    <td>'+r.ITNAME+'</td>\
                </tr>';
    }
    function imgCallback(){
        var curTr = $('#imgTbl').rf$GetFocus();
        var $imgPlace = $('#dvImages .dvImgPlace');
        $imgPlace
            .height($('#dvImages').innerHeight())
            .html(
                $('<img/>')
                    .attr('src', '/download/?filepath='+curTr.attr('path'))
                    .css({
                        'max-width': $imgPlace.innerWidth(),
                        'max-height': $imgPlace.innerHeight()
                    })
                    .click(function(){
                        $.fancybox({type : 'image', href: this.src});
                    })
            );
        $("#dvImgAdd").dialog("close");
    }
    function addImg(){
        var wlTr = $('#wlTbl').rf$GetFocus();
        if ($("#dvImgAdd").length) $("#dvImgAdd").dialog("destroy").remove();
        var html = '';
        html += '<form id="frmImgAdd">'+
                    '�������� <input type=text name=iname><br/>'+
                    '��� <select name=itype></select><br/>'+
                    '���� <input type=file accept="image/*" name=fileupload><br/>'+
                    '<input type="hidden" name="wlotid" value="'+wlTr.attr('wlot')+'">'+
                    '<div class="buttons" style="width:100%;"><hr>'+
                        '<button type="submit" id="imgSave" title="���������"><img src="'+eng_img+'/actions/save.png" border="0">���������</button>&nbsp;'+
                        '<button type="button" id="imgCancel" title="��������"><img src="'+eng_img+'/actions/cancel.png" border="0">��������</button><br>'+
                    '</div>'+
                '</form>';
        $dv = $("<div/>").attr("id","dvImgAdd")
            .addClass("flora").css("text-align","right")
            .dialog($.extend({
                        title:'���������� �����������',
                        height:170,
                        width:400
                    },dialogOptions))
            .html(html).find("button:last").click(function(){ $("#dvImgAdd").dialog("close"); }).end()
            .find('form').ajaxForm({
                url: 'saveNewImage',
                type: 'POST',
                success: function(response){
                    response = JSON.parse(response);
                    if(!showErr(response)){
                        $('#imgTbl tbody').append(imgTr({
                            IMAGEID: response.data.IMGID,
                            IMGWLID: response.data.IMGWLID,
                            INAME: $('#frmImgAdd input[name="iname"]').val(),
                            ITNAME: $('#frmImgAdd option:selected').text(),
                            ITTYPE: $('#frmImgAdd select').val(),
                            IPATH: response.data.PATH
                        }));
                        $('#imgTbl')
                            .kTblScroll('100%')
                            .rowFocus({rfFocusCallBack: imgCallback})
                    }
                    $("#dvImgAdd").dialog("close");
                }
            });

        $.blockUI({message: '<h1>..�������� �����..</h1>'});
        $.getJSON('getImageTypes', function(response){
            if(!showErr(response)){
                var $sel = $('#frmImgAdd select');
                $sel.empty();
                $.each(response.data, function(key, value){
                    $sel.append($('<option/>')
                                    .attr('value', value.IMGLINKTID)
                                    .text(value.NAME))
                })
            }
            $.unblockUI();
        });
    }

    function delImg(){
        var curTr = $('#imgTbl').rf$GetFocus();
        if(curTr.length){
            if(confirm('�� ������������� ������ ������� �����������?\n������ �������� ����������!')){
                $.getJSON('deleteImg',{imgwlid: curTr.attr('imgwl'), path: curTr.attr('path')},function(response){
                    if(!showErr(response)){
                        curTr.remove();
                        $('#imgTbl')
                            .kTblScroll('100%')
                            .rowFocus({rfFocusCallBack: imgCallback});
                    }
                });
            }
        }
    }
    
})(jQuery)