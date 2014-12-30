import mp4, hash, os, sys, re
from os.path import join, getsize

def hashMP4(filename):
  file = open(filename, 'rb')
  try:
    mp4.isMP4(file)
  except Exception as e:
    # So far the only exception is an invalid MP4 header found, so not much to grab
    print(e)
  tempfile = mp4.stripMetadata(file)
  #print os.path.exists(tempfile.name)
  hashresult = hash.sha512file(tempfile.name)
  #print hashresult
  #print tempfile
  tempfile.close()
  os.remove(tempfile.name)
  return hashresult

source_dir = os.path.abspath(sys.argv[1])
compare_dir = os.path.abspath(sys.argv[2])
deleted_files = 0
space_saved = 0
for root, subfolders, files in os.walk(source_dir):
  # Since root contains the working folder, and we'll move onto subfolders later,
  # We only care about the filename
  (null, path, pathsuffix) = root.rpartition(source_dir)
  dup_folder = os.path.normpath(compare_dir + "/" + pathsuffix)
  # Mention what path we're working in.
  print("Comparing: %s" % os.path.abspath(root).encode("utf-8"))
  print("To: %s" % os.path.abspath(dup_folder).encode("utf-8"))
  for filename in files:
    # If is does, hash & add it to the db
    #hashAndAdd(os.path.abspath(join(root,filename)))
    dup = os.path.abspath(dup_folder + "/" + filename)
    filename = join(root,filename)
    if os.path.exists(dup):
      if re.search(".m4a",os.path.splitext(filename)[1],re.IGNORECASE) and re.search(".m4a",os.path.splitext(dup)[1],re.IGNORECASE):
        hash1 = hashMP4(filename)
        hash2 = hashMP4(dup)
      else:
        hash1 = hash.sha512file(filename)
        hash2 = hash.sha512file(dup)
      if hash1 == hash2:
        print("%s:\n %s" % (os.path.abspath(filename).encode("utf-8"), hash1))
        print("%s:\n %s" % (os.path.abspath(dup).encode("utf-8"), hash2))
        deleted_files = deleted_files + 1
        space_saved = space_saved + os.path.getsize(dup)
        print("[%s] Removing %s" % (str(deleted_files), dup.encode("utf-8")))
        os.remove(dup)
  if os.path.exists(dup_folder) and not os.listdir(dup_folder):
    os.rmdir(dup_folder)
print("Deleted " + str(deleted_files) + ", saving " + str(space_saved) + " bytes of space")
