# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 15:33:28 2023

@author: S18
"""

"""
inf_file_names:
"TOF_vs_chi_A1_27Aug2100", 
"TOF_vs_chi_A1_28Aug2011", 
"TOF_vs_chi_A1_ifg_29Aug1207",  
"TOF_vs_chi_A1_ifg_SD_30Aug1745", 
"TOF_vs_chi_A1_ifg_01Sep0509", 
"TOF_vs_chi_A1_ifg_04Sep2204",
"TOF_vs_chi_A1_19pt_07Sep0441", 
"TOF_vs_chi_A1_19pt_09Sep1224", 
"TOF_vs_chi_A1_19pt_10Sep0417", 
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
mu_N=-9.6623651#*1e-27 J/T
hbar= 6.62607015/(2*np.pi) #*1e-34 J s
f_2=15
B_1=10
B_0=18.55
T=10
v0=2060.43 #m/s
phi_1=0
order=4
w_ps=0
rad=np.pi/180
chi=0
chi_0=0
C=0
a=8
a_21=2

# inf_file_names=["TOF_vs_chi_S2+A1_19pt_pi8_1500s_12Sep1404",]
# inf_file_names=["TOF_vs_chi_S2+A1_19pt_pi16_1500s_14Sep0831",]
# inf_file_names=["TOF_vs_chi_S2+A1_19pt_pi8_SD_1500s_15Sep1823",]
# inf_file_names=["TOF_vs_chi_S2+A1_19pt_pi8_In1_1500s_17Sep0632",]
inf_file_names=["TOF_vs_chi_S2+A1_19pt_pi8_In2_1500s_18Sep0800",]
# Un, pi/8

if (inf_file_names[0][24])=="1":
    a=16
alpha_1=-np.pi/a

def w2(chi):
    return 1-(1/(1+a_21*np.exp(1j*chi)))

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def fit_cos2(x, A, B, C):
    return A+B*np.cos(x/2-C)**2

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

def fit_O_beam(t, A, B, a_1, xi_1):
    # a_1=alpha(T,f_2,B_1)
    # xi_1=phi_1+(2*np.pi*f_2*1e-3*T+np.pi)/2#-2*np.pi*f_2*1e3/v0
    chi_fit=chi
    return A + B*np.cos(chi_fit-a_1*np.sin(2*np.pi*1e-3*f_2*t+xi_1))/2

def O_beam_weak(t, chi, alpha_1, xi_1):
    w_re=w2(chi).real
    w_im=w2(chi).imag
    w_abs=np.abs(w2(chi))
    return np.cos(chi/2)**2*(1+alpha_1**2/2*(w_abs**2-w_re)-alpha_1**2/2*(w_abs**2-w_re)*np.cos(2*(2*np.pi*1e-3*f_2*t+xi_1))+2*alpha_1*w_im*np.sin(2*np.pi*1e-3*f_2*t+xi_1))


