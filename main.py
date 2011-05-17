import db, hash, mp3, os, sys, re
from os.path import join
def hashAndAdd(file):
	title, artist, album = mp3.getid3(file)
	tempfile = mp3.stripid3(file)
	hashresult = hash.sha512file(tempfile[1])
	os.close(tempfile[0])
	os.remove(tempfile[1])
	#print db.insertIntoDB(dbcursor, str(title), str(artist), str(album), hashresult, os.path.abspath(file))
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
