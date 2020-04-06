var curAdminField = "none";
var adminID = -1;
var adminCID = -1;
var curPID = -1;
var curCASEID = -1;
let movePID = -1;

function loadAdmin(cid) {
    /* Requests to load admin page of a given competition.

    Args:
        cid: The competition id
    */
    hideAllSections();
    $("#web_header").show();
    $("#admin_page").show();
    $("#admin_overlayTitle").html("Loading...");
    $("#admin_overlayLong").html("Retrieving Info...");
    $("#admin_overlay").show();
    send({func:"loadAdmin", cid:cid});
}

function loadAdminCallback(obj) {
    /* Loads the admin page.

    Args:
        cid: The competition id
        adminid: The id of the user with admin access to the given competition
        competitionkey: The competition key, used for loading images
    */
    hideAllSections();
    hideAdminSections();
    
    adminCID = obj.cid;
    adminID = obj.adminid;
    adminCompKey = obj.competitionkey;

    $("#admin_overlay").hide();

    $("#admin_competition_name").html(obj.name);
    $("#top_competition_name").html(" - "+obj.name);
    curAdminField = "backlay";
    
    curPage = "admin";
    makeEditComp(obj);
    $("#web_header").show();
    $("#admin_page").show();
}


function makeEditComp(obj)
{
    /* Opens the edit competition page.

    Args:
        name: The name of the competition
        short_description: A short description of the competition
        cid: The competition's id
    */
    hideAdminSections();
    $("#editCompPage").html(
        "<div style='height:100%;'>"
            +"<div style='height:100%;color:white;border-radius:20px;width:auto;'>"
                +"<div style='height:auto;padding:5px;text-align:center;border-radius:20px 20px 0px 0px;border-bottom:solid 1px rgb(60,60,60);font-size:40px'> Edit Competition </div>"
                +"<div style='color:black;height:80%;padding:20px;text-align:center'>"
                    +"<div style='color:white;font-size:20px'> Competition Name </div>"
                    +"<input class='createComp' id='compName' style='width:300px;padding:5px;height:auto;margin:3px' type='text' value='"+obj.name+"'>"
                    +"<br><br>"
                    +"<div style='color:white;font-size:20px'> Short Description  </div>"
                    +"<input class='createComp' id='compShortDesc' style='width:300px;padding:5px;height:auto;margin:3px' type='text' value='"+obj.short_desc+"'>"
                    +"<br>"
                    +"<input class='btn btn-primary' style='cursor:pointer;width:200px;padding:8px;margin-top:20px;margin-left:5%;margin-right:5%;height:auto;' \
                    onclick='saveComp("+obj.cid+", \"comp\");return false;' type='submit' value='Save'>"
                +"</div>"
            +"</div>"
        +"<br><br><br></div>");
    $("#editCompPage").css( "margin-top", ($("#web_header").height()+50).toString() + "px");
    hideLoading();
}

function hideAdminSections() {
    /* Hides all admin pages.

    Args:
    */
    curAdminField = "none";
    $("#admin_problems").hide();
    $("#admin_levels").hide();
    $("#admin_groups").hide();
    $("#admin_backlay").hide();
    $("#admin_problem_general").hide();
    $("#admin_problem_cases").hide();
    $("#admin_case").hide();
    $("#admin_competitors").hide();
    $("#admin_competitor_info").hide();
    $("#admin_submissions").hide();
    $("#admin_results").hide();
    $("#admin_control_panel").hide();
    $("#editCompPage").hide();
    typeOfSubmissions="noSubmissions";
}

function adminProblems() {
    /* Opens the list of problems for the competition.

    Args:
    */
    hideAdminSections();
    $("#admin_problems").show();
    curAdminField = "problems";
    $("#admin_problems_list").html("Loading...");
    send({func:"adminProblems", cid:adminCID});
}

function adminEditProblem(pid) {
    /* Requests to open the problem editor.

    Args:
        pid: The problem id
    */
    hideAdminSections();
    curPID = pid;
    $("#admin_problem_general").show();
    $("#admin_problem_cases").show();
    $("#admin_problem_general_inner").html("Loading...");
    $("#admin_problem_cases_inner").html("Loading...");
    send({func:"getAdminProblem",pid:pid,cid:adminCID});
}

function adminEditCase(caseid) {
    /* Requests to open the sample/test case editor.

    Args:
        caseid: The sample/test case id
    */
    hideAdminSections();
    curCASEID = caseid;
    send( {func:"adminGetCase", cid:adminCID, pid:curPID, caseid:curCASEID} );
}

function adminEditCaseCallback(obj)
{
    /* Opens sample/test case editor.

    Args:
        input: The case's input
        output: The case's output
        value: The number of points a competitor can earn by getting the case right
    */
    if(obj.result == "bad")
        alert("Something messed up in adminEditCaseCallback");
    else
    {
        $("#editInput").val(obj.input);
        $("#editOutput").val(obj.output);
        $("#editValue").val(obj.value);
        $("#admin_case").show();
    } 
}

