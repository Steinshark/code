from single import *

def most():
    filename = str(input("File: "))
    count = int(input("Count: "))
    names = [name.rstrip() for name in open(filename, "r").readlines()]

    distincts = {}
    mispeleability = {}
    c= 0
    for name in names:
        c += 1
        if (c%100) == 0:
            print(str(c) + " out of " + str(len(names)))
        if name in distincts:
            continue
        else:
            distincts[name] = True
            mispeleability = run(names,name)

    highest = []
    for x in range(0,count):
        max = 0
        max_item = None
        for x in distincts:
            if distincts[x] > max:
                if not (x,distincts[x]) in highest:
                    max_item = x
                    max = distincts[x]
        highest.append((max_item,max))
        print((max_item,max))

def scratch():
    filename = str(input("File: "))
    names = [name.rstrip() for name in open(filename, "r").readlines()]

    counts = {}
    for name in names:
        try:
            counts[name] += 1
        except KeyError:
            counts[name] = 1

    distincts = {}
    mispeleability = {}
    c = 0
    size = len(counts.keys())
    for name in counts.keys():
        c += 1
        if (c%100) == 0:
            print(str(c) + " out of " + str(size))
        mispeleability = run(names,name)
    print(str(len(counts)) + " distinct entries of " + str(len(names)))
    print("done")


scratch()
