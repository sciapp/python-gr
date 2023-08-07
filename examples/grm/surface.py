from math import pi, sin, cos
from typing import Dict, List

import grm.plot

X_DIM = 40
Y_DIM = 20

X_MIN = -2.0
X_MAX = 2.0
Y_MIN = 0.0
Y_MAX = pi


def test_surface() -> None:
    x = [X_MIN + (X_MAX - X_MIN) * (i / (X_DIM - 1)) for i in range(X_DIM)]
    y = [Y_MIN + (Y_MAX - Y_MIN) * (i / (Y_DIM - 1)) for i in range(Y_DIM)]
    z = [0.0] * (X_DIM * Y_DIM)
    for i in range(X_DIM):
        for j in range(Y_DIM):
            z[(Y_DIM - 1 - j) * X_DIM + i] = sin(x[i]) + cos(y[j])

    print("plot a surface with x, y and z")
    grm.plot.surface(x=x, y=y, z=z)
    input("Press enter to continue")

    print("plot a surface with y and z")
    grm.plot.surface(y=y, z=z)
    input("Press enter to continue")

    print("plot a surface with z only")
    grm.plot.surface(z=z, z_dims=(Y_DIM, X_DIM))
    input("Press enter to continue")

    # TODO plots look broken
    print("plot a surface with z only (but with limits)")
    grm.plot.surface(z=z, z_dims=(Y_DIM, X_DIM), x_range=(X_MIN, X_MAX), y_range=(Y_MIN, Y_MAX))
    input("Press enter to continue")

    print("plot a surface with x, y and z (but with larger limits)")
    grm.plot.surface(x=x, y=y, z=z, z_dims=(Y_DIM, X_DIM), x_range=(X_MIN - 1, X_MAX + 1), y_range=(Y_MIN - 1, Y_MAX + 1))
    input("Press enter to continue")

    print("plot two surfaces")
    series: List[Dict[str, grm.args._ElemType]] = [
        {
            "z": z,
            "z_dims": (Y_DIM, X_DIM),
            "x_range": (-4.25, -0.25),
            "y_range": (Y_MIN, Y_MAX)
        },
        {
            "z": z,
            "z_dims": (Y_DIM, X_DIM),
            "x_range": (0.25, 4.25),
            "y_range": (Y_MIN, Y_MAX)
        }
    ]
    grm.plot.surface(series=series)
    input("Press enter to continue")


if __name__ == "__main__":
    test_surface()
