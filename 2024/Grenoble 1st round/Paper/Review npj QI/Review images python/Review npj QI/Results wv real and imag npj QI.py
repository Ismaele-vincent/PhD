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
import matplotlib.gridspec as GS
from matplotlib import font_manager
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
from matplotlib.patches import Rectangle
from matplotlib.patches import FancyArrowPatch
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
plt.rcParams["figure.dpi"] = 300
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

Re_1_unb=wv_1_unb[:,1]
Re_1_unb_err=wv_1_unb[:,2]
Re_2_unb=wv_2_unb[:,1]
Re_2_unb_err=wv_2_unb[:,2]

Re_1_bal=wv_1_bal[:,1]
Re_1_bal_err=wv_1_bal[:,2]
Re_2_bal=wv_2_bal[:,1]
Re_2_bal_err=wv_2_bal[:,2]

fig = plt.figure(figsize=(9,7), dpi=300)
fig.text(0.05, 0.9, "(a)", fontweight='bold')
fig.text(0.5, 0.9, "(b)", fontweight='bold')
gs_b = fig.add_gridspec(6,2, hspace=0.1, wspace=0.4)
axs_b_im=[fig.add_subplot(gs_b[:, 1]),fig.add_subplot(gs_b[:2, 1]),fig.add_subplot(gs_b[2:, 1])]
axs_b_re=[fig.add_subplot(gs_b[:, 0]),fig.add_subplot(gs_b[:4, 0]),fig.add_subplot(gs_b[4:, 0])]
for ax_b in axs_b_im:
    ax_b.tick_params(axis="both", bottom=False, labelbottom=False, left=False, labelleft=False)    
    for side in ['right','left','top','bottom']:
        ax_b.spines[side].set_visible(False)

for ax_b in axs_b_re:
    ax_b.tick_params(axis="both", bottom=False, labelbottom=False, left=False, labelleft=False)    
    for side in ['right','left','top','bottom']:
        ax_b.spines[side].set_visible(False)
    
gs = fig.add_gridspec(6,2 , wspace=0.4)
gs_im= GS.GridSpecFromSubplotSpec(6,2, hspace=0.1, wspace=0, subplot_spec=gs[:,1])
gs_re= GS.GridSpecFromSubplotSpec(6,2, hspace=0.1, wspace=0, subplot_spec=gs[:,0])
axs_im = [fig.add_subplot(gs_im[:2, 0]), fig.add_subplot(gs_im[:2, 1]),fig.add_subplot(gs_im[2:4, 0]),fig.add_subplot(gs_im[2:4, 1]),fig.add_subplot(gs_im[4:6, 0]),fig.add_subplot(gs_im[4:6, 1])]
axs_re = [fig.add_subplot(gs_re[:4, 0]), fig.add_subplot(gs_re[:4, 1]),fig.add_subplot(gs_re[4:, 0]),fig.add_subplot(gs_re[4:, 1])]

axs_im[0].set_title("Path 1")
axs_im[1].set_title("Path 2")
axs_b_im[0].set_ylabel("Imaginary part of the weak value $w^\mathrm{I}_{j,+}$", labelpad=25)

axs_b_im[1].plot([1.03,1.03], [0,1], transform=axs_b_im[1].transAxes, lw=1.5, color="#cc00cc",clip_on=False)
axs_b_im[1].plot([1.03,1.03], [0.25,0.75], transform=axs_b_im[1].transAxes, lw=3., color='w', clip_on=False)
axs_b_im[1].text(1.03, 0.5, "Unbalanced", color="#cc00cc", ha="center", va="center", rotation=-90, transform=axs_b_im[1].transAxes)
axs_b_im[2].plot([1.03,1.03], [0,1], transform=axs_b_im[2].transAxes, lw=1.5, color="#e67e22",clip_on=False)
axs_b_im[2].plot([1.03,1.03], [0.4,0.6], transform=axs_b_im[2].transAxes, lw=3., color='w', clip_on=False)
axs_b_im[2].text(1.03, 0.5, "Balanced", color="#e67e22", ha="center", va="center", rotation=-90, transform=axs_b_im[2].transAxes)
colors=["k","#f10d0c","#00a933","#5983b0"]
plt.rcParams["mathtext.fontset"]="cm"
for ax in [*axs_im]:
    ax.set_xticks([-np.pi,0,np.pi])
    ax.set_xticklabels(["${-\pi}$", "${0}$","${\pi}$"])
    ax.grid(True, ls="dotted")
    ax.set_facecolor("#fffff2")

    
# for ax in axs_im[:]:
#     ax.set_facecolor("#fffff2")
for ax in axs_im[-2:]:
    ax.set_xlabel("Initial relative\nphase $\phi$ [rad]")
    # ax.set_facecolor("#f7f7f7")
