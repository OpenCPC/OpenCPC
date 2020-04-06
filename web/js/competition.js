var curField = "backlay";
var curBackground = "none";
var liveScoring = [];
var typeOfSubmissions="clientSubmissions";
var endTime;
let curProblemID = -1;
var currProblemNum = -1;
var currCompId = -1;

function loadCompetition(_id) {
    /* Requests to load a competition.

    Args:  
        _id: The id of the competition to load
    */
    hideAllSections();
    hideAllFields();
    $("#web_header").show();
    $("#competition_page").show();
    $("#competition_overlay").show();
    $("#competition_overlayTitle").html("Loading...");
    $("#competition_overlayLong").html("Retrieving Info...");
    $("#competition_time").html("Loading...");
    curField = "none";
    send({func:"getCompetitionInfo",cid:_id})
}

function getCompetition(obj)
{
    /* Loads the competition.

    Args:
        competitionkey: 
        name: The competition's name
        group: The competitor's group in the competition
        division: The competitor's division in the competition
    */
    curPage = "competition";
    curCompKey = obj.competitionkey;
    hideAllSections();
    hideAllFields();
    currCompId = obj.id;
    $("#competition_name").html(obj.name);
    $("#competition_overlayTitle").html("Loading Competition");
    $("#competition_overlayLong").html("");
    $("#competition_overlay").show();
    $("#competition_page").show();
    $("#web_header").show();
    $("#backlay").show();
    $("#sidebar_group").html(obj.group);
    $("#sidebar_division").html(obj.division);
    $("#top_competition_name").html(" - "+obj.name);
    curField = "backlay";
}

function hideAllFields() {
    /* Hides all competition pages.

    Args:
    */
    $("#backlay").hide();
    $("#problemlist").hide();
    $("#problemchart").hide();
    $("#scoreboard").hide();
    $("#allSubmissions").hide();
    $(".problemd").hide();
    $("#loading").hide();
    if($("#fieldSubShadow").is(":visible"))
        returnFromFieldSub();
}

function translateSubStatus(status)
{
    /* Translates a set submission status number into a message.

    Args:
        status: a number (0, 1, 2) that represents "waiting for processing", "compile failed", and "graded", respectively
    */
    switch(status)
    {
        case 0:
            return "Submitted, waiting for processing...";
        case 1:
            return "Compile failed. Check log.";
        case 2:
            return "Graded.";
        }
}

function problemDescriptionParse(str) {
    /* Goes through the problem's text and customizes specific parts of it.

    Args:
        str: The problem's text
    */
    str = htmlspecialchars(str);
    str = str.replace(/[\r\n]*\[input\][\r\n]*/gi, "<div style=\"font-weight:bold;text-align:left;margin-top:20px;margin-bottom:20px;\">Input</div>");
    str = str.replace(/[\r\n]*\[output\][\r\n]*/gi, "<div style=\"font-weight:bold;text-align:left;margin-top:20px;margin-bottom:20px;\">Output</div>");
    str = str.replace();
    str = str.replace(/\n/g, "<br>");

    let regex = /\[image_([0-9]*)\]*/g;
    while(m=regex.exec(str))
    {
        str = str.replace(m[0], "<img style='display:block;' src='img.php?compkey="+curCompKey+"&imgid="+m[1]+"&type=comp'></img>");
    }
    return str;
}

function openProblem(problemID) {
    /* Requests to open a problem.

    Args:
        problemID: The problem's id
    */
    hideAllFields();
    curBackground = "problem"+problemID;
	if ($("#problem"+problemID).length>0) {
        $("#problem"+problemID).remove();
	}
    $("#loading").show();
    send({ func:"openProblem",pid:problemID,cid:currCompId} );
    typeOfSubmissions="clientSubmissions";
}

