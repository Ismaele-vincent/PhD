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
plt.rcParams["axes.titlesize"] = 12
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
print(len(chi))
chi_plt=np.linspace(chi[0], chi[-1], 1000)
Re_1_unb=wv_1_unb[:,1]
Re_1_unb_err=wv_1_unb[:,2]
Re_2_unb=wv_2_unb[:,1]
Re_2_unb_err=wv_2_unb[:,2]

Re_1_bal=wv_1_bal[:,1]
Re_1_bal_err=wv_1_bal[:,2]
Re_2_bal=wv_2_bal[:,1]
Re_2_bal_err=wv_2_bal[:,2]

fig = plt.figure(figsize=(4,7), dpi=150)
gs_b = fig.add_gridspec(1,1)
ax_b=fig.add_subplot(gs_b[0, 0])
ax_b.tick_params(axis="both", bottom=False, labelbottom=False, left=False, labelleft=False)
for side in ['right','left','top','bottom']:
    ax_b.spines[side].set_visible(False)

gs = fig.add_gridspec(2,2 , height_ratios=(2,1), hspace=0.03, wspace=0.0)
axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[0, 1]),fig.add_subplot(gs[1, 0]),fig.add_subplot(gs[1, 1])]
# axs[0].set_title("$w_{1,+}$", fontsize=13)
# axs[1].set_title("$w_{2,+}$", fontsize=13)
axs[0].set_title("Path 1")
axs[1].set_title("Path 2")
ax_b.set_ylabel("Real part of the weak value $w^\mathrm{R}_{j,+}$", labelpad=25)
# axs[1].yaxis.set_label_position("right")
# axs[1].set_ylabel("Unbalanced", rotation=-90, labelpad=15)
# axs[3].yaxis.set_label_position("right")
# axs[3].set_ylabel("Balanced", rotation=-90, labelpad=15)
# axs[0].set_ylabel("Weak value\nReal part $w^\mathrm{R}_{j,+}$")
# axs[2].set_ylabel("Weak value\nReal part $w^\mathrm{R}_{j,+}$")
axs[1].plot([1.07,1.07], [0,1], transform=axs[1].transAxes, lw=1.5, color="#cc00cc",clip_on=False)
axs[1].plot([1.07,1.07], [0.37,0.63], transform=axs[1].transAxes, lw=3., color='w', clip_on=False)
axs[1].text(1.07, 0.5, "Unbalanced", color="#cc00cc", ha="center", va="center", rotation=-90, transform=axs[1].transAxes)
axs[3].plot([1.07,1.07], [0,1], transform=axs[3].transAxes, lw=1.5, color="#e67e22",clip_on=False)
axs[3].plot([1.07,1.07], [0.30,0.7], transform=axs[3].transAxes, lw=3., color='w', clip_on=False)
axs[3].text(1.07, 0.5, "Balanced", color="#e67e22", ha="center", va="center", rotation=-90, transform=axs[3].transAxes)


# axs[1].text(1.1, 0.5, "Unbalanced", ha="center", va="center", transform=axs[1].transAxes)
# axs[2].text(0.25, 0.02, "Balanced", ha="center", va="center", transform=ax_b.transAxes)
# axs[3].text(0.75, 0.02, "Balanced", ha="center", va="center", transform=ax_b.transAxes)

# fig.suptitle(inf_file_name)
colors=["k","#f10d0c","#00a933","#5983b0", "#fffff2"]
plt.rcParams["mathtext.fontset"]="cm"
for ax in axs:
    ax.set_xticks([-np.pi,0,np.pi])
    ax.set_xticklabels(["${-\pi}$", "${0}$","${\pi}$"])
    ax.grid(True, ls="dotted")
for ax in axs[2:]:
    ax.set_xlabel("Initial relative\nphase $\phi$ [rad]")
axs[0].tick_params(axis="x", bottom=False, labelbottom=False)
axs[1].tick_params(axis="x", bottom=False, labelbottom=False)
axs[1].tick_params(axis="y", left=False, labelleft=False)
axs[3].tick_params(axis="y", left=False, labelleft=False)

