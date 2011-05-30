from mutagen.id3 import ID3
import mutagen.id3
import shutil
import tempfile
import os

def stripid3(file):
	temp = tempfile.mkstemp()
	shutil.copyfile(file,temp[1])
	audio = ID3(temp[1])
	audio.delete()
	# Returns a *tuple* of the file reference & file path!
	# file *path* is temp[1]!
	return temp

def getid3(file):
	try:
		audio = ID3(file)
	except mutagen.id3.ID3NoHeaderError as e:
		raise Exception(file + " has no ID3 tag!")
	try:
		title = audio["TIT2"]
	except:
		title = "Unknown"
	try:
		artist = audio["TPE1"]
	except:
		artist = "Unknown"
	try:
		album = audio["TALB"]
	except:
		album = "Unknown"
	print str(title).decode('utf-8'), str(artist).decode('utf-8'), str(album).decode('utf-8')
	#return title,artist,album
	return str(title).decode('utf-8'), str(artist).decode('utf-8'), str(album).decode('utf-8')
