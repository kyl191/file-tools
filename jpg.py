from PIL import Image
import shutil
import tempfile
import os

def stripmetadata(file):
	temp = tempfile.NamedTemporaryFile(suffix = ".jpg", delete = False)
	try:
		Image.open(file).copy().save(temp.name)
	except IOError: 
		print("IOError processing" + file)
		temp.close()
		return False
	temp.close()
	return temp.name


