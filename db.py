import sqlite3
def startDB(dbPath):
	try:
		conn = sqlite3.connect(dbPath)
		conn.text_factory = unicode
		c = conn.cursor()
		c.execute("SELECT * from filededup")
	except sqlite3.OperationalError as e:
		print("SQLite3 Error : Operational Error", e.args[0])
	except sqlite3.DatabaseError as e:
		print("SQLite3 Error : Database Error", e.args[0])
	except sqlite3.Error as e:
		print("SQLite 3: Unknown Error", e.args[0])
	except Exception as e:
		print("Unknown Error", e)
	return conn

def insertIntoDB(db, info):
	# info = title, artist, album, hash, filepath, mtime
	try:
		db.execute(u"INSERT into filededup VALUES (Null, ?, ?, ?, ?, ?, ?)",info)
	except sqlite3.Error as e:
		print("SQLite 3: Unknown Error", e.args[0])
	return info

def checkIfExists(db,filepath):
	try:
		(results,) = db.execute(u"SELECT COUNT(*) from filededup WHERE filepath = ?",[filepath])
	except sqlite3.Error as e:
		print("SQLite 3: Unknown Error", e.args[0])
	else:
		if results[0] > 0:
			(mtime,) = db.execute(u"SELECT mtime from filededup WHERE filepath = ?",[filepath])
			return (results[0],mtime[0])
		else:
			return (0, -1)
def updateDB(db, info):
	# info = hash, filepath, mtime
	try:
		db.execute(u"UPDATE filededup set hash = :hash, mtime = :mtime where filepath = :path",
			{"hash":info.hash, "mtime":info.mtime, "path":info.filepath})
	except sqlite3.Error as e:
		print("SQLite 3: Unknown Error", e.args[0])
	return info

def createDB(db):
	sql = """BEGIN TRANSACTION;
CREATE TABLE filededup (
    "id" INTEGER,
    "hash" TEXT,
    "strippedhash" TEXT,
    "filepath" TEXT,
    "mtime" INTEGER
);
CREATE INDEX "path_index" on "filededup" (filepath ASC);
CREATE INDEX "hash_index" on "filededup" (hash ASC);
CREATE INDEX "strippedhash_index" on "filededup" (strippedhash ASC);
COMMIT;"""
	try:
		db.execute(sql)
	except sqlite3.Erroras e:
		print("SQLite 3: Unknown Error", e.args[0])
