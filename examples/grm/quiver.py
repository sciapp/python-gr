import grm


X_DIM = 30
Y_DIM = 20

X_MIN = -1.0
X_MAX = 1.0
Y_MIN = -1.0
Y_MAX = 1.0


def test_quiver() -> None:
    x = [X_MIN + (X_MAX - X_MIN) * (i / (X_DIM - 1)) for i in range(X_DIM)]
    y = [Y_MIN + (Y_MAX - Y_MIN) * (i / (Y_DIM - 1)) for i in range(Y_DIM)]
    u = [0.0] * (X_DIM * Y_DIM)
    v = [0.0] * (X_DIM * Y_DIM)

    for i in range(X_DIM):
        for j in range(Y_DIM):
            u[j * X_DIM + i] = X_MIN + (X_MAX - X_MIN) * (i / (X_DIM - 1))
            v[j * X_DIM + i] = Y_MIN + (Y_MAX - Y_MIN) * (j / (Y_DIM - 1))

    print("plot a quiver with x, y and z")
    grm.plot.quiver(x=x, y=y, u=u, v=v)
    input("Press enter to continue")


if __name__ == "__main__":
    test_quiver()
