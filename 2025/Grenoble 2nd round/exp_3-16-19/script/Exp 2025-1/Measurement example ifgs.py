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
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
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

state=r"$|\psi_{0,-\frac{\pi}{2},-\pi}> \approx \frac{1}{\sqrt{3}}(|1>-\mathrm{i}|2>-|3>)$"

# Colors
colors = [
    "#D97A00",  # burnt orange
    "#c32d9b",  # magenta
    "#006699",  # TU blue
    "#2A9D8F",  # teal
    "#7A8F3A",  # olive green
    "#6A4C93"   # deep violet
]

chi_1_0=0
chi_2_0=-np.pi/2
chi_3_0=-np.pi

chi_0s=[chi_1_0,chi_2_0,chi_3_0]

colors=["k","#f10d0c","#00a933","#5983b0", "#D97A00", "#c32d9b",  "#006699"]
labels=[r"Intensity", r"Intensity", r"Intensity"]
def fit_cos(x, A, B, C):
    return A*(1+B*np.cos(x-C))/2

sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/Report/Ifg example/"
cleandata=sorted_fold_path+"/Cleantxt"
chi_0=[0, np.pi/2, np.pi, 3*np.pi/2]
i=0
A_avg=0
Dchi=np.zeros(4)
C_avg=0
C_err=0
fig = plt.figure(figsize=(8,5), dpi=350)
gs = fig.add_gridspec(3,1, hspace=0.8, wspace=0)
axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[1, 0]),fig.add_subplot(gs[2, 0])]
# fig = plt.figure(figsize=(5,6), dpi=150)
# gs = fig.add_gridspec(2,2, hspace=0.0, wspace=0)
# axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[0, 1]),fig.add_subplot(gs[1, 0]),fig.add_subplot(gs[1, 1])]
for root, dirs, files in os.walk(sorted_fold_path, topdown=False):
    files=np.sort(files)
    # I_0_matrix=np.zeros((4,points))
    # I_0_matrix=np.zeros((4,points))
    # print(files[::-1])
    for name in (files[:]):
        # print(name)
        tot_data=np.loadtxt(os.path.join(root, name))
        # print(time)
        chi=tot_data[:,0]
        # print(chi)
        chi_plt=np.linspace(chi[0],chi[-1],200)
        I_0=tot_data[:,1]
        I_0_err=tot_data[:,2]
        if i==0:
            chi_1=tot_data[:,0]
            chi_1_plt=np.linspace(chi[0],chi[-1],200)
            I_0_1=tot_data[:,1]
            I_mpi2_1=tot_data[:,3]
            I_ppi2_1=tot_data[:,5]
            I_pi_1=tot_data[:,7]
            I_0_1_err=tot_data[:,2]
            I_mpi2_1_err=tot_data[:,4]
            I_ppi2_1_err=tot_data[:,6]
            I_pi_1_err=tot_data[:,8]
            
        P0=[(np.amax(I_0)+np.amin(I_0))/2, 0.7, 0]
        B0=([np.amin(I_0)/2,0,-2*np.pi],[np.amax(I_0)*3,np.amax(I_0)*2, 2*np.pi])
        p,cov=fit(fit_cos, chi, I_0, sigma=I_0_err, p0=P0,  bounds=B0)
        if i==0:
            p1=p.copy()
            
            axs[0].errorbar(chi[0],I_0[0],fmt="o", color=colors[1], ms=10, mfc="none")
            axs[i].errorbar([chi[0],chi[4]],[100,100], fmt="-|", color=colors[0], lw=1)
            axs[0].vlines(chi[0],I_0[0]+15, 100, color=colors[1], linestyle="--", lw=1, clip_on=False)
            axs[0].errorbar(chi[4],I_0[4],fmt="o", color=colors[1], ms=10, mfc="none")
            axs[0].text((chi[4]-chi[0])/2, 105, "$\\frac{\\pi}{2}$", color=colors[0],  va="bottom", ha="center")
            axs[0].vlines(chi[4], I_0[4]+15, 100, color=colors[1], linestyle="--", lw=1, clip_on=False)
            
            # axs[0].errorbar(chi[0],I_0[0],fmt="o", color=colors[1], ms=10, mfc="none")
            # axs[0].text(chi[0],190, "$\\delta_1=0$", color=colors[1], va="bottom", ha="center")
            # axs[0].vlines(chi[0],I_0[0]+15, 190, color=colors[1], linestyle="-", lw=1, clip_on=False)
            
            # axs[0].errorbar(chi[4],I_0[4],fmt="o", color=colors[3], ms=10, mfc="none")
            # axs[0].text(chi[4], 230, "$\\delta_1=\\frac{\\pi}{2}$", color=colors[3],  va="bottom", ha="center")
            # axs[0].vlines(chi[4], I_0[4]+15, 230, color=colors[3], linestyle="-", lw=1, clip_on=False)
            
            # axs[0].errorbar(chi[8],I_0[8],fmt="o", color=colors[5], ms=10, mfc="none")
            # axs[0].text(chi[8], 190, "$\\delta_1=\\pi$", color=colors[5],  va="bottom", ha="center")
            # axs[0].vlines(chi[8], I_0[8]+15, 190, color=colors[5], linestyle="-", lw=1, clip_on=False)
            
            # axs[0].errorbar(chi[12],I_0[12],fmt="o", color=colors[4], ms=10, mfc="none")
            # axs[0].text(chi[12], 230, "$\\delta_1=-\\frac{\\pi}{2}$", color=colors[4],  va="bottom", ha="center")
            # axs[0].vlines(chi[12], I_0[12]+15, 230, color=colors[4], linestyle="-", lw=1, clip_on=False)
            
            # axs[0].text(chi[8],I_0[8], color=colors[3], ms=10, mfc="none")
            # axs[0].text(chi[12],I_0[12],color=colors[0], ms=10, mfc="none")
        # P0_unb=[100000, 3, -0.5, 0.7]
        # B0_unb=([0,1,-10, 0],[1e10,4,10,1])
        # p_unb,cov_unb=fit(fit_cos_unb, chi, I_0, p0=P0_unb,  bounds=B0_unb)
        err=np.diag(cov)**0.5
        axs[i].errorbar(chi,I_0,yerr=I_0_err,fmt=".", color=colors[0],capsize=3, ms=4, label="Data")
        axs[i].plot(chi_plt,fit_cos(chi_plt, *p), "-", color=colors[2], lw=1.5, label="Theory")
        axs[i].set_ylabel(labels[i]+"\n[counts s$^{-1}$]")
        i+=1

