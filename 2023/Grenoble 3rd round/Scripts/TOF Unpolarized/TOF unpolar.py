#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:01:41 2023

@author: aaa
"""

"""
inf_file_names:
"TOF_vs_chi_A1_19pt_pi4_Unpol_1500s_28Sep2044", 
"TOF_vs_chi_S2_19pt_pi4_Unpol_1500s_29Sep0443", 
"TOF_vs_chi_S2+A1_19pt_pi8_Unpol_1500s_28Sep0301", 
"TOF_vs_chi_A1_19pt_pi8_Unpol_1500s_27Sep1105", 
"TOF_vs_chi_S2_19pt_pi8_Unpol_1500s_27Sep1903",
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
mu_N=-9.6623651#*1e-27 J/T
hbar= 6.62607015/(2*np.pi) #*1e-34 J s
f_1=10
B_1=10
B_0=18.55
T=10
v0=2060.43 #m/s
phi_1=0
order=4
w_ps=0
rad=np.pi/180
chi=0
chi_0=0
C=0
a=4
a_21=1
a_1=1/2**0.5
a_2=1/2**0.5
# inf_file_names=["TOF_vs_chi_A1_19pt_pi4_Unpol_1500s_28Sep2044",]
inf_file_names=["TOF_vs_chi_S2_19pt_pi4_Unpol_1500s_29Sep0443"]
# inf_file_names=["TOF_vs_chi_S2+A1_19pt_pi8_Unpol_1500s_28Sep0301", ]
# inf_file_names=["TOF_vs_chi_A1_19pt_pi8_Unpol_1500s_27Sep1105",]
# inf_file_names=["TOF_vs_chi_S2_19pt_pi8_Unpol_1500s_27Sep1903",]

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

def fit_O_beam(t, A, B, a_1, xi_1):
    # a_1=alpha(T,f_1,B_1)
    # xi_1=phi_1+(2*np.pi*f_1*1e-3*T+np.pi)/2#-2*np.pi*f_1*1e3/v0
    chi_fit=chi
    return A + B*np.cos(chi_fit-a_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1))/2


for inf_file_name in inf_file_names:
    # if "pi8" in inf_file name:
    print(inf_file_name, " -> ", "pi/", a, sep="")
    sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/exp_3-16-14/Sorted data/TOF Unpolarized/"+inf_file_name
    cleandata=sorted_fold_path+"/Cleantxt"
    i=0
    for root, dirs, files in os.walk(cleandata, topdown=False):
        files=np.sort(files)
        for name in files:
            if i==0:
                tot_data=np.loadtxt(os.path.join(root, name))[:,:]
                time=tot_data[:,1]
                f_1=tot_data[0,-3]*1e-3
                print(tot_data)
                i=1
            else:
                data=np.loadtxt(os.path.join(root, name))[:,:]
                tot_data = np.vstack((tot_data, data))
    ps_pos=tot_data[::len(time),-1]
    matrix=np.zeros((len(ps_pos),len(time)))
    matrix_err=np.zeros((len(ps_pos),len(time)))
    for i in range(len(ps_pos)):
        matrix[i]=tot_data[:,4][tot_data[:,-1]==ps_pos[i]]
        matrix_err[i]=matrix[i]**0.5
    
    ps_data=np.sum(matrix, axis=1)
    P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, 0]
    B0=([np.amin(ps_data),0,0.01,-10],[np.amax(ps_data),np.amax(ps_data),5, 10])
    p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
    C= p[1]/p[0]
    w_ps=p[-2]
    chi_0=p[-1]
    print("C=",C)
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
    ax.errorbar(ps_pos,ps_data, yerr=ps_data**0.5,fmt="ko",capsize=5, ms=3)
    ax.plot(x_plt,fit_cos(x_plt, *p), "b")
    for i in range(len(ps_pos)):
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        ax.errorbar(time, matrix[i], yerr= matrix_err[i], fmt="ko")

plt.show()