import db, hash, mp3, os
dbPath = "/home/kyl191/mp3dedup/mp3dedup.db"
db = db.startDB(dbPath)
file = "test.mp3"
info = mp3.getid3(file)
hash = hash.sha512file(mp3.stripid3(file))
print db.insertIntoDB(db, info, hash, os.path.abspath(file))
