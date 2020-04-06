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

from ..utility import hashPassword

async def login(uobj, params):
    sql = uobj.storage.sql
    tmp = await sql.execute("SELECT id, password, lastvisited FROM users WHERE username=%s",(params["username"]))
    results = await tmp.fetchall()
    if len(results) != 1:
        await uobj.ws.send(json.dumps({"func":"login", "result":"bad", "reason":""}))
    else:
        if bcrypt.checkpw(params["password"].encode('utf-8'), results[0][1].encode('utf-8')):
            tmp = await sql.execute("""SELECT competitions.id, participants.groupid FROM competitions
                                            INNER JOIN participants ON participants.competitionid=competitions.id
                                            WHERE participants.userid=%s""", results[0][0])
            res = await tmp.fetchall()
            for i in range(0, len(res)):
                if res[i][0] in uobj.groups:
                    await uobj.ws.send(json.dumps({"func":"compError", "reason":"Multiple groups for same competition???"}))
                    return
                uobj.groups[res[i][0]] = res[i][1]
            uobj.username = params["username"]
            uobj.uid = results[0][0]
            uobj.curpath = results[0][2]
            uobj.loggedIn = True
            reloadToken = jwt.encode({"username":params["username"], "time":time.time()+3600000}, results[0][1], algorithm="HS256" ).decode('utf-8')
            await sql.execute("UPDATE users SET reloadtoken=%s WHERE id=%s", [reloadToken, results[0][0]])
            await uobj.ws.send(json.dumps({"func":"login", "result":"good", "username":params["username"], "uid":results[0][0], "reloadToken":reloadToken}))
        else:
            await uobj.ws.send(json.dumps({"func":"login", "result":"bad", "reason":""}))

async def reloadLogin(params, uobj):
    sql = uobj.storage.sql
    tmp = await sql.execute("SELECT id, username, password, lastvisited FROM users WHERE reloadtoken=%s", [params["reloadToken"]])
    results = await tmp.fetchall()
    if len(results) != 1:
        await uobj.ws.send(json.dumps({"func":"login", "result":"bad", "reason":"token not found"}))
    else:
        obj = jwt.decode(params["reloadToken"], results[0][2], algorithms=["HS256"])
        if (obj["username"] == results[0][1]) and (time.time() < obj["time"]):
            tmp = await sql.execute("""SELECT competitions.id, participants.groupid FROM competitions
                                            INNER JOIN participants ON participants.competitionid=competitions.id
                                            WHERE participants.userid=%s""", results[0][0])
            res = await tmp.fetchall()
            for i in range(0, len(res)):
                if res[i][0] in uobj.groups:
                    await uobj.ws.send(json.dumps({"func":"compError", "reason":"Multiple groups for same competition???"}))
                    return
                uobj.groups[res[i][0]] = res[i][1]
            uobj.loggedIn = True
            uobj.username = results[0][1]
            uobj.uid = results[0][0]
            reloadToken = jwt.encode({"username":results[0][1], "time":time.time()+3600000}, results[0][2], algorithm="HS256" ).decode('utf-8')
            await sql.execute("UPDATE users SET reloadtoken=%s WHERE id=%s", [reloadToken, results[0][0]])
            await uobj.ws.send(json.dumps({"func":"login", "result":"good", "username":results[0][1], "uid":results[0][0], "reloadToken":reloadToken}))
        else:
            await uobj.ws.send(json.dumps({"func":"login", "result":"bad", "reason":"token expired"}))

async def signup(params, uobj):
    sql = uobj.storage.sql
    tmp = await sql.execute("SELECT id FROM users WHERE username=%s", (params["username"]))
    results = await tmp.fetchall()
    if len(results) == 0:
        userTmp = await sql.execute("""INSERT INTO users (username, password, name, school, lastvisited, email, reloadtoken)
                                  VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                                  (params["username"], await hashPassword(params["password"]), params["name"], params["school"], "main:0", params["email"], ""))
        await login(uobj, params)
    else:
        await uobj.ws.send(json.dumps( {"func":"signup"} ))
