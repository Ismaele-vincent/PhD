# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 18:41:54 2023

@author: S18
"""

"""
inf_file_names:
"TOF_vs_chi_S2_ifg_29Aug1924",
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
T=24.588
v0=2060.43 #m/s
phi_1=0
order=4
w_ps=0
rad=np.pi/180
chi=0
chi_0=0
C=0

def j0_fit(x, a, b):
    w=f_1*2*np.pi
    a_1=mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2)
    return abs(a*jv(0,a_1*b*x))

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

def B(T,f,alpha):
    w=f*2*np.pi
    return alpha/(mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2))

def fit_O_beam(t, A, B, a_1, xi_1):
    # a_1=alpha(T,f_1,c_1)
    # xi_1=phi_1+(2*np.pi*f_1*1e-3*T+np.pi)/2#-2*np.pi*f_1*1e3/v0
    chi_fit=chi
    return A + B*np.cos(chi_fit-a_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1))/2



inf_file_names=[
"TOF_vs_chi_A_22pt_pi16_1200s_07Nov1808",
"TOF_vs_chi_A_22pt_pi8_1200s_06Nov1855",
"TOF_vs_chi_A_22pt_pi4_1200s_08Nov0132",
"TOF_vs_chi_A_22pt_pi2_1200s_12Nov0455",
"TOF_vs_chi_A_22pt_pi_1200s_12Nov1232"
]
J_0=np.zeros((len(inf_file_names)))
J_1=np.zeros((len(inf_file_names)))
J_2=np.zeros((len(inf_file_names)))
J_3=np.zeros((len(inf_file_names)))
ampl=np.zeros((len(inf_file_names)))
j=0

for inf_file_name in inf_file_names:
    sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/TOF A/"+inf_file_name
    cleandata=sorted_fold_path+"/Cleantxt"
    # niels_path="/home/aaa/Desktop/Niels/Data/"+inf_file_name
    # niels_fourier_path="/home/aaa/Desktop/Niels/Fourier/"+inf_file_name

    # if not os.path.exists(niels_path):
    #     os.makedirs(niels_path)
    # if not os.path.exists(niels_fourier_path):
    #     os.makedirs(niels_fourier_path)

    i=0
    for root, dirs, files in os.walk(cleandata, topdown=False):
        files=np.sort(files)
        # print(files)
        for name in files:
            # print(name)
            if i==0:
                tot_data=np.loadtxt(os.path.join(root, name))[:,:]
                time=tot_data[:,1]
                f_1=tot_data[0,-3]*1e-3#
                amp_1=tot_data[0,-4]
                # print("f=", f_1)
                # print("amp=", amp_1)
                i=1
            else:
                data=np.loadtxt(os.path.join(root, name))[:,:]
                tot_data = np.vstack((tot_data, data))
    ps_pos=tot_data[::len(time),-1]
    N = len(time)
    S_F=50
    matrix=np.zeros((len(ps_pos),len(time)))
    matrix_err=np.zeros((len(ps_pos),len(time)))
    for i in range(len(ps_pos)):
        matrix[i]=tot_data[:,5][tot_data[:,-1]==ps_pos[i]]
        matrix_err[i]=matrix[i]**0.5
        
    ps_data=np.sum(matrix, axis=1)
    P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, -3]
    B0=([1000,0,0.01,-10],[np.amax(ps_data)+1000,np.amax(ps_data)+1000,5, 10])
    p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
    err=np.diag(cov)**0.5
    Co= p[1]/p[0]
    w_ps=p[-2]
    chi_0=p[-1]
    chi_0_err=err[-1]
    if j==0:
        print(p)
        print("C=", Co)
        print("bg=", p[0]-p[1])
        print("amp=", 2*p[1])
    # fig = plt.figure(figsize=(8,6))
    # ax = fig.add_subplot(111)
    # ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
    # ax.errorbar(ps_pos,ps_data, yerr=ps_data**0.5,fmt="ko",capsize=5, ms=3)
    # ax.plot(ps_plt,fit_cos(ps_plt, *p), "b")
    # ax.vlines(p[-1]/p[-2],fit_cos(p[-1]/p[-2]+np.pi,*p),fit_cos(p[-1]/p[-2],*p), color="k")
    P0=[300,300, -0.8, 1]
    chi=ps_pos*w_ps-chi_0
    chi_plt=np.linspace(chi[0], chi[-1], 100)
    
    J_0_chi=np.zeros((len(ps_pos)))
    J_1_chi=np.zeros((len(ps_pos)))
    J_2_chi=np.zeros((len(ps_pos)))
    J_3_chi=np.zeros((len(ps_pos)))
    # c_0_data=np.zeros((len(amplitude)),dtype=complex)
    # c_1_data=np.zeros((len(amplitude)),dtype=complex)
    # c_2_data=np.zeros((len(amplitude)),dtype=complex)
    # c_3_data=np.zeros((len(amplitude)),dtype=complex)
    # c_0_data_err=np.zeros((len(amplitude)),dtype=complex)
    # c_1_data_err=np.zeros((len(amplitude)),dtype=complex)
    # c_2_data_err=np.zeros((len(amplitude)),dtype=complex)
    # c_3_data_err=np.zeros((len(amplitude)),dtype=complex)
    for i in range(len(ps_pos)):
        func_data=(matrix[i])/22045.410531465674
        # print(len(func_data))
        func_data_err=matrix_err[i]
        yf_data = fft(func_data)
        yf_data_err = np.ones(len(yf_data))*np.sum(matrix_err)**0.5
        # print(sum(abs(yf_data)))
        xf = fftfreq(N, S_F)*1e3
        # fig = plt.figure(figsize=(8,6))
        # ax = fig.add_subplot(111)
        # ax.errorbar(time, matrix[i], yerr= matrix_err[i], fmt="ko")
        # ax.set_title(str("%.2f"%chi[i],))
        x_1=f_1#xf[xf>0][abs(yf_data[xf>0])==np.amax(abs(yf_data[xf>0]))]
        c_0_data=abs(yf_data[abs(xf)<1/S_F/2]).astype(complex)
        c_1_data=(yf_data[abs(xf-x_1)<1/S_F/2]).astype(complex)
        c_2_data=(yf_data[abs(xf-2*x_1)<1/S_F/2]).astype(complex)
        c_3_data=(yf_data[abs(xf-3*x_1)<1/S_F/2]).astype(complex)
        var=np.sum(func_data)**0.5
        c_0_data_err=var
        c_1_data_err=var
        c_2_data_err=var
        c_3_data_err=var
        J_0_chi[i]=abs(2*(c_0_data)-1)/abs(np.cos(chi[i]))
        J_1_chi[i]=abs(2*(c_1_data)/abs(np.sin(chi[i])))
        J_2_chi[i]=abs(2*(c_2_data)/abs(np.cos(chi[i])))
        J_3_chi[i]=abs(2*(c_3_data)/abs(np.cos(chi[i])))
        c_0_err_rel=c_0_data_err/abs(c_0_data)
        c_1_err_rel=c_1_data_err/abs(c_1_data)
        c_2_err_rel=c_2_data_err/abs(c_2_data)
        c_3_err_rel=c_3_data_err/abs(c_3_data)
    fig = plt.figure(figsize=(10,6))
    # ax = fig.add_subplot(111)
    # ax.errorbar(chi, abs(J_0_chi), yerr= abs(J_0_chi)*c_0_err_rel,fmt="g.")
    # ax.errorbar(chi, abs(J_1_chi), yerr= abs(J_1_chi)*c_1_err_rel,fmt="k.")
    # ax.errorbar(chi, abs(J_2_chi),yerr= abs(J_2_chi)*c_2_err_rel, fmt="r.")
    # ax.errorbar(chi, abs(J_3_chi),yerr= abs(J_3_chi)*c_3_err_rel, fmt="b.")
    J_0[j]=J_0_chi[8]
    J_1[j]=J_1_chi[8]
    J_2[j]=J_2_chi[8]
    J_3[j]=J_3_chi[8]
    # ampl[j]=amp_1
    j+=1
