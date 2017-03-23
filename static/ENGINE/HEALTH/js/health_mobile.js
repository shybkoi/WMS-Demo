$(document).ready(function(){
    $('body').attr('leftmargin',"0").attr('topmargin',"0").attr('marginwidth',"0").attr('marginheight',"0");
    DefaultVariables();
    AjaxGetSliceMobile(0);
});
function DefaultVariables(){
    slices = ['PACKET', 'SALE', 'AORDERSTAT', 'AORDER', 'RORDER', 'PRICING', 'WSETPRLIST', 'MAINSUPPLIERS', 'SHARE', 'ROBOTS', 'PYTHON'];
    slicesrc = ['/KURS/CONTRSYSPACK/images/logo.png',
                '/ONLINE/CASHONLINE/images/logo.png',
                '/KURS/AORDER/images/autoorder_stats.png',
                '/KURS/AORDER/images/logo.png',
                '/KURS/WSETFDU/images/logo.png',
                '/KURS/PRICING/images/logo.png',
                '/KURS/WSETPRLIST/images/logo.png',
                '/KURS/AMWARESSET/MAINSUPPLIER/images/logo.png',
                '/KURS/MSHARES/images/logo.png',
                '/KURS/images/robots.png',
                '/ENGINE/images/apps/firepy.png'];
}
function RotateRefresh(){
    $('img.refreshImg').rotate({
        angle:0, 
        animateTo:360, 
        callback: RotateRefresh,
        easing: function (x,t,b,c,d){
            return c*(t/d)+b;
        }
     });
}
function AjaxGetSliceMobile(slice, onlythis){
    if (slice < slices.length){
        if (onlythis) {
            $('div.Image:eq('+slice+')').html('<img class="refreshImg" width="40px" height="40px" src="/ENGINE/images/actions/update_arrow.png"/>');
            RotateRefresh();
        }
        $.getJSON('get_block',{'rmode':'jsontmpl',refresh_block:slices[slice].toLowerCase(),ismobile:'1'},function(data){
            if (onlythis) $('#health-detail div.row:eq('+slice+')').replaceWith(data.data.TMPL);
            else $('#health-detail').append(data.data.TMPL);
            $('#health-detail').find('div.row:eq('+slice+')').find('td:eq(0)')
                .html('<div class="Image"><img src="'+slicesrc[slice]+'" width="40px" height="40px"></div>');
            $('div.Image:eq('+slice+')').click(function() {
                AjaxGetSliceMobile($('div.Image').index(this), true);
            });
            if(onlythis)
                AjaxGetSliceMobile(slices.length);
            else
                AjaxGetSliceMobile(slice+1);
        });
    }
}