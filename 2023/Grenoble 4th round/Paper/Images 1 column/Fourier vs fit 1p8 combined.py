#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:46:58 2024

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
plt.rcParams["mathtext.fontset"]="cm"
colors=["k","#f10d0c","#00a933","#5983b0"]
rad=np.pi/180
a_1= 0.496
a_1_err= 0.003
a_2= 0.868
a_2_err= 0.002
a_21=a_2/a_1
a_21_err= a_21*((a_1_err/a_1)**2+(a_2_err/a_2)**2)**0.5
# inf_file_name="TOF_vs_chi_A+B_In1_22pt_pi16_2000s_4P_16Nov1733"
inf_file_name="TOF_vs_chi_A+B_In1_22pt_pi16_1200s_4P_15Nov0927"

alpha_1=0.1932 #/2.354
alpha_1_err=0.0005
alpha_2=0.1969 #/2.354
alpha_2_err=0.0004

def w1(chi):
    return (1/(1+a_21*np.exp(1j*chi)))

def w2(chi):
    return (1-1/(1+a_21*np.exp(1j*chi)))

def fit_cos(x, A, B, C, D):
    return A/2*(1+B*np.cos(C*x-D))

data_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Results txt/In 1p8"

i=0
k=0
j=0
for root, dirs, files in os.walk(data_fold_path, topdown=False):
    n_data_set=len(files)/3
    # print(n_data_set)
    for name in files:
        if "cos2" in name:
            if j==0:
                ps_pos=np.loadtxt(os.path.join(root, name))[:,0]
                cos2_avg=np.loadtxt(os.path.join(root, name))[:,1]/np.loadtxt(os.path.join(root, name))[:,2]**2
                cos2_avg_err=1/np.loadtxt(os.path.join(root, name))[:,2]**2
                j+=1
            else:
                cos2_avg+=np.loadtxt(os.path.join(root, name))[:,1]/np.loadtxt(os.path.join(root, name))[:,2]**2
                cos2_avg_err+=1/np.loadtxt(os.path.join(root, name))[:,2]**2
        if "Wv12_Im" in name:
            # print(name)
            if i==0:
                chi_im=np.loadtxt(os.path.join(root, name))[:,0]
                Im_1_avg=np.loadtxt(os.path.join(root, name))[:,1]/np.loadtxt(os.path.join(root, name))[:,2]**2
                Im_1_avg_err=1/np.loadtxt(os.path.join(root, name))[:,2]**2
                Im_2_avg=np.loadtxt(os.path.join(root, name))[:,3]/np.loadtxt(os.path.join(root, name))[:,4]**2
                Im_2_avg_err=1/np.loadtxt(os.path.join(root, name))[:,4]**2
                i+=1
            else:
                Im_1_avg+=np.loadtxt(os.path.join(root, name))[:,1]/np.loadtxt(os.path.join(root, name))[:,2]**2
                Im_1_avg_err+=1/np.loadtxt(os.path.join(root, name))[:,2]**2
                Im_2_avg+=np.loadtxt(os.path.join(root, name))[:,3]/np.loadtxt(os.path.join(root, name))[:,4]**2
                Im_2_avg_err+=1/np.loadtxt(os.path.join(root, name))[:,4]**2
        if "Wv12_Re" in name:
            # print(name)
            if k==0:
                chi_Re=np.loadtxt(os.path.join(root, name))[:,0]
                Re_1_avg=np.loadtxt(os.path.join(root, name))[:,1]/np.loadtxt(os.path.join(root, name))[:,2]**2
                Re_1_avg_err=1/np.loadtxt(os.path.join(root, name))[:,2]**2
                Re_2_avg=np.loadtxt(os.path.join(root, name))[:,3]/np.loadtxt(os.path.join(root, name))[:,4]**2
                Re_2_avg_err=1/np.loadtxt(os.path.join(root, name))[:,4]**2
                k+=1
            else:
                Re_1_avg+=np.loadtxt(os.path.join(root, name))[:,1]/np.loadtxt(os.path.join(root, name))[:,2]**2
                Re_1_avg_err+=1/np.loadtxt(os.path.join(root, name))[:,2]**2
                Re_2_avg+=np.loadtxt(os.path.join(root, name))[:,3]/np.loadtxt(os.path.join(root, name))[:,4]**2
                Re_2_avg_err+=1/np.loadtxt(os.path.join(root, name))[:,4]**2
