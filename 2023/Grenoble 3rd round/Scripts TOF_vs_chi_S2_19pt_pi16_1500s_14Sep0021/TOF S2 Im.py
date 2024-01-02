#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 16:40:03 2023

@author: aaa
"""

"""
inf_file_names:
"TOF_vs_chi_S2_ifg_29Aug1924", 
"TOF_vs_chi_S2_ifg_30Aug2349",
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
f_2=10
B_2=10
B_0=18.55
T=10
v0=2060.43 #m/s
phi_2=0
order=4
w_ps=3.174960654269423
w_ps_err=0.024073832955880906
rad=np.pi/180
chi=0
chi_0=0.7
Co=0.6590116765538198
Co_err=0.022491135210979854
a=8
a_21=1
a_1=1/2**0.5
a_2=1/2**0.5

inf_file_names=["TOF_vs_chi_S2_19pt_pi16_1500s_14Sep0021",]

# In2, pi/8
# spin up, pi/4
# Un, pi/4
# Un, pi/8

if (inf_file_names[0][21])=="1":
    a=16
alpha_2=0.37/2#np.pi/a #/2.354
alpha_2_err=0.1*alpha_2
def w2(chi):
    return 1-1/(1+a_21*np.exp(1j*chi))

def fit_cos2(x, A, B, C):
    return A+B*np.cos(x/2-C)**2

def fit_cos_unb(x, A, B, C):
    return A*((1 - Co)/2 + Co*(1/2+a_1*a_2*np.cos(B*x-C)))

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

def fit_O_beam(t, A, B, chi, a_2, xi_2):
    # a_2=alpha(T,f_2,B_2)
    # xi_2=phi_2+(2*np.pi*f_2*1e-3*T+np.pi)/2#-2*np.pi*f_2*1e3/v0
    chi_fit=chi
    return A + B*np.cos(chi_fit-a_2*np.sin(2*np.pi*1e-3*f_2*t+xi_2))/2


