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
import My_module_Exp_2025_1 as mymod
import matplotlib.transforms as mtransforms

def fit_cos(x, A, B, C, D):
    return A*(1+B*np.cos(C*x-D))/2

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
vec_phi=r"$\vec\phi=(\pi,0,0)$"
colors=["k","#f10d0c","#00a933","#5983b0", "#D97A00", "#c32d9b",  "#006699"]


phi_1_0=np.pi
phi_2_0=0
phi_3_0=0

phi_0=np.array([phi_1_0,phi_2_0,phi_3_0])
N=21

ifg_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/Report/Ifg example (0pipi)/"
inf_file_names=["ifg_wv1_psi_+1-1-1_no_fit_23Oct0152", "ifg_wv2_psi_+1-1-1_no_fit_23Oct0229","ifg_wv3_psi_+1-1-1_no_fit_23Oct0305"]
C_12, C_13, C_23 = mymod.contrast(inf_file_names[0]) 
# print("C_12=", C_12, "C_13=", C_13, "C_23=", C_23)

fold_results="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Ifg wv no fit/Results Corrected/"

phi_1=np.array([])
phi_2=np.array([])
phi_3=np.array([])
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
            # print("wv1",name)
            phi_1=tot_data[:N,0]
            I_1=tot_data[:N,1]
            I_1_err=tot_data[:N,2]
            phi_1_plt=np.linspace(phi_1[0],phi_1[-1],200)
        if "wv2" in name:
            # print("wv2",name)
            phi_2=tot_data[:N,0]
            I_2=tot_data[:N,1]
            I_2_err=tot_data[:N,2]
            phi_2_plt=np.linspace(phi_2[0],phi_2[-1],200)
        if "wv3" in name:
            # print("wv3",name)
            phi_3=tot_data[:N,0]
            I_3=tot_data[:N,1]
            I_3_err=tot_data[:N,2]
            phi_3_plt=np.linspace(phi_3[0],phi_3[-1],200)

phi=np.array([phi_1,phi_2,phi_3])
phi_plt=np.array([phi_1_plt,phi_2_plt,phi_3_plt])
I=np.array([I_1,I_2,I_3])
I_err=np.array([I_1_err,I_2_err,I_3_err])

fig = plt.figure(figsize=(8.27, 6), dpi=350)
gs = fig.add_gridspec(3,3, hspace=0.1, wspace=0.1)
axs_ifg = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[0, 1]),fig.add_subplot(gs[0, 2])]

for i in [0,1,2]:
    phi_aux=np.arange(N)*np.pi/8 
    phi_plt_aux=np.linspace(0, (N-1)*np.pi/8,200)
    I_aux=I[i]
    I_aux_err=I_err[i]
    
    P0=[(np.amax(I[i])+np.amin(I[i]))/2, 0.7,1,np.pi]
    B0=([np.amin(I_aux)/2,0,0.8,-2*np.pi],[np.amax(I_aux)*3, 1, 1.2, 2*np.pi])
    p,cov=fit(fit_cos, phi_aux, I_aux, sigma=I_aux_err, p0=P0,  bounds=B0)
    # if i==0:
    #     axs_ifg[0].errorbar(phi_aux[4],I_aux[4],fmt="o", color=colors[1], ms=10, mfc="none")
    #     axs_ifg[0].errorbar([phi_aux[4],phi_aux[8]],[200,200], fmt="-|", color=colors[0], lw=1)
    #     axs_ifg[0].vlines(phi_aux[4],I_aux[4]+15, 200, color=colors[1], linestyle="--", lw=1, clip_on=False)
    #     axs_ifg[0].errorbar(phi_aux[8],I_aux[8],fmt="o", color=colors[1], ms=10, mfc="none")
    #     axs_ifg[0].text((phi_aux[8]+phi_aux[4])/2, 205, "$\\frac{\\pi}{2}$", color=colors[0],  va="bottom", ha="center")
    #     axs_ifg[0].vlines(phi_aux[8], I_aux[8]+15, 200, color=colors[1], linestyle="--", lw=1, clip_on=False)
    # phi[i]=phi_0[i]+np.arange(N)*np.pi/8    
    err=np.diag(cov)**0.5
    phi[i]=phi_0[i]+phi_aux*p[2]
    phi_plt[i]=phi_0[i]+phi_plt_aux*p[2]
    # axs_ifg[i].errorbar(phi_aux[0],I_aux[0],fmt="o", color=colors[4], ms=10, mfc="none")
    axs_ifg[i].errorbar(phi[i],I_aux,yerr=I_aux_err,fmt=".", color=colors[0],capsize=3, ms=4, label="Data")
    # axs_ifg[i].plot(phi_plt[i],fit_cos(phi_plt_aux, *p), "-", color=colors[2], lw=1.5, label="Theory")
    axs_ifg[i].errorbar(phi[i][0],I_aux[0],I_aux_err[0],fmt=".", color=colors[4],capsize=3, ms=4)
