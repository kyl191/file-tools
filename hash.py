import hashlib, os, time

def sha512file(file):
	sha512 = hashlib.sha512()
	try:
		f = open(file,'rb')
	except IOError:
		print("IO Error, unable to open file", file)
	start2 = time.clock()
	hash2 = hashlib.sha512(f.read()).hexdigest()
	end2 = time.clock()
	start = time.clock()
	f.seek(0)
	while True:
		data = f.read(10240) # SHA512 take 512 bits, 512*20=10240, read more just to be nice & efficient
		if not data:
			break
		sha512.update(data)
	hash1 = sha512.hexdigest()
	end = time.clock()
	print "Took", end - start, "seconds to read", os.stat(file).st_size, "bytes"
	print "Took", end2 - start2, "seconds to read", os.stat(file).st_size, "bytes at once"
	f.close()
	assert(hash1 == hash2)
	return hash1
