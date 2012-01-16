import db, hash, os, sys, re
from os.path import join
from collections import namedtuple
fileinfo = namedtuple('fileinfo', "hash filepath mtime")

def hashAndAdd(file):
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

# Initial setup of DB & search path
os.chdir(sys.argv[1])
compare = sys.argv[2]
#dbPath = "filededup.db"
#dbconn = db.startDB(dbPath)
#dbcursor = dbconn.cursor()

# If there's something wrong with the db, we should try & create it.
#try:
#	
#except Exception as e:
#	sql = """BEGIN TRANSACTION;
#CREATE TABLE filededup (
#    "id" INTEGER,
#    "hash" TEXT,
#    "filepath" TEXT,
#    "mtime" INTEGER
#);
#CREATE INDEX "path_index" on "filededup" (filepath ASC);
#CREATE INDEX "hash_index" on "filededup" (hash ASC);
#COMMIT;"""


# End initial setup

# Walk the directory structure
for root, subfolders, files in os.walk('.'):
	# Mention what path we're working in.
	print("Working in", os.path.abspath(root))
	# Since root contains the working folder, and we'll move onto subfolders later, 
	# We only care about the filename
	for filename in files:
		# If is does, hash & add it to the db
		#hashAndAdd(os.path.abspath(join(root,filename)))
		(filenameprefix, dot, filenamesuffix) = filename.rpartition(".")
		dup = filenameprefix + "_2." + filenamesuffix
		if os.path.exists(dup):
			hash1 = hash.sha512file(filename)
			hash2 = hash.sha512file(dup)
			if hash1 == hash2:
				print "Removing " + dup + "!"
				os.remove(dup)

# Close the cursor & commit the DB one last time just for good measure
#dbcursor.close()
#dbconn.commit()