axs_ifg[0].set_ylabel("Intensity\n[counts s$^{-1}$]")

phi_1=phi[0]
phi_2=phi[1]
phi_3=phi[2]

phi_1_plt=phi_plt[0]
phi_2_plt=phi_plt[1]
phi_3_plt=phi_plt[2]

I_vec_1 = np.loadtxt(fold_results+inf_file_names[0]+"_Ij.txt")
I_vec_2 = np.loadtxt(fold_results+inf_file_names[1]+"_Ij.txt")
I_vec_3 = np.loadtxt(fold_results+inf_file_names[2]+"_Ij.txt")
I_plt=np.array([I_vec_1, I_vec_2, I_vec_3])
I_theory_1=mymod.I_corr(np.sum(I_plt[0])*3, *(I_plt[0]/np.sum(I_plt[0]))**0.5, phi_1_plt, 0, 0, phi_2_0, 0, phi_3_0, C_12, C_13, C_23)
I_theory_2=mymod.I_corr(np.sum(I_plt[1])*3, *(I_plt[1]/np.sum(I_plt[1]))**0.5, 0, phi_1_0, phi_2_plt, 0, 0, phi_3_0, C_12, C_13, C_23)
I_theory_3=mymod.I_corr(np.sum(I_plt[2])*3, *(I_plt[2]/np.sum(I_plt[2]))**0.5, 0, phi_1_0, 0, phi_2_0, phi_3_plt, 0, C_12, C_13, C_23)
I_theory=np.array([I_theory_1, I_theory_2, I_theory_3])
for i in [0,1,2]:
    axs_ifg[i].plot(phi_plt[i],I_theory[i], "-", color=colors[2], lw=1.5, label="Theory")

i=0
xrange=axs_ifg[0].get_xlim()
# print(yrange)
for ax in axs_ifg:
    ax.set_ylim(0,270)
    ax.xaxis.set_major_locator(MultipleLocator(np.pi))
    ax.xaxis.set_major_formatter('{x:.2f}')
    ax.xaxis.set_minor_locator(MultipleLocator(np.pi/2))
    ax.yaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_minor_locator(MultipleLocator(50))
    ax.tick_params(axis="x", which='both', bottom=False, labelbottom=False)
    x_labels_int=(ax.get_xticks()/np.pi).astype(int)
    ax.grid(True, which="both", ls="dotted")
    ax.set_facecolor("#f7f7f7")
    trans = mtransforms.blended_transform_factory(ax.transData,  ax.transAxes)
    ax.annotate("", xy=(phi_0[i], 0), xytext=(phi_0[i],1), xycoords=ax.get_xaxis_transform(), textcoords=ax.get_xaxis_transform(), ha="center", va="center", color=colors[4], arrowprops=dict(arrowstyle="-", linestyle=":",color=colors[4], lw=1, clip_on=False, shrinkA=0, shrinkB=0))
    # ax.arrow("", xy=(phi_0[i], axs_ifg[0].get_ylim()), xytext=(phi_0[i],-0.45), xycoords=ax.get_xaxis_transform(), textcoords=ax.get_xaxis_transform(), ha="center", va="center", arrowprops=dict(arrowstyle="->", color=colors[5], lw=1, clip_on=False, shrinkA=0, shrinkB=0))
    i+=1
# ax.text(x_text, y_text, "Label", transform=trans, ha="center", va="center", bbox=dict(facecolor="white", edgecolor="none", pad=2), clip_on=False)
# axs_ifg[1].annotate(vec_phi, xy=(phi_0[0], -0.45), xytext=(phi_0[0]-0.5,-0.45), xycoords=axs_ifg[2].get_xaxis_transform(), textcoords=axs_ifg[0].get_xaxis_transform(), ha="right", va="center", bbox=dict(facecolor="white", edgecolor="none", pad=2), arrowprops=dict(arrowstyle="-", color=colors[5], lw=1, clip_on=False, shrinkA=0, shrinkB=0))
axs_ifg[1].tick_params(axis="y", left=False, labelleft=False)
axs_ifg[2].tick_params(axis="y", left=False, labelleft=False)
axs_ifg[0].set_title("Path 1")
axs_ifg[1].set_title("Path 2")
axs_ifg[2].set_title("Path 3")

