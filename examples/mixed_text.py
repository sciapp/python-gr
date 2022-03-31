# coding: utf8

from gr import selntran, settextfontprec, settextalign, setcharheight, clearws, setcharup, text, inqtext, fillarea, updatews
from math import pi, sin, cos
from numpy import linspace

s = 'Using inline math $\\frac{2hc^2}{\\lambda^5} \\frac{1}{e^{\\frac{hc}{\\lambda k_B T}} - 1}$ in GR text\nmixed with raw strings ' + r'$- \frac{{\hbar ^2}}{{2m}}\frac{{\partial ^2 \psi (x,t)}}{{\partial x^2 }} + U(x)\psi (x,t) = i\hbar \frac{{\partial \psi (x,t)}}{{\partial t}}$' + '\n– with line breaks\nand UTF-8 characters (ħπ),\nand rendered using GR\'s text attributes'

selntran(0)

settextfontprec(232, 3)
settextalign(2, 3)
setcharheight(0.02)

for phi in linspace(0, 2 * pi, 360):
    clearws()
    setcharup(sin(phi), cos(phi))
    text(0.5, 0.5, s)
    tbx, tby = inqtext(0.5, 0.5, s)
    fillarea(tbx, tby)
    updatews()
