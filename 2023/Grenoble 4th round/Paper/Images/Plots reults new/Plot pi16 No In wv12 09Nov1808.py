#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 12:24:11 2024

@author: aaa
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 15:14:27 2024

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
a_1= 0.751
a_1_err= 0.003
a_2= 0.660
a_2_err=0.003
a_21=a_2/a_1
a_21_err= a_21*((a_1_err/a_1)**2+(a_2_err/a_2)**2)**0.5

inf_file_name="TOF_vs_chi_A+B_22pt_pi16_1200s_09Nov1808"
# inf_file_name="TOF_vs_chi_A+B_22pt_pi16_1200s_4P_11Nov1354"
# inf_file_name="TOF_vs_chi_A+B_22pt_pi16_1200s_4P_11Nov0502"
alpha_1=0.1932 #/2.354
alpha_1_err=0.0005
alpha_2=0.1969 #/2.354
alpha_2_err=0.0004


def w1(chi):
    return (1/(1+a_21*np.exp(1j*chi)))

def w2(chi):
    return (1-1/(1+a_21*np.exp(1j*chi)))

def w2_Im(chi, a_21, chi_0):
    return (1-1/(1+a_21*np.exp(1j*(chi-chi_0)))).imag

def w1_Im(chi, a_21, chi_0):
    return (1/(1+a_21*np.exp(1j*(chi-chi_0)))).imag

def djv0(x):
    return (x*np.cos(x)-np.sin(x))/x**2

def fit_cos(x, A, B, C, D):
    return A/2*(1+B*np.cos(C*x-D))
    # return A/2*(1+B*np.cos(C*x-D))
A_aus=1
def fit_Im(t, B, Im_1, Im_2, xi_1, xi_2):
    return B*(1-2*Im_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)-2*Im_2*np.sin(2*np.pi*1e-3*f_2*t+xi_2))
    # return A_aus*((1-C_id)/2+C_id*B*(1-2*Im_1*alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)-2*Im_2*alpha_2*np.sin(2*np.pi*1e-3*f_2*t+xi_2)))

sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/TOF A+B/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"

i=0
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    # print(files)
    for name in files:
        # print(name)
        if i==0:
            tot_data=np.loadtxt(os.path.join(root, name))[:,:]
            time=tot_data[:,1]
            f_2=tot_data[0,-3]*1e-3
            f_1=tot_data[0,-6]*1e-3
            am_2=tot_data[0,-4]
            am_1=tot_data[0,-7]
            print("f1=", f_1)
            print("f2=", f_2)
            print("a1=", am_1)
            print("a2=", am_2)
            i=1
        else:
            data=np.loadtxt(os.path.join(root, name))[:,:]
            tot_data = np.vstack((tot_data, data))
time_plt=np.linspace(time[0], time[-1], 1000)
ps_pos=tot_data[::len(time),-1]
N = len(time)
S_F=16.6667
matrix=np.zeros((len(ps_pos),len(time)))
matrix_err=np.zeros((len(ps_pos),len(time)))
for i in range(len(ps_pos)):
    matrix[i]=tot_data[:,5][tot_data[:,-1]==ps_pos[i]]
    matrix_err[i]=matrix[i]**0.5
    
