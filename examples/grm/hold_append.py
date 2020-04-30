#!/usr/bin/env python3
"""
[GRM] Resizing plots after input and changing series
"""
import math
import sys
import numpy as np
import grm


print("filling argument container...")

n = 1000
x_vals = np.linspace(0, 2 * math.pi, n)
plots = [[x_vals, np.sin(x_vals)], [x_vals, np.cos(x_vals)]]

series = [{"x": plots[0][0], "y": plots[0][1]}, {"x": plots[1][0], "y": plots[1][1]}]

args = grm.args.new(
    {
        "append_plots": 1,  # Automatically create new plots, if no `plot_id` is given
        "hold_plots": 1,  # Do not delete contents of the default plot automatically
    }
)
grm.plot.merge(args)
args["series"] = series[0]

print("plotting data...")
grm.plot.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)
args2 = args
# del args

args = grm.args.new({"size": [800.0, 800.0], "plot_id": 0})  # Avoid creating a new plot

print("plotting data...")
grm.plot.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

del args
args = grm.args.new({"series": series[1]})
grm.plot.merge(args)
# This call will create a new plot with id `1`
print("plotting data...")
grm.plot.switch(1)
grm.plot.plot(None)
print("Press any key to continue...")
sys.stdin.read(1)
#
# args.delete()
#
# grm.finalize()
