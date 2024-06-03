#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 16:13:12 2024

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

a_1=0.5**0.5
a_2=0.5**0.5
alpha_1 = [0, np.pi/3, np.pi/2,np.pi]
xi_1=2
xi_2=-0.5
f_1=2
f_2=3
chi_plt=np.linspace(-2*np.pi,2*np.pi,1000)


def Int_O_beam(chi, alpha):
    return 1/2 + a_1*a_2*jv(0,alpha)*np.cos(chi)

alpha_l=["$\\alpha_1=0$","$\\alpha_1=\\dfrac{\pi}{3}$", "$\\alpha_1=\\dfrac{\pi}{2}$", "$\\alpha_1=\pi$"]
fig = plt.figure(figsize=(5,3))
ax = fig.add_subplot(111)   
for i in range(len(alpha_1)):
    ls=["-", "-","-", "-"]
    colors=["k","#f10d0c","#00a933","#5983b0"]
    # ax.errorbar(time, matrix[i], yerr= matrix_err[i], fmt="."+colors[i%5], capsize=3, label="$\chi=$"+str("%.2f"%chi[i],))
    ax.plot(chi_plt, Int_O_beam(chi_plt, alpha_1[i]),ls=ls[i], color=colors[i], label=alpha_l[i])
    # ax.set_title(str("%.2f"%chi[i],))
    # ax.set_xlim([-5,5])
    ax.set_xlabel("$\\chi$")
    ax.set_ylabel("Average time-integrated intensity")
# fig.suptitle("$\\alpha_1=\\alpha_2=\pi/8$\t$\omega_1 = 4\pi 10^{3}$ rad\t$\omega_2 = 6\pi 10^{3}$ rad", fontsize=11)
# ax.legend(ncol=2, bbox_to_anchor=(0.5,1.1), loc="center")
ax.legend(framealpha=1, loc=5)
plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images/time int sim.pdf", format="pdf",bbox_inches="tight")

# plt.show()