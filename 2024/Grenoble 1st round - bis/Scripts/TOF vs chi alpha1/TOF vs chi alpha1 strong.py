#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 11:38:15 2024

@author: aaa
"""

import os
import numpy as np
import shutil
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq, fft, fftfreq, dct, dst
from mpl_toolkits import mplot3d
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from PIL import Image as im
from scipy.optimize import curve_fit as fit
from scipy.special import jv

rad=np.pi/180
lim=0
chi_0=1.1
"""
No indium, pencil detector in
"""
T_1= 0.5638959255337962 +- 0.002012633569493103
T_2= 0.4361040744662038 +- 0.002012633569493103
a_1= 0.751
a_1_err= 0.003
a_2= 0.660
a_2_err=0.003
a_21=a_2/a_1
pencil_in=True
# inf_file_name_ifg="ifgPS1_2p_22pt_02Apr2032"
inf_file_name="TOF_vs_chi_alpha1_22pt_Bessel_0_2kHz_1200s_02Apr2041"
inf_file_name_ifg="ifgPS1_2p_22pt_03Apr0405"
xi_0=2.4
sgn=1
chi_0=-0.1
"""
Indium 1mm path1, pencil detector out (phase and contrast not stable)
"""
# T_1= 0.37845574117271946 +- 0.0018480181383231822
# T_2= 0.6215442588272806 +- 0.0018480181383231822
# a_1= 0.615
# a_1_err= 0.003
# a_2= 0.788
# a_2_err=0.002
# a_21=a_2/a_1
# pencil_in=False
# # inf_file_name_ifg="ifgPS1_2p_22pt_03Apr2146"
# inf_file_name="TOF_vs_chi_alpha1_22pt_Bessel_0_2kHz_1200s_03Apr2207"
# inf_file_name_ifg="ifgPS1_2p_22pt_04Apr0531"
# xi_0=0.9
# sgn=-1

"""
Indium 1mm path1, pencil detector out
"""
# T_1= 0.37845574117271946 +- 0.0018480181383231822
# T_2= 0.6215442588272806 +- 0.0018480181383231822
# a_1= 0.615
# a_1_err= 0.003
# a_2= 0.788
# a_2_err=0.002
# a_21=a_2/a_1
# pencil_in=False
# # inf_file_name_ifg="ifgPS1_2p_22pt_04Apr0622"
# inf_file_name="TOF_vs_chi_alpha1_22pt_Bessel_0_2kHz_1200s_04Apr0643"
# # inf_file_name_ifg="ifgPS1_2p_22pt_04Apr1407" #only one point
# inf_file_name_ifg="ifgPS1_2p_22pt_04Apr1412"
# xi_0=0.9
# sgn=-1
# lim=1
# chi_0=1.1
"""
Indium 1mm path2, pencil detector out - Great measurement!
"""
# T_1= 0.733036893619524 +- 0.0027541752345118893
# T_2= 0.26696310638047605 +- 0.0027541752345118893
# a_1= 0.856
# a_1_err= 0.003
# a_2= 0.517
# a_2_err= 0.005
# a_21=a_2/a_1
# pencil_in=False
# # inf_file_name_ifg="ifgPS1_2p_22pt_05Apr0720"
# inf_file_name="TOF_vs_chi_alpha1_22pt_Bessel_0_2kHz_900s_05Apr0730"
# inf_file_name_ifg="ifgPS1_2p_22pt_05Apr1303" 
# xi_0=0.9
# sgn=1

"""
Indium 1mm path2, pencil detector out
"""
# a_1= 0.856
# a_1_err= 0.003
# a_2= 0.517
# a_2_err= 0.005
# a_21=a_2/a_1
# pencil_in=False
# inf_file_name_ifg="ifgPS1_2p_22pt_06Apr0751"
# inf_file_name="TOF_vs_chi_alpha1_22pt_Bessel_0_2kHz_900s_06Apr0800"
# # inf_file_name_ifg="ifgPS1_2p_22pt_06Apr1450"
# xi_0=-2.03
# sgn=1

"""
Indium 1.5mm path1, pencil detector out
"""
# T_1= 0.28697528798598826 +- 0.0016654280796631897
# T_2= 0.7130247120140117 +- 0.0016654280796631897
# a_1= 0.536
# a_1_err= 0.003
# a_2= 0.844
# a_2_err= 0.002
# a_21=a_2/a_1
# pencil_in=False
# inf_file_name_ifg="ifgPS1_2p_22pt_06Apr2249"
# inf_file_name="TOF_vs_chi_alpha1_22pt_Bessel_0_2kHz_900s_06Apr2259"
# # inf_file_name_ifg="ifgPS1_2p_22pt_07Apr0433"
# xi_0=-2.3
# sgn=-1

"""
Indium 1.8mm path1, pencil detector out
"""
# T_1= 0.2457849692234557 +- 0.0015595993045329918
# T_2= 0.7542150307765443 +- 0.0015595993045329918
# a_1= 0.496
# a_1_err= 0.003
# a_2= 0.868
# a_2_err= 0.002
# a_21=a_2/a_1
# pencil_in=False
# inf_file_name_ifg="ifgPS1_2p_22pt_07Apr2027"
# inf_file_name="TOF_vs_chi_alpha1_22pt_Bessel_0_2kHz_1200s_07Apr2037"
# # inf_file_name_ifg="ifgPS1_2p_22pt_08Apr0400"
# # inf_file_name_ifg="ifgPS1_2p_22pt_08Apr0421"
# xi_0=-2.1
# sgn=-1

"""
Indium 1.8mm path1, pencil detector out (bad)
"""
# T_1= 0.2457849692234557 +- 0.0015595993045329918
# T_2= 0.7542150307765443 +- 0.0015595993045329918
# a_1= 0.496
# a_1_err= 0.003
# a_2= 0.868
# a_2_err= 0.002
# a_21=a_2/a_1
# pencil_in=False
# # inf_file_name_ifg="ifgPS1_2p_22pt_09Apr0601"
# inf_file_name="TOF_vs_chi_alpha1_22pt_Bessel_0_2kHz_1200s_09Apr0611"
# inf_file_name_ifg="ifgPS1_2p_22pt_09Apr1216"
# xi_0=-2.1
# sgn=-1
# lim=0

"""
Indium 1.5mm path2, pencil detector out
"""
# T_1= 0.805979978856342 +- 0.003091309944344375
# T_2= 0.19402002114365802 +- 0.003091309944344375
# a_1= 0.898
# a_1_err= 0.003
# a_2= 0.440
# a_2_err= 0.007
# a_21=a_2/a_1
# pencil_in=False
# # inf_file_name_ifg="ifgPS1_2p_22pt_11Apr0209"
# inf_file_name="TOF_vs_chi_alpha1_22pt_Bessel_0_2kHz_900s_11Apr0219"
# inf_file_name_ifg="ifgPS1_2p_22pt_11Apr0753"
# xi_0=-2.1
# sgn=1

sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round - bis/exp_CRG-3126/Sorted data/TOF vs chi alpha1/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"

sorted_fold_path_ifg="/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round - bis/exp_CRG-3126/Sorted data/Ifg/"+inf_file_name_ifg
cleandata_ifg=sorted_fold_path_ifg+"/Cleantxt"


alpha_1=-2.4048
alpha_1_err=0.0035

def w1(chi, a_21):
    return 1/(1+a_21*np.exp(1j*chi))

def w2(chi, a_21):
    return 1-w1(chi, a_21)

def fit_cos(x, A, B, C, D):
    return A/2*(1+B*np.cos(C*x-D))
A_avg=1
def fit_wv(t, B, Im_1, Re_1, xi_1):
    # return A_avg*((1-C_id)/2+Co*B*(1+2*Re_1*(1-np.cos(alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)))+2*Im_1*np.sin(alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1))))
    return B*(1+2*Re_1*(1-np.cos(alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)))+2*Im_1*np.sin(alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)))

for root, dirs, files in os.walk(cleandata_ifg, topdown=False):
    for name in files:
         tot_data=np.loadtxt(os.path.join(root, name))
if pencil_in:
    data_ifg=tot_data[:,2]+tot_data[:,5]
else:
    data_ifg=tot_data[:,2]
data_ifg_err=data_ifg**0.5
ps_pos=tot_data[:,0]
P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, chi_0]
print(P0)
B0=([np.amin(data_ifg),0,0.01,-5],[np.amax(data_ifg)*2,np.amax(data_ifg)*2,5, 5])

p_ifg,cov_ifg=fit(fit_cos, ps_pos, data_ifg, sigma=data_ifg_err, p0=P0,  bounds=B0)
err_ifg=np.diag(cov_ifg)**0.5
C_id = p_ifg[1]/(2*a_1*a_2)
C_id_err = (err_ifg[1]**2+C_id**2/(a_1**2)*a_1_err**2+C_id**2/(a_2**2)*a_2_err**2)**0.5/(2*a_1*a_2)
A=p_ifg[0]*(1-C_id)/2
w_ps=p_ifg[-2]
chi_0=p_ifg[-1]
print(chi_0)
chi_0_err=err_ifg[-1]
# print("A(1-C)/2=", A, "+-", A_err)
print("C_id=",C_id)
print("chi_err=",err_ifg[-1])
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
ax.errorbar(ps_pos,data_ifg, yerr=data_ifg**0.5,fmt="ko",capsize=5, ms=3)
ax.plot(ps_plt,fit_cos(ps_plt, *p_ifg), "b")
ax.vlines(p_ifg[-1]/p_ifg[-2],fit_cos(p_ifg[-1]/p_ifg[-2]+np.pi,*p_ifg),fit_cos(p_ifg[-1]/p_ifg[-2],*p_ifg), color="k")


i=0
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    # print(files)
    for name in files[:]:
        # print(name)
        if i==0:
            tot_data=np.loadtxt(os.path.join(root, name))[:,:]
            time=tot_data[:,1]
            f_1=tot_data[0,-3]*1e-3
            am_1=tot_data[0,-4]
            print("f1=", f_1)
            print("a1=", am_1)
            i=1
        else:
            data=np.loadtxt(os.path.join(root, name))[:,:]
            tot_data = np.vstack((tot_data, data))
time_plt=np.linspace(time[0], time[-1], 1000)
ps_pos=tot_data[::len(time),-1]
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)

matrix=np.zeros((len(ps_pos),len(time)))
matrix_err=np.zeros((len(ps_pos),len(time)))
for i in range(len(ps_pos)):
    if pencil_in:
        K=(np.average(tot_data[:,3][tot_data[:,-1]==ps_pos[i]])+np.average(tot_data[:,4][tot_data[:,-1]==ps_pos[i]]))
        matrix[i]=tot_data[:,5][tot_data[:,-1]==ps_pos[i]]
        matrix_err[i]=abs(matrix[i]/K)*(1/matrix[i]+1/K)**0.5
        matrix[i]/=K

    else:
        K=(np.average(tot_data[:,3][tot_data[:,-1]==ps_pos[i]])+np.average(tot_data[:,4][tot_data[:,-1]==ps_pos[i]]))
        matrix[i]=tot_data[:,3][tot_data[:,-1]==ps_pos[i]]
        matrix_err[i]=abs(matrix[i]/K)*(1/matrix[i]+1/K)**0.5
        matrix[i]/=K

ps_data=np.sum(matrix, axis=1)
ps_data_err=np.sum(matrix_err**2, axis=1)**0.5
P0=[(np.amax(ps_data)+np.amin(ps_data))/2, 0.001, *p_ifg[2:]]
B0=([0.01,0,0.01,-10],[np.amax(ps_data)+100000,1000,5, 10])
# p_int,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
# err_int=np.diag(cov)**0.5
A_avg=np.average(ps_data[3:-4])/len(time)*2
A_avg_err=np.sum(ps_data[3:-4])**0.5/len(ps_data)/len(time)*2
# print("C=", p_int[1], "+-", cov[1,1]**0.5)
fig = plt.figure(figsize=(7,3))
ax = fig.add_subplot(111)
ax.set_title("Integrated intensity")
ax.errorbar(ps_pos,ps_data, yerr=ps_data_err,fmt="ko",capsize=5, ms=3)
ax.set_ylim([np.average(ps_data)-1,np.average(ps_data)+1])
ax.set_xlabel("$\chi$")
ax.set_ylabel("Arb.")
avg_err=np.sum(ps_data_err**2)**0.5/len(ps_data)
C_int=(np.amax(ps_data)-np.amin(ps_data))/(2*np.average(ps_data))
C_int_err=(ps_data_err[ps_data==np.amax(ps_data)]**2+ps_data_err[ps_data==np.amin(ps_data)]**2+4*C_int**2*avg_err**2)**0.5/(2*np.average(ps_data))
print("C_int=", str("%.3f" %(C_int),)+" $\pm$ "+str("%.3f" %(C_int_err),))
ax.text(0,np.amax(ps_data)+2*np.amax(ps_data_err),"$C=\dfrac{max-min}{2\,avg}$="+str("%.3f" %(C_int),)+"$\\pm$"+str("%.3f" %(C_int_err),), ha="center")
plt.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round - bis/Report/Images/Results path 1/Integ_int_"+inf_file_name[-9:]+".pdf", format="pdf",bbox_inches="tight")


matrix_err=(matrix_err**2/(C_id*A_avg)**2+matrix**2*A_avg_err**2/(A_avg**2*C_id)**2+((matrix/A_avg-0.5)/C_id**2)**2*C_id_err**2)**0.5
matrix=(matrix-A_avg/2)/(A_avg*C_id)+1/2


P0=[300,300, -0.8, 1]
p_tot=np.zeros((len(ps_pos),len(P0)))
err_tot=np.zeros((len(ps_pos),len(P0)))

P0=[300,300, -0.8, 1]
p_tot=np.zeros((len(ps_pos),len(P0)))
err_tot=np.zeros((len(ps_pos),len(P0)))

Im=np.zeros((len(ps_pos)))
Im_err=np.zeros((len(ps_pos)))

Re=np.zeros((len(ps_pos)))
Re_err=np.zeros((len(ps_pos)))

rho=np.zeros((len(ps_pos)))
chi=ps_pos*w_ps-chi_0
chi_plt=np.linspace(chi[0], chi[-1], 100)
cos2=np.zeros((len(ps_pos)))
cos2_err=np.zeros((len(ps_pos)))
cos2_fit=np.zeros((len(ps_pos)))
cos2_err_fit=np.zeros((len(ps_pos)))

for i in range(len(ps_pos)):
    func_data=matrix[i]
    func_data_err=matrix_err[i]
    chi_aus=chi[i]
    P0=[np.cos(chi[i]/2)**2, w1(chi[i],a_21).imag, abs(w1(chi[i],a_21))-w1(chi[i],a_21).real-1000, xi_0]
    # print(P0)
    B0=([0,w1(chi[i],a_21).imag-1000,abs(w1(chi[i],a_21))-w1(chi[i],a_21).real-1000, -2*np.pi],[np.inf, w1(chi[i],a_21).imag+1000, abs(w1(chi[i],a_21))-w1(chi[i],a_21).real+1000, 2*np.pi])
    try: 
        p_wv,cov_wv = fit(fit_wv, time, func_data, p0=P0, bounds=B0, sigma=matrix_err[i])
        # print(p_wv[-1])
    except:
        print("fit not found ps=", ps_pos[i])
    err_wv=np.diag(cov_wv)**0.5
    # print(p_wv[-1])
    # print(p_wv,err_wv)
    Im[i]=p_wv[1]
    Im_err[i]=(err_wv[1]**2+np.sin(chi[i])**2*chi_0_err**2)**0.5
    if a_1==0.751:
        s=np.sign(1+4*(p_wv[2]-p_wv[1]**2))*abs(1+4*(p_wv[2]-p_wv[1]**2))**0.5
    else:
        s=(1+4*(p_wv[2]-p_wv[1]**2))**0.5
    Re[i]=(1+sgn*s)/2
    Re_err[i]=(err_wv[2]**2+4*Im[i]**2*Im_err[i]**2)**0.5/abs(s)

    cos2_fit[i]=p_wv[0]#*Co#+p_wv[0]*(1-C_id)/2
    cos2_err_fit[i]=err_wv[0]
    
    # fig = plt.figure(figsize=(8,6))
    # ax = fig.add_subplot(111)
    # ax.errorbar(time, matrix[i], yerr= matrix_err[i], fmt="ko")
    # ax.plot(time_plt, fit_wv(time_plt, *p_wv))
    # ax.set_title(str("%.2f'"%ps_pos[i],))
fig = plt.figure(figsize=(8, 4), dpi=200)
fig.suptitle(inf_file_name)
gs = GridSpec(1,2, figure=fig, wspace=0, hspace=0, top=0.85, bottom=0)
axs=[fig.add_subplot(gs[:,:]), fig.add_subplot(gs[0,0]),fig.add_subplot(gs[0,1])]
axs[2].tick_params(axis="y", labelleft=False, left = False, labelright=True, right=True)
# axs[1].set_ylabel("Arb.", fontsize = plt.rcParams['axes.titlesize'])
axs[1].set_title("$\Im(w_{1,+})$")
axs[2].set_title("$\Re(w_{1,+})$")
axs[0].set_xlabel("$\chi$ [rad]", labelpad=20)
axs[0].tick_params(axis="both", labelleft=False, left = False, labelbottom=False, bottom = False)
axs[0].set_frame_on(False)
axs[1].plot(chi_plt, w1(chi_plt,a_21).imag,"k--", alpha=0.5)
axs[1].errorbar(chi, Im, Im_err, fmt="k.", capsize=3)
axs[2].plot(chi_plt, w1(chi_plt,a_21).real,"r--", alpha=0.5)
axs[2].errorbar(chi, Re, abs(Re_err), fmt="r.", capsize=3)
if lim:
    axs[1].set_ylim([-2,2])
    axs[2].set_ylim([-sgn*1,sgn*5])

plt.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round - bis/Report/Images/Results path 1/Wv_"+inf_file_name[-9:]+".pdf", format="pdf",bbox_inches="tight")
fig = plt.figure(figsize=(8,6), dpi=200)
ax = fig.add_subplot(111)
ax.errorbar(ps_pos, cos2_fit, yerr=cos2_err_fit, fmt="k.", capsize=5, label="$c_0$")
ax.plot(ps_plt, 1/2+a_1*a_2*np.cos(chi_plt))

plt.show()