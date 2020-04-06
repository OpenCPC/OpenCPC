def rmc(a):
    return a.strip(" \t\r\n").replace("\r", "")

def grade(a, b):
    return 0 if rmc(a) == rmc(b) else 1