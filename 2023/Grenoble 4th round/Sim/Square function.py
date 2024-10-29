#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 11:56:53 2023

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

def sinc(x,A, B):
    return A*(abs(np.sinc(B*x)))
    

pi=np.pi
np.random.seed(12345)

N=500
S_F=16.6667
t= np.linspace(0,N*S_F, N, endpoint=False)
print(N*S_F)
func= 500+t*0#+ 20*np.sin(2*pi*2e-3*t) + 30*np.sin(3*2*np.pi*t) 
func[:6]=0
func[66:]=0
noise= np.random.normal(0, func**0.5)
data= func#+noise
fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111)
ax.plot(t, func, "r-")
ax.errorbar(t, data, yerr=data**0.5, fmt="ko", capsize=5)

xf = fftfreq(N, S_F)*1e3
yf = fft(func)
p, cov = fit(sinc, xf, abs(yf), p0=(3000, 1))

fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111)
ax.errorbar(xf, abs(yf), fmt="ko", capsize=5)
ax.plot(xf, sinc(xf,*p))
ax.set_xlim([-5,5])