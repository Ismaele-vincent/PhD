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

state="$|\\psi_{in}>=(exp(-i60)|1>+|2>+exp(i120)|3>)/\\sqrt{3}$"
a_1=1/3**0.5
a_1_err=0
a_2=1/3**0.5
a_2_err=0
a_3=1/3**0.5
a_3_err=0
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


def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

bad_apples=[
            ]

good_apples=["ifg_wv2_psi_+exp(-i60)+1+exp(i120)_no_fit_21Oct2319" #good prolly
            "ifg_wv2_psi_+exp(-i60)+1+exp(i120)_no_fit_22Oct2237" #good
            "ifg_wv2_psi_+exp(-i60)+1+exp(i120)_no_fit_24Oct1953" #good maybe
             ]

inf_file_names=[
"ifg_wv2_psi_+exp(-i60)+1+exp(i120)_no_fit_24Oct1953" #good maybe
]
# a_21=1/2

def w1(chi_1, chi_2, chi_3):
    return a_1*np.exp(1j*(chi_1_0+chi_1))/(a_1*np.exp(1j*(chi_1_0+chi_1))+a_2*np.exp(1j*(chi_2_0+chi_2))+a_3*np.exp(1j*(chi_3_0+chi_3)))

def w2(chi_1, chi_2, chi_3):
    return a_2*np.exp(1j*(chi_2_0+chi_2))/(a_1*np.exp(1j*(chi_1_0+chi_1))+a_2*np.exp(1j*(chi_2_0+chi_2))+a_3*np.exp(1j*(chi_3_0+chi_3)))

def w3(chi_1, chi_2, chi_3):
    return a_3*np.exp(1j*(chi_3_0+chi_3))/(a_1*np.exp(1j*(chi_1_0+chi_1))+a_2*np.exp(1j*(chi_2_0+chi_2))+a_3*np.exp(1j*(chi_3_0+chi_3)))

def I_corr(A, chi_1, chi_2, chi_3):
    return A/3*(1+2*a_1*a_2*np.cos(chi_1_0+chi_1-chi_2_0-chi_2)+2*a_1*a_3*np.cos(chi_1_0+chi_1-chi_3_0-chi_3) + 2*a_2*a_3*np.cos(chi_2_0+chi_2-chi_3_0-chi_3))

