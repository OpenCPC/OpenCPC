

function mainMenuPracticeMessageCallback(obj) {
    /* Opens the practice page on the main menu.

    Args:
        list[0]: The competition's id
        list[1]: The competition's name
        list[2]: A short description of the competition
        list[3]: The competition's admin's id
    */
    clearAllInputs('loginpage');
    if(obj.isSiteAdmin)
        $("#createPracButton").show();
    mainMenuReset();
    mainMenuSPS();
    $("#main_menu_practice").show();
    $("#main_menu_practice_list").html("Loading...");
    $("#createCompPage").hide();
    curPage = "mainMenuPractice";
    var cons = "";
    for (var i =0;i<obj.total;i++) {
        cons += '<div '+(obj.list[i][6]?'':'onclick="mmloadCompetition('+obj.list[i][0]+');"')+' id='+obj.list[i][0]+' style="cursor:pointer;margin:5px;padding:10px;border-radius:5px;background-color:#EEEEEE;border:solid 1px 777777;">\
                    <table><tr><td style="width:100%;'+(obj.list[i][6]?'opacity:0.5;':'')+'"><span style="font-weight:bold;">'+obj.list[i][1]+'</span> - '+obj.list[i][2]+' - Problems: '+obj.list[i][3]+'</td>\
                    <td>'+(obj.list[i][5]?'<div class="mmAdminButton" style="cursor:pointer;border:solid 1px #777777;border-radius:4px;padding:4px;" id="acb'+obj.list[i][0]+'">Admin</div>':'')+'</td>\
                    <td>'+(obj.list[i][6]?'<div class="mmJoinButton" style="cursor:pointer;border:solid 1px #777777;border-radius:4px;padding:4px;" id="acb'+obj.list[i][0]+'">Join</div>':'')+'</td></tr></table>\
        </div>';
    }
    $("#main_menu_practice_list").html(cons);
    $("#createCompPage").hide();
    $(".mmAdminButton").click(adminClickHandler);
    $(".mmJoinButton").click(joinClickHandler);
}

function mainMenuCompeteMessageCallback(obj) {
    /* Opens the competitions page on the main menu.

    Args:
        list[0]: The competition's id
        list[1]: The competition's name
        list[2]: A short description of the competition
        list[3]: The competition's admin's id
    */
    clearAllInputs('loginpage');
    mainMenuReset();
    mainMenuSPS();
    $("#main_menu_compete").show();
    $("#main_menu_compete_list").html("Loading...");
    $("#createCompPage").hide();
    curPage = "mainMenuCompete";
    var cons = "";
    for (var i =0;i<obj.total;i++) {
        cons += '<div onclick="mmloadCompetition('+obj.list[i][0]+', false);" id='+obj.list[i][0]+' style="cursor:pointer;margin:5px;padding:10px;border-radius:5px;background-color:#EEEEEE;border:solid 1px 777777;">\
                    <table><tr><td style="width:100%;"><span id="compName'+obj.list[i][0]+'" style="font-weight:bold;">'+obj.list[i][1]+'</span> - \
                    <span id="compDesc'+obj.list[i][0]+'">'+ obj.list[i][2]+'</span> - \
                    Problems: '+obj.list[i][3]+'</td>\
                    <td>'+(obj.list[i][5]?'<div class="mmAdminButton" style="cursor:pointer;border:solid 1px #777777;border-radius:4px;padding:4px;" id="acb'+obj.list[i][0]+'">Admin</div>':'')+'</td></tr></table>\
        </div>';
    }
    $("#main_menu_compete_list").html(cons);
    $("#createCompPage").hide();
    $(".mmAdminButton").click(adminClickHandler);
    $(".mmJoinButton").click(joinClickHandler);
}

function adminClickHandler(e) {
    /* Load the admin page for the competition.

    Args:
        e: 
    */
    var cid = parseInt(this.id.substring(3));
    loadAdmin(cid);
    e.stopPropagation();
}

function joinClickHandler(e) {
    /* Joins the user to the competition.

    Args:
        e: 
    */
    var cid = parseInt(this.id.substring(3));
    send( {func:"joinComp", cid:cid, type:"prac"} )
    e.stopPropagation();
}

