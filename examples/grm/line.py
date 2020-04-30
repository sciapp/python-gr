#!/usr/bin/env python3
"""
[GRM] Simple line example
"""
import sys
import grm

args = grm.args.new({"x": [0.0, 1.0], "y": [0.0, 1.0]})

grm.plot.plot(args)

print("Press enter to exit")
sys.stdin.read(1)

del args
grm.plot.finalize()
