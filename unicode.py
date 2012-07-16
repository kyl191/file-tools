import os, sys
from os.path import join, getsize

compare_dir = unicode(os.path.abspath(sys.argv[1]))
print(repr(compare_dir))
print("=======")

for root, subfolders, files in os.walk(compare_dir, topdown=False):
	# Delete 0-sized files. Assuming by default they're not necessary for anything,
	# i.e. not sentiel files
	for file in files:
		print("Unicode escaped names: ", join(root.encode('unicode_escape'),file.encode('unicode_escape')))
		file = join(root,file)
		file = unicode(os.path.normpath(file))
		print(repr(file))
		print("Filename", file.encode('mbcs'))
		print(os.stat(file))
		if os.path.getsize(file) == 0:
			os.remove(file)
	for folder in subfolders:
		if not os.listdir(join(root, folder)):
			os.rmdir(join(root, folder))
