# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:37:41 2023

@author: S18
"""
"""
inf_file_names:

"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib import font_manager
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
from matplotlib.lines import Line2D
chi_1_0=0
chi_2_0=0
chi_3_0=0
chi_1=0
chi_2=0
chi_3=0

C_12=0.74
C_13=0.66
C_23=0.63

a_1=0.5658772802794784 
a_2=0.5670749054927576 
a_3=0.5985056016645798

def w1(chi_1, chi_2, chi_3):
    Dchi_12=chi_1_0+chi_1-(chi_2_0+chi_2)
    Dchi_13=chi_1_0+chi_1-(chi_3_0+chi_3)
    Dchi_23=chi_2_0+chi_2-(chi_3_0+chi_3)
    A=a_1**2+C_12*a_1*a_2*np.exp(-1j*Dchi_12)+C_13*a_1*a_3*np.exp(-1j*Dchi_13)
    B=1+2*C_12*a_1*a_2*np.cos(Dchi_12)+2*C_13*a_1*a_3*np.cos(Dchi_13)+2*C_23*a_2*a_3*np.cos(Dchi_23)
    return A/B

def w2(chi_1, chi_2, chi_3):
    Dchi_12=chi_1_0+chi_1-(chi_2_0+chi_2)
    Dchi_13=chi_1_0+chi_1-(chi_3_0+chi_3)
    Dchi_23=chi_2_0+chi_2-(chi_3_0+chi_3)
    A=C_12*a_1*a_2*np.exp(1j*Dchi_12)+a_2**2+C_23*a_2*a_3*np.exp(-1j*Dchi_23)
    B=1+2*C_12*a_1*a_2*np.cos(Dchi_12)+2*C_13*a_1*a_3*np.cos(Dchi_13)+2*C_23*a_2*a_3*np.cos(Dchi_23)
    return A/B

def w3(chi_1, chi_2, chi_3):
    Dchi_12=chi_1_0+chi_1-(chi_2_0+chi_2)
    Dchi_13=chi_1_0+chi_1-(chi_3_0+chi_3)
    Dchi_23=chi_2_0+chi_2-(chi_3_0+chi_3)
    A=C_12*a_1*a_3*np.exp(1j*Dchi_13)+C_23*a_2*a_3*np.exp(1j*Dchi_23)+a_3**2
    B=1+2*C_12*a_1*a_2*np.cos(Dchi_12)+2*C_13*a_1*a_3*np.cos(Dchi_13)+2*C_23*a_2*a_3*np.cos(Dchi_23)
    return A/B


font_path = "/home/aaa/root/fonts/cmunrm.ttf"
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [prop.get_name(), "DejaVu Sans"]  # <- DejaVu als Fallback
plt.rcParams["font.size"] = 12
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["figure.dpi"] = 150
# plt.rcParams["legend.markerscale"] = 1
plt.rcParams["legend.fontsize"] = 11
plt.rcParams["axes.unicode_minus"] = False  # <- richtige Variante!

a_21_unb=0.588
a_21_bal=1
wv_1=np.loadtxt("/home/aaa/Desktop/Fisica/PhD/2026/Talks/ILL Seminar/Wv1_3_path.txt")
wv_2=np.loadtxt("/home/aaa/Desktop/Fisica/PhD/2026/Talks/ILL Seminar/Wv2_3_path.txt")
wv_3=np.loadtxt("/home/aaa/Desktop/Fisica/PhD/2026/Talks/ILL Seminar/Wv3_3_path.txt")

chi_1=wv_1[:,0]-2*np.pi
chi_2=wv_2[:,0]-2*np.pi
chi_3=wv_3[:,0]-2*np.pi
# print(len(chi))
chi_plt_1=np.linspace(chi_1[0], chi_1[-1], 1000)
chi_plt_2=np.linspace(chi_2[0], chi_2[-1], 1000)
chi_plt_3=np.linspace(chi_3[0], chi_3[-1], 1000)

