$(document).ready(function(){
  $.datepicker.setDefaults($.extend($.datepicker.regional['ru']));
  $('#bdate,#edate,#prbdate,#predate').datepicker().mask('99.99.9999').val(kToday());
  $('#prbdate').val(kToday(-30));
	
  $('form').unbind('submit').submit(function(){
    alert('Фильтр не настроен!');
    return false;
  });

  $("#btnPrint").click(function(){
    if ($("#tbl").length){
        var wnd = window.open(sp_reports+'/print.html');
        wnd.onload = function(){
            wnd.document.getElementById("tbl").innerHTML = $("#tbl").printHTML();
        };
    }
    else alert('Нет данных для печати');
  });  
  
  $.getJSON('getObjects',function(JSON){
    for(var i=0;i<JSON.data.length;++i)
      $('#fromobj').append('<option value="'+JSON.data[i].OBJID+'" '+(JSON.data[i].OBJID==JSON.ext_data.curzone?'selected':'')+'>'+JSON.data[i].OBJNAME+'</option>');
	if (JSON.data.length == 1) 
      $('#fromobj').attr({'disabled':'disabled'})
  
    var containerheight = kScreenH();
    $("#dvMain").css({"height": containerheight, 'overflow-y': 'auto'});
    $("#toobjname").kObjAutoComplete({hiddenName:"toobj"});
    $("#wares").kWaresLocate({idHE:"waresid"});

    $('form').unbind('submit').submit(function(){
      $('#dvMain').empty();
      $.getJSON('qData', $(this).kFormSubmitParam(), report);
      return false;
    });  

    function clickTreeElement() {
      var dv = $(this).attr('data-val');
      var $tr = $(this).parents('tr:first');
      if (dv == '-') {
        $('#tbody>tr[id^="' + $tr.attr('id') + '_"][data-treelvl='+ (kInt($tr.attr('data-treelvl')) + 1) + ']')
            .find('img.imgClick[data-val="-"]').click().end()
            .hide();
        if ($tr.nextAll(':visible:first').length) {
          $(this).replaceWith('<img class="imgClick" data-val="+" src="' + sp_img + '/tv-expandable.gif' + '"/>');
        }
        else {
          $(this).replaceWith('<img class="imgClick" data-val="+" src="' + sp_img + '/tv-expandable-last.gif' + '"/>');
        }
      }
      else if (dv == '+') {
        $('#tbody>tr[id^="' + $tr.attr('id') + '_"][data-treelvl='+ (kInt($tr.attr('data-treelvl')) + 1) + ']').show();
        $(this).replaceWith('<img class="imgClick" data-val="-" src="' + sp_img + '/tv-collapsable.gif' + '"/>');
      }
      $tr.find('>td:first img.imgClick').click(clickTreeElement);
    };
    
    function report(json){
      if (showErr(json))
        return;
      var R = {};
      for (var i=0; i<json.data.length; i++){
        var I = json.data[i];
        var q = kFloat(I.Q);
        if (!R[I.CLID]){
          R[I.CLID] = {
            'CLNAME': I.CLNAME,
            'Q': q,
            'WARES': {}
          }
        }
        else {
          R[I.CLID]['Q'] += q;
        }
        var W = R[I.CLID]['WARES'];
        if (!W[I.WID]){
          W[I.WID] = {
            'WCODE': I.WCODE,
            'WNAME': I.WNAME,
            'Q': q,
            'PRDATES': {}
          }
        }
        else {
          W[I.WID]['Q'] += q;
        }
        var PD = W[I.WID]['PRDATES'];
        var PrDate = kDate(I.PRDATE);
        if (!PD[kDate(I.PRDATE)]){
          var Spl = PrDate.split('.');
          PD[PrDate] = {
            'Q': q,
            'DOCS': {},
            'MS': new Date(Spl[2], Spl[1], Spl[0])
          }
        }
        else{
          PD[PrDate]['Q'] = q;
        }        
        var D = PD[PrDate]['DOCS'];
        if (!D[I.DOCID]){
          D[I.DOCID] = {
            'Q': q,
            'DOCNUM': I.DOCNUM,
            'DOCDATE': kDate(I.DOCDATE)
          }
        }        
        else{
          D[I.DOCID]['Q'] = q;
        }        
      }
      var html = '<table id=tbl><thead><tr><th>Наименование</th><th>Количество</th></tr></thead><tbody id=tbody>';
      var RSort = kObjectSort(R, 'CLNAME');
      for (var i=0; i<RSort.length; i++){
        var CL = RSort[i].val;
        html += '<tr id="tr_' + RSort[i].item + '" class=trTreeView data-treelvl=1>' + 
          '<td class=text>' +
            '<div class=dvLeft>'+
              '<img data-val="+" class="imgClick" src="' + sp_img + '/tv-expandable' + (i == (RSort.length - 1) ? '-last' : '') + '.gif">' +
            '</div>' +
            '<div class=dvLeft>'+ CL.CLNAME + '</div>' + 
          '</td>' + 
          '<td class=number>' + CL.Q + '</td></tr>';
        var WSort = kObjectSort(CL.WARES, 'WCODE');
        for (var j=0; j<WSort.length; j++){
          var W = WSort[j].val;
          html += '<tr id="tr_' + RSort[i].item + '_' + WSort[j].item + '" class=trTreeView data-treelvl=2 style="display: none">' + 
            '<td class=text>' + 
              '<div class=dvLeft>'+
                '<img data-val="=" src="' + sp_img + '/vertline.gif">' +
                '<img data-val="+" class="imgClick" src="' + sp_img + '/tv-expandable' + (j == (WSort.length - 1) ? '-last' : '') + '.gif">' +
              '</div>' +
              '<div class=dvLeft>(' + W.WCODE + ') ' + W.WNAME + '</div></td>' +
              '<td class=number>' + W.Q + '</td></tr>';
          var PDSort = kObjectSort(W.PRDATES, 'MS');            
          for (var k=0; k<PDSort.length; k++){
            var PD = PDSort[k].val;
            html += '<tr id="tr_' + RSort[i].item + '_' + WSort[j].item + '_' + PDSort[k].item + '" class=trTreeView data-treelvl=3 style="display: none">' + 
              '<td class=text>' + 
                '<div class=dvLeft>'+
                  '<img data-val="=" src="' + sp_img + '/vertline.gif">' +
                  '<img data-val="=" src="' + sp_img + '/vertline.gif">' +
                  '<img data-val="+" class="imgClick" src="' + sp_img + '/tv-expandable' + (k == (PDSort.length - 1) ? '-last' : '') + '.gif">' +
                '</div>' +
                '<div class=dvLeft>' + PDSort[k].item + '</div>' + 
              '</td>' + 
              '<td class=number>' + PD.Q + '</td></tr>';
            var DSort = kObjectSort(PD.DOCS, 'DOCNUM');
            for (var l=0; l<DSort.length; l++){
              var D = DSort[l].val;
              html += '<tr id="tr_' + RSort[i].item + '_' + WSort[j].item + '_' + PDSort[k].item + '_' + DSort[l].item +'" class=trTreeView data-treelvl=4 style="display: none">' + 
                '<td class=text>' + 
                  '<div class=dvLeft>'+
                    '<img data-val="=" src="' + sp_img + '/vertline.gif">' +
                    '<img data-val="=" src="' + sp_img + '/vertline.gif">' +
                    '<img data-val="=" src="' + sp_img + '/vertline.gif">' +
                    '<img src="' + sp_img + '/tv-item' + (l == (DSort.length - 1) ? '-last' : '') + '.gif">' +
                  '</div>' +
                  '<div class=dvLeft>' + D.DOCDATE + ' №' + D.DOCNUM + '</div>' +
                '</td>' +
                '<td class=number>' + D.Q + '</td></tr>';
            }            
          }
        }
      }
      html += '</tbody></table>';
      
      $('#dvMain').html(html).find('table:first img.imgClick').click(clickTreeElement);
    }
  });	
})
