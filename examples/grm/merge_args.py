import math, grm, sys

plots = [[[0] * 3] * 2] * 4

for i in range(0, 4):
    for j in range(0, 2):
        for k in range(0, 3):
            plots[i][j][k] = i * 3 * 2 + j * 3 + k


series = grm.args.new({"x": plots[1][0], "y": plots[1][1]})

if not grm.merge(series):
    sys.exit(1)

del series

series = grm.args.new({"x": plots[0][0], "y": plots[0][1]})

if not grm.merge(series):
    sys.exit(1)

del series

series = grm.args.new({"x": plots[1][0], "y": plots[1][1], "series_id": 2})

if not grm.merge(series):
    sys.exit(1)

del series

series = grm.args.new({"x": plots[3][0], "y": plots[3][1], "id": "2.2"})

if not grm.merge(series):
    sys.exit(1)

del series

series = grm.args.new({"x": plots[2][0], "y": plots[2][1]})
subplot = grm.args.new({"series": series, "subplot_id": 2})

if not grm.merge(series):
    sys.exit(1)

del subplot
del series

series = grm.args.new()
series["x"] = plots[3][1]
series["id"] = "2.1"

if not grm.merge(series):
    sys.exit(1)

del series

series = grm.args.new({"x": plots[2][0], "y": plots[2][1], "id": "2.1"})

if not grm.merge(series):
    sys.exit(1)
