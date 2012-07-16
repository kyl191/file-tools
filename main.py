import db, hash, os, shutil, sys, mp4, re
from os.path import join
from collections import namedtuple
fileinfo = namedtuple('fileinfo', "hash filepath mtime")

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
	return hashresult

def hashAndAdd(file):
	#hashAndAdd(os.path.abspath(join(root,filename)))
	mtime = os.path.getmtime(file)
	(exists,dbmtime) = db.checkIfExists(dbcursor, unicode(str(os.path.abspath(file)).decode('utf-8')))
	update = False
	# Gets back a tuple with (count of rows, mtime)
	# Check if the file has already been hashed
	if exists > 0:
		# If the file hasn't been modified since it was checked, don't bother hashing it
		if dbmtime >= mtime:
			return
		else:
			# Need to come up with an update statement...
			print("Updating", file)
			update = True
	hashresult = hash.sha512file(file)
	info = fileinfo(unicode(hashresult), unicode(str(os.path.abspath(file)).decode('utf-8')), mtime)
	if not update:
		print(info,"Ins")
		db.insertIntoDB(dbcursor, info)
	else:
		print(info,"upd")
		db.updateDB(dbcursor, info)
	dbconn.commit()

#dbPath = "filededup.db"
#dbconn = db.startDB(dbPath)
#dbcursor = dbconn.cursor()

os.chdir(sys.argv[1])
compare = sys.argv[2]

for root, subfolders, files in os.walk(sys.argv[1]):
	# Mention what path we're working in.
	print("Working in", os.path.abspath(root))
	
	
	for filename in files:
	
		# Dup files in *ONE* directory
		# eg. filename.ext and filename 1.ext
		(filenameprefix, dot, filenamesuffix) = filename.rpartition(".")
		dup = filenameprefix + "_2." + filenamesuffix
		if os.path.exists(dup):
			hash1 = hash.sha512file(filename)
			hash2 = hash.sha512file(dup)
			if hash1 == hash2:
				print "Removing " + dup + "!"
				os.remove(dup)
		
		# Need to find some way to recurse directories in sync with src
		src = os.path.abspath(join(root,filename))
		dst = os.path.abspath(join(sys.argv[2],filename))
		# Merging files... but it looks as if we're moving from the first directory to the second, not the other way around
		if not os.path.isfile(dst):
			shutil.move(src, dst)
			print("Moved {0} to {1}").format(src, dst)
		
		else:
			# should be standard hash first, then metadata stripping
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

# Close the cursor & commit the DB one last time just for good measure
#dbcursor.close()
#dbconn.commit()
