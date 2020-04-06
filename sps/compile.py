import sys, subprocess, traceback, os

def compileProgram(code, lang, problem):
    # lang can be of cpp, py, java
    # returns tuple of result (0 total error, 1 lang error, 2 compile fail, 3 success), output path or error

    subprocess.call("rm compile/* -R", shell=True)

    try:
        if lang == 'py':
            return compileProgram_py(code)
        elif lang == 'cpp':
            return compileProgram_cpp(code)
        elif lang == 'java':
            return compileProgram_java(code, problem)
        elif lang == 'c':
            return compileProgram_c(code)
        else:
            return 1, "Language Error"
    except Exception as ex:
        return 0, traceback.print_exc()
    except:
        return 0, "General Error"

def compileProgram_py(code):

    codeFile = open("compile/main.py", "w")
    codeFile.write(code)
    codeFile.close()

    subprocess.call("python3 -m py_compile compile/main.py 2> compile/log.txt", shell=True)

    logInfo = os.stat("compile/log.txt")

    if logInfo.st_size > 0:
        return 2, ''.join(open("compile/log.txt").readlines())

    return 3, "compile/main.py"

def compileProgram_cpp(code):

    codeFile = open("compile/main.cpp", "w")
    codeFile.write(code)
    codeFile.close()

    subprocess.call("g++ -o compile/main compile/main.cpp -std=c++11 2> compile/log.txt", shell=True)

    logInfo = os.stat("compile/log.txt")

    if logInfo.st_size > 0:
        return 2, ''.join(open("compile/log.txt").readlines())
    else:
        subprocess.call("chmod a+x compile/main", shell=True)

    return 3, "compile/main"

def compileProgram_java(code, problem):

    codeFile = open("compile/Problem"+str(problem)+".java", "w")
    codeFile.write(code)
    codeFile.close()

    subprocess.call("javac -d compile/ compile/Problem"+str(problem)+".java 2> compile/log.txt", shell=True)

    logInfo = os.stat("compile/log.txt")

    if logInfo.st_size > 0:
        return 2, ''.join(open("compile/log.txt").readlines())

    return 3, "Problem"+str(problem)

def compileProgram_c(code):

    codeFile = open("compile/main.c", "w")
    codeFile.write(code)
    codeFile.close()

    subprocess.call("gcc compile/main.c -o compile/main 2> compile/log.txt", shell=True)

    logInfo = os.stat("compile/log.txt")

    if logInfo.st_size > 0:
        return 2, ''.join(open("compile/log.txt").readlines())
    else:
        subprocess.call("chmod a+x compile/main", shell=True)

    return 3, "compile/main"