function adminSaveCase()
{
    /* Save the case the admin is working on.

    Args:
    */
    if(isNaN(parseInt($("#editValue").val())))
        alert("Value must be a number.");

    send( {func:"adminSaveCase", input:$("#editInput").val(), output:$("#editOutput").val(), value:parseInt($("#editValue").val()), cid:adminCID, pid:curPID, caseid:curCASEID, aid:adminID} );
}

function adminSaveCaseCallback() {
    /* Open problem editor once a case has been saved.

    Args:
    */
    adminEditProblem(curPID);
}

function adminSaveQuestion()
{
    /* Save the problem the admin is working on.

    Args:
    */
    send( {func:"adminSaveQuestion", question:$("#admin_problem_general_inner").val(), problemname:$("#admin_edit_problemname").val(), runtime:$("#admin_problem_general_runtime").val(), memory:$("#admin_problem_general_memory").val(), level:$("#admin_problem_level").val(), pid:curPID, aid:adminID, cid:adminCID} )
}

function adminSetCompStatus(status) {
    /* Sets the competition status (before, during, or after).

    Args:
        status: The competition status
    */
    send( {func:"adminSetCompStatus", status:status, cid:adminCID} );
    adminControlPanel();
}

function adminSetAutomaticCompetitionStatus(status) {
    /* Puts the competition on an admin-set timer so that the competition automatically ends after the timer ends.

    Args:
    */
    send( {func:"adminSetAutomaticCompetitionStatus", delay:$("#adminControlPanelStartingTimeDelay").val(), duration:$("#adminControlPanelDuration").val(), cid:adminCID} );
    adminControlPanel();
}

function adminEnableScoreboard(status) {
    /* Allow users to see the scoreboard.

    Args:
    */
    send( {func:"adminSetScoreboard", scoreboardvisible: 1, cid:adminCID} );
    adminControlPanel();
}

function adminDisableScoreboard(status) {
    /* Doesn't allow users to see the scoreboard.

    Args:
    */
    send( {func:"adminSetScoreboard", scoreboardvisible: 0, cid:adminCID} );
    adminControlPanel();
}

function adminRegradeProblemSubmissions()
{
    /* Sets the status of all the problem's submissions as ungraded, causing the grading software to regrade all those submissions.

    Args:
    */
    send( {func:"adminRegradeProblemSubmissions", pid:curPID, aid:adminID, cid:adminCID} );
    adminSubmissions();
}

function adminRemoveCase(caseid)
{
    /* Deletes a case from the problem.

    Args:
        caseid: The case's id
    */
    if(confirm("Do you really want to delete this case?"))
        send( {func:"adminRemoveCase", caseid:caseid, pid:curPID, cid:adminCID} );
}

function adminAddCase()
{
    /* Adds a case to the problem.

    Args:
    */
    send( {func:"adminAddCase", pid:curPID, cid:adminCID} );
}

function adminCustomRun(sid) {
    /* Custom runs a submission, allowing admin to compare all output to expected output.

    Args:
        sid: The submission's id
    */
    send( {func:"customrun", sid:sid} );
    adminSubmissions();
}

function adminRemoveProblem(pid)
{
    /* Deletes a problem.

    Args:
        pid: The problem's id
    */
    if(confirm("Do you really want to delete this case?"))
        send( {func:"adminRemoveProblem", pid:pid, cid:adminCID} );
}

function adminControlPanel() {
    /* Requests to open the control panel.

    Args:
    */
    $("#adminCurrentSituation").html("Loading...");
    send({func:"adminControlPanel", cid:adminCID});
}

function adminControlPanelCallback(obj) {
    /* Opens the control panel.

    Args:
        automatic: Whether or not the competition's timer automatically ticks down and ends, or the end time is manually determined
        status: The competition's status (before, during, or after)
        scoreboardvisible: Whether the scoreboard is visible to competitors or not
        startTime: The competition's start time, set by the admin
        endtime: The competition's end time, set by the admin
    */
    hideAdminSections();
    $("#admin_control_panel").show();

    let opt = "";

    if (obj.automatic==1) {
        opt += "Competition is set to automatically start at "+obj.startTime+" and end at "+obj.endTime+". Competition status will be ignored.<br>";
    }
    else if (obj.status==0) {
        opt += "Competition status: Before competition. Competition is not set to automatically start.<br>";
    }
    else if (obj.status==1) {
        opt += "Competition status: During competition. Competition is not set to automatically stop.<br>";
    }
    else if (obj.status==2) {
        opt += "Competition status: After competition.<br>";
    }
    else {
        opt += "Situation analysis error.<br>";
    }


    if (obj.scoreboardvisible == 1) {
        opt += "Scoreboard is visible during competition.<br>";
    }
    else {
        opt += "Scoreboard is hidden during competition.<br>";
    }

    opt += "<br>Raw values: Status: "+obj.status+" Automatic: "+obj.automatic+" Start time: "+obj.startTime+" End time: "+obj.endTime+" Scoreboard Visible: "+obj.scoreboardvisible+"<br>";

    $("#adminCurrentSituation").html(opt);
}

