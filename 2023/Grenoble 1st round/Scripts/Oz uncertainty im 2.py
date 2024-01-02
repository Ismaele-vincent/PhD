#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 16:53:52 2023

@author: aaa
"""
import os
import numpy as np
import shutil
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
from PIL import Image as im
from scipy.optimize import curve_fit as fit
from scipy.interpolate import UnivariateSpline as spline

a_1=1/5**0.5
a_2=2/5**0.5

def cos(chi):
    return 0.5+a_1*a_2*np.cos(chi)
def w1(chi):
    return 1/(1+a_2/a_1*np.exp(-1j*chi))


rad=np.pi/180
C=0.7914937937064894 
C_err=0.015566869131704356
alpha=1#22.5
# inf_file_name="path1pi8cb_g_09Apr1441"
# correct_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 1st round/exp_3-16-13/Corrected data/"+inf_file_name
# gamma_fold_clean=correct_fold_path+"/Gamma"
# data_gamma=np.loadtxt(correct_fold_path+"/"+inf_file_name[:8]+"_Gamma_corrected.txt")
data_gamma=np.loadtxt("TOF_vs_c_Im_corrected.txt")
chi=data_gamma[:,0]
chi_plt=np.linspace(chi[0], chi[-1], 500)

fig = plt.figure(figsize=(20,6))
ax= fig.add_subplot(111)
ax.errorbar(chi, data_gamma[:,1]/alpha, yerr=data_gamma[:,2]/alpha, fmt="ko", capsize=4)
ax.plot(chi_plt, w1(chi_plt).imag, "b-")

fig = plt.figure(figsize=(20,6))
ax= fig.add_subplot(111)
ax.errorbar(chi, 2*abs(data_gamma[:,1]/alpha*cos(chi)), yerr=data_gamma[:,2]/alpha*cos(chi), fmt="ko", capsize=4)
ax.plot(chi_plt, abs(a_1*a_2*np.sin(chi_plt)), "b-")