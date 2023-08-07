import grm


def test_recv() -> None:
    with grm.net.open(True, "localhost", 8002, None, None) as handle:
        args = {}
        res = handle.recv({"title": "test"})
        grm.plot.plot(res)

    input("Press enter to continue")


if __name__ == "__main__":
    test_recv()