function openProblemCallback(obj) {
    /* Opens the problem.

    Args:
        pid: The problem's id
        pnum: The problem number in the competition
        pms: The max score
        pt: The problem's text
        rl: Runtime limit
        ml: Memory limit
        subs: An array of all the submissions the group has for the problem
            [0]: id
            [1]: status
            [2]: score
        cases: An array of all the sample cases of the problem
            [0]: input
            [1]: expected output
    */
    hideAllFields();
    curProblemID = obj.pid;
    curField = "problem";
    problem = obj.pid;
    currProblemNum = obj.pnum;
    $("#loading").hide();

    //Set up page with places for the problem name, text, description, images, runtimelimit, memorylimit, etc., as well as a table for its sample/test cases
    if ($("#problem"+problem).length<=0) {
		$("#field").append(
            "<div id='problem"+problem+"' class='problemd'>"
                +"<div id='problem"+problem+"subpanel' style='color:white;margin-left:60px;margin-right:60px;margin-top:60px;border-radius:20px;width:calc(100% - 120px);background-color:rgb(30,30,30);'>"
                    +"<div style='padding:5px;text-align:center;font-size:30px;background-color:rgb(40,40,40);border-radius:20px 20px 0px 0px;border-bottom:solid 1px rgb(60,60,60);' id='problemTitle'>Problem "+obj.pnum+". "+obj.pname+" ("+obj.pms+")</div>"
                    +"<div style='padding:20px;font-size:20px;'>"
                        +"<div style=\"font-size:30px;text-align:left;margin-top:20px;\">Problem Description</div>"
                        +"<div style=\"padding-left:20px;\">"
                            +"<div style='width:100%;margin-top:20px;' id='problemQuestion'>" + problemDescriptionParse(obj.pt) + "</div>"
                            +"<div style=\"font-weight:bold;text-align:left;margin-top:20px;display:inline-block;\">Grading Server Specifications</div>"
                            +"<div id='"+problem+"_gradingSpecsToggle' class='glyphicon glyphicon-chevron-up' style='top:4px;margin-left:10px;' onclick='gradingSpecsToggle("+problem+")'></div>"
                            +"<br>"
                            +"<ul id='"+problem+"_gradingSpecsList' style=\"margin-top:20px;height:auto;\">"
                                +"<li style=\"padding:5px;\" id='"+problem+"runtimeLimit'>Runtime Limit: "+obj.rl+"s</li>"
                                +"<li style=\"padding:5px;\" id='"+problem+"memoryLimit'>Memory Limit: "+obj.ml+"MB</li>"
                                +"<li style=\"padding:5px;\">Input/Output: Standard</li>"
                            +"</ul>"
                            +"<div style=\"font-weight:bold;text-align:left;margin-top:20px;display:inline-block;\">Sample Cases</div>"
                            +"<div id='"+problem+"_sampleCasesToggle' class='glyphicon glyphicon-chevron-up' style='top:4px;margin-left:10px;' onclick='sampleCasesToggle("+problem+")'></div>"
                            +"<br>"
                            +"<ul id='"+problem+"_sampleCasesList' style='margin-top:20px;font-size:20px;'>"
                            +"</ul>"
                        +"</div>"
                        +"<div style=\"font-size:30px;text-align:left;margin-top:20px;\">New Submission</div>"
                        +"<div style='margin-top:20px;'><textarea rows=20 style='width:100%;background-color:rgb(40,40,40);font-size:20px;' id='problem"+problem+"Textarea' placeholder='Copy and paste your code here...'></textarea></div>"
                        +"<button style='width:auto;margin-top:30px;display:inline-block;' class='sidebarbutton' onclick='submitProblem("+problem+",\"c\");'>Submit C 11</button>"
                        +"<button style='width:auto;margin-top:30px;display:inline-block;' class='sidebarbutton' onclick='submitProblem("+problem+",\"cpp\");'>Submit C++ 11</button>"
                        +"<button style='width:auto;margin-top:30px;display:inline-block;' class='sidebarbutton' onclick='submitProblem("+problem+",\"py\");'>Submit Python 3.5.2</button>"
                        +"<button style='width:auto;margin-top:30px;display:inline-block;' class='sidebarbutton' onclick='submitProblem("+problem+",\"java\");'>Submit Java 1.8.0</button>"
    
                    +"</div>"
                +"</div>"
                +"<div id='problem"+problem+"submissionsd' style='color:white;margin-left:60px;margin-right:60px;margin-top:60px;border-radius:20px;width:calc(100% - 120px);background-color:rgb(30,30,30);'>"
                    +"<div style='padding:5px;text-align:center;font-size:30px;background-color:rgb(40,40,40);border-radius:20px 20px 0px 0px;border-bottom:solid 1px rgb(60,60,60);' id='subsTableTitle'>Problem "+obj.pnum+" ("+obj.subs.length+") - Submissions</div>"
                    +"<div style='padding:20px;' id='problem"+problem+"Submissions'>"
                        +"Loading..."
                    +"</div>"
                +"</div>"
            +"<br><br><br></div>");
            $("#problem"+problem+"Textarea").linedtextarea();
            $("#problem"+problem).show();
    }

    //Set up sample/test cases table
    $("#"+problem+"_sampleCasesList").html("");
    for(let i=0; i < obj.cases.length; i++)
    {
        $("#"+problem+"_sampleCasesList").append(
             "<li style='padding:5px;'>"
            +"<div style='display:inline-block;'> Test Case "+(i+1).toString()+"</div>"
            +"<div id='"+problem+"_"+i.toString()+"_caseToggle' class='glyphicon glyphicon-chevron-down' style='top:4px;margin-left:10px;' onclick='caseToggle("+problem+", "+i+")'></div>"
            +"<br>"
            +"<div id='"+problem+"_"+i.toString()+"_case' style='display:none;height:auto;'>"
            +"<span style='vertical-align:top;'>Input: </span><div style='display:inline-block;'>" + htmlspecialchars(obj.cases[i][0]).replace(/\n/g, "<br>") + "</div>"
            +"<br>"
            +"<span style='vertical-align:top;'>Output: </span><div style='display:inline-block;'>" + htmlspecialchars(obj.cases[i][1]) .replace(/\n/g, "<br>") + "</div>"
            +"</div>"
            +"</li>"
        );
    }
    refreshSubmissions(problem, currCompId);
}

