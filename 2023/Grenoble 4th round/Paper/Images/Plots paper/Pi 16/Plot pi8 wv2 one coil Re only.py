#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 15:14:27 2024

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
a_1= 0.751
a_1_err= 0.003
a_2= 0.660
a_2_err=0.003
a_21=a_2/a_1
a_21_err= a_21*((a_1_err/a_1)**2+(a_2_err/a_2)**2)**0.5

# inf_file_name="TOF_vs_chi_B_19pt_pi4_1200s_04Nov1031"
# inf_file_name="TOF_vs_chi_B_19pt_pi8_1200s_04Nov2355"
# inf_file_name_pi8="TOF_vs_chi_B_19pt_pi8_1200s_05Nov1240"
inf_file_name_pi8="TOF_vs_chi_B_22pt_pi8_1200s_07Nov0219"
inf_file_name_pi16="TOF_vs_chi_B_22pt_pi16_1200s_07Nov1016" 
# inf_file_name_pi16="TOF_vs_chi_B_19pt_pi16_1200s_06Nov0126" 

alpha_2_pi8=0.3942 #/2.354
alpha_2_pi8_err=0.0008

alpha_2_pi16=0.1971 #/2.354
alpha_2_pi16_err=0.0004


def w1(chi):
    return (1/(1+a_21*np.exp(1j*chi)))

def w2(chi):
    return (1-1/(1+a_21*np.exp(1j*chi)))

def w2_Im(chi, a_21, chi_0):
    return (1-1/(1+a_21*np.exp(1j*(chi-chi_0)))).imag

def w1_Im(chi, a_21, chi_0):
    return (1/(1+a_21*np.exp(1j*(chi-chi_0)))).imag

def djv0(x):
    return (x*np.cos(x)-np.sin(x))/x**2

def fit_cos(x, A, B, C, D):
    return A/2*(1+B*np.cos(C*x-D))
    # return A/2*(1+B*np.cos(C*x-D))
A_aus=1
def fit_Im(t, B, Im_2, xi_2):
    return B*(1-2*Im_2*np.sin(2*np.pi*1e-3*f_2*t+xi_2))

sorted_fold_path_pi8="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/TOF B/"+inf_file_name_pi8
cleandata_pi8=sorted_fold_path_pi8+"/Cleantxt"

i=0
for root, dirs, files in os.walk(cleandata_pi8, topdown=False):
    files=np.sort(files)
    # print(files)
    for name in files:
        # print(name)
        if i==0:
            tot_data_pi8=np.loadtxt(os.path.join(root, name))[:,:]
            time=tot_data_pi8[:,1]
            f_2=tot_data_pi8[0,-3]*1e-3
            print("f2=", f_2)
            # print("a2=", am_1)
            i=1
        else:
            data_pi8=np.loadtxt(os.path.join(root, name))[:,:]
            tot_data_pi8 = np.vstack((tot_data_pi8, data_pi8))
time_plt=np.linspace(time[0], time[-1], 1000)
ps_pos=tot_data_pi8[::len(time),-1]
N = len(time)
S_F=50
matrix_pi8=np.zeros((len(ps_pos),len(time)))
matrix_pi8_err=np.zeros((len(ps_pos),len(time)))
for i in range(len(ps_pos)):
    matrix_pi8[i]=tot_data_pi8[:,5][tot_data_pi8[:,-1]==ps_pos[i]]
    matrix_pi8_err[i]=matrix_pi8[i]**0.5

sorted_fold_path_pi16="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/TOF B/"+inf_file_name_pi16
cleandata_pi16=sorted_fold_path_pi16+"/Cleantxt"
i=0
for root, dirs, files in os.walk(cleandata_pi16, topdown=False):
    files=np.sort(files)
    # print(files)
    for name in files:
        # print(name)
        if i==0:
            tot_data_pi16=np.loadtxt(os.path.join(root, name))[:,:]
            time=tot_data_pi16[:,1]
            f_2=tot_data_pi16[0,-3]*1e-3
            print("f1=", f_2)
            # print("a1=", am_1)
            i=1
        else:
            data_pi16=np.loadtxt(os.path.join(root, name))[:,:]
            tot_data_pi16 = np.vstack((tot_data_pi16, data_pi16))
time_plt=np.linspace(time[0], time[-1], 1000)
ps_pos=tot_data_pi16[::len(time),-1]
N = len(time)
S_F=50
matrix_pi16=np.zeros((len(ps_pos),len(time)))
matrix_pi16_err=np.zeros((len(ps_pos),len(time)))
for i in range(len(ps_pos)):
    matrix_pi16[i]=tot_data_pi16[:,5][tot_data_pi16[:,-1]==ps_pos[i]]
    matrix_pi16_err[i]=matrix_pi16[i]**0.5    

int_data_pi16=np.sum(matrix_pi16, axis=1)
int_data_pi16_err=np.sum(matrix_pi16_err**2, axis=1)**0.5
int_data_pi8=np.sum(matrix_pi8, axis=1)
int_data_pi8_err=np.sum(matrix_pi8_err**2, axis=1)**0.5

