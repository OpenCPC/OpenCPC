let levels = ["easy", "medium", "hard"];
/*
function getCompObj(cid)
{
    for(let i=0; i<compInfoArray.length; i++)
    {
        if(compInfoArray[i].cid == cid)
        {
            return compInfoArray[i];
        }
    }
    return null;
}
*/



function openProblemList(obj)
{
    /* Opens the list of problems.

    Args:
        levels: A double array of all the difficulty levels in the competition.
            [0]: name
        probs: A double array of all the problems in the competition.
            [0]: level
            [1]: name
            [2]: id
            [3]: number
            [4]: max score
        subs: A double array of the group's performance on each problem 
            [0]: highest score of any submission on the problem
            [1]: problem id of the submission
    */
    $("#problemlist").show();
    curBackground = "none";
    curField = "problemlist";
    let levelsout = "";
    for(let i=0; i < obj.levels.length; i++)
    {
        levelsout += "<table> <tr> <td style='padding:5px;'>"+obj.levels[i][0]+"</td> <td style='width:100%;'>"+
                     "<div style='height:1px;width:100%;background-color:rgb(60,60,60);'> </div></td> </tr> </table>"+
                     "<div id='pl"+obj.levels[i][0]+"'> </div>"
    }
    $("#problemListInner").html(levelsout);
    for(let i=0; i < obj.levels.length; i++)
    {
        currLvl = obj.levels[i][0];
        loadProblemList(obj.probs.filter(lvlFilter), obj.subs)
    }
}
function generateProblemCircleColor(percent) {
    /* Return a set color for a certain percentage correct on a problem.

    Args:
        percent: The number of points earned divided by max points on a problem
    */
    if(percent == 0)
        return "#EE7700";
    else if(percent < 0.5)
        return "#EEEE00";
    else if(percent < 1)
        return "#00ADFF";
    else
        return "#00EE00";

}
function generateProblemRectangleColor(percent) {
    /* 

    Args:
    */
    if(percent == 0)
        return "#750000";
    else if(percent < 0.5)
        return "#9D9D00";
    else if(percent < 1)
        return "#007BB5";
    else
        return "#108000";

}

function loadProblemList(probs, subs)
{
    /* Loads the list of problems.

    Args:
        probs: A double array of all the problems in a given level in the competition
            [0]: level
            [1]: name
            [2]: id
            [3]: number
            [4]: max score
        subs: A double array of the group's performance on each problem 
            [0]: highest score of any submission on the problem
            [1]: problem id of the submission
    */
    let cons = "";
    for(let i=0; i < probs.length; i++)
    {
        let backgroundColor = "#FFFFFF";
        for(let j=0; j < subs.length; j++)
        {
            if(probs[i][2] == subs[j][1])
            {
                let percent = subs[j][0]/probs[i][4];
                backgroundColor = generateProblemCircleColor(percent);
            }
        }
        cons += "<div onclick='openProblem(" + probs[i][2] + ");'style='cursor:pointer;box-sizing:content-box;position:relative;border-radius:4px;padding:4px 4px 4px 24px;background-color:rgb(40,40,40);border:solid 1px rgb(60,60,60);display:inline-block;height:16px;'>\
                 <div style='position:absolute;left:4px;top:4px;width:16px;height:16px;border-radius:100%;background-color:" + backgroundColor + "'> </div>\
                 " + probs[i][3] + ". " + probs[i][1] + " ("+probs[i][4]+")"+"</div> ";
    }
    $("#pl"+currLvl).html(cons);
}

function lvlFilter(curr)
{
    /* Filter each problem by its level.

    Args:
        curr: The current problem
    */
    if(curr[0] == currLvl)
        return true;
    return false;
}

function loadScoreboard(obj)
{
    /* Loads the scoreboard.

    Args:
        users: An array of every user in the competition
    */
    curBackground = "none";
    let scoreboard = "<div style='font-size:20px;text-align:center;margin:20px 20px 30px 20px;'>Top 10</div><table class='problemSubmissionsTable'><tr><th>Place</th><th>Name</th><th>Score</th></tr>";
    for(let i=0; i < obj.users.length; i++)
    {
        scoreboard += "<tr><td>"+i+"</td><td>"+rj.users[i].name+"</td><td>"+rj.users[i].score+"</td></tr>";
    }
    $("#scoreboardInner").html(scoreboard);
}

//button hooks
function sbProblemList() {
    /* Request the problem list.

    Args:
    */
    hideAllFields();
    $("#plEasy").html("");
    $("#plMedium").html("");
    $("#plHard").html("");
    $("#problemlist").show();
    curField = "problemlist";

    let obj = { func: "getProblemList", cid:currCompId };
    send(obj); 
}

function sbScoreboard() {
    /* Request the scoreboard.

    Args:
    */
    hideAllFields();
    curField='Scoreboard';
    $('#scoreboard').show();
    $("#scoreboardInner").html("Loading...");
    let obj = { func: "getScoreboard", cid:currCompId };
    send(obj);
}

