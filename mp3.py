from mutagen.id3 import ID3
import shutil
import tempfile
import os

def stripid3(file):
	temp = tempfile.mkstemp()
	shutil.copyfile(file,temp[1])
	audio = ID3(temp[1])
	audio.delete()
	# Returns a *tuple* of the file reference & file path!
	return temp

def getid3(file):
	audio = ID3(file)
	title = audio["TIT2"]
	artist = audio["TPE1"]
	album = audio["TALB"]
	return title,artist,album

file = "test.mp3"
title, artist, album = getid3(file)
test = stripid3(file)
#print test[1]
#print title, ":", artist, ":" , album
os.close(test[0])
os.remove(test[1])