function adminAddProblem()
{
    /* Adds a problem to the competition.

    Args:
    */
    send( {func:"adminAddProblem", cid:adminCID} );
}
//
function getAdminProblemCallback(obj) {
    /* Opens the problem editor.

    Args:
        problemname: The problem's name
        problemtext: The content of the problem
        memorylimit: The memory limit
        runtimelimit: The runtime limit
        level: The difficulty level of the problem, set by the admin
        images: A double array of all the images associated with the problem
            [0]: image id
            [1]: file name
        cases: A double array of all the cases associated with the problem
            [0]: case id
            [1]: value
            [2]: input
        levels: A double array of all the levels associated with the problem
            [0]: name
    */
    hideAdminSections();
    curPID = obj.pid;

    $("#admin_edit_problemname").val(obj.problemname);
    
    $("#admin_problem_general_inner").html(htmlspecialchars(obj.problemtext));
    $("#admin_problem_general_inner").val(obj.problemtext);
    $("#admin_problem_general_memory").val(obj.memorylimit);
    $("#admin_problem_general_runtime").val(obj.runtimelimit);
    $("#admin_problem_level").val(obj.level);

    let imagesout = ""
    for(let i=0; i < obj.images.length; i++)
    {
        imagesout += "<li id='image_"+obj.images[i][0]+"' class=\"image_tag\" style='padding:5px;'>"+obj.images[i][1]+" <span class='glyphicon glyphicon-trash' style='margin-left:10px;' onclick='adminRemoveImage("+obj.images[i][0]+");'></span>";
        imagesout += "<img style='display:block;' src='img.php?compkey="+adminCompKey+"&imgid="+obj.images[i][0]+"&type=admin'> </li>";
    }
    let casesout = "";
    if(obj.cases.length == 0)
        casesout = "<div style='font-size:20px;'>No cases found.</div>";
    else
    {
        casesout += "<table class='problemSubmissionsTable'><tr><th>ID</th><th>Input (First 20)</th><th>Value</th><th>Options</th></tr>";
        for(let i=0; i <obj.cases.length; i++)
        {
            casesout += "<tr><td>"+obj.cases[i][0]+"</td><td>"+obj.cases[i][2]+"</td><td>"+obj.cases[i][1]+"</td><td style='width:200px;'>" +
                        "<button class='sidebarbutton' style='width:auto;display:inline-block;' onclick='adminEditCase("+obj.cases[i][0]+");'>Edit</button>"+
                        "<button class='sidebarbutton' style='border-radius:10px;background-color:#d9534f;width:auto;display:inline-block;' onclick='adminRemoveCase("+obj.cases[i][0]+");'>Remove</button>" +"</td></tr>";
        }
        casesout += "</table>";
    }
    let levelsout = "";
    if(obj.levels.length == 0)
    {
        alert("Why are there no levels...?");
    }
    else
    {
        for(let i=0; i < obj.levels.length; i++)
        {
            if(obj.level == obj.levels[i][0])
                levelsout += "<option value=\""+obj.levels[i][0]+"\" selected>"+obj.levels[i][0]+"</option>";
            else
                levelsout += "<option value=\""+obj.levels[i][0]+"\">"+obj.levels[i][0]+"</option>";
        }
    }
    $(".image_tag").remove();
    $("#admin_problem_level").html(levelsout);
    $("#admin_problem_images").prepend(imagesout)
    $("#admin_problem_cases_list").html(casesout);
    $("#admin_problem_general").show();
    $("#admin_problem_cases").show();
}

function adminProblemsCallback(obj) {
    /* Opens the list of problems in the competition.

    Args:
        probs: A double array of all the problems in the competition
            [0]: level
            [1]: name
            [2]: id
            [3]: number
            [4]: max score
    */
    let problemsout = "";
    if(obj.probs.length == 0)
        problemsout = "<div style='font-size:20px;'>No problems found.</div>"
    else
    {
        problemsout += "<table class='adminProblemsTable'><tr><th># (ID)</th><th>Problem Name</th><th style='width:35%;'>Options</th></tr>";
        for(let i=0; i <obj.probs.length; i++)
        {
            problemsout += "<tr id=\""+obj.probs[i][2]+"_problemrow\"><td>"+obj.probs[i][3]+" ("+obj.probs[i][2]+")</td><td>"+obj.probs[i][1]+"</td><td>" +
                           "<button class='sidebarbutton' style='width:auto;display:inline-block;' onclick='adminEditProblem("+obj.probs[i][2]+");'>Edit</button>" +
                           "<button class='sidebarbutton' style='width:auto;display:inline-block;' onclick='adminMoveProblem("+obj.probs[i][2]+");'>Move</button>" +
                           "<button class='sidebarbutton' style='border-radius:10px;background-color:#d9534f;width:auto;display:inline-block;' onclick='adminRemoveProblem("+obj.probs[i][2]+");'>Remove</button>" + "</td></tr>"+
                           "<tr class='moveToDiv' onclick='moveProblem("+obj.probs[i][2]+")'><td></td><td></td><td></td></tr>";
        }
        problemsout += "</table>";
    }
    $("#admin_problems_list").html(problemsout);
    $("#admin_problems").show();
}

function adminMoveProblem(pid)
{
    /* Turns the problem list into "move problem" mode, where admin can shift the order of a given problem.

    Args:
        pid: The problem's id
    */
    $("#"+pid+"_problemrow").css("font-weight", "bold")
    movePID = pid;
    $('.moveToDiv').each(function(i, obj) {
        $(this).show();
    });
}

