import math, time, sys, grm

M_PI = math.pi

plots = [
    [[], []],
    [[], []],
    [[], []],
    [[], []]
]

n = 1000
subplots = [grm.args.new(), grm.args.new(), grm.args.new(), grm.args.new()]

print("filling argument container...")

for i in range(0, 2):
    for j in range(0, n):
        plots[i][0].append(j * 2 * M_PI / n)
        plots[i][1].append(math.sin((j * (i + 1) * 2) * M_PI / n))
        plots[2 + i][0].append(j * 2 * M_PI / n)
        plots[2 + i][1].append(math.cos((j * (i + 1) * 2) * M_PI / n))

for i in range(0, 4):
    subplots[i]["x"] = plots[i][0]
    subplots[i]["y"] = plots[i][1]
    subplots[i]["subplot"] = [0.5 * (i % 2), 0.5 * (i % 2 + 1), 0.5 * (i // 2), 0.5 * (i // 2 + 1)]

args = grm.args.new();
args["subplots"] = subplots

print("plotting data...")

grm.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

time.sleep(10)

grm.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

del args
grm.finalize()