for inf_file_name in inf_file_names:
    print(inf_file_name, " -> ", "pi/", a, sep="")
    sorted_fold_path="C:/Users/S18/Desktop/Grenoble-2023 Ismaele/Grenoble 3rd round/exp_3-16-14/Sorted data/TOF S2+A1/"+inf_file_name
    cleandata=sorted_fold_path+"/Cleantxt"
    i=0
    for root, dirs, files in os.walk(cleandata, topdown=False):
        files=np.sort(files)
        for name in files:
            if "ifg_20s_" in name:
                print(name)
                tot_data_ifg=np.loadtxt(os.path.join(root, name))
                data_ifg=tot_data_ifg[:,2]+tot_data_ifg[:,5]
                data_ifg_err=data_ifg**0.5
                ps_pos_ifg=tot_data_ifg[:,0]
                P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, 0]
                B0=([np.amin(data_ifg),0,0.01,-10],[np.amax(data_ifg),np.amax(data_ifg),5, 10])
                p,cov=fit(fit_cos, ps_pos_ifg, data_ifg, p0=P0,  bounds=B0)
                # err=np.diag(cov)**0.5
                # print(p[3], err[3])
                x_plt = np.linspace(ps_pos_ifg[0], ps_pos_ifg[-1],100)
                fig = plt.figure(figsize=(8,6))
                ax = fig.add_subplot(111)
                fig.suptitle(name[:-4])
                ax.errorbar(ps_pos_ifg,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                ax.plot(x_plt,fit_cos(x_plt, *p), "b")
                ax.vlines(p[-1]/p[-2],fit_cos(p[-1]/p[-2]+np.pi,*p),fit_cos(p[-1]/p[-2],*p), color="k")
                # ax.set_ylim([0,1500])
                C+= p[1]/p[0]/3
                w_ps+=p[-2]/3
                chi_0+=p[-1]/3
                # print("C=", p[1]/p[0])
                # print("w_ps=", p[-2])
                # print("chi_0=", p[-1])
            else:
                if i==0:
                    tot_data=np.loadtxt(os.path.join(root, name))[1:-1,:]
                    time=tot_data[:,1]
                    f_2=tot_data[0,-3]*1e-3
                    print(f_2)
                    i=1
                else:
                    data=np.loadtxt(os.path.join(root, name))[1:-1,:]
                    tot_data = np.vstack((tot_data, data))
    ps_pos=tot_data[::len(time),-1]
    DURATION=len(time)
    N = len(time)
    S_F=1/3
    matrix=np.zeros((len(ps_pos),len(time)))
    matrix_err=np.zeros((len(ps_pos),len(time)))
    for i in range(len(ps_pos)):
        if tot_data[:,4].all()==0:
            matrix[i]=tot_data[:,3][tot_data[:,-1]==ps_pos[i]]
        else:
            matrix[i]=tot_data[:,4][tot_data[:,-1]==ps_pos[i]]
        matrix_err[i]=matrix[i]**0.5
    
    ps_data=np.sum(matrix, axis=1)
    P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, 0]
    B0=([np.amin(ps_data),0,0.01,-10],[np.amax(ps_data),np.amax(ps_data),5, 10])
    p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
    C= p[1]/p[0]
    w_ps=p[-2]
    chi_0=p[-1]
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
    ax.errorbar(ps_pos,ps_data, yerr=ps_data**0.5,fmt="ko",capsize=5, ms=3)
    ax.plot(x_plt,fit_cos(x_plt, *p), "b")
    P0=[300,300, -0.8, 1]
    p_tot=np.zeros((len(ps_pos),len(P0)))
    err_tot=np.zeros((len(ps_pos),len(P0)))
    Re=np.zeros((len(ps_pos)))
    Re_data=np.zeros((len(ps_pos)))
    Im=np.zeros((len(ps_pos)))
    Im_data=np.zeros((len(ps_pos)))
    rho=np.zeros((len(ps_pos)))
    chi=ps_pos*w_ps-chi_0
    chi_plt=np.linspace(chi[0], chi[-1], 100)
    cos2=np.zeros((len(ps_pos)))
    for i in range(len(ps_pos)):
        # func=O_beam(time,chi[i], 0)
        # yf = fft(func)
        func_data=matrix[i]
        yf_data = fft(func_data)
        xf = fftfreq(N, S_F)
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        ax.errorbar(time, matrix[i], yerr= matrix_err[i], fmt="ko")
        # ax.set_title(str("%.2f"%ps_pos[i],))
        # # ax.plot(xf, np.abs(yf)/(3*N), "k")
        # ax.plot(xf, np.abs(yf_data)/(N), "r--")
        # ax.plot(x,func, "k-")
        # # ax.plot(x,func_data, "r--")
        
        # ax.set_xlim([0,0.15])
        # ax.set_ylim([0,1500])
        # ax.set_ylim([0,0.005])
        # if i==0:
        #     x_1=xf[2:][yf[2:]==np.amax(yf[2:])]
        # a_2=abs((yf[abs(xf-2*x_1)<1/N/6]/N).astype(complex))
        # b_1=abs((yf[abs(xf-x_1)<1/N/6]/N).astype(complex))
        # a_0=abs((yf[abs(xf)<1/N/6]/N).astype(complex))
        # # # Re[i]=1+(0.25-(b_1**2 + 2*a_0*(a_0+2*a_2)**2)/(alpha_1**2*(a_0+2*a_2)**2))**0.5
        # Im[i]=b_1/(a_0+2*a_2)
        if i==0:
            x_1=xf[xf>0][abs(yf_data[xf>0])==np.amax(abs(yf_data[xf>0]))]
            print(x_1)
        c_2_data=(yf_data[abs(xf-2*x_1)<1/N/6]/N).astype(complex)/831.4
        c_1_data=(yf_data[abs(xf-x_1)<1/N/6]/N).astype(complex)/831.4
        c_0_data=(yf_data[abs(xf)<1/N/6]/N).astype(complex)/831.4
        # print(c_0_data)
        xi=np.arctan(c_2_data.imag/c_2_data.real)/2#(np.angle(c_2_data))/2#np.angle(c_2_data)/2#np.arctan(c_1_data.imag/c_1_data.real)
        e_m2xi=np.exp(-2j*abs(xi))#(np.angle(c_2_data)-np.angle(c_1_data))
        # print("xi=",np.angle(c_2_data)-np.angle(c_1_data))
        cos2[i]=c_0_data.real+(2*c_2_data*e_m2xi).real-0.182
        Im_data[i]=abs(c_1_data/(cos2[i])/alpha_1)
        # d=Im_data[i]**2 + 4*(c_2_data*e_m2xi)/(alpha_1**2*cos2[i]) # old
        # d=Im_data[i]**2 - (c_0_data.real/(c_0_data.real+2*abs(c_2_data))-1)*2/alpha_1**2 # new
        # print(chi[i],d)
        # d=Im_data[i]**2 + (2/alpha_1**2)*(1-(c_0_data.real)/cos2[i])
        # print(chi[i], 4*d.real)
        # Re_data[i]=0.5+0.5*(1-4*d.real)**0.5
        # # print(np.amax(abs(yf))/N)
    p_cos2,cov_cos2=fit(fit_cos2, chi, cos2, p0=[100, 800,0], bounds= ([0,0,-3],[1000,1000,3]))
    fig = plt.figure(figsize=(8,6))
    r=abs(w2(chi).imag)/Im_data
    
    ax = fig.add_subplot(111)
    # ax.plot(chi, r, "go")
    ax.plot(chi_plt, abs(w2(chi_plt).imag),"b-")
    ax.plot(chi, Im_data, "ko")
    # ax.plot(chi_plt, abs(w2(chi_plt).real), "r-")
    # ax.plot(chi, Re_data, "ro")
    # ax.plot(chi, cos2, "ko")
    # ax.plot(chi_plt, fit_cos2(chi_plt,*p_cos2), "b-")
    # print(p_cos2)  
    ax.set_ylim([0,5])  
    # fig = plt.figure(figsize=(6,8))
    # param_names=["A", "C", "$\\alpha_1$", "$\\xi_1$"]
    # gs = GridSpec(len(param_names),1, figure=fig, hspace=0, wspace=0)
    # axs=[]
    # for i in range(len(param_names)):
    #     axs.append(fig.add_subplot(gs[i,0]))
    #     axs[i].set_ylabel(param_names[i])
    #     axs[i].errorbar(ps_pos, p_tot[:,i], yerr=err_tot[:,i])
    #     y_min=np.amin(p_tot[:,i])
    #     y_max=np.amax(p_tot[:,i])
    #     axs[i].set_ylim([y_min*(1-np.sign(y_min)*0.1),y_max*(1+np.sign(y_min)*0.1)])
    
plt.show()