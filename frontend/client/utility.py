import json
import time
import bcrypt
from enum import Enum


class CompetitionStatus(Enum):
    BEFORE = 0
    DURING = 1
    AFTER = 2


async def isAdmin(cid, uobj):
    """Check if a user is an admin of a competition.

    Args:
        cid: Competition ID to check against
        uobj: User object to check

    Returns:
        True if the user is an admin of the competition, False if not.
    """
    tmp = await uobj.storage.sql.execute("""
        SELECT 1 FROM participants
        INNER JOIN competitions ON competitions.adminid=participants.groupid
        WHERE competitions.id=%s AND participants.competitionid=%s AND participants.userid=%s
    """, [cid, cid, uobj.uid])
    res = await tmp.fetchall()
    if len(res) == 0:
        await uobj.ws.send(json.dumps(
            {
                "func": "compError",
                "reason": "Permissions Error"
            }
        ))
        return False
    elif len(res) == 1:
        return True
    else:
        await uobj.ws.send(json.dumps({
            "func": "compError",
            "reason": "Permissions Error"
        }))
        return False


async def isAdminOfProblem(pid, uobj):
    """Check if a user is an admin of the competition that a problem is a part of.

    Args:
        pid: Problem ID (to get the competition from)
        uobj: User object to check

    Returns:
        True if the user is an admin of the problem, False if not.
    """
    tmp = await uobj.storage.sql.execute("SELECT competitionid FROM problems WHERE id=%s", [pid])
    res = await tmp.fetchall()
    if len(res) != 1:
        await uobj.ws.send(json.dumps({
            "func": "compError",
            "reason": "Permissions Error"
        }))
        return False
    return await isAdmin(res[0][0], uobj)


async def isLoggedIn(passedUID, uobj):
    """Check if a user is logged in completely.

    Args:
        passedUID: Claimed user ID by the client
        uobj: Actual user object representing the client

    Returns:
        True if the user is logged in, False if not.
    """
    passedUID = int(passedUID)
    if passedUID == uobj.uid and passedUID != -1 and uobj.loggedIn:
        return True
    await uobj.ws.send(json.dumps({"func": "NL"}))
    return False


async def inComp(cid, uobj):
    """Checks if a user is in a competition.

    Args:
        cid: Competition ID to check against
        uobj: User to check

    Returns:
        True if the user is in the competition, False if not.
    """
    sql = uobj.storage.sql
    compTmp = await sql.execute("SELECT type FROM competitions WHERE id=%s", [cid])
    compResults = await compTmp.fetchall()
    if len(compResults) == 0:
        await uobj.ws.send(json.dumps({
            "func": "compError",
            "reason": "this competition doesn't exist..."
        }))
        return False
    elif len(compResults) > 1:
        await uobj.ws.send(json.dumps({
            "func": "compError",
            "reason": "how is there more than one comp with id=" + cid
        }))
        return False
    else:
        if compResults[0][0] == "comp":
            if cid in uobj.groups:
                return True
            else:
                await uobj.ws.send(json.dumps({
                    "func": "compError", "reason": "you aren't registered for this competition..."
                }))
                return False
        else:
            return True


async def compStatus(cid, uobj):
    """Get current competition status.

    Args:
        cid: Competition ID to check
        uobj: Inquiring user

    Returns:
        A CompetitionStatus representing the status of the competition.
    """
    sql = uobj.storage.sql
    tmp = await sql.execute("""
        SELECT competitionstatus, type, automatic, startTime, endTime
        FROM competitions WHERE id=%s
    """, [cid])
    results = await tmp.fetchall()
    if len(results) != 1:
        await uobj.ws.send(json.dumps({
            "func": "compError",
            "reason": "no competition found for compStarted"
        }))
        return CompetitionStatus.BEFORE
    else:
        if results[0][1] == "prac":
            return CompetitionStatus.DURING
        elif results[0][2] == 1:
            tmp = time.time()*1000
            if tmp < results[0][3]:
                return CompetitionStatus.BEFORE
            elif tmp <= results[0][4]:
                return CompetitionStatus.DURING
            else:
                return CompetitionStatus.AFTER
        else:
            return CompetitionStatus(results[0][0])


async def isDuringCompetition(cid, uobj):
    """Check if a competition is active (During Competition).

    Intended for use only with preventing stuff, not general usage.

    Args:
        cid: Competition id
        uobj: Inquiring user object

    Returns:
        True if the competition is "during competition," False if not.
    """
    if (await compStatus(cid, uobj)) == CompetitionStatus.DURING:
        return True
    print("Blocked competition access! CompID:", cid, "UID:", uobj.uid)
    return False


async def isScoreboardAllowed(cid, uobj):
    """Gets whether the scoreboard should be visible.

    Args:
        cid: Competition ID of the scoreboard
        uobj: Inquiring user object

    Returns:
        True if the scoreboard is allowed, False if not.
    """
    sql = uobj.storage.sql
    tmp = await sql.execute("SELECT scoreboardvisible FROM competitions WHERE id=%s", [cid])
    results = await tmp.fetchall()
    if len(results) != 1:
        return False
    else:
        return results[0][0] == 1


async def isPrac(cid, uobj):
    """Gets whether a competition is a practice competition.

    Args:
        cid: Competition ID to check
        uobj: Inquiring user object

    Returns:
        True if the competition is a practice competition, False if not.
    """
    sql = uobj.storage.sql
    tmp = await sql.execute("SELECT type FROM competitions WHERE id=%s", cid)
    results = await tmp.fetchall()
    if len(results) != 1:
        await uobj.ws.send(json.dumps({
            "func": "compError",
            "reason": "no competition found for isPrac"
        }))
    else:
        if results[0][0] == "prac":
            return True
        elif results[0][0] == "comp":
            return False
        else:
            await uobj.ws.send(json.dumps({
                "func": "compError",
                "reason": "competition type not supported for competitionid=" + str(cid)
            }))


async def hashPassword(password):
    """Hashes a password.

    Args:
        password: Password to hash

    Returns:
        A hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
