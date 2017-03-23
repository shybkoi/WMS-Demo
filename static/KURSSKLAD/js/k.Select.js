/*
	kast 12.09.2012
	
	fclass - класс td подлежащий группировке
	recalculation[{// пересчет выбранных полей при change
		td:{'eq':2,      -- td по которой пойдёт пересчет
             class:'в разработке',
	         id:'в разработке'},
		th:{'id':'sumq', -- th в которую пишем пересчет
		  class:'в разработке',
		     eq:'в разработке'
		} 
	}]
    recalccount - кол-во видимых
*/


$.fn.kSelect = function(options) {
	var $self = this;
	
	var options = $.extend({
					'recalculation':false,
                    'recalccount':false,
                    'data':false
			   },options);
	
	$self.css({'text-transform':'none'}).addClass('kfilter');
	
	var $tbl = options.tbl || $(this).parents('table:first');
	var $tbl_tbody_tr = $tbl.find('tbody>tr');
    
    if (options.recalculation) {
        for (var i=0;i<options.recalculation.length;i++) {
            var $selector = $('#'+options.recalculation[i].th.id)
            $selector.attr('first_sel_sum',$selector.text());
        }
    }
    if (options.data && typeof options.data  == 'object') {
        var html = '<option value=all>------</option>';
        for (var i in options.data) {
            html += (i ? '<option value="'+options.data[i]+'">'+options.data[i]+'</option>' : '');
        }
        $self.append(html)
    }
	
	$self.change(function(){
		var value = $(this).val() || '';
		if (value=='all') {
			$tbl_tbody_tr.removeClass('hide');
            if (options.recalculation) {
                for (var i=0;i<options.recalculation.length;i++) {
                    var $selector = $('#'+options.recalculation[i].th.id)
                    $selector.text($selector.attr('first_sel_sum'));
                }
            }
            //$tbl.kTblScroll({quick:false}).kTblSorter();
		}
		else {
			$tbl_tbody_tr.removeClass('hide')
            
            if (value.length) {
                $tbl_tbody_tr.find('td.'+options.fclass).each(function() {
                    var $this = $(this), text = $this.text()?escape($this.text()):'Без наименования';
                    
                    if (text!=escape(value)) $this.parents('tr:first').addClass('hide');
                })
            }
            if (options.recalculation) {
                for (var i=0;i<options.recalculation.length;i++) {
                    var find = '>td:eq('+options.recalculation[i].td.eq+')', sum = 0.0;
                    $tbl_tbody_tr.filter(':visible').each(function(){
                        sum += parseFloat($(this).find(find).text());
                    });
                    $('#'+options.recalculation[i].th.id).html(kFloat(sum,3));
                }
            }
            //$tbl.kTblScroll().kTblSorter();
		}
		
        
        if (options.recalccount) {
            $tbl.find('>tfoot>tr>th:first').text($tbl_tbody_tr.filter('tr:visible').length);
        }
        $self.parents('tfoot:first').find('select.kfilter')
            .not($self).each(function(){
                $(this).find('option:first').attr('selected','selected');
            });
        $tbl.kTblScroll().kTblSorter();
	});
	return $self;
}