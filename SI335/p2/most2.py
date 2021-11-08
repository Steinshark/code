from singleR2 import *
import time
import copy

def most():
    #Import file
    filename = str(input("File: "))
    count = int(input("Count: "))
    names = [name.rstrip() for name in open(filename, "r").readlines()]
    #Init lists, dicts, etc...
    distincts = []
    counts = {}
    pairs = {}
    mispeleability = {}
    c= 0
    time1 = time.time()

    for name in names:
        try:
            counts[name] += 1
        except KeyError:
            distincts.append(name)
            counts[name] = 1
            pairs[name] = []

    size = len(distincts)
    searchList = copy.copy(distincts)

    #Pair search
    for name in distincts:
        mispeleability[name], returned = run(searchList,name, counts)
        for key in returned:
            pairs[key].append(name)
        searchList.remove(name)

    highest = []
    for i in range(0,count):
        max_num = 0
        max_item = None
        for key in mispeleability.keys():
            if mispeleability[key] > max_num:
                max_num = mispeleability[key]
                max_item = key
        highest.append((max_item,max_num))
        mispeleability.pop(max_item)

    print("solved in " + str(time.time()-time1))
    for name, count in highest:
        print(str(name) + " " + str(count))


most()
