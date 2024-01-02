# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 18:41:54 2023

@author: S18
"""

"""
inf_file_names:
"TOF_vs_chi_S2_ifg_29Aug1924",
"""

import os
import numpy as np
from scipy.special import jv
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
f_1=20
c_1=10
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

def j0_fit(x, a, b, c):
    w=f_1*2*np.pi
    a_1=mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2)
    return c +abs(a*jv(0,a_1*b*x))

def j1_fit(x, a, b):
    w=f_1*2*np.pi
    a_1=mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2)
    return abs(a*jv(1,a_1*b*x))

def j2_fit(x, a, b):
    w=f_1*2*np.pi
    a_1=mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2)
    return abs(a*jv(2,a_1*b*x))

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)


def I_px(t, A, B, alpha, xi_0):
    I = A+B*np.cos(np.pi/4+alpha*np.sin(2*np.pi*1e-3*f_1*t-xi_0))
    return I

inf_file_names=["TOF_S2_alpha_ifg_resonance_10Sep1913"]#,"TOF_A1_alpha_ifg_08Sep1959"]
for inf_file_name in inf_file_names:
    print(inf_file_name)
    sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/exp_3-16-14/Sorted data/Alpha Fourier/"+inf_file_name
    cleandata=sorted_fold_path+"/Cleantxt"
    i=0
    j=0
    for root, dirs, files in os.walk(cleandata, topdown=False):
        files=np.sort(files)
        ps_pos=np.array([])
        w_ps=np.array([])
        chi_0=np.array([])
        bg=np.array([])
        p1=np.array([])
        for name in files:
            if "ifg_" not in name:
                if i==0:
                    tot_data=np.loadtxt(os.path.join(root, name))[11:-1,:]
                    time=tot_data[:,1]
                    f_1=tot_data[0,-3]*1e-3
                    ps_pos=np.append(ps_pos, tot_data[0,-1])
                    print(f_1)
                    i+=1
                else:
                    data=np.loadtxt(os.path.join(root, name))[11:-1,:]
                    ps_pos=np.append(ps_pos, data[0,-1])
                    tot_data = np.vstack((tot_data, data))
                    
            else:
                # print(name)
                tot_data_ifg=np.loadtxt(os.path.join(root, name))
                data_ifg=tot_data_ifg[:,2]+tot_data_ifg[:,5]
                data_ifg_err=data_ifg**0.5
                ps_pos_ifg=tot_data_ifg[:,0]
                P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, -0.7*j]
                B0=([np.amin(data_ifg),0,0.01,-20],[np.amax(data_ifg),np.amax(data_ifg),5, 20])
                p,cov=fit(fit_cos, ps_pos_ifg, data_ifg, p0=P0,  bounds=B0)
                bg=np.append(bg, p[0]-p[1])
                p1=np.append(p1, p[1])
                # err=np.diag(cov)**0.5
                # print(p[3], err[3])
                w_ps=np.append(w_ps, p[-2])
                chi_0=np.append(chi_0, p[-1])
                x_plt = np.linspace(ps_pos_ifg[0], ps_pos_ifg[-1],100)
                fig = plt.figure(figsize=(8,6))
                ax = fig.add_subplot(111)
                fig.suptitle(name[:-4]+"\t"+ str("%.2f" % ((ps_pos[j]*w_ps[j]-chi_0[j])/np.pi) ,))
                ax.errorbar(ps_pos_ifg,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                ax.plot(x_plt,fit_cos(x_plt, *p), "b")
                ax.vlines(p[-1]/p[-2],fit_cos(p[-1]/p[-2]+np.pi,*p),fit_cos(p[-1]/p[-2],*p), color="k")
                ax.vlines(ps_pos[j],fit_cos(p[-1]/p[-2]+np.pi,*p),fit_cos(ps_pos[j],*p), color="r")
                # ax.set_ylim([0,1500])
                # print("C=", p[1]/p[0])
                # print("w_ps=", p[-2])
                # print("chi_0=", p[-1])
                j+=1
                
    # w_ps[9]=w_ps[8]
    # chi_0[9]=chi_0[8]
    amplitude=tot_data[::len(time),5]
    # print(len(amplitude))
    ps_pos=tot_data[::len(time),-1]
    # ps_pos[9]=ps_pos[8]
    # print(ps_pos)
    chi=ps_pos*w_ps-chi_0
    # current=np.array([0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8])/2
    current=np.array([1.2, 1.76, 3.6, 5.8, 7.3, 10.3, 13.6, 16.4])/2
    # print(amplitude)
    N = len(time)
    S_F=1/3
    matrix=np.zeros((len(amplitude),len(time)))
    matrix_err=np.zeros((len(amplitude),len(time)))
    for i in range(len(amplitude)):
        matrix[i]=tot_data[:,4][tot_data[:,5]==amplitude[i]]
        matrix_err[i]=matrix[i]**0.5
    P0=[300,300, -0.8, 1]
    p_tot=np.zeros((len(amplitude),len(P0)))
    err_tot=np.zeros((len(amplitude),len(P0)))
    c_0=np.zeros((len(amplitude)))
    c_0_data=np.zeros((len(amplitude)))
    c_1=np.zeros((len(amplitude)))
    c_1_data=np.zeros((len(amplitude)))
    c_2=np.zeros((len(amplitude)))
    c_2_data=np.zeros((len(amplitude)))
    J_0=np.zeros((len(amplitude)))
    J_1=np.zeros((len(amplitude)))
    J_2=np.zeros((len(amplitude)))
    for i in range(len(amplitude)):
        func_data=matrix[i][10:-10]
        P0=[1000, 500, -3, -1.3]
        B0=([0,0, -30, -2*np.pi],[10000, 10000, 30, 2*np.pi])
        # p,cov=fit(I_px, time[10:-10], func_data, p0=P0,  bounds=B0)
        print(p)
        P0=p.copy()
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        ax.set_title(str("%.2f"%amplitude[i],))
        ax.errorbar(time,matrix[i],yerr=matrix_err[i],fmt="ko",capsize=5, ms=3)
        # ax.plot(time, I_px(time,*p), "b-")
        
        func_data-=bg[i]
        func_data/=2*p1[i]
        # fig = plt.figure(figsize=(8,6))
        # ax = fig.add_subplot(111)
        # ax.set_title(str("%.2f"%amplitude[i],))
        # ax.errorbar(time,matrix[i],yerr=matrix_err[i],fmt="ko",capsize=5, ms=3)
        # ax.plot(time, I_px(time,*p), "b-")
        yf_data = fft(func_data)
        xf = fftfreq(N-20, S_F)
        if i==0:
            x_1=xf[xf>0][abs(yf_data[xf>0])==np.amax(abs(yf_data[xf>0]))]
            # print(x_1)
        c_2_data[i]=abs((yf_data[abs(xf-2*x_1)<1/(6*N)]/(100*N)).astype(complex))
        c_1_data[i]=abs((yf_data[abs(xf-x_1)<1/(6*N)]/(100*N)).astype(complex))
        c_0_data[i]=abs((yf_data[abs(xf)<1/(6*N)]/(100*N)).astype(complex))
        # print(c_1_data[i], c_2_data[i])
        # ax.plot(x,func, "k-")
        # ax.plot(x,func_data, "r--")
        # ax.set_xlim([-0.5,0.5])
        # ax.set_ylim([0,0.005])
    chi=np.pi/4
    J_0=(2*c_0_data-8)/abs(np.cos(chi))
    J_1=2*c_1_data/abs(np.sin(chi))
    J_2=2*c_2_data/abs(np.cos(chi))
    points=range(len(J_0))#[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    P0=[10,5]
    p0,cov0=fit(j0_fit, current[:-1], abs(J_0[:-1]), p0=[10,5,0], bounds=([0,0,0],[100,50, 20]))
    p1,cov1=fit(j1_fit, current[:-1], abs(J_1[:-1]), p0=P0, bounds=([0,0],[100,50]))
    p2,cov2=fit(j2_fit, current[:-1], abs(J_2[:-1]), p0=P0, bounds=([0,0],[100,50]))
    print(p0, p1,p2)
    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)
    ax.plot(current*p1[1], abs(J_0)/np.amax(abs(J_0)), "go")
    ax.plot(current*p1[1], abs(J_2)/p2[0], "ko")
    ax.plot(current*p1[1], abs(J_1)/p1[0], "ro")
    c_plt= np.linspace(0,8,150)
    ax.plot(c_plt*p1[1], j0_fit(c_plt,1, p1[1], 0), "g-")
    ax.plot(c_plt*p1[1], j1_fit(c_plt,1, p1[1]), "r-")
    ax.plot(c_plt*p1[1],  j2_fit(c_plt, 1, p1[1]), "k-")
    # ax.plot(amplitude, J_2, "bo")
    # ax.set_ylim([-10,10])
    fig = plt.figure(figsize=(6,8))
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