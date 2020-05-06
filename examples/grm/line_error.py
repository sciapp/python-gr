#!/usr/bin/env python3
"""
[GRM] Errorplot example with custom cap colors
"""
import sys
import numpy as np
import grm

x = np.linspace(0, 1, 10)
y = np.sin(x)
e = np.array([0.2] * len(y))
e = 0.2
print(e)
args = grm.args.new(
    {
        "x": x,
        "y": y,
        "error": {
            "relative": e,
            "absolute": 0.005,
            "upwardscap_color": 2,
            "downwardscap_color": 3,
            "errorbar_color": 4,
        },
    }
)

grm.plot.plot(args)

print("Press enter to exit")
sys.stdin.read(1)

del args
grm.plot.finalize()