for inf_file_name in inf_file_names:
    print(inf_file_name, " -> ", "pi/", a, sep="")
    sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/exp_3-16-14/Sorted data/TOF S2/"+inf_file_name
    cleandata=sorted_fold_path+"/Cleantxt"
    niels_path="/home/aaa/Desktop/Niels/Data/"+inf_file_name
    niels_fourier_path="/home/aaa/Desktop/Niels/Fourier/"+inf_file_name
    
    if not os.path.exists(niels_path):
        os.makedirs(niels_path)
    if not os.path.exists(niels_fourier_path):
        os.makedirs(niels_fourier_path)
    
    i=0
    for root, dirs, files in os.walk(cleandata, topdown=False):
        files=np.sort(files)
        # print(files)
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
                Co+= p[1]/p[0]/3
                w_ps+=p[-2]/3
                chi_0+=p[-1]/3
                # print("C=", p[1]/p[0])
                # print("w_ps=", p[-2])
                # print("chi_0=", p[-1])
            else:
                # print(name)
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
    # ps_pos=ps_pos[:-2]
    N = len(time)
    S_F=3
    matrix=np.zeros((len(ps_pos),len(time)))
    matrix_err=np.zeros((len(ps_pos),len(time)))
    for i in range(len(ps_pos)):
        if tot_data[:,4].all()==0:
            matrix[i]=tot_data[:,3][tot_data[:,-1]==ps_pos[i]]
        else:
            matrix[i]=tot_data[:,4][tot_data[:,-1]==ps_pos[i]]
        matrix_err[i]=matrix[i]**0.5
        
    ps_data=np.sum(matrix, axis=1)
    P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, -3]
    B0=([1000,0,0.01,-10],[np.amax(ps_data)+1000,np.amax(ps_data)+1000,5, 10])
    p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
    Co= p[1]/p[0]
    # w_ps=p[-2]
    # chi_0=p[-1]
    print("C=",Co)
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
    ax.errorbar(ps_pos,ps_data, yerr=ps_data**0.5,fmt="ko",capsize=5, ms=3)
    ax.plot(ps_plt,fit_cos(ps_plt, *p), "b")
    ax.vlines(p[-1]/p[-2],fit_cos(p[-1]/p[-2]+np.pi,*p),fit_cos(p[-1]/p[-2],*p), color="k")
    P0=[300,300, -0.8, 1]
    p_tot=np.zeros((len(ps_pos),len(P0)))
    err_tot=np.zeros((len(ps_pos),len(P0)))
    Re_data=np.zeros((len(ps_pos)))
    Re_data_err=np.zeros((len(ps_pos)))
    Im_data=np.zeros((len(ps_pos)))
    Im_data_err=np.zeros((len(ps_pos)))
    rho=np.zeros((len(ps_pos)))
    chi=ps_pos*w_ps-chi_0
    chi_plt=np.linspace(chi[0], chi[-1], 100)
    cos2=np.zeros((len(ps_pos)))
    cos2_err=np.zeros((len(ps_pos)))
    for i in range(len(ps_pos)):
        func_data=matrix[i]
        # print(len(func_data))
        func_data_err=matrix_err[i]
        yf_data = fft(func_data)
        yf_data_err = np.ones(len(yf_data))*np.sum(matrix_err)**0.5
        # print(sum(abs(yf_data)))
        xf = fftfreq(N, S_F)*1e3
        # fig = plt.figure(figsize=(8,6))
        # ax = fig.add_subplot(111)
        # ax.errorbar(time, matrix[i], yerr= matrix_err[i], fmt="ko")
        # ax.set_title(str("%.2f"%chi[i],))
        # ax.errorbar(xf, np.abs(yf_data), np.abs(yf_data_err), fmt="k.", capsize=5)
        # ax.plot(x,func, "k-")
        # ax.vlines(x_1, 0, abs(c_0_data), color="b" )
        # ax.set_xlim([-20,20])
        # ax.set_ylim([0,1500])
        # ax.set_ylim([0,0.005])
        
        if i==0:
            x_1=10#xf[xf>0][abs(yf_data[xf>0])==np.amax(abs(yf_data[xf>0]))]
            print(x_1)
        c_1_data=(yf_data[abs(xf-x_1)<1/S_F/2]).astype(complex)
        c_0_data=abs(yf_data[abs(xf)<1/S_F/2]).astype(complex)-15253.208609221087#-22117.395363815085#-21894.845382878237
        var=np.sum(func_data)**0.5/2
        c_1_data_err=var
        c_0_data_err=var+2066.3222700017036
        
        # print(chi[i], np.angle(c_1_data))
        if np.angle(c_1_data)>0:
            # print("here")
            e_m1xi=np.exp(-1j*(np.angle(c_1_data)))
        else:
            e_m1xi=np.exp(-1j*(np.angle(c_1_data)+np.pi))
        e_m2xi=e_m1xi**2
        
        cos2[i]=abs(c_0_data)
        cos2_err[i]=abs(c_0_data_err)
        
        Im_data[i]=(c_1_data*e_m1xi).real/(cos2[i])/alpha_2
        Im_data_err[i]=(abs(c_1_data_err/cos2[i])**2 + (abs((c_1_data*e_m1xi)/cos2[i]**2)*cos2_err[i])**2+abs((c_1_data*e_m1xi)/cos2[i]/alpha_2*alpha_2_err)**2)**0.5/abs(alpha_2)
        data_txt=np.array([time, func_data,func_data_err ]) 
        # with open(niels_path+"/"+str("%i" %(i),) +".txt", 'w') as f:
        #         np.savetxt(f, np.transpose(data_txt), header= "time(microsec) data err")
        # data_fourier_txt=np.array([xf, np.abs(yf_data)]) 
        # with open(niels_fourier_path+"/"+str("%i" %(i),) +".txt", 'w') as f:
        #         np.savetxt(f, np.transpose(data_fourier_txt), header= "freq abs(c)")
    B0=([0,1,-10],[1000000,4,10])
    p_cos_unb,cov_unb=fit(fit_cos_unb, ps_pos, cos2, p0=[100000,3,-0.5], bounds=B0)
    chi=ps_pos*p_cos_unb[-2]-p_cos_unb[-1]
    chi_plt=np.linspace(chi[0], chi[-1], 100)
    fig = plt.figure(figsize=(8,8), dpi=200)
    ax = fig.add_subplot(211)
    ax1 = fig.add_subplot(212)
    ax.set_title(inf_file_name)
    ax.plot(chi_plt, w2(chi_plt).imag,"b-", label="Im($w_{1,+}$) theory")
    ax.errorbar(chi, Im_data, Im_data_err, fmt="o", capsize=5, color=(0.1,0.1,0.6), label="Im($w_{1,+}$) data")
    ax1.plot(chi_plt, w2(chi_plt).real,"r-", label="Re($w_{1,+}$) theory")
    ax1.errorbar(chi, Im_data/np.tan(chi/2), Im_data_err/np.tan(chi/2), fmt="o", color=(0.6,0.1,0.1), capsize=5, label="Re($w_{1,+}$) data")
    # ax.plot(chi_plt, w2(chi_plt).real,"r-")
    # ax.errorbar(chi, Re_data, Re_data_err, fmt="gv", capsize=5)
    # ax.errorbar(ps_pos, cos2, yerr=cos2_err, fmt="ko", capsize=5, label="$c_0$")
    # ax.plot(chi_plt, fit_cos2(chi_plt,*p_cos2), "b-")
    # ax.plot(ps_plt, fit_cos_unb(ps_plt,*p_cos_unb), "b-", label="Fit")
    ax.legend()
    print("param cos_unb=",p_cos_unb)
    corr_unb=p_cos_unb[0]
    corr_err=(np.diag(cov_unb)**0.5)
    print("correction_unb="+str(p_cos_unb[0]*(1-Co)/2)+" +- "+str(0.5*((abs(1-Co)*corr_err[0])**2+(abs(p_cos_unb[0])*Co_err)**2)**0.5))
    if a_21==1:
        ax.set_ylim([-5,5])  
    
    # fig = plt.figure(figsize=(6,8))
    # param_names=["A", "C", "$\\alpha_2$", "$\\xi_1$"]
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