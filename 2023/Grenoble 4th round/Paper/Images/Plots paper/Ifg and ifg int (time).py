#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 21:37:36 2024

@author: aaa
"""


import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as fit

colors=["k","#f10d0c","#00a933","#5983b0"]

int_file_name="TOF_vs_chi_A+B_In1_08mm_22pt_pi16_1200s_4P_16Nov0206"



def fit_cos(x, A, B, C, D):
    return A/2*(1+B*np.cos(C*x-D))

sorted_fold_path_int="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/TOF A+B/"+int_file_name
cleandata_int=sorted_fold_path_int+"/Cleantxt"

i=0
for root, dirs, files in os.walk(cleandata_int, topdown=False):
    files=np.sort(files)
    # print(files)
    for name in files:
        # print(name)
        if i==0:
            tot_data_int=np.loadtxt(os.path.join(root, name))[:,:]
            time=tot_data_int[:,1]
            f_2=tot_data_int[0,-3]*1e-3
            f_1=tot_data_int[0,-6]*1e-3
            am_2=tot_data_int[0,-4]
            am_1=tot_data_int[0,-7]
            tau_int=tot_data_int[0,2]
            print("f1=", f_1)
            print("f2=", f_2)
            print("a1=", am_1)
            print("a2=", am_2)
            print("tau_int=", tau_int)
            i=1
        else:
            data=np.loadtxt(os.path.join(root, name))[:,:]
            tot_data_int = np.vstack((tot_data_int, data))
ps_int=tot_data_int[::len(time),-1]
matrix=np.zeros((len(ps_int),len(time)))
matrix_err=np.zeros((len(ps_int),len(time)))
for i in range(len(ps_int)):
    matrix[i]=tot_data_int[:,3][tot_data_int[:,-1]==ps_int[i]]
    matrix_err[i]=matrix[i]**0.5
matrix=matrix/tau_int/(time[-1]*1e-6)
matrix_err=matrix_err/tau_int/(time[-1]*1e-6)
print("time",1/(time[-1]*1e-6))
data_int=np.sum(matrix, axis=1)/len(time)
data_int_err=np.sum(matrix_err**2, axis=1)**0.5/len(time)

inf_file_name_ifg="ifg_-2to2_60s_16Nov0142"
sorted_fold_path_ifg="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/Ifg off/"+inf_file_name_ifg
cleandata_ifg=sorted_fold_path_ifg+"/Cleantxt"
for root, dirs, files in os.walk(cleandata_ifg, topdown=False):
    files=np.sort(files) 
    for name in files[:]:
        # print(name)
        tot_data_ifg=np.loadtxt(os.path.join(root, name))[:,:]

data_ifg=(tot_data_ifg[:,2]+0*tot_data_ifg[:,5])
tau_ifg=tot_data_ifg[0,1]
print("tau_ifg=", tau_ifg)
# print(tot_data_ifg)
# print(data_ifg)
data_ifg_err=data_ifg**0.5/tau_ifg
data_ifg/=tau_ifg
ps_ifg=tot_data_ifg[:,0]

P0=[(np.amax(data_int)+np.amin(data_int))/2, (np.amax(data_int)-np.amin(data_int))/2, 3, 0]
B0=([0,0,0.01,-10],[np.amax(data_int)+10000,np.amax(data_int)+10000,5, 10])
p_int,cov_int=fit(fit_cos, ps_int, data_int, p0=P0,  bounds=B0)
err_int=np.diag(cov_int)**0.5
A_int= p_int[0]
A_int_err=err_int[0]
C_int= p_int[1]
C_int_err=err_int[1]
w_ps_int=p_int[-2]
chi_0_int=p_int[-1]
chi_int=w_ps_int*ps_int-chi_0_int
chi_plt_int = np.linspace(chi_int[0], chi_int[-1],100)
print("C=",C_int, "+-", C_int_err)
print("A=",A_int, "+-", A_int_err)

P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, 0]
B0=([1,0,0.01,-10],[np.amax(data_ifg)+10000,np.amax(data_ifg)+10000,5, 10])
p_ifg,cov_ifg=fit(fit_cos, ps_ifg, data_ifg, p0=P0,  bounds=B0)
err_ifg=np.diag(cov_ifg)**0.5
A_ifg= p_ifg[0]
A_ifg_err=err_ifg[0]
C_ifg= p_ifg[1]
C_ifg_err=err_ifg[1]
w_ps_ifg=p_ifg[-2]
chi_0_ifg=p_ifg[-1]
chi_ifg=w_ps_ifg*ps_ifg-chi_0_ifg
chi_plt_ifg = np.linspace(chi_ifg[3], chi_ifg[-3],100)
print("C=",C_ifg, "+-", C_ifg_err)
print("A=",A_ifg, "+-", A_ifg_err)
# print(p_int[0]/1200)
print("C_ifg-C_int", C_ifg-C_int,"+-", (C_ifg_err**2+C_int_err**2)**0.5)
print("A_ifg-A_int", A_ifg-A_int,"+-", (C_ifg_err**2+C_int_err**2)**0.5)
print("A_ifg/A_int", A_ifg/A_int)

fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
ps_plt_int = np.linspace(ps_int[0], ps_int[-1],100)
ps_plt_ifg = np.linspace(ps_ifg[3], ps_ifg[-3],100)
ax.errorbar(ps_int,data_int/p_int[0]*100, yerr=data_int_err/p_int[0]*100,fmt="o",color=colors[1], capsize=5, ms=3, label="$\mathcal{N}_+ (\\alpha_{1,2}\\approx\pi/16$)")
ax.errorbar(ps_plt_int,fit_cos(ps_plt_int, *p_int)/p_int[0]*100,fmt="-",color=colors[1], label="Fit")
ax.errorbar(ps_ifg[3:-2],data_ifg[3:-2]/p_ifg[0]*100,yerr=data_ifg_err[3:-2]/p_ifg[0]*100,fmt="o",color=colors[3],capsize=5, ms=3, label="$\mathcal{N}_+ (\\alpha_{1,2}=0$)")
ax.errorbar(ps_plt_ifg,fit_cos(ps_plt_ifg, *p_ifg)/p_ifg[0]*100,fmt="--", color=colors[3], label="Fit")
ax.set_xlabel("Phase-shifter position [arb.]")
ax.legend(loc=1)
# ax.tick_params(axis="y", left=False, labelleft=False)
ax.set_ylabel("Arb.")
# plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images/Ifg and time average.pdf", format="pdf",bbox_inches="tight")