for ax in axs:
    ax.plot(chi_plt, chi_plt*0, "-", color=colors[1], lw=0.5)
    ax.plot(chi_plt, chi_plt*0+1, "-", color=colors[1], lw=0.5)
    ax.plot(chi_plt, chi_plt*0+0.5, ":", color=colors[2], lw=1)#, label="Eigenvalue bound")
    # ax.fill_between(chi_plt,0,1, color=colors[3], alpha=0.07)#, label="Eigenvalue range")
    ax.fill_between(chi_plt,1,3, color="#fceeee")#, label="Eigenvalue range")
    ax.fill_between(chi_plt,-3,0, color="#fceeee")
    # ax.fill_between(chi_plt,1,np.amax(w1(chi_plt, a_21_unb).real), color="#fceeee")#, label="Eigenvalue range")
    # ax.fill_between(chi_plt,-3,0, color="#fff2ff")
    # ax.fill_between(chi_plt,1,np.amax(w1(chi_plt, a_21_unb).real), color="#fceeee")#, label="Eigenvalue range")
    # ax.fill_between(chi_plt,np.amin(w2(chi_plt, a_21_unb).real),0, color="#fceeee")
    ax.set_facecolor("#fffff2")
    # ax.set_facecolor("#f5f5f5")
# axs[0].fill_between(chi_plt, 1, w1(chi_plt, a_21_unb).real, where=w1(chi_plt, a_21_unb).real>1, color="#fff2ff")
# axs[1].fill_between(chi_plt,w2(chi_plt, a_21_unb).real, 0, where=w2(chi_plt, a_21_unb).real<0, color="#fceeee")
# for ax in axs[:2]:
#     ax.set_facecolor("#fffff2")
#     # ax.set_facecolor("#fafafa")
# for ax in axs[2:]:
#     # ax.set_facecolor("#fffff2")
#     ax.set_facecolor("#f7f7f7")

axs[1].errorbar(chi,Re_2_unb, Re_2_unb_err, fmt="k.", capsize=3, ms=4)
axs[1].plot(chi_plt, w2(chi_plt, a_21_unb).real, color=colors[3], lw=1.5)
axs[3].errorbar(chi,Re_2_bal, Re_2_bal_err, fmt="k.", capsize=3, ms=4)
axs[3].plot(chi_plt, w2(chi_plt, a_21_bal).real, color=colors[3], lw=1.5)

axs[0].set_ylim([-1.5,2.5])
axs[1].set_ylim([-1.5,2.5])
axs[0].set_yticks([-1,0,0.5,1, 2])
axs[1].set_yticks([-1,0,0.5,1, 2])
axs[0].set_yticklabels([int(-1),0,0.5,1, 2])
# axs[1].set_ytickslabel([-1,0,0.5,1, 2])

axs[2].set_ylim([-0.5,1.5])
axs[3].set_ylim([-0.5,1.5])
axs[2].set_yticks([0,0.5,1])
axs[3].set_yticks([0,0.5,1])
axs[2].set_yticklabels([int(0),0.5,1])
axs[0].plot(chi_plt, w1(chi_plt, a_21_unb).real, color=colors[3], lw=1.5)
axs[2].plot(chi_plt, w1(chi_plt, a_21_bal).real, color=colors[3], lw=1.5)
axs[0].errorbar(chi,Re_1_unb, Re_1_unb_err, fmt="k.", capsize=3, ms=4)
axs[2].errorbar(chi,Re_1_bal, Re_1_bal_err, fmt="k.", capsize=3, ms=4)

# axs[1].text(-np.pi, 1.1,"Eigenvalue bound", color=colors[1])
# axs[1].text(-np.pi, 1.1,"Eigenvalue range", color=colors[3])
# axs[0].legend()
    
fig.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Images NatCom/Results wv real.pdf", format="pdf",bbox_inches="tight")   
plt.show()