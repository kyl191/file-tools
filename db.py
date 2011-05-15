import sqlite3
def startDB(dbPath):
	try:
		conn = sqlite3.connect(dbPath)
		c = conn.cursor()
		c.execute("SELECT * from mp3dedup")
	except sqlite3.OperationalError, e:
		print "SQLite3 Error : Operational Error", e.args[0]
	except sqlite3.DatabaseError, e:
		print "SQLite3 Error : Database Error", e.args[0]
	except sqlite3.Error, e:
		print "SQLite 3: Unknown Error", e.args[0]
	except:
		print "Unknown Error"
	return c

def insertIntoDB(db,title,artist,album,hash,filepath):
	info = title, artist, album, hash, filepath
	try:
		db.execute("INSERT into mp3dedup VALUES (Null, ?, ?, ?, ?, ?)",info)
	except sqlite3.Error, e:
		print "SQLite 3: Unknown Error", e.args[0]
	return info
