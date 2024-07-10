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
a_1= 0.496
a_1_err= 0.003
a_2= 0.868
a_2_err= 0.002
a_21=a_2/a_1
inf_file_name="TOF_vs_chi_A+B_In1_22pt_pi16_2000s_4P_16Nov1733"
# inf_file_name="TOF_vs_chi_A+B_In1_22pt_pi16_1200s_4P_15Nov0927"

alpha_1=0.1923 #/2.354
alpha_1_err=0.0009 
alpha_2=-0.1971 #/2.354
alpha_2_err=0.0004

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
def fit_Im(t, B, Im_1, Im_2, xi_1, xi_2):
    return B*(1-2*Im_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)-2*Im_2*np.sin(2*np.pi*1e-3*f_2*t+xi_2))
    # return A_aus*((1-C_id)/2+C_id*B*(1-2*Im_1*alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)-2*Im_2*alpha_2*np.sin(2*np.pi*1e-3*f_2*t+xi_2)))

sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/TOF A+B/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"

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
            am_2=tot_data[0,-4]
            am_1=tot_data[0,-7]
            print("f1=", f_1)
            print("f2=", f_2)
            print("a1=", am_1)
            print("a2=", am_2)
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
P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, 0.5]
B0=([100,0,0.01,-10],[np.amax(ps_data)+10000,np.amax(ps_data)+10000,5, 10])
p_int,cov_int=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
err_int=np.diag(cov_int)**0.5
j0_1=jv(0,alpha_1*0)
j0_2=jv(0,alpha_2*0)
j0_1_err=abs(djv0(alpha_1)*alpha_1_err)*0
j0_2_err=abs(djv0(alpha_2)*alpha_2_err)*0
C_D=(2*a_1*a_2)
C_id = p_int[1]/C_D
C_id_err = ((C_D*err_int[1])**2+(C_D*a_1_err/a_1)**2+(C_D*a_2_err/a_2)**2+(C_D*j0_1_err/j0_1)**2+(C_D*j0_2_err/j0_2)**2)**0.5
A=p_int[0]*(1-C_id)/2
A_err= (((1-C_id)/2*err_int[0])**2+(p_int[0]/2*C_id_err)**2)**0.5
A_aus=p_int[0]/len(time)
A_aus_err=err_int[0]/len(time)
w_ps=p_int[-2]
chi_0=p_int[-1]
chi_0_err=err_int[-1]
print("A(1-C)/2=", A, "+-", A_err)
print("C=",C_id, "+-", C_id_err)
print("chi_err=",err_int[-1])
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
ax.errorbar(ps_pos,ps_data, yerr=ps_data**0.5,fmt="ko",capsize=5, ms=3)
ax.plot(ps_plt,fit_cos(ps_plt, *p_int), "b")
ax.vlines(p_int[-1]/p_int[-2],fit_cos(p_int[-1]/p_int[-2]+np.pi,*p_int),fit_cos(p_int[-1]/p_int[-2],*p_int), color="k")

matrix_err_fit=(matrix_err**2/(C_id*A_aus)**2+matrix**2*A_aus_err**2/(A_aus**2*C_id)**2+((matrix/A_aus-0.5)/C_id**2)**2*C_id_err**2)**0.5
matrix_fit=(matrix-A_aus/2)/(A_aus*C_id)+1/2

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