for inf_file_name in inf_file_names:
        print(inf_file_name)
        sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Ifg wv no fit/"+inf_file_name
        cleandata=sorted_fold_path+"/Cleantxt"
        chi_0=[0, np.pi/2, np.pi, 3*np.pi/2]
        
        A_avg=0
        Dchi=np.zeros(4)
        C_avg=0
        C_err=0
        for root, dirs, files in os.walk(cleandata, topdown=False):
            files=np.sort(files)
            data_ifg_matrix=np.zeros((4,points))
            name = files[0]
            # print(name)
            tot_data=np.loadtxt(os.path.join(root, name))[:,1:]
            time_ifg=tot_data[0,1]
            data_ifg=tot_data[:,2]
            data_ifg_matrix[3]=data_ifg
            i=0
            for k in [2,1,3]:
                data_ifg_matrix[i]=np.roll(data_ifg, -4*k)
                i+=1
            # data_ifg_matrix[0]=data_ifg
            # i=0
            # for k in [3,1,2]:
            #     data_ifg_matrix[i+1]=np.roll(data_ifg, -4*k)
            #     i+=1
            data_ifg_err=data_ifg**0.5
            ps_pos=tot_data[:,0]
            P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 6, 1.7]
            B0=([np.amin(data_ifg),0,0.01,-2*np.pi],[np.amax(data_ifg)*2,np.amax(data_ifg)*2,7, 2*np.pi])
            p,cov=fit(fit_cos, ps_pos, data_ifg, sigma=data_ifg_err, p0=P0,  bounds=B0)
            # print(p)
            err=np.diag(cov)**0.5
            A_avg+=p[0]/4
            C_avg+=p[1]/p[0]/4
            C_err+=p[1]**2/p[0]**4*err[0]**2+err[1]**2/p[0]**2
            A_err=err[0]**2
            x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
           
            for k in [0,1,2,3]:
                fig = plt.figure(figsize=(8,6))
                ax = fig.add_subplot(111)
                ax.errorbar(ps_pos,data_ifg_matrix[k],yerr=data_ifg_matrix[k]**0.5,fmt="ko",capsize=5, ms=3)
            fig = plt.figure(figsize=(8,6))
            ax = fig.add_subplot(111)
            fig.suptitle(name[:-4])
            ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
            ax.plot(x_plt,fit_cos(x_plt, *p), "b")
            # ax.set_ylim([0,1500])
            print("C=", p[1]/p[0], "+-", ((err[1]/p[0])**2+(err[1]*p[1]/p[0]**2)**2)**0.5)
            Dchi[i]=p[3]
            # print(p[3])

            chi_2=(ps_pos-ps_pos[0])*p[2]

        chi_2_plt=np.linspace(chi_2[0], chi_2[-1], 1000)
        
        int_data=np.loadtxt(os.path.join(root, files[-1]))[:,3]
        time_int=np.loadtxt(os.path.join(root, files[-1]))[0,2]
        print("path (213) intensities =",int_data)
        T_1=int_data[1]
        T_2=int_data[0]
        T_3=int_data[2]
        a_1=(T_1/(T_1+T_2+T_3))**0.5
        a_2=(T_2/(T_1+T_2+T_3))**0.5
        a_3=(T_3/(T_1+T_2+T_3))**0.5
        # print(abs(Dchi-Dchi[[1,2,3,0]])/np.pi*2)
        C_err=C_err**0.5/4
        A_err=A_err**0.5/4
        # print("A_avg=",A_avg, "+-",A_err)
        
        C_id=1#C_avg/0.8
        C_id_err=(C_err**2+C_avg**2/(a_1**2)*a_1_err**2+C_avg**2/(a_2**2)*a_2_err**2)**0.5/(2*a_1*a_2)
        # print("C_avg=",C_avg, "+-",C_err, "C_ideal=", C_id, "+-", C_id_err)
        A=np.sum(int_data*3*time_ifg/time_int)
        print(A/3*(1+2*(C_13*a_1*a_3*np.cos(chi_1_0+chi_3_0))), np.average(data_ifg_matrix[0]))
        # print(A_avg/(3+2*C_13), A)
        data_ifg_matrix_err=(data_ifg_matrix+((1-C_id)/2)**2*A_err**2+(A_avg/2)**2*C_id_err**2)**0.5
        data_ifg_matrix_err=(data_ifg_matrix/C_id**2+((1/C_id+1)/2)**2*A_err**2+(A_avg/2-data_ifg_matrix)**2*(C_id_err/C_id**2)**2)**0.5
        k=0
        chi_2_0_aux=chi_2_0 
        for i in [1,0,2,3]:
            chi_2_0=chi_2_0_aux-np.pi/2+k*np.pi/2
            data_ifg_matrix[i]+=A/3*(2*(1-C_12)*a_1*a_2*np.cos(chi_1+chi_1_0-chi_2-chi_2_0) + 2*(1-C_13)*a_1*a_3*np.cos(chi_1+chi_1_0-chi_3-chi_3_0) + 2*(1-C_23)*a_2*a_3*np.cos(chi_2+chi_2_0-chi_3-chi_3_0))
            k+=1
        chi_2_0=chi_2_0_aux 
        P2=int_data[1]*time_ifg/time_int
        P2_corr=P2
        P2_corr_err=(C_id**2*P2+P2**2*C_id_err**2)**0.5
        
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        ax.errorbar(chi_2, data_ifg_matrix[0],yerr=data_ifg_matrix[0]**0.5,fmt="ko",capsize=5, ms=3)
        ax.plot(chi_2_plt, I_corr(A, chi_1, chi_2_plt, chi_3))
        
        Re_2=P2_corr/data_ifg_matrix[0] + 1/4 - data_ifg_matrix[3]/(data_ifg_matrix[0]*4)
        Re_2_err=(P2_corr_err**2+(data_ifg_matrix_err[2]/4)**2+(Re_2-1/4)**2*data_ifg_matrix_err[0]**2)**0.5/abs(data_ifg_matrix[0])
        
        Im_2=(data_ifg_matrix[1]-data_ifg_matrix[2])/data_ifg_matrix[0]/4
        Im_2_err=(data_ifg_matrix_err[1]**2+data_ifg_matrix_err[3]**2+(4*Im_2)**2*data_ifg_matrix_err[0]**2)**0.5/(4*abs(data_ifg_matrix[0]))
        
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
        
        # axs[0].errorbar(chi_2,Re_1, Re_1_err, fmt="k.", capsize=3)
        axs[0].errorbar(chi_2_plt, w1(0,chi_2_plt,0).real, color=colors[3], alpha=0.8)
        
        # axs[1].errorbar(chi_2,Im_1, Im_1_err, fmt="k.", capsize=3)
        axs[1].plot(chi_2_plt, w1(0,chi_2_plt,0).imag, color=colors[3], alpha=0.8 )
        
        axs[2].errorbar(chi_2,Re_2, Re_2_err, fmt="k.", capsize=3)
        axs[2].errorbar(chi_2_plt, w2(0,chi_2_plt,0).real, color=colors[3], alpha=0.8)
        
        axs[3].errorbar(chi_2,Im_2, Im_2_err, fmt="k.", capsize=3)
        axs[3].plot(chi_2_plt, w2(0,chi_2_plt,0).imag, color=colors[3], alpha=0.8 )
        
        # axs[4].errorbar(chi_2,Re_1, Re_1_err, fmt="k.", capsize=3)
        axs[4].errorbar(chi_2_plt, w3(0,chi_2_plt,0).real, color=colors[3], alpha=0.8)
        
        # axs[5].errorbar(chi_2,Im_1, Im_1_err, fmt="k.", capsize=3)
        axs[5].plot(chi_2_plt, w3(0,chi_2_plt,0).imag, color=colors[3], alpha=0.8 )
        
        for ax in axs:
            # ax.set_xticks([-2*np.pi,-np.pi,0,np.pi,2*np.pi])
            # ax.set_xticklabels(["$\mathdefault{-2\pi}$","$\mathdefault{-\pi}$", "$\mathdefault{0}$","$\mathdefault{\pi}$","$\mathdefault{2\pi}$"])
            ax.grid(True, ls="dotted")
            ax.set_ylim([-2.5,2.5])
        for ax in axs[2:]:
            ax.set_xlabel("$\mathdefault{\\chi_2}$ [rad]")
            
        plt.show()