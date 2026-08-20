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
import My_module_Exp_2025_1 as mymod

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def fit_C(x, C_13, B, D, E):
    return A/3*(1-2*C_13*a_1*a_3+2*B*np.cos(D*x-E))

state="$|\\psi_{in}>=(exp(-i60)|1>+|2>+exp(i120)|3>)/\\sqrt{3}$"

chi_1_0=-np.pi/3
chi_2_0=0
chi_3_0=2*np.pi/3
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

good_apples=[
             ]

inf_file_names=[
                # "ifg_wv2_psi_+exp(-i60)+1+exp(i120)_no_fit_21Oct2319" #good prolly
                "ifg_wv2_psi_+exp(-i60)+1+exp(i120)_no_fit_22Oct2237" #best
                # "ifg_wv2_psi_+exp(-i60)+1+exp(i120)_no_fit_24Oct1953" #good maybe
]

correct=1

C_12, C_13, C_23 = mymod.contrast(inf_file_names[0])
# C_12, C_13, C_23 = mymod.contrast("group_p1m1m1_25_Oct")
if correct:
    C_12, C_12_err, C_13, C_13_err, C_23, C_23_err = mymod.CandA(inf_file_names[0])
print("C_12=", C_12, "C_13=", C_13, "C_23=", C_23)

for inf_file_name in inf_file_names:
        # print(inf_file_name)
        sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Ifg wv no fit/"+inf_file_name
        cleandata=sorted_fold_path+"/Cleantxt"
        for root, dirs, files in os.walk(cleandata, topdown=False):
            files=np.sort(files)
            name = files[0]
            # print(name)
            tot_data=np.loadtxt(os.path.join(root, name))[:,1:]
            time_meas=tot_data[0,1]
            N_ifg=time_meas#tot_data[:,5]/np.average(tot_data[:,5])*time_meas
            # S1=((tot_data[:,2]+tot_data[:,3])+tot_data[:,5])
            data_O_err=tot_data[:,2]**0.5/N_ifg
            data_O=tot_data[:,2]/N_ifg
            data_H_err=tot_data[:,3]**0.5/N_ifg
            data_H=tot_data[:,3]/N_ifg
            data_OH_err=(tot_data[:,2]+tot_data[:,3])**0.5/N_ifg
            data_OH=(tot_data[:,2]+tot_data[:,3])/N_ifg
            data_aux_err=tot_data[:,5]**0.5/N_ifg
            data_aux=tot_data[:,5]/N_ifg
            ps_pos=tot_data[:,0]
            int_data=np.loadtxt(os.path.join(root, files[-1]))[:,3]
            time_int=np.loadtxt(os.path.join(root, files[-1]))[0,2]
            # print("path (213) intensities =",int_data)
I_1=int_data[1]/time_int
I_2=int_data[0]/time_int
I_3=int_data[2]/time_int
I_1_err=int_data[1]**0.5/time_int
I_2_err=int_data[0]**0.5/time_int
I_3_err=int_data[2]**0.5/time_int

a_1=(I_1/(I_1+I_2+I_3))**0.5
a_2=(I_2/(I_1+I_2+I_3))**0.5
a_3=(I_3/(I_1+I_2+I_3))**0.5
if correct:
    a_1,a_2,a_3=1/3**0.5,1/3**0.5,1/3**0.5

A=(I_1+I_2+I_3)*3
A_err=(I_1_err**2+I_2_err**2+I_3_err**2)**0.5*3
# print(A)
ps_pos=tot_data[:,0]
P0=[(np.amax(data_O)+np.amin(data_O))/2, 10, 6.4, -2.6]
B0=([np.amin(data_O)/2,1,5,-2*np.pi],[np.amax(data_O)*3,np.amax(data_O)*2,7, 2*np.pi])
p,cov=fit(fit_cos, ps_pos, data_O, sigma=data_O_err, p0=P0,  bounds=B0)
err=np.diag(cov)**0.5
A_fit=p[0]
C_fit=p[1]
C_fit_err=err[1]**2
A_fit_err=err[0]**2
x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)

