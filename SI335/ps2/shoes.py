import random
import matplotlib.pyplot as plt
def scramble(l):
    for i in range(100):
        index_1 = random.randint(0,len(l)-1)
        index_2 = random.randint(0,len(l)-1)

        temp = l[index_1]
        l[index_1] = l[index_2]
        l[index_2] = temp
    return l
def sort_shoes(n):

    ## Divide the shoes into L and R piles
    shoes_l = scramble({x : False for x in range(0,n)})
    shoes_r = scramble({x : False for x in range(0,n)})
    person_is_on = {x : x for x in range(0,n)}

    person = {x : (False,False) for x in range(0,n)}

    iterations = 0

    ## while people dont have both shoes
    while True in [False in x for x in person.values()]:
        iterations += 1
        zero_fits = []
        l_fits = []
        both_fits = []
        shift+=1

        ## have each person look through the pair they dont have
        for p in person:


            ## have everyone start searching for the left shoe
            if not person[p][0]:
                trying_on = (shift + p) % len(shoes_l)
                while trying_on in shoes_l_done:
                    trying_on = (shift + p) % len(shoes_l)

                zero_fits.append(p)
                if p == shoes_l[trying_on]:
                    person[p] = (True,False)
                    shoes_l_done.append(trying_on)
                    shoes_l.pop(trying_on)

            ## if they already found
            elif not person[p][1]:
                trying_on = (shift + p) % len(shoes_r)
                while trying_on in shoes_r_done:
                    trying_on = (shift + p) % len(shoes_r)

                l_fits.append(p)
                if p == shoes_r[trying_on]:
                    person[p] = (True,True)
                    shoes_r_done.append(trying_on)
                    shoes_r.pop(trying_on)
            else:
                both_fits.append(p)
    #print("finished after " + str(iterations) + " iterations ")
    return iterations


def trial_run(runs,n):
    spread = [i*10 for i in range(1,n+1)]
    y = []
    for i in spread:
        print("size of " + str(i))
        sum = 0
        for run in range(runs):
            sum += sort_shoes(i)
        y.append(float(sum)/runs)


    plt.plot(spread,y,'o',markersize=3)
    print("showing")
    plt.savefig("out.png")


trial_run(int(input("trials: ")),int(input("spread: ")))



def shoeParty(friends, shoes):
    ## sorting shoes between L and R is theta(2n)
    L,R = sort_shoes(shoes)

    ## worst case this is theta(2n)
    while not done_matching:
        done_matching = True
        for f in friends:
            if not f.found_Left:
                if L(f.position) == f.L_shoe:
                    f.found_left = True
                else:
                    f.move_down_L_line()
                    done_matching = False
            elif not f.found_right:
                if R(f.position) == f.R_shoe"
                    f.found_right = True
                else:
                    f.move_down_R_line()
                    done_matching = False
