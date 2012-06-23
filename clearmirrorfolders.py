import hash, os, sys, re
from os.path import join, getsize

source_dir = os.path.abspath(sys.argv[1])
compare_dir = os.path.abspath(sys.argv[2])
deleted_files = 0
space_saved = 0
for root, subfolders, files in os.walk(source_dir):
	# Since root contains the working folder, and we'll move onto subfolders later, 
	# We only care about the filename
	(null, path, pathsuffix) = root.rpartition(source_dir)
	dup_folder = os.path.normpath(compare_dir + "/" + pathsuffix)
	# Mention what path we're working in.
	print("Comparing: " + os.path.abspath(root))
	print("To: " + os.path.abspath(dup_folder))
	for filename in files:
		dup = os.path.abspath(dup_folder + "/" + filename)
		filename = join(root,filename)
		if os.path.exists(dup):
			hash1 = hash.sha512file(filename)
			hash2 = hash.sha512file(dup)
			if hash1 == hash2:
				#print os.path.abspath(filename) + ": \n" + hash1
				#print os.path.abspath(dup) + ": \n" + hash2
				deleted_files = deleted_files + 1
				space_saved = space_saved + os.path.getsize(dup)
				print "[" + str(deleted_files) + "] Removing " + dup
				#os.remove(dup)
	if os.path.exists(dup_folder) and not os.listdir(dup_folder):
		os.rmdir(dup_folder)
print("Deleted " + str(deleted_files) + ", saving " + str(space_saved) + " bytes of space")
