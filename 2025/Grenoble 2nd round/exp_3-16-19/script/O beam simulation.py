# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 11:07:01 2025

@author: S18
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as fit
colors=["k","r--","g--","b--"]
a_1=1/3**0.5
a_2=1/3**0.5
a_3=1/3**0.5

T_1=2222
T_2=2525
T_3=2352
a_1=(T_1/(T_1+T_2+T_3))**0.5
a_2=(T_2/(T_1+T_2+T_3))**0.5
a_3=(T_3/(T_1+T_2+T_3))**0.5

"""
psi +exp(-i pi/3) +1  +exp(i 2pi/3) 
"""
# chi_1_0=-np.pi/3
# chi_2_0=0
# chi_3_0=2*np.pi/3

"""
psi +1 -i -1
"""
# chi_1_0=0
# chi_2_0=-np.pi/2
# chi_3_0=-np.pi

"""
psi +1 -1 -i
"""
chi_1_0=0
chi_2_0=-np.pi
chi_3_0=-np.pi/2

chi=np.linspace(-np.pi, 2*np.pi, 100)
def I_psi(chi_1,chi_2,chi_3):
    I_psi = 1/3*abs(a_1*np.exp(1j*(chi_1_0+chi_1))+a_2*np.exp(1j*(chi_2_0+chi_2))+a_3*np.exp(1j*(chi_3_0+chi_3)))**2
    return I_psi

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

p,cov=fit(fit_cos, chi, I_psi(chi,0,0), p0=[0.3,0.2, 1, -np.pi/6])
print(p,-np.pi/3)
fig = plt.figure(figsize=(5,6), dpi=150)
# fig.suptitle("$|\\psi_{in}>=(|1>+|2>+|3>)/\\sqrt{3}$")
gs = fig.add_gridspec(3,1)
axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[1, 0]),fig.add_subplot(gs[2, 0])]

Dchi=[0, -np.pi/2, np.pi/2, np.pi]
labels=["0","$-\pi/2$", "$\pi/2$","$\pi$"]
for i in [0,1,2,3]:
    axs[0].plot(chi, I_psi(chi+Dchi[i],0,0), colors[i], label=labels[i])
    axs[1].plot(chi, I_psi(0,chi+Dchi[i],0), colors[i])
    axs[2].plot(chi, I_psi(0,0,chi+Dchi[i]), colors[i])
fig.legend(loc=9, ncol=4)
axs[2].plot(np.pi/6, I_psi(0,0, np.pi/6), "ko")
axs[1].plot(2*np.pi/3+5*np.pi/6, I_psi(0,2*np.pi/3,0), "ko")
for ax in axs:
    ax.set_ylim([0,1])
    ax.grid(True, ls="dotted")
    ax.set_xticks([0,np.pi/2,np.pi,3*np.pi/2, 2*np.pi])
    ax.set_xticklabels(["$\mathdefault{0}$","$\mathdefault{\pi/2}$","$\mathdefault{\pi}$","$\mathdefault{3\pi/2}$","$\mathdefault{2\pi}$"])