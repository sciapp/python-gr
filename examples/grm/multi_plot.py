from math import pi, sin, cos
from typing import Dict

import grm


LENGTH = 1000


def test_multiple_plots() -> None:
    plot_x = [i * 2 * pi / LENGTH for i in range(LENGTH)]
    plot_sin = [sin(i * 2 * pi / LENGTH) for i in range(LENGTH)]
    plot_cos = [cos(i * 2 * pi / LENGTH) for i in range(LENGTH)]

    args: Dict[str, grm.args._ElemType] = {
        "x": plot_x,
        "y": plot_sin
    }
    print("plotting sin")
    grm.plot.plot(args)
    input("Press enter to continue")

    args["y"] = plot_cos
    print("plotting cos")
    grm.plot.plot(args)
    input("Press enter to continue")

    grm.plot.switch(1)

    args["y"] = plot_sin
    print("plotting sin")
    grm.plot.plot(args)
    input("Press enter to continue")

    args["y"] = plot_cos
    args["id"] = ":.2"
    print("plotting sin AND cos")
    grm.plot.plot(args)
    input("Press enter to continue")


if __name__ == "__main__":
    test_multiple_plots()
