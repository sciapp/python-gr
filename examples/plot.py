#!/usr/bin/env python
"""
Plot a function with the use of gr
"""

import time

from gr.pygr import plot

x = [-3.3 + t*0.1 for t in range(66)]
y = [t**5 - 13*t**3 + 36*t for t in x]
plot(x, y)
