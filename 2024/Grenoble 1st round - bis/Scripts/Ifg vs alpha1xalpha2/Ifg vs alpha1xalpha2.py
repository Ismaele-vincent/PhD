# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 18:41:54 2023

@author: S18
"""

"""
inf_file_names:
"ifg_vs_alpha2_19pt_28Mar1138", 
"ifg_vs_alpha2_19pt_28Mar1346", 
"ifg_vs_alpha2_19pt_risingtemp_28Mar2200_no_rock", 
"ifg_vs_alpha2_19pt_stabletemp_28Mar1834", 
"ifg_vs_alpha2_19pt_stabletemp_29Mar0607", 
"ifg_vs_alpha2_19pt_stabletemp_29Mar0839", 
"""

import os
import numpy as np
from scipy.special import jv
import shutil
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq, fft, fftfreq, dct, dst
from mpl_toolkits import mplot3d
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from PIL import Image as im
from scipy.optimize import curve_fit as fit
mu_N=-9.6623651#*1e-27 J/T
hbar= 6.62607015/(2*np.pi) #*1e-34 J s
f_1=20
c_1=10
B_0=18.55
T=24.5881
v0=2060.43 #m/s
phi_1=0
order=4
w_ps=0
rad=np.pi/180
chi=0
chi_0=0
C=0


def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def j0j0(x, a_1, a_2, b):
    alpha1=a_1*x
    alpha2=a_2*x
    return b*abs(jv(0,alpha1)*jv(0,alpha2))#+b*(jv(3,alpha1)*jv(2,alpha2)-jv(3,alpha1)*jv(2,alpha2)))

def j3j2(x, a_1, a_2, b):
    alpha1=a_1*x
    alpha2=a_2*x
    return b*abs(jv(3,alpha1)*jv(2,alpha2))#+b*(jv(3,alpha1)*jv(2,alpha2)-jv(3,alpha1)*jv(2,alpha2)))

def j6j4(x, a_1, a_2, b):
    alpha1=a_1*x
    alpha2=a_2*x
    return b*abs(jv(6,alpha1)*jv(4,alpha2))#+b*(jv(3,alpha1)*jv(2,alpha2)-jv(3,alpha1)*jv(2,alpha2)))

def contr(x, a_1, a_2, A, B):
    alpha1=a_1*x
    alpha2=a_2*x
    return ((A*jv(0,alpha1)*jv(0,alpha2))**2+(B*jv(3,alpha1)*jv(2,alpha2))**2)**0.5#A*jv(0,alpha1)*jv(0,alpha2)+B*jv(3,alpha1)*jv(2,alpha2)#

inf_file_name="ifg_vs_alpha1xalpha2_14pt_risingtemp_no_rock_01Apr1912"
print(inf_file_name)
sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round - bis/exp_CRG-3126/Sorted data/Ifg vs alpha1xalpha2/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"
i=0
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    for name in files[:-1]:
        if i==0:
            tot_data=np.loadtxt(os.path.join(root, name))[:,:]
            ps_pos=tot_data[:,0]
            print(name)
            i+=1
        else:
            data=np.loadtxt(os.path.join(root, name))[:,:]
            tot_data = np.vstack((tot_data, data))
               
amplitude=tot_data[::len(ps_pos),-1]
# print(amplitude)
# print(tot_data)
current=amplitude


matrix=np.zeros((len(amplitude),len(ps_pos)))
matrix_err=np.zeros((len(amplitude),len(ps_pos)))
for i in range(len(amplitude)):
    matrix[i]=tot_data[:,2][tot_data[:,-1]==amplitude[i]]+tot_data[:,4][tot_data[:,-1]==amplitude[i]]
    matrix_err[i]=matrix[i]**0.5

ps_plt=np.linspace(ps_pos[0], ps_pos[-1], 500)
chi_0=np.zeros(len(amplitude))
chi_0_err=np.zeros(len(amplitude))
C=np.zeros(len(amplitude))
C_err=np.zeros(len(amplitude))

for i in range(len(amplitude)):
    ps_data=matrix[i]
    P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, -3.5]
    B0=([0,0,2.5,-10],[np.amax(ps_data)+100,np.amax(ps_data)+100,3.5, 10])
    p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0, sigma=matrix_err[i])
    err=np.diag(cov)**0.5
    C[i] = p[1]/p[0]
    C_err[i] = ((1/p[0]*err[1])**2+(p[1]/p[0]**2*err[0])**2)**0.5
    w_ps=p[-2]
    chi_0[i]=p[-1]
    chi_0_err[i]=err[-1]
    # fig = plt.figure(figsize=(8,6))
    # ax = fig.add_subplot(111)
    # ax.errorbar(ps_pos, matrix[i], yerr= matrix_err[i], fmt="ko")
    # ax.plot(ps_plt, fit_cos(ps_plt,*p))
    # ax.set_title(str("%.2f"%amplitude[i],))
    # print(C[i], w_ps, chi_0[i])
# C[6]=0
curr_plt=np.linspace(current[0], current[-1], 10000)
ampl_plt=np.linspace(0, amplitude[-1], 1000)
p,cov=fit(contr, current, C, p0=[0.45,1.1,1,1], bounds=([0,0,0,0],[5,5,5,5]))

err=np.diag(cov)**0.5
print(p, np.diag(cov)**0.5)
print(curr_plt[contr(curr_plt,*p)==np.amin(contr(curr_plt,*p))])
alpha_plt=p[-1]*curr_plt#alpha(T, f_1, p[-1]*curr_plt)

print("alpha/V_c=",p[1],"+-",err[1])
print("alpha=",p[1]*8.36,"+-", err[1]*2.01)
print("pi/16\t V_c=",np.pi/16/p[1],"+-", err[1]*(np.pi/16/p[1])**2)
print("pi/8\t V_c=",np.pi/8/p[1],"+-", err[1]*(np.pi/8/p[1])**2)
print("pi/4\t V_c=",np.pi/4/p[1],"+-", err[1]*(np.pi/4/p[1])**2)
# print("2.4048\t V_c=",2.4048/p[1],"+-", err[1]*(2.4048/p[1])**2)
fig = plt.figure(figsize=(5,5))
title=fig.suptitle(inf_file_name)
ax = fig.add_subplot(111)
# ax.errorbar(amplitude, chi_0, yerr= chi_0_err, fmt="ko")
ax.errorbar(current, C, yerr= C_err, fmt="k.")
ax.plot(curr_plt, contr(curr_plt,*p))
ax.plot(curr_plt, j0j0(curr_plt,*p[:3]))
ax.plot(curr_plt, j3j2(curr_plt,*p[:3]))
# ax.plot(curr_plt, j6j4(curr_plt,*p[:3]))

ax.set_xlabel("$V_p$ [V]")
ax.vlines(2.4048/p[1], 0, 0.5, color="k", ls="dashed")
# ax.text(curr_0, 0.5, "$\\alpha\\approx$"+str("%.4f" %(alpha_0,)) ,va="bottom", ha="center")
# ax.set_ylim([0,1])
# plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Report/Images/C_bessel_B_3kHz.pdf", format="pdf",bbox_inches="tight")
plt.show()