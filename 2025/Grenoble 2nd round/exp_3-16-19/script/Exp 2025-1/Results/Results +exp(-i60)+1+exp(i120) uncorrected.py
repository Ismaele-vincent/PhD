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
import My_module_Exp_2025_1 as mymod

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

chi_1_0=-np.pi/3
chi_2_0=0
chi_3_0=2*np.pi/3
chi_1=0
chi_2=0
chi_3=0

inf_file_names=["ifg_wv1_psi_+exp(-i60)+1+exp(i120)_no_fit_22Oct2158", "ifg_wv2_psi_+exp(-i60)+1+exp(i120)_no_fit_22Oct2237", "ifg_wv3_psi_+exp(-i60)+1+exp(i120)_no_fit_22Oct2317"]

C_12, C_13, C_23 = mymod.contrast(inf_file_names[0])
print("C_12=", C_12, "C_13=", C_13, "C_23=", C_23)

fold_results="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Ifg wv no fit/Results Uncorrected/"
wv_1=np.loadtxt(fold_results+inf_file_names[0]+".txt")
wv_2=np.loadtxt(fold_results+inf_file_names[1]+".txt")
wv_3=np.loadtxt(fold_results+inf_file_names[2]+".txt")
a_vec_1 = np.loadtxt(fold_results+inf_file_names[0]+"_int.txt")
a_vec_2 = np.loadtxt(fold_results+inf_file_names[1]+"_int.txt")
a_vec_3 = np.loadtxt(fold_results+inf_file_names[2]+"_int.txt")

chi_1=wv_1[:,0]-2*np.pi
chi_2=wv_2[:,0]-2*np.pi
chi_3=wv_3[:,0]-2*np.pi
# print(len(chi))
chi_1_plt=np.linspace(chi_1[0], chi_1[-1], 1000)
chi_2_plt=np.linspace(chi_2[0], chi_2[-1], 1000)
chi_3_plt=np.linspace(chi_3[0], chi_3[-1], 1000)

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

w1=mymod.w1(*a_vec_1,  chi_1_plt, chi_1_0, 0, chi_2_0, 0, chi_3_0, C_12, C_13, C_23)
w2=mymod.w2(*a_vec_2,  0, chi_1_0, chi_2_plt, chi_2_0, 0, chi_3_0, C_12, C_13, C_23)
w3=mymod.w3(*a_vec_3,  0, chi_1_0, 0, chi_2_0, chi_3_plt, chi_3_0, C_12, C_13, C_23)

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
axs[0].plot(chi_1_plt, chi_1_plt*0, "-", color=colors[1], lw=0.5)
axs[0].plot(chi_1_plt, chi_1_plt*0+1, "-", color=colors[1], lw=0.5)
axs[0].plot(chi_1_plt, chi_1_plt*0+1/3, ":", color=colors[2], lw=1)#, label="Eigenvalue bound")
# ax.fill_between(chi_1_plt,0,1, color=colors[3], alpha=0.07)#, label="Eigenvalue range")
axs[0].fill_between(chi_1_plt,1,3, color="#fceeee")#, label="Eigenvalue range")
axs[0].fill_between(chi_1_plt,-3,0, color="#fceeee")
axs[1].plot(chi_2_plt, chi_2_plt*0, "-", color=colors[1], lw=0.5)
axs[1].plot(chi_2_plt, chi_2_plt*0+1, "-", color=colors[1], lw=0.5)
axs[1].plot(chi_2_plt, chi_2_plt*0+1/3, ":", color=colors[2], lw=1)#, label="Eigenvalue bound")
# ax.fill_between(chi_2_plt,0,1, color=colors[3], alpha=0.07)#, label="Eigenvalue range")
axs[1].fill_between(chi_2_plt,1,3, color="#fceeee")#, label="Eigenvalue range")
axs[1].fill_between(chi_2_plt,-3,0, color="#fceeee")
axs[2].plot(chi_1_plt, chi_3_plt*0, "-", color=colors[1], lw=0.5)
axs[2].plot(chi_3_plt, chi_3_plt*0+1, "-", color=colors[1], lw=0.5)
axs[2].plot(chi_3_plt, chi_3_plt*0+1/3, ":", color=colors[2], lw=1)#, label="Eigenvalue bound")
# ax.fill_between(chi_1_plt,0,1, color=colors[3], alpha=0.07)#, label="Eigenvalue range")
axs[2].fill_between(chi_1_plt,1,3, color="#fceeee")#, label="Eigenvalue range")
axs[2].fill_between(chi_1_plt,-3,0, color="#fceeee")

axs[0].errorbar(chi_1,Re_1, Re_1_err, fmt="k.", capsize=3, ms=4)
axs[0].plot(chi_1_plt, w1.real, color=colors[3], lw=1.5)
axs[1].errorbar(chi_2,Re_2, Re_2_err, fmt="k.", capsize=3, ms=4)
axs[1].plot(chi_2_plt, w2.real, color=colors[3], lw=1.5)
axs[2].errorbar(chi_3,Re_3, Re_3_err, fmt="k.", capsize=3, ms=4)
axs[2].plot(chi_3_plt, w3.real, color=colors[3], lw=1.5)

for ax in axs:
    ax.set_ylim([-0.25,1.1])
    ax.set_yticks([0, 0.5, 1])
    # ax.set_yticklabels([-0.4,0, 0.4])

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
axs1[0].plot(chi_1_plt, w1.imag, color=colors[3], lw=1.5)
axs1[1].errorbar(chi_2,Im_2, Im_2_err, fmt="k.", capsize=3, ms=4)
axs1[1].plot(chi_2_plt, w2.imag, color=colors[3], lw=1.5)
axs1[2].errorbar(chi_3,Im_3, Im_3_err, fmt="k.", capsize=3, ms=4)
axs1[2].plot(chi_3_plt, w3.imag, color=colors[3], lw=1.5)

for ax in axs1:
    # ax.set_ylim([-0.55,0.55])
    ax.set_yticks([-0.5,0, 0.5])
    ax.set_yticklabels([-0.5,0, 0.5])

# axs[1].text(-np.pi, 1.1,"Eigenvalue bound", color=colors[1])
# axs[1].text(-np.pi, 1.1,"Eigenvalue range", color=colors[3])
# axs[0].legend()

fig.savefig("/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/Report/Results/Results_"+(inf_file_names[0])[12:-17]+"_uncorrected.pdf",format='pdf', bbox_inches='tight', pad_inches=0, transparent=False)   

plt.show()