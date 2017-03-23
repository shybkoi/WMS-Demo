/**
 *  Всплывающая информация о местоположении
 *  @version 2.0.1
 *   
 *  @author Denys Skychko (denysskychko@gmail.com)
 */
(function($){
    $.titleInfo = function(){
        var $this = $(this),
            w = 0,
            h = 0;
        if( $this.hasClass('clShTitle') ) 
            return;
        $.getJSON('titleInfo',{sid:$this.kID()},function(JSON){
            if( !showErr(JSON) ){
                var data = {'keys':[]};
                var obj;
                var mx = 1, my = 1, mz = 1;
                for(var i=0;i<JSON.data.length;i++){
                    obj = JSON.data[i];
                    if( obj.SITEID != '' ){
                        if( data['s_'+obj.SITEID] == undefined ){
                            data.keys.push( 's_'+obj.SITEID );
                            data['s_'+obj.SITEID] =
                                   {'SNAME':obj.SNAME,
                                    'SPCODE':obj.SPCODE,
                                    'SPNAME':obj.SPNAME,
                                    'SLENGTH':parseInt(obj.SLENGTH,10),
                                    'SWIDTH':parseInt(obj.SWIDTH,10),
                                    'SHEIGHT':parseInt(obj.SHEIGHT,10),
                                    'X':parseInt(obj.X,10),
                                    'Y':parseInt(obj.Y,10),
                                    'Z':parseInt(obj.Z,10),
                                    'PALLETS':{'keys':[]}};
                            if(parseInt(obj.SWIDTH,10) > w) w = parseInt(obj.SWIDTH,10);
                            h += parseInt(obj.SHEIGHT,10);
                            if( obj.PALLETID != '' ){
                                data['s_'+obj.SITEID]['PALLETS'].keys.push( 'p_'+obj.PALLETID );
                                data['s_'+obj.SITEID]['PALLETS']['p_'+obj.PALLETID] = {'PALLETID':obj['PALLETID'],
                                                                                       'PNUMBER':obj['PNUMBER'],
                                                                                       'PBARCODE':obj['PBARCODE'],
                                                                                       'PTYPE':obj['PTYPE'],
                                                                                       'PSTATUS':obj['PSTATUS'],
                                                                                       'WARES':[]}
                                if( obj.WARESID != '' )
                                    data['s_'+obj.SITEID]['PALLETS']['p_'+obj.PALLETID]['WARES'].push({'WARESID':obj.WARESID,
                                                                                                       'WCODE':obj.WCODE,
                                                                                                       'WNAME':obj.WNAME,
                                                                                                       'WAMOUNT':obj.WAMOUNT,
                                                                                                       'UNAME':obj.UNAME,
                                                                                                       'VIEWAMOUNT':viewQuantity(obj.WAMOUNT,obj.VIEWUFACTOR,obj.VIEWUCODE,obj.MAINUFACTOR,obj.MAINUCODE)});
                            }
                        
                            if( parseInt(obj.X,10) + parseInt(obj.SLENGTH,10) - 1 > mx )
                                mx = parseInt(obj.X,10) + parseInt(obj.SLENGTH,10) - 1;
                            if( parseInt(obj.Y,10) + parseInt(obj.SWIDTH,10) - 1 > my )
                                my = parseInt(obj.Y,10) + parseInt(obj.SWIDTH,10) - 1;
                            if( parseInt(obj.Z,10) + parseInt(obj.SHEIGHT,10) - 1 > mz )
                                mz = parseInt(obj.Z,10) + parseInt(obj.SHEIGHT,10) - 1;
                        }
                        else{
                            if( obj.PALLETID != '' ){
                                if( data['s_'+obj.SITEID]['PALLETS']['p_'+obj.PALLETID] == undefined ){
                                    data['s_'+obj.SITEID]['PALLETS'].keys.push( 'p_'+obj.PALLETID );
                                    data['s_'+obj.SITEID]['PALLETS']['p_'+obj.PALLETID] = {'PALLETID':obj['PALLETID'],
                                                                                           'PNUMBER':obj['PNUMBER'],
                                                                                           'PBARCODE':obj['PBARCODE'],
                                                                                           'PTYPE':obj['PTYPE'],
                                                                                           'PSTATUS':obj['PSTATUS'],
                                                                                           'WARES':[]}
                                    if( obj.WARESID != '' )
                                        data['s_'+obj.SITEID]['PALLETS']['p_'+obj.PALLETID]['WARES'].push({'WARESID':obj.WARESID,
                                                                                                           'WCODE':obj.WCODE,
                                                                                                           'WNAME':obj.WNAME,
                                                                                                           'WAMOUNT':obj.WAMOUNT,
                                                                                                           'UNAME':obj.UNAME,
                                                                                                           'VIEWAMOUNT':viewQuantity(obj.WAMOUNT,obj.VIEWUFACTOR,obj.VIEWUCODE,obj.MAINUFACTOR,obj.MAINUCODE)});
                                }
                                else
                                    if( obj.WARESID != '' )
                                        data['s_'+obj.SITEID]['PALLETS']['p_'+obj.PALLETID]['WARES'].push({'WARESID':obj.WARESID,
                                                                                                           'WCODE':obj.WCODE,
                                                                                                           'WNAME':obj.WNAME,
                                                                                                           'WAMOUNT':obj.WAMOUNT,
                                                                                                           'UNAME':obj.UNAME,
                                                                                                           'VIEWAMOUNT':viewQuantity(obj.WAMOUNT,obj.VIEWUFACTOR,obj.VIEWUCODE,obj.MAINUFACTOR,obj.MAINUCODE)});
                            }
                        }
                    }
                }
                
                //var H = parseInt(JSON.ext_data.SHEIGHT,10);
                var H = mz;
                //var W = parseInt(JSON.ext_data.SWIDTH,10);
                var W = mx;
                //var L = parseInt(JSON.ext_data.SLENGTH,10);
                //console.log(H,W)
                
                var CH, CHK, CHL, CW, CWK, CWL;
                if( H > W ){
                    CH = H; CHK = 'Z'; CHL = 'SHEIGHT';
                    CW = W; CWK = 'Y'; CWL = 'SWIDTH';
                }
                else{
                    CH = W; CHK = 'Y'; CHL = 'SWIDTH';
                    CW = H; CWK = 'Z'; CWL = 'SHEIGHT';
                }
                /*if( L > CW ){
                    if( L > CH ){
                        CW = CH; CWK = CHK; CWL = CHL;
                        CH = L; CHK = 'X'; CHL = 'SLENGTH';
                    }
                    else
                        CW = L; CWK = 'X'; CWL = 'SLENGTH';
                }*/
                
                var width_popup = 480;
                //var height_popup = 230;
                console.log(h,w)
                var height_popup = 20+2*10+60/w*h;
                var height = (height_popup-20-2*10);
                var width = 100;
                var dvH = height/h;
                var dvW = 60/w;
                var br = 3;
                var mp = '';
                var d;
                var it = 0, il = 0, iw, ih, har;
                if(dvW > dvH){
                    il = (dvW-dvH)/2;
                    iw = dvH-br*2;
                    ih = dvH-br*2;
                    har = 'height';
                }
                else{
                    it = (dvH-dvW)/2;
                    iw = dvW-br*2;
                    ih = dvW-br*2;
                    har = 'width';
                }
                var imgPalGray = 'palGray.png';
                var imgPalGreen = 'palGreen.png';
                var imgPalRed = 'palRed.png';
                var imgFreePal = 'free.png';
                var arrow = sp_img+'/arrow.png';
                
                //dvH = Math.min(dvW,dvH);
                //dvW = dvH;
                var border = '';
                for(var i=0;i<data.keys.length;i++){
                    d = data[data.keys[i]];
                    border = 'border:'+br+'px solid #1B2249;';
                    var img = d['SPCODE'] == 'S'?(d.PALLETS.keys.length > 0?imgPalGreen:imgFreePal):(d.PALLETS.keys.length > 0?imgPalGray:'');
                    //console.log(img)
                    
                    mp += '<div style="width:'+(dvW*d[CWL])+'px;height:'+dvH*d[CHL]+'px;position:absolute;\
                                       top:'+(20+10+dvH*(CH-(d[CHK]+d[CHL]-1)))+'px;\
                                       left:'+(20+(parseInt(d['X'],10)-1)*dvW)+'px">'+
                                
                                /*<div style="float:left;height:100%;widht:20px;color:RGB(255,255,255);\
                                            text-shadow: black 1px 1px 1px;\
                                            line-height:'+dvH*d[CHL]+'px;">'+d.SNAME.split('-')[2]+'</div>\*/
                                '<div'+(d.PALLETS.keys.length > 0 ? ' class="dvLChild" ' : ' ')+
                                        'site="'+data.keys[i]+'" style="\
                                            border:'+br+'px solid #1B2249;\
                                            height:'+(dvH*d[CHL]-br*2)+'px;'+
                                            (d.PALLETS.keys.length > 0 ? 'cursor:pointer;': '')+
                                            'float:left;\
                                            background-color:black;\
                                            width:'+(dvW*d[CWL]-br*2)+'px;\
                                        ">\
                                    <div style="position:relative;'+
                                                //top:'+it*d[CHL]+'px;\
                                                //left:'+il+'px
                                                'background: url('+sp_img+'/'+img+') 50% 50% no-repeat;'+
                                                'background-size:cover;'+
                                                'width:'+(dvW*d[CWL]-br*2)+'px;\
                                                height:'+(dvH*d[CHL]-br*2)+'px;">'+
                                            //img+
                                    '<div style="position:absolute;top:0;left:-20px;height:100%;width:20px;\
                                            text-shadow: black 1px 1px 1px;color:white;\
                                            ">'+((d.SNAME.split('-')[2])||(d.SNAME))+'</div>'+
                                    '</div>'+
                                '</div>\
                           </div>';
                }
                    
                var ahtml = '<div style="width:100%;\
                                         height:20px;\
                                         text-align:center;\
                                         font-weight:800;\
                                         font-size:12pt;\
                                         borderbottom:1px solid #5C5C5C;\
                                         background-color:#5C5C5C;\
                                         color:#ffffff;\
                                         text-shadow: black 1px 1px 1px;">'+$this.attr('title').split(' ')[0]+'</div>\
                             <div style="width:100%;height:'+(height_popup-20)+'px;background-color:RGB(255;255;255) !important;">\
                                <div style="width:60px;background-color:#5C5C5C;height:'+(height_popup-20-2*10)+'px;float:left;padding:10px 10px 10px 20px;">'+mp+'</div>\
                                <div style="width:'+(width_popup-60-20-30)+'px;height:'+(height_popup-20-2*10)+'px;float:left;padding:10px;background-color:RGB(255,255,255);">\
                                    <div style="width:'+(width_popup-60-20-30)+'px;height:'+(height_popup-20-2*10)+'px;position:absolute;z-index:9999;background-color:RGB(255,255,255);">\
                                        <div id="dvWHPal" style="width:100%;height:40%;">Стеллаж пуст.</div>\
                                        <div id="dvWHWar" style="width:100%;height:60%;"></div>\
                                    </div>\
                                    <div style="width:'+(width_popup-60-20-30)+'px;height:'+(height_popup-20-2*10)+'px;position:absolute;z-index:9998">\
                                        <div id="dvPArrow" style="widht:50px;height:50px;position:absolute;left:-40px;display:none;">\
                                            <img src="'+arrow+'" style="width:100%;height:100%;">\
                                        </div>\
                                    </div>\
                                </div>\
                             </div>';
                $this.popup({dvID:'pTitle',html:ahtml,width:width_popup,height:height_popup,callback:function(){
                        $('#pTitle').find('div.dvLChild').unbind('click').click(function(){
                            if( $(this).hasClass('aktivSite') )
                                return;
                            $('#pTitle').find('div.aktivSite').removeClass('aktivSite');
                            $(this).addClass('aktivSite');
                            var top = $(this).parent().get(0).offsetTop-30+$(this).parent().height()/2-26;
                            $('#dvPArrow').css({'top':top}).show();
                            var num = $(this).attr('site');
                            //var pal = data[data['keys'][num]].PALLETS;
                            var pal = data[num].PALLETS;
                            var html = '<table style="width:100%;"><thead><tr>\
                                            <th>Номер</th>\
                                            <th>ШК</th>\
                                        </tr></thead><tbody>';
                            for(var i=0;i<pal['keys'].length;++i)
                                html += '<tr pal="'+i+'">\
                                            <td>'+pal[pal['keys'][i]].PNUMBER+'</td>\
                                            <td>'+pal[pal['keys'][i]].PBARCODE+'</td>\
                                        </tr>';
                            html += '</tbody></table>';
                            $('#dvWHPal').html(html).find('table:first').kTblScroll().rowFocus({rfFocusCallBack:function(){
                                    if(pal['keys'].length == 1){
                                        $('#dvWHWar').css({'height':'100%'});
                                        $('#dvWHPal').hide();
                                    } else {
                                        $('#dvWHWar').css({'height':'60%'});
                                        $('#dvWHPal').show();
                                    }
                                    var num = $(this).attr('pal');
                                    var war = pal[pal['keys'][num]]['WARES'];
                                    var html = '<table style="width:100%;"><thead>'+
                                                (pal['keys'].length == 1?('<tr><th colspan='+( useviewunit ? '4' : '3' )+'>'+pal[pal['keys'][0]].PNUMBER+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ШК: '+pal[pal['keys'][0]].PBARCODE+'</th></tr>'):'')+
                                                '<tr>\
                                                    <th>Код</th>\
                                                    <th>Наименование</th>'+
                                                    ( useviewunit ? '<th>Кол-во</th>' : '' )+
                                                    '<th>Итого</th>\
                                                </tr></thead><tbody>';
                                    for(var i=0;i<war.length;++i)
                                        html += '<tr>\
                                                    <td>'+war[i].WCODE+'</td>\
                                                    <td class="text">'+war[i].WNAME+'</td>'+
                                                    //( useviewunit ? '<td>'+war[i].VIEWAMOUNT+'</td>' : '' )+
                                                    ( useviewunit ? '<td>'+war[i].VIEWAMOUNT+'</td>' : '' )+
                                                    '<td class="number">'+kNumber(war[i].WAMOUNT,3)+'</td>\
                                                </tr>';
                                    $('#dvWHWar').html(html).find('table:first').kTblScroll();
                                }
                            });
                        }).eq(0).click();
                    }
                }); 
            }                   
        });
    }
})(jQuery);