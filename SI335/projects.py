import copy
import random
import time
import matplotlib.pyplot as plt
import numpy

def meetings(size):
    number_of_ppl = size
    group = [x for x in range(0,number_of_ppl)]
    meetings = []
    ## cost of nC2
    for person in group:
        number = person
        personnel = [(number,x) for x in range(group.index(person) + 1,len(group))]
        for meeting in personnel:
            meetings.append(meeting)

    minutes = 0
    remaining = []
    swaps_made = []
    iteration = 0
    while not len(meetings) == 0:
        time1 = time.time()
        #print("iter " + str(iteration := iteration + 1),end= ': start ' + str(len(meetings)) + " made ")
        meets = build_session_meetings(meetings)
        remaining.append(len(meetings))
        swaps_made.append(len(meets))
        iteration += 1
        #print("minute " + str(minutes := minutes + 1) + "\twith " + str(len(meets)) + "\tmeetings" + "\tand " + str(len(meetings)) + "\tremaining")
    return iteration, size

def run_meetings(max):
    fig, axs = plt.subplots(6,6)
    run_tuples = []
    for i in range(1,max):
        sizes, times = meetings(i*10)
        x = (i-1)//6
        y = (i-1) % 6
        axs[x,y].plot(sizes,times,"o",markersize=4)
        axs[x,y].set_title("size " + str(i*10))
        #print("generated plot ("+ str(x) + "," + str(y) + ")")
    plt.show()

def run_all(upto):
    x= []
    y= []
    for i in range(1,upto):
        minutes, size = meetings(i)
        x.append(size)
        y.append(minutes)
    plt.plot(x,y,"o",markersize=4)
    plt.show()


def build_session_meetings(meetings):
    meet_copy = copy.copy(meetings)
    found_a_meeting = True
    meetings_to_happen = []
    while not len(meet_copy) == 0:
        person1,person2 = meet_copy[0]
        meetings.remove(meet_copy[0])
        meetings_to_happen.append(copy.copy(meet_copy[0]))
        meet_copy = remove_instances_of(person1,person2,meet_copy)
    #print(len(meetings_to_happen))
    return meetings_to_happen
def remove_instances_of(p1,p2,list):
    dinq_list = []
    for item in list:
        #person1,person2 = item
        #if person1 == p1 or person1 == p2 or person2 == p1 or person2 == p2:
        if p1 in item or p2 in item:
            dinq_list.append(item)
    for item in dinq_list:
        list.remove(item)
    return list

def coastalSearch(num):
    miles_traveled = 0
    our_location = 0
    limit = 1
    factor = 2

    port_location = num
    found = False
    while not found:
        if limit < 0:
            while not our_location < limit:
                our_location -= 1
                miles_traveled += 1
                if our_location == port_location:
                    #print("traveled " + str(miles_traveled))
                    return miles_traveled

        elif limit > 0:
            while not our_location > limit:
                our_location += 1
                miles_traveled += 1
                if our_location == port_location:
                    #print("traveled " + str(miles_traveled))
                    return miles_traveled
        limit = limit*-2

def test():
    domain = numpy.arange(0,20000)
    actual = []
    for factor in domain:
        runs = []
        actual.append(coastalSearch(factor))
        if (factor%1000) == 0:
            print("*",end='',flush=True)

    plt.plot(domain,actual,'o',markersize=4,label="graph")
    plt.show()
    input()

def count(A, x):
    '''Returns the number of times x occurs in A'''
    c = 0
    for a in A:
        if a == x:
            c += 1
    return c
def popular_better(A):
    '''Returns all elements that occur more than n/3 times'''
    if len(A) <= 1:
        return A
    else:
        mid = len(A) // 2
        B = A[0 : mid]
        C = A[mid: len(A)]
        apop = []
        for x in popular_better(B):
            if count(A,x) > len(A)/3:
                apop.append(x)
        for x in popular_better(C):
            if x not in apop and count(A,x) > len(A)/3:
                apop.append(x)
        return apop

def popular_basic(A):
    '''Returns all elements that occur more than n/3 times'''
    apop = []
    for x in A:
        if count(A, x) > len(A)/3:
            apop.append(x)
    return apop




import math


#to reduce unneeded if checks, just make the people 1 and up
def pop(list):
    popular = [None,None]
    hash = dict()

    people = list

    for i in people:
        if i in hash:
            hash[i] +=1
        else:
            hash[i] = 1

        #this loop is actually constant run time, only operates 2x
        for j in range(len(popular)):
            if popular[j] == None and i not in popular:
                popular[j] = i
                break
            else:
                try:
                    if hash[i] > hash[popular[j]] and i not in popular:
                        popular[j] = i
                        break
                except KeyError:
                    continue
    greater = []
    #only ever runs twice
    for i in popular:
        if i in hash:
            if hash[i]/len(people) > 1/3:
                greater.append(i)

    print(greater)

def meet(size):
    top = []
    bot = []

    for i in range(math.ceil(size/2)):
        top.append(int(i))
        bot.append(int(math.ceil(size/2) + i))
    if(size%2 == 1):
        bot.pop()
        bot.append('x')

    for i in range(size-1):
        print(top)
        print(bot)
        print()
        top.insert(1, bot.pop(0))
        bot.insert(len(bot), top.pop())

test()
