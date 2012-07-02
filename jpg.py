from PIL import Image
import shutil
import tempfile
import os

def stripmetadata(file):
	temp = tempfile.mkstemp(".jpg")
	image = Image.open(file).copy().save(temp[1])
	# Returns a *tuple* of the file reference & file path!
	# file *path* is temp[1]!
	return temp


