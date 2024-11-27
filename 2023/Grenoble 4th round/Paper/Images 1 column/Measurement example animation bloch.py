#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 19:01:51 2024

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
from scipy.optimize import curve_fit as fit
from scipy.special import jv
from pylab import *
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D 
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import cv2

rad=np.pi/180
plt.rcParams["mathtext.fontset"]='dejavusans'#['dejavusans', 'dejavuserif', 'cm', 'stix', 'stixsans', 'custom']
a_1= 0.751
a_1_err= 0.003
a_2= 0.660
a_2_err=0.003
a_21=a_2/a_1
# a_1= (2/5)*0.5
# a_1_err= 0.003
# a_2= 1/5*0.5
# a_2_err=0.003

# inf_file_name="TOF_vs_chi_A+B_22pt_pi16_1200s_09Nov1808"
inf_file_name="TOF_vs_chi_A+B_22pt_pi16_1200s_4P_11Nov1354"
# inf_file_name="TOF_vs_chi_A+B_22pt_pi16_1200s_4P_11Nov0502"
# inf_file_name="TOF_vs_chi_A+B_In1_22pt_pi16_2000s_4P_16Nov1733"
# inf_file_name="TOF_vs_chi_A+B_In1_22pt_pi16_1200s_4P_15Nov0927"
alpha_1=0.1923 #/2.354
alpha_1_err=0.0009 
alpha_2=0.1971 #/2.354
alpha_2_err=0.0004


def w1(chi):
    return (1/(1+a_21*np.exp(1j*chi)))

def w2(chi):
    return (1-1/(1+a_21*np.exp(1j*chi)))

def fit_cos(x, A, B, C, D):
    return A/2*(1+B*jv(0,alpha_1)*jv(0,alpha_2)*np.cos(C*x-D))

A_aus=1
def fit_Im(t, A, B, xi_1, xi_2):
    return A+B*np.cos(chi_aus+alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)-alpha_2*np.sin(2*np.pi*1e-3*f_2*t+xi_2))

sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/TOF A+B/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"
niels_path="/home/aaa/Desktop/Niels/Data/"+inf_file_name
niels_fourier_path="/home/aaa/Desktop/Niels/Fourier/"+inf_file_name


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
            # a_2=tot_data[0,-4]
            # a_1=tot_data[0,-7]
            print("f1=", f_1)
            print("f2=", f_2)
            # print("a1=", a_1)
            # print("a2=", a_2)
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
P0=[(np.amax(ps_data)+np.amin(ps_data))/2, 0.6, 3, 0.]
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


