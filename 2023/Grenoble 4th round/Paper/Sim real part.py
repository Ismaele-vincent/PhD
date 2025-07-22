#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:08:44 2024

@author: aaa
"""

import os
import numpy as np
import matplotlib.pyplot as plt
th= np.pi/4
a_2= np.sin(th/2)
a_1= np.cos(th/2)
# a_1= 1/5**0.5
# a_2= 2/5**0.5
# a_1= 0.51**0.5
# a_2= 0.49**0.5
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
# psi_p=(a_1+np.exp(1j*chi)*a_2)/(2**0.5)
# psi_m=(a_1-np.exp(1j*chi)*a_2)/(2**0.5)
# M=np.abs(psi_p/psi_m)
# th= np.angle(psi_p/psi_m)

w_pol= 0.5*(1+np.sin(th)*np.exp(-1j*chi)+np.cos(th))/(1+np.sin(th)*np.cos(chi))

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
# ax.plot(chi,np.abs(psi_p)**2)
# ax.plot(chi,np.abs(psi_m)**2)
# Rep1=wm1(chi).imag/(M*np.sin(th))-wp1(chi).imag/np.tan(th)
# Rep2=-wp2(chi).imag/np.tan(th)-wm2(chi).imag/(M*np.sin(th))
# ax.plot(chi,Rep1)
# ax.plot(chi, abs(psi_p)**2*(abs(wp1(chi))**2*0-wp1(chi).real),"-")
ax.plot(chi, wp1(chi).real,"-")
ax.plot(chi, w_pol.real,"--")
# ax.plot(chi, abs(wp2(chi))**2-wp2(chi).real,"--")
# ax.plot(chi, wp2(chi).real,"--")
# ax.set_ylim([0,2])
plt.show()
