#!/usr.bin/env python
"""
various polar_histograms.
"""
from gr.pygr.mlab import polar_histogram

import numpy as np
from time import sleep

norms = ['count', 'probability', 'countdensity', 'pdf', 'cumcount', 'cdf']
random_theta = np.random.rand(1, 10000) * 2 * np.pi
theta = [0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1]
col = (1, 1, 1000)
bc = [6, 9, 0, 4, 3]
be = [0, 0.2, 0.5, 0.9, 2, 2.5]

for param in norms:
    print(param)

    polar_histogram(theta, rlim=None, philim=None, normalization=param, draw_edges=False,
                    colormap=None, bin_edges=None, num_bins=None)
    print("normal")
    sleep(1)

    polar_histogram(random_theta, num_bins=100)
    print("normal with random theta")
    sleep(1)

    polar_histogram(bc, stairs=True, num_bins=None)
    print("bincounts")
    sleep(1)

    polar_histogram(bc, bin_edges=be)
    print("bincounts and binedges")
    sleep(1)

    polar_histogram(theta, rlim=(0.125, 0.75), stairs=True)
    print("bin_edges, rlim and stairs")
    sleep(1)

    polar_histogram(theta, colormap=col, draw_edges=True, philim=(np.pi / 3, np.pi * 1.5),
                    stairs=False, bin_edges=None)
    print("philim, rlim and colormap+drawedges")
    sleep(1)

    polar_histogram(theta, colormap=col, draw_edges=True, bin_edges=be)
    print("philim. rlim, colormap and binedges")
    sleep(1)
