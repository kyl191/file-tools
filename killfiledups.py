import os, sys, filecmp, rmdir, glob, mp3, re
from os.path import join, getsize

source_dir = unicode(os.path.abspath(sys.argv[1]))
deleted_files = 0
space_saved = 0
testing = False
debug = True
for root, subfolders, files in os.walk(source_dir):
	# Mention what path we're working in.
	print("Working in: " + os.path.abspath(root).encode('mbcs'))
	for dup in glob.glob(root + "/* [0-9].*"):
		print("Looking at " + dup)
		dup = join(root, dup)
		(filebase, fileext) = os.path.splitext(dup)
		# Ignore the space and extension - we 
		filebase = filebase.rpartition(" ")[0]
		filename = os.path.abspath(join(root, filebase + fileext))
		if os.path.exists(filename):
			# VS using filecmp
			if filecmp.cmp(filename, dup, shallow = False):
				print(filename.encode('mbcs') + " and " + dup.encode('mbcs') + " are identical.")
				deleted_files = deleted_files + 1
				space_saved = space_saved + os.path.getsize(dup)
				print("[" + str(deleted_files) + "] Removing " + dup.encode('mbcs'))
				if not testing:
					os.remove(dup)
			# striping metadata & recomparing
			elif re.search(".mp3",filename,re.IGNORECASE):
				# stripmetadata returns an empty file if opening the image fails!
				# Problem because then it's picked up as metadata differing...
				srcinfo = mp3.getid3(filename)
				dupinfo = mp3.getid3(dup)
				print("Comparing metadata for ", srcinfo, dupinfo, srcinfo == dupinfo)
				if srcinfo == dupinfo:
					print("Stripped metadata for ", filename, dup)
					tempsrc = mp3.stripid3(filename)
					tempdup = mp3.stripid3(dup)
					if filecmp.cmp(tempsrc, tempdup, shallow = False):
						print(filename + " and " + dup + " differ by metadata, but contents are the same.")
						deleted_files = deleted_files + 1
						space_saved = space_saved + os.path.getsize(dup)
						print("[" + str(deleted_files) + "] Removing " + dup)
						if not testing:
							os.remove(dup)
					os.remove(tempsrc)
					os.remove(tempdup)
print("Wiping empty folders")
rmdir.rmdir(source_dir)
print("Deleted " + str(deleted_files) + ", saving " + str(space_saved) + " bytes of space")