function generateScoreboard(obj, showAdmin=false) {

    //All the competition's groups, indexed by group id
    let groups = {};
    //A list of group ids to be sorted later
    let groups_sort_arr = [];
    //Set up the groups
    for (let i = 0; i < obj.groups.length;i++) {
        //New group
        groups[obj.groups[i][1]] = {};
        groups_sort_arr.push(obj.groups[i][1]);
        groups[obj.groups[i][1]].name = obj.groups[i][0];
        groups[obj.groups[i][1]].users = "";
        //Each problem for that group
        groups[obj.groups[i][1]].problems = {};
        for (let i2=0;i2<obj.problems.length;i2++) {
            groups[obj.groups[i][1]].problems[obj.problems[i2][2]] = {
                name: obj.problems[i2][0],
                number: obj.problems[i2][1],
                max: obj.problems[i2][3],
                score: 0,
                ct: 0
            };
        }
        groups[obj.groups[i][1]].total = 0;
        groups[obj.groups[i][1]].last_submission_increase_time = 0;
    }
    for (let i=0;i<obj.best_scores.length;i++) {
        groups[obj.best_scores[i][2]].total += obj.best_scores[i][0];
        if (obj.best_scores[i][0] > 0) {
            groups[obj.best_scores[i][2]].last_submission_increase_time = 
                Math.max(groups[obj.best_scores[i][2]].last_submission_increase_time, obj.best_scores[i][4]);
        }
        groups[obj.best_scores[i][2]].problems[obj.best_scores[i][3]].score = obj.best_scores[i][0];
        groups[obj.best_scores[i][2]].problems[obj.best_scores[i][3]].ct = obj.best_scores[i][1];
    }
    for (let i=0;i<obj.users.length;i++) {
        if (groups[obj.users[i][1]].users=="") 
            groups[obj.users[i][1]].users += obj.users[i][0];
        else
            groups[obj.users[i][1]].users += ", " + obj.users[i][0];
    }

    var accul = "";
    if (showAdmin) {
        accul += "Division: "+obj.division[1]+" ("+obj.division[0]+") <select id='admin_sb_division_gef' style='color:black;display:inline-block;border-radius:8px;padding:3px;margin-left:20px;'>";
        for (let i=0;i<obj.divisions.length;i++) {
            accul+="<option value='"+obj.divisions[i][0]+"'>"+obj.divisions[i][1]+"</option>";
        }
        accul+= "</select> <button style='color:black;' onclick='adminScoreboardDivision();'>Load</button><br>";
    }
    accul += "Problem numbers are on the right. Problem status boxes have the current score at the top and the total number of submissions at the bottom.<br><br>"
        +"<table class='problemSubmissionsTable'><tr><th style='width:100px;'>Place</th><th style='width:200px;'>Group<div style='font-size:12px;'>Members</div></th><th style='width:100px;'>Total</th>";
    for (let i=0;i<obj.problems.length;i++) {
        accul += "<th>" + obj.problems[i][1] + "</th>";
    }
    accul += "</tr>";
    groups_sort_arr.sort(function(l, r){
        let x = groups[l];
        let y = groups[r];
        if (x.total > y.total)
            return -1;
        if (x.total < y.total)
            return 1;
        if (x.last_submission_increase_time < y.last_submission_increase_time)
            return -1;
        if (x.last_submission_increase_time > y.last_submission_increase_time)
            return 1;
        return 0;
    });
    let current_place = 0;
    for (var i=0;i<groups_sort_arr.length;i++) {
        let g = groups[groups_sort_arr[i]];
        if (g.name == "Admin") {
            if (!showAdmin)
                continue;
        }
        else
            current_place += 1;
        accul+="<tr><td>" + current_place + "</td>";
        if (g.name=="Single") {
            accul+="<td>"+g.users+"</td>";
        }
        else {
            accul+="<td><div style='display:inline-block;width:100%;max-width:150px;word-break:break-word;text-align:center;'>"+g.name
            +"<div style='font-size:12px;'>"+g.users+"</div></div></td>";
        }
        accul+="<td>"+g.total+"</td>";
        for (let i2=0;i2<obj.problems.length;i2++) {
            if (g.problems[obj.problems[i2][2]].ct != 0)

                accul += "<td style='background-color:"+generateProblemRectangleColor(g.problems[obj.problems[i2][2]].score /g.problems[obj.problems[i2][2]].max )+";'>" 
                +  g.problems[obj.problems[i2][2]].score 
                    + "<div style='font-size:12px;'>"+g.problems[obj.problems[i2][2]].ct
                    +"</div></td>";
            else
                accul += "<td></td>";
        }
        accul+="</tr>";
    }
    accul += "</table>";
    return accul;
}

function sbScoreboardCallback(obj)
{
    $("#scoreboardInner").html(generateScoreboard(obj));
    $("#scoreboard").show();
}

function sbAllSubmissions() {
    hideAllFields();
    curField='AllSub';
    $('#allSubmissions').show();
    send( {func:"getAllSubmissions", cid:currCompId} );
}

function sbAllSubmissionsCallback(obj)
{
    curBackground = "none";
    let submissions = "";
    $('#allSubmissions').show();
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
                        "<button class='sidebarbutton' style='width:auto;display:inline-block;' onclick='getPopUp(\"programcode\", "+obj.subs[i][0]+");'>Code</button>" +
                         "<button class='sidebarbutton' style='width:auto;display:inline-block;' onclick='getPopUp(\"runlog\", "+obj.subs[i][0]+");'>Log</button>" +
                         "</td><td>"+obj.subs[i][2]+"/"+obj.subs[i][4]+"</td></tr>";
        }
        subTable += "</table>";
        submissions += subTable;
    }
    $("#allProblemSubmissions").html(submissions);
    $('#allSubmissions').show();
}