let params = null;

function checkRequiredInputs(className)
{
    let valid = true;
    $("." + className).each( function(index, element) {
        if(!this.checkValidity() || (this.value.trim() == ""))
            valid = false;
    });

    return valid;
}

function resetPassword()
{
    /* Request that the password be changed.

    Args:
    */
    hideNotifs();
    hideAllSections();
    $("#resetpasswordpage").show();

    let url = window.location.href;
    let jwt = (url.split("?"))[1];

    if(checkRequiredInputs("form-control"))
        send( {func:"resetPassword", username:$("#mcst_username").val(), password1:$("#mcst_newPassword1").val(), password2:$("#mcst_newPassword2").val(), encodedJWT:jwt} );
    else
        $("#mcst_reset_notif_4").show();
}

function resetPasswordCallback(obj)
{
    /* Show the appropriate message after reset password finishes.

    Args:
        result: The result of the reset password
    */
    if(obj.result == "good")
        window.location = "https://mcsc.enrog.com";
    else if(obj.result == "badPassword")
        $("#mcst_reset_notif_3").show();
    else if(obj.result == "badUser")
        $("#mcst_reset_notif_1").show();
    else if(obj.result == "timedOut")
        $("#mcst_reset_notif_5").show();
    else if(obj.result == "veryBad")
        alert("Something very wrong just happened. Alert the administrators.");
}