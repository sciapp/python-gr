#!/usr/bin/env python3
"""
[GRM] Complex example of multiple subplots and series
"""
import sys

import numpy as np
import grm

x = np.linspace(-1, 1, 40)[:, np.newaxis, np.newaxis]
y = np.linspace(-1, 1, 40)[np.newaxis, :, np.newaxis]
z = np.linspace(-1, 1, 40)[np.newaxis, np.newaxis, :]
v = 1 - ((x - 0.5) ** 2 + y ** 2 + z ** 2) ** 0.5
v2 = 1 - ((x + 0.5) ** 2 + y ** 2 + z ** 2) ** 0.5
v3 = np.zeros((40, 40, 40))
v4 = np.zeros((40, 40, 40))
v5 = np.zeros((40, 40, 40))
v3[0, :, :] = 1
v4[:, 0, :] = 1
v5[:, :, 0] = 1
grm.plot.plot(
    grm.args.new(
        {
            "subplots": [
                {
                    "x": np.linspace(0, 2, 100),
                    "y": np.sin(np.linspace(0, 2, 100)),
                    "title": "Plot of sin from y = 0 to 2",
                    "subplot": [0, 1, 0.5, 1],
                },
                {
                    "series": [
                        {"c": v3, "isovalue": 0.5, "foreground_color": [0.8, 0.3, 0.2]},
                        {"c": v4, "isovalue": 0.5, "foreground_color": [0.2, 0.8, 0.3]},
                        {"c": v5, "isovalue": 0.5, "foreground_color": [0.6, 0.3, 0.8]},
                        {"c": v2, "isovalue": 0.5, "foreground_color": [0.2, 0.8, 0.3]},
                        {"c": v, "isovalue": 0.5, "foreground_color": [0.2, 0.3, 0.8]},
                    ],
                    "kind": "isosurface",
                    # "rotation": 30.0,
                    "title": "Example of multi-series Isosurface",
                    "subplot": [0, 0.5, 0, 0.5],
                },
                {
                    "c": np.maximum(v, v2),
                    "isovalue": 0.5,
                    "foreground_color": [0.2, 0.5, 0.3],
                    "title": "Single series isosurface",
                    "subplot": [0.5, 1, 0, 0.5],
                    "kind": "isosurface",
                },
            ],
            "size": [1000, 800],
        }
    )
)

print("press enter to quit")
sys.stdin.read(1)
