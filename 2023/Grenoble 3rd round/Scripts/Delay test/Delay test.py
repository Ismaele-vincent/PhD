# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 13:51:44 2023

@author: S18
"""
"""
.inf file names:
"TOF_test_vs_chi_23Aug1857.inf", 
"TOF_test_vs_chi_24Aug0034.inf", 
"TOF_test_vs_chi_24Aug0612.inf", 
"TOF_test_vs_chi_24Aug1149.inf", 
"TOF_test_vs_chi_24Aug1822.inf", 
"TOF_test_vs_chi_24Aug2359.inf", 
"TOF_test_vs_chi_25Aug0536.inf"
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
v0=2060.43 #m/s
phi1=0
phi2=0
order=4
w_ps=3
rad=np.pi/180

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)
def fit_O_beam(t, A, B, chi, a_1, xi_1):
    # a_1=alpha(T,f_1,B_1)
    # xi_1=phi_1+(2*np.pi*f_1*1e-3*T+np.pi)/2#-2*np.pi*f_1*1e3/v0
    chi_fit=chi
    return A + B*np.cos(chi_fit-a_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1))

inf_file_names=[ "TOF_A1_delay_07Sep1529","TOF_S2_delay_07Sep1539", ]

for inf_file_name in inf_file_names:
    print(inf_file_name)
    sorted_fold_path="C:/Users/S18/Desktop/Grenoble-2023 Ismaele/Grenoble 3rd round/exp_3-16-14/Sorted data/Delay tests/"+inf_file_name
    cleandata=sorted_fold_path+"/Cleantxt"
    for root, dirs, files in os.walk(cleandata, topdown=False): 
        for name in files:
            # print(name)
            if "A1" in inf_file_name:
                print("here")
                tot_data=np.loadtxt(os.path.join(root, name))
                data_tof=tot_data[:,4]
                data_tof_err=data_tof**0.5
                # bins=tot_data[:,1]
                time=tot_data[:,1]
                P0=[400,200, np.pi/2, -3.8, -0.7]
                B0=([5,5, -np.pi,-5, -2*np.pi],[1500, 3500, np.pi, 0, 2*np.pi])
                p,cov=fit(fit_O_beam, time[40:80], data_tof[40:80], p0=P0,  bounds=B0)
                print(p)
                P0=[(np.amax(data_tof)+np.amin(data_tof))/2, (np.amax(data_tof)-np.amin(data_tof))/2, 3, 0]
                B0=([np.amin(data_tof),0,0.01,-10],[np.amax(data_tof),np.amax(data_tof),5, 10])
                # p,cov=fit(fit_cos, time, data_tof, p0=P0,  bounds=B0)
                # err=np.diag(cov)**0.5
                # print(p[3], err[3])
                x_plt = np.linspace(time[0], time[-1],100)
                fig = plt.figure(figsize=(8,6))
                ax = fig.add_subplot(111)
                fig.suptitle(inf_file_name[:-4])
                ax.errorbar(time,data_tof,yerr=data_tof_err,fmt="ro",capsize=2, ms=1)
                # ax.plot(time, fit_O_beam(time, *p))
            if "S2" in inf_file_name:
                tot_data=np.loadtxt(os.path.join(root, name))
                data_tof=tot_data[:,4]
                data_tof_err=data_tof**0.5
                time=tot_data[:,1]
                P0=[400,200, np.pi/2, 3.8, -3]
                B0=([5,5, -np.pi,0, -2*np.pi],[1500, 3500, np.pi, 4, 2*np.pi])
                # p,cov=fit(fit_O_beam, time[30:70], data_tof[30:70], p0=P0,  bounds=B0)
                print(p)
                P0=[(np.amax(data_tof)+np.amin(data_tof))/2, (np.amax(data_tof)-np.amin(data_tof))/2, 3, 0]
                B0=([np.amin(data_tof),0,0.01,-10],[np.amax(data_tof),np.amax(data_tof),5, 10])
                # p,cov=fit(fit_cos, time, data_tof, p0=P0,  bounds=B0)
                # err=np.diag(cov)**0.5
                # print(p[3], err[3])
                x_plt = np.linspace(time[0], time[-1],100)
                # fig = plt.figure(figsize=(8,6))
                # ax = fig.add_subplot(111)
                fig.suptitle(inf_file_name[:-4])
                ax.errorbar(time,data_tof,yerr=data_tof_err,fmt="ko",capsize=2, ms=1)
                delta=-0.76680993+3.23514551-np.pi
                # ax.plot(time, fit_O_beam(time, *p[:-1],p[-1]))
                # ax.plot(time-delta/0.2*np.pi,fit_O_beam(time, *p))
                # ax.set_xlim([0, 150])
                print(-delta/0.2*np.pi)
plt.show()