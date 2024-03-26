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
a_1=1/2**0.5
a_2=1/2**0.5

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def fit_cos_unb(x, A, C, D, Co): 
    return A/2*(1 + 2*Co*a_1*a_2*np.cos(C*x-D))
inf_file_names=[
"ifgPS1_PS2_42pt_19Mar2322", 
]
a_21=1/2

def w1(chi, a_21):
    return 1/(1+a_21*np.exp(1j*chi))

def w2(chi, a_21):
    return 1-w1(chi, a_21)

for inf_file_name in inf_file_names:
        print(inf_file_name)
        sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/exp_CRG-3125/Sorted data/Ifg/"+inf_file_name
        cleandata=sorted_fold_path+"/Cleantxt"
        chi_0=[0, np.pi/2, np.pi, 3*np.pi/2]
        i=0
        A_avg=0
        Dchi=np.zeros(4)
        C_avg=0
        for root, dirs, files in os.walk(cleandata, topdown=False):
            files=np.sort(files)
            data_ifg_matrix=np.zeros((4,42))
            for name in files:
                # print(name)
                tot_data=np.loadtxt(os.path.join(root, name))
                data_ifg=tot_data[:,2]
                data_ifg_matrix[i]=data_ifg
                data_ifg_err=data_ifg**0.5
                ps_pos=tot_data[:,0]
                P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, -0.1+chi_0[i]]
                B0=([np.amin(data_ifg),0,0.01,-3],[np.amax(data_ifg)*2,np.amax(data_ifg)*2,5, 20])
                p,cov=fit(fit_cos, ps_pos, data_ifg, p0=P0,  bounds=B0)
                # P0_unb=[100000, 3, -0.5, 0.7]
                # B0_unb=([0,1,-10, 0],[1e10,4,10,1])
                # p_unb,cov_unb=fit(fit_cos_unb, ps_pos, data_ifg, p0=P0_unb,  bounds=B0_unb)
                err=np.diag(cov)**0.5
                A_avg+=p[0]/4
                C_avg+=p[1]/p[0]/4
                x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
                fig = plt.figure(figsize=(8,6))
                ax = fig.add_subplot(111)
                fig.suptitle(name[:-4])
                ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                ax.plot(x_plt,fit_cos(x_plt, *p), "b")
                # # ax.set_ylim([0,1500])
                # print("C=", p[1]/p[0], "+-", ((err[1]/p[0])**2+(err[1]*p[1]/p[0]**2)**2)**0.5)
                # print("C_unb=", p_unb[-1])
                # print(p_unb)
                # print("w_ps=", p[-2], "+-", err[-2])
                # print("chi_0=", p[-1])
                Dchi[i]=p[3]
                print(p[3])
                if i==0:
                    chi=ps_pos*p[2]-p[3]
                i+=1
        print(abs(Dchi-Dchi[[1,2,3,0]]))
        print("C_avg=",C_avg, "C_ideal=", C_avg/0.8, C_avg/0.77)
        data_ifg_matrix-=A_avg*(1-C_avg/0.8)
        chi_plt=np.linspace(chi[0], chi[-1], 1000)
        Im=(data_ifg_matrix[3]-data_ifg_matrix[1])/data_ifg_matrix[0]/4
        err_Im=0#((data_ifg_matrix[3]+data_ifg_matrix[1])/data_ifg_matrix[0]**2+Im**2/data_ifg_matrix[0])**0.5/4
        fig = plt.figure(figsize=(8,6))
        fig.suptitle(inf_file_name[:-4])
        ax = fig.add_subplot(111)
        ax.errorbar(chi,Im, err_Im, fmt="ko", capsize=0)
        ax.plot(chi_plt, w1(chi_plt, a_21).imag, "b" )
        # plt.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Report/Images/Imaginary17Mar1718.pdf", format="pdf",bbox_inches="tight")
        
        Re=(1+(data_ifg_matrix[2]/data_ifg_matrix[0]-4*Im**2)**0.5)/2
        fig = plt.figure(figsize=(8,6))
        fig.suptitle(inf_file_name[:-4])
        ax = fig.add_subplot(111)
        ax.plot(chi,Re, "ko")
        ax.plot(chi_plt, w1(chi_plt, a_21).real, "b" )
        # plt.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Report/Images/Real17Mar1718.pdf", format="pdf",bbox_inches="tight")
        plt.show()