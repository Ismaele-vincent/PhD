#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 11:56:38 2023

@author: aaa
"""

import os
import numpy as np
import shutil
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq, fft, fftfreq, dct, dst
from mpl_toolkits import mplot3d
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from PIL import Image as im
from scipy.optimize import curve_fit as fit
from scipy.special import jv

mu_N=-9.6623651#*1e-27 J/T
hbar= 6.62607015/(2*np.pi) #*1e-34 J s
f_1=10
B_1=10
B_0=18.55
T=10
v0=2060.43 #m/s
phi_1=0
order=4
w_ps=3
rad=np.pi/180

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

a_1=0.5**0.5
a_2=0.5**0.5
alpha_1 = -np.pi/16#alpha(19.4,1,5)
alpha_2 = np.pi/16
xi_1=-1
xi_2=1.2
f_1=2
f_2=3
time_plt=np.linspace(0,2000,1000)


def O_beam(t, chi):
    return 1/2 + a_1*a_2*np.cos(chi+alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)-alpha_2*np.sin(2*np.pi*1e-3*f_2*t+xi_2))
print(np.pi/3)
chi_aus=[0,np.pi/3, np.pi, 4/3*np.pi]
print(chi_aus)
chi_l=["$\\chi=0$","$\\chi=\\dfrac{\pi}{3}$", "$\\chi=\pi$", "$\\chi=\\dfrac{4}{3}\pi$"]
fig = plt.figure(figsize=(5,2))
ax = fig.add_subplot(111)   
for i in range(len(chi_aus)):
    colors=["k","#f10d0c","#00a933","#5983b0"]
    # ax.errorbar(time, matrix[i], yerr= matrix_err[i], fmt="."+colors[i%5], capsize=3, label="$\chi=$"+str("%.2f"%chi[i],))
    ax.plot(time_plt, O_beam(time_plt, chi_aus[i]),"-", color=colors[i], label=chi_l[i])
    # ax.set_title(str("%.2f"%chi[i],))
    ax.set_xlim([0,2000])
    ax.set_ylim([0,1.05])
    ax.set_xlabel("Time [$\mu$ s]")
    ax.set_ylabel("Intesity $I_+$ (arb.)")
# fig.suptitle("$\\alpha_1=\\alpha_2=\pi/8$\t$\omega_1 = 4\pi 10^{3}$ rad\t$\omega_2 = 6\pi 10^{3}$ rad", fontsize=11)
# ax.legend(ncol=2, bbox_to_anchor=(0.5,1.1), loc="center")
ax.legend(framealpha=1, loc=10, bbox_to_anchor=(1.15,0.5))
plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images 1 column/time resolved sim.pdf", format="pdf",bbox_inches="tight")

# plt.show()