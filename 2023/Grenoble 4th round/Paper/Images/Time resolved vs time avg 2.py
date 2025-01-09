#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 12:44:18 2025

@author: aaa
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
from scipy.special import jv

# plt.rcParams["mathtext.fontset"]=""
plt.rcParams.update(plt.rcParamsDefault)
colors=["k","#f10d0c","#00a933","#5983b0"]

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
    return A/2*(1+B*np.cos(C*x-D))

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

ps_data=np.average(matrix, axis=1)/1200
ps_data_err = (np.sum(matrix_err**2, axis=1))**0.5/len(time)/1200
P0=[(np.amax(ps_data)+np.amin(ps_data))/2, 0.6, 3, -1.]
B0=([0,0,0.01,-10],[np.amax(ps_data)+100,2,5, 10])
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
chi=ps_pos*w_ps-chi_0
chi_plt=np.linspace(chi[0], chi[-1], 200)
print("A(1-C)/2=", A, "+-", A_err)
print("C=",p[1], "+-", err[1])
print("chi_err=",err[-1])

fig = plt.figure(figsize=(8.5,5), dpi=150)
# gs = fig.add_gridspec(1,2, width_ratios=(1,1), hspace=0.0,wspace=0.25)
# axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[0, 1])]
ax=fig.add_subplot(111)
sub_ax = inset_axes(
    parent_axes=ax,
    loc=4,
    # bbox_to_anchor=(0.5,0.5),
    # bbox_to_anchor=(np.pi-0.6, 0.1, 2, 0.1),
    # bbox_transform=ax.transData,
    width="10%",
    height="60%",
    borderpad=1  # padding between parent and inset axes
)
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],200)
ax.errorbar(chi,ps_data, yerr=ps_data_err,fmt="ko",capsize=3, ms=3)
ax.plot(chi_plt,fit_cos(ps_plt, *p), color=colors[2])
# ax.vlines(p[-1]/p[-2],fit_cos(p[-1]/p[-2]+np.pi,*p),fit_cos(p[-1]/p[-2],*p), color="k")
ax.set_xlabel("$\\chi$ [rad]")
ax.set_ylabel("Neutron rate (count / s)")
ax.set_yticks(ax.get_yticks()[::2])

P0=[300,300, -0.8, 1]
p_tot=np.zeros((len(ps_pos),len(P0)))
err_tot=np.zeros((len(ps_pos),len(P0)))

k=0
[6,8,13,16]
p_fit=[128.99298884/1200,  97.63956079/1200,   2.2038275,    1.2313203]
for i in [-6]:
    func_data=matrix[i]
    func_data_err=matrix_err[i]
    chi_aus=chi[i]
    # P0=[0.1,0.05, 2.3, 2]
    # # print(P0)
    # B0=([0,0, 0, 0],[1,1, np.pi, np.pi])
    # p_Im,cov_Im = fit(fit_Im, time, func_data/1200, p0=P0, bounds=B0)
    # err_Im=np.diag(cov_Im)**0.5
    # print(p_Im[-2],p_Im[-1])
    # print(p_Im,err_Im)
    # Im_data_fit[i]=p_Im[2]
    # Im_data_fit_err[i]=(err_Im[2]**2+np.sin(chi[i])**2*chi_0_err**2)**0.5
    # cos2_fit[i]=p_Im[1]*p_Im[0]#*Co#+p_Im[0]*(1-Co)/2
    # cos2_fit_err[i]=err_Im[1]
    
    sub_ax.grid(True, ls="dotted")
    sub_ax.errorbar(time, matrix[i]/1200, yerr= matrix_err[i]/1200, fmt=".",  color=colors[3], capsize=2, elinewidth=1, ms=2, label="$\chi=$"+str("%.2f"%chi[i],))
    # ax.fill_between(time,  matrix[i]/1200-matrix_err[i]/1200,matrix[i]/1200+matrix_err[i]/1200,color=colors[k], alpha=0.2, label="$\chi=$"+str("%.2f"%chi[i],))
    # ax.errorbar(time_plt+time[-1]*i, fit_Im(time_plt, *p_fit),fmt="-", color=colors[0])
    # ax.plot(time, matrix[i]/1200,".", color=colors[k], alpha=0.2, label="$\chi=$"+str("%.2f"%chi[i],))
    # ax.set_title(str("%.2f"%chi[i],))
    # ax.errorbar(xf, np.abs(yf_data), np.abs(yf_data_err), fmt="k.", capsize=5)
    sub_ax.set_ylim([0,0.2])
    # avg=np.average(matrix[i]/1200)
    # ax.set_ylim([avg-0.06,avg+0.06])
    # ax.set_yticks(ticks=[avg-0.03,avg,avg+0.03])
    # ax.set_yticklabels([str("%.2f"%abs(avg-0.03),),str("%.2f"%avg,),str("%.2f"%(avg+0.03),)])
    sub_ax.set_xlabel("Time [$\mu\,$s]")
    # sub_ax.set_ylabel("[count / s]")
    k+=1
sub_ax.set_xlim([0,time[-1]])

sub_ax.set_yticks(ax.get_yticks()[::2])
# ax.legend(framealpha=1, ncol=3, loc=9, bbox_to_anchor=(0.5, 1.22))
# ax.legend(ncol=4, bbox_to_anchor=(0.5,1.1), loc="center")
# plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images/Measurement_example.pdf", format="pdf",bbox_inches="tight")
plt.show()