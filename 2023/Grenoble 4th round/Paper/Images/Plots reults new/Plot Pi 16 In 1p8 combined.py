#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:46:58 2024

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
rad=np.pi/180
a_1= 0.496
a_1_err= 0.003
a_2= 0.868
a_2_err= 0.002
a_21=a_2/a_1
a_21_err= a_21*((a_1_err/a_1)**2+(a_2_err/a_2)**2)**0.5
# inf_file_name="TOF_vs_chi_A+B_In1_22pt_pi16_2000s_4P_16Nov1733"
inf_file_name="TOF_vs_chi_A+B_In1_22pt_pi16_1200s_4P_15Nov0927"

alpha_1=0.1923 #/2.354
alpha_1_err=0.0009 
alpha_2=-0.1971 #/2.354
alpha_2_err=0.0004


def w1(chi):
    return (1/(1+a_21*np.exp(1j*chi)))

def w2(chi):
    return (1-1/(1+a_21*np.exp(1j*chi)))

def fit_cos(x, A, B, C, D):
    return A/2*(1+B*np.cos(C*x-D))

data_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Results txt/In 1p8"

i=0
k=0
j=0
for root, dirs, files in os.walk(data_fold_path, topdown=False):
    n_data_set=len(files)/3
    # print(n_data_set)
    for name in files:
        if "cos2" in name:
            ps_pos=np.loadtxt(os.path.join(root, name))[:,0]
            cos2_avg=np.loadtxt(os.path.join(root, name))[:,1]
            cos2_avg_err=np.loadtxt(os.path.join(root, name))[:,2]**2
        if "Wv12_Im" in name:
            # print(name)
            if i==0:
                chi_im=np.loadtxt(os.path.join(root, name))[:,0]
                Im_1_avg=np.loadtxt(os.path.join(root, name))[:,1]
                Im_1_avg_err=np.loadtxt(os.path.join(root, name))[:,2]**2
                Im_2_avg=np.loadtxt(os.path.join(root, name))[:,3]
                Im_2_avg_err=np.loadtxt(os.path.join(root, name))[:,4]**2
                i+=1
            else:
                Im_1_avg+=np.loadtxt(os.path.join(root, name))[:,1]
                Im_1_avg_err+=np.loadtxt(os.path.join(root, name))[:,2]**2
                Im_2_avg+=np.loadtxt(os.path.join(root, name))[:,3]
                Im_2_avg_err+=np.loadtxt(os.path.join(root, name))[:,4]**2
        if "Wv12_Re" in name:
            # print(name)
            if k==0:
                chi_Re=np.loadtxt(os.path.join(root, name))[:,0]
                Re_1_avg=np.loadtxt(os.path.join(root, name))[:,1]
                Re_1_avg_err=np.loadtxt(os.path.join(root, name))[:,2]**2
                Re_2_avg=np.loadtxt(os.path.join(root, name))[:,3]
                Re_2_avg_err=np.loadtxt(os.path.join(root, name))[:,4]**2
                k+=1
                
            else:
                Re_1_avg+=np.loadtxt(os.path.join(root, name))[:,1]
                Re_1_avg_err+=np.loadtxt(os.path.join(root, name))[:,2]**2
                Re_2_avg+=np.loadtxt(os.path.join(root, name))[:,3]
                Re_2_avg_err+=np.loadtxt(os.path.join(root, name))[:,4]**2
Im_1_avg/=n_data_set
Im_2_avg/=n_data_set
Re_1_avg/=n_data_set
Re_1_avg/=n_data_set
cos2_avg/=n_data_set
Im_1_avg_err=Im_1_avg_err**0.5/n_data_set
Im_2_avg_err=Im_2_avg_err**0.5/n_data_set
Re_1_avg_err=Re_1_avg_err**0.5/n_data_set
Re_1_avg_err=Re_1_avg_err**0.5/n_data_set
cos2_avg_err=cos2_avg_err**0.5/n_data_set

P0=[(np.amax(cos2_avg)+np.amin(cos2_avg))/2, (np.amax(cos2_avg)-np.amin(cos2_avg))/2, 3, 0]
B0=([100,0,0.01,-10],[np.amax(cos2_avg)+10000,np.amax(cos2_avg)+10000,5, 10])
p_int,cov_int=fit(fit_cos, ps_pos, cos2_avg, p0=P0,  bounds=B0, sigma=cos2_avg_err)
err_int=np.diag(cov_int)**0.5
w_ps=p_int[-2]
chi_0=p_int[-1]
chi=ps_pos*w_ps-chi_0

