#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 15:24:12 2024

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
colors=["k","#f10d0c","#00a933","#5983b0"]
plt.rcParams["mathtext.fontset"]="cm"
rad=np.pi/180
# T_1= 0.4103632617796827 +- 0.0018958686061004615
# T_2= 0.5896367382203174 +- 0.0018958686061004615
# a_1= 0.641
# a_1_err=0.003
# a_2= 0.768
# a_2_err=0.002
# a_21=a_2/a_1

# inf_file_name="TOF_vs_chi_A+B_In1_08mm_22pt_pi16_1200s_4P_16Nov0206"

# a_1= 0.496
# a_1_err= 0.003
# a_2= 0.868
# a_2_err= 0.002
# a_21=a_2/a_1
# a_21_err= a_21*((a_1_err/a_1)**2+(a_2_err/a_2)**2)**0.5
# # inf_file_name="TOF_vs_chi_A+B_In1_22pt_pi16_2000s_4P_16Nov1733"
# inf_file_name="TOF_vs_chi_A+B_In1_22pt_pi16_1200s_4P_15Nov0927"

a_1= 0.751
a_1_err= 0.003
a_2= 0.660
a_2_err=0.003
a_21=a_2/a_1
a_21_err= a_21*((a_1_err/a_1)**2+(a_2_err/a_2)**2)**0.5

inf_file_name="TOF_vs_chi_A+B_22pt_pi16_1200s_09Nov1808"
# inf_file_name="TOF_vs_chi_A+B_22pt_pi16_1200s_4P_11Nov1354"
# inf_file_name="TOF_vs_chi_A+B_22pt_pi16_1200s_4P_11Nov0502"

alpha_1=0.1932 #/2.354
alpha_1_err=0.0005
alpha_2=0.1969 #/2.354
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
def fit_Im(t, A, B, C, xi_1, xi_2):
    # xi_1=2.2038275    
    # xi_2=1.2313203
    return A+2*B*np.sin(2*np.pi*1e-3*f_1*t+xi_1)+2*C*np.sin(2*np.pi*1e-3*f_2*t+xi_2)

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
P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, 0]
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
fig = plt.figure(figsize=(3,3), dpi=200)
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
chi_plt=np.linspace(chi[0], chi[-1], 200)
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
    P0=[np.cos(chi[i]/2)**2, w1(chi[i]).imag*(alpha_1*(np.cos(chi[i]/2)**2-A_aus*(1-C_id)/2)), w2(chi[i]).imag*alpha_2*A_aus, 2.2, 1.23]
    # print(P0)
    B0=([0,w1(chi[i]).imag*alpha_1-1000, w2(chi[i]).imag*alpha_2-1000, -2*np.pi, -2*np.pi],[np.inf, w1(chi[i]).imag*alpha_1+1000, w2(chi[i]).imag*alpha_2+1000, 2*np.pi, 2*np.pi])
    
    p_Im,cov_Im = fit(fit_Im, time, func_data, sigma=func_data_err, p0=P0, bounds=B0)
    err_Im=np.diag(cov_Im)**0.5
    # print(p_Im[-1],p_Im[-2])
    # print(p_Im,err_Im)
    A_err_fit= (((1-C_id)/2*A_aus_err)**2+(A_aus/2*C_id_err)**2)**0.5
    err_Im[0]=(err_Im[0]**2+A_err_fit**2)**0.5
    # p_Im[0]-=A/len(time)
    Im_data_1_fit[i]=p_Im[1]/(alpha_1*(p_Im[0]-A_aus*(1-C_id)/2))
    Im_data_err_1_fit[i]=abs(Im_data_1_fit[i])*((err_Im[1]/p_Im[1])**2+(alpha_1_err/alpha_1)**2+(err_Im[0]/p_Im[0])**2)**0.5
    Im_data_2_fit[i]=p_Im[2]/(alpha_2*(p_Im[0]-A_aus*(1-C_id)/2))
    Im_data_err_2_fit[i]=abs(Im_data_2_fit[i])*((err_Im[2]/p_Im[2])**2+(alpha_2_err/alpha_2)**2+(err_Im[0]/p_Im[0])**2)**0.5
    cos2_fit[i]=p_Im[1]*p_Im[0]#*C_id#+p_Im[0]*(1-C_id)/2
    cos2_err_fit[i]=err_Im[1]
    
    # p_Im,cov_Im = fit(fit_Im, time, func_data_fit, sigma=func_data_fit_err, p0=P0, bounds=B0)
    # err_Im=np.diag(cov_Im)**0.5
    # # print(p_Im[-1],p_Im[-2])
    # # print(p_Im,err_Im)
    # Im_data_1_fit[i]=p_Im[1]/alpha_1
    # Im_data_err_1_fit[i]=(err_Im[1]**2/alpha_1**2+alpha_1_err**2*p_Im[1]**2/alpha_1**4)**0.5
    # Im_data_2_fit[i]=p_Im[2]/alpha_2
    # Im_data_err_2_fit[i]=(err_Im[2]**2/alpha_2**2+alpha_2_err**2*p_Im[2]**2/alpha_2**4)**0.5
    # cos2_fit[i]=p_Im[1]*p_Im[0]#*C_id#+p_Im[0]*(1-C_id)/2
    # cos2_err_fit[i]=err_Im[1]
    Norm=1#N**2
    yf_data = fft(func_data)/(Norm)**0.5
    
    # print(sum(abs(yf_data)))
    xf = fftfreq(N, S_F)*1e3
    var=np.sum(func_data/2)**0.5
    yf_data_err = np.ones(len(yf_data))*var
    print(var)
    # fig = plt.figure(figsize=(8,6))
    # ax = fig.add_subplot(111)
    # # ax.errorbar(time, matrix[i], yerr= matrix_err[i], fmt="ko")
    # # ax.plot(time_plt, fit_Im(time_plt, *p_Im))
    # # ax.set_title(str("%.2f"%chi[i],))
    # ax.errorbar(0, np.average(matrix[i]), fmt="ro", capsize=5)
    # ax.errorbar(0,A/Norm**0.5, fmt="bo", capsize=5)
    # ax.errorbar(xf, np.abs(yf_data), np.abs(yf_data_err), fmt="k.", capsize=5)
    # ax.set_xlim([-5,5])
    
    c_0_data=abs(yf_data[abs(xf)<1/S_F/2]).astype(complex)-A/Norm**0.5
    c_1_data_1=(yf_data[abs(xf-f_1)<1/S_F/2]).astype(complex)
    c_1_data_2=(yf_data[abs(xf-f_2)<1/S_F/2]).astype(complex)
    var=(abs(yf_data[abs(xf)<1/S_F/2])/2)**0.5
    c_0_data_err=(2*var**2+A_err**2/Norm**2)**0.5
    c_1_data_err_1=var
    c_1_data_err_2=var
    e_mxi_1=np.exp(-1j*(np.angle(c_1_data_1)))
    e_mxi_2=np.exp(-1j*(np.angle(c_1_data_2)))
    # xi_1=2.404544909127107
    # e_mxi_1=np.exp(-1j*(xi_1))
    # xi_2=2.6491221178165554-np.pi/2
    # e_mxi_2=np.exp(-1j*xi_2)
    
    cos2[i]=abs(c_0_data)
    cos2_err[i]=abs(c_0_data_err)
    
    # Im_data_1[i]=np.sign(c_1_data_1.real)*abs(c_1_data_1)/(cos2[i])/alpha_1
    Im_data_1[i]=np.sign(e_mxi_1.real)*abs(c_1_data_1)/(cos2[i])/alpha_1
    Im_data_err_1[i]=abs(Im_data_1[i])*(abs(c_1_data_err_1/abs(c_1_data_1))**2 + (cos2_err[i]/cos2[i])**2+(alpha_1_err/alpha_1)**2)**0.5
    Im_data_2[i]=np.sign(e_mxi_2.real)*abs(c_1_data_2)/(cos2[i])/alpha_2
    Im_data_err_2[i]=abs(Im_data_2[i])*(abs(c_1_data_err_2/abs(c_1_data_2))**2 + (cos2_err[i]/cos2[i])**2+(alpha_2_err/alpha_2)**2)**0.5

