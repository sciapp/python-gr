#!/usr/bin/env python3
"""
[GRM] Simple isosurface plot
"""
import sys

import numpy as np
import grm

x = np.linspace(-1, 1, 40)[:, np.newaxis, np.newaxis]
y = np.linspace(-1, 1, 40)[np.newaxis, :, np.newaxis]
z = np.linspace(-1, 1, 40)[np.newaxis, np.newaxis, :]
v = 1 - (x ** 2 + y ** 2 + z ** 2) ** 0.5
grm.plot.plot(
    grm.args.new(
        {
            "c": v,
            "isovalue": 0.5,
            "foreground_color": [0.2, 0.3, 0.8],
            "kind": "isosurface",
            "rotation": 30.0,
            "title": "Single-series isosurface plot.",
        }
    )
)

print("press enter to quit")
sys.stdin.read(1)
