#Everett Stenberg m226252
#Sorts a list of (company#,name) tuples such that all companies' members are together


## IMPORTS
import sys
##/IMPORTS

#
    #does the actual sorting
#
def swap_rooms(room_list):
    pass


#
    #determines the sorting method
#
def define_bounds(room_list):
    pass

#
    #collects input from terminal input
#
def build_input():
    raw_input = sys.stdin.readlines()
    mids_list = []
    for line in raw_input:
        mid_tuple = (line[0],line[1])
        print(mid_tuple)
        mids_list.append(mid_tuple)
    return mids_list


list = build_input()
