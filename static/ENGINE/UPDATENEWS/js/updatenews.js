$(document).ready(function() {

    function ntobr(s){
        return s.replace(/\r\n|\r|\n/g, '<br>');
    }

    var issuetracker_prefix_url = ''; //Префикс для URL задачи трэкера задач (подгружается динамически)

    function getRedmineLink(issuenumber) {
        if (issuenumber)
            return "<a href='" + issuetracker_prefix_url + issuenumber + "' target='_blank'>"+issuenumber+"</a>";
        else
            return '';
    }

    $.ajax({url: 'getIssueTrackerParams',
        dataType: 'json',
        async: false,
        success: function(JSON) {
            issuetracker_prefix_url = JSON.data.ISSUETRACKER_PREFIX_URL;
        }
    });

    $('div#updatenews').css({'float':'left',
'position':'relative',
'width':'100%'});
    $('input.Date').datepicker({showStatus: true,
                            dateFormat: 'dd.mm.yy',
                            duration: "fast",
                            showOn: "button",
                            buttonImage: eng_img + "/datetime/calendar.gif",
                            buttonImageOnly: true });
    $('input#dbeg').val(getToday());
    $('input#dend').val(IncStrDateByDays(getToday(),1));
    $('a#idgo').unbind('click').bind('click', GetUpdateNews);

    function GetUpdateNews(){
        var dbeg = $('input#dbeg').val(),
            dend = $('input#dend').val();
        $('div#updatenews').empty();
        $.ajax({
                url: 'getupdatenews',
                data: {
                    dbeg: dbeg,
                    dend: dend,
                },
                success: function (JSON) {
                    if (JSON.data.length>0) {
                        var tbl = $('<table id="tblupdatenews"/>')
                                         .append($('<thead/>')
                                            .append($('<tr/>')
                                                .append($('<th/>').addClass('Date').append(_('Дата')))
                                                .append($('<th/>').append(_('ФИО')))
                                                .append($('<th/>').append(_('Система')))
                                                .append($('<th/>').append(_('Описание')))
                                                .append($('<th/>').append(_('Номер задачи')))
                                               ))
                                         .append($('<tbody/>'));

                        var tbody = $("tbody",tbl);
                        for (var i = 0; i < JSON.data.length; i++){
                            var rowspan = JSON.data[i].SYSINFO.length;

                            var html = "<tr><td class='Date' rowspan='"+rowspan+"'>"+JSON.data[i].UPLOAD_STAMP+"</td>"+
                                              "<td style='text-align: left;' rowspan='"+rowspan+"'>"+JSON.data[i].FIO+"</td>";

                            for(var j=0; j < rowspan; j++) {
                                if(j>0) html += "<tr>";
                                html += "<td style='text-align: left;'>"+JSON.data[i].SYSINFO[j].SHOW_NAME+"</td>"+
                                        "<td style='text-align: left;'>"+ntobr(JSON.data[i].SYSINFO[j].DESCRIPTION)+"</td>"+
                                        "<td style='text-align: right;'>"+getRedmineLink(JSON.data[i].SYSINFO[j].REDMINE_URL)+"</td></tr>";
                            }

                            /*tbl.find('tbody').append($('<tr>')
                                                .append($('<td>').addClass('Date').append(JSON.data[i].UPLOAD_STAMP))
                                                .append($('<td>').css('text-align', 'left').append(JSON.data[i].FIO))
                                                .append($('<td>').css('text-align', 'left').append(JSON.data[i].DESCRIPTION))
                                                );*/
                            tbody.append(html);
                        }
                        $('div#updatenews').append(tbl);

                        $('#tblupdatenews').kScrollableToDown(
                            {widths: {0: '120px',  4: '100px'}}
                            );
                    }
                    else{
                        $('div#updatenews').append(_('Обновлений не найдено!'));
                    }
                },
                dataType: 'json',
                async: false

            });
    }
});


