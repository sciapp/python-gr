#!/usr/bin/env python
"""
Simple surface plot example
"""

import math
import gr

x = [-2 + i * 0.5 for i in range(0, 29)]
y = [-7 + i * 0.5 for i in range(0, 29)]
z = list(range(0, 841))

for i in range(0, 29):
    for j in range(0, 29):
        r1 = math.sqrt((x[j] - 5)**2 + y[i]**2)
        r2 = math.sqrt((x[j] + 5)**2 + y[i]**2)
        z[i * 29 - 1 + j] = (math.exp(math.cos(r1)) + math.exp(math.cos(r2)) - 0.9) * 25

gr.setcharheight(24.0/500)
gr.settextalign(gr.TEXT_HALIGN_CENTER, gr.TEXT_VALIGN_TOP)
gr.textext(0.5, 0.9, "Surface Example")
(tbx, tby) = gr.inqtextext(0.5, 0.9, "Surface Example")
gr.fillarea(tbx, tby)

gr.setwindow(-2, 12, -7, 7)
gr.setspace(-80, 200, 45, 70)

gr.setcharheight(14.0/500)
gr.axes3d(1, 0, 20, -2, -7, -80, 2, 0, 2, -0.01)
gr.axes3d(0, 1,  0, 12, -7, -80, 0, 2, 0,  0.01)
gr.titles3d("X-Axis", "Y-Axis", "Z-Axis")

gr.surface(x, y, z, 3)
gr.surface(x, y, z, 1)

gr.updatews()
