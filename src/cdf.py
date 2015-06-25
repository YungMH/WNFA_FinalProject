import numpy as np
import matplotlib.pyplot as plt

x = np.random.rand(100)
y = np.sin(2*np.pi*x) + 2 * x * (np.random.rand(100)-0.5)
nbins = 10

n, _ = np.histogram(x, bins=nbins)
sy, _ = np.histogram(x, bins=nbins, weights=y)
sy2, _ = np.histogram(x, bins=nbins, weights=y*y)
mean = sy / n
std = np.sqrt(sy2/n - mean*mean)

plt.plot(x, y, 'bo')
plt.errorbar((_[1:] + _[:-1])/2, mean, yerr=std, fmt='r-')
plt.show()