function sampleCasesToggle(pid)
{
    /* Open or close the sample cases section.

    Args:
        pid: The problem's id
    */
    if($("#"+pid+"_sampleCasesList").is(":visible"))
        $("#"+pid+"_sampleCasesToggle").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
    else
        $("#"+pid+"_sampleCasesToggle").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
    $("#"+pid+"_sampleCasesList").animate({height:'toggle'});
}

function gradingSpecsToggle(pid)
{
    /* Open or close the grading specifications section showing memory and runtime limit.

    Args:
        pid: The problem's id
    */
    if($("#"+pid+"_gradingSpecsList").is(":visible"))
        $("#"+pid+"_gradingSpecsToggle").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
    else
        $("#"+pid+"_gradingSpecsToggle").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
    $("#"+pid+"_gradingSpecsList").animate({height:'toggle'});
}

function caseToggle(pid, caseid)
{
    /* Open or close the specifics (input and expected output) of each sample case.

    Args:
        pid: The problem's id
        caseid: The sample case's id
    */
    if($("#"+pid+"_"+caseid+"_case").is(":visible"))
        $("#"+pid+"_"+caseid+"_caseToggle").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
    else
        $("#"+pid+"_"+caseid+"_caseToggle").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
    $("#"+pid+"_"+caseid+"_case").animate({height:'toggle'});
}

function refreshSubmissions(problem, competitionid)
{
    /* Retrieve the current user's group's submissions.

    Args:  
        problem: The problem's id
        competitionid: The competition's id
    */
    send( {func:"getSubmissions", pid:problem, cid:competitionid} )
}

