#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:08:44 2024

@author: aaa
"""

import os
import numpy as np
import matplotlib.pyplot as plt
a_1= 0.496
a_2= 0.868
a_1= 0.25**0.5
a_2= 0.75**0.5
# a_1= 0.5**0.5
# a_2= 0.5**0.5
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
psi_m=(a_1-np.exp(1j*chi)*a_2)/(2**0.5)
M=np.abs(psi_p/psi_m)
th= np.angle(psi_p/psi_m)
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
# ax.plot(chi,np.abs(psi_p)**2)
# ax.plot(chi,np.abs(psi_m)**2)
# Rep1=wm1(chi).imag/(M*np.sin(th))-wp1(chi).imag/np.tan(th)
# Rep2=-wp2(chi).imag/np.tan(th)-wm2(chi).imag/(M*np.sin(th))
ax.plot(chi,M)
ax.plot(chi,np.sin(th))
ax.plot(chi,1/np.tan(th))
# ax.plot(chi, Rep2)
ax.set_ylim([-10,10])
plt.show()