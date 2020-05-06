#!/usr/bin/env python
"""
3D contour plot
"""

import os
import time
import numpy as np
from gr.pygr import *

z = np.loadtxt(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            "fecr.dat")).reshape(200, 200)
contour(z)
