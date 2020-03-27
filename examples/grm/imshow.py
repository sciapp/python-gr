#!/usr/bin/env python3
"""
[GRM] Using the imshow plot
"""
import numpy as np
import grm
import sys

x = np.linspace(-2, 2, 40)
y = np.linspace(0, np.pi, 20)
z = np.sin(x[np.newaxis, :]) + np.cos(y[:, np.newaxis])

grm.plot.plot(grm.args.new({"c": z, "kind": "imshow", "title": "imshow-test"}))

print("Press enter to exit")
sys.stdin.readline()
