import db, hash, mp3, os, sys
print sys.argv
os.chdir(sys.argv[1])
dbPath = "/home/kyl191/mp3dedup/mp3dedup.db"
dbconn = db.startDB(dbPath)
dbcursor = dbconn.cursor()
for root, dirs, files in os.walk('.'):
	print root, dirs, files
for file in os.listdir("."):
	print file
title, artist, album = mp3.getid3(file)
tempfile = mp3.stripid3(file)
hash = hash.sha512file(tempfile[1])
os.close(tempfile[0])
os.remove(tempfile[1])
print title, artist, album
print db.insertIntoDB(dbcursor, str(title), str(artist), str(album), hash, os.path.abspath(file))
dbcursor.close()
dbconn.commit()
