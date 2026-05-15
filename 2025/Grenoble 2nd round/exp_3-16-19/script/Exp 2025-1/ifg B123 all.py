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

C_12=0.69
C_13=0.74
C_23=0.62

points=32
points_per=16

dtype_new = np.dtype([
    ("name", "U50"),
    ("value", "f8"),
    ("index", "i8")
])


def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

bad_apples=["ifg_wv1_psi_+1+1+1_no_fit_B123_B1_23Oct2335.txt",
            "ifg_wv1_psi_+1+1+1_no_fit_B123_B2_23Oct2335.txt",
            "ifg_wv1_psi_+1+1+1_no_fit_B123_B3_23Oct2335.txt"
    ]
good_apples=[
    ]


def w1(chi_1, chi_2, chi_3):
    return a_1*np.exp(1j*(chi_1_0+chi_1))/(a_1*np.exp(1j*(chi_1_0+chi_1))+a_2*np.exp(1j*(chi_2_0+chi_2))+a_3*np.exp(1j*(chi_3_0+chi_3)))

def w2(chi_1, chi_2, chi_3):
    return a_2*np.exp(1j*(chi_2_0+chi_2))/(a_1*np.exp(1j*(chi_1_0+chi_1))+a_2*np.exp(1j*(chi_2_0+chi_2))+a_3*np.exp(1j*(chi_3_0+chi_3)))

def w3(chi_1, chi_2, chi_3):
    return a_3*np.exp(1j*(chi_3_0+chi_3))/(a_1*np.exp(1j*(chi_1_0+chi_1))+a_2*np.exp(1j*(chi_2_0+chi_2))+a_3*np.exp(1j*(chi_3_0+chi_3)))

sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Ifg wv B123/Cleantxt all"
chi_0=[0, np.pi/2, np.pi, 3*np.pi/2]

A_avg=0
Dchi=np.zeros(4)
C_avg=0
C_err=0

for root, dirs, files in os.walk(sorted_fold_path, topdown=False):
    files=np.sort(files)
    data_ifg_matrix=np.zeros((3,points))
    i=0
    C12=np.array([], dtype=dtype_new)
    C13=np.array([], dtype=dtype_new)
    C23=np.array([], dtype=dtype_new)
    
    for name in files[:]:
        if (name not in bad_apples):
            # print(name)
            tot_data=np.loadtxt(os.path.join(root, name))[:,1:]
            time_ifg=tot_data[0,1]
            data_ifg=tot_data[:,2]
            # data_ifg_matrix[i]=data_ifg
            data_ifg_err=data_ifg**0.5
            ps_pos=tot_data[:,0]
            P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 6, -6.6]
            B0=([np.amin(data_ifg),0,5,-4*np.pi],[np.amax(data_ifg)*2,np.amax(data_ifg)*2,7, 1*np.pi])
            p,cov=fit(fit_cos, ps_pos, data_ifg, sigma=data_ifg_err, p0=P0,  bounds=B0)
            # print(p)
            # P0_unb=[100000, 3, -0.5, 0.7]
            # B0_unb=([0,1,-10, 0],[1e10,4,10,1])
            # p_unb,cov_unb=fit(fit_cos_unb, ps_pos, data_ifg, p0=P0_unb,  bounds=B0_unb)
            err=np.diag(cov)**0.5
            A=p[0]
            C=p[1]/p[0]
            C_err=p[1]**2/p[0]**4*err[0]**2+err[1]**2/p[0]**2
            A_err=err[0]**2
            x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
            fig = plt.figure(figsize=(8,6))
            ax = fig.add_subplot(111)
            fig.suptitle(name[:-4])
            ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
            ax.plot(x_plt,fit_cos(x_plt, *p), "b", label="%.2f"%C,)
            # ax.legend()
            # ax.set_ylim([0,1500])
            # print("C=", p[1]/p[0], "+-", ((err[1]/p[0])**2+(err[1]*p[1]/p[0]**2)**2)**0.5)
            # print("C_unb=", p_unb[-1])
            # print(p_unb)
            # print("w_ps=", p[-2], "+-", err[-2])
            # print("chi_0=", p[-1])
            Dchi[i]=p[3]
            # print(p[3])
            # if i==0:
            #     chi=ps_pos*p[2]-p[3]
            # i+=1
            if ("B123_B1" in name) and ("wv1" not in name):
                if ("wv2" in name):
                    C23=np.append(C23, np.array([(name[-13:-4],C,2)], dtype=dtype_new))
                if ("wv3" in name):
                    C23=np.append(C23, np.array([(name[-13:-4],C,3)], dtype=dtype_new))                
                # fig = plt.figure(figsize=(8,6))
                # ax = fig.add_subplot(111)
                # fig.suptitle(name[:-4])
                # ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                # ax.plot(x_plt,fit_cos(x_plt, *p), "b", label="%.2f"%C,)
                # ax.legend()
            if ("B123_B2" in name) and ("wv2" not in name):
                if ("wv1" in name):
                    C13=np.append(C13, np.array([(name[-13:-4],C,1)], dtype=dtype_new))
                if ("wv3" in name):
                    C13=np.append(C13, np.array([(name[-13:-4],C,3)], dtype=dtype_new))
            if ("B123_B3" in name) and ("wv3" not in name):
                if ("wv1" in name):
                    C12=np.append(C12, np.array([(name[-13:-4],C,1)], dtype=dtype_new))
                if ("wv2" in name):
                    C12=np.append(C12, np.array([(name[-13:-4],C,2)], dtype=dtype_new))
                # fig = plt.figure(figsize=(8,6))
                # ax = fig.add_subplot(111)
                # fig.suptitle(name[:-4])
                # ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                # ax.plot(x_plt,fit_cos(x_plt, *p), "b", label="%.2f"%C,)
                # ax.legend()
    