ps_data=np.sum(matrix, axis=1)
P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, -0.5]
B0=([100,0,0.01,-10],[np.amax(ps_data)+10000,np.amax(ps_data)+10000,5, 10])
p_int,cov_int=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
err_int=np.diag(cov_int)**0.5
j0_1=jv(0,alpha_1*0)
j0_2=jv(0,alpha_2*0)
j0_1_err=abs(djv0(alpha_1)*alpha_1_err)*0
j0_2_err=abs(djv0(alpha_2)*alpha_2_err)*0
C_D=(2*a_1*a_2)
C_id = p_int[1]/C_D
C_id_err = ((C_D*err_int[1])**2+(C_D*a_1_err/a_1)**2+(C_D*a_2_err/a_2)**2+(C_D*j0_1_err/j0_1)**2+(C_D*j0_2_err/j0_2)**2)**0.5
A=p_int[0]*(1-C_id)/2
A_err= (((1-C_id)/2*err_int[0])**2+(p_int[0]/2*C_id_err)**2)**0.5
A_aus=p_int[0]/len(time)
A_aus_err=err_int[0]/len(time)
w_ps=p_int[-2]
chi_0=p_int[-1]
chi_0_err=err_int[-1]
print("A(1-C)/2=", A, "+-", A_err)
print("C=",C_id, "+-", C_id_err)
print("chi_err=",err_int[-1])
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
ax.errorbar(ps_pos,ps_data, yerr=ps_data**0.5,fmt="ko",capsize=5, ms=3)
ax.plot(ps_plt,fit_cos(ps_plt, *p_int), "b")
ax.vlines(p_int[-1]/p_int[-2],fit_cos(p_int[-1]/p_int[-2]+np.pi,*p_int),fit_cos(p_int[-1]/p_int[-2],*p_int), color="k")

matrix_err_fit=(matrix_err**2/(C_id*A_aus)**2+matrix**2*A_aus_err**2/(A_aus**2*C_id)**2+((matrix/A_aus-0.5)/C_id**2)**2*C_id_err**2)**0.5
matrix_fit=(matrix-A_aus/2)/(A_aus*C_id)+1/2

P0=[300,300, -0.8, 1]
p_tot=np.zeros((len(ps_pos),len(P0)))
err_tot=np.zeros((len(ps_pos),len(P0)))
Im_data_1=np.zeros((len(ps_pos)))
Im_data_err_1=np.zeros((len(ps_pos)))

Im_data_1_fit=np.zeros((len(ps_pos)))
Im_data_err_1_fit=np.zeros((len(ps_pos)))

Im_data_2=np.zeros((len(ps_pos)))
Im_data_err_2=np.zeros((len(ps_pos)))

Im_data_2_fit=np.zeros((len(ps_pos)))
Im_data_err_2_fit=np.zeros((len(ps_pos)))

rho=np.zeros((len(ps_pos)))
chi=ps_pos*w_ps-chi_0
chi_plt=np.linspace(chi[0], chi[-1], 300)
cos2=np.zeros((len(ps_pos)))
cos2_err=np.zeros((len(ps_pos)))
cos2_fit=np.zeros((len(ps_pos)))
cos2_err_fit=np.zeros((len(ps_pos)))

