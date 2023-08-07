from math import pi, sin, cos
from typing import Dict, Iterable

import grm

X_DIM = 40
Y_DIM = 20

X_MIN = -2.0
X_MAX = 2.0
Y_MIN = 0.0
Y_MAX = pi


def test_heatmap() -> None:
    x = [X_MIN + (X_MAX - X_MIN) * (i / (X_DIM - 1)) for i in range(X_DIM)]
    y = [Y_MIN + (Y_MAX - Y_MIN) * (i / (Y_DIM - 1)) for i in range(Y_DIM)]
    z = [0.0 for i in range(X_DIM * Y_DIM)]

    for i in range(X_DIM):
        for j in range(Y_DIM):
            z[((Y_DIM - 1) - j) * X_DIM + i] = sin(x[i]) + cos(y[j])

    print("plot a heatmap with x, y and z")
    grm.plot.heatmap(x=x, y=y, z=z)
    input("Press enter to continue")

    print("plot a heatmap with y and z")
    grm.plot.heatmap(y=y, z=z)
    input("Press enter to continue")

    print("plot a heatmap with z only")
    grm.plot.heatmap(z=z, z_dims=(Y_DIM, X_DIM))
    input("Press enter to continue")

    print("plot a heatmap with z only (but with limits)")
    grm.plot.heatmap(z=z, z_dims=(Y_DIM, X_DIM), x_range=(-2.0, 2.0), y_range=(0.0, pi))
    input("Press enter to continue")

    print("plot a heatmap with x, y, z and with (larger) limits")
    args: Dict[str, grm.args._ElemType] = {
        "x": x,
        "y": y,
        "z": z,
        "z_dims": (Y_DIM, X_DIM),
        "x_range": (-3.0, 3.0),
        "y_range": (-1.0, pi + 1.0)
    }
    grm.plot.heatmap(args)
    input("Press enter to continue")

    series: Iterable[Dict[str, grm.args._ElemType]] = [
        {"z": z, "z_dims": (Y_DIM, X_DIM), "x_range": (-4.25, -0.25), "y_range": (0.0, pi)},
        {"z": z, "z_dims": (Y_DIM, X_DIM), "x_range": (0.25, 4.25), "y_range": (0.0, pi)}
    ]
    print("plot two heatmaps")
    grm.plot.heatmap(series=series)
    input("Press enter to continue")

    print("plot a heatmap with x, y, z and resample method (nearest)")
    args = {
        "x": x,
        "y": y,
        "z": z,
        "resample_method": "nearest"
    }
    grm.plot.heatmap(args)
    input("Press enter to continue")

    print("plot a heatmap with x, y, z and resample method (linear)")
    args["resample_method"] = "linear"
    grm.plot.heatmap(args)
    input("Press enter to continue")

    print("plot a heatmap with x, y, z and resample method (lanczos)")
    args["resample_method"] = "lanczos"
    grm.plot.heatmap(args)
    input("Press enter to continue")

    # MISSING CONSTANTS
    # print("plot a heatmap with x, y, z and resample method (custom)")
    # args["resample_method"] = GKS_K_DOWNSAMPLE_HORIZONTAL_NEAREST | GKS_K_DOWNSAMPLE_VERTICAL_LINEAR | GKS_K_UPSAMPLE_HORIZONTAL_LANCZOS | GKS_K_UPSAMPLE_VERTICAL_NEAREST
    # grm.plot.heatmap(args)
    # input("Press enter to continue")

    x[0:5] = (-3.25, -1.25, -0.25, 0.25, 1.25, 3.25)
    y[0:2] = (0.0, 2.0, 3.0)
    series = [
        {"x": x[0:2], "y": y[0:2], "z": z[0:8], "z_dims": (3, 3)},
        {"x": x[3:5], "y": y[0:2], "z": z[0:8], "z_dims": (3, 3)}
    ]
    print("plot two non-uniform heatmaps")
    grm.plot.heatmap(series=series)
    input("Press enter to continue")


if __name__ == "__main__":
    test_heatmap()
