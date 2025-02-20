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
# plt.rcParams["mathtext.fontset"]=""
plt.rcParams.update(plt.rcParamsDefault)
colors=["k","#f10d0c","#00a933","#5983b0"]
# colors=["k","k","#00a933","#5983b0"]

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

ps_data=np.average(matrix, axis=1)
ps_data_err = (np.sum(matrix_err**2, axis=1))**0.5/len(time)
P0=[(np.amax(ps_data)+np.amin(ps_data))/2, 0.6, 3, -1.]
B0=([0,0,0.01,-10],[np.amax(ps_data)+10000,2,5, 10])
p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
err=np.diag(cov)**0.5
Co = 0.731#0.70456183532707045 
Co_err= 0.00646151528318766
C_int=p[1]
print("C=",p[1]/p[0])
A=p[0]*(1-Co)/2
A_err= (((1-Co)/2*err[0])**2+(p[0]/2*err[1])**2)**0.5
A_aus=p[0]/len(time)
w_ps=p[-2]
chi_0=p[-1]
chi_0_err=err[-1]
chi=ps_pos#*w_ps-chi_0
chi_plt=np.linspace(chi[0], chi[-1], 200)
print("A(1-C)/2=", A, "+-", A_err)
print("C=",p[1], "+-", err[1])
print("chi_err=",err[-1])

n_r=7
fig = plt.figure(figsize=(7,2), dpi=150)
gs = fig.add_gridspec(n_r,2, width_ratios=(1.5,1), hspace=0,wspace=0)#,wspace=-0.056)
axs = [fig.add_subplot(gs[:, 0]),fig.add_subplot(gs[1:-1, 1])]
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],200)
axs[0].set_title("Time-averaged intensity", fontsize=10)
axs[0].errorbar(chi,ps_data, yerr=ps_data_err,fmt="ko",capsize=3, ms=3, label="Data")
axs[0].errorbar(chi[-6],ps_data[-6], fmt="o",color=colors[1],capsize=3, ms=10, mfc="none")
# axs[0].errorbar(chi[-6:],ps_data[-6]+0*chi[-6:],fmt="k--", lw=1)
axs[0].plot(chi_plt,fit_cos(ps_plt, *p), color=colors[2], label="Fit")
oldlim=axs[0].get_xlim()
axs[0].hlines(ps_data[-6],chi[-6]+0.07,chi[-1]+1, color=colors[1], ls=(2, (8, 3)), lw=1)
# axs[0].set_xlabel("$\\chi$ [rad]")
axs[0].set_xlabel("Phase shifter rotation [deg]")
axs[0].set_ylabel("Average intensity")
axs[1].set_ylabel("Neutron rate\n[counts/1200sec]", rotation=270, labelpad=22.5)
axs[1].yaxis.set_label_position("right")
axs[0].set_ylim([0,260])
axs[0].set_xlim(oldlim)
axs[0].grid(True, ls="dotted")
axs[0].plot([chi[-6], oldlim[1]],[ps_data[-6], 240/n_r*(n_r-1)], "-", color=colors[0],lw=0.8)
axs[0].plot([chi[-6], oldlim[1]],[ps_data[-6], 240/n_r], "-",color=colors[0], lw=0.8)
# axs[0].plot([chi[-6], 1.5],[ps_data[-6], 240/n_r*(n_r-1)], "k-", lw=0.8)
# axs[0].plot([chi[-6], 1.5],[ps_data[-6], 240/n_r], "k-", lw=0.8)


# axs[0].set_xticks([*axs[0].get_xticks()[1:-1],4.51])
# axs[0].vlines(4.51,0,ps_data[-6], color="k", ls="dashed", lw=1)
P0=[300,300, -0.8, 1]
p_tot=np.zeros((len(ps_pos),len(P0)))
err_tot=np.zeros((len(ps_pos),len(P0)))

k=0
[6,8,13,16]
p_fit=[128.99298884,  97.63956079,   2.2038275,    1.2313203]
colors_point=[(0.8,0.8,0.8),(0.9,0.8,0.8),(0.8,0.9,0.8),(0.85,0.85,1)]
colors_point_2=[(0.6,0.6,0.6),(0.9,0.6,0.6),(0.6,0.8,0.6),(0.7,0.7,1)]
for i in [-6]:
    func_data=matrix[i]
    func_data_err=matrix_err[i]
    chi_aus=chi[i]
    # P0=[0.1,0.05, 2.3, 2]
    # # print(P0)
    # B0=([0,0, 0, 0],[1,1, np.pi, np.pi])
    # p_Im,cov_Im = fit(fit_Im, time, func_data, p0=P0, bounds=B0)
    # err_Im=np.diag(cov_Im)**0.5
    # print(p_Im[-2],p_Im[-1])
    # print(p_Im,err_Im)
    # Im_data_fit[i]=p_Im[2]
    # Im_data_fit_err[i]=(err_Im[2]**2+np.sin(chi[i])**2*chi_0_err**2)**0.5
    # cos2_fit[i]=p_Im[1]*p_Im[0]#*Co#+p_Im[0]*(1-Co)/2
    # cos2_fit_err[i]=err_Im[1]
    yf_data = fft(func_data)
    yf_data_err = np.ones(len(yf_data))*np.sum(matrix_err)**0.5
    # print(sum(abs(yf_data)))
    xf = fftfreq(N, S_F)*1e3
    
    axs[1].grid(True, ls="dotted")
    axs[1].errorbar(time, matrix[i], yerr= matrix_err[i], fmt=".",  color=colors[3], capsize=2, ms=3, elinewidth=1, label="Data")# $\chi\\approx$"+str("%.2f"%chi[i],))
    # axs[1].errorbar(time, matrix[i], fmt=".",  color=colors[3], capsize=3)
    # ax.fill_between(time,  matrix[i]-matrix_err[i],matrix[i]+matrix_err[i],color=colors[k], alpha=0.2, label="$\chi=$"+str("%.2f"%chi[i],))
    # axs[1].errorbar(time_plt, fit_Im(time_plt, *p_fit),fmt="-", color=colors[1])
    # ax.plot(time, matrix[i],".", color=colors[k], alpha=0.2, label="$\chi=$"+str("%.2f"%chi[i],))
    # ax.set_title(str("%.2f"%chi[i],))
    axs[1].errorbar([-40,*time],np.average(matrix[i]), fmt="-",  color=colors[1], label="Average")
    axs[1].set_ylim([240/n_r,240/n_r*(n_r-1)])
    # avg=np.average(matrix[i])
    # ax.set_ylim([avg-0.06,avg+0.06])
    # ax.set_yticks(ticks=[avg-0.03,avg,avg+0.03])
    # ax.set_yticklabels([str("%.2f"%abs(avg-0.03),),str("%.2f"%avg,),str("%.2f"%(avg+0.03),)])
    axs[1].set_xlabel("Time [$\mu$s]")
    # axs[1].set_ylabel("Neutron rate (count / s)")
    k+=1
