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

from ..utility import isAdmin
from .competition import sendUsersInComp


async def sendCompStatus(cid, uobj):
    """Broadcasts the competition status to all competitors.

    Args:
        cid: Competition ID to distribute the status of
        uobj: (Generally) the UserObject of the admin who
            requested the competition status broadcast
    """
    if not (await isAdmin(cid, uobj)):
        return
    sql = uobj.storage.sql

    tmp = await sql.execute("""
        SELECT automatic, competitionstatus, startTime, endTime FROM competitions
        WHERE id=%s
    """, [cid])
    tmp = await tmp.fetchone()

    automatic = tmp[0]
    status = tmp[1]
    startTime = tmp[2]
    endTime = tmp[3]

    curTime = int(time.time() * 1000)

    await sendUsersInComp(
        {
            "func": "compstatus",
            "current_time": curTime,
            "cid": cid,
            "status": status,
            "automatic": automatic,
            "startTime": startTime,
            "endTime": endTime
        },
        uobj.storage
    )
