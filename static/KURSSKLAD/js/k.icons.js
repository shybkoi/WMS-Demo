(function(jQuery){
    $.tdWaresType = function(WaresType){
        if (WaresType=='1') return '<td title="Весовой товар"><img src="'+sps_img.KURSSKLAD+'/balance.png" border="0"></td>';
        else return '<td title="Штучный товар"><img src="'+sps_img.KURSSKLAD+'/box.png" border="0"></td>';
    };
    
    $.iconYesNo = function(YesNo){
        if (YesNo) return '<img src="'+sps_img.KURSSKLAD+'/YesNo/yes.png" border="0">';
        else return '<img src="'+sps_img.KURSSKLAD+'/YesNo/no.png" border="0">';
    };
    
    function docStatusImgPath(status){
        switch (status){ 
            case "0": 
                return sps_img.KURSSKLAD+'/status/doc/forming.png';
            case "1": 
                return sps_img.KURSSKLAD+'/status/doc/formed.png';
            case "s": 
                return sps_img.KURSSKLAD+'/status/doc/sent.png';
            case "e": 
                return sps_img.KURSSKLAD+'/status/doc/closed.png';
            case "i": 
                return sps_img.KURSSKLAD+'/status/doc/importing.png';
            case "v": 
                return sps_img.KURSSKLAD+'/status/doc/checked.png';
            case "c": 
                return sps_img.KURSSKLAD+'/status/doc/coming.png';
            case "g": 
                return sps_img.KURSSKLAD+'/status/doc/selecting.png';
            case "w": 
                return sps_img.KURSSKLAD+'/status/doc/came.png';
            case "2": 
                return sps_img.KURSSKLAD+'/status/doc/selected.png';
            case "x": 
                return sps_img.KURSSKLAD+'/status/doc/exporting.png';
            case "k":
                return sps_img.KURSSKLAD + '/status/doc/controlling.png';
            case "У": 
                return sps_img.KURSSKLAD+'/status/doc/deleted.png';
            case "К": 
                return sps_img.KURSSKLAD+'/status/doc/korrecting.png';
            case "А": 
                return sps_img.KURSSKLAD+'/status/doc/aorder.png';
            case "П": 
                return sps_img.KURSSKLAD+'/status/doc/korrecting.png';
        }     
    };
    
    function docStatusTitle(status,title){
        if (title) return title;
        else switch (status){ 
            case "0": return 'Формируемый';
            case "1": return 'Сформированный';
            case "s": return 'Отправленный';
            case "e": return 'Закрытый';
            case "i": return 'Импортируемый';
            case "v": return 'Проверенный';
            case "c": return 'Принимаемый';
            case "g": return 'Отбираемый';
            case "w": return 'Принятый';
            case "2": return 'Отобранный';
            case "x": return 'Экспортируемый';
            case "k": return 'На контроле';
            case "У": return 'Удаленный';
            case "К": return 'Корректирующий';
            case "А": return 'Атозаказ';
            case "П": return 'Полученный';
        } 
        return '';
    }
    
    $.tdDocStatus = function(status,title){
		if (status)
			return '<td title="'+docStatusTitle(status,title)+'"><img src="'+docStatusImgPath(status)+'" border="0"></td>';
		else
			return '<td></td>';
    };
    
    $.fn.tdDocStatus = function(status,title){
        return this.attr('title',docStatusTitle(status,title)).html('<img src="'+docStatusImgPath(status)+'" border="0">');
    };    
    
    $.optionDocStatus = function(status,title,restr){
        if (status===false){
            if (!title) title = 'Без фильтра';
            return '<option value="null" style="padding-left:20px;">'+title+'</option>';
        }

        function restrict(r) {
            return r != undefined ? ' restrict="' + r + '" ' : '';
        }        
        
        var html = '<option value="'+status+'"' +
            restrict(restr) +
            ' style="background-image:URL(' + docStatusImgPath(status) + ');background-repeat:no-repeat;padding-left:20px;">';

        html += docStatusTitle(status, title) + '</option>';
        return html;
    };
    
    function taskStatusImgPath(status){
        return sps_img.KURSSKLAD+'/status/task/'+status+'.png';
    };
    
    $.optionTaskStatus = function(status,title){
        if (status===false){
            if (!title) title = 'Без фильтра';
            return '<option value="null" style="padding-left:20px;">'+title+'</option>';
        }    
        
        var html = '<option value="'+status+'" style="background-image:URL('+taskStatusImgPath(status)+');background-repeat:no-repeat;padding-left:20px;">';
        switch (status){ 
            case "0": 
                html += (title ? title : 'Ожидает выполнения'); break;
            case "1": 
                html += (title ? title : 'Выполняется'); break;
            case "2": 
                html += (title ? title : 'Выполнено успешно'); break;
            case "3": 
                html += (title ? title : 'Выполнено с ошибкой'); break;
            case "4": 
                html += (title ? title : 'Отложено'); break;
        }     
        html += '</option>';
        return html;
    };
    
    function imgTaskStatus(status){
        if (status=='+') return '+';
        else if (status=='-') return '-';
        else return '<img src="'+taskStatusImgPath(status)+'" border="0">';
    };
    
    function titleTaskStatus(status){
        switch (status){ 
            case "0": 
                return 'Ожидает выполнения';
            case "1": 
                return 'Выполняется';
            case "2": 
                return 'Выполнено успешно';
            case "3": 
                return 'Выполнено с ошибкой';
            case "4": 
                return 'Отложено';
            case "5": 
                return 'Ожидает подтверждения';
            case "О": 
                return 'Ошибочное';
        }     
    };
    
    $.tdTaskStatus = function(status,title){
        return '<td title="'+(title ? title : titleTaskStatus(status)) +'">'+imgTaskStatus(status)+'</td>';
    };    
    
    $.fn.tdTaskStatus = function(status,title){
        return this.attr('title',title ? title : titleTaskStatus(status) ).html( imgTaskStatus(status) );
    };    
    
    $.tdPlusMinus = function(status,title,attr){
        if (status=='0'){
            if (title) 
                return '<td title="' + title + '"' + (attr ? ' ' + attr : '') + '>' +
                            '<img src="' + eng_img + '/actions/delete.png" border="0">' +
                        '</td>';
            else 
                return '<td' + (attr ? ' ' + attr : '') + '>' + 
                            '<img src="'+eng_img+'/actions/delete.png" border="0">' +
                        '</td>';
        }
        else
        if (status=='1'){
            if (title) 
                return '<td title="' + title +'"' + (attr ? ' ' + attr : '') + '>' +
                            '<img src="' + eng_img + '/actions/add.png" border="0">' + 
                        '</td>';
            else 
                return '<td' + (attr ? ' ' + attr : '') + '>' +
                            '<img src="' + eng_img + '/actions/add.png" border="0">' +
                        '</td>';
        }
        else
            return '<td' + (attr ? ' ' + attr : '') + '>&nbsp;</td>';
    };

    $.tUnitStatusImgPath = function(s) {
        switch(s) {
            case "0": return '<img src="'+sps_img.KURSSKLAD+'/status/tunit/no.png" title="Не активен">';
            case "1": return '<img src="'+sps_img.KURSSKLAD+'/status/tunit/yes.png" title="Активен">';
            case "g": return '<img src="'+sps_img.KURSSKLAD+'/status/tunit/selecting.png" title="Отбираемая">';
            case "s": return '<img src="'+sps_img.KURSSKLAD+'/status/tunit/sent.png" title="Отправленная">';
        }
    };
})(jQuery);