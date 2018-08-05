import matplotlib.pyplot as plt
import numpy as np

n = 500
y1 = np.random.randn(n)

trend = np.cumsum(100*np.abs(np.random.randn(n)))
y2 = y1 + trend

plt.plot(y1)
plt.xticks([])
plt.yticks([])
plt.savefig('y1.png', bbox_inches='tight')

plt.clf()
plt.plot(y2)
plt.xticks([])
plt.yticks([])
plt.savefig('y2.png', bbox_inches='tight')
