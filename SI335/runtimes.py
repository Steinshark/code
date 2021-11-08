    import matplotlib.pyplot as plt
import math
import threading

KEYGEN = .0000001
ENCRYPT = .15
DECRYPT = .0001
CRACK = 5.22
def keyGen(key_size,cores):
    try:
        return KEYGEN*(key_size**4)/cores
    except OverflowError:
        return None
def Encrypt(key_size,cores):
    try:
        return ENCRYPT*(key_size*math.log(key_size,10))/cores
    except OverflowError:
        return None
def Decrypt(key_size,cores):
    try:
        return DECRYPT*(key_size**2)/cores
    except OverflowError:
        return None
def Crack(key_size,cores):
    try:
        return CRACK*(1.1**key_size)/cores
    except OverflowError:
        return None

FUNCS1 = {\
        "keygen" : keyGen,\
        "encrypt" : Encrypt,\
        "decrypt" : Decrypt,\
        "crack" : Crack\
}


def graph():
    x,y,name = build_set()
    plt.figure(1)
    plt.plot(x,y,'o',markersize=1,label=name)
    plt.draw()

def show():
    plt.legend(loc="best")
    plt.show()

FUNCS2 = {\
"graph" : graph,\
"show" : show\
}

def build_set():
    size = int(input("dataset size: "))
    x = [x for x in range(1,size+1)]
    y = []
    function = str(input("graphing: "))
    param2 = int(input("cores: "))
    for i in range(1,size+1):
        y.append(FUNCS1[function](i,param2))
    return x,y,str(function) + "ing " + str(param2) + "cores"

def print_num(number):
    string = ''
    pre_dec = str(number).index('.')

    if str(number)[-4] == 'e':
        return str(number)[:6] + "            " + str(number)[-4:] + "  "
    post_dec = len(str(number)) - pre_dec - 1
    string += str(number)[:pre_dec]
    if pre_dec < 16:
        string += "                "[:16-pre_dec]
    string += '.'
    if post_dec > 5:
        string += str(number)[pre_dec+1:][:5]
    else:
        for i in range(0,5):
            if i < post_dec:
                string += str(number)[pre_dec+1:][i]
            else:
                string += " "
    return string + "\t"

running = True
while running:
    command_name = str(input("> "))
    try:
        result = FUNCS1[command_name](int(input("   keysize: ")),int(input("   cores:   ")))
        print("   RUNTIME------------------------------")
        if result == None:
            print("overflow error :o\n\n")
            continue
        print("\t"+print_num(result) + "seconds-")
        print("\t"+print_num(result/60) + "minutes-")
        print("\t"+print_num(result/3600) + "hours  -")
        print("\t"+print_num(result/(3600*24)) + "days   -")
        print("\t"+print_num(result/(3600*24*360)) + "years  -\n\n")
    except KeyError:
        pass
    try:
        result = FUNCS2[command_name]()
    except KeyError:
        pass
    if command_name == 'quit':
        running = False














Def sail():
	n = 1
	while(true):
		moveNorth(n)   #From origin
		if(foundPort()): break
		moveSouth(n)  # Get back to origin
		n = n*2
        moveSouth(n)  #South two n from origin
        if(foundPort()): break
        moveNorth(n)   #Get back to origin
        n = n*2
