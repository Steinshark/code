import random
import time

class searches:
    ## basic utilities
    @staticmethod
    def time_runtime(function):
        start = time.time()
        return_value = function()
        end = time.time()
        return start-end
    @staticmethod
    def get_random_index(given_list):
        return random.randint(0, len(given_list)-1)
    @staticmethod
    def build_random_list(size, value_min, value_max):
        return [random.randint(value_min,value_max) for i in range(0, size)]

    @staticmethod
    def insertion_sort(given_list):
        time1 = time.time()
        for i in range(0, len(given_list)-1):
            i = len(given_list)-1 -i
            max = i
            for j in range(0, i):
                if given_list[j] > given_list[max]:
                    max = j
            temp = given_list[i]
            given_list[i] = given_list[max]
            given_list[max] = temp
            if i%(len(given_list)/100) == 0:
                print("finished " + str(i) + " in " + str(time.time()-time1))
                time1 = time.time()
        return given_list
    @staticmethod
    def merge_sort(given_list):
        if len(given_list) <= 10:
            return insertion_sort(given_list)
        else:
            mid = len(given_list) // 2
            list_a = given_list[:mid]
            list_b = given_list[mid:]
            list_a = merge_sort(list_a)
            list_b = merge_sort(list_b)
            return combine(list_a, list_b)


    ##searches
    @staticmethod
    def linear_search(given_list, search_term, sorted):
        if sorted:
            index = 0
            while not (result := given_list[index]) == search_term:
                index = index + 1
                if result > search_term:
                    return -1
            return index
        else:
            for i in range(0, len(given_list)-1):
                if given_list[i] == search_term:
                    return i
            return -1
    @staticmethod
    def binary_search(given_list, search_term, min, max):
        if not min > max:
            midpoint = (max + min) // 2
            #print("called with min:" + str(min) + " max:" + str(max) + " midpoint: " +  str(midpoint) + " found " + str(given_list[midpoint]))
            result = given_list[midpoint]
            if search_term == result:
                return midpoint
            if search_term > result:
                return searches.binary_search(given_list, search_term, midpoint+1, max)
            elif search_term < result:
                return searches.binary_search(given_list, search_term, min, midpoint-1)
        print("didnt find " + str(search_term))
        return -1

    @staticmethod
    def random_search(given_list, search_term):
        index = random.randint(0, len(given_list)-1)
        while given_list[index] != search_term:
            index = random.randint(0, len(given_list)-1)
        return index
