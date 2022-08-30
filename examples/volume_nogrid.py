"""
Draws a cubic volume using the nogrid volume renderer
"""

from math import sqrt
import numpy as np
import gr

data = np.zeros((10, 10, 10, 4))
for i in range(10):
    for j in range(10):
        for k in range(10):
            data[i, j, k] = (i, j, k, 1)

gr.setwindow3d(0, 10, 0, 10, 0, 10)
gr.setspace3d(20, 45, 0, 0)
gr.setcolormap(gr.COLORMAP_VIRIDIS)
gr.volume_interp_tri_linear_init(1, 1, 1)
gr.volume_nogrid(data.reshape(10 * 10 * 10, 4), gr.VOLUME_EMISSION, "trilinear", sqrt(3.))
