#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 14:05:36 2023

@author: aaa
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
a_1=1/2**0.5
a_2=1/2**0.5

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def fit_cos_unb(x, A, C, D, Co): 
    return A*((1 - Co)/2 + Co*(1/2+a_1*a_2*np.cos(C*x-D)))

alpha=np.pi/8
w=2*np.pi*10e3
exp_t=5
chi = np.linspace(0, 100,50)
t=np.linspace(0, exp_t*len(chi),1000*len(chi))
phi=alpha*np.sin(w*t)
phi_1=np.reshape(phi, (len(chi), len(t)//len(chi)))

# fig = plt.figure(figsize=(8,6))
# ax = fig.add_subplot(111)
# ax.plot(t[:len(t)//len(chi)],phi_1[0], "b.")


# f=(1+np.cos(chi - phi))/2





# fig = plt.figure(figsize=(8,6))
# ax = fig.add_subplot(111)
# ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
# ax.plot(x_plt,fit_cos(x_plt, *p), "b")
# ax.plot(x_plt,fit_cos_unb(x_plt, *p_unb), "r--")
# ax.set_ylim([0,1500])

plt.show()