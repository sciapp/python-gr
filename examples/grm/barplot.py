from typing import Dict, Iterable, Union

import grm


_ElemType = grm.args._ElemType


y = (4.0, 5.0, 8.0)
yy1 = [4.0, 8.0, 2.0]
yy2 = [7.0, 3.0, 9.0]
yy3 = [1.0, 4.0, 6.0]
inner_yy2_1 = [5.0, 2.0]
inner_yy2_2 = [3.0]
inner_yy2_3 = [9.0]
yy_pos_neg = [5.0, -5.0, 3.0, -3.0]
c = [984, 992, 993]
c2 = [997, 998, 999]
c_rgb = [
    0.5, 0.4, 0.3,
    0.3, 0.4, 0.5,
    0.4, 0.3, 0.5
]
inner_c = [989, 984]
inner_c_rgb = [
    0.5, 0.4, 0.3,
    0.8, 0.1, 0.1
]
bar_color = 992
edge_color = 989
bar_width = 0.5
edge_width = 1.5
xticklabels = ["eins", "zwei", "drei"]
ylabels = ["4", "5", "8"]
yy1_labels = ["4", "8", "2"]
yy2_labels = ["7", "3", "9"]
yy3_labels = ["1", "4", "6"]
yy2_labels_for_inner = ["5", "2", "3", "9"]
yy_pos_neg_labels = ["5", "-5", "3", "-3"]
indices = [1, 2]


# Draw the bar plot
args: Dict[str, _ElemType] = {"y": y}
grm.plot.barplot(args)
input("Press enter to continue")

# Draw the bar plot with locations specified by x and y values in the bars
args["x_tick_labels"] = xticklabels
args["y_labels"] = ylabels
grm.plot.barplot(args)
input("Press enter to continue")

# Draw the bar plot with different bar_width, edge_width, edge_color and bar_color
args["edge_width"] = edge_width
args["bar_width"] = bar_width
args["edge_color"] = edge_color
args["bar_color"] = bar_color
grm.plot.barplot(args)
input("Press enter to continue")
# or
args["bar_color"] = [0.66, 0.66, 0.66]
args["edge_color"] = [0.33, 0.33, 0.33]
grm.plot.barplot(args)
input("Press enter to continue")

# TODO does not display any change
# Draw the bar plot with bars that have individual bar_color, edge_color, edge_with
ind_bar_color: Iterable[Dict[str, _ElemType]] = [
    {"indices": indices, "rgb": (0.0, 0.666, 0.333)},
    {"indices": 3, "rgb": (0.111, 0.222, 0.333)}
]
ind_edge_color = {"indices": 3, "rgb": (0.9, 0.6, 0.3)}
ind_edge_width = {"indices": 3, "width": 5.0}
grm.plot.barplot(args, ind_bar_color=ind_bar_color, ind_edge_color=ind_edge_color, ind_edge_width=ind_edge_width)
input("Press enter to continue")

# Draw the bar plot with colorlist
args.clear()
args["y"] = y
grm.plot.barplot(args, c=c)
input("Press enter to continue")
# or
grm.plot.barplot(args, c=c_rgb)
input("Press enter to continue")

# Draw a 2D bar plot lined
series: Iterable[Dict[str, _ElemType]] = [
    {"y": yy1, "y_labels": yy1_labels},
    {"y": yy2, "y_labels": yy2_labels},
    {"y": yy3, "y_labels": yy3_labels}
]
abc: Dict[str, _ElemType] = {}
grm.plot.barplot(series=series, style="lined")
input("Press enter to continue")

# Draw a 2D bar plot stacked
grm.plot.barplot(style="stacked", series=series)
input("Press enter to continue")

# Draw a 2D bar plot with colorlist
series = [
    {"y": yy1, "c": c},
    {"y": yy2},
    {"y": yy3}
]
grm.plot.barplot(style="stacked", series=series)
input("Press enter to continue")

# Draw a 2D bar plot stacked with positive and negative values
# The positive and negative values are stacked separately
args.clear()
args["y"] = yy_pos_neg
args["style"] = "stacked"
args["y_labels"] = yy_pos_neg_labels
grm.plot.barplot(args)
input("Press enter to continue")

# Draw a bar plot that is lined and stacked with inner color list (rgb)
args.clear()
inner_series: Iterable[Dict[str, Union[Iterable[int], Iterable[float]]]] = [
    {"y": inner_yy2_1, "c": inner_c_rgb},
    {"y": inner_yy2_2},
    {"y": inner_yy2_3}
]
series = [
    {"y": yy1, "c": c_rgb},
    {"inner_series": inner_series, "c": c_rgb},
    {"y": yy3, "c": c_rgb}
]
grm.plot.barplot(style="lined", series=series)
input("Press enter to continue")

# Draw a bar plot that is lined and stacked with inner color list and ylabels
inner_series = [
    {"y": inner_yy2_1, "c": inner_c},
    {"y": inner_yy2_2},
    {"y": inner_yy2_3}
]
series = [
    {"y": yy1, "y_labels": yy1_labels},
    # ylabels for series containing inner_series can alternatively be put in each inner_series
    {"inner_series": inner_series, "y_labels": yy2_labels_for_inner},
    {"y": yy3, "y_labels": yy3_labels}
]

grm.plot.barplot(style="lined", series=series)
input("Press enter to continue")
