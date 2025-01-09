#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 13:56:33 2024

@author: aaa
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
a_1=1/5**0.5
a_2=2/5**0.5
a_21=a_2/a_1
def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def w1(chi, a_21):
    return 1/(1+a_21*np.exp(1j*chi))

def w2(chi, a_21):
    return 1-w1(chi, a_21)

def Ip1(chi, chi_0, a_21):
    p_psi= (a_1+a_2*np.exp(1j*chi_0))/2**0.5
    w1p=w1(chi_0, a_21)
    return abs(p_psi)**2*(1+2*(abs(w1p)**2-w1p.real)*(1-np.cos(chi))+2*w1p.imag*np.sin(chi))

def Ip2(chi, chi_0, a_21):
    p_psi= (a_1+a_2*np.exp(1j*chi_0))/2**0.5
    w2p=w2(chi_0, a_21)
    return abs(p_psi)**2*(1+2*(abs(w2p)**2-w2p.real)*(1-np.cos(chi))-2*w2p.imag*np.sin(chi))

chi_plt=np.linspace(-2*np.pi, 2*np.pi, 200)
chi_0=np.pi/8
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.plot(chi_plt, Ip1(chi_plt,chi_0, a_21))
ax.plot(chi_plt, Ip2(chi_plt,chi_0, a_21), "--")

w1r=a_1**2/(2*Ip1(0,chi_plt,a_21))-(Ip1(np.pi, chi_plt, a_21)-Ip1(0, chi_plt, a_21))/(4*Ip1(0,chi_plt,a_21))
w2r=a_2**2/(2*Ip1(0,chi_plt,a_21))-(Ip1(np.pi, chi_plt, a_21)-Ip1(0, chi_plt, a_21))/(4*Ip1(0,chi_plt,a_21))
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.plot(chi_plt, w1(chi_plt,a_21).real+w2(chi_plt,a_21).real)
ax.plot(chi_plt, w1r+w2r, "--")
ax.set_ylim(0,2)