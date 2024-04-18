# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:37:41 2023

@author: S18
"""
"""
inf_file_names:
a_21=1/sqrt(2)
"ifgPS1_PS2_3p_45pt_17Mar1718",
"ifgPS1_PS2_42pt_In08_18Mar2141", 
"ifgPS1_PS2_42pt_In08_19Mar1120", 
"ifgPS1_PS2_42pt_19Mar1726", 
"ifgPS1_PS2_42pt_19Mar1940", 
"ifgPS1_PS2_42pt_19Mar2054", 
"ifgPS1_PS2_42pt_19Mar2208", 
"ifgPS1_PS2_42pt_19Mar2322", 

a_21=1/2
"ifgPS1_PS2_3p_45pt_In18_18Mar1055",
"ifgPS1_PS2_42pt_20Mar0121", 
"ifgPS1_PS2_42pt_20Mar0235", 
"ifgPS1_PS2_42pt_20Mar0349", 
"ifgPS1_PS2_42pt_20Mar0503", 
"ifgPS1_PS2_42pt_20Mar0617", 
"ifgPS1_PS2_42pt_20Mar0731", 

"""


import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
a_1=0.25**0.5
a_2=0.75**0.5
a_21=a_2/a_1
def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def fit_cos_unb(x, A, C, D, Co): 
    return A/2*(1 + 2*Co*a_1*a_2*np.cos(C*x-D))
inf_file_names=[
"ifg_Indium15", 
]

plot=False
def w1(chi, a_21):
    return 1/(1+a_21*np.exp(1j*chi))

def w2(chi, a_21):
    return 1-w1(chi, a_21)

for inf_file_name in inf_file_names:
        # print(inf_file_name)
        sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round - bis/exp_CRG-3126/Sorted data/Wv from ifg/"+inf_file_name
        cleandata=sorted_fold_path+"/Cleantxt"
        chi_0=[0, np.pi/2, np.pi, 3*np.pi/2]
        i=0
        A_avg=0
        A_4p=0
        A_1p=0
        Dchi=np.zeros(4)
        C_avg=0
        for root, dirs, files in os.walk(cleandata, topdown=False):
            files=np.sort(files)
            data_ifg_matrix_4p=np.zeros((4,35))
            data_ifg_matrix_1p=np.zeros((4,35))
            for name in files:
                # print(name)
                if "_PS2=0_" in name:
                    # print(name)
                    tot_data=np.loadtxt(os.path.join(root, name))
                    
                    ps_pos=tot_data[:,0]
                    data_ifg=tot_data[:,2]
                    if ps_pos[-1]>2.5:
                        data_ifg_matrix_4p[0]+=data_ifg
                    else:
                        data_ifg_matrix_1p[0]+=data_ifg
                    data_ifg_err=data_ifg**0.5

                    P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, 0]
                    B0=([np.amin(data_ifg),0,0.01,-3],[np.amax(data_ifg)*2,np.amax(data_ifg)*2,5, 20])
                    p,cov=fit(fit_cos, ps_pos, data_ifg, p0=P0,  bounds=B0)
                    err=np.diag(cov)**0.5
                    if ps_pos[-1]>2.5:
                        A_4p+=p[0]
                        C_4p=p[1]/p[0]/8
                    else:
                        A_1p+=p[0]
                        C_1p=p[1]/p[0]/16
                    A_avg+=p[0]/len(files)
                    A_avg+=p[0]/len(files)
                    C_avg+=p[1]/p[0]/len(files)
                    x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
                    if plot:
                        fig = plt.figure(figsize=(8,6))
                        ax = fig.add_subplot(111)
                        fig.suptitle(name)
                        ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                        ax.plot(x_plt,fit_cos(x_plt, *p), "b")
        
                    if i==0:
                        if ps_pos[-1]>2.5:
                            chi_4p=ps_pos*p[2]-p[3]
                        else:
                            # print("here")
                            chi_1p=ps_pos*p[2]-p[3]
                        
            
                if "_PS2=90_" in name:
                    i+=1
                    # print(name)
                    tot_data=np.loadtxt(os.path.join(root, name))
                    
                    ps_pos=tot_data[:,0]
                    data_ifg=tot_data[:,2]
                    if ps_pos[-1]>2.5:
                        data_ifg_matrix_4p[1]+=data_ifg
                    else:
                        data_ifg_matrix_1p[1]+=data_ifg
                    data_ifg_err=data_ifg**0.5

                    P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, chi_0[1]]
                    B0=([np.amin(data_ifg),0,0.01,-3],[np.amax(data_ifg)*2,np.amax(data_ifg)*2,5, 20])
                    p,cov=fit(fit_cos, ps_pos, data_ifg, p0=P0,  bounds=B0)
                    err=np.diag(cov)**0.5
                    if ps_pos[-1]>2.5:
                        # A_4p+=p[0]
                        C_4p=p[1]/p[0]/8
                    else:
                        # A_1p+=p[0]
                        C_1p=p[1]/p[0]/16
                    A_avg+=p[0]/len(files)
                    C_avg+=p[1]/p[0]/len(files)
                    x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
                    if plot:
                        fig = plt.figure(figsize=(8,6))
                        ax = fig.add_subplot(111)
                        fig.suptitle(name)
                        ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                        ax.plot(x_plt,fit_cos(x_plt, *p), "b")

                    # print(p[3])
                if "_PS2=180_" in name:
                    # print(name)
                    tot_data=np.loadtxt(os.path.join(root, name))
                    
                    ps_pos=tot_data[:,0]
                    data_ifg=tot_data[:,2]
                    if ps_pos[-1]>2.5:
                        data_ifg_matrix_4p[2]+=data_ifg
                    else:
                        data_ifg_matrix_1p[2]+=data_ifg
                    data_ifg_err=data_ifg**0.5
                    
                    P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, chi_0[2]]
                    B0=([np.amin(data_ifg),0,0.01,-3],[np.amax(data_ifg)*2,np.amax(data_ifg)*2,5, 20])
                    p,cov=fit(fit_cos, ps_pos, data_ifg, p0=P0,  bounds=B0)
                    err=np.diag(cov)**0.5
                    if ps_pos[-1]>2.5:
                        # A_4p+=p[0]
                        C_4p=p[1]/p[0]/8
                    else:
                        # A_1p+=p[0]
                        C_1p=p[1]/p[0]/16
                    A_avg+=p[0]/len(files)
                    C_avg+=p[1]/p[0]/len(files)
                    x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
                    if plot:
                        fig = plt.figure(figsize=(8,6))
                        ax = fig.add_subplot(111)
                        fig.suptitle(name)
                        ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                        ax.plot(x_plt,fit_cos(x_plt, *p), "b")
                    # print(p[3])
                if "_PS2=270_" in name:
                    # print(name)
                    tot_data=np.loadtxt(os.path.join(root, name))
                    
                    ps_pos=tot_data[:,0]
                    data_ifg=tot_data[:,2]
                    if ps_pos[-1]>2.5:
                        data_ifg_matrix_4p[3]+=data_ifg
                    else:
                        data_ifg_matrix_1p[3]+=data_ifg
                    data_ifg_err=data_ifg**0.5
                    
                    P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, chi_0[3]]
                    B0=([np.amin(data_ifg),0,0.01,-3],[np.amax(data_ifg)*2,np.amax(data_ifg)*2,5, 20])
                    p,cov=fit(fit_cos, ps_pos, data_ifg, p0=P0,  bounds=B0)
                    err=np.diag(cov)**0.5
                    if ps_pos[-1]>2.5:
                        # A_4p+=p[0]
                        C_4p=p[1]/p[0]/8
                    else:
                        # A_1p+=p[0]
                        C_1p=p[1]/p[0]/16
                    A_avg+=p[0]/len(files)
                    C_avg+=p[1]/p[0]/len(files)
                    x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
                    if plot:
                        fig = plt.figure(figsize=(8,6))
                        ax = fig.add_subplot(111)
                        fig.suptitle(name)
                        ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                        ax.plot(x_plt,fit_cos(x_plt, *p), "b")
                    # print(p[3])
                
        # print(abs(Dchi-Dchi[[1,2,3,0]]))
        # print("C_4p=",C_avg/(2*a_1*a_2))
        # print("A_4p=",A_avg)
        # data_ifg_matrix_4p-=A_4p*(1-C_avg/(2*a_1*a_2))
        # fig = plt.figure(figsize=(8,6))
        # ax = fig.add_subplot(111)
        # fig.suptitle(name)
        # ax.errorbar(ps_pos, data_ifg_matrix_4p[0],fmt="ko",capsize=5, ms=3)
        # chi_plt_4p=np.linspace(chi_4p[0], chi_4p[-1], 1000)
        # Im=(data_ifg_matrix_4p[3]-data_ifg_matrix_4p[1])/data_ifg_matrix_4p[0]/4
        # err_Im=0#((data_ifg_matrix_4p[3]+data_ifg_matrix_4p[1])/data_ifg_matrix_4p[0]**2+Im**2/data_ifg_matrix_4p[0])**0.5/4
        # fig = plt.figure(figsize=(8,6))
        # fig.suptitle(inf_file_name[:-4])
        # ax = fig.add_subplot(111)
        # ax.errorbar(chi_4p,Im, err_Im, fmt="k.", capsize=0)
        # ax.plot(chi_plt_4p, w1(chi_plt_4p, a_21).imag, "b" )
        # ax.set_ylim(-3,3)

        # Re=(1+abs(data_ifg_matrix_4p[2]/data_ifg_matrix_4p[0]-4*Im**2)**0.5)/2
        # fig = plt.figure(figsize=(8,6))
        # fig.suptitle(inf_file_name[:-4])
        # ax = fig.add_subplot(111)
        # ax.plot(chi_4p,Re, "k.")
        # ax.plot(chi_plt_4p, w1(chi_plt_4p, a_21).real, "r" )
        # ax.set_ylim(0,2)
        # C_avg=0.782
        print("C_1p=",C_avg)
        print("A_1p=",A_avg)
        data_ifg_matrix_1p-=A_1p*(1-C_avg/(2*a_2*a_1))
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        fig.suptitle(name)
        ax.errorbar(ps_pos, data_ifg_matrix_1p[0],fmt="ko",capsize=5, ms=3)
        chi_plt_1p=np.linspace(chi_1p[0], chi_1p[-1], 1000)
        Im=(data_ifg_matrix_1p[3]-data_ifg_matrix_1p[1])/data_ifg_matrix_1p[0]/4
        err_Im=0#((data_ifg_matrix_1p[3]+data_ifg_matrix_1p[1])/data_ifg_matrix_1p[0]**2+Im**2/data_ifg_matrix_1p[0])**0.5/4
        fig = plt.figure(figsize=(8,6))
        fig.suptitle(inf_file_name+" $\Im(w)$")
        ax = fig.add_subplot(111)
        ax.errorbar(chi_1p,Im, err_Im, fmt="k.", capsize=0)
        ax.plot(chi_plt_1p, w1(chi_plt_1p, a_21).imag, "b" )
        ax.set_ylim(-3,3)

        Re=(1-(data_ifg_matrix_1p[2]/data_ifg_matrix_1p[0]-4*Im**2)**0.5)/2
        fig = plt.figure(figsize=(8,6))
        fig.suptitle(inf_file_name+" $\Re(w)$")
        ax = fig.add_subplot(111)
        ax.plot(chi_1p,Re, "k.")
        ax.plot(chi_plt_1p, w1(chi_plt_1p, a_21).real, "r" )
        ax.set_ylim(-2,1)
        plt.show()