for ax in axs_im[:-2]:
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
axs_im[1].tick_params(axis="y", left=False, labelleft=False)
axs_im[3].tick_params(axis="y", left=False, labelleft=False)
axs_im[5].tick_params(axis="y", left=False, labelleft=False)
# axs_im[7].tick_params(axis="y", left=False, labelleft=False)

for ax in axs_im:
    ax.plot(chi_plt, chi_plt*0, ":", color=colors[2], lw=1)
axs_im[0].errorbar(chi_plt, w1(chi_plt, a_21_unb).imag, color=colors[3], lw=1.5)
axs_im[0].errorbar(chi,Im_1_unb, Im_1_unb_err, fmt="k.", capsize=3, ms=4)
axs_im[1].errorbar(chi,Im_2_unb, Im_2_unb_err, fmt="k.", capsize=3, ms=4)
axs_im[1].plot(chi_plt, w2(chi_plt, a_21_unb).imag, color=colors[3], lw=1.5)

for ax in axs_im[2::2]:
    ax.plot(chi_plt, w1(chi_plt, a_21_bal).imag, color=colors[3], lw=1.5)
    ax.errorbar(chi,Im_1_bal, Im_1_bal_err, fmt="k.", capsize=3, ms=4)
for ax in axs_im[3::2]:
    ax.errorbar(chi,Im_2_bal, Im_2_bal_err, fmt="k.", capsize=3, ms=4)
    ax.plot(chi_plt, w2(chi_plt, a_21_bal).imag, color=colors[3], lw=1.5)
    
axs_im[0].set_ylim([-1.25,1.25])
axs_im[1].set_ylim([-1.25,1.25])
axs_im[0].set_yticks([-1,0,1])
axs_im[1].set_yticks([-1,0,1])

for ax in axs_im[2:4]:
    # ax.spines["bottom"].set_visible(False)
    ax.set_ylim([-9,9])
    ax.set_yticks([-8,-4,0,4,8])
for ax in axs_im[4:6]:
    # ax.spines["top"].set_visible(False)
    # ax.spines["bottom"].set_visible(False)
    ax.set_ylim([-1.25,1.25])
    ax.set_yticks([-1,0,1])
    for side in ['right','left','top','bottom']:
        ax.spines[side].set_visible(False)
ax.spines["left"].set_visible(True)
color_inset="brown"
rect= Rectangle([axs_im[2].get_xlim()[0], -1.25], (axs_im[2].get_xlim()[1]-axs_im[2].get_xlim()[0])*2, 2.5, transform=axs_im[2].transData, edgecolor=color_inset, fc="none", ls="-", lw=1.5)
rect1= Rectangle([0, 0], 2, 1, transform=axs_im[4].transAxes, edgecolor=color_inset, fc="none", lw=1.5)
# line=Line2D([axs_im[2].get_xlim()[1], axs_im[2].get_xlim()[0]*0.995], [-1.35, -9.80], transform=axs_im[2].transData, lw=1, ls="-", color=color_inset)
# line1=Line2D([axs_im[3].get_xlim()[0], axs_im[3].get_xlim()[1]*0.995], [-1.35, -9.80], transform=axs_im[3].transData, lw=1,ls="-", color=color_inset)
line=Line2D([axs_im[2].get_xlim()[1], axs_im[2].get_xlim()[0]*0.995], [-1.35, -9.80], transform=axs_im[2].transData, lw=1.5, ls="-", color=color_inset)
line1=Line2D([axs_im[3].get_xlim()[0], axs_im[3].get_xlim()[1]*0.995], [-1.35, -9.80], transform=axs_im[3].transData, lw=1.5,ls="-", color=color_inset)
# line=Line2D([axs_im[2].get_xlim()[0], axs_im[2].get_xlim()[0]], [-1.35, -9.80], transform=axs_im[2].transData, lw=1.5, ls="-", color=color_inset)
# line1=Line2D([axs_im[3].get_xlim()[1], axs_im[3].get_xlim()[1]], [-1.35, -9.80], transform=axs_im[3].transData, lw=1.5,ls="-", color=color_inset)
fig.add_artist(rect)
fig.add_artist(rect1)
fig.add_artist(line)
fig.add_artist(line1)

