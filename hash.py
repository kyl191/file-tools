import hashlib, os, time

def sha512file(file):
	sha512 = hashlib.sha512()
	try:
		f = open(file,'rb')
	except IOError:
		print("IO Error, unable to open file", file)
	start = time.clock()
	while True:
		# Read in by chunks so we don't max out RAM if we're reading a large file
		# Difference in time between reading by chunks & reading entire file at once for small files is approx 0.03 secs
		data = f.read(20480) # SHA512 take 512 bits, 512*40=20480, read more just to be nice & efficient
		if not data:
			break
		sha512.update(data)
	hash = sha512.hexdigest()
	end = time.clock()
	print "Took", end - start, "seconds to read", os.stat(file).st_size, "bytes"
	f.close()
	return hash