for i in range(len(ps_pos)):
    func_data=matrix[i]
    func_data_err=matrix_err[i]
    func_data_fit=matrix_fit[i]
    func_data_fit_err=matrix_err_fit[i]
    chi_aus=chi[i]
    P0=[np.cos(chi[i]/2)**2, w1(chi[i]).imag*alpha_1, w2(chi[i]).imag*alpha_2, -1, 1]
    # print(P0)
    B0=([0,w1(chi[i]).imag*alpha_1-1000, w2(chi[i]).imag*alpha_2-1000, -2*np.pi, -2*np.pi],[np.inf, w1(chi[i]).imag*alpha_1+1000, w2(chi[i]).imag*alpha_2+1000, 2*np.pi, 2*np.pi])
    p_Im,cov_Im = fit(fit_Im, time, func_data_fit, sigma=func_data_fit_err, p0=P0, bounds=B0)
    err_Im=np.diag(cov_Im)**0.5
    # print(p_Im[-1],p_Im[-2])
    # print(p_Im,err_Im)
    Im_data_1_fit[i]=p_Im[1]/alpha_1
    Im_data_err_1_fit[i]=(err_Im[1]**2/alpha_1**2+alpha_1_err**2*p_Im[1]**2/alpha_1**4)**0.5
    Im_data_2_fit[i]=p_Im[2]/alpha_2
    Im_data_err_2_fit[i]=(err_Im[2]**2/alpha_2**2+alpha_2_err**2*p_Im[2]**2/alpha_2**4)**0.5
    cos2_fit[i]=p_Im[1]*p_Im[0]#*C_id#+p_Im[0]*(1-C_id)/2
    cos2_err_fit[i]=err_Im[1]
    
    yf_data = fft(func_data)
    yf_data_err = np.ones(len(yf_data))*np.sum(matrix_err)**0.5
    # print(sum(abs(yf_data)))
    xf = fftfreq(N, S_F)*1e3
    var=np.sum(np.average(func_data)/2)**0.5
    
    # fig = plt.figure(figsize=(8,6))
    # ax = fig.add_subplot(111)
    # ax.errorbar(time, matrix_fit[i], yerr= matrix_err_fit[i], fmt="ko")
    # ax.plot(time_plt, fit_Im(time_plt, *p_Im))
    # ax.set_title(str("%.2f"%chi[i],))
    # ax.errorbar(xf, np.abs(yf_data), np.abs(yf_data_err), fmt="k.", capsize=5)
    # ax.set_xlim([-5,5])
    
    c_0_data=abs(yf_data[abs(xf)<1/S_F/2]).astype(complex)-A
    c_1_data_1=(yf_data[abs(xf-f_1)<1/S_F/2]).astype(complex)
    c_1_data_2=(yf_data[abs(xf-f_2)<1/S_F/2]).astype(complex)
    
    c_0_data_err=(2*var**2+A_err**2)**0.5
    c_1_data_err_1=var
    c_1_data_err_2=var
    e_mxi_1=np.exp(-1j*(np.angle(c_1_data_1)))
    e_mxi_2=np.exp(-1j*(np.angle(c_1_data_2)))
    # xi_1=2.404544909127107
    # e_mxi_1=np.exp(-1j*(xi_1))
    # xi_2=2.6491221178165554-np.pi/2
    # e_mxi_2=np.exp(-1j*xi_2)
    
    cos2[i]=abs(c_0_data)
    cos2_err[i]=abs(c_0_data_err)
    
    # Im_data_1[i]=np.sign(c_1_data_1.real)*abs(c_1_data_1)/(cos2[i])/alpha_1
    Im_data_1[i]=np.sign(e_mxi_1.real)*abs(c_1_data_1)/(cos2[i])/alpha_1
    Im_data_err_1[i]=(abs(c_1_data_err_1/cos2[i])**2 + ((abs(c_1_data_1)/cos2[i]**2)*cos2_err[i])**2+(abs(c_1_data_1)/cos2[i]/alpha_1*alpha_1_err)**2)**0.5/abs(alpha_1)
    Im_data_2[i]=np.sign(e_mxi_2.real)*abs(c_1_data_2)/(cos2[i])/alpha_2
    Im_data_err_2[i]=(abs(c_1_data_err_2/cos2[i])**2 + (abs((c_1_data_2*e_mxi_2)/cos2[i]**2)*cos2_err[i])**2+abs((c_1_data_2*e_mxi_2)/cos2[i]/alpha_2*alpha_2_err)**2)**0.5/abs(alpha_2)

