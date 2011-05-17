import db, hash, mp3, os, sys, re
from os.path import join
def hashAndAdd(file):
	title, artist, album = mp3.getid3(file)
	tempfile = mp3.stripid3(file)
	hashresult = hash.sha512file(tempfile[1])
	os.close(tempfile[0])
	os.remove(tempfile[1])
	print title, artist, album
	print db.insertIntoDB(dbcursor, str(title), str(artist), str(album), hashresult, os.path.abspath(file))
	dbconn.commit()

# Initial setup of DB & search path
os.chdir(sys.argv[1])
dbPath = "/home/kyl191/mp3dedup/mp3dedup.db"
dbconn = db.startDB(dbPath)
dbcursor = dbconn.cursor()
# End initial setup

for root, dirs, files in os.walk('.'):
	for filename in files:
		print os.path.abspath(join(root,filename))
		if re.search(".mp3",filename):
			hashAndAdd(os.path.abspath(join(root,filename)))
			print "found MP3 file: ", os.path.abspath(join(root,filename))

# Close the cursor & commit the DB one last time just for good measure
dbcursor.close()
dbconn.commit()
