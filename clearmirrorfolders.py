import mp4, hash, os, sys, re
from os.path import join, getsize

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


os.chdir(sys.argv[1])
compare_dir = sys.argv[2]
deleted_files = 0
space_saved = 0
for root, subfolders, files in os.walk('.'):
	# Since root contains the working folder, and we'll move onto subfolders later, 
	# We only care about the filename
	(null, path, pathsuffix) = root.rpartition(sys.argv[1])
	dup_folder = os.path.normpath(compare_dir + pathsuffix)
	# Mention what path we're working in.
	print("Comparing: " + os.path.abspath(root))
	print("To: " + os.path.abspath(dup_folder))
	for filename in files:
		# If is does, hash & add it to the db
		#hashAndAdd(os.path.abspath(join(root,filename)))
		dup = dup_folder + "/" + filename
		filename = join(root,filename)
		#print os.path.abspath(filename)
		#print os.path.abspath(dup)
		if os.path.exists(dup):
			if mp4.isMP4(filename) and mp4.isMP4(dup):
				hash1 = hashmp4(filename)
				hash2 = hashmp4(dup)
			else:
				hash1 = hash.sha512file(filename)
				hash2 = hash.sha512file(dup)
			if hash1 == hash2:
				deleted_files = deleted_files + 1
				space_saved = space_saved + os.path.getsize(dup)
				print "[" + str(deleted_files) + "] Removing " + dup
				os.remove(dup)
	if os.path.exists(dup_folder) and not os.listdir(dup_folder):
		os.rmdir(dup_folder)		
print("Deleted " + str(deleted_files) + ", saving " + str(space_saved) + " bytes of space")
