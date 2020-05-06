#!/usr/bin/env python3
"""
[GRM] Rotation of isovalue plot with two spheres
"""
import sys
import time
import numpy as np
import grm

x = np.linspace(-1, 1, 100)[:, np.newaxis, np.newaxis]
y = np.linspace(-1, 1, 100)[np.newaxis, :, np.newaxis]
z = np.linspace(-1, 1, 100)[np.newaxis, np.newaxis, :]
v = 1 - ((x - 0.5) ** 2 + y ** 2 + z ** 2) ** 0.5
v2 = 1 - ((x + 0.5) ** 2 + y ** 2 + z ** 2) ** 0.5
args = grm.args.new(
    {
        "c": np.maximum(v, v2),
        "isovalue": 0.5,
        "foreground_color": [0.2, 0.5, 0.3],
        "title": "Single series isosurface",
        "kind": "isosurface",
        "hold_plots": 1,
    }
)

grm.plot.merge(args)
for i in range(0, 180, 2):
    grm.plot.plot(grm.args.new({"rotation": float(i), "plot_id": "0"}))
    time.sleep(0.1)

print("press enter to quit")
sys.stdin.read(1)
