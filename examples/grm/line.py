import grm, sys

args = grm.args.new({"x": [0.0, 1.0], "y": [0.0, 1.0]})

grm.plot(args)

print("Press enter to exit")
sys.stdin.read(1)

del args
grm.finalize()
