from PIL import Image
import shutil
import tempfile
import os

def stripmetadata(file):
	temp = tempfile.NamedTemporaryFile(suffix = ".jpg", delete = False)
	Image.open(file).copy().save(temp.name)
	temp.close()
	return temp.name


