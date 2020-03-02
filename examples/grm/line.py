import grm, sys

args = grm.args.new()
args["x"] = [0.0, 1.0]
args["y"] = [0.0, 1.0]
grm.plot(args)

print("Press enter to exit")
sys.stdin.read(1)

del args
grm.finalize()
