def pi(n):
    from math import factorial
    t = 0
    pi = 0
    deno = 0
    k = 0
    for k in range(n):
        t = ((-1)**k)*(factorial(6*k))*(13591409+545140134*k)
        deno = factorial(3*k)*(factorial(k)**3)*(640320**(3*k))
        pi += t/deno
    pi = pi * 12/(640320**(1.5))
    pi = 1/pi
    return pi


import multiprocessing
import time
maxn = 20
tasks = 100
task_complexity = 1000
x = range(1, maxn+1)
y = [0]*maxn

for n in range(1, maxn+1):
    p = multiprocessing.Pool(n)
    tic = time.time()
    p.map(pi, [task_complexity]*tasks)
    toc = time.time()
    y[n-1] = toc-tic
    print('%2d %ds' % (n, y[n-1]))

import matplotlib.pyplot as plt
#plt.style.use('ggplot')
plt.plot(x, y)
plt.xlabel('Number of processes')
plt.xlim(1, maxn)
plt.xticks(x)
plt.ylabel('Time in seconds')
plt.savefig('plot.png')
plt.show()