wv_1=np.loadtxt(fold_results+inf_file_names[0]+".txt")[:N,:]
wv_2=np.loadtxt(fold_results+inf_file_names[1]+".txt")[:N,:]
wv_3=np.loadtxt(fold_results+inf_file_names[2]+".txt")[:N,:]
# a_vec_1 = np.loadtxt(fold_results+inf_file_names[0]+"_int.txt")
# a_vec_2 = np.loadtxt(fold_results+inf_file_names[1]+"_int.txt")
# a_vec_3 = np.loadtxt(fold_results+inf_file_names[2]+"_int.txt")
a_vec_1 = [1/3**0.5, 1/3**0.5, 1/3**0.5]
a_vec_2 = [1/3**0.5, 1/3**0.5, 1/3**0.5]
a_vec_3 = [1/3**0.5, 1/3**0.5, 1/3**0.5]

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

w1=mymod.w1(*a_vec_1,  phi_1_plt, 0, 0, phi_2_0, 0, phi_3_0, 1, 1, 1)
w2=mymod.w2(*a_vec_2,  0, phi_1_0, phi_2_plt, 0, 0, phi_3_0, 1, 1, 1)
w3=mymod.w3(*a_vec_3,  0, phi_1_0, 0, phi_2_0, phi_3_plt, 0, 1, 1, 1)

axs_re = [fig.add_subplot(gs[1, 0]),fig.add_subplot(gs[1, 1]),fig.add_subplot(gs[1, 2])]
axs_im = [fig.add_subplot(gs[2, 0]),fig.add_subplot(gs[2, 1]),fig.add_subplot(gs[2, 2])]

axs_re[0].set_ylabel("Real part of\nthe weak value")
i=0
for ax in axs_re:
    ax.xaxis.set_major_locator(MultipleLocator(np.pi))
    ax.xaxis.set_major_formatter('{x:.2f}')
    ax.xaxis.set_minor_locator(MultipleLocator(np.pi/2))
    ax.grid(True, which="both", ls="dotted")
    ax.set_facecolor("#fffff2")
    ax.tick_params(axis="x", which='both', bottom=False, labelbottom=False)
    ax.grid(True, ls="dotted")
    ax.set_ylim([-1.2,1.2])
    ax.set_xlim(axs_ifg[i].get_xlim())
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_minor_locator(MultipleLocator(0.5))
    ax.annotate("", xy=(phi_0[i], 0), xytext=(phi_0[i],1), xycoords=ax.get_xaxis_transform(), textcoords=ax.get_xaxis_transform(), ha="center", va="center", color=colors[4], arrowprops=dict(arrowstyle="-", linestyle=":",color=colors[4], lw=1, clip_on=False, shrinkA=0, shrinkB=0))
    # ax.yaxis.set_minor_formatter('{x:.1f}')
    i+=1
axs_re[1].tick_params(axis="y", which='both', left=False, labelleft=False)
axs_re[2].tick_params(axis="y", which='both', left=False, labelleft=False)
for ax in axs_re:
    ax.plot(ax.get_xlim(), [0,0], "-", color=colors[1], lw=0.5)
    ax.plot(ax.get_xlim(), [1,1], "-", color=colors[1], lw=0.5)
    ax.plot(ax.get_xlim(), [1/3,1/3], ":", color=colors[2], lw=1)
    ax.fill_between(ax.get_xlim(),1,ax.get_ylim()[1], color="#fceeee")#, label="Eigenvalue range")
    ax.fill_between(ax.get_xlim(),ax.get_ylim()[0],0, color="#fceeee")

