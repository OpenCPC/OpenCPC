//code for handling what is visible on the wide scale

//not for tiny manipulations like within competition_page

//available sections: main_menu, web_header, loginpage, and competition_page
//some code for section manipulation is handled elsewhere. competition_page is switched to in competition.js, but it still calls hideAllSections() and $("#web_header").show();.

let curPage = "login";

let currentLoginPageMode = 0;

function hideAllSections() {
    $("#main_menu").hide();
    $("#web_header").hide();
    $("#loginpage").hide();
    $("#createCompPage").hide();
    $("#competition_page").hide();
    $("#admin_page").hide();
    $("#resetpasswordpage").hide();
}

function hideNotifs()
{
    $("#mcst_login_notif_1").css({display:"none"});
    $("#mcst_login_notif_3").css({display:"none"});
    $("#mcst_login_notif_4").css({display:"none"});
    $("#mcst_login_notif_5").css({display:"none"});
    $("#mcst_login_notif_6").css({display:"none"});
    $("#mcst_reset_notif_1").hide();
    $("#mcst_reset_notif_2").hide();
    $("#mcst_reset_notif_3").hide();
    $("#mcst_reset_notif_4").hide();
    $("#mcst_reset_notif_5").hide();
}

function gotoLogin() {
    hideAllSections();
    $("#loginpage").show();
    $("#loginPageInstructions").html("Log In");
    $("#mcst_tmpforgotpassword").hide();
    $("#mcst_username").show();
    $("#mcst_password").show();
    $("#mcst_name").hide();
    $("#mcst_school").hide();
    $("#mcst_email").hide();
    $("#mcst_login").show();
    $("#mcst_signup").hide();
    $("#mcst_forgotPassword").hide();
    $("#mcst_gotoSignup").show();
    $("#mcst_gotoLogin").hide();
    $("#mcst_gotoForgotPassword").show();
    currentLoginPageMode = 0;
    hideNotifs();
}

function gotoSignup()
{
    hideAllSections();
    $("#loginpage").show();
    $("#loginPageInstructions").html("Sign Up");
    $("#mcst_tmpforgotpassword").hide();
    $("#mcst_username").show();
    $("#mcst_password").show();
    $("#mcst_name").show();
    $("#mcst_school").show();
    $("#mcst_email").show();
    $("#mcst_login").hide();
    $("#mcst_signup").show();
    $("#mcst_forgotPassword").hide();
    $("#mcst_gotoSignup").hide();
    $("#mcst_gotoLogin").show();
    $("#mcst_gotoForgotPassword").show();
    currentLoginPageMode = 1;
    hideNotifs();
}

function gotoForgotPassword()
{
    hideAllSections();
    $("#loginpage").show();
    $("#loginPageInstructions").html("Forgot Password");
    $("#mcst_tmpforgotpassword").show();
    $("#mcst_username").hide();
    $("#mcst_password").hide();
    $("#mcst_name").hide();
    $("#mcst_school").hide();
    $("#mcst_email").hide();
    $("#mcst_login").hide();
    $("#mcst_signup").hide();
    $("#mcst_forgotPassword").hide();
    $("#mcst_gotoSignup").hide();
    $("#mcst_gotoLogin").show();
    $("#mcst_gotoForgotPassword").hide();
    currentLoginPageMode = 2;
    hideNotifs();
}

function gotoMainMenu() {
    hideAllSections();
    $("#web_header").show();
    $("#main_menu").show();
    $("#top_competition_name").html("");
    mainMenuPractice();
}

function returnFromFieldSub() {

	$("#fieldSubShadow").animate({opacity:0},300);
	setTimeout(function(){$("#fieldSubShadow").css({display:"none"});},300);
    $("#fieldSub").animate({left:"100vw",opacity:0.0},300);
    send({func:"returnFromFieldSub"})
}

function adminReturnFromFieldSub() {

	$("#adminFieldSubShadow").animate({opacity:0},300);
	setTimeout(function(){$("#adminFieldSubShadow").css({display:"none"});},300);
    $("#adminFieldSub").animate({left:"100vw",opacity:0.0},300);
    send({func:"returnFromFieldSub"})
}

function showLoading() {
	$("#loading").show();
}
function hideLoading() {
	$("#loading").hide();
}

function showPopup()
{
    showLoading();
    $("#fieldSubShadow").css({display:"block",opacity:0.0});
	$("#fieldSub").css({display:"block",opacity:0.0,left:"100vw"});
    $("#fieldSubShadow").animate({opacity:1.0},300);
    $("#fieldSub").animate({left:"350px",opacity:1.0},300);
}

function adminShowPopup()
{
    showLoading();
    $("#adminFieldSubShadow").css({display:"block",opacity:0.0});
	$("#adminFieldSub").css({display:"block",opacity:0.0,left:"100vw"});
    $("#adminFieldSubShadow").animate({opacity:1.0},300);
    $("#adminFieldSub").animate({left:"350px",opacity:1.0},300);
}

function updateComp(obj)
{
    if(curPage == "mainMenuCompete")
    {
        $("#compName"+obj.cid).html(obj.name);
        $("#compDesc"+obj.cid).html(obj.short_desc);
    }
    else if(curPage == "competition")
    {
        $("#competition_name").html(obj.name);
        endTime = obj.endTime;
    }
}