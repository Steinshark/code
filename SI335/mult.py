import random
import time
nums_list = ["1","2","3","4","5","6","7","8","9"]
times = []
mult = 1000000
for i in range(1,2):
    num1 = ''
    num2 = ''
    time1 = time.time()
    for j in range(0,mult*i):
        num1 += nums_list[random.randint(0,8)]
        num2 += nums_list[random.randint(0,8)]
    num3 = int(num1) * int(num2)
    time2 = time.time()
    times.append(time2-time1)
import matplotlib.pyplot as plt

plt.plot([x * mult for x in range(len(times))],times,'o',markersize=3,label="exhibit A")
plt.legend(loc='best')
plt.xlabel("digits")
plt.ylabel("runtime (seconds)")
plt.show()
