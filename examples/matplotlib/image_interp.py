import numpy as np
import matplotlib.pyplot as plt

A = np.random.rand(5,5)
plt.figure(1)
plt.imshow(A, interpolation='nearest')
plt.grid(True)

plt.figure(2)
plt.imshow(A, interpolation='bilinear')
plt.grid(True)

plt.figure(3)
plt.imshow(A, interpolation='bicubic')
plt.grid(True)

plt.show()
