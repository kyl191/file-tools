import hash, os, shutil, sys, mp4, re
from os.path import join

def hashMP4(filename):
	file = open(filename, 'r')
	try:
		mp4.isMP4(file)
	except Exception as e:
		# So far the only exception is an invalid MP4 header found, so not much to grab
		print(e)
		return
	tempfile = mp4.stripMetadata(file)
	#print os.path.exists(tempfile.name)
	hashresult = hash.sha512file(tempfile.name)
	#print tempfile
	tempfile.close()
	os.remove(tempfile.name)

for root, subfolders, files in os.walk(sys.argv[1]):
	# Mention what path we're working in.
	print("Working in", os.path.abspath(root))
	# Since root contains the working folder, and we'll move onto subfolders later,
	# We only care about the filename
	for filename in files:
		src = os.path.abspath(join(root,filename))
		# Need to find some way to recurse directories in sync with src
		dst = os.path.abspath(join(sys.argv[2],filename))
		if not os.path.isfile(dst):
			shutil.move(src, dst)
			print("Moved {0} to {1}").format(src, dst)
		else:
			if re.search(".mp4",filename,re.IGNORECASE):
				srchash = hashMP4(src)
				dsthash = hashMP4(dst)
			else:
				srchash = hash.sha512file(src)
				dsthash = hash.sha512file(dst)
			if srchash == dsthash:
				print("{0} and {1} are identical. Deleting {2}.").format(src, dst, src)
				os.remove(src)
			else:
				filebase = os.path.splitext(os.path.split(src)[1])[0]
				fileext = os.path.splitext(os.path.split(src)[1])[1]
				count = 2
				while os.path.isfile(os.path.abspath(join(sys.argv[2],filebase + " " + str(count) + fileext))):
					count = count + 1
				newdst = os.path.abspath(join(sys.argv[2],filebase + " " + str(count) + fileext))
				print("{0} and {1} are not identical. Renaming {2} to {3} and moving.").format(src, dst, src, newdst)
				#shutil.move(src, newdst)
