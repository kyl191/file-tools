import db, hash, mp3, os, sys, re
def hashAndAdd(file):
	title, artist, album = mp3.getid3(file)
	tempfile = mp3.stripid3(file)
	hash = hash.sha512file(tempfile[1])
	os.close(tempfile[0])
	os.remove(tempfile[1])
	print title, artist, album
	print db.insertIntoDB(dbcursor, str(title), str(artist), str(album), hash, os.path.abspath(file))
	dbconn.commit()

os.chdir(sys.argv[1])
dbPath = "/home/kyl191/mp3dedup/mp3dedup.db"
dbconn = db.startDB(dbPath)
dbcursor = dbconn.cursor()
# I believe os.walk is a far more optimal implementation, just have to figure out how it works
#for root in os.walk('.'):
#	for dirs in root:
#		for files in dirs:
#			print files
files = []
for file in os.listdir("."):
	print file
	if re.search(".mp3",file):
		files.append(file)
		
for file in files:
	hashAndAdd(file)

dbcursor.close()
dbconn.commit()