chi_plt=np.linspace(chi[0], chi[-1],500)
psi_p=(a_1+np.exp(1j*chi)*a_2)/(2**0.5)
psi_m=(a_1-np.exp(1j*chi)*a_2)/(2**0.5)
M=np.abs(psi_p/psi_m)
th= np.angle(psi_p/psi_m)
pi_shift=[*np.arange(7,22),*np.arange(0,7)]

cos2pi=-cos2_avg+np.amax(cos2_avg)
M[:15]=(cos2_avg[:15]/cos2_avg[pi_shift[:15]])**0.5
# M=(cos2_avg/cos2_avgpi)**0.5
M_err=M**0.5*((cos2_avg_err/cos2_avg)**2+(cos2_avg_err[pi_shift]/cos2_avg[pi_shift])**2)**0.5
Re_1_avg=Im_1_avg[pi_shift]/(M*np.sin(th))-Im_1_avg/np.tan(th)
Re_1_avg_err=((Im_1_avg_err[pi_shift]/(M*np.sin(th)))**2+(Im_1_avg[pi_shift]/(M**2*np.sin(th)))**2*M_err**2+(Im_1_avg_err/np.tan(th))**2)**0.5
Re_2_avg=-Im_2_avg/np.tan(th)-Im_2_avg[pi_shift]/(M*np.sin(th))
Re_2_avg_err=((Im_2_avg_err[pi_shift]/(M*np.sin(th)))**2+(Im_2_avg[pi_shift]/(M**2*np.sin(th)))**2*M_err**2+(Im_2_avg_err/np.tan(th))**2)**0.5

xlim1=chi[0]-0.2
xlim2=chi[-7]-0.2
d=0.02
h=0.05

ylim_re_1=-1.5
ylim_re_2=3
y_re_labels=np.arange(ylim_re_1+1,ylim_re_2,1)
ylim_im_1=-1
ylim_im_2=1
y_im_labels=np.arange(ylim_im_1+0.5,ylim_im_2,0.5)

fig = plt.figure(figsize=(8,5), dpi=150)
gs = fig.add_gridspec(3,3, height_ratios=(7,1, 6), hspace=0.0,wspace=0.3)
# ax_aus=fig.add_subplot(gs[1:, 0])
# ax_aus.tick_params(axis="both", bottom=False, labelbottom=False,left=False, labelleft=False,)

axsl = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[1:, 0])]
axsl[0].tick_params(axis="x", bottom=False, labelbottom=False)
axsl[0].set_title("$w_{+,1}$")#"a_2/a_1\\approx$"+str("%.2f" % (a_21),)+")")



axsl[0].errorbar(chi, Im_1_avg, Im_1_avg_err, fmt=".", color=colors[0], capsize=3, label="$\Im(w_{1,+})$ data")
axsl[0].plot(chi_plt, w1(chi_plt).imag, "--",color=colors[0], alpha=0.5, label="$\Im(w_{1,+})$ theory")
axsl[0].set_ylim([ylim_im_1,ylim_im_2])
axsl[0].set_yticks(ticks=y_im_labels)
axsl[0].grid(True, ls="dotted")
# axsl[0].yaxis.set_label_coords(-0.25,0.5)
axsl[0].set_ylabel("Imaginary part", fontsize=12)

axsl[1].errorbar(chi[:-7], Re_1_avg[:-7], Re_1_avg_err[:-7], fmt=".", color=colors[2], capsize=3, label="$\Im(w_{1,+})$ data")
axsl[1].plot(chi_plt, w1(chi_plt).real, "--", color=colors[2], alpha=0.5, label="$\Im(w_{1,+})$ theory")
axsl[1].grid(True, ls="dotted")
# axsl[1].yaxis.set_label_coords(-0.2,0.5)
axsl[1].set_ylabel("Real part", fontsize=12)
axsl[1].set_ylim([ylim_re_1,ylim_re_2])
# axsl[1].set_yticks(ticks=axsl[1].get_yticks()[1:-1])
axsl[1].set_yticks(ticks=y_re_labels)
axsl[1].set_xlabel("$\\chi$ [rad]")
for ax in axsl:
    ax.set_xticks([-2*np.pi,-np.pi,0,np.pi])
    ax.set_xticklabels(["-$2\pi$","-$\pi$","0","$\pi$"])
    
ylim_re_1=-0.5
ylim_re_2=2.5
y_re_labels=np.arange(ylim_re_1+0.5,ylim_re_2,0.5)
ylim_im_1=-1
ylim_im_2=1
y_im_labels=np.arange(ylim_im_1+0.5,ylim_im_2,0.5)

