from math import pi, sin, cos
from typing import Dict, List

import grm


LENGTH = 1000


def test_hold_append() -> None:
    plot_x = [i * 2 * pi / LENGTH for i in range(LENGTH)]
    plot_sin = [sin(i * 2 * pi / LENGTH) for i in range(LENGTH)]
    plot_cos = [cos(i * 2 * pi / LENGTH) for i in range(LENGTH)]

    series: List[Dict[str, grm.args._ElemType]] = [
        {
            "x": plot_x,
            "y": plot_sin
        },
        {
            "x": plot_x,
            "y": plot_cos
        }
    ]
    args: Dict[str, grm.args._ElemType] = {
        "append_plots": True,
        "hold_plots": True,
        "series": series[0]
    }
    grm.plot.plot(args)
    input("Press enter to continue")

    args.clear()
    args = {
        "size": (800.0, 800.0),
        "plot_id": 0
    }
    grm.plot.plot(args)
    input("Press enter to continue")

    args.clear()
    args = {
        "series": series[1]
    }
    grm.plot.merge(args)
    grm.plot.switch(1)
    grm.plot.plot(None)
    input("Press enter to continue")


if __name__ == "__main__":
    test_hold_append()
