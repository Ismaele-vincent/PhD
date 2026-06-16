# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 15:50:57 2025

@author: S18
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
from datetime import datetime

a_1=1/3**0.5
a_1_err=0
a_2=1/3**0.5
a_2_err=0
a_3=1/3**0.5
a_3_err=0
chi_1_0=0
chi_2_0=0
chi_3_0=0

# C_12=0.69
# C_13=0.74
# C_23=0.62

points=32
points_per=16

dtype_new = np.dtype([
    ("PS", "U50"),
    ("date", "U50"),
    ("value", "f8"),
    ("index", "i8")
])


def fit_cos(x, A, B, C, D):
    return A*(1+B*np.cos(C*x-D))/2

bad_apples=[
    ]
good_apples=[
    ]


def w1(chi_1, chi_2, chi_3):
    return a_1*np.exp(1j*(chi_1_0+chi_1))/(a_1*np.exp(1j*(chi_1_0+chi_1))+a_2*np.exp(1j*(chi_2_0+chi_2))+a_3*np.exp(1j*(chi_3_0+chi_3)))

def w2(chi_1, chi_2, chi_3):
    return a_2*np.exp(1j*(chi_2_0+chi_2))/(a_1*np.exp(1j*(chi_1_0+chi_1))+a_2*np.exp(1j*(chi_2_0+chi_2))+a_3*np.exp(1j*(chi_3_0+chi_3)))

def w3(chi_1, chi_2, chi_3):
    return a_3*np.exp(1j*(chi_3_0+chi_3))/(a_1*np.exp(1j*(chi_1_0+chi_1))+a_2*np.exp(1j*(chi_2_0+chi_2))+a_3*np.exp(1j*(chi_3_0+chi_3)))

sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Contrast loops/Cleantxt all"
chi_0=[0, np.pi/2, np.pi, 3*np.pi/2]

A_avg=0
Dchi=np.zeros(4)
C_avg=0
C_err=0

