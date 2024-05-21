import sys
from typing import Dict

import grm


def merge_end_callback(event: grm.event.EVENT_MERGE_END) -> None:
    print(f"merge end: {event.identificator}")


def test_merge() -> None:
    plots = [[[float(i * 3 * 2 + j * 3 + k) for k in range(3)] for j in range(2)] for i in range(4)]

    series: Dict[str, grm.args._ElemType] = {"x": plots[1][0], "y": plots[1][1]}

    if not grm.plot.merge(series):
        print(f"failed merging {series}")
        sys.exit(1)

    series = {"x": plots[0][0], "y": plots[0][1]}

    if not grm.plot.merge(series):
        print(f"failed merging {series}")
        sys.exit(1)

    series = {"x": plots[1][0], "y": plots[1][1], "series_id": 2}

    if not grm.plot.merge(series):
        print(f"failed merging {series}")
        sys.exit(1)

    series = {"x": plots[3][0], "y": plots[3][1], "id": "2.2"}

    if not grm.plot.merge(series):
        print(f"failed merging {series}")
        sys.exit(1)

    series = {"x": plots[2][0], "y": plots[2][1]}
    subplot: Dict[str, grm.args._ElemType] = {"series": series, "subplot_id": 2}

    if not grm.plot.merge(subplot):
        print(f"failed merging {subplot}")
        sys.exit(1)

    series = {"x": plots[3][1], "id": "2.1"}

    if not grm.plot.merge(series):
        print(f"failed merging {series}")
        sys.exit(1)

    series = {"x": plots[2][0], "y": plots[2][1], "id": "2.1"}

    if not grm.plot.merge(series):
        print(f"failed merging {series}")
        sys.exit(1)


def test_merge_options() -> None:
    plots = [[[float(i * 3 * 2 + j * 3 + k) for k in range(3)] for j in range(2)] for i in range(4)]

    series: Dict[str, grm.args._ElemType] = {
        "x": plots[1][0],
        "y": plots[1][1]
    }
    if not grm.plot.merge(series):
        print(f"failed merging {series}")
        sys.exit(1)

    series = {
        "x": plots[0][0],
        "y": plots[0][1]
    }
    if not grm.plot.merge_extended(series, hold=False, identificator="extended"):
        print(f"failed merging {series}")
        sys.exit(1)

    series = {
        "x": plots[2][0],
        "y": plots[2][1]
    }
    if not grm.plot.merge_named(series, "named"):
        print(f"failed merging {series}")
        sys.exit(1)


if __name__ == "__main__":
    test_merge()
    grm.event.register(grm.event.EventType.MERGE_END, merge_end_callback)
    test_merge_options()