psi_p=(a_1+np.exp(1j*chi)*a_2)/(2**0.5)
psi_m=(a_1-np.exp(1j*chi)*a_2)/(2**0.5)
M=np.abs(psi_p/psi_m)
th= np.angle(psi_p/psi_m)
pi_shift=[*np.arange(7,22),*np.arange(8,15)]
cos2pi=-cos2+np.amax(cos2)
M[:15]=(cos2[:15]/cos2[pi_shift[:15]])**0.5
# M=(cos2/cos2pi)**0.5
M_err=M**0.5*((cos2_err/cos2)**2+(cos2_err[pi_shift]/cos2[pi_shift])**2)**0.5
Re_1=Im_data_1[pi_shift]/(M*np.sin(th))-Im_data_1/np.tan(th)
Re_err_1=((Im_data_err_1[pi_shift]/(M*np.sin(th)))**2+(Im_data_1[pi_shift]/(M**2*np.sin(th)))**2*M_err**2+(Im_data_err_1/np.tan(th))**2)**0.5
Re_2=-Im_data_2/np.tan(th)-Im_data_2[pi_shift]/(M*np.sin(th))
Re_err_2=((Im_data_err_2[pi_shift]/(M*np.sin(th)))**2+(Im_data_2[pi_shift]/(M**2*np.sin(th)))**2*M_err**2+(Im_data_err_2/np.tan(th))**2)**0.5

ylim_re_1=0
ylim_re_2=8
y_re_labels=np.arange(ylim_re_1,ylim_re_2-0.5,1)
ylim_im_1=-4
ylim_im_2=4
y_im_labels=np.arange(ylim_im_1+1,ylim_im_2,1)

y1=0.512
y2=0.135
xlim1=chi[0]-0.2
xlim2=chi[-7]-0.2
d=0.02
h=0.05
fig = plt.figure(figsize=(5,7))
gs = fig.add_gridspec(3,2, height_ratios=(7,1, 6), hspace=0.0,wspace=0.0)
# ax_aus=fig.add_subplot(gs[1:, 0])
# ax_aus.tick_params(axis="both", bottom=False, labelbottom=False,left=False, labelleft=False,)

axsl = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[1:, 0])]
axsl[0].tick_params(axis="x", bottom=False, labelbottom=False)
axsl[0].set_title("$w_{+,1}$")#"a_2/a_1\\approx$"+str("%.2f" % (a_21),)+")")
colors=["k","#f10d0c","#00a933","#5983b0"]

axsl[0].errorbar(chi, Im_data_1, Im_data_err_1, fmt=".", color=colors[0], capsize=3, label="$\Im(w_{1,+})$ data")
axsl[0].plot(chi_plt, w1(chi_plt).imag, "--",color=colors[0], alpha=0.5, label="$\Im(w_{1,+})$ theory")
axsl[0].set_ylim([ylim_im_1,ylim_im_2])
axsl[0].set_yticks(ticks=y_im_labels)
axsl[0].grid(True, ls="dotted")
axsl[0].set_xlim([chi[0]-0.2,chi[-1]+0.2])
# axsl[0].yaxis.set_label_position("right")
# axsl[0].set_ylabel("$w^\Im_{+,1}$", fontsize=12, rotation=270, va="bottom", ha="center")
axsl[0].yaxis.set_label_coords(-0.2,0.5)
axsl[0].set_ylabel("Imaginary part", fontsize=12)

axsl[1].errorbar(chi[:-7], Re_1[:-7], Re_err_1[:-7], fmt=".", color=colors[2], capsize=3, label="$\Im(w_{1,+})$ data")
axsl[1].plot(chi_plt[chi_plt<xlim2], w1(chi_plt).real[chi_plt<xlim2], "--", color=colors[2], alpha=0.5, label="$\Im(w_{1,+})$ theory")
axsl[1].grid(True, ls="dotted")
axsl[1].set_xlim([chi[0]-0.2,chi[-1]+0.2])
# axsl[1].yaxis.set_label_position("right")
# axsl[1].set_ylabel("$w^\Re_{+,1}$", fontsize=12, rotation=270, va="bottom", ha="center")
axsl[1].yaxis.set_label_coords(-0.2,0.5)
axsl[1].set_ylabel("Real part", fontsize=12)
axsl[1].set_ylim([ylim_re_1,ylim_re_2])
axsl[1].set_yticks(ticks=y_re_labels)
axsl[1].set_xlabel("$\mathrm{\\chi$ [rad]")

