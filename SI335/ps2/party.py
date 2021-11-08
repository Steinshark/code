import random
import itertools
import copy
import pprint

def build_lists(f_s,e_s):
    F = [i for i in range(f_s)]
    E,E_a = make_enemies(F,e_s)
    return F, E, E_a

def make_enemies(F,e_s):
    enemies = []
    enemies_all = []
    for i in range(e_s):
        p1 = F[random.randint(0,len(F)-1)]
        p2 = F[random.randint(0,len(F)-1)]
        while p1 == p2:
            p2 = F[random.randint(0,len(F)-1)]
        enemies.append({p1,p2})

        if not p1 in enemies_all:
            enemies_all.append(p1)
        if not p2 in enemies_all:
            enemies_all.append(p2)
    return enemies, enemies_all

def compute_combinations(F,E,E_a):
    for i in range(1,len(E)+1):
        for comb in itertools.combinations(E_a,i):
            E_copy = copy.copy(E)
            #print(str(E_copy) + " vs " + str(comb))
            mark_del = []
            for x in comb:
                for y in E_copy:
                    if x in y:
                        mark_del.append(y)
            for x in mark_del:
                try:
                    E_copy.remove(x)
                except ValueError:
                    continue
            #print("yielded " + str(E_copy))
            if len(E_copy) == 0:
                return set(F) - set(comb)

def compute_elim(F,E,E_a):
    hater_pairs = {}
    removed = []
    we_have_seen = []
    for s in E:
        we_have_seen.append(s)

        x,y = s
        try:
            hater_pairs[x].append(y)
        except KeyError:
            hater_pairs[x] = [y]
        try:
            hater_pairs[y].append(x)
        except KeyError:
            hater_pairs[y] = [x]
    while conflicting(hater_pairs):
        hater_pairs, r = remove_max(hater_pairs)
        removed.append(r)
    #print("removed " + str(len(removed)) + "- "+ str(removed))
    return set(F) - set(removed)

def conflicting(h):
    big = []
    for x in h.keys():
        if x in big:
            return True
        big.append(x)
        for l in h[x]:
            if l in big:
                return True
            big.append(l)
    return False

def remove_max(h):
    max = list(h.keys())[0]
    ## Find who is preventing the most people from coming
    for k in h.keys():
        if len(h[k]) > len(h[max]):
            max = k
    ## remove them and solve every conflict that they create
    for k in h.keys():
        if max in h[k]:
            h[k].remove(max)
    del h[max]
    return h,max


F, E, E_a = build_lists(int(input("number of  Friends: ")),int(input("pairs of Enemies: ")))

print("E is " + str(E))
elim = str(set(F) - set(compute_elim(F,E,E_a)))
print("elimm removed" + str(len(F) - len(elim)) + " : " + elim)
brute = str(set(F) - set(compute_combinations(F,E,E_a)))

print("brute removed" + str(len(F) - len(brute)) + " : " + brute)
