import matplotlib.pyplot as plt
import time
import numpy as np
import subprocess
import string
import random

def build_dataset(size,companies):
    file = open(fname := ("dataset.txt"), "w")
    write_string = ""
    for j in range(0, size):
        name = ""
        [name := name + string.ascii_uppercase[random.randint(0,25)] for x in range(0,14)]
        write_string += str(random.randint(1,companies))+ " " +  str(name) + "\n"
        file.write(write_string)
    file.close()

def run_rooms():
    fname = "dataset.txt"
    argument = "plot.exe"
    run = subprocess.Popen(["type", str(fname), "|", argument], stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True, close_fds=True)
    stdinput = "type " + str(fname) + " | " + argument
    time.sleep(.1)

def fetch_results():
    file = open("output.txt", "r")
    time.sleep(.1)
    try:
        fetched = file.readlines()[0]
        file.close()
        return (int(fetched.split(" ")[0]),float(fetched.split(" ")[1]))
    except IndexError:
        print("error on co ")
        file.close()
        return (0,0)

x_val = []
y_val = []
for i in range(0,1000):
    x_val.append(i+1)
    dataset = build_dataset(4000,30)
    run_rooms()
    y_val.append(fetch_results()[0])

plt.plot(x_val,y_val,'o')
plt.show()
#plt.plot(runtimes,)
