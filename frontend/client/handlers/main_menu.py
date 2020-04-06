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
from ..utility import isLoggedIn
from .admin import loadAdmin
from ..utility import hashPassword

async def getMainMenuList(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)):
        return
    sql = uobj.storage.sql
    isSiteAdmin = (uobj.uid == 1)
    tmp = None
    if params["type"] == "prac":
        tmp = await sql.execute("""SELECT id, competitionname, short_desc, (SELECT COUNT(id) FROM problems WHERE problems.competitionid=competitions.id) AS total_problems, adminid
                                        FROm competitions WHERE type=%s""", ["prac"])
    else:
        tmp = await sql.execute("""SELECT competitions.id, competitions.competitionname, competitions.short_desc, (SELECT COUNT(id) FROM problems WHERE problems.competitionid=competitions.id) AS total_problems, competitions.adminid 
                                        FROM competitions INNER JOIN participants ON competitions.id=participants.competitionid
                                        WHERE type=%s AND userid=%s""", [params["type"], uobj.uid])
    _results = await tmp.fetchall()
    results = []
    for i in range(len(_results)):
        if _results[i][4] in uobj.groups.values():
            results.append(list(_results[i])+[True])
        else:
            results.append(list(_results[i])+[False])
    func = None
    if params["type"] == "prac":
        func = "getMainMenuPracticeList"
        tmp = await sql.execute("""SELECT competitions.id FROM competitions INNER JOIN participants ON competitions.id=participants.competitionid
                                        WHERE participants.userid=%s AND competitions.type=%s""", [uobj.uid, params["type"]])
        _results = await tmp.fetchall()
        cid_list = [row[0] for row in _results]
        for i in range(len(results)):
            if results[i][0] in cid_list:
                results[i].append(False)
            else:
                results[i].append(True)
    else:
        func = "getMainMenuCompeteList"
    await uobj.ws.send(json.dumps({"func":func, "total":len(results), "list":results, "isSiteAdmin":isSiteAdmin}))

async def getMainMenuSPS(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)):
        return

    sps = []
    for sp in uobj.storage.all_sp:
        sps.append(["SPS "+sp.spsName+" ("+str(sp.spid)+")", "- "+("Busy" if sp.busy else "Not Busy")])
    await uobj.ws.send(json.dumps({"func":"mainMenuSPS", "total":len(sps), "list":sps}))

async def createComp(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)):
        return

    sql = uobj.storage.sql

    if params["type"] == "prac" and uobj.uid != 1:
        await uobj.ws.send(json.dumps( {"func":"compError", "reason":"only admin can create new practice competitions"}))
        return

    status = 0
    if params["type"] == "prac":
        status = 1

