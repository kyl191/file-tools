import db, hash, os, shutil, sys, mp4, re, mp3, filecmp
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


# Close the cursor & commit the DB one last time just for good measure
#dbcursor.close()
#dbconn.commit()