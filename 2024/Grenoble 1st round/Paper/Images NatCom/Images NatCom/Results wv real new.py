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

def w1(chi, a_21):
    return 1/(1+a_21*np.exp(1j*chi))

def w2(chi, a_21):
    return 1-w1(chi, a_21)

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)


font_path = "/home/aaa/root/fonts/cmunrm.ttf"
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [prop.get_name(), "DejaVu Sans"]  # <- DejaVu als Fallback
plt.rcParams["font.size"] = 12
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["figure.dpi"] = 150
# plt.rcParams["legend.markerscale"] = 1
plt.rcParams["legend.fontsize"] = 11
plt.rcParams["axes.unicode_minus"] = False  # <- richtige Variante!

a_21_unb=0.588
a_21_bal=1
wv_1_unb=np.loadtxt("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Images NatCom/Images NatCom/Wv1_unb")
wv_1_bal=np.loadtxt("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Images NatCom/Images NatCom/Wv1_bal")
wv_2_unb=np.loadtxt("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Images NatCom/Images NatCom/Wv2_unb")
wv_2_bal=np.loadtxt("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Images NatCom/Images NatCom/Wv2_bal")

chi=wv_1_unb[:,0]
chi_plt=np.linspace(chi[0], chi[-1], 1000)
Re_1_unb=wv_1_unb[:,1]
Re_1_unb_err=wv_1_unb[:,2]
Re_2_unb=wv_2_unb[:,1]
Re_2_unb_err=wv_2_unb[:,2]

Re_1_bal=wv_1_bal[:,1]
Re_1_bal_err=wv_1_bal[:,2]
Re_2_bal=wv_2_bal[:,1]
Re_2_bal_err=wv_2_bal[:,2]

fig = plt.figure(figsize=(5,7), dpi=150)
gs_b = fig.add_gridspec(1,1)
ax_b=fig.add_subplot(gs_b[0, 0])
ax_b.tick_params(axis="both", bottom=False, labelbottom=False, left=False, labelleft=False)
gs = fig.add_gridspec(2,2 , height_ratios=(2,1), hspace=0.0, wspace=0.0)
axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[0, 1]),fig.add_subplot(gs[1, 0]),fig.add_subplot(gs[1, 1])]
# axs[0].set_title("$w_{1,+}$", fontsize=13)
# axs[1].set_title("$w_{2,+}$", fontsize=13)
axs[0].set_title("Path 1")
axs[1].set_title("Path 2")
ax_b.set_ylabel("Real part of the weak value $w^\mathrm{I}_{j,+}$", labelpad=25)
# axs[0].set_ylabel("Weak value\nReal part $w^\mathrm{R}_{j,+}$")
# axs[2].set_ylabel("Weak value\nReal part $w^\mathrm{R}_{j,+}$")
# fig.suptitle(inf_file_name)
colors=["k","#f10d0c","#00a933","#5983b0"]
plt.rcParams["mathtext.fontset"]="cm"
for ax in axs:
    ax.set_xticks([-np.pi,0,np.pi])
    ax.set_xticklabels(["${-\pi}$", "${0}$","${\pi}$"])
    ax.grid(True, ls="dotted")
for ax in axs[2:]:
    ax.set_xlabel("Initial relative phase\n$\phi$ [rad]")
axs[0].tick_params(axis="x", bottom=False, labelbottom=False)
axs[1].tick_params(axis="x", bottom=False, labelbottom=False)
axs[1].tick_params(axis="y", left=False, labelleft=False)
axs[3].tick_params(axis="y", left=False, labelleft=False)
    
for ax in axs:
    ax.plot(chi_plt, chi_plt*0, "-", color=colors[1], lw=1)
    ax.plot(chi_plt, chi_plt*0+1, "-", color=colors[1], lw=1)
    ax.plot(chi_plt, chi_plt*0+0.5, "--", color=colors[2], lw=1)#, label="Eigenvalue bound")
    # ax.fill_between(chi_plt,0,1, color=colors[2], alpha=0.07)#, label="Eigenvalue range")
    ax.fill_between(chi_plt,1,3, color="#fff2ff")#, label="Eigenvalue range")
    ax.fill_between(chi_plt,-3,0, color="#fff2ff")

# axs[0].fill_between(chi_plt, 1, w1(chi_plt, a_21_unb).real, where=w1(chi_plt, a_21_unb).real>1, color="#fff2ff")
# axs[1].fill_between(chi_plt,w2(chi_plt, a_21_unb).real, 0, where=w2(chi_plt, a_21_unb).real<0, color="#fff2ff")

axs[1].errorbar(chi,Re_2_unb, Re_2_unb_err, fmt="k.", capsize=3)
axs[1].plot(chi_plt, w2(chi_plt, a_21_unb).real, color=colors[3])
axs[3].errorbar(chi,Re_2_bal, Re_2_bal_err, fmt="k.", capsize=3)
axs[3].plot(chi_plt, w2(chi_plt, a_21_bal).real, color=colors[3])

axs[0].set_ylim([-1.7,2.7])
axs[1].set_ylim([-1.7,2.7])
axs[0].set_yticks([-1,0,0.5,1, 2])
axs[1].set_yticks([-1,0,0.5,1, 2])
axs[0].set_yticklabels([int(-1),0,0.5,1, 2])
# axs[1].set_ytickslabel([-1,0,0.5,1, 2])

axs[2].set_ylim([-0.25,1.75])
axs[3].set_ylim([-0.25,1.75])
axs[2].set_yticks([0,0.5,1])
axs[3].set_yticks([0,0.5,1])
axs[2].set_yticklabels([int(0),0.5,1])
axs[0].errorbar(chi_plt, w1(chi_plt, a_21_unb).real, color=colors[3])
axs[2].errorbar(chi_plt, w1(chi_plt, a_21_bal).real, color=colors[3])
axs[0].errorbar(chi,Re_1_unb, Re_1_unb_err, fmt="k.", capsize=3)
axs[2].errorbar(chi,Re_1_bal, Re_1_bal_err, fmt="k.", capsize=3)

# axs[1].text(-np.pi, 1.1,"Eigenvalue bound", color=colors[1])
# axs[1].text(-np.pi, 1.1,"Eigenvalue range", color=colors[2])
# axs[0].legend()
    
fig.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Images NatCom/Results wv real.pdf", format="pdf",bbox_inches="tight")   
plt.show()