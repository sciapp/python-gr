import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

# make up data.
# npts = int(raw_input('enter # of random points to plot:'))
np.random.seed(0)
npts = 200
x = np.random.uniform(-2, 2, npts)
y = np.random.uniform(-2, 2, npts)
z = x * np.exp(-x ** 2 - y ** 2)
# define grid
xi, yi = np.mgrid[-2.1:2.1:100j, -2.1:2.1:200j]
# grid the data.
zi = griddata((x, y), z, (xi, yi), method='linear')
# contour the gridded data, plotting dots at the nonuniform data points.
plt.contour(xi, yi, zi, 15, linewidths=0.5, colors='k')
plt.contourf(xi, yi, zi, 15, cmap=plt.cm.rainbow, vmax=np.nanmax(np.abs(zi)), vmin=-np.nanmax(np.abs(zi)))
plt.colorbar()  # draw colorbar
# plot data points.
plt.scatter(x, y, marker='o', c='b', s=5, zorder=10)
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.title('griddata test (%d points)' % npts)
plt.show()
