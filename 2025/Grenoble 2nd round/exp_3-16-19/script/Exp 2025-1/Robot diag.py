#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 13:28:57 2026

@author: aaa
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
import My_module_Exp_2025_1 as mymod

pre_In_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/rawdata/sc/robot_diag_double_Cd_90deg_test_02Oct1000.dat"
# pre_In_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/rawdata/sc/robot_diag_double_Cd_90deg_test_29Sep1846.dat"

Pre_In_data = np.loadtxt(pre_In_path, encoding='windows-1252', comments="*",skiprows=28,delimiter="\t")
Pre_In_int = Pre_In_data[:,3]
n=[5,10,16]
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.errorbar(Pre_In_data[:,1],Pre_In_data[:,3],yerr=Pre_In_data[:,3]**0.5,fmt="r-",capsize=5, ms=3)
ax.errorbar(Pre_In_data[n,1],Pre_In_data[n,3],yerr=Pre_In_data[n,3]**0.5,fmt="b-",capsize=5, ms=3)

I_3=Pre_In_data[n[2],3]/np.sum(Pre_In_data[n,3])
I_2=Pre_In_data[n[0],3]/np.sum(Pre_In_data[n,3])
I_1=Pre_In_data[n[1],3]/np.sum(Pre_In_data[n,3])

print(I_1,I_2,I_3, I_1+I_2+I_3)