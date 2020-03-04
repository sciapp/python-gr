import math, sys, grm
import numpy as np


def new_plot_callback(event):
    print("Got new plot event, plot_id: %s" % event.plot_id, file=sys.stderr)


def size_callback(event):
    print("Got size event, size: (%s, %s)" % (event.width, event.width))


n = 1000
x_vals = np.linspace(0, 2 * math.pi, n)

print("filling argument container...")


args = grm.args.new(
    {
        "series": [{"x": x_vals, "y": np.sin(x_vals)}, {"x": x_vals, "y": np.cos(x_vals)}],
        "labels": ["sin", "cos"],
        "kind": "line",
    }
)

grm.event.register(grm.event.EventType.NEW_PLOT, new_plot_callback)
grm.event.register(grm.event.EventType.SIZE, size_callback)

print("plotting data...")

grm.plot(args)

print("Press any key to continue...")
sys.stdin.read(1)

args["size"] = [1000.0, 1000.0]

print("plotting data...")

grm.plot(args)

print("Press any key to continue...")
sys.stdin.read(1)

args["size"] = [1000.0, 1000.0]

print("plotting data...")

grm.switch(1)
grm.plot(args)

print("Press any key to continue...")
sys.stdin.read(1)

del args
grm.finalize()
