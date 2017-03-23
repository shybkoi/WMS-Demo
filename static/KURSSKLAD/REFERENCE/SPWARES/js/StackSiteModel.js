
// партии ( по приходам)
(function($){
    
    $.fn.waresStackModels = function(options) {
        
        var options = $.extend({
            'wid': false // товар
        },options);
        
        if (!options.wid) {
            showMes('Внимание','Товар не найден!');
            return false;
        }
            
            
        var $container = $(this).html('<div style="position:relative;float:left;height:100%;width:100%;">\
                                         <div style="position:relative;float:left;height:100%;width:50%;"></div>\
                                         <div style="position:relative;float:left;height:100%;width:50%;"></div>\
                                       </div>');
            
        $.getJSON('waresStackModelList', {wid: options.wid}, listWaresStackModels);
            
        return $(this);
        
        
        function listWaresStackModels(json) {
            if (!showErr(json)) {
                var html = '<table id=tblWaresStackModel data-wid=' + json.ext_data.WID + '><thead><tr>\
                                <th ksort="false">&nbsp;</th>\
                                <th ksort="text">Модель</th>\
                                <th>Пр</th>\
                            </tr></thead><tbody>';
                var amount_sum = 0;
                for (var i=0; i<json.data.length; i++){
                    var tr = json.data[i];
                    html += '<tr data-modelid="' + tr.MODELID + '">'+
                                '<td><input type=checkbox disabled' + (tr.PRIORITY > 0 ? ' checked' : '') +'></td>'+
                                '<td class="text">' + tr.MODELNAME + '</td>'+
                                '<td><input type="text" size="2" value="' + tr.PRIORITY + '"></td>'+
                            '</tr>';
                }  
                html += '</tbody><tfoot><tr><th>' + json.data.length +'</th><th>&nbsp;</th><th>&nbsp;</th></tr></tfoot></table>';
                $container.find('>div:first>div:first').html(html)
                    .find('table').kTblScroll().kTblSorter().rowFocus()
                        .find('tbody>tr>td>input:text').kInputInt({selectOnFocus: true}).change(function(){
                            var P = {
                                priority: $(this).val(),
                                wid: $(this).parents('table:first').attr('data-wid'),
                                modelid: $(this).parents('tr:first').attr('data-modelid')
                            }
                            $.getJSON('waresStackModelSet', P, function(json){
                                if (!showErr(json)){
                                    var $tr = $('#tblWaresStackModel').find('tr[data-modelid=' + json.ext_data.MODELID + ']');                                    
                                    if ($tr.length){
                                        if (json.data.R == 'D'){
                                            $tr.find('input:checkbox').removeAttr('checked');
                                            $tr.find('input:text').val('0');
                                        }
                                        else{
                                            $tr.find('input:checkbox').attr('checked', 'checked');
                                            $tr.find('input:text').val(json.ext_data.PRIORITY);
                                        }
                                    }
                                }
                            });
                        });
                        /*.rowFocus({rfSetDefFocus: true, rfFocusCallBack: function(){
                            var p = {wid: $(this).parents('table:first').attr('data-wid'), modelid: $(this).attr('data-modelid')};
                            $.getJSON('listWaresStackModelSites', p, listWaresStackModelSite);
                        }});*/
            }
        }

        function listWaresStackModelSite(json) {
            if (!showErr(json)) {
                var html = '<table><thead><tr>\
                                <th ksort="text">Штабель</th>\
                                <th ksort="digit" title="Количество паллет">КП</th>\
                            </tr></thead><tbody>';
                for (var i=0; i<json.data.length; i++){
                    var tr = json.data[i];
                    html += '<tr>'+
                                '<td class="text">' + tr.SNAME + '</td>'+
                                '<td class="number">' + tr.PALCNT + '</td>'+
                            '</tr>';
                }  
                html += '</tbody></table>';
                
                $container.find('>div:first>div:last').html(html)
                    .find('table').kTblScroll().kTblSorter();
                
            }
        }
    }
})(jQuery);