P0=[(np.amax(int_data_pi8)+np.amin(int_data_pi8))/2, (np.amax(int_data_pi8)-np.amin(int_data_pi8))/2, 3, -0.5]
B0=([100,0,0.01,-10],[np.amax(int_data_pi8)+10000,np.amax(int_data_pi8)+10000,5, 10])
p_int_pi8,cov_int_pi8=fit(fit_cos, ps_pos, int_data_pi8, p0=P0,  bounds=B0)
err_int_pi8=np.diag(cov_int_pi8)**0.5
j0_2=jv(0,alpha_2_pi8)
j0_2_err=abs(djv0(alpha_2_pi8)*alpha_2_pi8_err)
C_D_pi8=(2*a_1*a_2*j0_2)
C_id_pi8 = p_int_pi8[1]/C_D_pi8
C_id_pi8_err = ((C_D_pi8*err_int_pi8[1])**2+(C_D_pi8*a_1_err/a_1)**2+(C_D_pi8*j0_2_err/j0_2)**2)**0.5
A_pi8=p_int_pi8[0]*(1-C_id_pi8)/2
A_pi8_err= (((1-C_id_pi8)/2*err_int_pi8[0])**2+(p_int_pi8[0]/2*C_id_pi8_err)**2)**0.5
A_aus_pi8=p_int_pi8[0]
A_aus_pi8_err=err_int_pi8[0]
w_ps_pi8=p_int_pi8[-2]
chi_0_pi8=p_int_pi8[-1]
chi_0_pi8_err=err_int_pi8[-1]
print("A(1-C)/2=", A_pi8, "+-", A_pi8_err)
print("C=",C_id_pi8, "+-", C_id_pi8_err)
print("chi_err=",err_int_pi8[-1])
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
ax.errorbar(ps_pos,int_data_pi8, yerr=int_data_pi8_err,fmt="ko",capsize=5, ms=3)
ax.plot(ps_plt,fit_cos(ps_plt, *p_int_pi8), "b")
ax.vlines(p_int_pi8[-1]/p_int_pi8[-2],fit_cos(p_int_pi8[-1]/p_int_pi8[-2]+np.pi,*p_int_pi8),fit_cos(p_int_pi8[-1]/p_int_pi8[-2],*p_int_pi8), color="k")

chi_pi8=ps_pos*w_ps_pi8-chi_0_pi8
chi_pi8_plt=np.linspace(chi_pi8[0], chi_pi8[-1], 1000)

P0=[(np.amax(int_data_pi16)+np.amin(int_data_pi16))/2, (np.amax(int_data_pi16)-np.amin(int_data_pi16))/2, 3, -0.5]
B0=([100,0,0.01,-10],[np.amax(int_data_pi16)+10000,np.amax(int_data_pi16)+10000,5, 10])
p_int_pi16,cov_int_pi16=fit(fit_cos, ps_pos, int_data_pi16, p0=P0,  bounds=B0)
err_int_pi16=np.diag(cov_int_pi16)**0.5
j0_2=jv(0,alpha_2_pi16)
j0_2_err=abs(djv0(alpha_2_pi16)*alpha_2_pi16_err)
C_D_pi16=(2*a_1*a_2*j0_2)
C_id_pi16 = p_int_pi16[1]/C_D_pi16
C_id_pi16_err = ((C_D_pi16*err_int_pi16[1])**2+(C_D_pi16*a_1_err/a_1)**2+(C_D_pi16*j0_2_err/j0_2)**2)**0.5
A_pi16=p_int_pi16[0]*(1-C_id_pi16)/2
A_pi16_err= (((1-C_id_pi16)/2*err_int_pi16[0])**2+(p_int_pi16[0]/2*C_id_pi16_err)**2)**0.5
A_aus_pi16=p_int_pi16[0]
A_aus_pi16_err=err_int_pi16[0]
w_ps_pi16=p_int_pi16[-2]
chi_0_pi16=p_int_pi16[-1]
chi_0_pi16_err=err_int_pi16[-1]
print("A(1-C)/2=", A_pi16, "+-", A_pi16_err)
print("C=",C_id_pi16, "+-", C_id_pi16_err)
print("chi_err=",err_int_pi16[-1])
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
ax.errorbar(ps_pos,int_data_pi16, yerr=int_data_pi16_err,fmt="ko",capsize=5, ms=3)
ax.plot(ps_plt,fit_cos(ps_plt, *p_int_pi16), "b")
ax.vlines(p_int_pi16[-1]/p_int_pi16[-2],fit_cos(p_int_pi16[-1]/p_int_pi16[-2]+np.pi,*p_int_pi16),fit_cos(p_int_pi16[-1]/p_int_pi16[-2],*p_int_pi16), color="k")

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
ax.errorbar(ps_pos,int_data_pi8, yerr=int_data_pi8_err,fmt="ko",capsize=5, ms=3)
ax.plot(ps_plt,fit_cos(ps_plt, *p_int_pi8), "b")
ax.vlines(p_int_pi8[-1]/p_int_pi8[-2],fit_cos(p_int_pi8[-1]/p_int_pi8[-2]+np.pi,*p_int_pi8),fit_cos(p_int_pi8[-1]/p_int_pi8[-2],*p_int_pi8), color="k")