function moveProblem(pid)
{
    /* Moves the problem into its new position chosen by the admin.

    Args:
        _pid: The problem id
    */

    if(movePID == -1)
    {
        alert("You weren't supposed to get here.");
        return;
    }
    
    send({func:"moveProblem", from_pid:movePID, to_pid:pid, cid:adminCID})

    $('.moveToDiv').each(function(i, obj) {
        $(this).hide();
    });
    $("#"+movePID+"_problemrow").css("font-weight", "normal")
    movePID = -1;
}

function adminCompetitors()
{
    /* Requests to open the competitor list.

    Args:
    */
    hideAdminSections();
    $("#admin_competitors").show();
    curAdminField = "competitors";
    $("#admin_competitors_list").html("Loading...");
    send({func:"adminCompetitors", cid:adminCID});
}

function adminCompetitorsCallback(obj)
{
    /* Opens the competitor list.

    Args:
        groups: A double array of all the groups associated with the competition
            [0]: id
            [1]: name
        comps: A double array of all the competitors in the competition
            [0]: user name
            [1]: user school
            [2]: user id
            [3]: group id
            [4]: group name
    */
    $("#admin_competitors").show();
    let competitorsout = "";
    let groupsout = "<option value='-1'>Single</option>";

    for(let i = 0; i < obj.groups.length; i++)
    {
        groupsout += "<option value='"+obj.groups[i][0]+"'>"+obj.groups[i][1]+"</option>";
    }

    if(obj.type == "comp")
    {
        competitorsout += "<table id='competitorsTable' class='problemSubmissionsTable'><tr><th>School</th><th>Name</th><th>Group</th><th>Options</th></tr>";
        competitorsout += "<input id='competitorUsername' type='text' style='color:black;width:400px;display:inline-block;border-radius:8px;margin-bottom:25px;margin-left:auto;margin-right:auto;' placeholder='Username'>\
                           <select id='competitorGroup' style='color:black;display:inline-block;border-radius:8px;padding:3px;margin-left:20px;'>"+groupsout+"</select>\
                           <button class='btn btn-primary' onclick='addCompetitor();' style='height:auto;width:auto;display:inline-block;margin-left:20px'> Add Competitor </button> </tr> \
                           <div id='addCompetitorError' class='alert alert-danger' style='width:auto;display:none;'></div>";
        for(let i = 0; i < obj.comps.length; i++)
        {
            infoButton = "<button class='sidebarbutton' style='border-radius:10px;width:auto;display:inline-block;'" +
                         "onclick='adminCompetitorInfo("+obj.comps[i][2]+");'>Info</button>";
            removeButton = "<button class='sidebarbutton' style='border-radius:10px;background-color:#d9534f;width:auto;display:inline-block;'" +
                           "onclick='adminRemoveCompetitor("+obj.comps[i][2]+");'>Remove</button>";
            competitorsout += "<tr "+(obj.comps[i][5]?"style='color:rgb(0,255,0);'":"style='color:rgb(255,0,0);'")+"><td>"+obj.comps[i][1]+"</td><td>"+obj.comps[i][0]+"</td><td>"+
                              "<select id='competitor_"+obj.comps[i][2]+"_group' onchange='editCompetitor("+obj.comps[i][2]+","+obj.comps[i][3]+");'"+
                              "style='color:black;display:inline-block;border-radius:8px;padding:3px;margin-left:20px;'>"+groupsout+"</select>"+
                              "</td><td style='color:white;'>"+infoButton+removeButton+"</td></tr>";
        }
    }
    else
    {
        competitorsout += "<table id='competitorsTable' class='problemSubmissionsTable'><tr><th>Name</th><th>Email</th><th>School</th></tr>";
        for(let i = 0; i < obj.comps.length; i++)
        {
            infoButton = "<button class='sidebarbutton' style='border-radius:10px;width:auto;display:inline-block;'" +
                         "onclick='adminCompetitorInfo("+obj.comps[i][2]+");'>Info</button>";
            competitorsout += "<tr "+(obj.comps[i][5]?"style='color:rgb(0,255,0);'":"style='color:rgb(255,0,0);'")+"><td>"+obj.comps[i][1]+"</td><td>"+
                              "<select id='competitor_"+obj.comps[i][2]+"_group' onchange='editCompetitor("+obj.comps[i][2]+","+obj.comps[i][3]+");'"+
                              "style='color:black;display:inline-block;border-radius:8px;padding:3px;margin-left:20px;'>"+groupsout+"</select>"+
                              "</td><td style='color:white;'>"+infoButton+"</td></tr>";
            $("#competitor_"+obj.comps[i][2]+"_group").val(obj.comps[i][3]);
        }
    }
    if(obj.comps.length == 0)
    {
        competitorsout += "<div style='font-size:20px;margin-bottom:20px;'>No competitors found.";
    }
    competitorsout += "</table>";
    $("#admin_competitors_list").html(competitorsout);
    for(let i = 0; i < obj.comps.length; i++)
    {
        if(obj.comps[i][4] == "Single")
            $("#competitor_"+obj.comps[i][2]+"_group").val("-1")
        else
            $("#competitor_"+obj.comps[i][2]+"_group").val(obj.comps[i][3].toString())
    }
}

