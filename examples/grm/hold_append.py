import math, grm, sys
import numpy as np


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
grm.merge(args)
args["series"] = series[0]

print("plotting data...")
grm.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)
args2 = args
# del args

args = grm.args.new({"size": [800.0, 800.0], "plot_id": 0})  # Avoid creating a new plot

print("plotting data...")
grm.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

del args
args = grm.args.new({"series": series[1]})
grm.merge(args)
# This call will create a new plot with id `1`
print("plotting data...")
grm.switch(1)
grm.plot(None)
print("Press any key to continue...")
sys.stdin.read(1)
#
# args.delete()
#
# grm.finalize()
