import time, sys, copy
#test2
problems = []

class Problem:
    def __init__(self, pid, lastupdated, runtimelimit, memlimit, input, expected, points):
        self.pid = pid
        self.lastused = time.time()
        self.lastupdated = lastupdated
        self.runtimelimit = runtimelimit
        self.memlimit = memlimit
        self.input = copy.deepcopy(input)
        self.expected = copy.deepcopy(expected)
        self.points = copy.deepcopy(points)

    def getsize(self):
        totalsize = sys.getsizeof(self) + sys.getsizeof(self.pid)+ sys.getsizeof(self.lastused) + sys.getsizeof(self.lastupdated)
        totalsize += sys.getsizeof(self.input) + sys.getsizeof(self.expected) + sys.getsizeof(self.points)
        return totalsize

async def findProblem(pid):
    for i in range(len(problems)):
        if problems[i].pid == pid:
            print("findProblem(" + str(pid) + ") returns " + str(i))
            return i
    return -1

async def getTotalSize():
    totalsize = sys.getsizeof(problems)
    for i in range(len(problems)):
        totalsize += problems[i].getsize()
    print("getTotalSize() returns " + str(totalsize))
    return totalsize 

async def deleteProblem():
    oldest = 0
    for i in range(1, len(problems)):
        if problems[i].lastused < problems[oldest].lastused:
            oldest = i
    print("deleteProblem() returns " + str(oldest))
    del problems[oldest]

async def fixSize():
    while await getTotalSize() > 100000000:
        await deleteProblem()

async def addProblem(pid, lastupdated, runtimelimit, memlimit, input, output, values):
    print("Adding Problem")
    print(input)
    print(output)
    print(values)
    newproblem = Problem(pid, lastupdated, runtimelimit, memlimit, input, output, values)
    problems.append(newproblem)
    await fixSize()

async def updateProblem(pid, lastupdated, runtimelimit, memlimit, input, output, values):
    print("Updating Problem")
    toupdate = await findProblem(pid)
    problems[toupdate].lastupdated = lastupdated
    problems[toupdate].runtimelimit = runtimelimit
    problems[toupdate].memlimit = memlimit
    problems[toupdate].input = copy.deepcopy(input)
    problems[toupdate].expected = copy.deepcopy(output)
    problems[toupdate].points = copy.deepcopy(values)
    print("UPDATING INPUT")
    print(problems[toupdate].input)
    print(problems[toupdate].expected)
    print(problems[toupdate].points)
    await fixSize()