for i in range(len(ps_pos)):
    func_data=matrix[i]
    func_data_err=matrix_err[i]
    func_data_fit=matrix_fit[i]
    func_data_fit_err=matrix_err_fit[i]
    chi_aus=chi[i]
    P0=[np.cos(chi[i]/2)**2, w1(chi[i]).imag*alpha_1, w2(chi[i]).imag*alpha_2, -1, 1]
    # print(P0)
    B0=([0,w1(chi[i]).imag*alpha_1-1000, w2(chi[i]).imag*alpha_2-1000, -2*np.pi, -2*np.pi],[np.inf, w1(chi[i]).imag*alpha_1+1000, w2(chi[i]).imag*alpha_2+1000, 2*np.pi, 2*np.pi])
    p_Im,cov_Im = fit(fit_Im, time, func_data_fit, sigma=func_data_fit_err, p0=P0, bounds=B0)
    err_Im=np.diag(cov_Im)**0.5
    # print(p_Im[-1],p_Im[-2])
    # print(p_Im,err_Im)
    Im_data_1_fit[i]=p_Im[1]/alpha_1
    Im_data_err_1_fit[i]=(err_Im[1]**2/alpha_1**2+alpha_1_err**2*p_Im[1]**2/alpha_1**4)**0.5
    Im_data_2_fit[i]=p_Im[2]/alpha_2
    Im_data_err_2_fit[i]=(err_Im[2]**2/alpha_2**2+alpha_2_err**2*p_Im[2]**2/alpha_2**4)**0.5
    cos2_fit[i]=p_Im[1]*p_Im[0]#*C_id#+p_Im[0]*(1-C_id)/2
    cos2_err_fit[i]=err_Im[1]
    
    yf_data = fft(func_data)
    yf_data_err = np.ones(len(yf_data))*np.sum(matrix_err)**0.5
    # print(sum(abs(yf_data)))
    xf = fftfreq(N, S_F)*1e3
    var=np.sum(func_data_err**2/N)**0.5
    
    # fig = plt.figure(figsize=(8,6))
    # ax = fig.add_subplot(111)
    # ax.errorbar(time, matrix_fit[i], yerr= matrix_err_fit[i], fmt="ko")
    # ax.plot(time_plt, fit_Im(time_plt, *p_Im))
    # ax.set_title(str("%.2f"%chi[i],))
    # ax.errorbar(xf, np.abs(yf_data), np.abs(yf_data_err), fmt="k.", capsize=5)
    # ax.set_xlim([-5,5])
    
    c_0_data=abs(yf_data[abs(xf)<1/S_F/2]).astype(complex)-A
    c_1_data_1=(yf_data[abs(xf-f_1)<1/S_F/2]).astype(complex)
    c_1_data_2=(yf_data[abs(xf-f_2)<1/S_F/2]).astype(complex)
    
    c_0_data_err=(var**2+A_err**2)**0.5
    c_1_data_err_1=var
    c_1_data_err_2=var
    # print(chi[i], np.angle(c_1_data))
    # if i==0:
    #     # print("here")
    #     e_mxi_1=np.exp(-1j*(np.angle(c_1_data_1)))
    #     e_mxi_2=np.exp(-1j*(np.angle(c_1_data_2)))
    if (c_1_data_1).real>0:
        # print("here")
        e_mxi_1=np.exp(-1j*(np.angle(c_1_data_1)))
        
    else:
        e_mxi_1=np.exp(-1j*(np.angle(c_1_data_1)+np.pi))
    if (c_1_data_2).real<0:
        # print("here")
        e_mxi_2=np.exp(-1j*(np.angle(c_1_data_2)))
        
    else:
        e_mxi_2=np.exp(-1j*(np.angle(c_1_data_2)+np.pi))
    cos2[i]=abs(c_0_data)
    cos2_err[i]=abs(c_0_data_err)
    
    Im_data_1[i]=(c_1_data_1*e_mxi_1).real/(cos2[i])/alpha_1
    Im_data_err_1[i]=(abs(c_1_data_err_1/cos2[i])**2 + ((abs(c_1_data_1*e_mxi_1)/cos2[i]**2)*cos2_err[i])**2+(abs(c_1_data_1*e_mxi_1)/cos2[i]/alpha_1*alpha_1_err)**2)**0.5/abs(alpha_1)
    Im_data_2[i]=(c_1_data_2*e_mxi_2).real/(cos2[i])/alpha_2
    Im_data_err_2[i]=(abs(c_1_data_err_2/cos2[i])**2 + (abs((c_1_data_2*e_mxi_2)/cos2[i]**2)*cos2_err[i])**2+abs((c_1_data_2*e_mxi_2)/cos2[i]/alpha_2*alpha_2_err)**2)**0.5/abs(alpha_2)

