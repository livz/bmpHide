import sys
import base64

'''
Create a batch file that dumps and runs an exe.

	binary.txt	-> binary file, base64 encoded
	decode.vbs	-> decode the base64 encoded binary and dump to disk
	wrapper.bat -> output batch wile, wraps vbs decoder, runs exe, cleans up
	
Base64 encode a binary:
$ cat binary | base64 -w 0 > binary.txt

'''

def usage(progName):
	print "Create a batch file (.BAT) that dumps and runs an exe."
	print "Usage: %s <exe>" % progName
	sys.exit()
	
if __name__ == "__main__":
	if len(sys.argv) != 2:
		usage(sys.argv[0])
		
	decoder = "decode.vbs"
	bat = "wrapper.bat"
	exe = sys.argv[1]
	
	fin = open(decoder, "r")
	fout = open(bat, "w")

	fout.write("@echo off\n")
	
	for l in fin.readlines():
		if l.strip():
			fout.write("echo %s >> run.vbs\n" % l.strip())
	fin.close()

	# Add base64 encoded binary to the batch file
	content = ""
	fin = open(exe, "r")
	for l in fin.readlines():
		content += l
	contenBase64 = base64.b64encode(content)
	fin.close()

	chunks = [contenBase64[i:i + 80] for i in range(0, len(contenBase64), 80)]
	for c in chunks:
		fout.write("echo %s >> binary.txt\n" % c)
	
	# Decode binary
	fout.write("run.vbs binary.txt binary.exe\n")

	# Run
	fout.write("binary.exe\n")

	# Cleanup
	fout.write("del run.vbs\n")
	fout.write("del binary.exe\n")
	fout.write("del binary.txt\n")
	fout.write("del %s" % bat)

	fout.close()
	
