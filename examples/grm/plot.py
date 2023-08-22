from math import pi, sin, cos
from random import random
from typing import Dict, List

import grm


LENGTH = 1000


def test_consecutive_plots() -> None:
    print("test_consecutive_plots")
    plot_x = [i * 2 * pi / LENGTH for i in range(LENGTH)]
    plot_sin = [sin(i * 2 * pi / LENGTH) for i in range(LENGTH)]
    plot_cos = [cos(i * 2 * pi / LENGTH) for i in range(LENGTH)]

    args: Dict[str, grm.args._ElemType] = {
        "x": plot_x,
        "y": plot_sin
    }
    grm.plot.plot(args)
    input("Press enter to continue")

    args["y"] = plot_cos
    grm.plot.plot(args)
    input("Press enter to continue")


def test_line() -> None:
    print("test_line")
    plot_x = [i * 2 * pi / LENGTH for i in range(LENGTH)]
    plot_sin = [sin(i * 2 * pi / LENGTH) for i in range(LENGTH)]
    plot_cos = [cos(i * 2 * pi / LENGTH) for i in range(LENGTH)]

    labels = ["sin", "cos"]

    series: List[Dict[str, grm.args._ElemType]] = [
        {"x": plot_x, "y": plot_sin},
        {"x": plot_x, "y": plot_cos}
    ]
    args: Dict[str, grm.args._ElemType] = {
        "series": series,
        "labels": labels
    }
    grm.plot.line(args)
    input("Press enter to continue")


def test_line3d() -> None:
    print("test_line3d")
    x = [i * 30.0 / LENGTH for i in range(LENGTH)]
    y = [cos(x[i]) * x[i] for i in range(LENGTH)]
    z = [sin(x[i]) * x[i] for i in range(LENGTH)]

    args: Dict[str, grm.args._ElemType] = {
        "x": x,
        "y": y,
        "z": z
    }
    grm.plot.plot3(args)
    input("Press enter to continue")


def test_contourf() -> None:
    print("test_contourf")
    x = [random() * 8 - 4 for _ in range(100)]
    y = [random() * 8 - 4 for _ in range(100)]
    z = [sin(x[i]) + cos(y[i]) for i in range(100)]

    series = {
        "x": x,
        "y": y,
        "z": z
    }
    subplot = {
        "series": series,
    }
    grm.plot.contourf(subplots=subplot)
    input("Press enter to continue")


if __name__ == "__main__":
    test_consecutive_plots()
    test_line()
    test_line3d()
    test_contourf()