function addCompetitor()
{
    /* Adds a competitor to the competition.

    Args:
    */
    $("#addCompetitorError").hide();
    send( {func:"addCompetitor", username:$('#competitorUsername').val(), cid:adminCID, gid:parseInt($("#competitorGroup").val())} );
}

function addCompetitorCallback(obj)
{
    /* Shows an error if the system failed to add the competitor.

    Args:
    */
    $("#addCompetitorError").html(obj.reason);
    $("#addCompetitorError").show();
}

function editCompetitor(uid, gid)
{
    /* Assigns the competitor to a new group, chosen by the admin.

    Args:
        uid: The id of the user to be edited
        gid: The new group's id
    */
    let new_gid = parseInt($("#competitor_"+uid+"_group").val());
    send( {func:"editCompetitor", e_uid:uid, old_gid:gid, new_gid:new_gid, cid:adminCID} )
}

function adminRemoveCompetitor(remove_uid)
{
    /* Removes a competitor from the competition.

    Args:
        remove_uid: The id of the user to be removed
    */
    if(confirm("Are you sure you want to remove this competitor?"))
        send( {func:"removeCompetitor", ruid:remove_uid, cid:adminCID} );
}

function adminCompetitorInfo(uid_info)
{
    /* Requests information on the competitor's performance in the competition.

    Args:
    */
    send( {func:"adminCompetitorInfo", uid_info:uid_info, cid:adminCID} )
}

function adminCompetitorInfoCallback(obj)
{
    /* Shows statistics on the competitor's performance in the competition.

    Args:
        levels: An double array of all the difficulty levels in the competition
            [0]: level name
        probs: A double array of all the problems in the competition, and the competitor's results on each
            [0]: problem number
            [1]: level
            [2]: max score
            [3]: name
            [4]: id
        subs: A double array of all the the competitor's submissions in the current competition
            [0]: highest submission score for the given problem
            [1]: problem id
            [2]: number of submissions
    */
    hideAdminSections();
    $("#admin_competitor_info").show();
    let maxscore=0, totalscore=0, totalsubs=0, levelsout="";
    for(let i=0; i < obj.levels.length; i++)
    {
        levelsout += "<table> <tr> <td style='padding:5px;'>"+obj.levels[i][0]+"</td> <td style='width:100%;'>"+
                     "<div style='height:1px;width:100%;background-color:rgb(60,60,60);'> </div></td> </tr> </table>"+
                     "<div id='admin_pl"+obj.levels[i][0]+"'> </div>"
    }
    $("#competitor_detailed_stats").html(levelsout);


    for(let i=0; i < obj.probs.length; i++)
    {
        let backgroundColor = "#FFFFFF";
        let subid= -1;
        let problem_score="", sub_count=0;
        for(let j=0; j < obj.subs.length; j++)
        {
            if(obj.probs[i][4] == obj.subs[j][1])
            {
                subid = j;
                let percent = obj.subs[j][0]/obj.probs[i][2];
                if(percent == 0)
                    backgroundColor = "#EE7700";
                else if(percent < 0.5)
                    backgroundColor = "#EEEE00";
                else if(percent < 1)
                    backgroundColor = "#00ADFF";
                else
                    backgroundColor = "#00EE00";
                break;
            }
        }
        if(subid == -1)
        {
            problem_score = "Not Attempted";
            totalscore += 0;
        }
        else
        {
            problem_score = obj.subs[subid][0].toString() + "/" + obj.probs[i][2].toString();
            totalscore += obj.subs[subid][0];
            totalsubs += obj.subs[subid][2];
            sub_count = obj.subs[subid][2];
        }
        let cons = "<div style='box-sizing:content-box;position:relative;padding:4px 4px 4px 24px;display:inline-block;height:16px;'>\
                    <div style='position:absolute;left:4px;top:4px;width:16px;height:16px;border-radius:100%;background-color:" + backgroundColor + "'> </div>\
                    " + obj.probs[i][0] + ". " + obj.probs[i][3] + " ("+obj.probs[i][2]+")"+"</div><br>" +
                    "<div style='display:inline-block;margin-left:70px;'>"+problem_score+"</div><br>" + 
                    "<div style='display:inline-block;margin-left:70px;'># of Submissions: "+sub_count+"</div><br>";

        maxscore += obj.probs[i][2];

        $("#admin_pl"+obj.probs[i][1]).append(cons);
    }
    $("#competitors_score").html(totalscore.toString()+"/"+maxscore.toString());
    $("#competitors_totalsubs").html(totalsubs);
    $("#competitor_username").html(obj.user[0][0]);
}

function adminSubmissions()
{
    /* Requests to open the submissions list.

    Args:
    */
    hideAdminSections();
    $("#admin_submissions").show();
    curAdminField = "submissions";
    $("#admin_submissions_list").html("Loading...");
    send( {func:"adminSubmissions", cid:adminCID} );
    typeOfSubmissions="adminSubmissions";
}

