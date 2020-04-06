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

from ..utility import isLoggedIn, isAdmin, isAdminOfProblem, compStatus
from .general import sendCompStatus
from .competition import sendUsersInComp

async def adminProblems(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    probTmp = await sql.execute("""SELECT level, problemname, id, problemnumber, maxscore FROM problems
                                        WHERE competitionid=%s ORDER BY problemnumber""", (params["cid"]))
    probResults = await probTmp.fetchall()

    await uobj.ws.send(json.dumps({"func":"adminProblems", "probs":probResults}))

#params -- cid
async def adminCompetitors(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    # GROUPID IMPLEMENT
    typeTmp = await sql.execute("SELECT type FROM competitions WHERE id=%s", [params["cid"]])
    typeResult = await typeTmp.fetchall()

    groupTmp = await sql.execute("SELECT id, name FROM groups WHERE competitionid=%s AND name!=%s AND name!=%s", [params["cid"], "Admin", "Single"])
    groupResults = await groupTmp.fetchall()

    compTmp = await sql.execute("""SELECT users.name, users.school, users.id, groups.id, groups.name FROM users
                                        INNER JOIN participants ON participants.userid=users.id
                                        INNER JOIN competitions ON competitions.id=participants.competitionid
                                        INNER JOIN groups ON participants.groupid=groups.id AND groups.competitionid=participants.competitionid
                                        WHERE participants.competitionid=%s AND users.id!=%s ORDER BY users.name""", (params["cid"], uobj.uid))
    compResults = await compTmp.fetchall()
    userResults = []
    uid_list = [user.uid for user in uobj.storage.all_cl]
    for i in range(len(compResults)):
        if compResults[i][3] in uid_list:
            userResults.append(list(compResults[i])+[True])
        else:
            userResults.append(list(compResults[i])+[False])
    await uobj.ws.send(json.dumps({"func":"adminCompetitors", "comps":userResults, "type":typeResult[0][0], "groups":groupResults}))

async def loadAdmin(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    tmp = await sql.execute("SELECT competitionname, competitionstatus, duration, type, adminid, startTime, endTime, short_desc, competitionkey, automatic FROM competitions WHERE id=%s", (params["cid"]))
    results = await tmp.fetchone()

    current_time = int(time.time() * 1000)
    await uobj.ws.send(json.dumps({"func":"loadAdmin", "current_time":current_time, "name":results[0], "status":results[1], "duration":results[2], "type":results[3], "adminid":results[4], "cid":params["cid"], "startTime":results[5], "endTime":results[6], "short_desc":results[7], "competitionkey":results[8], "automatic":results[9]}))

async def getAdminProblem(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return 
    sql = uobj.storage.sql
    tmp = await sql.execute("SELECT competitionid, problemtext, problemname, memorylimit, runtimelimit, level FROM problems WHERE id=%s",[params["pid"]])
    results = await tmp.fetchall()
    if len(results)!=1:
        await uobj.ws.send(json.dumps({"func":"compError", "reason":"Bad PID"}))
        return
    prob = results[0]
    if not await isAdmin(prob[0], uobj):
        await uobj.ws.send(json.dumps({"func":"compError", "reason":"Bad permissions"}))
        return

    tmp = await sql.execute("SELECT id, value, input FROM cases WHERE problemid = %s", [params["pid"]])
    _cases = await tmp.fetchall()
    cases = []
    for c in _cases:
        cases.append(list(c[0:-1]) + [c[-1] if len(c[-1]) <= 20 else c[-1][0:20]])
    
    tmp = await sql.execute("SELECT id, filename FROM images WHERE problemid=%s AND competitionid=%s", [params["pid"], params["cid"]])
    images = await tmp.fetchall()

    tmp = await sql.execute("SELECT name FROM levels WHERE competitionid=%s", [params["cid"]])
    levels = await tmp.fetchall()

    await uobj.ws.send(json.dumps({"func":"getAdminProblem", "pid":params["pid"], "problemtext":prob[1], "memorylimit":prob[3], 
                                "runtimelimit":prob[4], "cases":cases, "problemname":prob[2], "images":images, "level":prob[5], "levels":levels}))
async def editComp(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    tmp = await sql.execute("SELECT type, competitionstatus FROM competitions WHERE id=%s", [params["cid"]])
    results = await tmp.fetchall()
    if len(results) != 1:
        await uobj.ws.send(json.dumps( {"func":"compError", "reason":"not only one competition found in editComp"}))
        return
        
    await sql.execute("UPDATE competitions SET competitionname=%s, short_desc=%s WHERE id=%s",
                            (params["name"], params["short_desc"], params["cid"]))

#params -- cid, username
async def addCompetitor(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    userTmp = await sql.execute("SELECT id FROM users WHERE username=%s", [params["username"]])
    userResults = await userTmp.fetchall()
    if len(userResults) == 0:
        await uobj.ws.send(json.dumps( {"func":"addCompetitor", "reason":"User not found. Please inform the prospective competitor must sign up on our site before entering."} ))
    elif len(userResults) == 1:
        participantTmp = await sql.execute("SELECT id FROM participants WHERE userid=%s AND competitionid=%s", [userResults[0][0], params["cid"]])
        participantsResults = await participantTmp.fetchall()
        if len(participantsResults) != 0:
            await uobj.ws.send(json.dumps( {"func":"addCompetitor", "reason":"User already is in the competition."} ))
            return
        # GROUPID IMPLEMENT
        groupid = None
        if params["gid"] == -1:
            tmp = await sql.execute("INSERT INTO groups (name, competitionid) VALUES (%s, %s)", ["Single", params["cid"]])
            groupid = tmp.lastrowid
        else:
            groupid = params["gid"]
        await sql.execute("INSERT INTO participants (competitionid, userid, spec, groupid) VALUES (%s, %s, %s, %s)",
                                [params["cid"], userResults[0][0], 0, groupid])
        for obj in uobj.storage.all_cl:
            if obj.uid == userResults[0][0]:
                obj.groups[params["cid"]] = groupid
                
        await adminCompetitors(params, uobj)
    else:
        await uobj.ws.send(json.dumps( {"func":"addCompetitor", "reason":"Please contact administrators about this issue."} ))

async def editCompetitor(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    gid = None
    if params["new_gid"] == params["old_gid"]:
        raise RuntimeError("bruh")
    tmp = await sql.execute("SELECT name FROM groups WHERE id=%s", [params["old_gid"]])
    res = await tmp.fetchall()
    if res[0][0] == "Single":
        await sql.execute("DELETE FROM groups WHERE id=%s", [params["old_gid"]])
    if params["new_gid"] == -1:
        tmp = await sql.execute("INSERT INTO groups (name, competitionid) VALUES (%s, %s)", ["Single", params["cid"]])
        gid = tmp.lastrowid
    else:
        gid = params["new_gid"]
    await sql.execute("UPDATE participants SET groupid=%s WHERE userid=%s AND competitionid=%s", [gid, params["e_uid"], params["cid"]])
    await sql.execute("UPDATE submissions SET groupid=%s WHERE userid=%s AND competitionid=%s", [gid, params["e_uid"], params["cid"]])
    for obj in uobj.storage.all_cl:
        if obj.uid == params["e_uid"]:
            obj.groups[params["cid"]] = gid
    await adminCompetitors(params, uobj)

#params -- cid, ruid
async def removeCompetitor(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    if params["ruid"] == uobj.uid:
        return
        
    if params["cid"] not in uobj.groups:
        await uobj.ws.send(json.dumps( {"func":"compError", "reason":"user not in a group in removeCompetitor"}))
        return
    tmp = await sql.execute("""
    SELECT groups.id
    FROM groups
    INNER JOIN participants
        ON participants.groupid = groups.id
            AND participants.userid = %s
            AND participants.competitionid = %s""",
        [params["uid"], params["cid"]])
    gid = (await tmp.fetchall())[0][0]
    # GROUPID IMPLEMENT
    tmp = await sql.execute("SELECT name FROM groups WHERE id=%s", [gid])
    results = await tmp.fetchall()

    if results[0][0] == "Single":
        await sql.execute("DELETE FROM groups WHERE id=%s", [gid])

    await sql.execute("DELETE FROM participants WHERE userid=%s AND competitionid=%s", [params["ruid"], params["cid"]])
    for obj in uobj.storage.all_cl:
        if obj.uid == params["ruid"]:
            del obj.groups[params["cid"]]

    await adminCompetitors(params, uobj)



async def adminSetCompStatus(params, uobj):
    if not (await isLoggedIn(params["uid"], uobj) and await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    compStatus = params["status"]

    if compStatus < 0:
        compStatus = 0
    elif compStatus > 2:
        compStatus = 2
    
    await sql.execute("UPDATE competitions SET competitionstatus=%s, automatic=0 WHERE id=%s", [compStatus, params["cid"]])
    await sendCompStatus(params["cid"], uobj)

async def adminSetAutomaticCompetitionStatus(params, uobj):
    if not (await isLoggedIn(params["uid"], uobj) and await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    delay = max(0, int(float(params["delay"])))*60*1000
    duration = max(0, int(float(params["duration"])))*60*1000

    startTime = time.time()*1000 + delay
    endTime = startTime + duration
    
    await sql.execute("UPDATE competitions SET startTime=%s, endTime=%s, automatic=1 WHERE id=%s", [startTime, endTime, params["cid"]])
    await sendCompStatus(params["cid"], uobj)

async def adminSetScoreboard(params, uobj):
    if not (await isLoggedIn(params["uid"], uobj) and await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    scoreboardvisible = params["scoreboardvisible"]
    
    await sql.execute("UPDATE competitions SET scoreboardvisible=%s WHERE id=%s", [scoreboardvisible, params["cid"]])


#params -- cid
async def adminControlPanel(params, uobj):
    if not (await isLoggedIn(params["uid"], uobj) and await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    cid = params["cid"]
    tmp = await sql.execute("SELECT automatic, competitionstatus, startTime, endTime, scoreboardvisible FROM competitions WHERE id=%s", [cid])
    tmp = await tmp.fetchone()

    automatic = tmp[0]
    status = tmp[1]
    startTime = tmp[2]
    endTime = tmp[3]
    scoreboardvisible = tmp[4]

    await uobj.ws.send(json.dumps({"func":"adminControlPanel", "status":status, "automatic":automatic, "startTime":startTime, "endTime":endTime, "scoreboardvisible": scoreboardvisible}))

### End Competition Timer & Status ###

#params -- cid
async def adminSubmissions(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    tmp = await sql.execute("""SELECT submissions.id, submissions.status, submissions.score, problems.problemnumber, problems.maxscore FROM submissions
                                    INNER JOIN problems WHERE submissions.problemid=problems.id AND 
                                    submissions.competitionid=%s ORDER BY submissions.id ASC""", [params["cid"]])
    results = await tmp.fetchall()
    await uobj.ws.send(json.dumps ( {"func":"getAdminSubmissions", "subs":results, "count":len(results)} ))
    
async def adminGetCase(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql

    tmp = await sql.execute("SELECT input, expected, value FROM cases WHERE competitionid=%s AND problemid=%s AND id=%s", [params["cid"], params["pid"], params["caseid"]])
    results = await tmp.fetchall()
    if len(results) != 1:
        await uobj.ws.send(json.dumps( {"func":"adminGetCase", "result":"bad"} ))
    else:
        await uobj.ws.send(json.dumps( {"func":"adminGetCase", "result":"good", "input":results[0][0], "output":results[0][1], "value":results[0][2], "caseid":params["caseid"]} ))

async def sendSaveQuestion(obj, uobj):
    sql = uobj.storage.sql
    tmp = await sql.execute("SELECT problemtext, problemname, runtimelimit, memorylimit, competitionid FROM problems WHERE id=%s", [obj["pid"]])
    results = await tmp.fetchall()
    if len(results) != 1:
        await uobj.ws.send({"func":"compError", "reason":"not exactly one comp in sendSaveQuestion"})
    else:
        await sendUsersInComp(
            {
                "func":"adminSaveQuestion",
                "question":results[0][0],
                "problemname":results[0][1],
                "runtimeLimit":results[0][2],
                "memoryLimit": results[0][3],
                "cid":results[0][4],
                "pid":obj["pid"]
            },
            uobj.storage
        )

async def adminSaveQuestion(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj))  or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    runtimeLimit = int(params["runtime"])
    memoryLimit = int(params["memory"])
    if runtimeLimit < 1:
        runtimeLimit = 1
    elif runtimeLimit > 30:
        runtimeLimit = 30
    if memoryLimit < 50:
        memoryLimit = 50
    elif memoryLimit > 400:
        memoryLimit = 400
    await sql.execute("UPDATE problems SET problemtext=%s, problemname=%s, runtimelimit=%s, memorylimit=%s, level=%s WHERE id=%s", [params["question"], params["problemname"], runtimeLimit, memoryLimit, params["level"], params["pid"]])
    await sendSaveQuestion({"pid":params["pid"]}, uobj)

async def adminRegradeProblemSubmissions(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj))  or not(await isAdminOfProblem(params["pid"], uobj)):
        return
    sql = uobj.storage.sql
    await sql.execute("UPDATE submissions SET status=0 WHERE problemid=%s", [params["pid"]])

async def adminSaveCase(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql

    await sql.execute("UPDATE problems SET lastupdated=%s WHERE id=%s", [time.time(), params["pid"]])
    await sql.execute("UPDATE cases SET input=%s, expected=%s, value=%s WHERE id=%s AND problemid=%s AND competitionid=%s",
                            [params["input"], params["output"], params["value"], params["caseid"], params["pid"], params["cid"]])
    await adminUpdateMaxscore(params["pid"], params["cid"], sql)
    await uobj.ws.send(json.dumps( {"func":"adminSaveCaseCallback" } ))

async def adminUpdateMaxscore(pid, cid, sql):
    tmp = await sql.execute("SELECT SUM(value) FROM cases WHERE problemid=%s AND competitionid=%s AND NOT value=%s", [pid, cid, -1])
    results = await tmp.fetchall()
    if results[0][0] == None:
        await sql.execute("UPDATE problems SET maxscore=%s WHERE id=%s AND competitionid=%s", [0, pid, cid])
    else:
        await sql.execute("UPDATE problems SET maxscore=%s WHERE id=%s AND competitionid=%s", [results[0][0], pid, cid])

async def adminRemoveCase(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql

    await sql.execute("DELETE FROM cases WHERE id=%s AND competitionid=%s", [params["caseid"], params["cid"]])
    await adminUpdateMaxscore(params["pid"], params["cid"], sql)
    await getAdminProblem(params, uobj)

async def adminRemoveProblem(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql

    await sql.execute("DELETE FROM problems WHERE id=%s AND competitionid=%s", [params["pid"], params["cid"]])
    await adminProblems(params, uobj)

async def adminAddCase(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    
    await sql.execute("INSERT INTO cases (problemid, competitionid, input, expected, value) VALUES (%s, %s, %s, %s, %s)",
                           [params["pid"], params["cid"], "", "", 0])
    await adminUpdateMaxscore(params["pid"], params["cid"], sql)
    await getAdminProblem(params, uobj)

async def adminCustomRun(params, uobj):
    sql = uobj.storage.sql
    sid = int(params["sid"])
    if sid < 0:
        return
    tmp = await sql.execute("SELECT competitionid, programtype, programcode, problemid,groupid FROM submissions WHERE id=%s",[sid])
    tmp = await tmp.fetchall()

    if len(tmp)!=1:
        return

    if not (await isLoggedIn(params["uid"], uobj) and await isAdmin(tmp[0][0], uobj)):
        return

    await sql.execute("INSERT INTO submissions (competitionid, programtype, programcode, problemid, customrunoriginal, userid,runlog,submissiontime,groupid) VALUES (%s,%s,%s,%s,%s,%s,'',%s,%s)",
    [tmp[0][0],tmp[0][1],tmp[0][2],tmp[0][3],sid,uobj.uid,int(time.time()),tmp[0][4]])
    uobj.storage.schedule_sdf()

async def adminAddProblem(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql

    tmp = await sql.execute("SELECT MAX(problemnumber) FROM problems WHERE competitionid=%s", [params["cid"]])
    results = await tmp.fetchall()
    pnum = results[0][0]
    if pnum == None:
        pnum = 0
    await sql.execute("""INSERT INTO problems (problemnumber, problemtext, level, maxscore, competitionid, problemname, lastupdated) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s)""", [pnum+1, "", "easy", 0, params["cid"], "", time.time()])
    await adminProblems(params, uobj)

async def adminAddImage(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql

    #https://stackoverflow.com/questions/2323128/convert-string-in-base64-to-image-and-save-on-filesystem-in-python
    #https://stackoverflow.com/questions/26070547/decoding-base64-from-post-to-use-in-pil/26085215
    
    allowed_set = ["jpg", "jpeg", "png", "gif"]
    extension = params["data"].split(";")[0].split("/")[1]
    data = params["data"].split("base64,")[1]

    if extension not in allowed_set:
        await uobj.ws.send({"func":"adminAddImage", "result":"bad"})
        return

    tmp = await sql.execute("SELECT AUTO_INCREMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s AND TABLE_NAME=%s", ["mcst", "images"])
    results = await tmp.fetchall()

    filename = "image_" + str(results[0][0])
    path = "/var/mcsc/imgs/"
 
    image = Image.open(BytesIO(base64.b64decode(data)))
    image.save(path+filename+"_large."+extension)
    image.thumbnail((200, 200))
    image.save(path+filename+"_small."+extension)

    await sql.execute("""INSERT INTO images (filename, fileextension, problemid, competitionid)
                              VALUES (%s, %s, %s, %s)""",
                              (filename, extension, params["pid"], params["cid"]))

    await uobj.ws.send(json.dumps({"func":"adminAddImage", "result":"good", "id":results[0][0], "filename":filename}))

async def adminRemoveImage(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql

    tmp = await sql.execute("SELECT filename, fileextension FROM images WHERE id=%s AND problemid=%s AND competitionid=%s", [params["id"], params["pid"], params["cid"]])
    results = await tmp.fetchall()
    if len(results) != 1:
        await uobj.ws.send(json.dumps({"func":"adminRemoveImage", "result":"bad", "reason":"not only one result queried"}))
        return

    largePath = "/var/mcsc/imgs/" + results[0][0] + "_large." + results[0][1]
    smallPath = "/var/mcsc/imgs/" + results[0][0] + "_small." + results[0][1]
    if not os.path.exists(largePath) or not os.path.exists(smallPath):
        await uobj.ws.send(json.dumps({"func":"adminRemoveImage", "result":"bad", "reason":"file doesn't exist???"}))
        return
    
    os.remove(largePath)
    os.remove(smallPath)
    await sql.execute("DELETE FROM images WHERE id=%s AND problemid=%s AND competitionid=%s", [params["id"], params["pid"], params["cid"]])

    await uobj.ws.send(json.dumps({"func":"adminRemoveImage", "result":"good", "id":params["id"]}))

async def adminAddLevel(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql

    tmp = await sql.execute("SELECT id FROM levels WHERE competitionid=%s AND name=%s", [params["cid"], params["name"]])
    results = await tmp.fetchall()
    if len(results) != 0:
        await uobj.ws.send(json.dumps( {"func":"compError", "result":"bad", "reason":"Level with the same name already exists."} ))
    else:
        await sql.execute("INSERT INTO levels (name, competitionid) VALUES (%s, %s)", 
                                [params["name"], params["cid"]])
        await adminLevels(params, uobj)

async def adminSaveLevel(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql

    tmp = await sql.execute("SELECT id FROM levels WHERE competitionid=%s AND name=%s AND id<>%s", [params["cid"], params["name"], params["lid"]])
    results = await tmp.fetchall()
    if len(results) != 0:
        await uobj.ws.send(json.dumps( {"func":"compError", "result":"bad", "reason":"Level with the same name already exists."} ))
    else:
        await sql.execute("UPDATE levels SET name=%s WHERE competitionid=%s AND id=%s", 
                                [params["name"], params["cid"], params["lid"]])
        await adminLevels(params, uobj)
    
async def adminDeleteLevel(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql

    tmp = await sql.execute("SELECT name FROM levels WHERE competitionid=%s AND id<>%s LIMIT 1", [params["cid"], params["lid"]])
    results = await tmp.fetchall()
    if len(results) == 0:
        await uobj.ws.send(json.dumps( {"func":"compError", "result":"bad", "reason":"There must be at least one level."} ))
    elif len(results) > 1:
        await uobj.ws.send(json.dumps( {"func":"compError", "result":"bad", "reason":"Very bad, please contact admin."} ))
    else:
        await sql.execute("UPDATE problems SET level=%s WHERE competitionid=%s AND id=%s", [results[0][0], params["cid"], params["lid"]])
        await sql.execute("DELETE FROM levels WHERE competitionid=%s AND id=%s", [params["cid"], params["lid"]])
        await adminLevels(params, uobj)

#params -- cid
async def adminLevels(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql

    tmp = await sql.execute("SELECT id, name FROM levels WHERE competitionid=%s", [params["cid"]])
    results = await tmp.fetchall()
    await uobj.ws.send(json.dumps( {"func":"adminLevels", "levels":results} ))

async def moveProblem(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql

    if params["from_pid"] == params["to_pid"]:
        return

    fromTmp = await sql.execute("SELECT problemnumber FROM problems WHERE id=%s", [params["from_pid"]])
    fromResults = await fromTmp.fetchall()

    toTmp = await sql.execute("SELECT problemnumber FROM problems WHERE id=%s", [params["to_pid"]])
    toResults = await toTmp.fetchall()

    if len(fromResults) != 1 or len(toResults) != 1:
        await uobj.ws.send(json.dumps( {"func":"compError", "result":"bad", "reason":"More than one problem found in moveProblem"} ))
        return
    if fromResults[0][0] < toResults[0][0]:
        await sql.execute("""UPDATE problems SET problemnumber=problemnumber-1 WHERE id IN
                                  (SELECT id FROM (SELECT id, problemnumber FROM problems) AS tmp WHERE problemnumber>%s AND problemnumber<=%s AND competitionid=%s)""",
                                  [fromResults[0][0], toResults[0][0], params["cid"]])
        await sql.execute("UPDATE problems SET problemnumber=%s WHERE id=%s", [toResults[0][0], params["from_pid"]])
        await adminProblems(params, uobj)
    elif fromResults[0][0] > toResults[0][0]:
        await sql.execute("""UPDATE problems SET problemnumber=problemnumber+1 WHERE id IN
                                  (SELECT id FROM (SELECT id, problemnumber FROM problems) AS tmp WHERE problemnumber<%s AND problemnumber>=%s AND competitionid=%s)""",
                                  [fromResults[0][0], toResults[0][0], params["cid"]])
        await sql.execute("UPDATE problems SET problemnumber=%s WHERE id=%s", [toResults[0][0], params["from_pid"]])
        await adminProblems(params, uobj)
    else: 
        await uobj.ws.send(json.dumps( {"func":"compError", "result":"bad", "reason":"same problemnumber, different pid"} ))
        return   

    if await compStatus(params["cid"], uobj) == 1:
        await sendUsersInComp(
            {
                "func":"moveProblem",
                "cid":params["cid"],
                "pnum":toResults[0][0]
            },
            uobj.storage
        )

async def adminCompetitorInfo(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    print("IN ADMIN COMPETITOR INFO: ", params)
    userTmp = await sql.execute("SELECT username FROM users WHERE id=%s", [params["uid"]])
    userResults = await userTmp.fetchall()

    probTmp = await sql.execute("""SELECT problemnumber, level, maxscore, problemname, id FROM problems
                                        WHERE competitionid=%s ORDER BY problemnumber""", [params["cid"]])
    probResults = await probTmp.fetchall()

# GROUPID IMPLEMENT
    subTmp = await sql.execute("""SELECT MAX(submissions.score), submissions.problemid, COUNT(submissions.id) FROM submissions 
                                       INNER JOIN participants ON participants.groupid=submissions.groupid
                                       WHERE participants.competitionid=%s AND participants.userid=%s 
                                       GROUP BY submissions.problemid""", [params["cid"], params["uid"]])
    subResults = await subTmp.fetchall()

    lvlTmp = await sql.execute("SELECT name FROM levels WHERE competitionid=%s", [params["cid"]])
    lvlResults = await lvlTmp.fetchall()

    await uobj.ws.send(json.dumps( {"func":"adminCompetitorInfo", "user":userResults, "probs":probResults, "subs":subResults, "levels":lvlResults} ))


# GROUPID IMPLEMENT
async def adminGroups(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    tmp = await sql.execute("""SELECT DISTINCT groups.id, groups.name, groups.division, users.name
    FROM groups
    LEFT JOIN participants ON groups.id = participants.groupid
    LEFT JOIN users ON participants.userid = users.id
    WHERE groups.competitionid=%s
    """, [params["cid"]])
    res = await tmp.fetchall()
    tmp = await sql.execute("SELECT id, name FROM divisions WHERE competitionid=%s", [params["cid"]])
    divs = await tmp.fetchall()

    divs = ((-1, "Default"),)+divs
    
    await uobj.ws.send(json.dumps( {"func":"adminGroups", "groups":res, "divisions":divs} ))

async def adminAddGroup(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    if params["name"] == "Admin":
        await uobj.ws.send(json.dumps({"func":"compError", "reason":"Group cannot be named Admin."}))
        return
    await sql.execute("INSERT INTO groups (name, competitionid) VALUES (%s, %s)", [params["name"], params["cid"]])
    await adminGroups(params, uobj)

async def adminSaveGroup(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    tmp = await sql.execute("SELECT id FROM groups WHERE name=%s AND competitionid=%s AND id!=%s", [params["name"], params["cid"], params["gid"]])
    res = await tmp.fetchall()
    if len(res) > 0 and params["name"] != "Single":
        await uobj.ws.send(json.dumps({"func":"compError", "reason":"A group with the same name already exists."}))
        return
    if params["name"] == "Admin":
        await uobj.ws.send(json.dumps({"func":"compError", "reason":"Group cannot be named Admin."}))
        return
    tmp = await sql.execute("SELECT name FROM groups WHERE id=%s AND competitionid=%s", [params["gid"], params["cid"]])
    res = await tmp.fetchall()
    if len(res) != 1:
        await uobj.ws.send(json.dumps({"func":"compError", "reason":"Group doesn't exist in this competition."}))
        return
    await sql.execute("UPDATE groups SET name=%s, division=%s WHERE id=%s", [params["name"], params["division"], params["gid"]])
    await adminGroups(params, uobj)

async def adminDeleteGroup(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)) or not(await isAdmin(params["cid"], uobj)):
        return
    sql = uobj.storage.sql
    tmp = await sql.execute("""
    SELECT groups.competitionid
    FROM groups
    WHERE groups.id = %s
    """
    , params["gid"])
    tmp = await tmp.fetchall()
    if len(tmp) == 0:
        await uobj.ws.send(json.dumps({"func":"compError", "reason":"35324"}))
        return
    elif tmp[0][0] != params["cid"]:
        await uobj.ws.send(json.dumps({"func":"compError", "reason":"t435324"}))
        return
        
    tmp = await sql.execute("SELECT userid FROM participants WHERE groupid=%s", [params["gid"]])
    res = await tmp.fetchall()
    for i in range(0, len(res)):
        tmp = await sql.execute("INSERT INTO groups (name, competitionid) VALUES (%s, %s)", ["Single", params["cid"]])
        gid = tmp.lastrowid
        await sql.execute("UPDATE participants SET groupid=%s WHERE userid=%s AND competitionid=%s", [gid, res[i][0], params["cid"]])
        await sql.execute("UPDATE submissions SET groupid=%s WHERE userid=%s AND competitionid=%s", [gid, res[i][0], params["cid"]])
        for obj in uobj.storage.all_cl:
            if obj.uid == res[i][0]:
                obj.groups[params["cid"]] = gid

    await sql.execute("DELETE FROM groups WHERE id=%s", [params["gid"]])
    await adminGroups(params, uobj)