for root, dirs, files in os.walk(sorted_fold_path, topdown=False):
    files=np.sort(files)
    i=0
    C_O=np.array([], dtype=dtype_new)
    C_H=np.array([], dtype=dtype_new)
    C_OH=np.array([], dtype=dtype_new)
    C_aux=np.array([], dtype=dtype_new)
    
    for name in files[:]:
        if (name not in bad_apples):
            # print(name)
            tot_data=np.loadtxt(os.path.join(root, name))
            time_meas=tot_data[0,1]
            if ("B1" not in name):
                S=time_meas*tot_data[:,5]/np.average(tot_data[:,5])
            else:
                S=time_meas#
            data_O_err=tot_data[:,2]**0.5/S
            data_O=tot_data[:,2]/S
            data_H_err=tot_data[:,3]**0.5/S
            data_H=tot_data[:,3]/S
            data_OH_err=(tot_data[:,2]+tot_data[:,3])**0.5/S
            data_OH=(tot_data[:,2]+tot_data[:,3])/S
            data_aux_err=tot_data[:,5]**0.5/S
            data_aux=tot_data[:,5]/S
            ps_pos=tot_data[:,0]
            
            P0_O=[(np.amax(data_O)+np.amin(data_O))/2, 0.6, 6, -6.6]
            B0_O=([np.amin(data_O),0,5,-4*np.pi],[np.amax(data_O)*2,1,7, 1*np.pi])
            p_O,cov=fit(fit_cos, ps_pos, data_O, sigma=data_O_err, p0=P0_O,  bounds=B0_O)
            # print(p)
            err_O=np.diag(cov)**0.5
            A_O=p_O[0]
            A_O_err=err_O[0]
            C_O_fit=p_O[1]
            # C_O_fit=p_O[1]*A_O
            C_O_fit_err=err_O[1]
            
            P0_aux=[(np.amax(data_aux)+np.amin(data_aux))/2, 0.6, 6, -6.6]
            B0_aux=([np.amin(data_aux),0,5,-4*np.pi],[np.amax(data_aux)*2,1,7, 1*np.pi])
            p_aux,cov=fit(fit_cos, ps_pos, data_aux, sigma=data_aux_err, p0=P0_aux,  bounds=B0_aux)
            # print(p)
            err_aux=np.diag(cov)**0.5
            A_aux=p_aux[0]
            A_aux_err=err_aux[0]
            C_aux_fit=p_aux[1]
            # C_aux_fit=p_aux[1]*A_aux
            C_aux_fit_err=err_aux[1]   
            
            P0_H=[(np.amax(data_H)+np.amin(data_H))/2, 0.6, 6, -6.6]
            B0_H=([np.amin(data_H),0,5,-4*np.pi],[np.amax(data_H)*2,1,7, 1*np.pi])
            p_H,cov=fit(fit_cos, ps_pos, data_H, sigma=data_H_err, p0=P0_H,  bounds=B0_H)
            # print(p)
            err_H=np.diag(cov)**0.5
            A_H=p_H[0]
            A_H_err=err_H[0]
            C_H_fit=p_H[1]
            # C_H_fit=p_H[1]*A_H
            C_H_fit_err=err_H[1] 
            
            P0_OH=[(np.amax(data_OH)+np.amin(data_OH))/2, 0.6, 6, -6.6]
            B0_OH=([np.amin(data_OH),0,5,-4*np.pi],[np.amax(data_OH)*2,1,7, 1*np.pi])
            p_OH,cov=fit(fit_cos, ps_pos, data_OH, sigma=data_OH_err, p0=P0_OH,  bounds=B0_OH)
            # print(p)
            err_OH=np.diag(cov)**0.5
            A_OH=p_OH[0]
            A_OH_err=err_OH[0]
            C_OH_fit=p_OH[1]
            # C_OH_fit=p_OH[1]*A_OH
            C_OH_fit_err=err_OH[1] 
            
            ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
            chi= ps_pos*p_O[-2]-p_O[-1]
            chi_plt = np.linspace(chi[0], chi[-1],100)
            fig = plt.figure(figsize=(8,6))
            ax = fig.add_subplot(111)
            fig.suptitle(name[:-4])
            ax.errorbar(chi,data_O,yerr=data_O_err,fmt="ro",capsize=5, ms=3)
            ax.plot(chi_plt,fit_cos(ps_plt, *p_O), "r", label="O C="+"%.2f"%C_O_fit,)
            ax.errorbar(chi,data_H,yerr=data_H_err,fmt="yo",capsize=5, ms=3)
            ax.plot(chi_plt,fit_cos(ps_plt, *p_H), "y", label="H C="+"%.2f"%C_H_fit,)
            ax.errorbar(chi,data_aux,yerr=data_aux_err,fmt="go",capsize=5, ms=3)
            ax.plot(chi_plt,fit_cos(ps_plt, *p_aux), "g", label="Aux C="+"%.2f"%C_aux_fit,)
            ax.errorbar(chi,data_OH,yerr=data_OH_err,fmt="bo",capsize=5, ms=3)
            ax.plot(chi_plt,fit_cos(ps_plt, *p_OH), "b", label="O+H C="+"%.2f"%C_OH_fit,)
            # ax.errorbar(chi,S,yerr=data_O_err,fmt="ro",capsize=5, ms=3)
            # ax.legend(loc=4, ncol=4)
            y_max=ax.get_ylim()[1]
            ax.set_ylim([0,y_max])
            ax.set_xlabel("$\chi$ ("+name[-17:-14]+")")
            ax.set_ylabel("Arb.")


            if ("B1_ps1" in name):
                C_O=np.append(C_O, np.array([(name[-17:-4], name[-13:-4],C_O_fit,1)], dtype=dtype_new))
                C_H=np.append(C_H, np.array([(name[-17:-4], name[-13:-4],C_H_fit,1)], dtype=dtype_new))
                C_OH=np.append(C_OH, np.array([(name[-17:-4], name[-13:-4],C_OH_fit,1)], dtype=dtype_new))
                C_aux=np.append(C_aux, np.array([(name[-17:-4], name[-13:-4],C_aux_fit,1)], dtype=dtype_new))
                # fig = plt.figure(figsize=(8,6))
                # ax = fig.add_subplot(111)
                # fig.suptitle(name[:-4])
                # ax.errorbar(chi,data_O,yerr=data_O_err,fmt="ko",capsize=5, ms=3)
                # ax.plot(chi_plt,fit_cos(ps_plt, *p), "b", label="%.2f"%C_O,)
                # ax.legend()
            if ("B2_ps1" in name) or ("B2_ps2" in name):
                C_O=np.append(C_O, np.array([(name[-17:-4], name[-13:-4],C_O_fit,2)], dtype=dtype_new))
                C_H=np.append(C_H, np.array([(name[-17:-4], name[-13:-4],C_H_fit,2)], dtype=dtype_new))
                C_OH=np.append(C_OH, np.array([(name[-17:-4], name[-13:-4],C_OH_fit,2)], dtype=dtype_new))
                C_aux=np.append(C_aux, np.array([(name[-17:-4], name[-13:-4],C_aux_fit,2)], dtype=dtype_new))
            if ("B3_ps2" in name):
                C_O=np.append(C_O, np.array([(name[-17:-4], name[-13:-4],C_O_fit,3)], dtype=dtype_new))
                C_H=np.append(C_H, np.array([(name[-17:-4], name[-13:-4],C_H_fit,3)], dtype=dtype_new))
                C_OH=np.append(C_OH, np.array([(name[-17:-4], name[-13:-4],C_OH_fit,3)], dtype=dtype_new))
                C_aux=np.append(C_aux, np.array([(name[-17:-4], name[-13:-4],C_aux_fit,3)], dtype=dtype_new))
                # fig = plt.figure(figsize=(8,6))
                # ax = fig.add_subplot(111)
                # fig.suptitle(name[:-4])
                # ax.errorbar(chi,data_O,yerr=data_O_err,fmt="ko",capsize=5, ms=3)
                # ax.plot(chi_plt,fit_cos(ps_plt, *p), "b", label="%.2f"%C_O,)
                # ax.legend()
    
