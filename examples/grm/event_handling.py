import math, sys, grm

M_PI = math.pi

def new_plot_callback(event):
  print("Got new plot event, plot_id: %s" % event.contents.new_plot_event.plot_id, file = sys.stderr)

def size_callback(event):
  print("Got size event, size: (%s, %s)" % (event.contents.size_event.width, event.contents.size_event.width))

plots = [
    [
        [], []
    ],
    [
        [], []
    ]
]

n = 1000
labels = ["sin", "cos"]
args = None
series = [None, None]

print("filling argument container...")

for i in range(0, n):
    plots[0][0].append(i * 2 * M_PI / n)
    plots[0][1].append(math.sin(i * 2 * M_PI / n))
    plots[1][0].append(i * 2 * M_PI / n)
    plots[1][1].append(math.cos(i * 2 * M_PI / n))

for i in range(0, 2):
    series[i] = grm.args.new();
    series[i]["x"] = plots[i][0]
    series[i]["y"] = plots[i][1]

args = grm.args.new();
args["series"] = series
args["labels"] = labels
args["kind"] = "line"

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
