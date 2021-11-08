file= open("names.txt","r")
names = []
for line in file.readlines():
	names.append(line)
