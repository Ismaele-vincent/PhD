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
ax=fig.add_subplot()
ax.tick_params(axis="both", labelleft=False, left = False, labelbottom=False, bottom = False)
ax.set_frame_on(False)
ax.errorbar([],[], fmt="b--", alpha=0.5,label="$\Im(w_{+,1})$  Theory")  
ax.errorbar([],[], fmt="k--", alpha=0.5,label="$\Re_1(w_{+,2})$  Theory")      
ax.errorbar([],[], fmt="r--", alpha=0.5,label="$\Re_2(w_{+,1})$  Theory")
ax.errorbar([],[], fmt="g--", alpha=0.5,label="$\Re_3(w_{+,2})$  Theory")
fig.legend(ncol=4, framealpha=1,frameon=0, loc=10)
plt.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Report/Images/legend Im Re_1.pdf", format="pdf",bbox_inches="tight")

fig = plt.figure(figsize=(8.5,0.1), dpi=200)
gs = GridSpec(2,2, figure=fig, wspace=0, hspace=0, top=1, bottom=0.135)
ax=fig.add_subplot()
ax.tick_params(axis="both", labelleft=False, left = False, labelbottom=False, bottom = False)
ax.set_frame_on(False)
ax.errorbar([], [], [], fmt="b.", capsize=3, label="$\Im(w_{+,1})$ Data")
ax.errorbar([], [], [], fmt="k.", capsize=3, label="$\Re_1(w_{+,2})$ Data")
ax.errorbar([], [], [], fmt="r.", capsize=3, label="$\Re_2(w_{+,1})$ Data")
ax.errorbar([], [], [], fmt="g.", capsize=3, label="$\Re_3(w_{+,2})$ Data")
fig.legend(ncol=4, framealpha=1,frameon=0, loc=10)
plt.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Report/Images/legend Re_2 Re_3.pdf", format="pdf",bbox_inches="tight")