ylim_re_1=-7.5
ylim_re_2=2.5
y_re_labels=np.arange(ylim_re_1,ylim_re_2,2.5)
ylim_im_1=-4
ylim_im_2=4
y_im_labels=np.arange(ylim_im_1+1,ylim_im_2,1.5)

ax_aus=fig.add_subplot(gs[1:, 1])
ax_aus.tick_params(axis="both", bottom=False, labelbottom=False,left=False, labelleft=False)
ax_aus.yaxis.set_label_position("right")
# ax_aus.set_ylabel("$w^\Re_{+,2}$", fontsize=12, rotation=270, va="bottom", ha="center")
axsr = [fig.add_subplot(gs[1, 1]),fig.add_subplot(gs[2, 1]),fig.add_subplot(gs[0, 1])]
axsr[0].spines["bottom"].set_visible(False)
axsr[1].spines["top"].set_visible(False)

axsr[0].tick_params(axis="x", bottom=False, labelbottom=False)
axsr[2].tick_params(axis="x", bottom=False, labelbottom=False)
axsr[2].set_title("$w_{+,2}$")#"\t$(a_2/a_1\\approx$"+str("%.2f" % (a_21),)+")")
colors=["k","#f10d0c","#00a933","#5983b0"]
for ax in axsr[:-1]:
    ax.errorbar(chi[:-7], Re_2[:-7], Re_err_2[:-7], fmt=".", color=colors[3], capsize=3, label="$\Im(w_{1,+})$ data")
    ax.plot(chi_plt[chi_plt<xlim2], w2(chi_plt).real[chi_plt<xlim2], "--", color=colors[3], alpha=0.5, label="$\Im(w_{1,+})$ theory")
    ax.grid(True, ls="dotted")
    ax.set_xlim([chi[0]-0.2,chi[-1]+0.2])
    ax.tick_params(axis="y", left=False, labelleft=False, right=True, labelright=True)
axsr[2].tick_params(axis="y", left=False, labelleft=False, right=True, labelright=True)
axsr[2].errorbar(chi, Im_data_2, Im_data_err_2, fmt=".", color=colors[1], capsize=3, label="$\Im(w_{2,+})$ data")
axsr[2].plot(chi_plt, w2(chi_plt).imag, "--",color=colors[1], alpha=0.5, label="$\Im(w_{2,+})$ theory")
axsr[2].set_ylim([ylim_im_1,ylim_im_2])
axsr[2].set_yticks(ticks=y_im_labels)
axsr[2].grid(True, ls="dotted")
axsr[2].set_xlim([chi[0]-0.2,chi[-1]+0.2])
axsr[2].yaxis.set_label_position("right")
# axsr[2].set_ylabel("$w^\Im_{+,2}$", fontsize=12, rotation=270, va="bottom", ha="center")

axsr[0].set_ylim([ylim_re_2,np.amax(Re_2)*1.5])
axsr[1].set_ylim([ylim_re_1,ylim_re_2])
# axsr[1].set_yticks(ticks=ylabels)
axsr[1].set_xlabel("$\\chi$ [rad]")

with open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Results txt/No In/Wv12_Im No In"+inf_file_name[-10:]+".txt","w") as f:
    np.savetxt(f,np.transpose([chi,Im_data_1,Im_data_err_1,Im_data_2,Im_data_err_2]), header="chi w_im1 w_im1_err w_im2 w_im2_err")
with open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Results txt/No In/Wv12_Re No In"+inf_file_name[-10:]+".txt","w") as f:
    np.savetxt(f,np.transpose([chi,Re_1,Re_err_1,Re_2,Re_err_2]), header="chi w_re1 w_re1_err w_re2 w_re2_err")

with open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Paper/Results txt/No In/cos2 No In"+inf_file_name[-10:]+".txt","w") as f:
    np.savetxt(f,np.transpose([ps_pos,cos2,cos2_err]), header="chi cos2 cos2err")

plt.show()