P0_C=[C_13, C_23*a_2*a_3-C_12*a_1*a_2, 6, 4.6]
B0_C=([0.1,-0.2,0,0.01],[1,1,7, 2*np.pi])
p_C,cov_C=fit(fit_C, ps_pos, data_O, sigma=data_O_err, p0=P0_C,  bounds=B0_C)
err_C=np.diag(cov_C)**0.5
print("C_13=",p_C[0],"+-",err_C[0],"C_23*a_2*a_3-C_12*a_1*a_2=",p_C[1],"+-",err_C[1])
print(C_13,C_23*a_2*a_3-C_12*a_1*a_2)
# print(p_C)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
fig.suptitle(name[:-4])
ax.errorbar(ps_pos,data_O,yerr=data_O_err,fmt="ko",capsize=5, ms=3, label="O")
ax.errorbar(ps_pos,data_H,yerr=data_H_err,fmt="ro",capsize=5, ms=3, label="H")
ax.errorbar(ps_pos,data_OH,yerr=data_OH_err,fmt="go",capsize=5, ms=3, label="O+H")
ax.errorbar(ps_pos,data_aux,yerr=data_aux_err,fmt="co",capsize=5, ms=3, label="Aux")
# ax.errorbar(ps_pos,S1,yerr=data_aux_err,fmt="yo",capsize=5, ms=3, label="O+H+Aux")
ax.plot(x_plt,fit_cos(x_plt, *p), "b")
ax.plot(x_plt,fit_C(x_plt, *p_C), "y--")
ax.legend()

chi_2=(ps_pos-ps_pos[0])*p_C[2]-np.pi
data_O_matrix=np.zeros((4,points))
data_O_matrix_err=np.zeros((4,points))
if correct:
    corr=A/3*(2*(1-C_12)*a_1*a_2*np.cos(chi_1+chi_1_0-chi_2-chi_2_0) + 2*(1-C_13)*a_1*a_3*np.cos(chi_1+chi_1_0-chi_3-chi_3_0) + 2*(1-C_23)*a_2*a_3*np.cos(chi_2+chi_2_0-chi_3-chi_3_0))
    # data_O+=A/3*(2*(1-C_12)*a_1*a_2*np.cos(chi_1+chi_1_0-chi_2-chi_2_0) + 2*(1-C_13)*a_1*a_3*np.cos(chi_1+chi_1_0-chi_3-chi_3_0) + 2*(1-C_23)*a_2*a_3*np.cos(chi_2+chi_2_0-chi_3-chi_3_0))
    data_O+=corr
    data_O_err=(data_O_err**2+(A_err*corr/A/3)**2 + (A*2/9)**2*((C_12_err*np.cos(chi_1+chi_1_0-chi_2-chi_2_0))**2+(C_13_err*np.cos(chi_1+chi_1_0-chi_3-chi_3_0))**2+(C_23_err*np.cos(chi_2+chi_2_0-chi_3-chi_3_0))**2))**0.5
data_O_matrix[3]=data_O
data_O_matrix_err[3]=data_O_err
i=0
for k in [2,1,3]:
    data_O_matrix[i]=np.roll(data_O, -4*k)
    data_O_matrix_err[i]=np.roll(data_O_err, -4*k)
    i+=1

chi_2+=np.pi
chi_2_plt=np.linspace(chi_2[0], chi_2[-1], 1000)

# chi_2_plt=np.linspace(chi_2[0], chi_2[-1], 1000)
# data_O+=A/3*(2*(1-C_12)*a_1*a_2*np.cos(chi_1+chi_1_0-chi_2-chi_2_0) + 2*(1-C_13)*a_1*a_3*np.cos(chi_1+chi_1_0-chi_3-chi_3_0) + 2*(1-C_23)*a_2*a_3*np.cos(chi_2+chi_2_0-chi_3-chi_3_0))
# data_O_matrix[0]=data_O
# i=0
# for k in [3,1,2]:
#     data_O_matrix[i+1]=np.roll(data_O, -4*k)
#     i+=1

# for k in [0,1,2,3]:
#     fig = plt.figure(figsize=(8,6))
#     ax = fig.add_subplot(111)
#     ax.set_title(k)
#     ax.errorbar(ps_pos,data_O_matrix[k],yerr=data_O_matrix[k]**0.5,fmt="ko",capsize=5, ms=3)

I_0=data_O_matrix[0]
I_mpi2=data_O_matrix[1]
I_ppi2=data_O_matrix[2]
I_pi=data_O_matrix[3]