# print(C_O_PS12)
C_O = C_O[np.argsort(np.array([datetime.strptime(x, "%d%b%H%M") for x in (C_O["date"])]))]
C_H = C_H[np.argsort(np.array([datetime.strptime(x, "%d%b%H%M") for x in (C_H["date"])]))]
C_OH = C_OH[np.argsort(np.array([datetime.strptime(x, "%d%b%H%M") for x in (C_OH["date"])]))]
C_aux = C_aux[np.argsort(np.array([datetime.strptime(x, "%d%b%H%M") for x in (C_aux["date"])]))]

# y_labels_23=[""]
X_23=np.arange(len(C_O["value"][C_O["index"]==1]))
fig1 = plt.figure(figsize=(6,6))
fig1.suptitle("Contrast paths 2,3", y=0.93)
gs = fig1.add_gridspec(3, 1, height_ratios=(1,1,1), hspace=0.05, wspace=0.3) #width_ratios=(0.5,0.5,2), 
axs = [fig1.add_subplot(gs[0]),fig1.add_subplot(gs[1]),fig1.add_subplot(gs[2])]
axs[0].plot(X_23, C_O["value"][C_O["index"]==1], "ro", label="O")
axs[0].plot(X_23, C_H["value"][C_H["index"]==1], "yo", label="H")
axs[0].plot(X_23, C_aux["value"][C_aux["index"]==1], "go", label="Aux")
axs[1].plot(X_23, C_aux["value"][C_aux["index"]==1], "go", label="Aux")
axs[0].plot(X_23, C_OH["value"][C_OH["index"]==1], "bo", label="O+H")
axs[2].plot(X_23, C_aux["value"][C_aux["index"]==1]/C_O["value"][C_O["index"]==1], "ko", label="Aux/O")
axs[2].plot(X_23, C_aux["value"][C_aux["index"]==1]/C_H["value"][C_H["index"]==1], "co", label="Aux/H")
axs[2].plot(X_23, C_aux["value"][C_aux["index"]==1]/C_OH["value"][C_OH["index"]==1], "mo", label="Aux/(O+H)")
axs[-1].set_xticks(X_23)
axs[-1].set_xticklabels(C_O["PS"][C_O["index"]==1],rotation=45, ha='right')
axs[-1].set_xlabel("PS & Date & time")
axs[0].tick_params(axis="x", bottom=False, labelbottom=False)

ylims=np.array([])
for ax in axs:
    ax.grid()
    ax.legend(ncol=len(ax.get_legend_handles_labels()[1]))
    ylims=np.append(ylims, ax.get_ylim())
for ax in axs[1:-1]:
    lim_avg=np.average(ax.get_ylim())
    yrange=np.amax(ylims[1::2]-ylims[::2])
    ax.set_ylim([lim_avg-yrange/2,lim_avg+yrange/2])

