import math


def isItPrime(num_to_check):
    for i in range(2, int(num_to_check)):
        if (num_to_check % i) == 0:
            return False
    return True

def changeBase(original_num, base):
    as_string = str(original_num)
    iterator = 0
    num_array = [pow(base,(len(as_string)) - iterator)*int(digit) for digit in as_string if (iterator := iterator + 1)]

    return sum(num_array)



def main():
    o_num = int(input("this number: "))
    new = str(o_num)
    higher_base = int(int(new[-1]) + 1)
    for i in range(higher_base,10000):
        if isItPrime(changeBase(o_num, i)):
            print("prime in base " + str(i) + " with value " + str(changeBase(o_num, i)))
            break

main()
