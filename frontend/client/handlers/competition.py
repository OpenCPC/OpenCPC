import websockets
import asyncio
import pickle
import json
import time
import re
import bcrypt
import smtplib
import ssl
import jwt
import random
import base64
import os
from PIL import Image
from io import BytesIO
from email.mime.text import MIMEText

from ..utility import (
    isLoggedIn, inComp, isDuringCompetition, compStatus, isAdmin, isScoreboardAllowed,
    CompetitionStatus
)

async def getCompetitionInfo(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await inComp(params["cid"], uobj)):
        return
    sql = uobj.storage.sql

    tmp = await sql.execute("SELECT competitionname, competitionstatus, duration, type, adminid, endTime, short_desc, competitionkey, startTime, automatic FROM competitions WHERE id=%s", (params["cid"]))
    results = await tmp.fetchone()
    tmp = await sql.execute("""
    SELECT divisions.name, divisions.id
    FROM divisions
    INNER JOIN participants
    INNER JOIN groups
        ON groups.id = participants.groupid
            AND groups.division = divisions.id
    WHERE participants.userid=%s AND participants.competitionid=%s""",[params["uid"], params["cid"]])
    division = await tmp.fetchall()
    if len(division) == 1:
        division = division[0][0]
    elif len(division) > 1:
        raise RuntimeError("bruh")
    else:
        division = "Default"
    tmp = await sql.execute("""
    SELECT groups.name, groups.id
    FROM participants
    INNER JOIN groups
        ON groups.id = participants.groupid
    WHERE participants.userid=%s AND participants.competitionid=%s""",[params["uid"], params["cid"]])
    group = (await tmp.fetchall())[0]
    group = str(group[0]) + " (" + str(group[1]) + ")"
    current_time = int(time.time() * 1000)
    await uobj.ws.send(json.dumps({"func":"getCompetitionInfo", "division":division, "current_time": current_time, "group": group, "name":results[0], "status":results[1], "duration":results[2], "type":results[3], "adminid":results[4], "id":params["cid"], "endTime":results[5], "short_desc":results[6], "competitionkey":results[7], "startTime":results[8], "automatic":results[9]}))

#params -- cid
async def getProblemList(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await inComp(params["cid"], uobj)) or not(await isDuringCompetition(params["cid"],uobj)):
        return
    sql = uobj.storage.sql

    probTmp = await sql.execute("""SELECT level, problemname, id, problemnumber, maxscore FROM problems
                                        WHERE competitionid=%s ORDER BY problemnumber""", (params["cid"]))
    probResults = await probTmp.fetchall()

    # GROUPID IMPLEMENT
    subTmp = await sql.execute("""SELECT MAX(submissions.score), submissions.problemid FROM submissions INNER JOIN problems ON problems.id=submissions.problemid 
                                       INNER JOIN participants ON participants.groupid=submissions.groupid
                                       WHERE submissions.competitionid=%s AND participants.userid=%s GROUP BY problemid ORDER BY problems.problemnumber""", (params["cid"], uobj.uid))
    subResults = await subTmp.fetchall()

    tmp = await sql.execute("SELECT name FROM levels WHERE competitionid=%s", [params["cid"]])
    lvlResults = await tmp.fetchall()
    await uobj.ws.send(json.dumps({"func":"getProblemList", "probs":probResults, "subs":subResults, "levels":lvlResults}))
async def getSubmissions(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await inComp(params["cid"], uobj)) or not(await isDuringCompetition(params["cid"],uobj)):
        return
    sql = uobj.storage.sql
    # GROUPID IMPLEMENT
    subTmp = await sql.execute("""SELECT id, status, score FROM submissions WHERE problemid=%s AND groupid=%s ORDER BY submissiontime""", 
                                       (params["pid"], uobj.groups[params["cid"]]))
    subResults = await subTmp.fetchall()
    probTmp = await sql.execute("SELECT maxscore FROM problems WHERE id=%s AND competitionid=%s", (params["pid"], params["cid"]))
    probResults = await probTmp.fetchone()
    if probResults==None:
        print("ERROR probResults==None",params)
    else:
        await uobj.ws.send(json.dumps( {"func":"getSubmissions", "subs":subResults, "pid":params["pid"], "cid":params["cid"], "pms":probResults[0]} ))