# ax_aus.set_ylabel("$w^\Re_{+,2}$", fontsize=12, rotation=270, va="bottom", ha="center")
axsc = [fig.add_subplot(gs[0, 1]),fig.add_subplot(gs[1:, 1])]
axsc[0].tick_params(axis="x", bottom=False, labelbottom=False)
axsc[0].set_title("$w_{+,2}$")#"\t$(a_2/a_1\\approx$"+str("%.2f" % (a_21),)+")")
axsc[0].errorbar(chi, Im_2_avg, Im_2_avg_err, fmt=".", color=colors[1], capsize=3, label="$\Im(w_{2,+})$ data")
axsc[0].plot(chi_plt, w2(chi_plt).imag, "--",color=colors[1], alpha=0.5, label="$\Im(w_{2,+})$ theory")
axsc[0].set_ylim([ylim_im_1,ylim_im_2])
axsc[0].set_yticks(ticks=y_im_labels)
axsc[0].grid(True, ls="dotted")

axsc[1].errorbar(chi[:-7], Re_2_avg[:-7], Re_2_avg_err[:-7], fmt=".", color=colors[3], capsize=3, label="$\Im(w_{1,+})$ data")
axsc[1].plot(chi_plt, w2(chi_plt).real, "--", color=colors[3], alpha=0.5, label="$\Im(w_{1,+})$ theory")
axsc[1].grid(True, ls="dotted")
# axsc[1].set_yticks(ticks=axsc[1].get_yticks()[1:-1])
axsc[1].set_ylim([ylim_re_1,ylim_re_2])
axsc[1].set_yticks(ticks=y_re_labels)
axsc[1].grid(True, ls="dotted")
# axsc[1].set_yticks(ticks=ylabels)
axsc[1].set_xlabel("$\\chi$ [rad]")
for ax in axsc:
    ax.set_xticks([-2*np.pi,-np.pi,0,np.pi])
    ax.set_xticklabels(["-$2\pi$","-$\pi$","0","$\pi$"])

axsr = [fig.add_subplot(gs[0, 2]),fig.add_subplot(gs[1:, 2])]
axsr[0].tick_params(axis="x", bottom=False, labelbottom=False)
axsr[0].errorbar(chi, Im_1_avg+Im_2_avg, (Im_1_avg_err**2+Im_2_avg_err**2)**0.5, fmt=".", color=colors[1], capsize=3, label="$\Im(w_{2,+})$ data")
axsr[0].plot(chi_plt, w1(chi_plt).imag+w2(chi_plt).imag, "--",color=colors[1], alpha=0.5, label="$\Im(w_{2,+})$ theory")
axsr[0].grid(True, ls="dotted")
axsr[0].set_ylim([-1,1])
axsr[0].set_yticks(ticks=axsr[0].get_yticks()[1:-1])
axsr[0].set_title("$w_{+,1}+w_{+,2}$")

axsr[1].errorbar(chi[:-7], Re_2_avg[:-7]+Re_1_avg[:-7], (Re_2_avg_err[:-7]**2+Re_2_avg_err[:-7]**2)**0.5, fmt=".", color=colors[3], capsize=3, label="$\Im(w_{1,+})$ data")
axsr[1].plot(chi_plt, w2(chi_plt).real+w1(chi_plt).real, "--", color=colors[3], alpha=0.5, label="$\Im(w_{1,+})$ theory")
axsr[1].grid(True, ls="dotted")
axsr[1].set_ylim([-1,3])
axsr[1].set_yticks(ticks=axsr[1].get_yticks()[1:-1])

axsr[1].set_xlabel("$\\chi$ [rad]")
for ax in axsr:
    ax.set_xticks([-2*np.pi,-np.pi,0,np.pi])
    ax.set_xticklabels(["-$2\pi$","-$\pi$","0","$\pi$"])
    
    ax.set_xticks([-2*np.pi,-np.pi,0,np.pi])
    ax.set_xticklabels(["-$2\pi$","-$\pi$","0","$\pi$"])

plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Images/Wv In 1p8 combined.pdf", format="pdf",bbox_inches="tight")


# with open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Results txt/No In/Wv12_Im No In"+inf_file_name[-10:]+".txt","w") as f:
#     np.savetxt(f,np.transpose([chi,Im_1_avg,Im_1_avg_err,Im_2_avg,Im_2_avg_err]), header="chi w_im1 w_im1_err w_im2 w_im2_err")
# with open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Results txt/No In/Wv12_Re No In"+inf_file_name[-10:]+".txt","w") as f:
#     np.savetxt(f,np.transpose([chi,Re_1,Re_err_1,Re_2,Re_err_2]), header="chi w_re1 w_re1_err w_re2 w_re2_err")
    

plt.show()