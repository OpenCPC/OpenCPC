import sys, os, time, subprocess, signal

###### ******* ********* ******** UNSECURE!!!! THIS FILE IS TEMPORARY AND MUST BE UDPATED WITH SECURE USER CHANGES AND A NEW DIRECTORY

#might want to change it so that it just waits for the child to exit and then while waiting it has a thread that terminates if it needs to
#that would give higher precision on the runtime

def ignoreSignal(a, b):
    os.wait()

runPid = -1
timeOut = [False]

def handleTimeout(a, b):
    global runPid, timeOut
    #print("IN HANDLE TIMEOUT")
    if runPid != -1 and runPid != 0:
        #print("IN HANDLETIMEOUT")
        timeOut[0] = True
        subprocess.call("sudo kill -9 "+str(runPid), shell=True)

def runProgram(path, lang, timecap, memlimit, uids, block_, rres, eloop):
    global runPid, timeOut
    # runs program at path and changes context to /run and supplies input.txt and outputs to output.txt and error.txt
    # returns status (0=self-ended, 1=terminated), runtime, program output, and error

    #override uids to 'nobody'
    uids = 65534

    if not os.geteuid() == 0:
        print("need euid 0")
        quit()

    timecap = int(timecap)
    if timecap < 1:
        timecap = 1
    if timecap > 30:
        timecap = 30

    startms = int(time.time() * 1000.0)

    pid = -1
    timeOut = [False]
    runPid = -1

    #def handleSignal(a, b):
        #print("IN HANDLE SIGNAL, pid:",str(pid))

        #tmppid, tmpstatus, rusage = os.wait4(pid, 0)
        #data.append(rusage)
        #print(rusage)
        #print(timedOut)
        #if timedOut[0]:
        #    data.append(1)
        #else:
        #    signal.alarm(0)
        #    data.append(0)

    #signal.signal(signal.SIGCHLD, handleSignal)

    pid = os.fork()

    #print("b",pid)

    if pid == 0:

        # WARNING DO NOT RETURN HERE. WILL CAUSE GLITCHES.


        if not os.geteuid() == 0:
            print("No root permissions during pipe setup, quitting to preserve security")
            quit()

        subprocess.call("touch run/output.txt", shell=True)
        subprocess.call("touch run/error.txt", shell=True)
        os.dup2(os.open('run/input.txt', os.O_RDONLY), 0)
        os.dup2(os.open('run/output.txt', os.O_RDWR|os.O_CREAT|os.O_TRUNC), 1)
        os.dup2(os.open('run/error.txt', os.O_RDWR|os.O_CREAT|os.O_TRUNC), 2)

        if not os.geteuid() == 0:
            print("No root permissions during security setup, quitting to preserve security")
            quit()

        os.setresgid(uids, uids, uids)
        os.setresuid(uids, uids, uids)

        c = os.getresuid() + os.getresgid()

        for cur in c:
            if cur != uids:
                print("User id set wrong, quitting to preserve security (dump:",c,")")
                quit()

        if os.geteuid() == 0:
            print("Effective user id still root, quitting to preserve security")
            quit()

        if lang=="cpp":
            os.execl(path, path[path.find('/')+1:])
        elif lang=="py":
            os.execl("/usr/bin/python3", "/usr/bin/python3", path)
        elif lang=="java":
            os.execl("/usr/bin/java", "/usr/bin/java", "-cp", "compile/", path)
        elif lang=="c":
            os.execl(path, path[path.find('/')+1:])
        else:
            print("LANG ERROR",lang)
        quit()
    else:
        runPid = pid
        #signal.sigwait([signal.SIGCHLD])
        tmppid, tmpstatus, rusage = os.wait4(pid, 0)
        #print(rusage)
        #print(timeOut)
        #print(os.path.isdir('/proc/{}'.format(pid)))

        #print("Fetching output")
        ols = open("run/output.txt").read(1000000)

        if len(ols) == 1000000:
            print("Capacity reached.")
            ols += "\r\nOutput limited to only 1,000,000 bytes."

        #print("Fetching error")
        els = open("run/error.txt").read(1000000)

        if len(els) == 1000000:
            print("Capacity reached.")
            els += "\r\nError limited to only 1,000,000 bytes."

        if timeOut[0] == False:
            signal.alarm(0)
            if rusage.ru_maxrss > memlimit*1000:
                rres += [2, int(timecap * 1000.0), ols, els]
            else:
                rres += [0, int(timecap * 1000.0), ols, els]
        elif timeOut[0] == True:
            #print("Returning timeOut")
            rres += [1, int(timecap * 1000.0), ols, els]
        #print("Releasing block...")
        eloop.call_soon_threadsafe(block_.set_result, (None))
        #print("Block released.")

