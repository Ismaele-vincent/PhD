#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 14:41:01 2024

@author: aaa
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq, fft, fftfreq, dct, dst
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
from scipy.stats import norm
from scipy.stats import rayleigh

np.random.seed()

def I(x, A, C, D):
    return A/2*(1+C*np.cos(x-D)) 

A=1000
C=0.7
D=0
chi= np.linspace(-2*np.pi,2*np.pi, 50)
chi_plt= np.linspace(-2*np.pi,2*np.pi, 100)
func=I(chi, A, C, D) 
noise= np.random.normal(0, func**0.5)
data = func+noise
data_c1=(data-A*(1-C)/2)/C
data_c2=data+A/2*(1-C)*np.cos(chi)
fig = plt.figure(figsize=(10,6), dpi=200)
ax = fig.add_subplot(111)
ax.plot(chi_plt, I(chi_plt,A, 1, D), "r-")
# ax.plot(chi, I(chi,A, 1, D), "r.")
ax.errorbar(chi, data, yerr=data**0.5, fmt="k.", capsize=5)
ax.errorbar(chi, data_c1, yerr=data**0.5, fmt="g.", capsize=5)
ax.errorbar(chi, data_c2, yerr=data**0.5, fmt="b.", capsize=5)
print(np.average(data_c1-I(chi,A, 1, D))**2,np.average(data_c2-I(chi,A, 1, D))**2)
plt.show()