#params -- cid, pid
async def openProblem(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await inComp(params["cid"], uobj)) or not(await compStatus(params["cid"], uobj) == CompetitionStatus.DURING):
        return
    sql = uobj.storage.sql
    tmp = await sql.execute("SELECT id, problemnumber, problemtext, level, maxscore, competitionid, problemname, runtimelimit, memorylimit FROM problems WHERE id=%s", [params["pid"]])
    results = await tmp.fetchall()

    # GROUPID IMPLEMENT
    subTmp = await sql.execute("""SELECT id, status, score FROM submissions WHERE problemid=%s AND groupid=%s ORDER BY submissiontime""", 
                                       [params["pid"], uobj.groups[params["cid"]]])
    subResults = await subTmp.fetchall()
    sampleTmp = await sql.execute("SELECT input, expected FROM cases WHERE value=%s AND problemid=%s AND competitionid=%s", [-1, params["pid"], params["cid"]])
    sampleResults = await sampleTmp.fetchall()
    if len(results) == 1:
        await uobj.ws.send(json.dumps({"func":"openProblem", "rl":results[0][7], "ml":results[0][8], "pid":results[0][0], "pnum":results[0][1], "pt":results[0][2], "pl":results[0][3], "pms":results[0][4], "pcid":results[0][5], "pname":results[0][6], "subs":subResults, "cases":sampleResults}))
    else:
        await uobj.ws.send(json.dumps({"func":"compError", "reason":"Problem could not be found"}))

