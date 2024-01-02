#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 15:59:17 2023

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
mu_N=-9.6623651#*1e-27 J/T
hbar= 6.62607015/(2*np.pi) #*1e-34 J s

a_21=1
a_1=1/2**0.5
a_2=1/2**0.5
inf_file_name="TOF_vs_chi_A+B_22pt_pi16_1200s_09Nov1749"

alpha_1=0.3123806231229692#0.37#np.pi/a #/2.354
#alpha_1=0.785398163397448 #pi/4


def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

def fit_O_beam(t, A, B, chi, a_1, xi_1):
    # a_1=alpha(T,f_1,B_1)
    # xi_1=phi_1+(2*np.pi*f_1*1e-3*T+np.pi)/2#-2*np.pi*f_1*1e3/v0
    chi_fit=chi
    return A + B*np.cos(chi_fit-a_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1))/2

sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/TOF A+B/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"

i=0
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    # print(files)
    for name in files:
        # print(name)
        if i==0:
            tot_data=np.loadtxt(os.path.join(root, name))[:,:]
            time=tot_data[:,1]
            f_1=tot_data[0,-3]*1e-3
            print(f_1)
            i=1
        else:
            data=np.loadtxt(os.path.join(root, name))[:,:]
            tot_data = np.vstack((tot_data, data))
ps_pos=tot_data[::len(time),-1]
N = len(time)
S_F=3
matrix=np.zeros((len(ps_pos),len(time)))
matrix_err=np.zeros((len(ps_pos),len(time)))
for i in range(len(ps_pos)):
    matrix[i]=tot_data[:,5][tot_data[:,-1]==ps_pos[i]]
    matrix_err[i]=matrix[i]**0.5
    
ps_data=np.sum(matrix, axis=1)
P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, -3]
B0=([100,0,0.01,-10],[np.amax(ps_data)+1000,np.amax(ps_data)+1000,5, 10])
p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
Co= p[1]/p[0]
w_ps=p[-2]
chi_0=p[-1]
print("C=",Co)
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.set_title("Integrated intensities")
ax.set_xlabel("Ps position")
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
ax.errorbar(ps_pos,ps_data, yerr=ps_data**0.5,fmt="ko",capsize=5, ms=3)
ax.plot(ps_plt,fit_cos(ps_plt, *p), "b")
ax.vlines(p[-1]/p[-2],fit_cos(p[-1]/p[-2]+np.pi,*p),fit_cos(p[-1]/p[-2],*p), color="k")
P0=[300,300, -0.8, 1]
p_tot=np.zeros((len(ps_pos),len(P0)))
err_tot=np.zeros((len(ps_pos),len(P0)))
Re_data=np.zeros((len(ps_pos)))
Re_data_err=np.zeros((len(ps_pos)))
Im_data=np.zeros((len(ps_pos)))
Im_data_err=np.zeros((len(ps_pos)))
rho=np.zeros((len(ps_pos)))
chi=ps_pos*w_ps-chi_0
chi_plt=np.linspace(chi[0], chi[-1], 100)
cos2=np.zeros((len(ps_pos)))
cos2_err=np.zeros((len(ps_pos)))
for i in range(len(ps_pos)):
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    ax.set_title("ps_pos="+str("%.3f" %(ps_pos[i],)))
    ax.set_xlabel("time ($\mu$s)")
    ax.errorbar(time, matrix[i], yerr= matrix_err[i], fmt="ko")
        
plt.show()