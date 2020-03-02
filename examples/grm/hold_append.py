import math, grm, sys

M_PI = math.pi

plots = [
    [
        [], []
    ],
    [
        [], []
    ]
]
series = [
    grm.args.new(),
    grm.args.new()
];
n = 1000

print("filling argument container...")

for i in range(1000):
    plots[0][0].append(i * 2 * M_PI / n)
    plots[0][1].append(math.sin(i * 2 * M_PI / n))
    plots[1][0].append(i * 2 * M_PI / n)
    plots[1][1].append(math.cos(i * 2 * M_PI / n))

for i in range(0, 2):
    series[i]["x"] = plots[i][0]
    series[i]["y"] = plots[i][1]

args = grm.args.new({
    "append_plots": 1, # Automatically create new plots, if no `plot_id` is given
    "hold_plots": 1   # Do not delete contents of the default plot automatically
    })
print("before")
grm.merge(args)
print("after")
args["series"] = series[0]

print("plotting data...")
grm.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

#args2 = args # we need to preserve the data which has been given as x and y
del args
args = [None, None] * 100000
print(series[0]._ptr)

args = grm.args.new()
args["size"] = [800.0, 800.0]
args["plot_id"] = 0 # Avoid creating a new plot

print("plotting data...")
grm.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

del args
args = grm.args.new()
args["series"] = series[1]
grm.merge(args); # This call will create a new plot with id `1`
print("plotting data...")
grm.switch(1)
grm.plot(None)
print("Press any key to continue...")
sys.stdin.read(1)
#
# args.delete()
#
# grm.finalize()