# print((3/(2*A)*((I_0[0]+I_pi[0]))-1)/(2*a_2*a_3),C_23)

I_0_err=data_O_matrix_err[0]
I_mpi2_err=data_O_matrix_err[1]
I_ppi2_err=data_O_matrix_err[2]
I_pi_err=data_O_matrix_err[3]

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.errorbar(chi_2, I_0,yerr=I_0_err,fmt="ko",capsize=5, ms=3)
if correct:
    ax.plot(chi_2_plt, mymod.I_corr(A, a_1, a_2, a_3, chi_1, chi_1_0, chi_2_plt, chi_2_0, chi_3, chi_3_0, 1, 1, 1))
else:
    ax.plot(chi_2_plt, mymod.I_corr(A, a_1, a_2, a_3, chi_1, chi_1_0, chi_2_plt, chi_2_0, chi_3, chi_3_0, C_12, C_13, C_23))

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

w1=mymod.w1(a_1, a_2, a_3, chi_1, chi_1_0, chi_2_plt, chi_2_0, chi_3, chi_3_0, C_12, C_13, C_23)
if correct:
    w1=mymod.w1(a_1, a_2, a_3, chi_1, chi_1_0, chi_2_plt, chi_2_0, chi_3, chi_3_0, 1, 1, 1)
# axs[0].errorbar(chi_1,Re_1, Re_1_err, fmt="k.", capsize=3)
axs[0].errorbar(chi_2_plt, w1.real, color=colors[3], alpha=0.8)
# axs[1].errorbar(chi_1,Im_1, Im_1_err, fmt="k.", capsize=3)
axs[1].plot(chi_2_plt, w1.imag, color=colors[3], alpha=0.8 )

w2=mymod.w2(a_1, a_2, a_3, chi_1, chi_1_0, chi_2_plt, chi_2_0, chi_3, chi_3_0, C_12, C_13, C_23)
if correct:
    w2=mymod.w2(a_1, a_2, a_3, chi_1, chi_1_0, chi_2_plt, chi_2_0, chi_3, chi_3_0, 1, 1, 1)
axs[2].errorbar(chi_2,Re_2, Re_2_err, fmt="k.", capsize=3)
axs[2].errorbar(chi_2_plt, w2.real, color=colors[3], alpha=0.8)
axs[3].errorbar(chi_2,Im_2, Im_2_err, fmt="k.", capsize=3)
axs[3].plot(chi_2_plt, w2.imag, color=colors[3], alpha=0.8 )

w3=mymod.w3(a_1, a_2, a_3, chi_1, chi_1_0, chi_2_plt, chi_2_0, chi_3, chi_3_0, C_12, C_13, C_23)
if correct:
    w3=mymod.w3(a_1, a_2, a_3, chi_1, chi_1_0, chi_2_plt, chi_2_0, chi_3, chi_3_0, 1, 1, 1)
# axs[4].errorbar(chi_3,Re_3, Re_3_err, fmt="k.", capsize=3)
axs[4].errorbar(chi_2_plt, w3.real, color=colors[3], alpha=0.8)
# axs[5].errorbar(chi_3,Im_3, Im_3_err, fmt="k.", capsize=3)
axs[5].plot(chi_2_plt, w3.imag, color=colors[3], alpha=0.8 )

for ax in axs:
    ax.set_xticks(chi_2[::8])
    # ax.set_xticklabels((chi_1[::8]/np.pi).astype(str))
    ax.grid(True, ls="dotted")
    # if correct:
    #     ax.set_ylim([-3,3])
for ax in axs[:]:
    ax.set_xlabel("$\mathdefault{\\chi_1}$ [rad]")

text_1=np.array([chi_2, Re_2, Re_2_err, Im_2, Im_2_err])
if correct:
    np.savetxt("/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Ifg wv no fit/Results Corrected/"+inf_file_names[0]+".txt", np.transpose(text_1))
else:
    np.savetxt("/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Ifg wv no fit/Results Uncorrected/"+inf_file_names[0]+".txt", np.transpose(text_1))

text_int=np.array([a_1, a_2, a_3])
np.savetxt("/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Ifg wv no fit/Results Corrected/"+inf_file_names[0]+"_int.txt", text_int)    
np.savetxt("/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Ifg wv no fit/Results Uncorrected/"+inf_file_names[0]+"_int.txt", text_int)

plt.show()