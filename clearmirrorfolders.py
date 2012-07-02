import hash, os, sys, re, shutil, jpg
from os.path import join, getsize

source_dir = os.path.abspath(sys.argv[1])
compare_dir = os.path.abspath(sys.argv[2])
deleted_files = 0
space_saved = 0
testing = True
debug = True
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
			if debug:
				print os.path.abspath(filename) + ": \n" + hash1
				print os.path.abspath(dup) + ": \n" + hash2
			if hash1 == hash2:
				print filename + " and " + dup + " are identical."
				deleted_files = deleted_files + 1
				space_saved = space_saved + os.path.getsize(dup)
				print "[" + str(deleted_files) + "] Removing " + dup
				if not testing:
					os.remove(dup)
			elif re.search(".jpg",filename,re.IGNORECASE):
				tempsrc = jpg.stripmetadata(filename)
				tempdup = jpg.stripmetadata(dup)
				hash1 = hash.sha512file(tempsrc)
				hash2 = hash.sha512file(tempdup)
				if debug:
					print os.path.abspath(filename) + " (Stripped): \n" + hash1
					print os.path.abspath(dup) + " (Stripped): \n" + hash2
				if hash1 == hash2:
					print  filename + " and " + dup + " differ by metadata, but contents are the same."
					deleted_files = deleted_files + 1
					space_saved = space_saved + os.path.getsize(dup)
					print "[" + str(deleted_files) + "] Removing " + dup
					if not testing:
						os.remove(dup)
				os.remove(tempsrc)
				os.remove(tempdup)
	# Merge files that are in the dup folder but aren't in the source folder
	# Skip the folder if it's not present in the dup folder but *is* in the source folder
	if os.path.exists(dup_folder):
		dup_folder_files = os.listdir(dup_folder)
		for file in dup_folder_files:
			# To keep things somewhat simple for the copying,
			# src_path is the dup folder, and dst_path is the primary folder
			src_path = os.path.abspath(join(dup_folder, file))
			dst_path = os.path.abspath(join(root, file))
			#print src_path, "-->", dst_path
			if not os.path.exists(dst_path):
				#shutil.move(src_path, dst_path)
				#print "Moved " + src_path + " to " + dst_path
				pass
for root, subfolders, files in os.walk(compare_dir, topdown=False):
	# Delete 0-sized files. Assuming by default they're not necessary for anything,
	# i.e. not sentiel files
	for file in files:
		if os.path.getsize(join(root,file)) == 0:
			os.remove(join(root,file))
	for folder in subfolders:
		if not os.listdir(join(root, folder)):
			os.rmdir(join(root, folder))
print("Deleted " + str(deleted_files) + ", saving " + str(space_saved) + " bytes of space")