Im_1_avg/=Im_1_avg_err
Im_2_avg/=Im_2_avg_err
Re_1_avg/=Re_1_avg_err
Re_2_avg/=Re_2_avg_err
cos2_avg/=cos2_avg_err
Im_1_avg_err=1/Im_1_avg_err**0.5#/n_data_set
Im_2_avg_err=1/Im_2_avg_err**0.5#/n_data_set
Re_1_avg_err=1/Re_1_avg_err**0.5#/n_data_set
Re_2_avg_err=1/Re_2_avg_err**0.5#/n_data_set
cos2_avg_err=1/cos2_avg_err**0.5

P0=[(np.amax(cos2_avg)+np.amin(cos2_avg))/2, (np.amax(cos2_avg)-np.amin(cos2_avg))/2, 3, -1.5]
B0=([100,0,0.01,-10],[np.amax(cos2_avg)+10000,np.amax(cos2_avg)+10000,5, 10])
p_int,cov_int=fit(fit_cos, ps_pos, cos2_avg, p0=P0,  bounds=B0, sigma=cos2_avg_err)
err_int=np.diag(cov_int)**0.5
w_ps=p_int[-2]
chi_0=p_int[-1]
chi=ps_pos*w_ps-chi_0

fig = plt.figure(figsize=(8.5,5), dpi=150)
ax=fig.add_subplot(111)
ax.errorbar(ps_pos, cos2_avg,cos2_avg_err, capsize=3, fmt="k.")
ax.plot(ps_pos, fit_cos(ps_pos, *p_int))

chi_plt=np.linspace(chi[0], chi[-1],500)


data_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Results txt fit/In 1p8"

i=0
k=0
j=0
for root, dirs, files in os.walk(data_fold_path, topdown=False):
    n_data_set=len(files)/3
    # print(n_data_set)
    for name in files:
        if "cos2" in name:
            if j==0:
                ps_pos=np.loadtxt(os.path.join(root, name))[:,0]
                cos2_avg_fit=np.loadtxt(os.path.join(root, name))[:,1]/np.loadtxt(os.path.join(root, name))[:,2]**2
                cos2_avg_fit_err=1/np.loadtxt(os.path.join(root, name))[:,2]**2
                j+=1
            else:
                cos2_avg_fit+=np.loadtxt(os.path.join(root, name))[:,1]/np.loadtxt(os.path.join(root, name))[:,2]**2
                cos2_avg_fit_err+=1/np.loadtxt(os.path.join(root, name))[:,2]**2
        if "Wv12_Im" in name:
            # print(name)
            if i==0:
                chi_im=np.loadtxt(os.path.join(root, name))[:,0]
                Im_1_avg_fit=np.loadtxt(os.path.join(root, name))[:,1]/np.loadtxt(os.path.join(root, name))[:,2]**2
                Im_1_avg_fit_err=1/np.loadtxt(os.path.join(root, name))[:,2]**2
                Im_2_avg_fit=np.loadtxt(os.path.join(root, name))[:,3]/np.loadtxt(os.path.join(root, name))[:,4]**2
                Im_2_avg_fit_err=1/np.loadtxt(os.path.join(root, name))[:,4]**2
                i+=1
            else:
                Im_1_avg_fit+=np.loadtxt(os.path.join(root, name))[:,1]/np.loadtxt(os.path.join(root, name))[:,2]**2
                Im_1_avg_fit_err+=1/np.loadtxt(os.path.join(root, name))[:,2]**2
                Im_2_avg_fit+=np.loadtxt(os.path.join(root, name))[:,3]/np.loadtxt(os.path.join(root, name))[:,4]**2
                Im_2_avg_fit_err+=1/np.loadtxt(os.path.join(root, name))[:,4]**2
        if "Wv12_Re" in name:
            # print(name)
            if k==0:
                chi_Re=np.loadtxt(os.path.join(root, name))[:,0]
                Re_1_avg_fit=np.loadtxt(os.path.join(root, name))[:,1]/np.loadtxt(os.path.join(root, name))[:,2]**2
                Re_1_avg_fit_err=1/np.loadtxt(os.path.join(root, name))[:,2]**2
                Re_2_avg_fit=np.loadtxt(os.path.join(root, name))[:,3]/np.loadtxt(os.path.join(root, name))[:,4]**2
                Re_2_avg_fit_err=1/np.loadtxt(os.path.join(root, name))[:,4]**2
                k+=1
            else:
                Re_1_avg_fit+=np.loadtxt(os.path.join(root, name))[:,1]/np.loadtxt(os.path.join(root, name))[:,2]**2
                Re_1_avg_fit_err+=1/np.loadtxt(os.path.join(root, name))[:,2]**2
                Re_2_avg_fit+=np.loadtxt(os.path.join(root, name))[:,3]/np.loadtxt(os.path.join(root, name))[:,4]**2
                Re_2_avg_fit_err+=1/np.loadtxt(os.path.join(root, name))[:,4]**2
