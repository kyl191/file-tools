import hash, os, sys, re
from os.path import join, getsize

os.chdir(sys.argv[1])
compare_dir = sys.argv[2]
deleted_files = 0
space_saved = 0
for root, subfolders, files in os.walk('.'):
	# Mention what path we're working in.
	print("Working in " + os.path.abspath(root))
	# Since root contains the working folder, and we'll move onto subfolders later, 
	# We only care about the filename
	(null, path, pathsuffix) = os.path.abspath(root).partition(os.path.abspath(sys.argv[1]))
	for filename in files:
		# If is does, hash & add it to the db
		#hashAndAdd(os.path.abspath(join(root,filename)))
		dup = compare_dir + pathsuffix + "/" + filename
		filename = join(root,filename)
		print os.path.abspath(filename)
		print os.path.abspath(dup)
		if os.path.exists(dup):
			hash1 = hash.sha512file(filename)
			hash2 = hash.sha512file(dup)
			if hash1 == hash2:
				deleted_files = deleted_files + 1
				space_saved = space_saved + os.path.getsize(dup)
				print "[" + str(deleted_files) + "] Removing " + dup
				os.remove(dup)
print("Deleted " + str(deleted_files) + ", saving " + str(space_saved) + " bytes of space")
