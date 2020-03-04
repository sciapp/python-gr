import math, time, sys, grm
import numpy as np


n = 1000
x_vals = np.linspace(0, 2 * math.pi, n)

plots = [[x_vals, np.sin(x_vals)], [x_vals, np.sin(x_vals * 2)], [x_vals, np.cos(x_vals)], [x_vals, np.cos(x_vals * 2)]]

subplots = []

print("filling argument container...")

for i in range(0, 4):
    subplots.append(
        {
            "x": plots[i][0],
            "y": plots[i][1],
            "subplot": [0.5 * (i % 2), 0.5 * (i % 2 + 1), 0.5 * (i // 2), 0.5 * (i // 2 + 1)],
        }
    )

args = grm.args.new({"subplots": subplots})

print("plotting data...")

grm.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

del args
grm.finalize()
