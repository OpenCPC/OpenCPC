import sys, subprocess, traceback, os, compile, run, grade, websockets, asyncio, pickle, threading, signal

def first1023(a):
    #ensures about 1023 and a single newline at the end
    if len(a)>1023:
        return a[:1023] + "\r\n" + "(1023 chars displayed of "+str(len(a))+")" + "\r\n"
    return a.strip("\r\n")+"\r\n"

async def submission(ws, spsName, uids, code, lang, problem, runtime, memlimit, input, expected, points, userid, subid, customrunoriginal, gid, problem_number):
    #return status, score, submission log
    ostatus = -1 # 0 is backend error, 1 is compile fail, 2 is successfully graded, 3 missed sample case (still graded test cases though)
    oscore = 0
    osublog = ""

    if ws != None:
        await ws.send(pickle.dumps({"func": "live", "command": "init", "uid": userid, "subid": subid, "pid": problem, "input_len": len(input), "gid": gid}))

    osublog += "Submission information:" + "\r\n"
    osublog += "Code Length: " + str(len(code)) + "\r\n"
    osublog += "Code Language: " + lang + "\r\n"
    osublog += "Problem ID: " + str(problem) + "\r\n"
    osublog += "Problem number: " + str(problem_number) + "\r\n"
    osublog += "User ID: " + str(userid) + "\r\n"
    osublog += "Submission ID: " + str(subid) + "\r\n"
    osublog += "Submission Processing Server Name: " + spsName + "\r\n"
    osublog += "\r\n"
    osublog += "Compiling submission..." + "\r\n"
    osublog += "\r\n"

    print("New Submission,",subid)

    cres = compile.compileProgram(code, lang, problem_number)

    if cres[0] == 0:
        print("General Error")
        osublog += "General error." + "\r\n"
        ostatus = 0

    elif cres[0] == 1:
        print("Lang Error")
        osublog += "Lang error." + "\r\n"
        ostatus = 0
    elif cres[0] == 2:
        print("Compile Fail")
        osublog += "Compile fail."
        osublog += "\r\n"
        osublog += "Compile log:" + "\r\n"
        osublog += first1023(cres[1])
        ostatus = 1
        if ws != None:
            await ws.send(pickle.dumps({"func": "live", "command": "comf", "uid": userid, "subid": subid, "pid": problem, "gid": gid}))
    elif cres[0] == 3:
        #print("Compile Success")

        totalScore = 0

        osublog += "Compile success." + "\r\n"
        osublog += "\r\n"
        osublog += "Grading submission on sample & test cases..." + "\r\n"
        osublog += "\r\n"

        missedSample = False

        for i in range(len(input)):
            #print("Case " + str(i+1) + "/" + str(len(input)))

            if ws != None:
                await ws.send(pickle.dumps({"func":"live", "command":"case", "uid":userid, "subid":subid, "pid":problem, "index":i, "gid": gid}))

            if points[i] == -1:
                osublog += "Case " + str(i+1) + "/" + str(len(input)) + " (Sample Case)" + "\r\n"
            else:
                osublog += "Case " + str(i+1) + "/" + str(len(input)) + " (Worth " + str(points[i]) + "pts)" + "\r\n"

            subprocess.call("rm run/* -R", shell=True)
            inpFile = open("run/input.txt", "w")
            inpFile.write(input[i])
            inpFile.close()

            block_ = asyncio.get_event_loop().create_future()
            rres = []
            signal.signal(signal.SIGALRM, run.handleTimeout)
            signal.alarm(runtime + 1)
            thr = threading.Thread(target=run.runProgram, args=(cres[1], lang, runtime, memlimit, uids, block_, rres, asyncio.get_event_loop()))
            thr.start()
            #rres = run.runProgram(cres[1], lang, runtime, memlimit, uids)
            await block_;
            thr.join()
            signal.alarm(0)
            #print("RRES:", rres)
            postSample = False

            if len(rres[3]):
                print("Run Time Error")
                osublog += "Run Time Error." + "\r\n"
                postSample = True
                if ws != None:
                    await ws.send(pickle.dumps({"func":"live", "command":"rte", "uid":userid, "subid":subid, "pid":problem, "index":i, "gid":gid}))
            elif rres[0] == 0:
                gres = grade.grade(rres[2], expected[i])
                if gres == 0:
                    #print("Correct Output, +"+str(points[i])+"pts (if is not sample)")
                    if ws != None:
                        await ws.send(pickle.dumps({"func":"live", "command":"co", "uid":userid, "subid":subid, "pid":problem, "index":i, "gid":gid}))
                    if points[i] == -1:
                        osublog += "Correct Output" + "\r\n"
                    else:
                        totalScore += points[i]
                        osublog += "Correct Output, +"+str(points[i])+"pts" + "\r\n"
                else:
                    print("Incorrect Output")
                    osublog += "Incorrect Output." + "\r\n"
                    if ws != None:
                        await ws.send(pickle.dumps({"func":"live", "command":"io", "uid":userid, "subid":subid, "pid":problem, "index":i, "gid":gid}))
                    postSample = True
            elif rres[0] == 1:
                print("Run Time Exceeded, Terminated")
                osublog += "Run Time Exceeded, Terminated." + "\r\n"
                if ws != None:
                    await ws.send(pickle.dumps({"func":"live", "command":"rtlet", "uid":userid, "subid":subid, "pid":problem, "index":i, "gid":gid}))
                postSample = True
            elif rres[0] == 2:
                print("Memory Limit Exceeded.")
                osublog += "Memory Limit Exceeded." + "\r\n"
                if ws != None:
                    await ws.send(pickle.dumps({"func":"live", "command":"mlet", "uid":userid, "subid":subid, "pid":problem, "index":i, "gid":gid}))
                postSample = True
            else:
                print("Return Error R")
                osublog += "Return Error r." + "\r\n"

            if (points[i] == -1 or customrunoriginal != -1) and postSample:
                missedSample = True
                if points[i] == -1:
                    osublog += "Since 'Correct Output' was not achieved, and since this is a sample case, here are the contents of the input file, output file, expected output, and error file:" + "\r\n"
                elif customrunoriginal != -1:
                    osublog += "Since 'Correct Output' was not achieved, and since this is a custom run, here are the contents of the input file, output file, expected output, and error file:" + "\r\n"

                osublog += "Input File:" + "\r\n"
                osublog += first1023(input[i])
                osublog += "Output File:" + "\r\n"
                osublog += first1023(rres[2])
                osublog += "Expected Output:" + "\r\n"
                osublog += first1023(expected[i])
                osublog += "Error File:" + "\r\n"
                osublog += first1023(rres[3])
            osublog += "\r\n"

        print("Total Score:",totalScore)
        osublog += "Finished grading." + "\r\n"
        osublog += "Total score: " + str(totalScore) + "\r\n"

        oscore = totalScore
        ostatus = 2
        if missedSample:
            ostatus = 3

    else:
        print("Return Error C")
        osublog += "Return Error C." + "\r\n"
        ostatus = 0


    if ws != None:
        await ws.send(pickle.dumps({"func":"live", "command":"stop", "uid":userid, "subid":subid, "pid":problem, "gid":gid}))

    print("Finished grading submission")
    return ostatus, oscore, osublog
