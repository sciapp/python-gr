#!/usr/bin/env python
# -*- no-plot -*-
"""
Compare figure output performance of Matplotlib vs. GR
"""

from __future__ import print_function

import sys
import os
from timeit import default_timer as timer
import numpy as np

if len(sys.argv) > 1:
    dev = sys.argv[1]
else:
    dev = 'ps'

x = np.arange(0, 2 * np.pi, 0.01)

# create an animation using GR

from gr.pygr import plot

tstart = timer()
os.environ["GKS_WSTYPE"] = dev
for i in range(1, 100):
    plot(x, np.sin(x + i / 10.0))
    if i % 2 == 0:
        print('.', end="")
        sys.stdout.flush()

fps_gr = int(100 / (timer() - tstart))
print('fps  (GR): %4d' % fps_gr)

# create the same animation using matplotlib

import matplotlib
matplotlib.use(dev)

import matplotlib.pyplot as plt

tstart = timer()
for i in range(1, 100):
    plt.clf()
    plt.plot(np.sin(x + i / 10.0))
    plt.savefig('mpl%04d.%s' % (i, dev))
    if i % 2 == 0:
        print('.', end="")
        sys.stdout.flush()


fps_mpl = int(100 / (timer() - tstart))
print('fps (mpl): %4d' % fps_mpl)

print('  speedup: %6.1f' % (float(fps_gr) / fps_mpl))
