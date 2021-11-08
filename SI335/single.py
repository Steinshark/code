import random
import string

def run(names,root):
    matches = []
    counts = {}
    name_list = []
    dinq_list = {}
    for name in names:
        if name in dinq_list:
            continue
        else:
            dinq_list[name] = True
            if isOneAwayFrom(name,root):
                try:
                    counts[name] += 1
                except KeyError:
                    counts[name] = 1
    return round(((sum(counts.values())-counts[root]) / counts[root])*100)

def run_better(names,root,preprocessed_pairs):
        matches = []
        counts = {}
        processed_names = {}
        for name in names:
            if not name in processed_names:
                processed_names[name] = isOneAwayFrom(name,root)
                if processed_names[name]:
                    processed_names[name+root] = True
                    counts[name] = 1
            else:
                if processed_names[name]:
                    counts[name] += 1
        return round(((sum(counts.values())-counts[root]) / counts[root])*100), preprocessed_pairs


def isOneAwayFrom(name,name2):
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
            # save some time with this quick check
            if name2[:-1] == name:
                return True
            name2_letter = 0
            name_letter = 0
            # check if they match until the first time they dont. THey are allowed to not match once
            while name2[name2_letter] == name[name_letter]:
                name2_letter += 1
                name_letter += 1
                if name2_letter >= len(name2):
                    return True
            # increment the longer one past the mismatch
            name_letter += 1
            #continue to check that the remaining letters match
            while name2[name2_letter] == name[name_letter]:
                name2_letter += 1
                name_letter += 1
                # if we reach the end of the word while were still matching, we're good
                if name2_letter >= len(name2):
                    return True
            return False
    else:
        return False

if __name__ == '__main__':
    print(run([name.rstrip() for name in open(str(input("File: ")),'r').readlines()],str(input("Name: "))))