function adminSubmissionsCallback(obj)
{
    /* Opens the list of every submission for every problem in the competition.

    Args:
        count: The number of submissions
        subs: A double array of all the submissions for the competition
            [0]: submission id
            [1]: submission status
            [2]: submission score
            [3]: problem number
            [4]: problem max score
    */
    $("#admin_submissions").show();
    let submissions = "";
    if(obj.count == 0)
        submissions = "<div style='font-size:20px;'>No submissions found.</div>"
    else
    {
        let subTable = "<table class='problemSubmissionsTable'><tr><th>Problem Number</th><th>ID</th><th>Submission Status</th><th>Options</th><th>Score</th></tr>";
        for(let i=obj.count-1; i >=0; i--)
        {
            let ascore = "?";
            if(obj.subs[i][1] == 2)
                ascore = obj.subs[i][2];
            subTable += "<tr><td>"+obj.subs[i][3]+"</td><td>"+obj.subs[i][0]+"</td><td id='rsid"+obj.subs[i][0]+"'>"+translateSubStatus(obj.subs[i][1])+"</td><td>" +
                        "<button class='sidebarbutton' style='width:auto;display:inline-block;' onclick='adminGetPopUp(\"programcode\", "+obj.subs[i][0]+");'>Code</button>" +
                         "<button class='sidebarbutton' style='width:auto;display:inline-block;' onclick='adminGetPopUp(\"runlog\", "+obj.subs[i][0]+");'>Log</button>" +
                         "<button class='sidebarbutton' style='width:auto;display:inline-block;' onclick='adminCustomRun("+obj.subs[i][0]+");'>CR</button>" +
                         "</td><td>"+obj.subs[i][2]+"/"+obj.subs[i][4]+"</td></tr>";
        }
        subTable += "</table>";
        submissions += subTable;
    }
    $("#admin_submissions_list").html(submissions);
}

function adminScoreboard()
{
    /* Requests to open the admin scoreboard.

    Args:
    */
    hideAdminSections();
    $("#admin_results").show();
    curAdminField = "results";
    $("#admin_results_list").html("Loading...");
    send( {func:"adminScoreboard", cid:adminCID} )
}

function adminScoreboardDivision() {
    /* Requests to open the scoreboard of a specific division.

    Args:
    */
    hideAdminSections();
    $("#admin_results").show();
    curAdminField = "results";
    send( {func:"adminScoreboard", cid:adminCID, division:$("#admin_sb_division_gef").val()} )
    $("#admin_results_list").html("Loading...");
}

function adminScoreboardCallback(obj)
{
    /* Shows the scoreboard.

    Args:
        obj: Everything needed to generate the scoreboard.
    */
    $("#admin_results").show();
    $("#admin_results_list").html(generateScoreboard(obj, true));
}

function adminEditComp() 
{
    /* Requests to open the edit competition page.

    Args:
    */
    hideAdminSections();
    $("#editCompPage").show();
}

function adminGetPopUp(_get, _subid)
{
    /* Requests to open a popup with either a submission's code or its output log. 

    Args:
        _get: Whether to get the code or log
        _subid: The submission's id
    */
    adminShowPopup();
    send( {func:"adminGetPopUp", get:_get, subid: _subid, cid:adminCID} );
}

function adminLoadPopUp(obj)
{
    /* Opens the popup with either a submission's code or its output log.

    Args:
        subid: The submission's id
        pid: The problem's id
        data: The code or the log
    */
    adminShowPopup();
    $("#adminFieldSub").html(
        "<div>"
            +"<div style='color:white;margin-left:60px;margin-right:60px;margin-top:60px;border-radius:20px;width:calc(100% - 120px);background-color:rgb(30,30,30);'>"
                +"<div style='padding:5px;text-align:center;font-size:30px;background-color:rgb(40,40,40);border-radius:20px 20px 0px 0px;border-bottom:solid 1px rgb(60,60,60);'>Problem "+obj.pid+" - Submission "+obj.subid+" - Run Log</div>"
                +"<div style='padding:20px;'>"
                    +"<textarea rows=20 style='width:100%;background-color:rgb(40,40,40);font-size:20px;' id='adminsub"+obj.subid+"logta' readonly>"+ obj.data +"</textarea>"
                +"</div>"
            +"</div>"
        +"<br><br><br></div>");
    $("#adminsub"+obj.subid+"logta").linedtextarea();
}

function adminAddImage()
{
    /* Adds an image to the problem.

    Args:
    */

    //if no file has been chosen
    if($("#newProblemImage").get(0).files.length === 0)
    {
        alert("An image file (jpg, jpeg, png, or gif) must be added before an image can be added.");
        return;
    }

    let reader = new FileReader();

    //https://www.javascripture.com/FileReader
    
    //sends the file as soon as it is retrieved
    reader.onload = function()
    {
        let dataURL = reader.result;
        send({func:"adminAddImage", data:dataURL, pid:curPID, cid:adminCID});
    }

    //gets the chosen file
    reader.readAsDataURL($("#newProblemImage").get(0).files[0])
}

