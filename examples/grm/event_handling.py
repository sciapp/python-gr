from math import pi, sin, cos
import sys
from typing import Dict, List

import grm


LENGTH = 1000


def new_plot_callback(event: grm.event.EVENT_NEW_PLOT) -> None:
    print("Got new plot event, plot_id: %s" % event.plot_id, file=sys.stderr)


def size_callback(event: grm.event.EVENT_SIZE) -> None:
    print("Got size event, size: (%s, %s)" % (event.width, event.width))


def test_line() -> None:
    plot_x = [i * 2 * pi / LENGTH for i in range(LENGTH)]
    plot_sin = [sin(i * 2 * pi / LENGTH) for i in range(LENGTH)]
    plot_cos = [cos(i * 2 * pi / LENGTH) for i in range(LENGTH)]

    labels = ("sin", "cos")

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

    grm.event.register(grm.event.EventType.NEW_PLOT, new_plot_callback)
    grm.event.register(grm.event.EventType.SIZE, size_callback)

    print("plotting data")
    grm.plot.line(series=series, labels=labels)
    input("Press enter to continue")

    print("plotting data")
    grm.plot.line(series=series, labels=labels, size=(1000.0, 1000.0))
    input("Press enter to continue")

    args: Dict[str, grm.args._ElemType] = {
        "series": series,
        "labels": labels,
        "size": (1000.0, 1000.0)
    }
    print("plotting data")
    grm.plot.switch(1)
    grm.plot.line(args)
    input("Press enter to continue")


if __name__ == "__main__":
    test_line()