ylim_im_1=-4
ylim_im_2=4

fig = plt.figure(figsize=(8,2.5), dpi=200)
gs = fig.add_gridspec(1,3)
axs=[fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[0, 2])]
axs[0].set_ylabel("$w^\Im_{+,1}$", fontsize=13)
axs[0].errorbar(chi, Im_data_1, Im_data_err_1, fmt=".", color=colors[0], capsize=3, label="Data")
axs[1].errorbar(chi, Im_data_1_fit, Im_data_err_1_fit, fmt=".", color=colors[0], capsize=3, label="Data")
axs[2].errorbar(chi, Im_data_1_fit-Im_data_1, fmt="-", color=colors[0], capsize=3, label="Data")
axs[2].errorbar(chi, Im_data_err_1_fit-Im_data_err_1, fmt="--", color=colors[1], capsize=3, label="Data")
# axs[0].set_ylim([ylim_im_1,ylim_im_2])
# axs[0].text("Fourier method")
# axs[0].text("Fit method")
# axs[1].tick_params(axis="y", left=False, labelleft=False)
# axs[2].tick_params(axis="y", left=False, labelleft=False)
k=0
for ax in axs[:-1]:
    ax.grid(True, ls="dotted")
    ax.set_xlabel("$\mathdefault{\\chi}$ [rad]")
    ax.plot(chi_plt, w1(chi_plt).imag, "-", color=colors[2], label="Theory")
    ax.set_ylim([ylim_im_1,ylim_im_2])
    ax.set_yticks(ticks=ax.get_yticks())
    k+=1
