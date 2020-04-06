

var login_username = "";
let login_uid = -1;
var loggedIn = false;

function loginFailed(obj) {
    /* Displays the appropriate error message if the login failed.

    Args:
        reason: Why the login failed
    */
    if (obj.reason != "") {
        hideNotifs();
        $("#mcst_password").val("");
    }
    else {
        $("#mcst_login_notif_1").css({display:"block"});
        $("#mcst_password").val("");
    }
}

function sendLogin() {
    /* Send login information to be checked by backend,

    Args:
    */
    send({ func: "login", username: $("#mcst_username").val(), password: $("#mcst_password").val() });
}

function checkLogin(obj) {
    /* Get login result.

    Args:
        result: If the login failed or not
    */
    if(obj.result == "good")
        loginSucceeded(obj)
    else
        loginFailed(obj)
}

function loginSucceeded(obj) {
    /* Directs user to main menu or the last page they were on if login succeeded.

    Args:
        username: User's username
        uid: User's id
        reloadToken: Once page reloads, 
    */
    login_username = obj.username;
    login_uid = obj.uid;
    loggedIn = true;
    this.sessionStorage.setItem("login_on_reload", "true");
    this.sessionStorage.setItem("reload_token", obj.reloadToken);
    clearAllInputs('loginpage');
    $("#top_name").html(login_username);
    hideAllSections();
    $("#web_header").show();
    $("#main_menu").show();
    mainMenuPractice();
}

function resetLogin() {
    /* Clear the local variables.

    Args:
    */
    login_uid = -1;
    login_username = "";
}

function doLogout() {
    /* Logs the user out.

    Args:
    */

    //Remove relogin cookies
    sessionStorage.removeItem("login_on_reload");
    sessionStorage.removeItem("reload_user_id");
    
    resetLogin();
    resetWS(true);
    restartWS();
}

function tryLogin() {
    /* Attempt to log the user in again after a system crash or restart.

    Args:
    */
    hideNotifs();
    if (socketOpen) {
        sendLogin();
    }
    else {
        alert("Please wait for socket connection.");
    }
}

function trySignup()
{
    /* Attempt to sign the user up.

    Args:
    */
    hideNotifs();
    if(!checkRequiredInputs("form-control"))
    {
        $("#mcst_login_notif_4").css({display:"block"});
        return;
    }
    else
    {
        send({
            func: "signup",
            username: $("#mcst_username").val(),
            password: $("#mcst_password").val(),
            name: $("#mcst_name").val(),
            school: $("#mcst_school").val(),
            email: $("#mcst_email").val()
        });
    }
}

function badSignup(obj)
{
    /* Show the appropriate error mesage if the signup fails.

    Args:
    */
    $("#mcst_login_notif_3").css({display:"block"});
}

function tryForgotPassword()
{
    /* Attempt to send a forgot password link to the user's email.

    Args:
    */
    hideNotifs();
    send({func:"forgotPassword", username: $("#mcst_username").val()});
}

function forgotPasswordCallback(obj)
{
    /* Show the appropriate essage if the forgot password link was unable to be sent,

    Args:
        result: If the link was successfully sent or not.
    */
    clearAllInputs('loginpage');
    if(obj.result == "good")
        $("#mcst_login_notif_6").css({display:"block"});
    else
        $("#mcst_login_notif_5").css({display:"block"});
}

function checkRequiredInputs(className)
{
    /* Check that all fields required have been filled out.

    Args:
        className: The group of input boxes to check
    */
    let valid = true;
    $("." + className).each( function(index, element) {
        if(!this.checkValidity() || (this.value.trim() == ""))
            valid = false;
    });
    return valid;
}

function clearAllInputs(className)
{
    /* Clear all input boxes.

    Args:
        className: The group of input boxes to clear.
    */
    $("." + className).each( function(index, element) {
        $(this).val("");
    });
}

function tryLoginAction() {
    /* Either log in, sign up, or send a forgot password link depending on what page the user is on.

    Args:
    */
    if (currentLoginPageMode==0) {
        tryLogin();
    }
    if (currentLoginPageMode==1) {
        trySignup();
    }
    if (currentLoginPageMode==2) {
        tryForgotPassword();
    }
}