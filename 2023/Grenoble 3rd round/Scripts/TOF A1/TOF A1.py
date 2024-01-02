# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 13:11:49 2023

@author: S18
"""

"""
.inf file names:
"TOF_vs_chi_A1_27Aug2100"",
"""

import os
import numpy as np
import shutil
import matplotlib.pyplot as plt
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
w_ps=3
rad=np.pi/180

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

def fit_O_beam(t, A, C, chi, B_1, phi_1, T):
    a_1=alpha(T,f_1,B_1)
    xi_1=phi_1+(2*np.pi*f_1*1e-3*T+np.pi)/2#-2*np.pi*f_1*1e3/v0
    return A*(1-C+C*(1+np.cos(chi+a_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)))/2)

inf_file_names=[
"TOF_vs_chi_A1_27Aug2100"]

for inf_file_name in inf_file_names:
    print(inf_file_name)
    sorted_fold_path="C:/Users/S18/Desktop/Grenoble-2023 Ismaele/Grenoble 3rd round/exp_3-16-14/Sorted data/TOF A1/"+inf_file_name
    cleandata=sorted_fold_path+"/Cleantxt"
    i=0
    for root, dirs, files in os.walk(cleandata, topdown=False):
        files=np.sort(files)
        for name in files:
            if i==0:
                tot_data=np.loadtxt(os.path.join(root, name))
                time=tot_data[:,1]
                f_1=tot_data[0,-3]*1e-3
                print(f_1)
                i=1
            else:
                data=np.loadtxt(os.path.join(root, name))
                tot_data = np.vstack((tot_data, data))
    ps_pos=tot_data[::len(time),-1]

    matrix=np.zeros((len(ps_pos),len(time)))
    matrix_err=np.zeros((len(ps_pos),len(time)))
    for i in range(len(ps_pos)):
        if tot_data[:,4].all()==0:
            matrix[i]=tot_data[:,3][tot_data[:,-1]==ps_pos[i]]
        else:
            matrix[i]=tot_data[:,4][tot_data[:,-1]==ps_pos[i]]
        matrix_err[i]=matrix[i]**0.5
        
    P0=[(np.amax(matrix[i])+np.amin(matrix[i]))/2, 0.7, 3*ps_pos[i], 10, 0.1, 10]
    p_tot=np.zeros((len(ps_pos),len(P0)))
    err_tot=np.zeros((len(ps_pos),len(P0)))
    for i in range(len(ps_pos)):
        B0=([np.amin(matrix),0.1,-3*np.pi,2,-3*np.pi,5],[3000,1,3*np.pi, 30, 3*np.pi,30])
        p,cov=fit(fit_O_beam, time, matrix[i], p0=P0,  bounds=B0)
        p_tot[i]=p.copy()
        err_tot[i]=np.diag(cov)**0.5
        P0=p.copy()
        err=np.diag(cov)**0.5
        print(p[3], err[3])
        x_plt = np.linspace(time[0], time[-1],100)
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        fig.suptitle("ps_pos="+str(ps_pos[i]))
        ax.errorbar(time,matrix[i],yerr=matrix_err[i],fmt="ko",capsize=5, ms=3)
        ax.plot(x_plt,fit_O_beam(x_plt, *P0), "b")
        ax.set_ylim([0,1500])
        # ax.legend(loc=4)
    fig = plt.figure(figsize=(6,8))
    param_names=["A", "C", "$\chi$", "$B_1$", "$\phi_1$", "T"]
    gs = GridSpec(len(param_names),1, figure=fig, hspace=0, wspace=0)
    axs=[]
    for i in range(len(param_names)):
        axs.append(fig.add_subplot(gs[i,0]))
        axs[i].set_ylabel(param_names[i])
        axs[i].errorbar(ps_pos, p_tot[:,i], yerr=err_tot[:,i])
        axs[i].set_ylim([np.amin(p_tot[:,i])*(0.9),np.amax(p_tot[:,i])*(1.1)])
        
        
plt.show()