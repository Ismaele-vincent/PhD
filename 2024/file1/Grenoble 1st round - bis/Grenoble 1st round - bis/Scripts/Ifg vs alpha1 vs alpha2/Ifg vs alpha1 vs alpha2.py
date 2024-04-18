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

def j0_fit(x, a, b, c, d, e):
    w=f_1*2*np.pi
    a_1=mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2)
    return c +d*(1-e*x**2)*abs(a*jv(0,a_1*b*x))

def j1_fit(x, a, b):
    w=f_1*2*np.pi
    a_1=mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2)
    return abs(a*jv(1,a_1*b*x))

def j2_fit(x, a, b):
    w=f_1*2*np.pi
    a_1=mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2)
    return abs(a*jv(2,a_1*b*x))

def j3_fit(x, a, b):
    w=f_1*2*np.pi
    a_1=mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2)
    return abs(a*jv(3,a_1*b*x))

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

def contr(x, A, a_1, b, c):
    B=a_1*x+c
    return b+A*abs(jv(0,B))
    # return A*(1/(1+c*x**2))*abs(jv(0,B))

def B(T,f,alpha):
    w=f*2*np.pi
    return alpha/(mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2))



def fit_O_beam(t, A, B, a_1, xi_1):
    # a_1=alpha(T,f_1,c_1)
    # xi_1=phi_1+(2*np.pi*f_1*1e-3*T+np.pi)/2#-2*np.pi*f_1*1e3/v0
    chi_fit=chi
    return A + B*np.cos(chi_fit-a_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1))/2
inf_file_name="ifg_vs_alpha1+alpha2_20pt_risingtemp_31Mar0114"#"ifg_vs_alpha2_19pt_risingtemp_28Mar2200_no_rock"
print(inf_file_name)
sorted_fold_path="C:/Users/S18/Desktop/Grenoble-2024 Ismaele/2024/Grenoble 1st round - bis/exp_CRG-3126/Sorted data/Ifg vs alpha1 vs alpha2/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"
i=0
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    for name in files[:]:
        if i==0:
            tot_data=np.loadtxt(os.path.join(root, name))[:,:]
            ps_pos=tot_data[:,0]
            print(name)
            i+=1
        else:
            data=np.loadtxt(os.path.join(root, name))[:,:]
            tot_data = np.vstack((tot_data, data))
# tot_data=np.sort(tot_data,axis=-2)
amplitude1=np.array([2,4,6,8])#tot_data[::len(ps_pos)*10,-2]
# tot_data=np.sort(tot_data, axis=-1)
amplitude2=np.array([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])#tot_data[::len(ps_pos)*4,-1]
print(amplitude1)
print(amplitude2)



matrix=np.zeros((len(amplitude1),len(amplitude2),len(ps_pos)))
matrix_err=np.zeros((len(amplitude1),len(amplitude2),len(ps_pos)))
for i in range(len(amplitude1)):
    matrix_aux=tot_data[tot_data[:,-2]==amplitude1[i]]
    print(matrix_aux)
    for j in range(len(amplitude2)):
        matrix[i,j,:]=matrix_aux[:,2][matrix_aux[:,-1]==amplitude2[j]]# and tot_data[:,-1]==amplitude2[i]]#+tot_data[:,4][tot_data[:,-2]==amplitude1[i]][tot_data[:,-1]==amplitude2[i]]
        matrix_err[i,j,:]=matrix[i,j,:]**0.5

ps_plt=np.linspace(ps_pos[0], ps_pos[-1], 500)
chi_0=np.zeros(len(amplitude1))
chi_0_err=np.zeros(len(amplitude1))
C=np.zeros((len(amplitude1),len(amplitude2)))
C_err=np.zeros((len(amplitude1),len(amplitude2)))

for i in range(len(amplitude1)):
    for j in range(len(amplitude2)):
        ps_data=matrix[i,j,:]
        ps_data_err=matrix_err[i,j,:]
        P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, -3]
        B0=([0,0,2.5,-10],[np.amax(ps_data)+100,np.amax(ps_data)+100,3.5, 10])
        p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0, sigma=ps_data_err)
        err=np.diag(cov)**0.5
        C[i,j] = p[1]/p[0]
        C_err[i,j] = ((1/p[0]*err[1])**2+(p[1]/p[0]**2*err[0])**2)**0.5
        w_ps=p[-2]
        chi_0[i]=p[-1]
        chi_0_err[i]=err[-1]
        # fig = plt.figure(figsize=(8,6))
        # ax = fig.add_subplot(111)
        # ax.errorbar(ps_pos, ps_data, yerr= ps_data_err, fmt="ko")
        # ax.plot(ps_plt, fit_cos(ps_plt,*p))
        # ax.set_title(str("%.2f"%amplitude1[i],))
        # print(C[i], w_ps, chi_0[i])
    # C[6]=0
    ampl_plt=np.linspace(0, amplitude2[-1], 1000)
    # p,cov=fit(contr, amplitude2, C[i], p0=[2500,1,0,-1.1*i])
    err=np.diag(cov)**0.5
    print(p, np.diag(cov)**0.5)
    print(ampl_plt[contr(ampl_plt,*p)==np.amin(contr(ampl_plt,*p))])
    alpha_plt=p[-1]*ampl_plt#alpha(T, f_1, p[-1]*ampl_plt)
    
    # print("alpha/V_c=",p[1],"+-",err[1])
    # print("alpha=",p[1]*8.36,"+-", err[1]*2.01)
    # print("pi/16\t V_c=",np.pi/16/p[1],"+-", err[1]*(np.pi/16/p[1])**2)
    # print("pi/8\t V_c=",np.pi/8/p[1],"+-", err[1]*(np.pi/8/p[1])**2)
    # print("pi/4\t V_c=",np.pi/4/p[1],"+-", err[1]*(np.pi/4/p[1])**2)
    # print("2.4048\t V_c=",2.4048/p[1],"+-", err[1]*(2.4048/p[1])**2)
    fig = plt.figure(figsize=(5,5))
    title=fig.suptitle(amplitude1[i])#*0.706
    ax = fig.add_subplot(111)
    # ax.errorbar(amplitude1, chi_0, yerr= chi_0_err, fmt="ko")
    ax.errorbar(amplitude2, C[i], yerr= C_err[i], fmt="k.") #*1.144
    # ax.errorbar(ampl_plt*1.144, contr(ampl_plt,*p))
    ax.set_xlabel("$V_p$ [V]")
    # ax.vlines(2.4048/p[1], 0, 0.5, color="k", ls="dashed")
    # ax.text(curr_0, 0.5, "$\\alpha\\approx$"+str("%.4f" %(alpha_0,)) ,va="bottom", ha="center")
    # ax.set_ylim([0,1])
    # plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Report/Images/C_bessel_B_3kHz.pdf", format="pdf",bbox_inches="tight")
    plt.show()