from typing import Dict

import grm


def test_pie() -> None:
    x = [188.6, 107.8, 100.3, 99.0]
    c = [
        93 / 255, 57 / 255, 101 / 255,
        175 / 255, 130 / 255, 185 / 255,
        207 / 255, 180 / 255, 213 / 255,
        223 / 255, 205 / 255, 227 / 255
    ]
    labels = ["Czech Republic", "Austria", "Romania", "Germany"]

    args: Dict[str, grm.args._ElemType] = {
        "x": x,
        "labels": labels,
        "title": "Beer consumption per capita in 2018 (litres per year)"
    }
    print("plot a pie chart with x")
    grm.plot.pie(args)
    input("Press enter to continue")


if __name__ == "__main__":
    test_pie()
