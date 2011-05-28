import db, hash, mp3, os, sys, re
from os.path import join
from collections import namedtuple
mp3info = namedtuple('mp3info', "title artist album hash filepath mtime")

def hashAndAdd(file):
	# Check if it's a valid MP3 file first by trying to get the ID3 info
	try:
		title, artist, album = mp3.getid3(file)
	except Exception as e:
		# So far the only exception is an invalid ID3 header found, so not much to grab
		print e
		return
	mtime = os.path.getmtime(file)
	exists = db.checkIfExists(dbcursor, os.path.abspath(file))
	print exists, file
	tempfile = mp3.stripid3(file)
	hashresult = hash.sha512file(tempfile[1])
	os.close(tempfile[0])
	os.remove(tempfile[1])
	info = mp3info(str(title), str(artist), str(album), hashresult, os.path.abspath(file), mtime)
	if not update:
		db.insertIntoDB(dbcursor, info)
	else:
		db.updateDB(dbcursor, info)
	dbconn.commit()

# Initial setup of DB & search path
os.chdir(sys.argv[1])
dbPath = "/home/kyl191/mp3dedup/mp3dedup.db"
dbconn = db.startDB(dbPath)
dbcursor = dbconn.cursor()
# End initial setup

# Walk the directory structure looking for MP3 files
for root, subfolders, files in os.walk('.'):
	# Mention what path we're working in.
	print "Working in", os.path.abspath(root)
	# Since root contains the working folder, and we'll move onto subfolders later, 
	# We only care about the filename
	for filename in files:
		# So, for each file, check if it has an MP3 extension
		if re.search(".mp3",filename,re.IGNORECASE):
			# If is does, hash & add it to the db
			hashAndAdd(os.path.abspath(join(root,filename)))
			#print "found MP3 file: ", os.path.abspath(join(root,filename))

# Close the cursor & commit the DB one last time just for good measure
dbcursor.close()
dbconn.commit()
