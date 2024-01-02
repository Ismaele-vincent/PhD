#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 10:41:40 2023

@author: aaa
"""

import numpy as np
import matplotlib.pyplot as plt

def w2(chi, a_21):
    return (1-1/(1+a_21*np.exp(1j*chi)))

chi=np.linspace(-2*np.pi,2*np.pi, 1000)

plt.plot(chi, w2(chi,2).imag, "b-")
plt.plot(chi, w2(chi,2).real, "r-")
plt.plot(chi, w2(chi,1/2).imag, "y--")
plt.plot(chi, w2(chi,1/2).real, "k--")
