import sys, remote, os

if len(sys.argv) != 3:
	print("Invalid arguments. Should be server name, hub local ip.")
	quit()

if len(sys.argv[1]) > 15:
	print("Server name too long.")
	quit()

#if not sys.argv[2].isnumeric():
#	print("rsid improper.")
#	quit()

if not os.geteuid() == 0:
	print("need euid 0")
	quit()

for c in sys.argv[1]:
	if not (c.isalnum() or c in "_-"):
		print("Server name must be alphanumeric or in \"_-\".")

if not os.path.isdir("/tmp/MCSC"):
	os.makedirs("/tmp/MCSC")
os.chdir("/tmp/MCSC")
if not os.path.isdir(sys.argv[1]):
	os.makedirs(sys.argv[1])
if not os.path.isdir(sys.argv[1] + "/run"):
	os.makedirs(sys.argv[1] + "/run")
if not os.path.isdir(sys.argv[1] + "/run/unused"):
	os.makedirs(sys.argv[1] + "/run/unused")
if not os.path.isdir(sys.argv[1] + "/compile"):
	os.makedirs(sys.argv[1] + "/compile")
if not os.path.isdir(sys.argv[1] + "/compile/unused"):
	os.makedirs(sys.argv[1] + "/compile/unused")
os.chdir(sys.argv[1])

remote.start(sys.argv[1], sys.argv[2], 65534)
