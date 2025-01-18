#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:13:33 2025

@author: aaa
"""

import numpy as np
import matplotlib.pyplot as plt

# a_1= 0.751
# a_1_err= 0.003
# a_2= 0.660
# a_2_err=0.003

a_1= 0.5**0.5
a_1_err=0.003
a_2= (1-a_1**2)**0.5
a_2_err=0.002

# a_1= 0.496
# a_1_err= 0.003
# a_2= (1-a_1**2)**0.5
# a_2_err= 0.002

rho=np.pi/8
# rho=np.linspace(0,np.pi/8,100)
F = abs(a_1**2+a_2**2*np.exp(1j*rho))**2
F1=a_1**4+a_2**4+2*a_1**2*a_2**2*np.cos(rho)
F2=1-4*a_1**2*a_2**2*np.sin(rho/2)**2
# plt.plot(rho, F)
# # plt.plot(rho, F1,"--")
# plt.plot(rho, F2,"--")
print(F, F1, F2)
