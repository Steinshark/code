import random
import string

#essentially the main
def run(names,root):
    #map already-seen names
    already_run = {}
    # keep track of name counts
    count = {}
    for name in names:
        # only add to count on an already seen name
        if name in already_run:
            if already_run[name]:
                count[name] += 1
        # if name is new, perform a check and update the count
        else:
            already_run[name] = isSimilar(name,root)
            if already_run[name]:
                count[name] = 1
    sum = 0
    # calculate the mispeleability
    for name in count.keys():
        if not name == root:
            if not count[name] >= count[root]:
                sum += count[name]
    return round(100*(sum/count[root]))

# simply Similarity calculator
def isSimilar(name,name2):
    if name == name2:
        return True

    # check that we are at most one letter away before continuing
    if abs(len(name)-len(name2)) <= 1:
        # check if a letter switch will match
        if len(name) == len(name2):
            fails = 0
            for i in range(0,len(name2)):
                if not name2[i] == name[i]:
                    fails += 1
                if fails > 1:
                    return False
            return True
        # check if an insert or delete will match
        else:
            # swap so that name2 is shorter
            if len(name2) == (len(name) + 1):
                temp = name2
                name2 = name
                name = temp
            # save some time with these quick checks
            if name[:-1] == name2:
                return True
            if name2 == name[1:]:
                return True
            #compare until first discrepency
            first_break = 0
            for i in range(0,len(name)):
                letter = name[i]
                try:
                    if not letter == name2[i]:
                        first_break = name.index(letter)
                        break
                except IndexError:
                    return False
            #move past mismatch and continue to check the rest is equal
            first_break += 1
            for i in range(first_break,len(name)):
                letter = name[i]
                if not letter == name2[i-1]:
                    return False
            # if we made it this far then were good to go
            return True
    return False

if __name__ == '__main__':
    print(run([name.rstrip().lower() for name in open(str(input("File: ")),'r').readlines()],str(input("Name: ")).lower()))
