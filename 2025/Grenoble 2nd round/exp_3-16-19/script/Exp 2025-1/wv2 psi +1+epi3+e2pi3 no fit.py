# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 16:38:31 2025

@author: S18
"""


import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit

state="$|\\psi_{in}>=(|1>+exp(-i60)|2>+exp(i120)|3>)/\\sqrt{3}$"

chi_1_0=np.pi/3
chi_2_0=0
chi_3_0=np.pi
chi_1=0
chi_2=0
chi_3=0

C_12=0.69
C_13=0.74
C_23=0.62

points=48
points_per=16

bad_apples=[
            ]

good_apples=["ifg_wv2_psi_+1+exp(-i60)+exp(i120)_no_fit_21Oct1356"#bit noisy
            "ifg_wv2_psi_+1+exp(-i60)+exp(i120)_no_fit_22Oct1812" #good-ish
            "ifg_wv2_psi_+1+exp(-i60)+exp(i120)_no_fit_24Oct2156" #bad
             ]

inf_file_names=["ifg_wv2_psi_+1+exp(-i60)+exp(i120)_no_fit_22Oct1812" #good-ish

]

def fit_cos(x, A, B, C, D):
    return A/2*(1+B*np.cos(C*x-D))

def w1(chi_1, chi_2, chi_3):
    return a_1*np.exp(-1j*(chi_1_0+chi_1))/(a_1*np.exp(-1j*(chi_1_0+chi_1))+a_2*np.exp(-1j*(chi_2_0+chi_2))+a_3*np.exp(-1j*(chi_3_0+chi_3)))

def w2(chi_1, chi_2, chi_3):
    return a_2*np.exp(-1j*(chi_2_0+chi_2))/(a_1*np.exp(-1j*(chi_1_0+chi_1))+a_2*np.exp(-1j*(chi_2_0+chi_2))+a_3*np.exp(-1j*(chi_3_0+chi_3)))

def w3(chi_1, chi_2, chi_3):
    return a_3*np.exp(-1j*(chi_3_0+chi_3))/(a_1*np.exp(-1j*(chi_1_0+chi_1))+a_2*np.exp(-1j*(chi_2_0+chi_2))+a_3*np.exp(-1j*(chi_3_0+chi_3)))

def I_corr(A, chi_1, chi_2, chi_3):
    return A/3*(1+2*a_1*a_2*np.cos(chi_1_0+chi_1-chi_2_0-chi_2)+2*a_1*a_3*np.cos(chi_1_0+chi_1-chi_3_0-chi_3) + 2*a_2*a_3*np.cos(chi_2_0+chi_2-chi_3_0-chi_3))

for inf_file_name in inf_file_names:
        print(inf_file_name)
        sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Ifg wv no fit/"+inf_file_name
        cleandata=sorted_fold_path+"/Cleantxt"
        for root, dirs, files in os.walk(cleandata, topdown=False):
            files=np.sort(files)
            data_ifg_matrix=np.zeros((4,points))
            name = files[0]
            # print(name)
            tot_data=np.loadtxt(os.path.join(root, name))[:,1:]
            time_ifg=tot_data[0,1]
            data_ifg=tot_data[:,2]
            int_data=np.loadtxt(os.path.join(root, files[-1]))[:,3]
            time_int=np.loadtxt(os.path.join(root, files[-1]))[0,2]
            # print("path (213) intensities =",int_data)
I_1=int_data[1]*time_ifg/time_int
I_2=int_data[0]*time_ifg/time_int
I_3=int_data[2]*time_ifg/time_int
I_1_err=int_data[1]**0.5*time_ifg/time_int
I_2_err=int_data[0]**0.5*time_ifg/time_int
I_3_err=int_data[2]**0.5*time_ifg/time_int

a_1=(I_1/(I_1+I_2+I_3))**0.5
a_2=(I_2/(I_1+I_2+I_3))**0.5
a_3=(I_3/(I_1+I_2+I_3))**0.5

A=(I_1+I_2+I_3)*3

data_ifg_err=data_ifg**0.5
ps_pos=tot_data[:,0]
P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, 0.7, 6, 4.6]
B0=([np.amin(data_ifg)/2,0,0.01,-2*np.pi],[np.amax(data_ifg)*3,np.amax(data_ifg)*2,7, 2*np.pi])
p,cov=fit(fit_cos, ps_pos, data_ifg, sigma=data_ifg_err, p0=P0,  bounds=B0)
err=np.diag(cov)**0.5
A_fit=p[0]
C_fit=p[1]
C_fit_err=err[1]**2
A_fit_err=err[0]**2
x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
fig.suptitle(name[:-4])
ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
ax.plot(x_plt,fit_cos(x_plt, *p), "b")

# p[2]=6.1
chi_2=(ps_pos-ps_pos[0])*p[2]-np.pi
data_ifg+=A/3*(2*(1-C_12)*a_1*a_2*np.cos(chi_1+chi_1_0-chi_2-chi_2_0) + 2*(1-C_13)*a_1*a_3*np.cos(chi_1+chi_1_0-chi_3-chi_3_0) + 2*(1-C_23)*a_2*a_3*np.cos(chi_2+chi_2_0-chi_3-chi_3_0))
data_ifg_matrix[3]=data_ifg
i=0
for k in [2,1,3]:
    data_ifg_matrix[i]=np.roll(data_ifg, -4*k)
    i+=1

chi_2+=np.pi
chi_2_plt=np.linspace(chi_2[0], chi_2[-1], 1000)

# chi_2_plt=np.linspace(chi_2[0], chi_2[-1], 1000)
# data_ifg+=A/3*(2*(1-C_12)*a_1*a_2*np.cos(chi_1+chi_1_0-chi_2-chi_2_0) + 2*(1-C_13)*a_1*a_3*np.cos(chi_1+chi_1_0-chi_3-chi_3_0) + 2*(1-C_23)*a_2*a_3*np.cos(chi_2+chi_2_0-chi_3-chi_3_0))
# data_ifg_matrix[0]=data_ifg
# i=0
# for k in [3,1,2]:
#     data_ifg_matrix[i+1]=np.roll(data_ifg, -4*k)
#     i+=1

for k in [0,1,2,3]:
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    ax.set_title(k)
    ax.errorbar(ps_pos,data_ifg_matrix[k],yerr=data_ifg_matrix[k]**0.5,fmt="ko",capsize=5, ms=3)
data_ifg_matrix_err=data_ifg_matrix**0.5

I_0=data_ifg_matrix[0]
I_mpi2=data_ifg_matrix[1]
I_ppi2=data_ifg_matrix[2]
I_pi=data_ifg_matrix[3]

I_0_err=data_ifg_matrix_err[0]
I_mpi2_err=data_ifg_matrix_err[1]
I_ppi2_err=data_ifg_matrix_err[2]
I_pi_err=data_ifg_matrix_err[3]

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.errorbar(chi_2, I_0,yerr=I_0**0.5,fmt="ko",capsize=5, ms=3)
ax.plot(chi_2_plt, I_corr(A, chi_1, chi_2_plt, chi_3))

Im_2=(I_ppi2-I_mpi2)/I_0/4
Im_2_err=(I_mpi2_err**2+I_pi_err**2+(4*Im_2)**2*I_0_err**2)**0.5/(4*abs(I_0))

Re_2=I_2/I_0 + 1/4 - I_pi/(I_0*4)
Re_2_err=(I_2_err**2+(I_ppi2_err/4)**2+(Re_2-1/4)**2*I_0_err**2)**0.5/abs(I_0)

# sa=I_pi/I_0-4*Im_2**2
# s=-np.sign(sa)*abs(sa)**0.5
# Re_2=(1+s)/2
# Re_2_err=1/4*((4*I_0**4*I_pi_err**2-4*I_pi*I_0*(I_ppi2-I_mpi2)**2*I_0_err**2+(I_ppi2-I_mpi2)**4*I_0_err**2+I_0**2*(4*I_pi**2*I_0_err**2+(I_ppi2-I_mpi2)**2*(I_ppi2_err**2+I_mpi2_err**2)))/(I_0**4*(4*I_pi*I_0-(I_ppi2-I_mpi2)**2)))**0.5

fig = plt.figure(figsize=(10,6), dpi=150)
fig.suptitle(state)
gs = fig.add_gridspec(2,3 , width_ratios=(0.5,2,0.5), hspace=0.0, wspace=0.3)
axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[1, 0]),fig.add_subplot(gs[0, 1]),fig.add_subplot(gs[1, 1]),fig.add_subplot(gs[0, 2]),fig.add_subplot(gs[1, 2])]
axs[0].set_title("$w_{1,+}$", fontsize=13)
axs[2].set_title("$w_{2,+}$", fontsize=13)
axs[4].set_title("$w_{3,+}$", fontsize=13)

axs[0].set_ylabel("Real part")
axs[1].set_ylabel("Imaginary part")
# fig.suptitle(inf_file_name)
colors=["k","#f10d0c","#00a933","#5983b0"]
plt.rcParams["mathtext.fontset"]="cm"
axs[0].tick_params(axis="x", bottom=False, labelbottom=False)
axs[2].tick_params(axis="x", bottom=False, labelbottom=False)
axs[4].tick_params(axis="x", bottom=False, labelbottom=False)
# axs[1].tick_params(axis="y", left=False, labelleft=False)
# axs[3].tick_params(axis="y", left=False, labelleft=False)

# axs[0].errorbar(chi_2,Re_2, Re_2_err, fmt="k.", capsize=3)
axs[0].errorbar(chi_2_plt, w1(0,chi_2_plt,0).real, color=colors[3], alpha=0.8)

# axs[1].errorbar(chi_2,Im_2, Im_2_err, fmt="k.", capsize=3)
axs[1].plot(chi_2_plt, w1(0,chi_2_plt,0).imag, color=colors[3], alpha=0.8 )

axs[2].errorbar(chi_2,Re_2, Re_2_err, fmt="k.", capsize=3)
axs[2].errorbar(chi_2_plt, w2(0,chi_2_plt,0).real, color=colors[3], alpha=0.8)

axs[3].errorbar(chi_2,Im_2, Im_2_err, fmt="k.", capsize=3)
axs[3].plot(chi_2_plt, w2(0,chi_2_plt,0).imag, color=colors[3], alpha=0.8 )

# axs[4].errorbar(chi_2,Re_2, Re_2_err, fmt="k.", capsize=3)
axs[4].errorbar(chi_2_plt, w3(0,chi_2_plt,0).real, color=colors[3], alpha=0.8)

# axs[5].errorbar(chi_2,Im_2, Im_2_err, fmt="k.", capsize=3)
axs[5].plot(chi_2_plt, w3(0,chi_2_plt,0).imag, color=colors[3], alpha=0.8 )

for ax in axs:
    ax.set_xticks(chi_2[::8])
    ax.set_ylim([-10,10])
    # ax.set_xticklabels((chi_2[::8]/np.pi).astype(str))
    ax.grid(True, ls="dotted")
for ax in axs[:]:
    ax.set_xlabel("$\mathdefault{\\chi_2}$ [rad]")
    
plt.show()