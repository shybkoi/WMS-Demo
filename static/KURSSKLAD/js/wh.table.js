;
(function ($) {
  var tFootData = {};
  $.whTblData = {
      tbl: {},
      tFoot: function(tblId){
          return tFootData[tblId];
      }
  };

//=====================================================================================================================
// Общие функции
//=====================================================================================================================
  function optGetVal(opt, param) {
      if (opt) {
          if (typeof opt == 'function') {
              if (param) {
                  if (typeof param == 'object') {
                      return opt.apply(null, param);
                  }
                  else {
                      return opt.call(null, param);
                  }
              }
              else
                  return opt();
          }
          else {
              return opt;
          }
      }
      else
          return '';
  }

//=====================================================================================================================
// Таблица документов
//=====================================================================================================================

  function trHTML(tr, options){
      var html = '';
      for (var j = 0; j < options.clmSortKey.length; j++) {
          var item = options.clmSortKey[j];
          if (options['td' + item]){
              html += optGetVal(options['td' + item], [tr, options['fld' + item]]);
          }
      }
      return html;
  }

  $.whTblTrHTML = trHTML;

  $.fn.whTblTrHTML = function(tr){
      var tblId;
      if ($(this).is('table')) tblId = $(this).attr('id');
      else if ($(this).is('tr')) tblId = $(this).parents('table:first').attr('id');
      var O = $.whTblData.tbl[tblId];
      return trHTML(tr, O);
  };

  $.fn.whTblThIndex = function(thName){
      var res = -1;
      $(this).find('thead>tr>th').each(function (index) {
          if ($(this).attr('data-clm') == thName)
              res = index;
      });
      return res;
  };

  $.fn.whTblTd = function (thName) {
      return $(this).find('>td').eq($(this).parents('table:first').whTblThIndex(thName));
  };

    $.whTblHTML = function(JSON, O){
      if (window.showErr && showErr(JSON)) return;

      if (O.idTable) {
          $.whTblData.tbl[O.idTable] = O;
          tFootData[O.idTable] = {'cntRecords': JSON.data.length};
      }

      var html = '<table' + (O.idTable ? (' id="' + O.idTable + '"') : '') + '><thead>' +
          (O.theadExt ? optGetVal(O.theadExt) : '') + '<tr>';
      for (var j=0; j<O.clmSortKey.length; j++){
          var item = O.clmSortKey[j];
          html += (O['th' + item] ? optGetVal(O['th' + item]) : '').replace(/^<th/g, '<th data-clm="' + item + '"');
      }
      html += '</tr></thead><tbody>';
      for (var i=0; i<JSON.data.length; i++){
          var tr = JSON.data[i];
          html += '<tr';
          if (O.attrTr)
              html += ' ' + optGetVal(O.attrTr, [tr]);
          if (O.footCalc && O.idTable)
              optGetVal(O.footCalc,[tr, tFootData[O.idTable]]);
          html += '>' + trHTML(tr, O) + '</tr>';
      }
      html += '</tbody>' + (O.idTable && O.footSet ? optGetVal(O.footSet, [tFootData[O.idTable], O.clmSortKey]) : '') + '</table>';
      return html;
  };
})(jQuery);