X_13=np.arange(len(C_O["value"][C_O["index"]==2]))
fig1 = plt.figure(figsize=(8,6))
fig1.suptitle("Contrast paths 1,3", y=0.93)
gs = fig1.add_gridspec(4, 1, height_ratios=(1,1,1,1), hspace=0.05, wspace=0.3) #width_ratios=(0.5,0.5,2), 
axs = [fig1.add_subplot(gs[0]),fig1.add_subplot(gs[1]),fig1.add_subplot(gs[2]),fig1.add_subplot(gs[3])]
axs[0].plot(X_13, C_O["value"][C_O["index"]==2], "ro", label="O")
axs[1].plot(X_13, C_H["value"][C_H["index"]==2], "yo", label="H")
axs[1].plot(X_13[::2], C_aux["value"][C_aux["index"]==1], "go", label="Aux (loop 2-3)")
axs[1].plot(X_13[1::2], C_aux["value"][C_aux["index"]==1], "go")
axs[2].plot(X_13, C_aux["value"][C_aux["index"]==2], "go", label="Aux")
axs[2].plot(X_13, C_OH["value"][C_OH["index"]==2], "bo", label="O+H")
axs[3].plot(X_13[::2], C_aux["value"][C_aux["index"]==1]/C_O["value"][C_O["index"]==2][::2], "ko", label="Aux(loop 2-3)/O")
# axs[3].plot(X_13[::2], C_aux["value"][C_aux["index"]==1]/C_H["value"][C_H["index"]==2][::2], "co", label="Aux/H")
# axs[3].plot(X_13[::2], C_aux["value"][C_aux["index"]==1]/C_OH["value"][C_OH["index"]==2][::2], "mo", label="Aux/(O+H)")
axs[-1].set_xticks(X_13)
axs[-1].set_xticklabels(C_O["PS"][C_O["index"]==2],rotation=45, ha='right')
axs[-1].set_xlabel("PS & Date & time")
for ax in axs[:-1]:
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
ylims=np.array([])
for ax in axs:
    ax.grid()
    ax.legend(ncol=len(ax.get_legend_handles_labels()[1]))
    ylims=np.append(ylims, ax.get_ylim())
for ax in axs[:-1]:
    lim_avg=np.average(ax.get_ylim())
    yrange=np.amax(ylims[1::2]-ylims[::2])
    ax.set_ylim([lim_avg-yrange/2,lim_avg+yrange/2])

X_12=np.arange(len(C_O["value"][C_O["index"]==3]))
fig1 = plt.figure(figsize=(6,6))
fig1.suptitle("Contrast paths 1,2", y=0.93)
gs = fig1.add_gridspec(4, 1, height_ratios=(1,1,1,1), hspace=0.05, wspace=0.3) #width_ratios=(0.5,0.5,2), 
axs = [fig1.add_subplot(gs[0]),fig1.add_subplot(gs[1]),fig1.add_subplot(gs[2]),fig1.add_subplot(gs[3])]
axs[0].plot(X_12[1:], C_O["value"][C_O["index"]==3][1:], "ro", label="O")
axs[1].plot(X_12[1:], C_H["value"][C_H["index"]==3][1:], "yo", label="H")
axs[1].plot(X_12[1:], C_aux["value"][C_aux["index"]==1][1:], "go", label="Aux(loop 2-3)")
axs[2].plot(X_12[1:], C_aux["value"][C_aux["index"]==3][1:], "go", label="Aux")
axs[2].plot(X_12[1:], C_OH["value"][C_OH["index"]==3][1:], "bo", label="O+H")
# axs[2].plot(X_12[1:], C_aux["value"][C_aux["index"]==1][1:]/C_O["value"][C_O["index"]==3][1:], "ko", label="Aux/O")
# axs[3].plot(X_12[1:], C_aux["value"][C_aux["index"]==1][1:]/C_H["value"][C_H["index"]==3][1:], "co", label="Aux/H")
axs[3].plot(X_12[1:], C_aux["value"][C_aux["index"]==3][1:]/C_OH["value"][C_OH["index"]==3][1:], "mo", label="Aux/(O+H)")
axs[-1].set_xticks(X_12[1:])
axs[-1].set_xticklabels(C_O["PS"][C_O["index"]==3][1:],rotation=45, ha='right')
axs[-1].set_xlabel("PS & Date & time")
for ax in axs[:-1]:
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
ylims=np.array([])
for ax in axs:
    ax.grid()
    ax.legend(ncol=len(ax.get_legend_handles_labels()[1]))
    ylims=np.append(ylims, ax.get_ylim())

for ax in axs[:-1]:
    lim_avg=np.average(ax.get_ylim())
    yrange=np.amax(ylims[1::2]-ylims[::2])
    ax.set_ylim([lim_avg-yrange/2,lim_avg+yrange/2])

C_23_O=C_O["value"][C_O["index"]==1]
C_13_O=(C_O["value"][C_O["index"]==2][::2]+C_O["value"][C_O["index"]==2][1::2])
C_12_O=C_O["value"][C_O["index"]==1]

C_12_13_O=C_12_O/C_13_O


# print(C_O["value"][-1],np.average(C13["value"][-2:]),C12["value"][-1])

plt.show()