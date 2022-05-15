#! python3.9 
import subprocess
from sys import argv, stderr

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

def get_owners_of_files_in_dir(dir):
	sp = subprocess.run(["dir", "/og", "/on", "/q", dir], capture_output=True, shell=True)
	full = str(sp.stdout).split("Directory of")[-1].split("\\r\\n")
	for i in [0,0,-1,-1,-1]:
		full.pop(i)
	files = []
	for line in full:
		info = line.replace("NT ","NT_").split()
		if len(info) < 6:
			#print("ERROR: Not enough info in:\n\t{{{}}}".format(line), file=stderr)
			continue
		try:
			if info[-1].strip() != "." and info[-1].strip() != "..":
				owner = info[4].split('\\')[-1]
				name = info[5]
				if info[3] == "<DIR>":
					files.append(FileInfo(name,owner,isDir=True))
				else:
					files.append(FileInfo(name,owner))
		except IndexError:
			print("ERROR: Not enough info in:\n\t{{{}}}".format(info), file=stderr)
			continue
	return files

def displayFiles(files):
	mWidth = max([max(len(f.getOwner()) for f in files), max(len(f.getName()) for f in files)])
	print("{}{}{}".format("Owner".ljust(mWidth),"".ljust(mWidth), "File/Folder"))
	for i in range(mWidth+1):
		print("---", end='')
		if i == mWidth:
			print('')
	for f in files:
		owner = f.getOwner().ljust(mWidth)
		if f.isADir():
			print("{}{}[{}]".format(owner, "".ljust(mWidth), f.getName()))
		else:
			print("{}{}{}".format(owner, "".ljust(mWidth), f.getName()))

if __name__ == "__main__":
	#print(argv)
	if len(argv) > 1:
		dir = argv[1]
		if dir == '.' or dir == ".\\":
			dir = argv[0].replace(argv[0].split('\\')[-1],'')
		files = get_owners_of_files_in_dir(dir)
		displayFiles(files)
		
	else:
		#files = get_owners_of_files_in_dir(argv[0].replace(argv[0].split('\\')[-1],''))
		displayFiles(get_owners_of_files_in_dir("."))