function refreshSubmissionsCallback(obj)
{
    /* Update the submissions table.

    Args:
        subs: An array of all the group's submissions.
        pid: The problem's id
    */
    let submissions = "";
    if(obj.subs.length == 0)
        submissions = "<div style='font-size:20px;'>No submissions found </div>";
    else
    {
        let subTable = "<table class='problemSubmissionsTable'><tr><th>ID</th><th>Submission Status</th><th>Options</th><th>Score</th></tr>";
        for(let i=obj.subs.length-1; i >=0; i--)
        {
            let ascore = "?";
            if(obj.subs[i][1] == 2)
                ascore = obj.subs[i][2];
            subTable += "<tr id='submissionListRow"+obj.subs[i][0]+"'><td>"+obj.subs[i][0]+"</td><td id='rsid"+obj.subs[i][0]+"'>"+translateSubStatus(obj.subs[i][1])+"</td><td>" +
                        "<button class='sidebarbutton' style='width:auto;display:inline-block;' onclick='getPopUp(\"programcode\", "+obj.subs[i][0]+");'>Code</button>" +
                         "<button class='sidebarbutton' style='width:auto;display:inline-block;' onclick='getPopUp(\"runlog\", "+obj.subs[i][0]+");'>Log</button>" +
                         "</td><td>"+ascore+"/"+obj.pms+"</td></tr>";
        }
        subTable += "</table>";
        submissions += subTable;
    }
    $("#problem"+obj.pid+"Submissions").html(submissions);

    paintLive();
}

function submitProblem(problem, extension)  
{
    /* Submits the user's code.

    Args:
        problem: The problem's id
        extension: The language the code is written in
    */
    if (extension=='java') {
        if ($("#problem"+curProblemID+"Textarea").val().indexOf("Problem"+currProblemNum) == -1) {
            alert("Please make your class name be 'Problem" + currProblemNum + "'.");
            return;
        }
    }
    let obj = {
        func: "submitProblem",
        cid: currCompId,
        pid: curProblemID,
        programcode: $("#problem"+curProblemID+"Textarea").val(),
        programtype: extension
    }
    $("#problem"+curProblemID+"Textarea").val('');
    $("#field").animate({scrollTop:$("#problem"+problem+"subpanel").height()-200},500);
    send(obj);
    //$("#field").addClass("fieldNewSubmission");
    //setTimeout(function(){$("#field").removeClass("fieldNewSubmission");},500);
    refreshSubmissions(curProblemID, currCompId);
    
}

function paintLive() {
    /* Animates the submission and grading process for each submission.

    Args:
    */
    for (var i6 = 0; i6 < liveScoring.length; i6++) {
        var tarr = liveScoring[i6];
        if ($("#rsid"+tarr[0]).length > 0) {

            var c = "";

            if (tarr[2]=="stop" || tarr[2]=="stopped") {
                c+="Finished Grading: ";
            }
            else {
                c+="Grading (Live): ";
            }
            

            if (tarr[2]=="init") {
                c+="Compiling... ";
                $("#submissionListRow"+tarr[0]).addClass("submissionLiveCompiling");
            }
            else {
                $("#submissionListRow"+tarr[0]).removeClass("submissionLiveCompiling");
                if (tarr[2] != "stop" && tarr[2] != "stopped")
                    $("#submissionListRow"+tarr[0]).addClass("submissionLiveGrading");
                if (tarr[1]!=-2) {

                    for (let i =0; i< tarr[1];i++) {
                        if (tarr[i+3] == -1)
                            c+="[ ] ";
                        else if (tarr[i+3] == 0)
                            c+="<span style='color:red;'>[X]</span> ";
                        else if (tarr[i+3] == 1)
                            c+="<span style='color:green;'>[O]</span> ";
                        else if (tarr[i+3] == -2)
                            c+="<span style='color:yellow;'>[?]</span> ";
                        else if (tarr[i+3] == -3)
                            c+="<span style='color:red;'>[-]</span> ";
                        else if (tarr[i+3] == -4)
                            c+="<span style='color:red;'>[T]</span> ";
                        else if (tarr[i+3] == -5)
                            c+="<span style='color:red;'>[E]</span> ";
                        else if(tarr[i+3] == -6)
                        c+="<span style='color:red;'>[M]</span> ";
                    }
                }
                else {
                    c+="Compile Failed.";
                }
            }

            if (tarr[2]=="stop") {
                $("#submissionListRow"+tarr[0]).removeClass("submissionLiveGrading");
                $("#submissionListRow"+tarr[0]).addClass("submissionLiveStop");
            }

            $("#rsid"+tarr[0]).html(c);
        }
    }
}

