# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 16:10:34 2023

@author: S18
"""

"""
inf_file_names:
 "TOF_vs_chi_S2+A1_25Aug1549", 
 "TOF_vs_chi_S2+A1_25Aug1917", 
 "TOF_vs_chi_S2+A1_26Aug1136", 
 "TOF_vs_chi_S2+A1_28Aug0752", 
 "TOF_vs_chi_S2+A1_30Aug0129", 
 "TOF_vs_chi_S2+A1_ifg_31Aug2303", 
 "TOF_vs_chi_S2+A1_ifg_SD_30Aug1140", 
 "TOF_vs_chi_S2+A1_ifg_SD_31Aug0601",  
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
f_2=10
B_2=10
B_0=18.55
T=10
v0=2060.43 #m/s
phi_1=0
phi_2=0
order=4
w_ps=0
rad=np.pi/180
chi=0
chi_0=0
C=0
def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

def fit_O_beam(t, A, B, a_1, xi_1, a_2, xi_2):
    # a_2=alpha(T,f_2,B_2)
    # xi_2=phi_2+(2*np.pi*f_2*1e-3*T+np.pi)/2#-2*np.pi*f_2*1e3/v0
    chi_fit=chi
    return A + B*np.cos(chi_fit-a_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)+a_2*np.sin(2*np.pi*1e-3*f_2*t+xi_2))/2

inf_file_names=["TOF_vs_chi_S2+A1_ifg_31Aug2303" ]

for inf_file_name in inf_file_names:
    print(inf_file_name)
    sorted_fold_path="C:/Users/S18/Desktop/Grenoble-2023 Ismaele/Grenoble 3rd round/exp_3-16-14/Sorted data/TOF S2+A1/"+inf_file_name
    cleandata=sorted_fold_path+"/Cleantxt"
    i=0
    for root, dirs, files in os.walk(cleandata, topdown=False):
        files=np.sort(files)
        for name in files:
            # print(name)
            if "ifg_20s_" in name:
                # print(name)
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
                ax.vlines(p[-1]/p[-2],fit_cos(p[-1]/p[-2]+np.pi,*p),fit_cos(p[-1]/p[-2],*p), color="k")
                # ax.set_ylim([0,1500])
                C+= p[1]/p[0]/3
                w_ps+=p[-2]/3
                chi_0+=p[-1]/3
                # print("C=", p[1]/p[0])
                # print("w_ps=", p[-2])
                # print("chi_0=", p[-1])
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
    print(w_ps)
    matrix=np.zeros((len(ps_pos),len(time)))
    matrix_err=np.zeros((len(ps_pos),len(time)))
    for i in range(len(ps_pos)):
        if tot_data[:,4].all()==0:
            matrix[i]=tot_data[:,3][tot_data[:,-1]==ps_pos[i]]
        else:
            matrix[i]=tot_data[:,4][tot_data[:,-1]==ps_pos[i]]
        matrix_err[i]=matrix[i]**0.5
    # P0=[300,300,w_ps*ps_pos[0]-chi_0, -0.8, 0.5, 0.8, 3.5]
    P0=[300,300, -0.8, 0.8, -0.5, -0.5]
    p_tot=np.zeros((len(ps_pos),len(P0)))
    err_tot=np.zeros((len(ps_pos),len(P0)))
    for i in range(len(ps_pos)):
        # print(P0)
        # B0=([100,100, -4*np.pi, -3, -2*np.pi, 0, 0],[1500, 1500, 4*np.pi, 0, 2*np.pi, 2*np.pi, 2*np.pi])
        B0=([100,100, -1, -np.pi/3, -1, -np.pi/3],[1500, 1500, 0, np.pi/3, 0, np.pi/3])
        chi=w_ps*ps_pos[i]-chi_0
        p,cov=fit(fit_O_beam, time, matrix[i], p0=P0,  bounds=B0)
        print(p)
        p_tot[i]=p.copy()
        err_tot[i]=np.diag(cov)**0.5
        P0=p.copy()
        # err=np.diag(cov)**0.5
        # print(p[3], err[3])
        x_plt = np.linspace(time[0], time[-1],100)
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        fig.suptitle("ps_pos="+str(ps_pos[i]))
        ax.errorbar(time,matrix[i],yerr=matrix_err[i],fmt="ko",capsize=5, ms=3)
        ax.plot(x_plt,fit_O_beam(x_plt, *p), "b")
        ax.set_ylim([0,1500])
        # ax.legend(loc=4)
    fig = plt.figure(figsize=(6,8))
    # param_names=["A", "C", "$\chi$", "|$\\alpha_1$|", "$\\xi_1$", "|$\\alpha_2$|", "$\\xi_2$"]
    param_names=["A", "C", "|$\\alpha_1$|", "$\\xi_1$", "|$\\alpha_2$|", "$\\xi_2$"]
    gs = GridSpec(len(param_names),1, figure=fig, hspace=0, wspace=0)
    axs=[]
    for i in range(len(param_names)):
        axs.append(fig.add_subplot(gs[i,0]))
        axs[i].set_ylabel(param_names[i])
        axs[i].errorbar(ps_pos, p_tot[:,i], yerr=err_tot[:,i])
        y_min=np.amin(p_tot[:,i])
        y_max=np.amax(p_tot[:,i])
        axs[i].set_ylim([np.sign(y_min)*abs(y_min)*1.1,np.sign(y_max)*abs(y_max)*1.1])
        
plt.show()