int_data_pi8_corr_err=(int_data_pi8_err**2/(C_id_pi8*A_aus_pi8)**2+int_data_pi8**2*A_aus_pi8_err**2/(A_aus_pi8**2*C_id_pi8)**2+((int_data_pi8/A_aus_pi8-0.5)/C_id_pi8**2)**2*C_id_pi8_err**2)**0.5
int_data_pi8_corr=(int_data_pi8-A_aus_pi8/2)/(A_aus_pi8*C_id_pi8)+1/2

int_data_pi16_corr_err=(int_data_pi16_err**2/(C_id_pi16*A_aus_pi16)**2+int_data_pi16**2*A_aus_pi16_err**2/(A_aus_pi16**2*C_id_pi16)**2+((int_data_pi16/A_aus_pi16-0.5)/C_id_pi16**2)**2*C_id_pi16_err**2)**0.5
int_data_pi16_corr=(int_data_pi16-A_aus_pi16/2)/(A_aus_pi16*C_id_pi16)+1/2


fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
ax.errorbar(ps_pos,int_data_pi8_corr, yerr=int_data_pi8_corr_err,fmt="ko",capsize=5, ms=3)
ax.errorbar(ps_pos,int_data_pi16_corr, yerr=int_data_pi16_corr_err,fmt="ro",capsize=5, ms=3)
ax.errorbar(ps_pos,(int_data_pi8_corr-int_data_pi16_corr)/(int_data_pi16_corr*w1(chi_pi8).real), yerr=int_data_pi16_corr_err,fmt="go",capsize=5, ms=3)
# ax.plot(ps_plt,fit_cos(ps_plt, *p_int), "b")
# ax.vlines(p_int[-1]/p_int[-2],fit_cos(p_int[-1]/p_int[-2]+np.pi,*p_int),fit_cos(p_int[-1]/p_int[-2],*p_int), color="k")

P0=[300,300, -0.8, 1]
p_tot=np.zeros((len(ps_pos),len(P0)))
err_tot=np.zeros((len(ps_pos),len(P0)))



psi_in=(int_data_pi8_corr-0.5)/jv(0,alpha_2_pi8)+0.5
# fig = plt.figure(figsize=(8,6))
# ax = fig.add_subplot(111)
# ax.plot(psi_in)
Re_2=(int_data_pi8_corr-psi_in)/psi_in/alpha_2_pi8**2/3
Re_err_2=Re_2*0

ylim1=-3.5
ylim2=2.5
y1=0.512
y2=0.135
xlim1=chi_pi8[0]-0.2
xlim2=chi_pi8[-7]-0.2
ylabels=np.arange(ylim1,ylim2,1)
d=0.02
h=0.05
fig = plt.figure(figsize=(5,6))
# fig, axs = plt.subplots(1, 2, figsize=(10, 4))
gs = fig.add_gridspec(2, 1,  height_ratios=(1, 6), hspace=0.1)
axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[1, 0])]
axs[0].spines["bottom"].set_visible(False)
axs[1].spines["top"].set_visible(False)

axs[0].tick_params(axis="x", bottom=False, labelbottom=False)
axs[0].set_title("$w_{+,1}$")# $(a_2/a_1\\approx$"+str("%.2f" % (a_21),)+")")
colors=["k","#f10d0c","#00a933","#5983b0"]
for ax in axs:
    ax.errorbar(chi_pi8, Re_2, Re_err_2, fmt=".", color=colors[2], capsize=3)
    # ax.plot(chi_pi8_plt, abs(w1(chi_pi8_plt))**2-w1(chi_pi8_plt).real, "--", color=colors[2], alpha=0.5)
    ax.plot(chi_pi8_plt, w1(chi_pi8_plt).real, "--", color=colors[3], alpha=0.5)
    ax.grid(True, ls="dotted")
    # ax.set_xlim([xlim1,xlim2])
# axs[0].set_ylim([-2.5,5])
# axs[0].set_ylim([6,np.amax(Re_2)+np.amax(Re_err_2)*1.5])
# axs[1].set_ylim([ylim1,ylim2])
# axs[1].set_yticks(ticks=ylabels)
axs[1].set_xlabel("$\\chi$ [rad]")
# axs[0].plot([xlim1,xlim2],[ylim1,ylim1], "r", lw=1, ls=(0,(5,3)))
# axs[0].plot([xlim1,xlim2],[ylim2,ylim2], "r", lw=1, ls=(0,(5,3)))

# kwargs = dict(transform=axs[1].transAxes, color='k', lw=0.8, clip_on=False)
# axs[1].plot((-d, d), (1-d, 1+d), **kwargs)
# axs[1].plot((1-d, 1+d), (1-d, 1+d), **kwargs)
# axs[1].plot((-d, d), (1+h-d, 1+h+d), **kwargs)
# axs[1].plot((1-d, 1+d), (1+h-d, 1+h+d), **kwargs)
# ax.legend()
# plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images/Wv1"+inf_file_name[-10:]+"ver2.pdf", format="pdf",bbox_inches="tight")

plt.show()