function adminAddImageCallback(obj)
{
    /* Shows the appropriate error message if the system fails to add the image.

    Args:
        id: The image's id
        filename: The name of the image file
    */
    if(obj.result == "bad")
        alert("The file must be jpg, jpeg, png, or gif.")
    else
    {
        let image = "<li id='image_"+obj.id+"' class=\"image_tag\" style='padding:5px;'>"+obj.filename+" <span class='glyphicon glyphicon-trash' style='margin-left:10px;' onclick='adminRemoveImage("+obj.id+");'></span>";
        image += "<img style='display:block;' src='img.php?compkey="+adminCompKey+"&imgid="+obj.id+"&type=admin'> </li>";
        $(image).insertBefore($("#adminAddImageFields"));
    }
}

function adminRemoveImage(id)
{
    /* Removes an image from a problem.

    Args:
        id: The image's id
    */
    if(confirm("Do you really want to delete this image?"))
        send({func:"adminRemoveImage", id:id, pid:curPID, cid:adminCID});
}

function adminRemoveImageCallback(obj)
{
    /* Shows the appropriate error message if the system fails to remove the image.

    Args:
    */
    if(obj.result == "bad")
        alert(obj.reason);
    else
        $("#image_"+obj.id).remove();
}

function adminLevels()
{
    /* Requests to open the difficulty levels list.

    Args:
    */

    //IMPORTANT NOTE: difficulty levels are for problems, while divisions are for competitors

    hideAdminSections();
    $("#admin_levels").show();
    curAdminField = "levels";
    $("#admin_levels_list").html("Loading...");
    send({func:"adminLevels", cid:adminCID});
}

function adminLevelsCallback(obj)
{
    /* Opens the difficulty levels list for the competition.

    Args:
        levels: A double array of all the difficulty levels for the competition
            [0]: level id
            [1]: level name
    */
    let levelsout = "";
    if(obj.levels.length == 0)
    {
        alert("There must be at least one level.");
        levelsout = "<div style='font-size:20px;'>No levels found.</div>";
    }
    else
    {
        levelsout += "<table class='levelsubmissionsTable' style='font-size:20px;width:100%;text-align:center;'><tr><th>ID</th><th>Level Name</th><th>Options</th></tr>";
        for(let i=0; i <obj.levels.length; i++)
        {
            levelsout += "<tr><td>"+obj.levels[i][0]+"</td><td><input type=\"text\" id=\"admin_level_"+obj.levels[i][0]+"_name\" style='border-radius:5px;width:400px;color:white;background-color:rgb(40,40,40);' value=\""+obj.levels[i][1]+"\" disabled> </td>" +
                         "<td style='width:200px;'> <button id=\"admin_level_"+obj.levels[i][0]+"_edit\" class='sidebarbutton' style='border-radius:10px;width:auto;display:inline-block;' onclick='adminEditLevel("+obj.levels[i][0]+");'>Edit</button>" +
                         "<button class='sidebarbutton' style='border-radius:10px;background-color:#d9534f;width:auto;display:inline-block;' onclick='adminDeleteLevel("+obj.levels[i][0]+");'>Remove</button>" + "</td></tr>";
        }
        levelsout += "<tr><td></td><td><input type=\"text\" id=\"admin_level_new_name\" style='border-radius:5px;width:400px;color:black;' value=\"\"> </td>" +
                     "<td style='width:205px;'> <button id=\"admin_level_new_edit\" class='sidebarbutton' style='width:auto;display:inline-block;' onclick='adminAddLevel();'>Add Level</button></td></tr>";
        levelsout += "</table>";
    }
    $("#admin_levels_list").html(levelsout);
    $("#admin_levels").show();
}

function adminEditLevel(lid)
{
    /* Turns the difficulty levels list from "view" to "edit" mode, where a single level's name can be changed.

    Args:
        lid: The id of the difficulty level the admin wants to edit
    */
    $("#admin_level_"+lid+"_name").prop("disabled", false);
    $("#admin_level_"+lid+"_name").css({"background-color":"white", "color":"black"});
    $("#admin_level_"+lid+"_edit").attr("onclick", "adminSaveLevel("+lid+");");
    $("#admin_level_"+lid+"_edit").html("Save");
}

function adminSaveLevel(lid)
{
    /* Turns the difficulty levels list from "edit" to "view" mode, and saves the changes made during "edit" mode.

    Args:
        lid: The id of the difficulty level the admin wants to edit
    */
    if($("#admin_level_"+lid+"_name").val() == "")
    {
        alert("Level name cannot be empty.");
        return;
    }
    send( {func:"adminSaveLevel", lid:lid, name:$("#admin_level_"+lid+"_name").val(), cid:adminCID} );
    $("#admin_level_"+lid+"_name").prop("disabled", true);
    $("#admin_level_"+lid+"_name").css({"background-color":"rgb(40,40,40)", "color":"white"});
    $("#admin_level_"+lid+"_edit").attr("onclick", "adminEditLevel("+lid+");");
    $("#admin_level_"+lid+"_edit").html("Edit");
}

function adminDeleteLevel(lid)
{
    /* Deletes a difficulty level.

    Args:
        lid: The id of the difficulty level the admin wants to edit
    */
    send( {func:"adminDeleteLevel", lid:lid, cid:adminCID} );
}

function adminAddLevel()
{
    /* Adds a difficulty level to the competition

    Args:
    */
    if($("#admin_level_new_name").val() == "")
    {
        alert("Level name cannot be empty.");
        return;
    }

    send( {func:"adminAddLevel", name:$("#admin_level_new_name").val(), cid:adminCID} );
}

