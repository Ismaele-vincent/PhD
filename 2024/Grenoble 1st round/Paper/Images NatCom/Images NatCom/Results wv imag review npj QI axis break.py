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
chi_plt=np.linspace(chi[0], chi[-1], 1000)
Im_1_unb=wv_1_unb[:,3]
Im_1_unb_err=wv_1_unb[:,4]
Im_2_unb=wv_2_unb[:,3]
Im_2_unb_err=wv_2_unb[:,4]

Im_1_bal=wv_1_bal[:,3]
Im_1_bal_err=wv_1_bal[:,4]
Im_2_bal=wv_2_bal[:,3]
Im_2_bal_err=wv_2_bal[:,4]

fig = plt.figure(figsize=(4,7), dpi=150)
gs_b = fig.add_gridspec(6,2 , hspace=0.1, wspace=0.0)
axs_b=[fig.add_subplot(gs_b[:, :]),fig.add_subplot(gs_b[:2, :]),fig.add_subplot(gs_b[2:, :])]

for ax_b in axs_b:
    ax_b.tick_params(axis="both", bottom=False, labelbottom=False, left=False, labelleft=False)    
    for side in ['right','left','top','bottom']:
        ax_b.spines[side].set_visible(False)
    
gs = fig.add_gridspec(6,2 , hspace=0.1, wspace=0.0)
axs = [fig.add_subplot(gs[:2, 0]), fig.add_subplot(gs[:2, 1]),fig.add_subplot(gs[2, 0]),fig.add_subplot(gs[2, 1]),fig.add_subplot(gs[3:5, 0]),fig.add_subplot(gs[3:5, 1]),fig.add_subplot(gs[5, 0]),fig.add_subplot(gs[5, 1])]

axs[0].set_title("Path 1")
axs[1].set_title("Path 2")
axs_b[0].set_ylabel("Imaginary part of the weak value $w^\mathrm{I}_{j,+}$", labelpad=25)

axs_b[1].plot([1.03,1.03], [0,1], transform=axs_b[1].transAxes, lw=1.5, color="#cc00cc",clip_on=False)
axs_b[1].plot([1.03,1.03], [0.25,0.75], transform=axs_b[1].transAxes, lw=3., color='w', clip_on=False)
axs_b[1].text(1.03, 0.5, "Unbalanced", color="#cc00cc", ha="center", va="center", rotation=-90, transform=axs_b[1].transAxes)
axs_b[2].plot([1.03,1.03], [0,1], transform=axs_b[2].transAxes, lw=1.5, color="#e67e22",clip_on=False)
axs_b[2].plot([1.03,1.03], [0.4,0.6], transform=axs_b[2].transAxes, lw=3., color='w', clip_on=False)
axs_b[2].text(1.03, 0.5, "Balanced", color="#e67e22", ha="center", va="center", rotation=-90, transform=axs_b[2].transAxes)

colors=["k","#f10d0c","#00a933","#5983b0"]
plt.rcParams["mathtext.fontset"]="cm"
for ax in [*axs]:
    ax.set_xticks([-np.pi,0,np.pi])
    ax.set_xticklabels(["${-\pi}$", "${0}$","${\pi}$"])
    ax.grid(True, ls="dotted")
    ax.set_facecolor("#fffff2")

    
# for ax in axs[:]:
#     ax.set_facecolor("#fffff2")
for ax in axs[-2:]:
    ax.set_xlabel("Initial relative\nphase $\phi$ [rad]")
    # ax.set_facecolor("#f7f7f7")
for ax in axs[:-2]:
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
axs[1].tick_params(axis="y", left=False, labelleft=False)
axs[3].tick_params(axis="y", left=False, labelleft=False)
axs[5].tick_params(axis="y", left=False, labelleft=False)
axs[7].tick_params(axis="y", left=False, labelleft=False)

for ax in axs:
    ax.plot(chi_plt, chi_plt*0, ":", color=colors[2], lw=1)
axs[0].errorbar(chi_plt, w1(chi_plt, a_21_unb).imag, color=colors[3], lw=1.5)
axs[0].errorbar(chi,Im_1_unb, Im_1_unb_err, fmt="k.", capsize=3, ms=4)
axs[1].errorbar(chi,Im_2_unb, Im_2_unb_err, fmt="k.", capsize=3, ms=4)
axs[1].plot(chi_plt, w2(chi_plt, a_21_unb).imag, color=colors[3], lw=1.5)

for ax in axs[2::2]:
    ax.plot(chi_plt, w1(chi_plt, a_21_bal).imag, color=colors[3], lw=1.5)
    ax.errorbar(chi,Im_1_bal, Im_1_bal_err, fmt="k.", capsize=3, ms=4)
for ax in axs[3::2]:
    ax.errorbar(chi,Im_2_bal, Im_2_bal_err, fmt="k.", capsize=3, ms=4)
    ax.plot(chi_plt, w2(chi_plt, a_21_bal).imag, color=colors[3], lw=1.5)

axs[0].set_ylim([-1.5,1.5])
axs[1].set_ylim([-1.5,1.5])
axs[0].set_yticks([-1,0,1])
axs[1].set_yticks([-1,0,1])

for ax in axs[2:4]:
    ax.spines["bottom"].set_visible(False)
    ax.set_ylim([1.5,9])
    ax.set_yticks([3,5,7])
for ax in axs[4:6]:
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_ylim([-1.5,1.5])
    ax.set_yticks([-1,0,1])
for ax in axs[6:8]:
    ax.spines["top"].set_visible(False)
    ax.set_ylim([-9,-1.5])
    ax.set_yticks([-7,-5,-3])   
h=0.03
for ax in axs[2:4]:
    ax.plot([-h,h], [h,-h], transform=ax.transAxes, lw=1, color="k",clip_on=False)
ax.plot([1-h,1+h], [h,-h], transform=ax.transAxes, lw=1, color="k",clip_on=False)
for ax in axs[4:6]:
    ax.plot([-h,h], [h/2,-h/2], transform=ax.transAxes, lw=1, color="k",clip_on=False)
    ax.plot([-h,h], [1+h/2,1-h/2], transform=ax.transAxes, lw=1, color="k",clip_on=False)
ax.plot([1-h,1+h], [h/2,-h/2], transform=ax.transAxes, lw=1, color="k",clip_on=False)
ax.plot([1-h,1+h], [1+h/2,1-h/2], transform=ax.transAxes, lw=1, color="k",clip_on=False)
for ax in axs[6:8]:
    ax.plot([-h,h], [1+h,1-h], transform=ax.transAxes, lw=1, color="k",clip_on=False)
ax.plot([1-h,1+h], [1+h,1-h], transform=ax.transAxes, lw=1, color="k",clip_on=False)

print(len(Im_1_bal))
    # ax.plot([0.95,1.05], [0.05,-0.05], transform=ax.transAxes, lw=1, color="k",clip_on=False)
# for ax in axs[[2,3,6,7]]:
#     axs[2].set_ylim([4,7])
#     axs[3].set_ylim([-5,5])
#     axs[2].set_yticks([-4,-2,0,2,4])
# axs[2].set_ylim([-5,5])
# axs[3].set_ylim([-5,5])
# axs[2].set_yticks([-4,-2,0,2,4])
# axs[3].set_yticks(range(-5,5,2))


# fig.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Images NatCom/Results wv imag.pdf", format="pdf",bbox_inches="tight")   
plt.show()