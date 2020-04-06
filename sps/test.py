import sys, subprocess, traceback, os, submission, time, websockets, asyncio, pickle

import sys, remote, os

if not os.geteuid() == 0:
	print("need euid 0")
	quit()

if not os.path.isdir("/tmp/MCSC"):
	os.makedirs("/tmp/MCSC")
os.chdir("/tmp/MCSC")
tvv = "MCSC_TEST"
if not os.path.isdir(tvv):
	os.makedirs(tvv)
if not os.path.isdir(tvv + "/run"):
	os.makedirs(tvv + "/run")
if not os.path.isdir(tvv + "/run/unused"):
	os.makedirs(tvv + "/run/unused")
if not os.path.isdir(tvv + "/compile"):
	os.makedirs(tvv + "/compile")
if not os.path.isdir(tvv + "/compile/unused"):
	os.makedirs(tvv + "/compile/unused")
os.chdir(tvv)



#async def submission(ws, spsName, uids, code, lang, problem, runtime, input, expected, points, userid, subid):

async def main():
    #correct
    print((await submission.submission(None, tvv, 65534, "print(input())", "py", -1, 2, ["hello", "hello2"], ["hello", "hello2"], [-1, 5], -1, -1)))
    #timeout
    print((await submission.submission(None, tvv, 65534, """while True:
    pass
    """, "py", -1, 2, ["hello", "hello2"], ["hello", "hello2"], [-1, 5], -1, -1)))
    #disallowed access
    print((await submission.submission(None, tvv, 65534, """
import os
os.makedirs("/home/ubuntu/testh")
    """, "py", -1, 2, ["hello", "hello2"], ["hello", "hello2"], [-1, 5], -1, -1)))


asyncio.get_event_loop().run_until_complete(main())
