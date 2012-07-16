import os
from os.path import join, getsize

def rmdir(dir):
	compare_dir = unicode(dir)
	for root, subfolders, files in os.walk(compare_dir, topdown=False):
		# Delete 0-sized files. Assuming by default they're not necessary for anything,
		# i.e. not sentiel files
		for file in files:
			file = unicode(os.path.normpath(join(root,file)))
			if os.path.getsize(file) == 0 or file == u"Thumbs.db" or file == u"desktop.ini":
				os.remove(file)
		for folder in subfolders:
			if not os.listdir(join(root, folder)):
				os.rmdir(join(root, folder))