axs_re[0].errorbar(phi_1,Re_1, Re_1_err, fmt="k.", capsize=3, ms=4)
axs_re[0].plot(phi_1_plt, w1.real, color=colors[3], lw=1.5)
axs_re[1].errorbar(phi_2,Re_2, Re_2_err, fmt="k.", capsize=3, ms=4)
axs_re[1].plot(phi_2_plt, w2.real, color=colors[3], lw=1.5)
axs_re[2].errorbar(phi_3,Re_3, Re_3_err, fmt="k.", capsize=3, ms=4)
axs_re[2].plot(phi_3_plt, w3.real, color=colors[3], lw=1.5)

# axs_re[0].errorbar(phi_1[0],Re_1[0],fmt="o", color=colors[4], ms=10, mfc="none")
# axs_re[1].errorbar(phi_2[0],Re_2[0],fmt="o", color=colors[4], ms=10, mfc="none")
# axs_re[2].errorbar(phi_3[0],Re_3[0],fmt="o", color=colors[4], ms=10, mfc="none")

axs_re[0].errorbar(phi_1[0],Re_1[0], Re_1_err[0], fmt=".", color=colors[4],capsize=3, ms=4)
axs_re[1].errorbar(phi_2[0],Re_2[0], Re_2_err[0], fmt=".", color=colors[4],capsize=3, ms=4)
axs_re[2].errorbar(phi_3[0],Re_3[0], Re_3_err[0], fmt=".", color=colors[4],capsize=3, ms=4)

axs_im[0].set_ylabel("Imaginary part of\nthe weak value")

axs_im[0].set_xlabel("$\phi_1$ [rad]")
axs_im[1].set_xlabel("$\phi_2$ [rad]")
axs_im[2].set_xlabel("$\phi_3$ [rad]")
axs_im[1].tick_params(axis="y", which='both', left=False, labelleft=False)
axs_im[2].tick_params(axis="y", which='both', left=False, labelleft=False)

axs_im[0].errorbar(phi_1,Im_1, Im_1_err, fmt="k.", capsize=3, ms=4)
axs_im[0].plot(phi_1_plt, w1.imag, color=colors[3], lw=1.5)
axs_im[1].errorbar(phi_2,Im_2, Im_2_err, fmt="k.", capsize=3, ms=4)
axs_im[1].plot(phi_2_plt, w2.imag, color=colors[3], lw=1.5)
axs_im[2].errorbar(phi_3,Im_3, Im_3_err, fmt="k.", capsize=3, ms=4)
axs_im[2].plot(phi_3_plt, w3.imag, color=colors[3], lw=1.5)

# axs_im[0].errorbar(phi_1[0],Im_1[0],fmt="o", color=colors[4], ms=10, mfc="none")
# axs_im[1].errorbar(phi_2[0],Im_2[0],fmt="o", color=colors[4], ms=10, mfc="none")
# axs_im[2].errorbar(phi_3[0],Im_3[0],fmt="o", color=colors[4], ms=10, mfc="none")

axs_im[0].errorbar(phi_1[0],Im_1[0], Im_1_err[0], fmt=".", color=colors[4],capsize=3, ms=4)
axs_im[1].errorbar(phi_2[0],Im_2[0], Im_2_err[0], fmt=".", color=colors[4],capsize=3, ms=4)
axs_im[2].errorbar(phi_3[0],Im_3[0], Im_3_err[0], fmt=".", color=colors[4],capsize=3, ms=4)

i=0
for ax in axs_im:
    ax.xaxis.set_major_locator(MultipleLocator(np.pi))
    ax.xaxis.set_major_formatter('{x:.2f}')
    ax.xaxis.set_minor_locator(MultipleLocator(np.pi/2))
    x_labels_int=(ax.get_xticks()/np.pi).astype(int)
    x_labels=x_labels_int.astype(str)
    x_labels[x_labels_int==1]="$\pi$"
    x_labels[x_labels_int==-1]="-$\pi$"
    x_labels[abs(x_labels_int)>1]+="$\pi$" 
    ax.set_xticklabels(x_labels)
    ax.grid(True, which="both", ls="dotted")
    ax.set_facecolor("#fffff2")
    ax.set_ylim([-1,1])
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_minor_locator(MultipleLocator(0.5))
    # ax.yaxis.set_minor_formatter('{x:.1f}')
    # ax.annotate("", xy=(phi_0[i], 0), xytext=(phi_0[i],3.45), xycoords=ax.get_xaxis_transform(), textcoords=ax.get_xaxis_transform(), ha="center", va="center", color=colors[4], arrowprops=dict(arrowstyle="-", linestyle=":",color=colors[4], lw=1, clip_on=False, shrinkA=0, shrinkB=0))
    # ax.annotate("", xy=(phi_0[i], 0), xytext=(phi_0[i],3.45), xycoords=ax.get_xaxis_transform(), textcoords=ax.get_xaxis_transform(), ha="center", va="center", color=colors[4], arrowprops=dict(arrowstyle="-", linestyle=":",color=colors[4], lw=1, clip_on=False, shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(phi_0[i], 0), xytext=(phi_0[i],1), xycoords=ax.get_xaxis_transform(), textcoords=ax.get_xaxis_transform(), ha="center", va="center", color=colors[4], arrowprops=dict(arrowstyle="-", linestyle=":",color=colors[4], lw=1, clip_on=False, shrinkA=0, shrinkB=0))
    # ax.annotate("", xy=(phi_0[i], -0.18), xytext=(phi_0[i],-0.45), xycoords=ax.get_xaxis_transform(), textcoords=ax.get_xaxis_transform(), ha="center", va="center", arrowprops=dict(arrowstyle="->", color=colors[5], lw=1, clip_on=False, shrinkA=0, shrinkB=0))
    i+=1
    
