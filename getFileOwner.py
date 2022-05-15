#! python3.9 
import subprocess
from sys import argv, stderr

# FileInfo stores the file name, owner, and if it a folder 
class FileInfo:
	def __init__(self, name, owner, isDir=None):
		self.name = name
		self.owner = owner
		self.isDir = isDir
	def getName(self):
		return self.name
	def getOwner(self):
		return self.owner
	def isADir(self):
		return self.isDir

# Returns a list of FileInfo objects for the files/folders in the dir
def get_owners_of_files_in_dir(dir):
	sp = subprocess.run(["dir", "/og", "/on", "/q", dir], capture_output=True, shell=True)
	full = str(sp.stdout).split("Directory of")[-1].split("\\r\\n")
	for i in [0,0,-1,-1,-1]:
		full.pop(i)
	files = []
	for line in full:
		info = line.replace("NT ","NT_").replace("\\TrustedInsta", "\\TrustedInsta ").split()
		if len(info) < 6:
			continue
		try:
			if info[-1].strip() != "." and info[-1].strip() != "..":
				owner = info[4].split('\\')[-1]
				name = ""
				for i in range(5,len(info)):
					name = name + ' ' + info[i]
				if info[3] == "<DIR>":
					files.append(FileInfo(name.strip(), owner, isDir=True))
				else:
					files.append(FileInfo(name.strip(), owner))
		except IndexError:
			print("ERROR: Not enough info in:\n\t{{{}}}".format(info), file=stderr)
			continue
	return files

# Print the list made by get_owners_of_files_in_dir()
def displayFiles(files):
	if len(files) > 0:
		import os
		mWidth = 0
		if max(len(f.getOwner()) for f in files) != sum(len(f.getOwner()) for f in files)/len(files) and \
			min([max([max(len(f.getOwner()) for f in files), max(len(f.getName()) for f in files)]), (os.get_terminal_size().columns)/2]) != \
				max([max(len(f.getOwner()) for f in files), max(len(f.getName()) for f in files)]):
			mWidth = max([max(len(f.getOwner()) for f in files), max(len(f.getName()) for f in files)])
			print("{}{}{}".format("Owner".ljust(mWidth),"".ljust(mWidth), "File/Folder"))
			for i in range(mWidth+1):
				print("---", end='')
				if i == mWidth:
					print('')
		else:
			mWidth = max(len(f.getOwner()) for f in files)+2
			width = min([max([max(len(f.getOwner()) for f in files), max(len(f.getName()) for f in files)]), (os.get_terminal_size().columns)/2])
			print("{}{}{}".format("Owner".ljust(mWidth),"".ljust(mWidth), "File/Folder"))
			for i in range(width + mWidth +9):
				print("-", end='')
				if i == width + mWidth +8:
					print('')
		for f in files:
			owner = f.getOwner().ljust(mWidth)
			if f.isADir():
				print("{}{}[{}]".format(owner, "".ljust(mWidth), f.getName()))
			else:
				print("{}{}{}".format(owner, "".ljust(mWidth), f.getName()))
	else:
		print("There are no files/folders at this location.")

if __name__ == "__main__":
	if len(argv) > 1:
		dir = argv[1]
		if dir == './' or dir == "../":
			dir = argv[1].replace('/','')
		files = get_owners_of_files_in_dir(dir)
		displayFiles(files)
	else:
		displayFiles(get_owners_of_files_in_dir("."))