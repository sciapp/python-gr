#!/usr/bin/env python
# -*- no-plot -*-
"""
Multiline text example
"""

from math import sin, cos, pi
import time

import gr

horizontal_alignment = {
    'Left': 1,
    'Center': 2,
    'Right': 3
}

vertical_alignment = {
    'Top': 1,
    'Cap': 2,
    'Half': 3,
    'Base': 4,
    'Bottom': 5
}

gr.selntran(0)
gr.setcharheight(0.024)

for angle in range(361):

    gr.setcharup(sin(-angle * pi / 180), cos(-angle * pi / 180))
    gr.setmarkertype(2)
    gr.clearws()

    for halign in horizontal_alignment:
        for valign in vertical_alignment:
            gr.settextalign(horizontal_alignment[halign], vertical_alignment[valign])
            x = -0.1 + horizontal_alignment[halign] * 0.3
            y = 1.1 - vertical_alignment[valign] * 0.2
            s = halign + '\n' + valign + '\n' + 'third line'
            gr.polymarker([x], [y])
            gr.text(x, y, s)
            tbx, tby = gr.inqtext(x, y, s)
            gr.fillarea(tbx, tby)

    gr.updatews()
    time.sleep(0.02)
