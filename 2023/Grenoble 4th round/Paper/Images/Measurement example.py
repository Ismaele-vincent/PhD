#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:52:56 2024

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

rad=np.pi/180
a_21=1
a_1=1/2**0.5
a_2=1/2**0.5

inf_file_name="TOF_vs_chi_A+B_22pt_pi16_1200s_09Nov1808"
inf_file_name="TOF_vs_chi_A+B_22pt_pi16_1200s_4P_11Nov1354"
# inf_file_name="TOF_vs_chi_A+B_22pt_pi8_1200s_4P_11Nov2118" 
# inf_file_name="TOF_vs_chi_A+B_22pt_pi8_1200s_10Nov0133"
alpha_1=0.1923 #/2.354
alpha_1_err=0.0009 
alpha_2=-0.1971 #/2.354
alpha_2_err=0.0004

def w1(chi):
    return (1/(1+a_21*np.exp(1j*chi)))

def w2(chi):
    return (1-1/(1+a_21*np.exp(1j*chi)))

def fit_cos(x, A, B, C, D):
    return A/2*(1+B*jv(0,alpha_1)*jv(0,alpha_2)*np.cos(C*x-D))

A_aus=1
def fit_Im(t, B, Im_1, Im_2, xi_1, xi_2):
    return A_aus*((1-Co)/2+Co*B*(1+2*Im_1*alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)+2*Im_2*alpha_2*np.sin(2*np.pi*1e-3*f_2*t+xi_2)))

sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/TOF A+B/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"
niels_path="/home/aaa/Desktop/Niels/Data/"+inf_file_name
niels_fourier_path="/home/aaa/Desktop/Niels/Fourier/"+inf_file_name

if not os.path.exists(niels_path):
    os.makedirs(niels_path)
if not os.path.exists(niels_fourier_path):
    os.makedirs(niels_fourier_path)

i=0
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    # print(files)
    for name in files:
        # print(name)
        if i==0:
            tot_data=np.loadtxt(os.path.join(root, name))[:,:]
            time=tot_data[:,1]
            f_2=tot_data[0,-3]*1e-3
            f_1=tot_data[0,-6]*1e-3
            a_2=tot_data[0,-4]
            a_1=tot_data[0,-7]
            print("f1=", f_1)
            print("f2=", f_2)
            print("a1=", a_1)
            print("a2=", a_2)
            i=1
        else:
            data=np.loadtxt(os.path.join(root, name))[:,:]
            tot_data = np.vstack((tot_data, data))
time_plt=np.linspace(time[0], time[-1], 1000)
ps_pos=tot_data[::len(time),-1]
N = len(time)
S_F=16.6667
matrix=np.zeros((len(ps_pos),len(time)))
matrix_err=np.zeros((len(ps_pos),len(time)))
for i in range(len(ps_pos)):
    matrix[i]=tot_data[:,5][tot_data[:,-1]==ps_pos[i]]
    matrix_err[i]=matrix[i]**0.5
    
ps_data=np.sum(matrix, axis=1)
P0=[(np.amax(ps_data)+np.amin(ps_data))/2, 0.6, 3, -1.]
B0=([100,0,0.01,-10],[np.amax(ps_data)+10000,2,5, 10])
p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
err=np.diag(cov)**0.5
Co = 0.731#0.70456183532707045 
Co_err= 0.00646151528318766
A=p[0]*(1-Co)/2
A_err= (((1-Co)/2*err[0])**2+(p[0]/2*err[1])**2)**0.5
A_aus=p[0]/len(time)
w_ps=p[-2]
chi_0=p[-1]
chi_0_err=err[-1]
print("A(1-C)/2=", A, "+-", A_err)
print("C=",p[1], "+-", err[1])
print("chi_err=",err[-1])
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
ax.errorbar(ps_pos,ps_data, yerr=ps_data**0.5,fmt="ko",capsize=5, ms=3)
ax.plot(ps_plt,fit_cos(ps_plt, *p), "b")
ax.vlines(p[-1]/p[-2],fit_cos(p[-1]/p[-2]+np.pi,*p),fit_cos(p[-1]/p[-2],*p), color="k")
P0=[300,300, -0.8, 1]
p_tot=np.zeros((len(ps_pos),len(P0)))
err_tot=np.zeros((len(ps_pos),len(P0)))
Im_data_1=np.zeros((len(ps_pos)))
Im_data_err_1=np.zeros((len(ps_pos)))

Im_data_1_fit=np.zeros((len(ps_pos)))
Im_data_err_1_fit=np.zeros((len(ps_pos)))

Im_data_2=np.zeros((len(ps_pos)))
Im_data_err_2=np.zeros((len(ps_pos)))

Im_data_2_fit=np.zeros((len(ps_pos)))
Im_data_err_2_fit=np.zeros((len(ps_pos)))

rho=np.zeros((len(ps_pos)))
chi=ps_pos*w_ps-chi_0
chi_plt=np.linspace(chi[0], chi[-1], 100)
cos2=np.zeros((len(ps_pos)))
cos2_err=np.zeros((len(ps_pos)))
cos2_fit=np.zeros((len(ps_pos)))
cos2_err_fit=np.zeros((len(ps_pos)))

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
k=0
for i in [6,8,13,16]:
    func_data=matrix[i]
    func_data_err=matrix_err[i]
    chi_aus=chi[i]
    P0=[np.cos(chi[i]/2)**2, w1(chi[i]).imag, w2(chi[i]).imag, -0.6, 1.2]
    # print(P0)
    B0=([0,w1(chi[i]).imag-1000, w2(chi[i]).imag-1000, -2*np.pi, -2*np.pi],[np.inf, w1(chi[i]).imag+1000, w2(chi[i]).imag+1000, 2*np.pi, 2*np.pi])
    p_Im,cov_Im = fit(fit_Im, time, func_data, p0=P0, bounds=B0)
    err_Im=np.diag(cov_Im)**0.5
    print(p_Im[-2],p_Im[-1])
    # print(p_Im,err_Im)
    # Im_data_fit[i]=p_Im[2]
    # Im_data_fit_err[i]=(err_Im[2]**2+np.sin(chi[i])**2*chi_0_err**2)**0.5
    # cos2_fit[i]=p_Im[1]*p_Im[0]#*Co#+p_Im[0]*(1-Co)/2
    # cos2_fit_err[i]=err_Im[1]
    
    yf_data = fft(func_data)
    yf_data_err = np.ones(len(yf_data))*np.sum(matrix_err)**0.5
    # print(sum(abs(yf_data)))
    xf = fftfreq(N, S_F)*1e3
    colors=["k","#f10d0c","#00a933","#5983b0"]
    
    ax.errorbar(time, matrix[i], yerr= matrix_err[i], fmt=".", color=colors[k], capsize=2, label="$\chi=$"+str("%.2f"%chi[i],))
    # ax.plot(time_plt, fit_Im(time_plt, *p_Im),"--"+colors[i%5])
    # ax.set_title(str("%.2f"%chi[i],))
    # ax.errorbar(xf, np.abs(yf_data), np.abs(yf_data_err), fmt="k.", capsize=5)
    ax.set_xlim([0,2000])
    ax.set_xlabel("Time [$\mu$ s]")
    ax.set_ylabel("Arb.")
    k+=1
ax.legend(framealpha=1, loc=6)
# ax.legend(ncol=4, bbox_to_anchor=(0.5,1.1), loc="center")
plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images/Measurement_example.pdf", format="pdf",bbox_inches="tight")
plt.show()