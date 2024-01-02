#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 15:54:09 2023

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

mu_N=-9.6623651#*1e-27 J/T
hbar= 6.62607015/(2*np.pi) #*1e-34 J s
f_1=10
B_1=10
B_0=18.55
T=10
v0=2060.43 #m/s
phi_1=0
order=4
w_ps=3.174960654269423
w_ps_err=0.024073832955880906
rad=np.pi/180
chi=0
chi_0=0.7
Co= 0.73
Co_err=0.022491135210979854
a_21=1
a_1=1/2**0.5
a_2=1/2**0.5

# inf_file_name="TOF_vs_chi_A_19pt_pi4_1200s_03Nov2326"
# inf_file_name="TOF_vs_chi_A_22pt_pi2_SD_1200s_13Nov0438"
inf_file_name="TOF_vs_chi_A_22pt_pi2_1200s_12Nov0455"
# inf_file_name="TOF_vs_chi_A_22pt_pi4_SD_1200s_12Nov2101"
# inf_file_name="TOF_vs_chi_A_22pt_pi4_1200s_08Nov0132"
# inf_file_name="TOF_vs_chi_B_22pt_pi4_1200s_08Nov0856"
# inf_file_name="TOF_vs_chi_A_22pt_pi_1200s_12Nov1232"
# In2, pi/8
# spin up, pi/4
# Un, pi/4
# Un, pi/8

alpha_1= -1.5#0.19181329#np.pi/16 #/2.354
alpha_1_err=0.1*alpha_1
def w1(chi):
    return (1/(1+a_21*np.exp(1j*chi)))

def fit_cos_unb(x, A, B, C):
    return A*((1 - Co)/2 + Co*(1/2+a_1*a_2*np.cos(B*x-C)))

def fit_cos(x, A, B, C, D):
    return A/2+jv(0,alpha_1)*B/2*np.cos(C*x-D)

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

def fit_O_beam(t, A, B, chi, a_1, xi_1):
    # a_1=alpha(T,f_1,B_1)
    # xi_1=phi_1+(2*np.pi*f_1*1e-3*T+np.pi)/2#-2*np.pi*f_1*1e3/v0
    chi_fit=chi
    return A + B*np.cos(chi_fit-a_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1))/2
chi_aus=0

# def fit_Im(t, A, B, Im, xi_1):
#     return A*((1-Co)/2+Co*np.cos(chi_aus/2)**2*(1+2*Im*alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)))
A_aus=1556.6205404620448#1493.880147983857
# def fit_Im(t, A, B, Im, xi_1):
#     return A_aus*((1-Co)/2+Co*B*(1+2*Im*alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)))

def fit_w(t, B, Re, xi_1):
    # return A_aus*((1-Co)/2+Co*B*(1+alpha_1**2*(w1(chi_aus).imag**2+Re**2 - Re)*np.sin(2*np.pi*1e-3*f_1*t+xi_1)**2+2*w1(chi_aus).imag*alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)))
    # return A_aus*((1-Co)/2+Co*B*(1+2*(Im**2+Re**2 - Re)*(1-np.cos(alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)))+2*Im*np.sin(alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1))))
    return A_aus*((1-Co)/2+Co*B*(1+2*(w1(chi_aus).imag**2+Re**2 - Re)*(1-np.cos(alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)))+2*w1(chi_aus).imag*np.sin(alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1))))


print(inf_file_name)
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
    for name in files[:-1]:
        # print(name)
        if i==0:
            tot_data=np.loadtxt(os.path.join(root, name))[:,:]
            time=tot_data[:,1]
            f_1=tot_data[0,-3]*1e-3
            Vpp=tot_data[0,-4]
            print("Vpp=",Vpp)
            print("f=", f_1)
            i=1
        else:
            data=np.loadtxt(os.path.join(root, name))[:,:]
            tot_data = np.vstack((tot_data, data))
