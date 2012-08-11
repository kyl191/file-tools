import os, sys, shutil, re
dir = os.path.abspath(sys.argv[1])
regex = re.compile(r"(?:s=)(\d+)(?:.htm)")
existing = re.compile(r"^\d")
for root, subfolders, files in os.walk(dir):
	for folder in subfolders:
		if len(str.split(folder, " - ")) == 1:
			#print str.split(folder, " - ")
			curfolder = os.path.join(root, folder)
			for file in os.listdir(curfolder):
				if regex.search(file):
					number = regex.search(file).group(1)
					if int(number) > 1000:
						print os.path.join(root, folder), "== >", os.path.join(root, number + " - " + folder)
						os.rename(os.path.join(root, folder), os.path.join(root, number + " - " + folder))
