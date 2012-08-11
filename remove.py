import os, shutil, sys, filecmp, glob, pprint, pickle
from os.path import join

source_dir = unicode(os.path.abspath(sys.argv[1]))
filedict={}
os.chdir(source_dir)
picklefile = "sizes.pypickle"
if os.path.exists(picklefile):
	filedict = pickle.load(open(picklefile, "rb"))
else:
	for root, subfolders, files in os.walk(source_dir):
		(null, path, pathsuffix) = root.rpartition(source_dir)
		# Mention what path we're working in.
		print("Working in", os.path.abspath(root))
		for filename in files:
			filename = os.path.abspath(os.path.join(root, filename))
			size = int(os.path.getsize(filename))
			try:
				filedict[size].extend([filename])
			except KeyError as e:
				filedict[size] = [filename]
for size in sorted(filedict):
	if len(filedict[size]) > 1:
		pprint.pprint(filedict[size])
		for filename in filedict[size]:
			filebase = os.path.splitext(os.path.split(filename)[1])[0]
			fileext = os.path.splitext(os.path.split(filename)[1])[1]
			#print(filename)
			fileglob = glob.glob(os.path.join(os.path.dirname(filename), filebase+"_2" + fileext))
			if len(fileglob) > 0:
				for file in fileglob:
					if filecmp.cmp(filename, file, shallow = False):
						print("removing", filename, "==>", file)
						os.remove(file)
pickle.dump(filedict, open(picklefile, 'wb'))
#pprint.pprint(sorted(filedict))