# ------------------------------------------------------        ADMIN = GROUP ADMINID         ---------------------------------------------------------------
    tmp = await sql.execute("""INSERT INTO competitions (competitionname, type, short_desc, competitionstatus, adminid, duration, startTime, endTime, competitionkey)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                                    (params["name"], params["type"], params["short_desc"], status, uobj.uid, 0, 0, 0, bcrypt.hashpw(str(time.time()+random.randint(0,10000)).encode('utf-8'), bcrypt.gensalt())))
    lastrow = tmp.lastrowid
    # GROUPID IMPLEMENT
    groupTmp = await sql.execute("INSERT INTO groups (name, competitionid) VALUES (%s, %s)", ["Admin", lastrow])
    last_gid = groupTmp.lastrowid
    participantTmp = await sql.execute("INSERT INTO participants (competitionid, userid, spec, groupid) VALUES (%s, %s, %s, %s)",
                                             [lastrow, params["uid"], 1, last_gid])
    uobj.groups[lastrow] = last_gid
    await sql.execute("""UPDATE competitions
        SET competitions.adminid = %s
        WHERE competitions.id = %s
        """,
        (last_gid, lastrow)
    )

    await sql.execute("INSERT INTO levels (name, competitionid) VALUES (%s, %s)", ["Easy", lastrow])
    await sql.execute("INSERT INTO levels (name, competitionid) VALUES (%s, %s)", ["Medium", lastrow])
    await sql.execute("INSERT INTO levels (name, competitionid) VALUES (%s, %s)", ["Hard", lastrow])

    await loadAdmin({"uid":params["uid"], "cid":lastrow}, uobj)

async def forgotPassword(params, uobj):
    sql = uobj.storage.sql
    tmp = await sql.execute("SELECT email, name, password, id FROM users WHERE username=%s", [params["username"]])
    results = await tmp.fetchall()
    if len(results) != 1:
        await uobj.ws.send(json.dumps( {"func":"forgotPassword", "result":"bad"} ))
    else:
        encodedJWT = jwt.encode( {"id":results[0][3], "time":time.time()+3600000}, results[0][2], algorithm="HS256" ).decode('utf-8')
        await sql.execute("INSERT INTO tokens (token, timeout, username) VALUES (%s, %s, %s)",
                                [encodedJWT, (time.time() + 3600000), params["username"]])
        link = "https://mcsc.enrog.com/index.php?" + encodedJWT
        message = """<div style='width: 550px; height: 350px; text-align: center; background-color:rgb(245,245,245);'>
                         <div style='height: 50px; font-size: 30px; text-align: left; color:rgb(0,109,117); margin-left: 20px; font-weight: bold;'>MCSC</div>
                         <div style='width: 450px; height: 260px; text-align: center; background-color: white; margin-left: auto; margin-right: auto;'>
                             <div style='width: 350px; text-align: left; margin-left: auto; margin-right: auto; padding-top: 20px;padding-bottom:10px;'>
                             <div style='font-size: 20px; font-weight: bold;color:black;'>Reset Your Password</div>
                             <hr style='margin-top: 20px;' />
                             <div style='width: 350px; margin-top: 20px; font-size: 12px;'>It seems like you've forgotten your password. No worries;
                                  click on the link below to reset it. However, the link can only be used once, and will expire in an hour.</div>
                             <a style='text-align:center;display:block;text-decoration:none;width: 350px; padding: 10px; margin-top: 25px; background-color:rgb(0,109,117); color: white; font-size: 20px; cursor: pointer;' href='"""+link+"""'>
                                 Reset Your Password
                             </a>
                         </div>
                         <a style='font-size: 10px; padding-top: 30px;' href='https://mcsc.enrog.com'>Main Site</a></div>
                     </div>"""
        msg = MIMEText(message, "html")
        msg['Subject'] = "Reset Password"
        msg['From'] = "contact@enrog.com"
        msg['To'] = results[0][0]
        s = smtplib.SMTP('localhost')
        s.starttls()
        s.ehlo()
        s.sendmail("contact@enrog.com", results[0][0], msg.as_string())
        s.quit()

        await uobj.ws.send(json.dumps( {"func":"forgotPassword", "result":"good"}))

#https://pyjwt.readthedocs.io/en/latest/
async def resetPassword(params, uobj):
    sql = uobj.storage.sql
    if params["password1"] != params["password2"]:
        await uobj.ws.send(json.dumps( {"func":"resetPassword", "result":"badPassword"} ))
        return

    userTmp = await sql.execute("SELECT id, password FROM users WHERE username=%s", [params["username"]])
    userResults = await userTmp.fetchall()
    if len(userResults) != 1:
        await uobj.ws.send(json.dumps( {"func":"resetPassword", "result":"badUser"} ))
        return

    try:
        obj = jwt.decode(params["encodedJWT"], userResults[0][1], algorithms=["HS256"])
        if obj["id"] != userResults[0][0]:
            await uobj.ws.send(json.dumps( {"func":"resetPassword", "result":"badUser"} ))
            return
    except:
        await uobj.ws.send(json.dumps( {"func":"resetPassword", "result":"badUser"} ))
        return

    tokenTmp = await sql.execute("SELECT timeout, id FROM tokens WHERE username=%s AND token=%s", [params["username"], params["encodedJWT"]])
    tokenResults = await tokenTmp.fetchall()
    if len(tokenResults) != 1 or time.time() > tokenResults[0][0]:
        await uobj.ws.send(json.dumps( {"func":"resetPassword", "result":"timedOut"} ))
        return

    await sql.execute("UPDATE users SET password=%s WHERE id=%s", [await hashPassword(params["password1"]), obj["id"]])
    await sql.execute("DELETE FROM tokens WHERE id=%s", tokenResults[0][1])
    await uobj.ws.send(json.dumps( {"func":"resetPassword", "result":"good"} ))

async def joinComp(params, uobj):
    if not(await isLoggedIn(params["uid"], uobj)):
        return
    sql = uobj.storage.sql
    tmp = await sql.execute("SELECT type FROM competitions WHERE id=%s", [params["cid"]])
    res = await tmp.fetchall()
    if (len(res) != 1) or (res[0][0] == "comp"):
        await uobj.ws.send(json.dumps({"func":"compError","reason":"Comp doesn't exist or is not a practice competition."}))
        return

    tmp = await sql.execute("SELECT id FROM participants WHERE userid=%s AND competitionid=%s", [params["uid"], params["cid"]])
    res = await tmp.fetchall()
    if len(res) != 0:
        await uobj.ws.send(json.dumps({"func":"compError","reason":"Already in comp."}))
        return

    tmp = await sql.execute("INSERT INTO groups (name, competitionid) VALUES (%s, %s)", ["Single", params["cid"]])
    gid = tmp.lastrowid
    uobj.groups[params["cid"]] = gid
    await sql.execute("""
    UPDATE submissions
    SET groupid=%s
    WHERE submissions.competitionid=%s AND submissions.userid=%s
    """, [gid, params["cid"], uobj.uid])
    await sql.execute("INSERT INTO participants (competitionid, userid, spec, groupid) VALUES (%s, %s, %s, %s)", [params["cid"], uobj.uid, 0, gid])
    await getMainMenuList(params, uobj)