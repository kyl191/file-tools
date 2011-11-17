import struct, tempfile

def stripMetadata(file):
	temp = tempfile.NamedTemporaryFile(delete=False)
	pos = findLastAtom(file)
	file.seek(pos)
	while True:
		data = file.read(51200)
		#print len(data)
		temp.write(data)
		if not data:
			break
	#print temp.name
	#print temp
	return temp
	
def isMP4(file):
	# Check if it's a valid MP4 file first by trying to get the file header 
	# 1st 4 bytes are length. 2nd 4 bytes are the signature.
	# Seek to the header @ 4th byte
	file.seek(4)
	header = file.read(4)
	if header == "ftyp":
		return True
	else:
		return False

def findLastAtom(file):
	file.seek(0)
	rawlength = file.read(4)
	length = struct.unpack(">I", rawlength)[0]
	name = file.read(4)
	while name != "mdat":
		#print name, length
		#print "seeking to " + str(file.tell() + length - 8)
		file.seek(file.tell()+length-8)
		rawlength = file.read(4)
		length = struct.unpack(">I", rawlength)[0]
		name = file.read(4)
	return file.tell()
		
		
		
#filename = 	"test.mp4"
#file = open(filename, 'r')
#print stripMetadata(file)
