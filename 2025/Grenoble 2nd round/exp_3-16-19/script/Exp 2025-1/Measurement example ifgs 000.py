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

phi_1=0
phi_2=0
phi_3=0

phi=[phi_1,phi_2,phi_3]

colors=["k","#f10d0c","#00a933","#5983b0", "#D97A00", "#c32d9b",  "#006699"]
labels=[r"Intensity", r"Intensity", r"Intensity"]
def fit_cos(x, A, B):
    return A*(1+B*np.cos(x))/2

ifg_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/Report/Ifg example (000)/"
chi_aux=[0, np.pi/2, np.pi, 3*np.pi/2]
A_avg=0
Dchi=np.zeros(4)
C_avg=0
C_err=0
chi_1=np.array([])
chi_2=np.array([])
chi_3=np.array([])
I_1=np.array([])
I_2=np.array([])
I_3=np.array([]) 
I_1_err=np.array([])
I_2_err=np.array([])
I_3_err=np.array([]) 
for root, dirs, files in os.walk(ifg_fold_path, topdown=False):
    for name in (files[:]):
        tot_data=np.loadtxt(os.path.join(root, name))
        if "wv1" in name:
            print("wv1",name)
            chi_1=tot_data[:,0]
            I_1=tot_data[:,1]
            I_1_err=tot_data[:,2]
            chi_plt_1=np.linspace(chi_1[0],chi_1[-1],200)
        if "wv2" in name:
            print("wv2",name)
            chi_2=tot_data[:,0]
            I_2=tot_data[:,1]
            I_2_err=tot_data[:,2]
            chi_plt_2=np.linspace(chi_2[0],chi_2[-1],200)
        if "wv3" in name:
            print("wv3",name)
            chi_3=tot_data[:,0]
            I_3=tot_data[:,1]
            I_3_err=tot_data[:,2]
            chi_plt_3=np.linspace(chi_3[0],chi_3[-1],200)

chi=np.array([chi_1,chi_2,chi_3])
chi_plt=np.array([chi_plt_1,chi_plt_2,chi_plt_3])
I=np.array([I_1,I_2,I_3])
I_err=np.array([I_1_err,I_2_err,I_3_err])

fig = plt.figure(figsize=(7,4.5), dpi=350)
gs = fig.add_gridspec(3,1, hspace=0.8, wspace=0)
axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[1, 0]),fig.add_subplot(gs[2, 0])]

for i in [0,1,2]:
    chi_aux=chi[i]
    chi_plt_aux=chi_plt[i]
    I_aux=I[i]
    I_aux_err=I_err[i]
    axs[i].errorbar(chi_aux,I_aux,yerr=I_aux_err,fmt=".", color=colors[0],capsize=3, ms=4, label="Data")
    P0=[(np.amax(I[i])+np.amin(I[i]))/2, 0.7]
    B0=([np.amin(I_aux)/2,0.2],[np.amax(I_aux)*3, 1])
    p,cov=fit(fit_cos, chi_aux, I_aux, sigma=I_aux_err, p0=P0,  bounds=B0)
    if i==0:
        axs[0].errorbar(chi_aux[0],I_aux[0],fmt="o", color=colors[1], ms=10, mfc="none")
        axs[i].errorbar([chi_aux[0],chi_aux[4]],[50,50], fmt="-|", color=colors[0], lw=1)
        axs[0].vlines(chi_aux[0],I_aux[0]+15, 50, color=colors[1], linestyle="--", lw=1, clip_on=False)
        axs[0].errorbar(chi_aux[4],I_aux[4],fmt="o", color=colors[1], ms=10, mfc="none")
        axs[0].text((chi_aux[4]+chi_aux[0])/2, 60, "$\\frac{\\pi}{2}$", color=colors[0],  va="bottom", ha="center")
        axs[0].vlines(chi_aux[4], I_aux[4]+15, 50, color=colors[1], linestyle="--", lw=1, clip_on=False)
        
    err=np.diag(cov)**0.5
    axs[i].plot(chi_plt_aux,fit_cos(chi_plt_aux, *p), "-", color=colors[2], lw=1.5, label="Theory")
    axs[i].set_ylabel(labels[i]+"\n[counts s$^{-1}$]")

# axs[1].legend(framealpha=1, loc=1, ncol=1)
# axs[0].set_title(state) 
axs[0].set_xlabel("$\phi_1$")# [$\pi$]")
axs[1].set_xlabel("$\phi_2$")# [$\pi$]")
axs[2].set_xlabel("$\phi_3$")# [$\pi$]")
# axs[1].text(-0.13,0,"Intensity (count/s)",rotation=90, ha="center", va="center", transform=axs[1].transAxes)
i=0
yrange=axs[0].get_ylim()
print(yrange)
for ax in axs:
    ax.set_ylim(0,250)
    ax.yaxis.set_ticks([0,100, 200])
    ax.xaxis.set_major_locator(MultipleLocator(np.pi))
    ax.xaxis.set_major_formatter('{x:.2f}')
    
    # For the minor ticks, use no labels; default NullFormatter.
    ax.xaxis.set_minor_locator(MultipleLocator(np.pi/2))
    # ax.set_xticks(np.linspace(0, 6*np.pi, 18)+chi_auxs[(i+3)%3])
    x_labels_int=(ax.get_xticks()/np.pi).astype(int)
    x_labels=x_labels_int.astype(str)
    x_labels[x_labels_int==1]="$\pi$"
    x_labels[x_labels_int>1]+="$\pi$" 
    ax.set_xticklabels(x_labels)
    ax.grid(True, which="both", ls="dotted")
    # ax.set_yticks([150,350,550])
    # ax.set_facecolor("#fffff2")
    # ax.set_facecolor("#f0f8f3")
    ax.set_facecolor("#f7f7f7")
    i+=1



fig.savefig("/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/Paper/Images/Measurement example 000.pdf", format="pdf",bbox_inches="tight")   

plt.show()