function mainMenuSPSCallback(obj) {
    /* List the number and availability of the submission processing servers.

    Args:
        list[i][0]: The name of the processing server
        list[i][1]: The availability of the server
    */
    var cons = "";
    for (var i =0;i<obj.total;i++) {
        cons += '<div style="margin:5px;padding:10px;border-radius:5px;background-color:#EEEEEE;border:solid 1px 777777;">\
                    <span style="font-weight:bold;">'+obj.list[i][0]+'</span> '+obj.list[i][1]+'\
        </div>';
    }

    if (obj.total==0) {
        cons += "No submission processing servers available at this time. Please contact administrators.";
    }

    $("#main_menu_sps").html(cons);
}

function mmloadCompetition(_id) {
    /* Load the competition.

    Args:
        _id: The competition's id
    */
    hideAllSections();
    loadCompetition(_id);
}

//internal use only
function mainMenuReset() {
    /* Hide the main menu pages.

    Args:
    */
    $("#main_menu_practice").hide();
    $("#main_menu_compete").hide();
}

function mainMenuSPS() {
    /* Request to load the submission processing server list.

    Args:
    */
    $("#main_menu_sps").html("Loading...");
    send({func:"getMainMenuSPS"});
}

function mainMenuPractice() {
    /* Request to open the practice page on the main menu.

    Args:
    */
    mainMenuReset();
    $("#main_menu_practice").show();
    $("#main_menu_practice_list").html("Loading...");
    mainMenuSPS();
    send({func:"getMainMenuList", type:"prac"});
}

function mainMenuCompete() {
    /* Request to open the competition page on the main menu.

    Args:
    */
    mainMenuReset();
    $("#main_menu_compete").show();
    $("#main_menu_compete_list").html("Loading...");
    mainMenuSPS();
    send({func:"getMainMenuList", type:"comp"});
}

function openCreateComp(_type)
{
    /* Opens the create competiton page.

    Args:
        _type: Creating a practice or compete type competition.
    */
    $("#createCompPage").show();
    let today = new Date();
    makeCreateComp({name:"", 
                    short_desc: "",
                    location: "",
                    format: "", 
                    instructions:"",
                    type: _type
                   });
}

function makeCreateComp(obj)
{
    $("#createCompPage").html(
        "<div style='height:100%;'>"
            +"<div style='height:100%;color:white;border-radius:20px;width:100%;background-color:rgb(30,30,30);'>"
                +"<div style='height:auto;padding:5px;text-align:center;background-color:rgb(40,40,40);border-radius:20px 20px 0px 0px;border-bottom:solid 1px rgb(60,60,60);font-size:40px'> Create Competition </div>"
                +"<div style='color:black;height:80%;padding:20px;text-align:center'>"
                    +"<div style='color:white;font-size:20px'> Competition Name </div>"
                    +"<input class='createComp' id='compName' style='width:100%;padding:5px;height:auto;margin:3px' type='text' value='"+obj.name+"'>"
                    +"<br><br>"
                    +"<div style='color:white;font-size:20px'> Short Description  </div>"
                    +"<input class='createComp' id='compShortDesc' style='width:100%;padding:5px;height:auto;margin:3px' type='text' value='"+obj.short_desc+"'>"
                    +"<br><br>"
                    +"<input class='btn btn-primary' style='cursor:pointer;width:200px;padding:8px;margin-top:20%;margin-left:auto;margin-right:auto;height:auto;display:block;'"
                    +"onclick='saveComp("+obj.cid+", \""+obj.type+"\");return false;' type='submit' value='Save'>"
                +"</div>"
            +"</div>"
        +"<br><br><br></div>");
    hideLoading();
}

async function saveComp(cid, _type)
{
    
    let func = "createComp";
    let aid = 0;
    if(curPage == "admin")
    {
        func = "editComp";
    }
    if(checkRequiredInputs("createComp"))
    {
        await send( {func: func,
                     name: $("#compName").val(),
                     short_desc: $("#compShortDesc").val(),
                     curPage: curPage,
                     aid: aid,
                     cid: cid,
                     type: _type
                   } );
        $("#createCompPage").hide();
   }
   else
   {
       alert("Please fill out all the fields.");
   }
}