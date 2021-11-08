import random

def check_a_billion():
    for i in range(1,1000000000):
        divide = 123638551987389189689312346/i
        if i % 1000000 == 0:
            print(i*1000000)
check_a_billion()
