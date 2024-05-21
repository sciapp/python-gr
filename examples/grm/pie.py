from typing import Dict

import grm


# TODO results in warning
#   GKS: Possible loss of precision in routine SET_WINDOW
#   GKS: Rectangle definition is invalid in routine SET_WINDOW
def test_pie() -> None:
    x = [188.6, 107.8, 100.3, 99.0]
    labels = ["Czech Republic", "Austria", "Romania", "Germany"]

    args: Dict[str, grm.args._ElemType] = {
        "x": x,
        "labels": labels,
        "title": "Beer consumption per capita in 2018 (litres per year)"
    }
    print("plot a pie chart with x")
    grm.plot.pie(args)
    input("Press enter to continue")

    c = [
        93 / 255, 57 / 255, 101 / 255,
        175 / 255, 130 / 255, 185 / 255,
        207 / 255, 180 / 255, 213 / 255,
        223 / 255, 205 / 255, 227 / 255
    ]

    print("plot a pie chart with x (custom color)")
    grm.plot.pie(args, c=c)
    input("Press enter to continue")


if __name__ == "__main__":
    test_pie()
