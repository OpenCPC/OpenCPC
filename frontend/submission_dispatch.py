import websockets
import asyncio
import pickle


async def submissionDispatchFunc(storage):
    """Dispatches submissions to submission processing servers.

    Args:
        storage: A Storage object
    """
    totalSDFRuntime = 0
    sql = storage.sql
    try:
        if storage.sdf_submission_dispatch_awaitable is None:
            storage.sdf_submission_dispatch_awaitable = asyncio.get_event_loop().create_future()

        while True:
            # Wait for another reason to run
            await storage.sdf_submission_dispatch_awaitable
            storage.sdf_submission_dispatch_awaitable = asyncio.get_event_loop().create_future()

            # Increment the total runtime so we can know about infinite loops
            totalSDFRuntime += 1
            if totalSDFRuntime > 100000:
                print("sdf running", totalSDFRuntime)

            # Pull submissions that have not been processed yet
            tmp = await sql.execute(
                "SELECT id, userid, competitionid, programtype, programcode, "
                "problemid, customrunoriginal, groupid FROM submissions WHERE "
                "status=0 ORDER BY id ASC LIMIT %s",
                [len(storage.all_sp)]
            )
            availsubs = list(await tmp.fetchall())

            # Remove submissions from the list if they are already being processed
            for sp in storage.all_sp:
                if sp.busy:
                    for i in range(len(availsubs)):
                        if availsubs[i][0] == sp.cursubid:
                            del availsubs[i]
                            break

            # Assign submissions to submission processing servers if they are available
            totalBusy = 0
            for sp in storage.all_sp:
                if not sp.busy:
                    if len(availsubs) > 0:
                        print("Grading Program")
                        problemTmp = await sql.execute("""
                            SELECT lastupdated, problemnumber FROM problems
                            WHERE id=%s
                        """, [availsubs[0][5]])
                        problemResults = await problemTmp.fetchall()

                        sp.busy = True
                        sp.cursubid = availsubs[0][0]
                        await sp.ws.send(pickle.dumps({
                            "func": "procsub",
                            "code": availsubs[0][4],
                            "lang": availsubs[0][3],
                            "pid": availsubs[0][5],
                            "uid": availsubs[0][1],
                            "gid": availsubs[0][7],
                            "problem_number": problemResults[0][1],
                            "subid": availsubs[0][0],
                            "lastupdated": problemResults[0][0],
                            "customrun": availsubs[0][6],
                            "pnum": problemResults[0][1]
                        }))
                        del availsubs[0]
                        totalBusy += 1
                else:
                    totalBusy += 1
    finally:
        print("SDF Exit")


async def submissionDispatchIntervalFunc(storage):
    """Makes sure the submission dispatcher runs at least every 5 seconds.

    Args:
        storage: A Storage object
    """
    try:
        if storage.sdf_submission_dispatch_awaitable is None:
            storage.sdf_submission_dispatch_awaitable = asyncio.get_event_loop().create_future()
        while True:
            storage.schedule_sdf()
            await asyncio.sleep(5)
    finally:
        print("SDFI Exit")