axs[1].legend(loc=9, ncol=1, framealpha=1)#, bbox_to_anchor=(0,0.45))
# axs[1].yaxis.set_label_coords(-0.15,1)
# ax.set_xlim([chi[0]-0.2,chi[-1]+0.2])
# ax.yaxis.set_label_position("right")
# ax.set_ylabel("$w^\Im_{+,1}$", fontsize=12, rotation=270, va="bottom", ha="center")
axs[2].grid(True, ls="dotted")
axs[2].set_ylim([-2,2])
axs[2].set_yticks(ticks=axs[2].get_yticks()[::2])
axs[0].set_title("Fourier transform method", fontsize=11)
axs[1].set_title("Fit method", fontsize=11)
axs[2].set_title("Difference", fontsize=11)
print(np.average(abs(Im_data_1_fit-Im_data_1)/(Im_data_err_1_fit**2+Im_data_err_1**2)**0.5))
# fig = plt.figure(figsize=(8,2.5), dpi=200)
# gs = fig.add_gridspec(1,2, wspace=0.0)
# axs=[fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])]
# axs[0].set_ylabel("$w^\Im_{+,1}$", fontsize=13)
# axs[0].errorbar(chi, Im_data_1, Im_data_err_1, fmt=".", color=colors[0], capsize=3, label="Data")
# axs[1].errorbar(chi, Im_data_1_fit, Im_data_err_1_fit, fmt=".", color=colors[0], capsize=3, label="Data")
# # axs[0].set_ylim([ylim_im_1,ylim_im_2])
# # axs[0].text("Fourier method")
# # axs[0].text("Fit method")
# axs[1].tick_params(axis="y", left=False, labelleft=False)

# for ax in axs:
#     ax.set_ylim([ylim_im_1,ylim_im_2])
#     ax.set_yticks(ticks=ax.get_yticks()[1:-1])
#     ax.grid(True, ls="dotted")
#     ax.plot(chi_plt, w1(chi_plt).imag, "-", color=colors[2], label="Theory")
#     ax.set_xlabel("$\mathdefault{\\chi}$ [rad]")
#     ax.set_yticks(ticks=ax.get_yticks())
# axs[0].legend(loc=1, ncol=2, framealpha=1)#, bbox_to_anchor=(0,0.45))
# # axs[1].yaxis.set_label_coords(-0.15,1)
# # ax.set_xlim([chi[0]-0.2,chi[-1]+0.2])
# # ax.yaxis.set_label_position("right")
# # ax.set_ylabel("$w^\Im_{+,1}$", fontsize=12, rotation=270, va="bottom", ha="center")

# axs[0].set_title("Fourier transform Method", fontsize=11)
# axs[1].set_title("Fit Method", fontsize=11)

# fig = plt.figure(figsize=(3,5), dpi=200)
# gs = fig.add_gridspec(2,1, hspace=0.0)
# axs=[fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[1, 0])]
# axs[0].set_title("$w_{+,1}$", fontsize=13)
# axs[0].errorbar(chi, Im_data_1, Im_data_err_1, fmt=".", color=colors[0], capsize=3, label="Data")
# axs[1].errorbar(chi, Im_data_1_fit, Im_data_err_1_fit, fmt=".", color=colors[0], capsize=3, label="Data")
# # axs[0].set_ylim([ylim_im_1,ylim_im_2])
# # axs[0].set_yticks(ticks=ax.get_yticks()[1:-1])
# # axs[0].text("Fourier method")
# # axs[0].text("Fit method")

# for ax in axs:
#     ax.set_ylim([ylim_im_1,ylim_im_2])
#     ax.set_yticks(ticks=ax.get_yticks()[1:-1])
#     ax.grid(True, ls="dotted")
#     ax.plot(chi_plt, w1(chi_plt).imag, "-",color=colors[3], alpha=0.8, label="Theory")
# axs[1].legend(loc=10, ncol=1, bbox_to_anchor=(0.5,1), framealpha=1)
# # axs[1].yaxis.set_label_coords(-0.15,1)
# # ax.set_xlim([chi[0]-0.2,chi[-1]+0.2])
# # ax.yaxis.set_label_position("right")
# # ax.set_ylabel("$w^\Im_{+,1}$", fontsize=12, rotation=270, va="bottom", ha="center")
# axs[1].set_xlabel("$\mathdefault{\\chi}$ [rad]")
# axs[0].set_ylabel("Imaginary part\n(Fourier Method)", fontsize=11)
# axs[1].set_ylabel("Imaginary part\n(Fit Method)", fontsize=11)

# plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images 1 column/Fourier vs Fit.pdf", format="pdf",bbox_inches="tight")

# with open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Results txt fit/No In/Wv12_Im No In"+inf_file_name[-10:]+".txt","w") as f:
#     np.savetxt(f,np.transpose([chi,Im_data_1_fit,Im_data_err_1_fit,Im_data_2_fit,Im_data_err_2_fit]), header="chi w_im1 w_im1_err w_im2 w_im2_err")
# with open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Results txt/In 0p8/Wv12_Re In 0p8"+inf_file_name[-10:]+".txt","w") as f:
#     np.savetxt(f,np.transpose([chi,Re_1,Re_err_1,Re_2,Re_err_2]), header="chi w_re1 w_re1_err w_re2 w_re2_err")

# with open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Results txt fit/No In/cos2 No In"+inf_file_name[-10:]+".txt","w") as f:
#     np.savetxt(f,np.transpose([ps_pos,cos2_fit,cos2_err_fit]), header="chi cos2 cos2err")

plt.show()