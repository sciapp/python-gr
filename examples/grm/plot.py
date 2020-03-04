import numpy as np
import grm, math, sys
from random import random


def test_consecutive_plots():
    n = 1000
    x_vals = np.linspace(0, 2 * math.pi, n)
    plots = [[x_vals, 2 * np.sin(x_vals)], [x_vals, np.sin(x_vals)]]

    print("filling argument container...")

    args = grm.args.new()
    for i in range(0, 2):
        args["x"] = plots[i][0]
        args["y"] = plots[i][1]
        grm.plot(args)
        print("Press any key to continue...")
        sys.stdin.read(1)


def test_line():
    n = 1000
    x_vals = np.linspace(0, 2 * math.pi, n)

    print("filling argument container...")

    args = grm.args.new()
    args["series"] = [{"x": x_vals, "y": np.sin(x_vals)}, {"x": x_vals, "y": np.cos(x_vals)}]
    args["labels"] = ["sin", "cos"]
    args["kind"] = "line"

    print("plotting data...")

    grm.plot(args)

    print("Press any key to continue...")
    sys.stdin.read(1)


def test_contourf():
    x = []
    y = []

    n = 100

    for i in range(0, n):
        x.append(random() * 8.0 - 4.0)
        y.append(random() * 8.0 - 4.0)

    z = np.sin(x) + np.cos(y)

    print("filling argument container...")

    args = grm.args.new({"subplots": {"series": {"x": x, "y": y, "z": z}, "kind": "contourf"}})

    print("plotting data...")

    grm.plot(args)

    print("Press any key to continue...")
    sys.stdin.read(1)


if __name__ == "__main__":
    test_line()
    test_consecutive_plots()
    test_contourf()
    grm.finalize()
