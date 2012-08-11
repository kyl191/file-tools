import os, shutil, sys, filecmp, rmdir
from os.path import join

source_dir = unicode(os.path.abspath(sys.argv[1]))
compare_dir = unicode(os.path.abspath(sys.argv[2]))

for root, subfolders, files in os.walk(source_dir):
	(null, path, pathsuffix) = root.rpartition(source_dir)
	dup_folder = os.path.normpath(compare_dir + "/" + pathsuffix)
	# Mention what path we're working in.
	print("Working in", os.path.abspath(root))
	
	for filename in files:
		# Need to find some way to recurse directories in sync with src
		src = os.path.abspath(join(root,filename))
		dst = os.path.abspath(dup_folder + "/" + filename)
		
		# Merging files... but it looks as if we're moving from the first directory to the second, not the other way around
		# But it only runs if destination isn't a file.
		# Doesn't check for folders because we're looping through filenames
		if not os.path.isfile(dst):
			shutil.move(src, dst)
			print("Moved {0} to {1}").format(src, dst)
			
		else:
			# delete exact duplicates, otherwise merge directory contents by appending the file count to the filename and moving it.
			if filecmp.cmp(src, dst, shallow = False):
				print(src.encode('mbcs') + " and " + dst.encode('mbcs') + " are identical.")
				deleted_files = deleted_files + 1
				space_saved = space_saved + os.path.getsize(dup)
				print("[" + str(deleted_files) + "] Removing " + src.encode('mbcs'))
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

rmdir.rmdir(source_dir)

