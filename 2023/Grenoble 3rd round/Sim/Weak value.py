#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 10:41:40 2023

@author: aaa
"""

import numpy as np
import matplotlib.pyplot as plt

a_1= 0.2**0.5
a_2= 0.8**0.5
a_21=a_2/a_1
def w1(chi, a_21):
    return 1/(1+a_21*np.exp(1j*chi))

def w2(chi, a_21):
    return 1-w1(chi, a_21)



chi=np.linspace(-2*np.pi,2*np.pi, 1000)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)

ax.plot(chi, w1(chi,a_21).real-w2(chi,a_21).real, "k--")
ax.plot(chi, w1(chi,a_21).imag-w2(chi,a_21).imag, "r--")
# ax.plot(chi, - a_1*a_2*np.sin(chi)/(1+2*a_1*a_2*np.cos(chi)), "g--")

ax.set_ylim([-3,3])