function compLive(obj) {
    /* Grades the submission live.

    Args:
        command:
        subid: The submission's id
        input_len:
        index:
    */
    params = obj.params;
    var tarr = -1;

    if (params.command == "init") {
        tarr = [params.subid, params.input_len, "init"];
        for (let i =0; i< params.input_len;i++) {
            tarr.push(-1);
        }
        liveScoring.push(tarr);
    }
    else {
        for (let i = 0; i < liveScoring.length; i++) {
            if (liveScoring[i][0] == params.subid) {
                tarr = liveScoring[i];
            }
        }

    }

    tarr[2] = params.command

    if (tarr==-1)
        return;

    if (params.command=="case") {
        tarr[3+params.index] = -2;
    }
    else if (params.command=="co") {
        tarr[3+params.index] = 1;
    }
    else if (params.command=="io") {
        tarr[3+params.index] = 0;
    }
    else if (params.command=="comf") {  
        tarr[1] = -2;        
    }
    else if (params.command=="rtlet") {  
        tarr[3+params.index] = -4;        
    }
    else if(params.command=="mlet")
    {
        tarr[3+params.index] = -6;
    }
    else if (params.command=="rte") {  
        tarr[3+params.index] = -5;        
    }
    else if(params.command=="stop") {

    }
    else {
        if (params.input_len>=0)
            tarr[3+params.index] = -3;
    }

    paintLive();
    if (tarr[2] == "stop") {
        tarr[2] = "stopped";
        setTimeout(function(){if (typeOfSubmissions=="clientSubmissions")refreshSubmissions(curProblemID, currCompId);else if (typeOfSubmissions=="adminSubmissions") send( {func:"adminSubmissions", cid:adminCID} );}, 500);
    }
} 

function getPopUp(_get, _subid)
{
    /* Request to open popup of the submission's code or runlog.

    Args:
        _get: Whether to retrieve the code or runlog
        _subid: The submission's id
    */
    showPopup();
    send( {func:"getPopUp", get:_get, subid: _subid, cid:currCompId} );
}

function loadPopUp(obj)
{
    /* Loads the popup with the submission's code or runlog.

    Args:
        type: Whether the code or runlog has been retrieved
        subid: The submission's id
        data: The code or runlog text
    */
    showPopup();
    let header = "";
    if(obj.type == "programcode")
        header = "Code";
    else if (obj.type == "runlog")
        header = "Run Log";
    else
        header = "Something's Wrong. Contact Site Admin."
    $("#fieldSub").html(
        "<div>"
            +"<div style='color:white;margin-left:60px;margin-right:60px;margin-top:60px;border-radius:20px;width:calc(100% - 120px);background-color:rgb(30,30,30);'>"
                +"<div style='padding:5px;text-align:center;font-size:30px;background-color:rgb(40,40,40);border-radius:20px 20px 0px 0px;border-bottom:solid 1px rgb(60,60,60);'>Problem "+currProblemNum+" - Submission "+obj.subid+" - "+header+"</div>"
                +"<div style='padding:20px;'>"
                    +"<textarea rows=20 style='width:100%;background-color:rgb(40,40,40);font-size:20px;' id='sub"+obj.subid+"logta' readonly>"+ obj.data +"</textarea>"
                +"</div>"
            +"</div>"
        +"<br><br><br></div>");
    $("#sub"+obj.subid+"logta").linedtextarea();
    hideLoading();
}

function competitionRefreshField() {
    /* Refresh the submissions table if the competitor is currently viewing a problem.

    Args:
    */
    if (curField == "problem") {
        refreshSubmissions(curProblemID, currCompId);
    }
}

function updateQuestion(obj)
{
    /* Update the contents of a question.

    Args:
        cid: The competition's id
        pid: The problem's id
        question: The problem's text
        runtimelimit: max runtime limit (in seconds)
        memorylimit: max memory limit (in MB)
    */
    if(obj.cid == currCompId)
    {
        if(curField == "problemlist")
        {
            sbProblemList();
        }
        else if(obj.pid == curProblemID)
        {
            $("#problemQuestion").html(problemDescriptionParse(obj.question));
            $("#"+obj.pid+"runtimeLimit").html("Runtime Limit: " + obj.runtimeLimit.toString() + "s");
            $("#"+obj.pid+"memoryLimit").html("Memory Limit: " + obj.memoryLimit.toString() + "MB");
        }
    }
}