# axs[1].legend(framealpha=1, loc=1, ncol=1)
# axs[0].set_title(state) 
axs[0].set_xlabel("Initial relative phase $\phi_1$ [rad]")
axs[1].set_xlabel("Initial relative phase $\phi_2$ [rad]")
axs[2].set_xlabel("Initial relative phase $\phi_3$ [rad]")
# axs[1].text(-0.13,0,"Intensity (count/s)",rotation=90, ha="center", va="center", transform=axs[1].transAxes)
i=0
yrange=axs[0].get_ylim()
print(yrange)
for ax in axs:
    ax.set_ylim(0,180)
    ax.yaxis.set_ticks([50, 100, 150])
    ax.xaxis.set_major_locator(MultipleLocator(np.pi))
    ax.xaxis.set_major_formatter('{x:.2f}')
    
    # For the minor ticks, use no labels; default NullFormatter.
    ax.xaxis.set_minor_locator(MultipleLocator(np.pi/2))
    # ax.set_xticks(np.linspace(0, 6*np.pi, 18)+chi_0s[(i+3)%3])
    # ax.set_xticklabels("")#(["${-\pi}$", "${0}$","${\pi}$"])
    ax.grid(True, which="both", ls="dotted")
    # ax.set_yticks([150,350,550])
    # ax.set_facecolor("#fffff2")
    # ax.set_facecolor("#f0f8f3")
    ax.set_facecolor("#f7f7f7")
    i+=1

# axs[0].text("Initial relative phase $\phi_1$ [rad]")
# axs[0].tick_params(axis="x", bottom=False, labelbottom=False)
# axs[1].tick_params(axis="x", bottom=False, labelbottom=False)

# axs[i].set_ylabel("Neutron rate (count / s)")
# axs[i].set_ylim([0,430])

# I_phi=[I_0_1,I_0_1_err, I_ppi2_1, I_ppi2_1_err, I_pi_1, I_pi_1_err, I_mpi2_1, I_mpi2_1_err]

# fig1 = plt.figure(figsize=(6,4), dpi=350)
# gs1 = fig1.add_gridspec(4,1, hspace=0, wspace=0)
# axs1 = [fig1.add_subplot(gs1[0, 0]),fig1.add_subplot(gs1[1, 0]),fig1.add_subplot(gs1[2, 0]), fig1.add_subplot(gs1[3, 0])]

# i=0
# for ax1 in axs1:
#     ax1.errorbar(chi_1,I_phi[i],yerr=I_phi[i+1],fmt=".", color=colors[0],capsize=3, ms=4, label="Data")
#     ax1.plot(chi_1_plt,fit_cos(chi_1_plt+chi_1_0, *p1), "-", color=colors[2], lw=1.5, label="Theory")
#     i+=2
#     chi_1_0+=np.pi/2
#     ax1.set_ylim(yrange)
#     ax1.yaxis.set_ticks([50, 100, 150])
#     ax1.xaxis.set_major_locator(MultipleLocator(np.pi))
#     ax1.xaxis.set_major_formatter('{x:.2f}')
    
#     # For the minor ticks, use no labels; default NullFormatter.
#     ax1.xaxis.set_minor_locator(MultipleLocator(np.pi/2))
#     # ax.set_xticks(np.linspace(0, 6*np.pi, 18)+chi_0s[(i+3)%3])
#     # ax.set_xticklabels("")#(["${-\pi}$", "${0}$","${\pi}$"])
#     ax1.grid(True, which="both", ls="dotted")
#     # ax.set_yticks([150,350,550])
#     # ax.set_facecolor("#fffff2")
#     # ax.set_facecolor("#f0f8f3")
#     ax1.set_facecolor("#f7f7f7")
#     ax1.tick_params(axis="x", bottom=False, labelbottom=False)
# axs1[-1].tick_params(axis="x", bottom=True, labelbottom=True)
fig.savefig("/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/Report/Measurement example.pdf", format="pdf",bbox_inches="tight")   






plt.show()