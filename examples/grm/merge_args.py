import math, grm, sys

M_PI = math.pi

plots = [[[0] * 3] * 2] * 4

for i in range(0, 4):
    for j in range(0, 2):
        for k in range(0, 3):
            plots[i][j][k] = i * 3 * 2 + j * 3 + k

subplot = series = None

def cleanup():
    global subplot, series
    if subplot is not None:
        subplot.delete()

    if series is not None:
        series.delete()
    grm.finalize()

series = grm.args.new()
series["x"] = plots[1][0]
series["y"] = plots[1][1]

if not grm.merge(series):
    cleanup()
    sys.exit(1)

series.delete()
series = None

series = grm.args.new()
series["x"] = plots[0][0]
series["y"] = plots[0][1]

if not grm.merge(series):
    cleanup()
    sys.exit(1)

series.delete()
series = None

series = grm.args.new()
series["x"] = plots[1][0]
series["y"] = plots[1][1]
series["series_id"] = 2

if not grm.merge(series):
    cleanup()
    sys.exit(1)

series.delete()
series = None

series = grm.args.new()
series["x"] = plots[3][0]
series["y"] = plots[3][1]
series["id"] = "2.2"

if not grm.merge(series):
    cleanup()
    sys.exit(1)

series.delete()
series = None

series = grm.args.new()
series["x"] = plots[2][0]
series["y"] = plots[2][1]
subplot = grm.args.new()
subplot["series"] = series
subplot["subplot_id"] = 2

if not grm.merge(series):
    cleanup()
    sys.exit(1)

subplot.delete()
subplot = None
series = None

series = grm.args.new()
series["x"] = plots[3][1]
series["id"] = "2.1"

if not grm.merge(series):
    cleanup()
    sys.exit(1)

series.delete()
series = None

series = grm.args.new()
series["x"] = plots[2][0]
series["y"] = plots[2][1]
series["id"] = "2.1"

if not grm.merge(series):
    cleanup()
    sys.exit(1)

series.delete()
series = None

cleanup()
