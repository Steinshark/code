import random
import math

def gen_prime():
    starting_point = random.randint(lower_bound,10*lower_bound)
    if (starting_point%2) == 0:
        starting_point += 1
    while not is_prime(starting_point):
        starting_point+=2
    return starting_point

def is_prime(number):
    if (number%2) == 0:
        return False

    for i in range(3,int(math.sqrt(number))+1,2):
        if (number%i) == 0:
            return False
    return True

def factor(number):
    if (number%2) == 0:
        return False

    for i in range(3,int(math.sqrt(number))+1,2):
        if (number%i) == 0:
            return i
    return -1


lower_bound = 1000000000000000
prime_1 = gen_prime()
prime_2 = gen_prime()
product = prime_1*prime_2


print("p1: " + str(prime_1) + "  p2: " + str(prime_2))


print("product is " + str(product))
print("factoring")
factor_1 = factor(product)
factor_2 = product / factor_1

print("f1: " + str(factor_1) + " f2: " + str(factor_2))