axs_re[0].set_title("Path 1")
axs_re[1].set_title("Path 2")
axs_b_re[0].set_ylabel("Real part of the weak value $w^\mathrm{R}_{j,+}$", labelpad=25)
# axs_re[1].yaxis.set_label_position("right")
# axs_re[1].set_ylabel("Unbalanced", rotation=-90, labelpad=15)
# axs_re[3].yaxis.set_label_position("right")
# axs_re[3].set_ylabel("Balanced", rotation=-90, labelpad=15)
# axs_re[0].set_ylabel("Weak value\nReal part $w^\mathrm{R}_{j,+}$")
# axs_re[2].set_ylabel("Weak value\nReal part $w^\mathrm{R}_{j,+}$")
axs_b_re[1].plot([1.03,1.03], [0,1], transform=axs_b_re[1].transAxes, lw=1.5, color="#cc00cc",clip_on=False)
axs_b_re[1].plot([1.03,1.03], [0.375,0.625], transform=axs_b_re[1].transAxes, lw=3., color='w', clip_on=False)
axs_b_re[1].text(1.03, 0.5, "Unbalanced", color="#cc00cc", ha="center", va="center", rotation=-90, transform=axs_b_re[1].transAxes)
axs_b_re[2].plot([1.03,1.03], [0,1], transform=axs_b_re[2].transAxes, lw=1.5, color="#e67e22",clip_on=False)
axs_b_re[2].plot([1.03,1.03], [0.3,0.7], transform=axs_b_re[2].transAxes, lw=3., color='w', clip_on=False)
axs_b_re[2].text(1.03, 0.5, "Balanced", color="#e67e22", ha="center", va="center", rotation=-90, transform=axs_b_re[2].transAxes)

# axs_re[1].text(1.1, 0.5, "Unbalanced", ha="center", va="center", transform=axs_re[1].transAxes)
# axs_re[2].text(0.25, 0.02, "Balanced", ha="center", va="center", transform=axs_b_re[0].transAxes)
# axs_re[3].text(0.75, 0.02, "Balanced", ha="center", va="center", transform=axs_b_re[0].transAxes)

# fig.suptitle(inf_file_name)
colors=["k","#f10d0c","#00a933","#5983b0", "#fffff2"]
plt.rcParams["mathtext.fontset"]="cm"
for ax in axs_re:
    ax.set_xticks([-np.pi,0,np.pi])
    ax.set_xticklabels(["${-\pi}$", "${0}$","${\pi}$"])
    ax.grid(True, ls="dotted")
for ax in axs_re[2:]:
    ax.set_xlabel("Initial relative\nphase $\phi$ [rad]")
axs_re[0].tick_params(axis="x", bottom=False, labelbottom=False)
axs_re[1].tick_params(axis="x", bottom=False, labelbottom=False)
axs_re[1].tick_params(axis="y", left=False, labelleft=False)
axs_re[3].tick_params(axis="y", left=False, labelleft=False)

for ax in axs_re:
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
# axs_re[0].fill_between(chi_plt, 1, w1(chi_plt, a_21_unb).real, where=w1(chi_plt, a_21_unb).real>1, color="#fff2ff")
# axs_re[1].fill_between(chi_plt,w2(chi_plt, a_21_unb).real, 0, where=w2(chi_plt, a_21_unb).real<0, color="#fceeee")
# for ax in axs_re[:2]:
#     ax.set_facecolor("#fffff2")
#     # ax.set_facecolor("#fafafa")
# for ax in axs_re[2:]:
#     # ax.set_facecolor("#fffff2")
#     ax.set_facecolor("#f7f7f7")

axs_re[1].errorbar(chi,Re_2_unb, Re_2_unb_err, fmt="k.", capsize=3, ms=4)
axs_re[1].plot(chi_plt, w2(chi_plt, a_21_unb).real, color=colors[3], lw=1.5)
axs_re[3].errorbar(chi,Re_2_bal, Re_2_bal_err, fmt="k.", capsize=3, ms=4)
axs_re[3].plot(chi_plt, w2(chi_plt, a_21_bal).real, color=colors[3], lw=1.5)

axs_re[0].set_ylim([-1.5,2.5])
axs_re[1].set_ylim([-1.5,2.5])
axs_re[0].set_yticks([-1,0,0.5,1, 2])
axs_re[1].set_yticks([-1,0,0.5,1, 2])
axs_re[0].set_yticklabels([int(-1),0,0.5,1, 2])
# axs_re[1].set_ytickslabel([-1,0,0.5,1, 2])

axs_re[2].set_ylim([-0.5,1.5])
axs_re[3].set_ylim([-0.5,1.5])
axs_re[2].set_yticks([0,0.5,1])
axs_re[3].set_yticks([0,0.5,1])
axs_re[2].set_yticklabels([int(0),0.5,1])
axs_re[0].plot(chi_plt, w1(chi_plt, a_21_unb).real, color=colors[3], lw=1.5)
axs_re[2].plot(chi_plt, w1(chi_plt, a_21_bal).real, color=colors[3], lw=1.5)
axs_re[0].errorbar(chi,Re_1_unb, Re_1_unb_err, fmt="k.", capsize=3, ms=4)
axs_re[2].errorbar(chi,Re_1_bal, Re_1_bal_err, fmt="k.", capsize=3, ms=4)

fig.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Review npj QI/Figure5.pdf", format="pdf",bbox_inches="tight")   
plt.show()