ps_pos=tot_data[::len(time),-1]
time_plt=np.linspace(time[0],time[-1],200)
N = len(time)
S_F=50
matrix=np.zeros((len(ps_pos),len(time)))
matrix_err=np.zeros((len(ps_pos),len(time)))
for i in range(len(ps_pos)):
    matrix[i]=tot_data[:,5][tot_data[:,-1]==ps_pos[i]]
    matrix_err[i]=matrix[i]**0.5
    
ps_data=np.average(matrix, axis=1)
P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, -0.1]
B0=([10,0,0.01,-10],[np.amax(ps_data)+1000,np.amax(ps_data)+1000,5, 10])
p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
err=np.diag(cov)**0.5
Co= p[1]/p[0]
w_ps=p[-2]
chi_0=p[-1]
chi_0_err=err[-1]
A_aus=p[0]
print("A=", p[0])
print("C=",Co)
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
Re_data=np.zeros((len(ps_pos)))
Re_data_err=np.zeros((len(ps_pos)))
Im_data=np.zeros((len(ps_pos)))
Im_data_fit=np.zeros((len(ps_pos)))
Im_data_fit_err=np.zeros((len(ps_pos)))
Re_data_fit=np.zeros((len(ps_pos)))
Re_data_fit_err=np.zeros((len(ps_pos)))
Im_data_err=np.zeros((len(ps_pos)))
Im_err_rel=np.zeros((len(ps_pos)))
rho=np.zeros((len(ps_pos)))
chi=ps_pos*w_ps-chi_0
chi_plt=np.linspace(chi[0], chi[-1], 100)
cos2=np.zeros((len(ps_pos)))
cos2_err=np.zeros((len(ps_pos)))
cos2_fit=np.zeros((len(ps_pos)))
cos2_fit_err=np.zeros((len(ps_pos)))
xi=-0.7
for i in range(len(ps_pos)):
    func_data=matrix[i]
    # print(len(func_data))
    func_data_err=matrix_err[i]
    chi_aus=chi[i]
    P0=[np.cos(chi[i]/2)**2, 0.5, xi]
    # print(P0)
    B0=([0, 0, -1],[np.inf, 1, 1])
    try:
        p_Im,cov_Im = fit(fit_w, time, func_data, p0=P0, bounds=B0)
        xi=p_Im[-1]
    except:
        p_Im=p_Im*0
        cov_Im*=0
    err_Im=np.diag(cov_Im)**0.5
    
    # print(i-len(ps_pos))
    # print(p_Im[0])
    # print(p_Im,err_Im)
    # Im_data_fit[i]=p_Im[1]
    # Im_data_fit_err[i]=err_Im[1]
    Re_data_fit[i]=p_Im[1]
    Re_data_fit_err[i]=err_Im[1]
    cos2_fit[i]=p_Im[0]#*Co#+p_Im[0]*(1-Co)/2
    cos2_fit_err[i]=err_Im[0]
    
    yf_data = fft(func_data)
    yf_data_err = np.ones(len(yf_data))*np.sum(matrix_err)**0.5
    # print(sum(abs(yf_data)))
    xf = fftfreq(N, S_F)*1e3
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    ax.errorbar(time, matrix[i], yerr= matrix_err[i], fmt="k.", capsize=3)
    ax.plot(time_plt, fit_w(time_plt, *p_Im))
    # ax.set_title(str("%.2f"%chi[i],))
    # ax.errorbar(xf, np.abs(yf_data), np.abs(yf_data_err), fmt="k.", capsize=5)
    # ax.set_xlim([-5,5])
    
    if i==0:
        x_1=f_1#xf[xf>0][abs(yf_data[xf>0])==np.amax(abs(yf_data[xf>0]))]
        # print(x_1)
    c_1_data=(yf_data[abs(xf-x_1)<1/S_F/2]).astype(complex)
    c_0_data=abs(yf_data[abs(xf)<1/S_F/2]).astype(complex)#-3607.1413237746724#-3597.8672630959286
    var=np.sum(func_data)**0.5/2
    c_1_data_err=var
    c_0_data_err=(var**2+14)**0.5
    
    # print(chi[i], np.angle(c_1_data))
    if (c_1_data).real>0:
        # print(np.angle(c_1_data))
        e_m1xi=np.exp(-1j*(np.angle(c_1_data)))
    else:
        e_m1xi=np.exp(-1j*(np.angle(c_1_data)+np.pi))
    e_m2xi=e_m1xi**2
    
    cos2[i]=abs(c_0_data)
    cos2_err[i]=abs(c_0_data_err)
    
    Im_data[i]=(c_1_data*e_m1xi).real/(cos2[i])/alpha_1
    Im_data_err[i]=(abs(c_1_data_err/cos2[i])**2 + (abs((c_1_data*e_m1xi)/cos2[i]**2)*cos2_err[i])**2+abs((c_1_data*e_m1xi)/cos2[i]/alpha_1*alpha_1_err)**2)**0.5/abs(alpha_1)
    Im_err_rel[i]=abs(Im_data_err[i]/Im_data[i])
    # data_txt=np.array([time, func_data,func_data_err ]) 
    # with open(niels_path+"/"+str("%i" %(i),) +".txt", 'w') as f:
    #         np.savetxt(f, np.transpose(data_txt), header= "time(microsec) data err")
    # data_fourier_txt=np.array([xf, np.abs(yf_data)]) 
    # with open(niels_fourier_path+"/"+str("%i" %(i),) +".txt", 'w') as f:
            # np.savetxt(f, np.transpose(data_fourier_txt), header= "freq abs(c)")
