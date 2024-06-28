#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 15:14:27 2024

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
colors=["k","#f10d0c","#00a933","#5983b0"]

fig = plt.figure(figsize=(10,0.5), dpi=200)
# fig.suptitle(inf_file_name)
gs = GridSpec(2,2, figure=fig, wspace=0, hspace=0, top=1, bottom=0.135)
ax=fig.add_subplot()
ax.tick_params(axis="both", labelleft=False, left = False, labelbottom=False, bottom = False)
ax.set_frame_on(False)
ax.errorbar([],[], fmt="k--", alpha=0.5,label="$w^\Im_{+,1}$  Theory")    
ax.errorbar([], [], [], fmt="k.", capsize=3, label="$w^\Im_{+,1}$ Data")
ax.errorbar([],[], fmt="--", color=colors[2], alpha=0.5,label="$w^\Im_{+,2}$  Theory")    
ax.errorbar([], [], [], fmt=".", color=colors[2], capsize=3, label="$w^\Im_{+,2}$ Data")
fig.legend(ncol=4, framealpha=1,frameon=0, loc=10)
plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images/legend Im ver2.pdf", format="pdf",bbox_inches="tight")

# fig = plt.figure(figsize=(8.5,0.1), dpi=200)# ax.plot([], "r--", alpha=0.5,label="$\Re(w_{+,1})$  Theory")    
# ax.errorbar([], [], [], fmt="r.", capsize=3, label="$\Re(w_{+,1})$ Data")
# ax.plot([], "b--", alpha=0.5,label="$\Re(w_{+,2})$  Theory")    
# ax.errorbar([], [], [], fmt="b.", capsize=3, label="$\Re(w_{+,2})$ Data")
# fig.suptitle(inf_file_name)
# gs = GridSpec(2,2, figure=fig, wspace=0, hspace=0, top=1, bottom=0.135)
# ax=fig.add_subplot()
# ax.tick_params(axis="both", labelleft=False, left = False, labelbottom=False, bottom = False)
# ax.set_frame_on(False)
# ax.plot([], "b--", alpha=0.5,label="$\Re(w_{+,1})$  Theory")    
# ax.errorbar([], [], [], fmt="b.", capsize=3, label="$\Re(w_{+,1})$ Data")
# ax.plot([], "r--", alpha=0.5,label="$\Re(w_{+,2})$  Theory")    
# ax.errorbar([], [], [], fmt="r.", capsize=3, label="$\Re(w_{+,2})$ Data")
# fig.legend(ncol=4, framealpha=1,frameon=0, loc=10)
# plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images/legend Re.pdf", format="pdf",bbox_inches="tight")