colors=["k","#f10d0c","#00a933","#5983b0"]
sec=1
p_fit=[128.99298884/sec,  97.63956079/sec,   2.2038275,    1.2313203]
for i in range(3):#len(chi)):
    func_data=matrix[i]
    func_data_err=matrix_err[i]
    chi_aus=chi[i]
    # print(P0)
    # B0=([0,0, chi[0]-0.5, 2, 1],[200,150, chi[-1]+0.5, 2.5, 1.2])
    # p_Im,cov_Im = fit(fit_Im, time, func_data/sec, p0=p_fit)
    
    fig = plt.figure(figsize=(10, 4), dpi=200)
    gs=GridSpec(2,2, width_ratios=(3,1), height_ratios=(1.5,1), wspace=0.2, figure=fig)
    axs = [fig.add_subplot(gs[:,0]), fig.add_subplot(gs[0,-1], projection="3d"),fig.add_subplot(gs[1,-1])]
    
    axs[1].set_axis_off()
    # Make data
    r = 1
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    z = r * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Plot the surface
    axs[1].plot_surface(x, y, z, color='gray', alpha=0.1)
    
    # plot circular curves over the surface
    theta = np.linspace(0, 2 * np.pi, 100)
    z = np.zeros(100)
    x = r * np.sin(theta)
    y = r * np.cos(theta)
    
    axs[1].plot(x, y, z, color='black', alpha=0.3)
    axs[1].plot(z, x, y, color='black', alpha=0.3)
    axs[1].set_xlim(-r*0.8,r*0.8)
    axs[1].set_ylim(-r*0.8,r*0.8)
    axs[1].set_zlim(-r*0.5,r)
    axs[1].text(0,0,1.1,"$\left| 1 \\right\\rangle$",va="bottom", ha="center")
    axs[1].text(0,0,-1.1,"$\left| 2 \\right\\rangle$",va="top",ha="center")
    axs[1].text(1.2,0,0,"$\left| + \\right\\rangle$",ha="left",va="center")
    axs[1].text(-1.2,0,0,"$\left| - \\right\\rangle$",ha="right",va="center")
    axs[1].text(0,0,1.45,"Bloch sphere",va="bottom", ha="center")
    
    th=2*np.arctan(a_21)
    axs[1].quiver(0,0,0,r*np.sin(th)*np.cos(chi[i]), r*np.sin(th)*np.sin(chi[i]), 
                r*np.cos(th), color=colors[1], label="$\left| \psi_{in} \\right\\rangle$")
    axs[1].quiver(0,0,0, 1, 0, 0, color=colors[3],label="$\left| + \\right\\rangle$")
    zeros = np.zeros(1000)
    line = np.linspace(-r,r,1000)
    
    axs[1].plot(line, zeros, zeros, color='black', alpha=0.75)
    axs[1].plot(zeros, line, zeros, color='black', alpha=0.75)
    axs[1].plot(zeros, zeros, line, color='black', alpha=0.75)
    axs[1].legend(loc=10, bbox_to_anchor=(-0.05,0.2))
    # axs[1].set_title("Bloch sphere")
    # axs[1].tick_params(axis="y", labelbottom=False, bottom = False,labelleft=False, left = False)
    # axs[1].tick_params(axis="x", pad=-4)
    # axs[1].set_xticks([0,np.pi/2,np.pi,np.pi*3/2])
    # axs[1].set_xticklabels(['0','$\pi/2$','$\pi$','$3\pi/2$'])
    # axs[1].grid(False)
    # axs[1].set_ylim([0,1])
    # axs[1].set_title("$\chi$", y=1.1, bbox=dict(facecolor='none', edgecolor='k'))
    # fig.suptitle("$\chi=$"+str("%.2f"%(chi[i]/np.pi,))+ " $\pi$", bbox=dict(facecolor='white', edgecolor='k'), fontsize=11)
    # axs[1].text(3*np.pi/4,1.2,"$\chi=$"+str("%.2f"%(chi[i]/np.pi,))+"$\pi$",ha="right",va="bottom", bbox=dict(facecolor='white', edgecolor='k'), fontsize=11)
    axs[0].grid(True, ls="dotted")
    axs[0].errorbar(time, matrix[i], yerr= matrix_err[i], fmt=".", color=colors[3], alpha=0.8, ms=3, capsize=2, label="Data")
    axs[0].errorbar(time_plt, fit_Im(time_plt, *p_fit),fmt="-", color=colors[0], lw=2, label="Fit theory")
    axs[0].set_ylim([0, 300])
    axs[0].set_ylabel("Intensity (counts/1200sec)")
    axs[0].set_xlabel("Time [$\mu\,$s]")
    axs[0].legend(framealpha=1,ncol=2, loc=1)
    # axs[1].plot([0,chi[i]],[0,1], "-k.")
    axs[2].errorbar(chi/np.pi,ps_data/1200, yerr=ps_data**0.5/1200,fmt="ko",capsize=3, ms=3)
    axs[2].errorbar(chi[i]/np.pi,ps_data[i]/1200, yerr=ps_data[i]**0.5/1200,fmt="o",color=colors[1],capsize=3, ms=3)
    axs[2].plot(chi_plt/np.pi,fit_cos(ps_plt, *p)/1200, color=colors[3])
    axs[2].set_ylabel("Time-averaged\nintensity")
    axs[2].set_xlabel("$\chi$ $[rad/\pi]$")

    # plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images 1 column/Animation/chi"+str(i)+".png", format='png',bbox_inches='tight')
    # plt.close(fig)

    # k+=1

