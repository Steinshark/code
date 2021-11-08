import matplotlib.pyplot as plt
import time
import numpy as np
import subprocess
import string
import random


fname = r"test.exe"
filename = str(input("filename: "))
count = str(input("count: "))
start_time = time.time()
run = subprocess.run([fname, filename, count])
end_time = time.time()

print(str(end_time - start_time) + " seconds have elapsed")
