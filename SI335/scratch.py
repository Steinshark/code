import math
def nextPrime(currentPrime):
    for i in range(currentPrime+1,currentPrime+10000):
        flag = True
        print("checking " + str(i))
        for factor in range(2,round(math.sqrt(i))+1):
            print("\tchecking factor " + str(factor))
            if (i % factor) == 0:
                print("\t\tnope")
                flag = False
                break
        if flag:
            print(str(i) + " was prime")
            return i
primes = [2]
while len(primes) <= 26:
    primes.append(nextPrime(primes[-1]))

import string
fileWrite = open("dictionary","w")
count = 0
for letter in string.ascii_lowercase:
    count += 1
    line = "\'"+ letter + "\':" + str(primes[string.ascii_lowercase.index(letter)]) + ", "
    if (count % 5) == 0:
        line += "\n"
    fileWrite.write(line)
fileWrite.close()