# print(C23_PS12)
C23 = C23[np.argsort(np.array([datetime.strptime(x, "%d%b%H%M") for x in C23["name"]]))]
C13 = C13[np.argsort(np.array([datetime.strptime(x, "%d%b%H%M") for x in C13["name"]]))]
C12 = C12[np.argsort(np.array([datetime.strptime(x, "%d%b%H%M") for x in C12["name"]]))]

X_23=np.arange(len(C23["value"]))

# print(C23["value"]==C23_PS12["value"])
fig = plt.figure(figsize=(5,5))
fig.suptitle("Loop paths  2+3")#, y=1.01)
ax1 = fig.add_subplot()
ax1.plot(X_23[C23["index"]==3], C23["value"][C23["index"]==3], "bo", label="PS 1")
ax1.plot(X_23[C23["index"]==2], C23["value"][C23["index"]==2], "ro", label="PS 1+2")
ax1.set_xticks(X_23)
ax1.set_xticklabels(C23["name"],rotation=45, ha='right')
ax1.set_xlabel("Date & time")
ax1.grid()
# ax1.xlabel(rotation=45, ha='right')
# ax2 = ax1.twiny() 
# ax1.plot(X_23, C23["value"], "w")
# ax2.plot(X_23[C23["index"]==3], C23_PS1["value"], "bo", label="PS 1")
# ax2.set_xticks(X_23[C23["index"]==3])
# ax2.set_xticklabels(C23_PS1["name"])
# ax2.set_xlabel("Phase shfter 1")
ax1.legend()

X_13=np.arange(len(C13["value"]))

fig = plt.figure(figsize=(5,5))
fig.suptitle("Loop paths  1+3")
ax1 = fig.add_subplot()
ax1.plot(X_13[C13["index"]==1], C13["value"][C13["index"]==1], "bo", label="PS 2")
ax1.plot(X_13[C13["index"]==3], C13["value"][C13["index"]==3], "ro", label="PS 1")
ax1.set_xticks(X_13)
ax1.set_xticklabels(C13["name"],rotation=45, ha='right')
ax1.set_xlabel("Date & time")
ax1.grid()
ax1.legend()

X_12=np.arange(len(C12["value"]))

fig = plt.figure(figsize=(5,5))
fig.suptitle("Loop paths  1+2")
ax1 = fig.add_subplot()
ax1.plot(X_12[C12["index"]==1], C12["value"][C12["index"]==1], "bo", label="PS 2")
ax1.plot(X_12[C12["index"]==2], C12["value"][C12["index"]==2], "ro", label="PS 1+2")
ax1.set_xticks(X_12)
ax1.set_xticklabels(C12["name"],rotation=45, ha='right')
ax1.set_xlabel("Date & time")
ax1.grid()
ax1.legend()

plt.show()