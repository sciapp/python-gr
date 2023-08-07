import grm


def test_send() -> None:
    plots = [
        [
            [0.0, 0.5, 1.0], [0.1, 0.25, 0.9]
        ],
        [
            [0.0, 0.5, 1.0], [0.2, 0.75, 0.95]
        ]
    ]
    labels = ["plot 1", "plot 2"]

    series = [
        {
            "x": plots[0][0],
            "y": plots[0][1]
        },
        {
            "x": plots[1][0],
            "y": plots[1][1]
        }
    ]
    args = {
        "series": series,
        "labels": labels,
        "kind": "line"
    }

    with grm.net.open(False, "localhost", 8002, None, None) as handle:
        handle.send_args(args)


if __name__ == "__main__":
    test_send()
