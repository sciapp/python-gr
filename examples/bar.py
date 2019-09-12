from gr.pygr.mlab import bar
import numpy as np
import time

# Create example data
y = np.random.uniform(0, 10, 5)

# Draw the bar plot
bar(y)
time.sleep(3)

# Draw the bar plot with locations specified by x
x = ['a', 'b', 'c', 'd', 'e']
bar(y, xnotations=x)
time.sleep(3)

# Draw the bar plot with different bar_width, edge_width, edge_color and bar_color
# (bar_width: float in (0;1], edge_width: float value bigger or equal to 0, color: int in [0;1255] or rgb list)
bar(y, bar_width=0.6, edge_width=1.5, bar_color=992, edge_color=989)
time.sleep(3)
bar(y, bar_color=[0.66, 0.66, 0.66], edge_color=[0.33, 0.33, 0.33])
time.sleep(3)

# Draw the bar plot with bars that have individual bar_color, edge_color, edge_with
bar(y, ind_bar_color=[1, [0.4, 0.4, 0.4]], ind_edge_color=[[1, 2], [0.66, 0.33, 0.33]], ind_edge_width=[[1, 2], 3])
time.sleep(3)

# Draw the bar plot with bars that have multiple individual colors
bar(y, ind_bar_color=[[1, [1, 0.3, 0]], [[2, 3], [1, 0.5, 0]]])
time.sleep(3)

# Draw the bar plot with default bar_width, edge_width, edge_color and bar_color
bar(y, bar_width=None, edge_width=None, bar_color=None, edge_color=None)
time.sleep(3)

# Draw the bar plot with colorlist
bar(y, [989, 982, 980, 981, 996])
time.sleep(3)

# Create example sublist data
yy = np.random.rand(3, 3)

# Draw the bar plot lined / stacked / with colorlist
bar(yy, bar_style='lined')
time.sleep(3)
bar(yy, bar_style='stacked')
time.sleep(3)
bar(yy, [989, 998, 994])
time.sleep(3)