B0=([0,1,-10],[100000,4,10])
p_cos_unb,cov_unb=fit(fit_cos_unb, ps_pos, cos2, p0=[10000,3,-0.5], bounds=B0)
# chi=ps_pos*p_cos_unb[-2]-p_cos_unb[-1]-np.pi
chi_plt=np.linspace(chi[0], chi[-1], 1000)
fig = plt.figure(figsize=(6,6), dpi=200)
ax = fig.add_subplot(111)
ax.set_title(inf_file_name)
ax.plot(chi_plt, w1(chi_plt).imag,"b--", alpha=0.5, label="Theory")
ax.plot(chi_plt, w1(chi_plt).real,"r--", alpha=0.5, label="Theory")
# ax.errorbar(chi, Im_data, Im_data_err, fmt="r.", capsize=5, label="Data Fourier Transform")
ax.errorbar(chi, Im_data_fit, Im_data_fit_err, fmt="b.", capsize=5, label="Data Fit")
ax.errorbar(chi, Re_data_fit, Re_data_fit_err, fmt="r.", capsize=5, label="Data Fit")

# ax.plot(chi_plt+np.pi, w2(chi_plt+np.pi).real,"r-")
# ax.errorbar(chi+np.pi, Re_chi_pi,yerr=Re_err, capsize=3,fmt="r.")
if a_21==1:
    ax.set_ylim([-3,3])  

# plt.savefig("/home/aaa/Desktop/Fig fit.pdf", format="pdf")
fig = plt.figure(figsize=(6,6), dpi=200)
ax = fig.add_subplot(111)
ax.errorbar(ps_pos, cos2, yerr=cos2_err, fmt="ko", capsize=5, label="$c_0$")
ax.plot(ps_plt, fit_cos_unb(ps_plt,*p_cos_unb), "b-", label="Fit")
ax.errorbar(ps_pos, ps_data*len(time), yerr=cos2_fit_err, fmt="g.", capsize=5, label="$c_0$")
ax.legend()
# print(cos2/cos2_fit)
print("param cos_unb=",p_cos_unb)
corr_unb=p_cos_unb[0]
corr_err=(np.diag(cov_unb)**0.5)
print("correction_unb="+str(p_cos_unb[0]*(1-Co)/2)+" +- "+str(0.5*((abs(1-Co)*corr_err[0])**2+(abs(p_cos_unb[0])*Co_err)**2)**0.5))