Re_1=wv_1[:,1]
Re_1_err=wv_1[:,2]
Re_2=wv_2[:,1]
Re_2_err=wv_2[:,2]
Re_3=wv_3[:,1]
Re_3_err=wv_3[:,2]

Im_1=wv_1[:,3]
Im_1_err=wv_1[:,4]
Im_2=wv_2[:,3]
Im_2_err=wv_2[:,4]
Im_3=wv_3[:,3]
Im_3_err=wv_3[:,4]

fig = plt.figure(figsize=(10,5), dpi=250)
# gs_b = fig.add_gridspec(1,1)
# ax_b=fig.add_subplot(gs_b[0, 0])
# ax_b.tick_params(axis="both", bottom=False, labelbottom=False, left=False, labelleft=False)
# for side in ['right','left','top','bottom']:
#     ax_b.spines[side].set_visible(False)

gs = fig.add_gridspec(2,3 , height_ratios=(1.5,1), hspace=0.05, wspace=0)
axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[0, 1]),fig.add_subplot(gs[0, 2])]
axs1 = [fig.add_subplot(gs[1, 0]),fig.add_subplot(gs[1, 1]),fig.add_subplot(gs[1, 2])]

axs[0].set_title("Path 1")
axs[1].set_title("Path 2")
axs[2].set_title("Path 3")

axs[0].set_ylabel("Real part of the\nweak value")

colors=["k","#f10d0c","#00a933","#5983b0", "#fffff2"]
plt.rcParams["mathtext.fontset"]="cm"
for ax in axs:
    ax.set_xticks([-2*np.pi,-np.pi,0,np.pi,2*np.pi,3*np.pi])
    ax.set_xticklabels(["${-2\pi}$","${-\pi}$", "${0}$","${\pi}$","${2\pi}$","${3\pi}$"])
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    ax.grid(True, ls="dotted")
# axs[0].set_xlabel("Initial relative\nphase $\phi_1$ [rad]")
# axs[1].set_xlabel("Initial relative\nphase $\phi_2$ [rad]")
# axs[2].set_xlabel("Initial relative\nphase $\phi_3$ [rad]")
axs[1].tick_params(axis="y", left=False, labelleft=False)
axs[2].tick_params(axis="y", left=False, labelleft=False)

for ax in axs:
    ax.set_facecolor("#fffff2")
axs[0].plot(chi_plt_1, chi_plt_1*0, "-", color=colors[1], lw=0.5)
axs[0].plot(chi_plt_1, chi_plt_1*0+1, "-", color=colors[1], lw=0.5)
axs[0].plot(chi_plt_1, chi_plt_1*0+1/3, ":", color=colors[2], lw=1)#, label="Eigenvalue bound")
# ax.fill_between(chi_plt_1,0,1, color=colors[3], alpha=0.07)#, label="Eigenvalue range")
axs[0].fill_between(chi_plt_1,1,3, color="#fceeee")#, label="Eigenvalue range")
axs[0].fill_between(chi_plt_1,-3,0, color="#fceeee")
axs[1].plot(chi_plt_2, chi_plt_2*0, "-", color=colors[1], lw=0.5)
axs[1].plot(chi_plt_2, chi_plt_2*0+1, "-", color=colors[1], lw=0.5)
axs[1].plot(chi_plt_2, chi_plt_2*0+1/3, ":", color=colors[2], lw=1)#, label="Eigenvalue bound")
# ax.fill_between(chi_plt_2,0,1, color=colors[3], alpha=0.07)#, label="Eigenvalue range")
axs[1].fill_between(chi_plt_2,1,3, color="#fceeee")#, label="Eigenvalue range")
axs[1].fill_between(chi_plt_2,-3,0, color="#fceeee")
axs[2].plot(chi_plt_1, chi_plt_3*0, "-", color=colors[1], lw=0.5)
axs[2].plot(chi_plt_3, chi_plt_3*0+1, "-", color=colors[1], lw=0.5)
axs[2].plot(chi_plt_3, chi_plt_3*0+1/3, ":", color=colors[2], lw=1)#, label="Eigenvalue bound")
# ax.fill_between(chi_plt_1,0,1, color=colors[3], alpha=0.07)#, label="Eigenvalue range")
axs[2].fill_between(chi_plt_1,1,3, color="#fceeee")#, label="Eigenvalue range")
axs[2].fill_between(chi_plt_1,-3,0, color="#fceeee")

