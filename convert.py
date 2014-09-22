import sys
import math
import Image

'''
Store any file inside the pixel array of a 24-bit bitmap image (BMP).

References:
http://en.wikipedia.org/wiki/BMP_file_format

'''

# Output file dimensions - multiples of 4 (dinamically adjusted)
# (Because each row in the pixels array is padded to a multiple of 4 bytes)
WIDTH = 256
HEIGHT = 256

def usage(progName):
	print "Convert any file into a pixel array and store in a 24-bit bitmap image."
	print "Usage: %s <in-file> <out-file>" % progName
	sys.exit()
	
def loadText(fname):
	print "[*] Reading text from %s" % fname

	body = "\r\n\r\n"
	f = open(fname)
	for c in f.readlines():
		body += c
	f.close()
	
	# Pad with '0' to multiple of 3
	body += (3 - len(body) % 3) * chr(0) 
	bodyLen = len(body)
	body = [ord(c) for c in body]

	# Compute minimum BMP dimensions based on input file size
	dmin = int(math.sqrt(bodyLen/3) + 1)
	dmin += (4 - dmin % 4)	# next multiple of 4
	global WIDTH, HEIGHT
	HEIGHT = WIDTH = dmin
	
	print "[*] Need a %dx%d BMP" % (HEIGHT, WIDTH)
	
	v = [[0 for y in range(HEIGHT)] for x in range(WIDTH)]
	
	i = 0
	# Place the row arrays in reverse !
	for h in xrange(HEIGHT-1, -1, -1):
		for w in range(WIDTH):
			if i < bodyLen:
				v[w][h] = (body[i+2], body[i+1], body[i])
			else:
				v[w][h] = (0, 0, 0)
			i += 3
		
	return v
		
def saveImage(inArr, outFile):
	img = Image.new( 'RGB', (WIDTH, HEIGHT))
	pixels = img.load()

	print "[+] Writting BMP to %s" % outFile
	
	for w in range(WIDTH):
		for h in range(HEIGHT):
			pixels[w, h] = inArr[w][h]

	img.save(outFile)
	
if __name__ == "__main__":
	if len(sys.argv) != 3:
		usage(sys.argv[0])
		
	v = loadText(sys.argv[1])
	saveImage(v, sys.argv[2])
	
