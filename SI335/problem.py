import time
def largest(data, start):
    for i in range(0, start):
        print(' ', end='')
    if start == len(data) - 1:
        # only one thing left in the list, so return it
        return data[start]
    elif data[start] > (num := largest(data, start+1)):
        # first thing is largest, so return that
        return data[start]
    else:
        # otherwise, largest thing comes from recursive call
        return num





list = [3,1,5,72,154,125,52,16,2626,757,17,1,52,2,73,37,4,125,6,4211,1,43,51,51,25,15,512,632,127,41234,166,11,1235,646,547,68,2345,2   ]
time1 = time.time()
print(largest(list, 0))
print("took " + str(time.time()-time1))
