#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 17:25:21 2023

@author: aaa
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq, fft, fftfreq, dct, dst
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
from scipy.stats import norm
a_1=1/5**0.5
a_2=2/5**0.5
a_21=a_2/a_1
def w2(chi):
    return 1-1/(1+a_21*np.exp(1j*chi))

chi=np.linspace(-2*np.pi+1, 2*np.pi-1, 1000)

Re_chi_pi = ((1+2*a_1*a_2*np.cos(chi))*w2(chi).imag+(a_1**2-a_2**2)*w2(chi+np.pi).imag)/(2*a_1*a_2*np.sin(chi))
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
# ax.plot(chi, w2(chi).imag, "r-")
# ax.plot(chi, w2(chi+np.pi/2).imag, "g-")
# ax.plot(chi, w2(chi+np.pi/2).imag-w2(chi).imag, "b-")
# ax.set_ylim([0,2.1])
ax.plot(chi, Re_chi_pi, "r-", label="$\Re{\left(w_{2,+}(\chi+\pi)\\right)}$ from Eq.48")
ax.plot(chi, w2(chi+np.pi).real, "b--", label="$\Re{\left(w_{2,+}(\chi+\pi)\\right)}$ from theory")
ax.set_ylim([0.3,2.1])
ax.set_xlabel("$\chi$")
ax.legend()
plt.show()
