import matplotlib.pyplot as plt
import time
import numpy as np
import subprocess
import string
import random

company_runs = []
print("*NOTES*")
print("To run, you MUST ADD code to your original rooms.XXX that:\n" + \
      "\t- writes \'number_of_swaps runtime\' to \'output.txt\'\n\t" +
      "- it must be in the same directory as this program.")

print("I wrote my rooms in c++. My extra code looks like this:")
print("\tofstream writer;\n" +\
  "\twriter.open(\"output.txt\");\n" + \
  "\twriter << swaps << \" \" << double(clock()-time1)/CLOCKS_PER_SEC << endl;\n" + \
  "\twriter.close();")

print("If you do not already have it, you must install matplotlib,subprocess,numpy")
print("(i dont remember if they are installed in vanilla python)")
print("If you need to install a package, type \"pip install *package_name*\" into terminal")

input("\ngood to go?")
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + \
    "- This program will analyze runtime and swap counts vs size of dataset. " + \
    "\n- It will run and build a series for N1 to N2 (inclusive) distinct companies incrementing" + \
    " by X companies")
print(\
    "\ti.e. for N1=2, N2=30, X = 7, it will build 5 series with number of companies being: [2,9,16,23,30]\n")
N1 = int(input("Set N1: "))
N2 = int(input("Set N2: "))+1
X = int(input("Set X: "))
print("\n\n- For each series, it will make M datasets, the size of each being index * mutiplier")
print("\ti.e. M = 5, multiplier = 100 makes datasets of size [100,200,300,400,500] for each series\n")

datasets = int(input("M: "))
multiplier = int(input("multiplier: "))
argument = str(input("executable name (\"compiled_to.exe\"): "))
size = [multiplier*i for i in range(1,datasets)]
figure, (swaps,times) = plt.subplots(2)
figure.suptitle("swaps and time vs size")


print("Crunching...")
for co in range(N1,N2,X):
    time1 = time.time()
    company_runs.append((runtimes := list()))
    for i in range(1, datasets):
        file = open(fname := ("dataset.txt"), "w")
        write_string = ""
        for j in range(0, i*multiplier):
            name = ""
            [name := name + string.ascii_uppercase[random.randint(0,25)] for x in range(0,14)]
            write_string += str(random.randint(1,co))+ " " +  str(name) + "\n"
        file.write(write_string)
        file.close()

        stdinput = "type " + str(fname) + " | " + argument
        run = subprocess.Popen(["type", str(fname), "|", argument], stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True, close_fds=True)
        time.sleep(.1)
        file = open("output.txt", "r")
        try:
            fetched = file.readlines()[0]
            runtimes.append((int(fetched.split(" ")[0]),float(fetched.split(" ")[1])))
        except IndexError:
            runtimes.append(0)
            print("error on co " + str(co) + " size " + str(i*multiplier))

        file.close()
    print("finished series with " + str(co) + " companies in " + str(time.time()-time1)[:5] + " seconds")
for i in range(0,len(company_runs)):
    swaps.plot(size,[company_runs[i][x][0] for x in range(0,len(size))],"o",markersize=4, label=str(str(N1+i*X) + " companies"))
    times.plot(size,[company_runs[i][x][1] for x in range(0,len(size))],"o",markersize=4,label=str(str(N1+i*X) + " companies"))
swaps.legend(loc="best")
times.legend(loc="best")
    #plt.sca(swaps)
    #plt.yticks([x for x in range(0,len(company_runs[i])*len(company_runs), int(datasets/10))])
    #plt.sca(times)
    #plt.yticks([x for x in range(0,len(company_runs[i]), int(datasets/10))])
swaps.yaxis.set_major_locator(plt.MaxNLocator(10))
swaps.yaxis.set_major_locator(plt.MaxNLocator(10))
swaps.set_title("swaps")
times.set_title("runtime")
plt.show()
#plt.plot(runtimes,)
