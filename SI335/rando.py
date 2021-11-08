def return_list():
    m = int(input("m"))
    a = int(input("a"))
    x_last = int(input("seed"))
    this_list = list()
    print('[',end='')
    for i in range(0,m*2):
        this_list.append(str(x_last :=(x_last*a)%m))
        if x_last < 10:
            print(" ", end='')
        print(str(x_last) + ",",end='')
    print("]")

return_list()
