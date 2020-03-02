import math, sys, grm

plots = [
    [
        [], []
    ], [
        [], []
    ]]
n = 1000
M_PI = math.pi
print("filling argument container...");

for i in range(0, 1000):
    plots[0][0].append(i * 2 * M_PI / n)
    plots[0][1].append(math.sin(i * 2 * M_PI / n))
    plots[1][0].append(i * 2 * M_PI / n)
    plots[1][1].append(math.cos(i * 2 * M_PI / n))

args = grm.args.new()
args["x"] = plots[0][0]
args["y"] = plots[0][1]

print("plotting sin...")
grm.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

args.clear()
args["x"] = plots[1][0]
args["y"] = plots[1][1]

print("plotting cos...")
grm.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

grm.switch(1)

args.clear();
args["x"] = plots[0][0]
args["y"] = plots[0][1]

print("plotting sin...")
grm.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

args.clear()
args["x"] = plots[1][0]
args["y"] = plots[1][1]
args["id"] = ":.2"

print("plotting sin AND cos...")
grm.plot(args)
print("Press any key to continue...")
sys.stdin.read(1)

del args
grm.finalize()
