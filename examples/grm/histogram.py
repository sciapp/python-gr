from math import pi, sin, fabs
from typing import Dict

import grm

LENGTH = 2000
NBINS = 20


def test_plot() -> None:
    plot = [sin(2 * pi * i / LENGTH) for i in range(LENGTH)]
    weights = [-1.0 for _ in range(LENGTH)]
    errors = [fabs(sin(pi * i / (NBINS - 1))) for i in range(NBINS)]

    error = {
        "relative": [errors, errors],
        "upward_scap_color": 2,
        "downward_scap_color": 3,
        "error_bar_color": 4
    }

    args: Dict[str, grm.args._ElemType] = {
        "x": plot,
        "weights": weights,
        "error": error,
        "num_bins": NBINS,
        "bar_color": (0.0, 0.0, 1.0),
        "edge_color": (1.0, 0.0, 0.0),
        "title": "Histogram of a sine wave [0; 2pi] with 20 bins and negative weights"
    }

    grm.plot.hist(args)
    input("Press enter to continue")


if __name__ == "__main__":
    test_plot()