oldlim1=axs[1].get_xlim()
axs[1].tick_params(axis="both", left=False, labelleft=False, right=True, labelright=True)
axs[1].set_title("Time-resolved intensity", fontsize=10)
axs[1].spines["left"].set_visible(False)
axs[0].spines["right"].set_visible(False)
axs[0].spines["top"].set_visible(False)
axs[0].spines["bottom"].set_visible(False)

# axs[1].hlines(ps_data[-6], oldlim1[0],0, color="k")
axs[1].set_xlim([-70,2070])

h=1
kwargs = dict(transform=axs[0].transAxes, color='k', lw=0.8, clip_on=False)
axs[0].plot((h, h), (0, 0.76/n_r), **kwargs)
axs[0].plot((h, h), (1.04/n_r*(n_r-1), 1), **kwargs)
axs[0].plot((0, h), (1, 1), **kwargs)
axs[0].plot((0, h), (0, 0), **kwargs)
# axs[0].plot((1, 1), (1/n_r, 1/n_r*(n_r-1)), **kwargs, ls="--")
# axs[0].plot((-1, 0), (0, 0), **kwargs)

# axs[1].set_xticks(axs[1].get_xticks()[:])
# axs[0].set_yticks(axs[0].get_yticks()[::2])
axs[1].set_yticks(axs[0].get_yticks()[1:-1])
for ax in axs:
    ax.legend(ncol=2)
# ax.legend(ncol=4, bbox_to_anchor=(0.5,1.1), loc="center")
inf_file_names=[
"ifg_-2to2_30s_12Nov0443", 
# "ifg_-2to2_30s_12Nov2048",  
# "ifg_-2to2_30s_12Nov1219", 
# "ifg_-2to2_30s_12Nov1956", 
# "ifg_-2to2_30s_12Nov2024",
]

colors=["k","#f10d0c","#00a933","#5983b0"]
C=np.array([])
chi_0=np.array([])
C_err=np.array([])
# fig = plt.figure(figsize=(4.5,2.5), dpi=200)
# ax = fig.add_subplot(111)
k=1
# ax.errorbar([],[],[],fmt="o", color="w", capsize=3, ms=3, label="$\mathrm{\mathbf{Date\ and\ time}}$")
for inf_file_name in inf_file_names:
    # if "20s" in inf_file_name:
        print(inf_file_name)
        sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/Ifg off/"+inf_file_name
        cleandata=sorted_fold_path+"/Cleantxt"
        for root, dirs, files in os.walk(cleandata, topdown=False):
            files=np.sort(files) 
            for name in files[:]:
                # print(name)
                tot_data=np.loadtxt(os.path.join(root, name))[:,:]
                data_ifg=tot_data[:,5]/30
                # print(data_ifg)
                data_ifg_err=tot_data[:,5]**0.5/30
                ps_pos=tot_data[:,0]
                P0=[(np.amax(ps_data)+np.amin(ps_data))/2, 0.6, 3, -1.]
                B0=([0,0,0.01,-10],[np.amax(ps_data)+10000,2,5, 10])
                p,cov=fit(fit_cos, ps_pos, data_ifg, p0=P0,  bounds=B0)
                err=np.diag(cov)**0.5
                # print(p[3], err[3])
                x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
                # fig.suptitle(name[:-4])
                # ax.set_ylabel("Arb.")
                axs[0].errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="o", color=colors[k], capsize=3, ms=3, label="Time "+inf_file_name[-4:-2]+":"+inf_file_name[-2:])
                axs[0].plot(x_plt,fit_cos(x_plt, *p), color=colors[k], lw=1)
                # ax.set_ylim([0,1500])
                C_ifg=np.append(C, p[1])
                chi_0=np.append(chi_0, p[-1])
                C_err=np.append(C_err,  ((err[1]/p[0])**2+(err[1]*p[1]/p[0]**2)**2)**0.5)
                k+=1
                
print(C_int/C_ifg)

# plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images 1 column/Time-average vs time-resolved.pdf", format="pdf",bbox_inches="tight")
plt.show()