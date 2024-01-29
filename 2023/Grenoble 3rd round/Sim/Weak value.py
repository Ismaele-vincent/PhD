#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 10:41:40 2023

@author: aaa
"""

import numpy as np
import matplotlib.pyplot as plt

a_21=2

def w1(chi, a_21):
    return 1/(1+a_21*np.exp(1j*chi))

def w2(chi, a_21):
    return 1-w1(chi, a_21)



chi=np.linspace(-2*np.pi,2*np.pi, 1000)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.plot(chi, w2(chi,a_21).imag, "b-")
ax.plot(chi, w2(chi,a_21).real, "r-")

ax.plot(chi, w1(chi,a_21).imag, "y--")
ax.plot(chi, w1(chi,a_21).real, "k--")

ax.plot(chi, -w1(chi,a_21).real+w2(chi,a_21).real, "g--")

ax.set_ylim([-3,3])