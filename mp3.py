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

file = "test.mp3"
test = stripid3(file)
print test[1]
os.close(test[0])
os.remove(test[1])
