# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:37:41 2023

@author: S18
"""
"""
inf_file_names:

"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
plt.rcParams.update({'figure.max_open_warning': 0})

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
wv_2_unb=np.loadtxt("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Images NatCom/Images NatCom/Wv2_unb")
wv_2_bal=np.loadtxt("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Images NatCom/Images NatCom/Wv2_bal")

chi=wv_2_unb[:,0]
chi_plt=np.linspace(chi[0], chi[-1], 1000)
Re_2_unb=wv_2_unb[:,1]
Re_2_unb_err=wv_2_unb[:,2]
Im_2_unb=wv_2_unb[:,3]
Im_2_unb_err=wv_2_unb[:,4]

Re_2_bal=wv_2_bal[:,1]
Re_2_bal_err=wv_2_bal[:,2]
Im_2_bal=wv_2_bal[:,3]
Im_2_bal_err=wv_2_bal[:,4]

fig = plt.figure(figsize=(5,10), dpi=150)
gs = fig.add_gridspec(2,2 , height_ratios=(1,2), hspace=0.0, wspace=0)
axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[0, 1]),fig.add_subplot(gs[1, 0]),fig.add_subplot(gs[1, 1])]
# axs[0].set_title("$w_{1,+}$", fontsize=13)
# axs[1].set_title("$w_{2,+}$", fontsize=13)
axs[0].set_title("Unbalanced")
axs[1].set_title("Balanced")
axs[0].set_ylabel("$w^\mathrm{R}_{2,+}$")
axs[2].set_ylabel("$w^\mathrm{I}_{2,+}$")
# fig.suptitle(inf_file_name)
colors=["k","#f10d0c","#00a933","#5983b0"]
plt.rcParams["mathtext.fontset"]="cm"
for ax in axs:
    ax.set_xticks([-np.pi,0,np.pi])
    ax.set_xticklabels(["${-\pi}$", "${0}$","${\pi}$"])
    ax.grid(True, ls="dotted")
for ax in axs[2:]:
    ax.set_xlabel("${\phi}$ [rad]")
axs[0].tick_params(axis="x", bottom=False, labelbottom=False)
axs[1].tick_params(axis="x", bottom=False, labelbottom=False)
axs[1].tick_params(axis="y", left=False, labelleft=False)
axs[3].tick_params(axis="y", left=False, labelleft=False)
    
axs[2].errorbar(chi,Im_2_unb, Im_2_unb_err, fmt="k.", capsize=3)
axs[2].plot(chi_plt, w2(chi_plt, a_21_unb).imag, color=colors[3], alpha=0.8 )
axs[3].errorbar(chi,Im_2_bal, Im_2_bal_err, fmt="k.", capsize=3)
axs[3].plot(chi_plt, w2(chi_plt, a_21_bal).imag, color=colors[3], alpha=0.8 )

axs[0].set_ylim([-1.7,1.7])
axs[1].set_ylim([-1.7,1.7])
axs[0].set_yticks([-1.5,-0.5, 0.5, 1.5])
axs[1].set_yticks([-1.5,-0.5, 0.5, 1.5])

axs[2].set_ylim([-5,2.6])
axs[3].set_ylim([-5,2.6])
axs[2].set_yticks((np.arange(-4,3,1)))
axs[3].set_yticks((np.arange(-4,3,1)))

axs[0].errorbar(chi_plt, w2(chi_plt, a_21_unb).real, color=colors[3], alpha=0.8)
axs[1].errorbar(chi_plt, w2(chi_plt, a_21_bal).real, color=colors[3], alpha=0.8)
axs[0].errorbar(chi,Re_2_unb, Re_2_unb_err, fmt="k.", capsize=3)
axs[1].errorbar(chi,Re_2_bal, Re_2_bal_err, fmt="k.", capsize=3)
fig.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Images NatCom/Results wv2.pdf", format="pdf",bbox_inches="tight")   
plt.show()