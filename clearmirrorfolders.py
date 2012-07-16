import hash, os, sys, re, shutil, jpg, filecmp, rmdir
from os.path import join, getsize

source_dir = unicode(os.path.abspath(sys.argv[1]))
compare_dir = unicode(os.path.abspath(sys.argv[2]))
deleted_files = 0
space_saved = 0
testing = False
debug = True
for root, subfolders, files in os.walk(source_dir):
	# Since root contains the working folder, and we'll move onto subfolders later, 
	# We only care about the filename
	(null, path, pathsuffix) = root.rpartition(source_dir)
	dup_folder = os.path.normpath(compare_dir + "/" + pathsuffix)
	# Mention what path we're working in.
	print("Comparing: " + os.path.abspath(root).encode('mbcs'))
	if os.path.exists(dup_folder):
		print("To: " + os.path.abspath(dup_folder).encode('mbcs'))
		for filename in files:
			dup = os.path.abspath(dup_folder + "/" + filename)
			filename = join(root,filename)
			if os.path.exists(dup):
				"""hash1 = hash.sha512file(filename)
				hash2 = hash.sha512file(dup)
				if debug:
					print os.path.abspath(filename).encode('unicode_escape') + ": \n" + hash1
					print os.path.abspath(dup).encode('unicode_escape') + ": \n" + hash2"""
				if filecmp.cmp(filename, dup, shallow = False):
					print(filename.encode('unicode_escape') + " and " + dup.encode('unicode_escape') + " are identical.")
					deleted_files = deleted_files + 1
					space_saved = space_saved + os.path.getsize(dup)
					print("[" + str(deleted_files) + "] Removing " + dup.encode('unicode_escape'))
					if not testing:
						os.remove(dup)
				elif re.search(".jpg",filename,re.IGNORECASE):
					# stripmetadata returns an empty file if opening the image fails!
					# Problem because then it's picked up as metadata differing...
					tempsrc = jpg.stripmetadata(filename)
					tempdup = jpg.stripmetadata(dup)
					"""hash1 = hash.sha512file(tempsrc)
					hash2 = hash.sha512file(tempdup)
					if debug:
						print(os.path.abspath(filename) + " (Stripped): \n" + hash1)
						print(os.path.abspath(dup) + " (Stripped): \n" + hash2)"""
					if filecmp.cmp(tempsrc, tempdup, shallow = False):
						print(filename + " and " + dup + " differ by metadata, but contents are the same.")
						deleted_files = deleted_files + 1
						space_saved = space_saved + os.path.getsize(dup)
						print("[" + str(deleted_files) + "] Removing " + dup)
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
print("Wiping empty folders")
rmdir.rmdir(compare_dir)
print("Deleted " + str(deleted_files) + ", saving " + str(space_saved) + " bytes of space")
