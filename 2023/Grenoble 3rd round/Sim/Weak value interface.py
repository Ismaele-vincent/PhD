#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 13:14:21 2024

@author: aaa
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.gridspec import GridSpec
matplotlib.rcParams['font.size'] = 13

def w1p(chi, a_21):
    return 1/(1+a_21*np.exp(-1j*chi))

def w2p(chi, a_21):
    return 1/(1+1/a_21*np.exp(1j*chi))

def w1m(chi, a_21):
    return 1/(1-a_21*np.exp(-1j*chi))

def w2m(chi, a_21):
    return 1/(1-1/a_21*np.exp(1j*chi))

chi = np.linspace(-2*np.pi, 2*np.pi, 1000)

a21_0 = 1

# Create the figure and the line that we will manipulate
fig = plt.figure(figsize=(16,9))
gs = GridSpec(2,1, figure=fig, hspace=0)#, hspace=0, bottom=0.2)#,hspace=0, bottom=0,top=0)
axs = [fig.add_subplot(gs[0,0]), fig.add_subplot(gs[1,0]),]
line1pr, = axs[0].plot(chi, w1p(chi, a21_0).real, lw=2, label = "$\Re(w_{1,+})$")
line1pi, = axs[0].plot(chi, w1p(chi, a21_0).imag, lw=2, label = "$\Im(w_{1,+})$")
line2pr, = axs[0].plot(chi, w2p(chi, a21_0).real, lw=2, label = "$\Re(w_{2,+})$")
line2pi, = axs[0].plot(chi, w2p(chi, a21_0).imag, lw=2, label = "$\Im(w_{2,+})$")

line1mr, = axs[1].plot(chi, w1m(chi, a21_0).real, lw=2, label = "$\Re(w_{1,+})$")
line1mi, = axs[1].plot(chi, w1m(chi, a21_0).imag, lw=2, label = "$\Im(w_{1,+})$")
line2mr, = axs[1].plot(chi, w2m(chi, a21_0).real, lw=2, label = "$\Re(w_{2,+})$")
line2mi, = axs[1].plot(chi, w2m(chi, a21_0).imag, lw=2, label = "$\Im(w_{2,+})$")


for ax in axs:
    # ax.yaxis.set_label_position("left")
    ax.set_ylim([-5,5])
axs[0].tick_params(axis="x", labelbottom=False, bottom = False)
axs[1].set_xlabel("$\chi$")
# axs[0].set_ylabel("$\\alpha$")


# Make horizontal sliders.
fig.subplots_adjust(bottom=0.2)

ax_a21 = fig.add_axes([0.25, 0.01, 0.5, 0.03])
a21_slider = Slider(
    ax=ax_a21,
    label="a_21",
    valmin=0,
    valmax=100,
    valinit=a21_0,
)

# The function to be called anytime a slider"s value changes
def update(val):
    line1pr.set_ydata(w1p(chi, a21_slider.val).real)
    line1pi.set_ydata(w1p(chi, a21_slider.val).imag)
    line2pr.set_ydata(w2p(chi, a21_slider.val).real)
    line2pi.set_ydata(w2p(chi, a21_slider.val).imag)
    
    line1mr.set_ydata(w1m(chi, a21_slider.val).real)
    line1mi.set_ydata(w1m(chi, a21_slider.val).imag)
    line2mr.set_ydata(w2m(chi, a21_slider.val).real)
    line2mi.set_ydata(w2m(chi, a21_slider.val).imag)
    
    fig.canvas.draw_idle()

# register the update function with each slider
a21_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.85, 0.025, 0.1, 0.04])
button = Button(resetax, "Reset", hovercolor="0.975")

def reset(event):
    a21_slider.reset()
button.on_clicked(reset)

plt.show()