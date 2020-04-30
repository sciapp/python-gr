
import numpy as np
import matplotlib.pyplot as plt

mu, sigma = 100, 15
x = np.random.normal(mu, sigma, 10000)

# the histogram of the data
n, bins, patches = plt.hist(x, 50, facecolor='g', alpha=0.75, density=True)

plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.axis([40, 160, 0, 0.03])
plt.grid(True)
plt.show()