function adminGroups()
{
    /* Requests to open the groups list.

    Args:
    */
    hideAdminSections();
    $("#admin_groups").show();
    curAdminField = "groups";
    $("#admin_groups_list").html("Loading...");
    send({func:"adminGroups", cid:adminCID});
}

function adminGroupsCallback(obj)
{
    /* Opens the groups list for the competition.

    Args:
        groups: A double array of all the groups currently in the competition
            [0]: group id
            [1]: group name
            [2]: group division
            [3]: user name
        divisions: A double array of all the competitor divisions in the competition
            [0]: division id
            [1]: division name
    */
    let groupsout = "";
    groupsout += "<table class='groupsubmissionsTable' style='font-size:20px;width:100%;text-align:center;'><tr><th>ID</th><th>Group Name and Division</th><th>Options</th></tr>";
    for(let i=0; i <obj.groups.length; i++)
    {
        let divisions_tmp = "";
        divisions_tmp += "<select id=\"admin_group_"+obj.groups[i][0]+"_division\" style='color:black;display:inline-block;border-radius:8px;padding:3px;margin-left:20px;' disabled>";
        for (let i2 =0;i2<obj.divisions.length;i2++) {
            if (obj.divisions[i2][0]==obj.groups[i][2])
                divisions_tmp += "<option selected value='"+obj.divisions[i2][0]+"'>"+obj.divisions[i2][1]+"</option>";
            else
                divisions_tmp += "<option value='"+obj.divisions[i2][0]+"'>"+obj.divisions[i2][1]+"</option>";
    
            }
        divisions_tmp += "</select>";
        if (obj.groups[i][1] == "Single") {
            divisions_tmp += " ("+obj.groups[i][3]+")";
        }
        groupsout += "<tr><td>"+obj.groups[i][0]+"</td><td><input type=\"text\" id=\"admin_group_"+obj.groups[i][0]+"_name\" style='border-radius:5px;width:400px;color:white;background-color:rgb(40,40,40);' value=\""+obj.groups[i][1]+"\" disabled> " +divisions_tmp+"</td>" +
                     "<td style='width:200px;'> <button id=\"admin_group_"+obj.groups[i][0]+"_edit\" class='sidebarbutton' style='border-radius:10px;width:auto;display:inline-block;' onclick='adminEditGroup("+obj.groups[i][0]+");'>Edit</button>" +
                     "<button class='sidebarbutton' style='border-radius:10px;background-color:#d9534f;width:auto;display:inline-block;' onclick='adminDeleteGroup("+obj.groups[i][0]+");'>Remove</button>" + "</td></tr>";
    }
    groupsout += "<tr><td></td><td><input type=\"text\" id=\"admin_group_new_name\" style='border-radius:5px;width:400px;color:black;' value=\"\"> </td>" +
                 "<td style='width:205px;'> <button id=\"admin_group_new_edit\" class='sidebarbutton' style='width:auto;display:inline-block;' onclick='adminAddGroup();'>Add Group</button></td></tr>";
    groupsout += "</table>";
    $("#admin_groups_list").html(groupsout);
    $("#admin_groups").show();
}

function adminEditGroup(gid)
{
    /* Turns the groups list from "view" to "edit" mode, where a single group's name can be changed.

    Args:
        gid: The id of the group to be edited
    */
    $("#admin_group_"+gid+"_name").prop("disabled", false);
    $("#admin_group_"+gid+"_division").prop("disabled", false);
    $("#admin_group_"+gid+"_name").css({"background-color":"white", "color":"black"});
    $("#admin_group_"+gid+"_edit").attr("onclick", "adminSaveGroup("+gid+");");
    $("#admin_group_"+gid+"_edit").html("Save");
}

function adminSaveGroup(gid)
{
    /* Turns the groups list from "edit" to "view" mode, and the edits made are saved.

    Args:
        gid: The id of the group to be updated
    */
    if($("#admin_group_"+gid+"_name").val() == "")
    {
        alert("Group name cannot be empty.");
        return;
    }
    send( {func:"adminSaveGroup", gid:gid, division:$("#admin_group_"+gid+"_division").val(), name:$("#admin_group_"+gid+"_name").val(), cid:adminCID} );
    $("#admin_group_"+gid+"_name").prop("disabled", true);
    $("#admin_group_"+gid+"_division").prop("disabled", true);
    $("#admin_group_"+gid+"_name").css({"background-color":"rgb(40,40,40)", "color":"white"});
    $("#admin_group_"+gid+"_edit").attr("onclick", "adminEditGroup("+gid+");");
    $("#admin_group_"+gid+"_edit").html("Edit");
}

function adminDeleteGroup(gid)
{
    /* Deletes a group.

    Args:
        gid: The id of the group to be deleted
    */
    send( {func:"adminDeleteGroup", gid:gid, cid:adminCID} );
}

function adminAddGroup()
{
    /* Adds a group.

    Args:
    */
    if($("#admin_group_new_name").val() == "")
    {
        alert("Group name cannot be empty.");
        return;
    }

    send( {func:"adminAddGroup", name:$("#admin_group_new_name").val(), cid:adminCID} );
}