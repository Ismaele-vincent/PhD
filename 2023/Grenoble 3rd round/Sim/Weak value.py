#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 10:41:40 2023

@author: aaa
"""

import numpy as np
import matplotlib.pyplot as plt

a_1= 1/5**0.5
a_2= 2*a_1
a_21=2
def w1(chi, a_21):
    return 1/(1+a_21*np.exp(1j*chi))

def w2(chi, a_21):
    return 1-w1(chi, a_21)

chi=np.linspace(-2*np.pi,2*np.pi, 1000)
# chi=np.array([-2.57373397e+00, -2.17296830e+00, -1.73880549e+00, -1.30767879e+00,
#  -8.40118838e-01, -4.39353167e-01, -5.19035769e-03,  4.62369591e-01,
#   8.60099158e-01,  1.32765911e+00,  1.72842478e+00,  2.22938187e+00,
#   2.66354467e+00,  3.06431035e+00,  3.49543705e+00,  3.96299700e+00,
#   4.39715981e+00,  4.83132262e+00,  5.26548543e+00,  5.66321500e+00,
#   6.13077494e+00,  6.56493775e+00])
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)

ax.plot(chi, w1(chi, a_21).real, "k-")
ax.plot(chi, w2(chi, a_21).real, "r--")

# ax.plot(chi, - a_1*a_2*np.sin(chi)/(1+2*a_1*a_2*np.cos(chi)), "g--")

# ax.set_ylim([-3,3])