axs[0].errorbar(chi_1,Re_1, Re_1_err, fmt="k.", capsize=3, ms=4)
axs[0].plot(chi_plt_1, w1(chi_plt_1,0,0).real, color=colors[3], lw=1.5)
axs[1].errorbar(chi_2,Re_2, Re_2_err, fmt="k.", capsize=3, ms=4)
axs[1].plot(chi_plt_2, w2(0,chi_plt_2,0).real, color=colors[3], lw=1.5)
axs[2].errorbar(chi_3,Re_3, Re_3_err, fmt="k.", capsize=3, ms=4)
axs[2].plot(chi_plt_3, w3(0,0,chi_plt_3).real, color=colors[3], lw=1.5)

for ax in axs:
    ax.set_ylim([-0.5,0.45])
    ax.set_yticks([-0.4,0, 0.4])
    ax.set_yticklabels([-0.4,0, 0.4])

axs1[0].set_ylabel("Imaginary part of\nthe weak value")

colors=["k","#f10d0c","#00a933","#5983b0", "#fffff2"]
plt.rcParams["mathtext.fontset"]="cm"
for ax in axs1:
    ax.set_xticks([-2*np.pi,-np.pi,0,np.pi,2*np.pi,3*np.pi])
    ax.set_xticklabels(["${-2\pi}$","${-\pi}$", "${0}$","${\pi}$","${2\pi}$","${3\pi}$"])
    ax.grid(True, ls="dotted")
axs1[0].set_xlabel("Initial relative\nphase $\phi_1$ [rad]")
axs1[1].set_xlabel("Initial relative\nphase $\phi_2$ [rad]")
axs1[2].set_xlabel("Initial relative\nphase $\phi_3$ [rad]")
# axs1[0].tick_params(axis="x", bottom=False, labelbottom=False)
# axs1[1].tick_params(axis="x", bottom=False, labelbottom=False)
axs1[1].tick_params(axis="y", left=False, labelleft=False)
axs1[2].tick_params(axis="y", left=False, labelleft=False)

for ax in axs1:
    ax.set_facecolor("#fffff2")

axs1[0].errorbar(chi_1,Im_1, Im_1_err, fmt="k.", capsize=3, ms=4)
axs1[0].plot(chi_plt_1, w1(chi_plt_1,0,0).imag, color=colors[3], lw=1.5)
axs1[1].errorbar(chi_2,Im_2, Im_2_err, fmt="k.", capsize=3, ms=4)
axs1[1].plot(chi_plt_2, w2(0,chi_plt_2,0).imag, color=colors[3], lw=1.5)
axs1[2].errorbar(chi_3,Im_3, Im_3_err, fmt="k.", capsize=3, ms=4)
axs1[2].plot(chi_plt_3, w3(0,0,chi_plt_3).imag, color=colors[3], lw=1.5)

for ax in axs1:
    ax.set_ylim([-0.55,0.55])
    ax.set_yticks([-0.5,0, 0.5])
    ax.set_yticklabels([-0.5,0, 0.5])



# axs[1].text(-np.pi, 1.1,"Eigenvalue bound", color=colors[1])
# axs[1].text(-np.pi, 1.1,"Eigenvalue range", color=colors[3])
# axs[0].legend()
fig.savefig("/home/aaa/Desktop/Fisica/PhD/2026/Talks/ILL Seminar/Results 3 paths.svg",format='svg', bbox_inches='tight', pad_inches=0, transparent=False)   
# fig_b.savefig("/home/aaa/Desktop/Fisica/PhD/2026/Talks/ILL Seminar/Results real bal.svg",format='svg', bbox_inches='tight', pad_inches=0, transparent=False)   
plt.show()