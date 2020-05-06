#!/usr/bin/env python
# -*- animation -*-
"""
Animation of a damped pendulum
"""

import numpy as np
import time
import gr

try:
    from time import perf_counter
except ImportError:
    from time import clock as perf_counter


def rk4(x, h, y, f):
    k1 = h * f(x, y)
    k2 = h * f(x + 0.5 * h, y + 0.5 * k1)
    k3 = h * f(x + 0.5 * h, y + 0.5 * k2)
    k4 = h * f(x + h, y + k3)
    return x + h, y + (k1 + 2 * (k2 + k3) + k4) / 6.0


def damped_pendulum_deriv(t, state):
    theta, omega = state
    return np.array([omega, -gamma * omega - 9.81 / L * np.sin(theta)])


def pendulum(t, theta, omega, acceleration):
    gr.clearws()
    gr.setviewport(0, 1, 0, 1)

    x = [0.5, 0.5 + np.sin(theta) * 0.4]
    y = [0.8, 0.8 - np.cos(theta) * 0.4]
    # draw pivot point
    gr.fillarea([0.46, 0.54, 0.54, 0.46], [0.79, 0.79, 0.81, 0.81]),

    gr.setlinecolorind(1)
    gr.setlinewidth(2)
    gr.polyline(x, y)  # draw rod
    gr.setmarkersize(5)
    gr.setmarkertype(gr.MARKERTYPE_SOLID_CIRCLE)
    gr.setmarkercolorind(86)
    gr.polymarker([x[1]], [y[1]])  # draw bob
    gr.setlinecolorind(4)
    V = 0.05 * omega  # show angular velocity
    gr.drawarrow(x[1], y[1], x[1] + V * np.cos(theta), y[1] + V * np.sin(theta))
    gr.setlinecolorind(2)
    A = 0.05 * acceleration  # show angular acceleration
    gr.drawarrow(x[1], y[1], x[1] + A * np.sin(theta), y[1] + A * np.cos(theta))

    gr.settextfontprec(2, gr.TEXT_PRECISION_STRING)
    gr.setcharheight(0.032)
    gr.settextcolorind(1)
    gr.textext(0.05, 0.95, 'Damped Pendulum')
    gr.setcharheight(0.040)
    gr.mathtex(0.4, 0.22, '\\omega=\\dot{\\theta}')
    gr.mathtex(0.4, 0.1, '\\dot{\\omega}=-\\gamma\\omega-\\frac{g}{l}sin(\\theta)')
    gr.setcharheight(0.028)
    gr.textext(0.05, 0.22, 't:%7.2f' % t)
    gr.textext(0.05, 0.16, '\\theta:%7.2f' % (theta / np.pi * 180))
    gr.settextcolorind(4)
    gr.textext(0.05, 0.10, '\\omega:%7.2f' % omega)
    gr.settextcolorind(2)
    gr.textext(0.05, 0.04, 'y_{A}:%6.2f' % acceleration)

    gr.updatews()


theta = 70.0  # initial angle
gamma = 0.1  # damping coefficient
L = 1  # pendulum length

t = 0
dt = 0.04
state = np.array([theta * np.pi / 180, 0])

now = perf_counter()

while t < 30:
    start = now

    t, state = rk4(t, dt, state, damped_pendulum_deriv)
    theta, omega = state
    acceleration = np.sqrt(2 * 9.81 * L * (1 - np.cos(theta)))
    pendulum(t, theta, omega, acceleration)

    now = perf_counter()
    if start + dt > now:
        time.sleep(start + dt - now)
