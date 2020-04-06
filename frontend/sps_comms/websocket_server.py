import websockets
import asyncio
import pickle
import json
from .sub_proc_object import SubProcObject


async def submissionProcessingServerHandleMessage(spo, msg, storage):
    """Handles submission processing server messages.

    Args:
        spo: The server's SubProcObject
        msg: The pickled message
        storage: A Storage object
    """
    sql = storage.sql
    params = pickle.loads(msg)
    if params["func"] == "subresult":
        if params["subid"] != spo.cursubid or not spo.busy:
            print("Unexpected sub result:", spo, msg)
        else:
            spo.busy = False
            rstat = 2
            if params["result"][0] == 1:
                rstat = 1
            tmp = await sql.execute(
                """
                    UPDATE submissions SET status=%s, runlog=%s, score=%s, sps=%s
                    WHERE id=%s
                """,
                [
                    rstat,
                    params["result"][2],
                    params["result"][1],
                    spo.spsName,
                    params["subid"]
                ]
            )
            storage.schedule_sdf()

    elif params["func"] == "live":
        for cl in storage.all_cl:
            if params["gid"] in cl.groups.values():
                await cl.ws.send(json.dumps({"func": "live", "params": params}))

    elif params["func"] == "requestProblem":
        problemTmp = await sql.execute("""
            SELECT lastupdated, runtimelimit, memorylimit, problemnumber FROM problems
            WHERE id=%s
        """, [params["params"]["pid"]])
        problemResults = await problemTmp.fetchall()

        tmp = await sql.execute("""
            SELECT id, input, expected, value FROM cases
            WHERE problemid=%s ORDER BY id
        """, [params["params"]["pid"]])
        cases = await tmp.fetchall()

        c_input = []
        c_expected = []
        c_value = []

        for c in cases:
            c_input.append(c[1])
            c_expected.append(c[2])
            c_value.append(c[3])
        await spo.ws.send(pickle.dumps({
            "func": "requestProblem",
            "code": params["params"]["code"],
            "lang": params["params"]["lang"],
            "pid": params["params"]["pid"],
            "pnum": problemResults[0][3],
            "uid": params["params"]["uid"],
            "gid": params["params"]["gid"],
            "problem_number": params["params"]["problem_number"],
            "subid": params["params"]["subid"],
            "lastupdated": problemResults[0][0],
            "runtimelimit": problemResults[0][1],
            "memlimit": problemResults[0][2],
            "input": c_input,
            "expected": c_expected,
            "values": c_value,
            "customrun": params["params"]["customrun"]
        }))
    else:
        print("spshm,", params)


async def submissionProcessingServerNewMessage(spo, storage):
    """Reads new submission processing server messages.

    Args:
        spo: The SubProcObject of the SPS
        storage: A Storage object
    """
    while True:
        msg = await spo.ws.recv()
        await submissionProcessingServerHandleMessage(spo, msg, storage)


async def submissionProcessingServer(ws, path, storage):
    """Serves a new submission processing server.

    Args:
        ws: A websocket
        path: The websocket's connection path (unused)
        storage: A Storage object
    """
    allSP = storage.all_sp
    checkCode = await ws.recv()

    if checkCode != "Hi, I'm a valid submission processing server and totally not an imposter.":
        ws.send("Invalid submission processing server check code.")
        print("Invalid submission processing server check code received.")
        return

    spsName = await ws.recv()

    for tsp in allSP:
        if tsp.spsName == spsName:
            ws.send("Duplicate sps name")
            print("Duplicate sps name, rejected server", spsName)
            return

    allSPL = SubProcObject(ws, storage.unique_spid, spsName)
    storage.unique_spid += 1
    allSP.append(allSPL)

    print("New submission processing server, " + spsName + ". Total:", len(allSP))

    try:
        await submissionProcessingServerNewMessage(allSPL, storage)
    except websockets.exceptions.ConnectionClosed:
        print("WS ConnClosed")
    finally:
        allSP.remove(allSPL)
    print("Lost submission processing server, " + spsName + ". Total:", len(allSP))
