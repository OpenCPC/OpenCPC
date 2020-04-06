var socketOpen = false;
var socket = null;
var restartWSCalled = false;
var socketTimeout = null;

function onMessage(event) {
    /* Handles (dispatches) a new message to the appropriate handler.

    Args:
        func: The function, as a string, of the message
        data: The data retrieved
    */

    obj = JSON.parse(event.data);
    console.log(obj);
    if (obj.func == "login")
        checkLogin(obj);
    else if (obj.func == "signup")
        badSignup(obj);
    else if (obj.func == "getMainMenuPracticeList")
        mainMenuPracticeMessageCallback(obj);
    else if (obj.func == "getMainMenuCompeteList")
        mainMenuCompeteMessageCallback(obj);
    else if (obj.func == "getCompetitionInfo"){
        getCompetition(obj);
        compStatusServerOrders(obj);}
    else if (obj.func == "getSubmissions")
        refreshSubmissionsCallback(obj);
    else if (obj.func == "openProblem") {
        openProblemCallback(obj);
        competitionRefreshField();
    } else if (obj.func == "compError") {
        $("#loading").hide();
        alert(obj.reason);
    } else if (obj.func == "getProblemList")
        openProblemList(obj);
    else if (obj.func == "getAdminProblem")
        getAdminProblemCallback(obj);
    else if (obj.func == "mainMenuSPS")
        mainMenuSPSCallback(obj);
    else if (obj.func == "live") {
        compLive(obj);
    } else if (obj.func == "getPopUp")
        loadPopUp(obj);
    else if (obj.func == "adminGetPopUp")
        adminLoadPopUp(obj);
    else if (obj.func == "loadAdmin"){
        loadAdminCallback(obj);
        compStatusServerOrders(obj);}
    else if (obj.func == "adminProblems")
        adminProblemsCallback(obj);
    else if (obj.func == "adminCompetitors")
        adminCompetitorsCallback(obj);
    else if (obj.func == "addCompetitor")
        addCompetitorCallback(obj);
    else if (obj.func == "getScoreboard")
        sbScoreboardCallback(obj);
    else if (obj.func == "getAllSubmissions")
        sbAllSubmissionsCallback(obj);
    else if (obj.func == "getAdminSubmissions")
        adminSubmissionsCallback(obj);
    else if (obj.func == "adminScoreboard")
        adminScoreboardCallback(obj);
    else if (obj.func == "editComp") {
        if (obj.cid == -1)
            adminEndTimer();
        else if (curPage != "admin")
            updateComp(obj);
        else
            loadAdmin(obj.cid);

    } else if (obj.func == "forgotPassword")
        forgotPasswordCallback(obj);
    else if (obj.func == "adminSaveCaseCallback")
        adminSaveCaseCallback(obj);
    else if (obj.func == "resetPassword")
        resetPasswordCallback(obj);
    else if (obj.func == "adminGetCase")
        adminEditCaseCallback(obj);
    else if (obj.func == "adminSaveQuestion") {
        if ((curPage != "admin") || (curBackground != "none"))
            updateQuestion(obj);
    } else if (obj.func == "NL")
        doLogout();
    else if (obj.func == "createComp")
        openCreateComp(obj.type);
    else if (obj.func == "adminEditComp")
        adminEditComp();
    else if (obj.func == "submitProblem")
        refreshSubmissions(obj.pid, obj.cid);
    else if (obj.func == "adminAddImage")
        adminAddImageCallback(obj);
    else if (obj.func == "adminRemoveImage")
        adminRemoveImageCallback(obj)
    else if (obj.func == "adminLevels")
        adminLevelsCallback(obj);
    else if (obj.func == "adminControlPanel")
        adminControlPanelCallback(obj);
    else if (obj.func == "compstatus")
        compStatusServerOrders(obj);
    else if(obj.func == "moveProblem") {
        if(currCompId == obj.cid)
        {
            if(curField == "problemlist")
                sbProblemList();
        }
    }
    else if(obj.func == "adminGroups")
        adminGroupsCallback(obj);
    else if(obj.func == "adminCompetitorInfo")
        adminCompetitorInfoCallback(obj);
    else
        console.log("unknown command" + obj);
}

function resetWS(cleanExit=false) {
    /* Close websocket and reset variables.

    Args:
        cleanExit: 
    */

    if (socket != null) {
        socket.close();
    }
    socket = null;
    if (socketOpen && !cleanExit) {
        $("#mcst_login_notif_2").css({
            display: "block"
        });
    }
    socketOpen = false;
    gotoLogin();
    $("#connstatus").html("<span style='color:red'>Connection Status: Not Connected</span>");
}

function restartWS() {
    /* Attempt to restart websocket every 5 seconds.
    */

    if (restartWSCalled == false) {
        restartWSCalled = true;
        socketTimeout = setTimeout(openSocket, 5000);
    }
}

function onClose(event) {
    /* Triggers when the websocket is closed for any reason.

    Args:
        event.code: The exit code according to RFC 6455 websocket protocol.
        event.reason: The reason why the websocket closed.
    */

    console.log("Websocket disconnected: " + event);
    resetLogin();
    resetWS();
    restartWS();
}

function onError(event) {
    /* Triggers when the websocket crashes.

    Args:
        event: Contains no information.
    */
    console.log("Websocket error: " + event);
    resetLogin();
    resetWS();
    restartWS();
}

function onOpen(event) {
    /* Triggers when a websocket opens.
    */
    console.log("Socket opened.");
    socketOpen = true;
    $("#connstatus").html("<span style='color:green'>Connection Status: Connected</span>");
    
    //Clear 'lost connection' message
    $("#mcst_login_notif_2").css({
        display: "none"
    });
    
    //Send welcome message
    socket.send("Hi, I'm a valid client.");

    //Auto relogin
    if (sessionStorage.getItem("login_on_reload") == "true") {
        socket.send(JSON.stringify({
            func: "reloadLogin",
            reloadToken: sessionStorage.getItem("reload_token")
        }));
        sessionStorage.removeItem("login_on_reload");
        sessionStorage.removeItem("reload_user_id");
    }
}

function openSocket() {
    /* Opens a websocket connection.
    */

    console.log("Attempting socket connection...");
    restartWSCalled = false;
    resetWS();
    try {
        socket = new WebSocket("wss://"+window.location.hostname+":80");
        socket.onopen = function (event) {
            onOpen(event);
        };
        socket.onmessage = function (event) {
            onMessage(event);
        };
        socket.onclose = function (event) {
            onClose(event);
        };
        socket.onerror = function (event) {
            onError(event);
        };
    } catch (err) {
        console.log("Failed to connect to websocket: general error.");
        resetWS();
        restartWS();
    }
}

function send(obj) {
    /* Sends data through the websocket to the backend.

    Args:
        obj: The data to send
    */
    obj.uid = login_uid;
    socket.send(JSON.stringify(obj));
}

$(function () {
    /* Entry point for the background scripts.
    */
   let url = window.location.href;
   let jwt = (url.split("?"));
   if(jwt.length == 2)
   {
       resetPassword();
   }
    openSocket();
    setInterval(compStatus500MSIntervalFire, 500);
});