# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 11:41:47 2023

@author: S18
"""
"""
inf_file_names:
"TOF_vs_chi_S2_ifg_29Aug1924", 
"TOF_vs_chi_S2_ifg_30Aug2349",
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
f_2=10
B_2=2
B_0=18.55
T=10
v0=2060.43 #m/s
phi_2=0
order=4
w_ps=3.127
rad=np.pi/180
chi=0
chi_0=0.7
C=0.6
def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

def fit_O_beam(t, A, B, a_2, xi_2):
    # a_2=alpha(T,f_2,B_2)
    # xi_2=phi_2+(2*np.pi*f_2*1e-3*T+np.pi)/2#-2*np.pi*f_2*1e3/v0
    chi_fit=chi
    return B+A*((1-C)/2 + C*(1+np.cos(chi_fit-a_2*np.sin(2*np.pi*1e-3*f_2*t+xi_2)))/2)

inf_file_names=[ 
"TOF_vs_chi_S2_ifg_29Aug1924",]

for inf_file_name in inf_file_names:
    print(inf_file_name)
    sorted_fold_path="C:/Users/S18/Desktop/Grenoble-2023 Ismaele/Grenoble 3rd round/exp_3-16-14/Sorted data/TOF S2/"+inf_file_name
    cleandata=sorted_fold_path+"/Cleantxt"
    i=0
    for root, dirs, files in os.walk(cleandata, topdown=False):
        files=np.sort(files)
        for name in files:
            if "ifg_20s_" in name:
                print(name)
                tot_data_ifg=np.loadtxt(os.path.join(root, name))
                data_ifg=tot_data_ifg[:,2]+tot_data_ifg[:,5]
                data_ifg_err=data_ifg**0.5
                ps_pos_ifg=tot_data_ifg[:,0]
                P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, 0]
                B0=([np.amin(data_ifg),0,0.01,-10],[np.amax(data_ifg),np.amax(data_ifg),5, 10])
                p,cov=fit(fit_cos, ps_pos_ifg, data_ifg, p0=P0,  bounds=B0)
                # err=np.diag(cov)**0.5
                # print(p[3], err[3])
                x_plt = np.linspace(ps_pos_ifg[0], ps_pos_ifg[-1],100)
                fig = plt.figure(figsize=(8,6))
                ax = fig.add_subplot(111)
                fig.suptitle(name[:-4])
                ax.errorbar(ps_pos_ifg,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                ax.plot(x_plt,fit_cos(x_plt, *p), "b")
                # ax.set_ylim([0,1500])
                C= p[1]/p[0]/3
                w_ps=p[-2]/3
                chi_0=p[-1]/3
                p_ifg=p.copy()
                print("C=", p[1]/p[0])
                print("w_ps=", p[-2])
                print("chi_0=", p[-1])
            else:
                if i==0:
                    tot_data=np.loadtxt(os.path.join(root, name))[1:-1,:]
                    time=tot_data[:,1]
                    f_2=tot_data[0,-3]*1e-3
                    # print(f_2)
                    i=1
                else:
                    data=np.loadtxt(os.path.join(root, name))[1:-1,:]
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
    
    ps_data=np.sum(matrix, axis=1)
    P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, -3]
    B0=([np.amin(ps_data),0,0.01,-10],[np.amax(ps_data),np.amax(ps_data),5, 10])
    p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
    print("C=", p[1]/p[0])
    print("w_ps=", p[-2])
    print("chi_0=", p[-1])
    # C= p[1]/p[0]
    w_ps=p[-2]
    chi_01=p[-1]
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
    ax.errorbar(ps_pos,ps_data, yerr=ps_data**0.5,fmt="ko",capsize=5, ms=3)
    ax.plot(x_plt,fit_cos(x_plt, *p), "b")
    P0=[np.average(matrix[i]),500, alpha(T,f_2,B_2), 2]
    p_tot=np.zeros((len(ps_pos),len(P0)))
    err_tot=np.zeros((len(ps_pos),len(P0)))
    for i in range(len(ps_pos)):
        # print(P0)
        B0=([np.amin(matrix),10, -3,1],[2000,np.amax(matrix)+300, 0, 2.5])
        chi=w_ps*ps_pos[i]-chi_0
        p,cov=fit(fit_O_beam, time, matrix[i], p0=P0,  bounds=B0)
        p_tot[i]=p.copy()
        err_tot[i]=np.diag(cov)**0.5
        P0=p.copy()
        err=np.diag(cov)**0.5
        # print(p[3], err[3])
        x_plt = np.linspace(time[0], time[-1],100)
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        fig.suptitle("ps_pos="+str(ps_pos[i]))
        ax.errorbar(time,matrix[i],yerr=matrix_err[i],fmt="ko",capsize=5, ms=3)
        ax.plot(x_plt,fit_O_beam(x_plt, *p), "b")
        ax.set_ylim([0,1500])
        ax.legend(loc=4)
    fig = plt.figure(figsize=(6,8))
    param_names=["A", "B", "$\\alpha_2$", "$\\xi_2$"]
    gs = GridSpec(len(param_names),1, figure=fig, hspace=0, wspace=0)
    axs=[]
    for i in range(len(param_names[:])):
        axs.append(fig.add_subplot(gs[i,0]))
        axs[i].set_ylabel(param_names[i])
        axs[i].errorbar(ps_pos, p_tot[:,i], yerr=err_tot[:,i])
        y_min=np.amin(p_tot[:,i])
        y_max=np.amax(p_tot[:,i])
        axs[i].set_ylim([y_min*(1-np.sign(y_min)*0.1),y_max*(1+np.sign(y_min)*0.1)])
plt.show()