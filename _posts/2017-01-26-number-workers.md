---
layout: post
title: How many workers are enough?
category: machine learning
---

In scientific computing, you often need to process several files, try a model using different parameters, et cetra. Furthermore, some algorithms can be run in parallel. You'll probably want to make use of your multi-core by parallelizing these tasks. The first thing you need to decide is, how large should the pool of workers be?

Workers are the name of processes you have running to carry out a given task. By default, Python `multiprocessing` package uses #workers=#processors. The package `scikit-learn` also does the same when you use `njobs=-1`. I have seen some people using #workers=#processors-1 to "leave some computing power for other tasks". Does this make sense?

First, we should classify our task as either CPU-bound or not-CPU-bound. If your task is memory-bound, then your computer will run into a grind as it swaps memory like crazy between processes. You want to use few processes in that case. If your task is disk-bound or bandwidth-bound, and some computations are required in the interim, it makes sense to use lots of processes so that the operating system can schedule computations while another worker is accessing the disk or the internet.

I am going to focus on CPU-bound processes here. How much should I run? Maybe we should base that number on the number of physical cores? Or maybe on the number of virtual cores? (Intel usually use two pipelines for each physical core and displays two virtual cores to the operating system.) And after we decide that, should we use a lower number to leave computing power for other tasks like the user interface? Or maybe a higher number because no task is 100%-CPU-bound and so we should take advantage of that?

Regardless, I will expect that as we increase the size of the pool of workers, something like this would happen:

![expected workers behavior](/imgs/blog/2017-01-26/05-expected.png)

1. negative slope as tasks take advantage of parallelization
2. positive slope as context switching starts being a pain
3. plateau

But... what I actually get is something like this:

![real workers behavior](/imgs/blog/2017-01-26/05-time.png)

This is a simulation whose code is given below. The CPU is an Intel Core i7-6700@3.40GHz with 4 physical cores and 8 virtual cores. The operating system is Ubuntu 16.04 with Linux 4.4.0.

This simulation is something I could never understand. I asked about this on [stackexchange.com](http://stackoverflow.com/questions/34965078/python-multiprocessing-no-diminishing-returns), and nobody provided a very plausible answer.

I tested in another computer. The gain is mostly up to the number of physical cores. But there are still small marginal gains afterwards, and, surprisingly, no marginal cost.

Maybe my tests are wrong? Here is my code. My task is to calculate the number of $$\pi$$ digits, up to a certain amount, which I called `task_complexity`. For whatever reason, I need to do this `tasks` times.

```python
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
plt.plot(x, y)
plt.xlabel('Number of processes')
plt.xlim(1, maxn)
plt.xticks(x)
plt.ylabel('Time in seconds')
plt.savefig('plot.png')
plt.show()
```

If these results are true, it means we should not worry about the size of the pool of workers, unless the task is memory-bound. And, in fact, we should probably create it a little bigger. Maybe #virtual_cores+2.
