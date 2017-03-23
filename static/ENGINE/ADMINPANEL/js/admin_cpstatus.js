$(
  function()
  {
    var tmr = "";
    //Features
    $("#tbl_threads")
    //sortable
    .tablesorter({widgets:['zebra'],headers:{0:{sorter:"digit"}, 1:{sorter:"digit"}, 2:{sorter:"currency"},  3:{sorter: "digit"}, 4:{sorter: "text"}}});
    
    $("select#refresh_time").unbind("change").bind("change", function() {
        ChangeRefreshTime();
    });
    
    function set_timer(freq) {
        tmr = $.timer(freq, function(){
            $.ajax({
                url: 'cpstatus',
                dataType: 'json',
                data: {'simplelist': 'true'},
                async: true,
                success: function(JSON) {
                    if(JSON.data && JSON.data.length) {
                        var tbl = $("#tbl_threads");
                        var tblbody = tbl.find("tbody").empty();
                        for(var i=0;i<JSON.data.length;i++) {                        
                            tblbody.append($.format('<tr><th>{0}</th><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>', 
                                                JSON.data[i].NUMBER,
                                                JSON.data[i].ID,
                                                JSON.data[i].IDLE_TIME,
                                                JSON.data[i].LAST_REQ_TIME,
                                                JSON.data[i].URL));
                        }
                    }
                    
                }
            });
            $("#tbl_threads")
                //sortable
                .tablesorter({widgets:['zebra'],headers:{0:{sorter:"digit"}, 1:{sorter:"digit"}, 2:{sorter:"currency"},  3:{sorter: "digit"}, 4:{sorter: "text"}}});
        });
    }
    
    function ChangeRefreshTime() {
        var val = $("select##refresh_time").val();
        if(val=="n") {
            if(typeof(tmr)!='string') {
                tmr.stop(); tmr="";
            }
        } else {
            freq = parseInt(val)*1000;
            if(typeof(tmr)!='string') { tmr.stop(); tmr=""; }
            set_timer(freq);
        }
    }
    
  }
);
