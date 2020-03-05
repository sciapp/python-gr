import numpy as np
import math, sys, grm

n = 1000
x_vals = np.linspace(0, 2 * math.pi, n)
sin_y_vals = np.sin(x_vals)
cos_y_vals = np.cos(x_vals)
print("filling argument container...")

args = grm.args.new({"x": x_vals, "y": sin_y_vals})

print("plotting sin...")
grm.plot.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

args.clear()
args.update({"x": x_vals, "y": cos_y_vals})

print("plotting cos...")
grm.plot.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

grm.plot.switch(1)

args.clear()
args.update({"x": x_vals, "y": sin_y_vals})

print("plotting sin...")
grm.plot.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

args.clear()
args.update({"x": x_vals, "y": cos_y_vals, "id": ":.2"})

print("plotting sin AND cos...")
grm.plot.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

del args
grm.plot.finalize()