print(ampl)
ampl=np.array([0.16991, 0.33982, 0.67964, 1.35928, 2.68])
P0=[10,5]
p0,cov0=fit(j0_fit,ampl, abs(J_0), p0=P0, bounds=([0,0],[1000,1000]))
p1,cov1=fit(j1_fit,ampl, abs(J_1), p0=P0, bounds=([0,0],[1000,1000]))
p2,cov2=fit(j2_fit,ampl, abs(J_2), p0=P0, bounds=([0,0],[1000,1000]))
p3,cov3=fit(j3_fit,ampl, abs(J_3), p0=P0, bounds=([0,0],[1000,1000]))
print(p0, p1,p2,p3)
print(np.diag(cov1)**0.5,np.diag(cov2)**0.5,np.diag(cov3)**0.5)
fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111)
# ax.plot(current, abs(J_0), "g.")
# alpha_plt=-alpha(T,f_1, p1[-1]*ampl)

ax.errorbar(ampl, abs(J_0), yerr= 0*abs(J_0)*c_0_err_rel,fmt="g.")
ax.errorbar(ampl, abs(J_1), yerr= 0*abs(J_1)*c_1_err_rel,fmt="k.")
ax.errorbar(ampl, abs(J_2),yerr= 0*abs(J_2)*c_2_err_rel, fmt="r.")
ax.errorbar(ampl, abs(J_3),yerr= 0*abs(J_3)*c_3_err_rel, fmt="b.")
c_plt= np.linspace(0,ampl[-1],150)

alpha_plt1=-alpha(T,f_1, p1[-1]*c_plt)
ax.plot(c_plt, j0_fit(c_plt, *p0), "g-")
ax.plot(c_plt, j1_fit(c_plt, *p1), "k-")
ax.plot(c_plt,  j2_fit(c_plt,*p2), "r-")
ax.plot(c_plt,  j3_fit(c_plt, *p3), "b-")
# ax.vlines(1.627615983862702, 0, j2_fit(1.6,*p2) )


plt.show()