# axs_im[0].annotate("", xy=(phi_0[2], 3.45), xytext=(phi_0[0],3.45), xycoords=axs_im[2].get_xaxis_transform(), textcoords=axs_im[0].get_xaxis_transform(), ha="center", va="center", color=colors[4], bbox=dict(facecolor="white", edgecolor="none", pad=2), arrowprops=dict(arrowstyle="-", linestyle=":",color=colors[4], lw=1, clip_on=False, shrinkA=0, shrinkB=0))
# axs_im[2].annotate(vec_phi, xy=(phi_0[2], 3.45), xytext=(phi_0[1],3.45), xycoords=axs_im[2].get_xaxis_transform(), textcoords=axs_im[1].get_xaxis_transform(), ha="center", va="center", color=colors[4], bbox=dict(facecolor="white", edgecolor="none", pad=2))
# axs_im[0].annotate(vec_phi, xy=(phi_0[0], 3.45), xytext=(phi_0[0],3.45), xycoords=axs_im[2].get_xaxis_transform(), textcoords=axs_im[1].get_xaxis_transform(), ha="center", va="center", color=colors[4], bbox=dict(facecolor="white", edgecolor="none", pad=2), arrowprops=dict(arrowstyle="-", linestyle=":",color=colors[4], lw=1, clip_on=False, shrinkA=0, shrinkB=0))
# axs_im[1].annotate(vec_phi, xy=(phi_0[0], 3.5), xytext=(phi_0[0],3.5), xycoords=axs_im[2].get_xaxis_transform(), textcoords=axs_im[1].get_xaxis_transform(), ha="center", va="center", bbox=dict(facecolor="white", edgecolor="none", pad=2), arrowprops=dict(arrowstyle="-", color=colors[4], lw=1, clip_on=False, shrinkA=0, shrinkB=0))
# axs_im[1].annotate(vec_phi, xy=(phi_0[0], 3.5), xytext=(phi_0[0],3.5), xycoords=axs_im[2].get_xaxis_transform(), textcoords=axs_im[1].get_xaxis_transform(), ha="center", va="center", bbox=dict(facecolor="white", edgecolor="none", pad=2), arrowprops=dict(arrowstyle="-", color=colors[4], lw=1, clip_on=False, shrinkA=0, shrinkB=0))
# axs_im[1].annotate(vec_phi, xy=(phi_0[0], -0.45), xytext=(phi_0[0]-0.5,-0.45), xycoords=axs_im[2].get_xaxis_transform(), textcoords=axs_im[0].get_xaxis_transform(), ha="right", va="center", bbox=dict(facecolor="white", edgecolor="none", pad=2), arrowprops=dict(arrowstyle="-", color=colors[5], lw=1, clip_on=False, shrinkA=0, shrinkB=0))

# ax.annotate(state, xy=(phi_0[0], -0.15), xytext=(phi_0[i],-0.45), xycoords=ax.get_xaxis_transform(), textcoords=ax.get_xaxis_transform(), ha="center", va="center", arrowprops=dict(arrowstyle="->", color=colors[5], lw=1, clip_on=False))
# fig.savefig("/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/Paper/Images/Ifg and wv 0pipi.pdf", format="pdf",bbox_inches="tight")

plt.show()
