#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:08:44 2024

@author: aaa
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv
a_1= 0.496
a_2= 0.868
a_1= 0.25**0.5
a_2= 0.75**0.5
# a_1= 0.5**0.5
# a_2= 0.5**0.5
alpha=0.1
a_21=a_2/a_1

def wp1(chi):
    return (1/(1+a_21*np.exp(1j*chi)))

def wp2(chi):
    return (1-wp1(chi))

def wm1(chi):
    return (1/(1-a_21*np.exp(1j*chi)))

def wm2(chi):
    return (1-wm1(chi))

chi=np.linspace(-2*np.pi,np.pi, 1000)
psi_p=(a_1+np.exp(1j*chi)*a_2)/(2**0.5)
psi_w=(a_1*(1-alpha)+np.exp(1j*chi)*a_2)/(2**0.5)
psi_j2=0.5+a_1*a_2*jv(0,5*alpha)*np.cos(chi)
fig = plt.figure(figsize=(6,6), dpi=200)
ax = fig.add_subplot(111)
ax.plot(chi,np.abs(psi_p)**2, label="$I_+$")
ax.plot(chi,np.abs(psi_w)**2, label="$I_{abs}$")
ax.plot(chi,psi_j2, label="$I_{osc.}$")
# ax.plot(chi,-(np.abs(psi_w)**2-np.abs(psi_p)**2)/np.abs(psi_p)**2/2/alpha)
# ax.plot(chi,wp1(chi))
ax.legend()
# ax.set_ylim([-10,10])
plt.show()