#params -- cid, pid
async def submitProblem(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await inComp(params["cid"], uobj)) or not(await isDuringCompetition(params["cid"],uobj)):
        return
    sql = uobj.storage.sql

    # GROUPID IMPLEMENT
    await sql.execute("""INSERT INTO submissions (userid, groupid, submissiontime, programtype, programcode, competitionid, problemid, score, status, runlog) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                              (uobj.uid, uobj.groups[params["cid"]], int(time.time()), params["programtype"], params["programcode"], params["cid"], params["pid"], 0, 0, ""))
    uobj.storage.schedule_sdf()
    # GROUPID IMPLEMENT
    await sendToGroup(
        uobj.groups[params["cid"]],
        {"func":"submitProblem", "pid":params["pid"], "cid":params["cid"]},
        uobj.storage
    )

async def getScoreboard(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await inComp(params["cid"], uobj)):
        return
    sql = uobj.storage.sql

    temp_func = "getScoreboard"
    if "func" in params:
        temp_func = params["func"]

    tmp = await sql.execute("""
    SELECT groups.division
    FROM groups
    INNER JOIN participants
        ON participants.groupid = groups.id
    WHERE participants.userid = %s
        AND participants.competitionid = %s""", (params["uid"], params["cid"]))
    scoreboard_division = (await tmp.fetchall())[0][0]


    if temp_func == "getScoreboard":
        if not(await isDuringCompetition(params["cid"],uobj)) or not await isScoreboardAllowed(params["cid"], uobj):
            await uobj.ws.send(json.dumps({"func":"compError", "reason":"Scoreboard is not available at this time. Please wait for the awards ceremony."}))
            return
    elif await isAdmin(params["cid"], uobj):
        if "division" in params:
            scoreboard_division = params["division"]
        else:
            scoreboard_division = -1
    else:
        return
    # GROUPID IMPLEMENT
    #tmp = await sql.execute("""SELECT CAST(SUM(subquery.maxscore) AS UNSIGNED) as total, users.name, users.school FROM 
    #                                (SELECT MAX(score) as maxscore, groupid FROM submissions WHERE competitionid=%s GROUP BY problemid, groupid) as subquery
    #                                INNER JOIN participants ON participants.groupid=subquery.groupid
    #                                INNER JOIN users ON users.id=participants.userid WHERE participants.competitionid=%s
    #                                GROUP BY participants.userid ORDER BY total DESC LIMIT 10 """, [params["cid"], params["cid"]])
    
    get_best_scores = await sql.execute(
        """
        SELECT MAX(submissions.score), COUNT(*), submissions.groupid, submissions.problemid,
            (
                SELECT MIN(t.submissiontime)
                FROM submissions AS t
                WHERE t.problemid = submissions.problemid
                    AND t.groupid = submissions.groupid
                    AND t.score = MAX(submissions.score)
            )
        FROM submissions
        INNER JOIN groups
            ON groups.id = submissions.groupid
            AND groups.division=%s
        WHERE submissions.competitionid = %s
        GROUP BY submissions.groupid, submissions.problemid
        """,
        (scoreboard_division, params["cid"],)
    )
    best_scores = await get_best_scores.fetchall()
    get_users = await sql.execute(
        """
        SELECT users.name, participants.groupid
        FROM participants
        INNER JOIN users ON participants.userid = users.id
        INNER JOIN groups
            ON groups.id = participants.groupid
            AND groups.division=%s
        WHERE participants.competitionid = %s
        """,
        (scoreboard_division, params["cid"])
    )
    users = await get_users.fetchall()
    get_groups = await sql.execute(
        """
        SELECT groups.name, groups.id
        FROM groups
        WHERE groups.competitionid = %s AND groups.division = %s
        """,
        (params["cid"], scoreboard_division)
    )
    groups = await get_groups.fetchall()
    get_problems = await sql.execute(
        """
        SELECT problems.problemname, problems.problemnumber, problems.id, problems.maxscore
        FROM problems
        WHERE problems.competitionid = %s
        ORDER BY problems.problemnumber ASC
        """,
        (params["cid"])
    )
    problems = await get_problems.fetchall()

    get_divisions = await sql.execute(
        """
        SELECT divisions.id, divisions.name
        FROM divisions
        WHERE divisions.competitionid = %s
        """,
        (params["cid"])
    )
    divisions = ((-1, "Default",),)+ await get_divisions.fetchall()

    division = (-1, "Default")
    if scoreboard_division != -1 and scoreboard_division != "-1":
        division = (await (await sql.execute("""
        SELECT divisions.id, divisions.name
        FROM divisions
        WHERE divisions.id = %s
        """, (scoreboard_division))).fetchall())[0]
    await uobj.ws.send(json.dumps( {
        "division": division,
        "divisions": divisions,
        "func":temp_func,
        "best_scores": best_scores,
        "groups": groups,
        "problems": problems,
        "users": users} ))
async def getAllSubmissions(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await inComp(params["cid"], uobj)) or not(await isDuringCompetition(params["cid"],uobj)):
        return
    sql = uobj.storage.sql
    # GROUPID IMPLEMENT
    tmp = await sql.execute("""SELECT submissions.id, submissions.status, submissions.score, problems.problemnumber, problems.maxscore FROM submissions
                                    INNER JOIN problems ON submissions.problemid=problems.id 
                                    WHERE submissions.groupid=%s""", [uobj.groups[params["cid"]]])
    results = await tmp.fetchall()
    await uobj.ws.send(json.dumps ( {"func":"getAllSubmissions", "subs":results, "count":len(results)} ))

async def getPopUp(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await inComp(params["cid"], uobj)) or not(await compStatus(params["cid"], uobj) == CompetitionStatus.DURING):
        return
    sql = uobj.storage.sql
    tmp = await sql.execute("SELECT "+str(re.sub('[^a-zA-Z]','',params["get"]))+", problemid FROM submissions WHERE id=%s", [params["subid"]])
    results = await tmp.fetchall()
    if len(results) != 1:
        await uobj.ws.send(json.dumps( {"func":"compError", "reason":"Not just one submission with given id"} ))
    else:
        await uobj.ws.send(json.dumps( {"func":params["func"], "subid":params["subid"], "data":results[0][0], "type":params["get"], "pid":results[0][1]} ))
async def sendToGroup(gid, obj, storage):
    sql = storage.sql
    tmp = await sql.execute("""SELECT participants.userid FROM participants INNER JOIN groups ON participants.groupid=groups.id
                                    WHERE groups.id=%s""", [gid])
    results = await tmp.fetchall()
    for i in range(0, len(results)):
        await sendToUser(results[i][0], obj, storage)

async def sendToUser(uid, obj, storage):
    allCL = storage.all_cl 
    for uobj in allCL:
        if uobj.uid == int(uid):
            await uobj.ws.send(json.dumps(obj))

async def sendUsersInComp(obj, storage):
    sql = storage.sql
    compTmp = await sql.execute("SELECT type FROM competitions WHERE id=%s", [obj["cid"]])
    compResults = await compTmp.fetchall()
    tmp = None
    if compResults[0][0] == "prac":
        tmp = await sql.execute("SELECT id FROM users WHERE 1")
    else:
        tmp = await sql.execute("SELECT userid FROM participants WHERE competitionid=%s", [obj["cid"]])
    results = await tmp.fetchall()
    allCL = storage.all_cl
    for uobj in allCL:
        if uobj.uid in [row[0] for row in results]:
            await uobj.ws.send(json.dumps( obj ))


