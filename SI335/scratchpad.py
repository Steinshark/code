coins = [1,5,10,25,50]
import copy

def memoize(f):
    memo = {}
    def helper(val,coins,bank):
        if val not in memo:
            memo[val] = f(val,coins,bank)
        return memo[val]
    return helper

#@memoize
def build_change(value,coins,coin_bank):
    if value == 0:
        return coin_bank
    if value < 0:
        return
    else:
        total_calls = []
        for coin in coins:
            bank = coin_bank.copy()
            bank.append(coin)
            total_calls.append(build_change(value-coin,coins,bank))
        return min(total_calls)
def min(list):
    min = 100
    min_item = []
    for item in list:
        if item == None:
            continue
        if len(item) < min:
            min_item = item
            min = len(item)
    return min_item
list = []
print(build_change(int(input("change for: ")),coins,list,))