Im_1_avg_fit/=Im_1_avg_fit_err
Im_2_avg_fit/=Im_2_avg_fit_err
Re_1_avg_fit/=Re_1_avg_fit_err
Re_2_avg_fit/=Re_2_avg_fit_err
cos2_avg_fit/=cos2_avg_fit_err
Im_1_avg_fit_err=1/Im_1_avg_fit_err**0.5#/n_data_set
Im_2_avg_fit_err=1/Im_2_avg_fit_err**0.5#/n_data_set
Re_1_avg_fit_err=1/Re_1_avg_fit_err**0.5#/n_data_set
Re_2_avg_fit_err=1/Re_2_avg_fit_err**0.5#/n_data_set
cos2_avg_fit_err=1/cos2_avg_fit_err**0.5

ylim_im_1=-4
ylim_im_2=4

fig = plt.figure(figsize=(8,2.5), dpi=200)
gs = fig.add_gridspec(1,3)
axs=[fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[0, 2])]
axs[0].set_ylabel("$w^\Im_{+,1}$", fontsize=13)
axs[0].errorbar(chi, Im_1_avg, Im_1_avg_err, fmt=".", color=colors[0], capsize=3, label="Data")
axs[1].errorbar(chi, Im_1_avg_fit, Im_1_avg_fit_err, fmt=".", color=colors[0], capsize=3, label="Data")
axs[2].errorbar(chi, Im_1_avg_fit-Im_1_avg, fmt="-", color=colors[0], capsize=3, label="Data")
axs[2].errorbar(chi, Im_1_avg_fit_err-Im_1_avg_err, fmt="--", color=colors[1], capsize=3, label="Data")
# axs[0].set_ylim([ylim_im_1,ylim_im_2])
# axs[0].text("Fourier method")
# axs[0].text("Fit method")
# axs[1].tick_params(axis="y", left=False, labelleft=False)
# axs[2].tick_params(axis="y", left=False, labelleft=False)
k=0
for ax in axs[:-1]:
    ax.grid(True, ls="dotted")
    ax.set_xlabel("$\mathdefault{\\chi}$ [rad]")
    ax.plot(chi_plt, w1(chi_plt).imag, "-", color=colors[2], label="Theory")
    ax.set_ylim([ylim_im_1,ylim_im_2])
    ax.set_yticks(ticks=ax.get_yticks())
    k+=1
axs[1].legend(loc=9, ncol=1, framealpha=1)#, bbox_to_anchor=(0,0.45))
# axs[1].yaxis.set_label_coords(-0.15,1)
# ax.set_xlim([chi[0]-0.2,chi[-1]+0.2])
# ax.yaxis.set_label_position("right")
# ax.set_ylabel("$w^\Im_{+,1}$", fontsize=12, rotation=270, va="bottom", ha="center")
axs[2].grid(True, ls="dotted")
axs[2].set_ylim([-1,1])
axs[2].set_yticks(ticks=axs[2].get_yticks()[::2])
axs[0].set_title("Fourier transform method", fontsize=11)
axs[1].set_title("Fit method", fontsize=11)
axs[2].set_title("Difference", fontsize=11)
print(np.average(abs(Im_1_avg_fit-Im_1_avg)/(Im_1_avg_fit_err**2+Im_1_avg_err**2)**0.5))

# plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images 1 column/Wv In 1p8 combined.pdf", format="pdf",bbox_inches="tight")


# with open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Results txt/No In/Wv12_Im No In"+inf_file_name[-10:]+".txt","w") as f:
#     np.savetxt(f,np.transpose([chi,Im_1_avg,Im_1_avg_err,Im_2_avg,Im_2_avg_err]), header="chi w_im1 w_im1_err w_im2 w_im2_err")
# with open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Results txt/No In/Wv12_Re No In"+inf_file_name[-10:]+".txt","w") as f:
#     np.savetxt(f,np.transpose([chi,Re_1,Re_err_1,Re_2,Re_err_2]), header="chi w_re1 w_re1_err w_re2 w_re2_err")
    
plt.show()