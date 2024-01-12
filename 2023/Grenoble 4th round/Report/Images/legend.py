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

fig = plt.figure(figsize=(8.5,0.1), dpi=200)
# fig.suptitle(inf_file_name)
gs = GridSpec(2,2, figure=fig, wspace=0, hspace=0, top=1, bottom=0.135)
axs=[fig.add_subplot(gs[:,:])]
# axs[1].tick_params(axis="x", labelbottom=False, bottom = False)
# axs[2].tick_params(axis="x", labelbottom=False, bottom = False)
# axs[2].tick_params(axis="y", labelleft=False, left = False)
# axs[4].tick_params(axis="y", labelleft=False, left = False)
# axs[1].set_ylabel("Perfect interfer.", fontsize = plt.rcParams['axes.titlesize'])
# axs[3].set_ylabel("Imperfect interf.", fontsize = plt.rcParams['axes.titlesize'])
# axs[1].set_title("Fourier Transform")
# axs[2].set_title("Fit")
axs[0].tick_params(axis="both", labelleft=False, left = False, labelbottom=False, bottom = False)
axs[0].set_frame_on(False)


axs[0].plot([], "k--", alpha=0.5,label="$\Im(w_{+,1})$  Theory")    
axs[0].errorbar([], [], [], fmt="k.", capsize=3, label="$\Im(w_{+,1})$ Data")
axs[0].plot([], "g--", alpha=0.5,label="$\Im(w_{+,2})$  Theory")    
axs[0].errorbar([], [], [], fmt="g.", capsize=3, label="$\Im(w_{+,2})$ Data")
fig.legend(ncol=4, framealpha=1,frameon=0, loc=10)
plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Report/Images/legend.pdf", format="pdf",bbox_inches="tight")