psi_p=(a_1+np.exp(1j*chi)*a_2)/(2**0.5)
psi_m=(a_1-np.exp(1j*chi)*a_2)/(2**0.5)
M=np.abs(psi_p/psi_m)
th= np.angle(psi_p/psi_m)
pi_shift=[*np.arange(7,22),*np.arange(0,7)]
cos2pi=-cos2+np.amax(cos2)
M[:15]=(cos2[:15]/cos2[pi_shift[:15]])**0.5
# M=(cos2/cos2pi)**0.5
M_err=M**0.5*((cos2_err/cos2)**2+(cos2_err[pi_shift]/cos2[pi_shift])**2)**0.5
Re_1=Im_data_1[pi_shift]/(M*np.sin(th))-Im_data_1/np.tan(th)
Re_err_1=((Im_data_err_1[pi_shift]/(M*np.sin(th)))**2+(Im_data_1[pi_shift]/(M**2*np.sin(th)))**2*M_err**2+(Im_data_err_1/np.tan(th))**2)**0.5
Re_2=-Im_data_2/np.tan(th)-Im_data_2[pi_shift]/(M*np.sin(th))
Re_err_2=((Im_data_err_2[pi_shift]/(M*np.sin(th)))**2+(Im_data_2[pi_shift]/(M**2*np.sin(th)))**2*M_err**2+(Im_data_err_2/np.tan(th))**2)**0.5

ylim1=-1.0
ylim2=2.5
y1=0.06
y2=0.05
xlim1=chi[0]-0.2
xlim2=chi[-7]-0.2
ws=0.2
fig = plt.figure(figsize=(10,5))
# fig, axs = plt.subplots(1, 2, figsize=(10, 4))
gs = fig.add_gridspec(1, 2,  width_ratios=(1, 1), wspace=ws)
axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[0, 1])]
# axs[0].spines["right"].set_visible(False)
# axs[1].spines["left"].set_visible(False)

axs[1].tick_params(axis="y", left=False, labelleft=False, right=True,labelright=True)
fig.suptitle("$w_{+,2}$")# $(a_2/a_1\\approx$"+str("%.2f" % (a_21),)+")")
colors=["k","#f10d0c","#00a933","#5983b0"]
for ax in axs:
    ax.errorbar(chi[:-7], Re_2[:-7], Re_err_2[:-7], fmt=".", color=colors[3], capsize=3, label="$\Im(w_{1,+})$ data")
    ax.plot(chi_plt[chi_plt<xlim2], w2(chi_plt).real[chi_plt<xlim2], "--", color=colors[3], alpha=0.5, label="$\Im(w_{1,+})$ theory")
    ax.errorbar(chi, Im_data_2, Im_data_err_2, fmt=".", color=colors[1], capsize=3, label="$\Im(w_{2,+})$ data")
    ax.plot(chi_plt, w2(chi_plt).imag, "--",color=colors[1], alpha=0.5, label="$\Im(w_{2,+})$ theory")
    # ax.set_xlim([xlim1,xlim2])
# axs[0].set_ylim([-2.5,5])
axs[1].set_ylim([ylim1,ylim2])
axs[0].set_xlabel("$\\chi$ [rad]")
axs[1].set_xlabel("$\\chi$ [rad]")
# axs[0].plot([xlim1,xlim2],[ylim1,ylim1], "r", lw=1, ls=(0,(5,3)))
# axs[0].plot([xlim1,xlim2],[ylim2,ylim2], "r", lw=1, ls=(0,(5,3)))

kwargs = dict(transform=axs[1].transAxes, color='k', lw=0.8, clip_on=False)
axs[1].plot((-ws, 0), (y1, 1), **kwargs)
axs[1].plot((-ws, 0), (y2, 0), **kwargs)
kwargs = dict(transform=axs[0].transAxes, color='k',  lw=0.8, clip_on=False)
axs[0].plot((0, 1), (y1, y1), **kwargs)
axs[0].plot((0, 1), (y2, y2), **kwargs)
axs[0].plot((0, 1), (y2, y2), **kwargs)
plt.show()