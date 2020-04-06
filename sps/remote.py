import sys, subprocess, traceback, os, submission, time, websockets, asyncio, pickle, iolist

# print(submission.submission("print(input())", "py", 1, 1, ["test"], ["tesst"], [-1], -1))



async def handleHubMessage(ws, msg, spsName, uids):
    params = pickle.loads(msg)
    if params["func"] == "procsub":
        listID = await iolist.findProblem(params["pid"])


        if listID == -1 or iolist.problems[listID].lastupdated != params["lastupdated"]:
            await ws.send(pickle.dumps({"func":"requestProblem", "params":params}))
        else:
            prob = iolist.problems[listID]
            await ws.send(pickle.dumps({"func":"subresult", "subid":params["subid"], "result":
                await submission.submission(ws, spsName, uids, params["code"], params["lang"], params["pid"], prob.runtimelimit, prob.memlimit, prob.input, prob.expected, prob.points, params["uid"], params["subid"], params["customrun"], params["gid"], params["problem_number"])}))
    elif params["func"] == "requestProblem":
        print("Requesting problem",params["pid"])
        listID = await iolist.findProblem(params["pid"])
        if listID == -1:
            await iolist.addProblem(params["pid"], params["lastupdated"], params["runtimelimit"], params["memlimit"], params["input"], params["expected"], params["values"])
        else:
            await iolist.updateProblem(params["pid"], params["lastupdated"], params["runtimelimit"], params["memlimit"], params["input"], params["expected"], params["values"])
        await ws.send(pickle.dumps({"func":"subresult", "subid":params["subid"], "result":
            await submission.submission(ws, spsName, uids, params["code"], params["lang"], params["pid"], params["runtimelimit"], params["memlimit"], params["input"], params["expected"], params["values"], params["uid"], params["subid"], params["customrun"], params["gid"], params["problem_number"])}))

    else:
        print(params)

async def getHubMessage(ws, spsName, uids):
    while True:
        msg = await ws.recv()
        await handleHubMessage(ws, msg, spsName, uids)

async def hubConnect(spsName, hubIP, uids):
    while True:
        try:
            async with websockets.connect('ws://' + hubIP + ':35123') as ws:
                print("Hub connected.")
                await ws.send("Hi, I'm a valid submission processing server and totally not an imposter.")
                await ws.send(spsName)
                await getHubMessage(ws, spsName, uids)
                print("Hub disconnnected.")
        except ConnectionRefusedError:
            print("WS ConRefused")
        except websockets.exceptions.ConnectionClosed:
            print("WS ConnectionClosed")

        await asyncio.sleep(5)



def start(spsName, hubIP, uids):
    asyncio.get_event_loop().run_until_complete(hubConnect(spsName, hubIP, uids))
