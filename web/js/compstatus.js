var compStatusStatus = -1;
var compStatusAutomatic = -1;
var compStatusStartTime = -1;
var compStatusEndTime = -1;
var compStatusOffset = -1;

function convertTimeToStr(ms) {
    /* Convert the current time into a string to be displayed

    Args:
        ms: Number of milliseconds since epoch
    */
    let rs = ms;
    rs = Math.floor(rs/1000);
    let rd = Math.floor(rs/(60*60*24));
    rs = rs - rd * 60 * 60 *24;
    let rh = Math.floor(rs/(60 * 60));
    rs = rs - rh * 60 * 60;
    let rm = Math.floor(rs / (60));
    rs = rs - rm * 60;

    if (rd==0&&rh==0&&rm==0&&rs==0) {
        return "0s";
    }
    if (rd==0&&rh==0&&rm==0) {
        return rs+"s";
    }
    if (rd==0&&rh==0) {
        return rm+"m "+rs+"s";
    }
    if (rd==0) {
        return rh+"h "+rm+"m "+rs+"s";
    }
    return rd+"d "+rh+"h "+rm+"m "+rs+"s";

}

var doingLast30 = false;
var doingLast30Interval = null;
var doingLast30CancelMe = null;
function doingLast30Tick() {
    /* 

    Args:
    */
    var ms = compStatusStartTime - ((new Date()).getTime() - compStatusOffset);

    if (ms < 0)
        ms = 0;

    let opt = '';

    for ( let i=0;i<6;i++) {
        opt = "</div></span>" + opt;
        if (i!=3) {
            opt = ms % 10 + opt;
            ms = Math.floor(ms/10);
        }
        else {
            opt = '.' + opt;
        }
        opt = "<span style='position:relative;color:rgba(0,0,0,0);'>#<div style='width:100%;text-align:center;color:white;position:absolute;left:0px;top:0px;'>"+opt;
    }


    $("#competition_overlay_last_30_countdown").html(opt);

}

function stopLast30() {
    if (!doingLast30)
        return;
    $("#competition_overlay_last_30_swipe").hide();
    $("#competition_overlay_last_30").hide();
    clearInterval(doingLast30Interval);
    doingLast30 = false;
    if (doingLast30CancelMe)
        clearTimeout(doingLast30CancelMe);
    doingLast30CancelMe = null;
}

function compStatusPaint() {
    let opt = "";

    let shouldDoLast30 = false;

    if (compStatusAutomatic==1) {
        var seconds = (new Date()).getTime() - compStatusOffset;//lies... it's actually ms


        if (seconds<compStatusStartTime) {
            $("#competition_overlayTitle").html("Before Competition");
            let rs = compStatusStartTime-seconds;
            $("#competition_overlayLong").html("Please wait for the competition to begin.<br>"+convertTimeToStr(rs)+"<br>");
            $("#competition_overlay").show();
            opt="Before Competition<br>"+convertTimeToStr(rs);
            if (rs <= 15 * 1000) {
                shouldDoLast30 = true;
            }
        }
        else if (seconds<=compStatusEndTime) {
            $("#competition_overlay").hide();
            opt=convertTimeToStr(compStatusEndTime-seconds);
        }
        else {
            $("#competition_overlayTitle").html("After Competition");
            $("#competition_overlayLong").html("The competition has ended.<br>Pending submissions will be processed.<br>");
            $("#competition_overlay").show();
            opt="After Competition";
        }
    }
    else if(compStatusStatus==0) {
        $("#competition_overlayTitle").html("Before Competition");
        $("#competition_overlayLong").html("Please wait for the competition to begin.<br>There is no current starting time.<br>");
        $("#competition_overlay").show();
        opt="Before Competition";
    }
    else if(compStatusStatus==1) {
        $("#competition_overlay").hide();
        opt="";
    }
    else if(compStatusStatus==2) {
        $("#competition_overlayTitle").html("After Competition");
        $("#competition_overlayLong").html("The competition has ended.<br>Pending submissions will be processed.<br>");
        $("#competition_overlay").show();
        opt="After Competition";
    }
    else {
        opt="Error";
        $("#competition_overlay").hide();
    }

    if (shouldDoLast30 && !doingLast30) {
        doingLast30 = true;
        doingLast30Interval = setInterval(doingLast30Tick, 10);
        $("#competition_overlay_last_30_swipe").css("top", "100%");
        $("#competition_overlay_last_30_swipe").animate({"top": "0%"}, 1000);
        $("#competition_overlay_last_30_swipe").show();
        doingLast30CancelMe = setTimeout(function() {

        }, 1000);
    }
    else if (!shouldDoLast30) {
        stopLast30();
    }

    $("#competition_time").html(opt);
    if (compStatusAutomatic==0 && compStatusStatus==1)
        opt="During Competition";
    $("#admin_time").html(opt);

}

function compStatusServerOrders(obj) {
    if (!(obj.func=="compstatus") || obj.cid == currCompId && curPage == "competition" || obj.cid == adminCID && curPage == "admin") {
        compStatusStatus = obj.status;
        compStatusAutomatic = obj.automatic;
        compStatusStartTime = obj.startTime;
        compStatusEndTime = obj.endTime;
        compStatusOffset = (new Date()).getTime() - obj.current_time;
        compStatusPaint();
    }
}

function compStatus500MSIntervalFire() {
    if (!socketOpen||!(curPage=="admin"||curPage=="competition")) {
        stopLast30();
        return;
    }
    compStatusPaint();
}