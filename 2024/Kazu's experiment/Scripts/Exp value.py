# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:37:41 2023

@author: S18
"""
"""
inf_file_names:

"""


import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
a_1=1/2**0.5
a_2=1/2**0.5
sgn=1
def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def s_x(x, r, th):
    return r*(np.cos(th)+np.sin(phi)*np.cos(th))

def s_y(x, r, th):
    return r*(np.cos(th)+np.sin(phi)*np.cos(th))

def s_z(x, r, th):
    return r*np.cos(th)

"""
Rho= |up> 
"""
# fold_name="31012025"
"""
Theta=pi/2
"""
fold_name="phiscan_theta_Pihalf_03022025"
th=np.pi

sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Kazu's experiment/Sorted data/"+fold_name
cleandata=sorted_fold_path+"/Cleantxt"
phi_0=[0, np.pi/2, np.pi, 3*np.pi/2]
i=0
A_avg=0
Dphi=np.zeros(4)
C_avg=0
C_err=0
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    Z_u=np.array([])
    Z_u_err=np.array([])
    Z_m=np.array([])
    Z_m_err=np.array([])
    X_u=np.array([])
    X_u_err=np.array([])
    X_m=np.array([])
    X_m_err=np.array([])
    Y_u=np.array([])
    Y_u_err=np.array([])
    Y_m=np.array([])
    Y_m_err=np.array([])
    for name in files:
        print(name)
        tot_data=np.loadtxt(os.path.join(root, name))
        data_spin=tot_data[:,1]
        data_spin_err=data_spin**0.5
        curr=tot_data[:,0]/100000
        if "Zplus" in name:
            Z_u=np.append(Z_u,data_spin)
            Z_u_err=np.append(Z_u_err,data_spin)
            phi_0=0
        elif "Zminus" in name:
            Z_m=np.append(Z_m,data_spin)
            Z_m_err=np.append(Z_m_err,data_spin)
            phi_0=0
        if "Xplus" in name:
            X_u=np.append(X_u,data_spin)
            X_u_err=np.append(X_u_err,data_spin)
            phi_0=0
        elif "Xminus" in name:
            X_m=np.append(X_m,data_spin)
            X_m_err=np.append(X_m_err,data_spin)
            phi_0=np.pi
        if "Yplus" in name:
            Y_u=np.append(Y_u,data_spin)
            Y_u_err=np.append(Y_u_err,data_spin)
            phi_0=-np.pi/2
        elif "Yminus" in name:
            Y_m=np.append(Y_m,data_spin)
            Y_m_err=np.append(Y_m_err,data_spin)
            phi_0=np.pi/2
        P0=[(np.amax(data_spin)+np.amin(data_spin))/2,(np.amax(data_spin)-np.amin(data_spin))/2, 0.2, phi_0]
        B0=([1,0,0.01,-np.pi],[np.amax(data_spin)+100,np.amax(data_spin)-np.amin(data_spin),1, 2*np.pi])
        p,cov=fit(fit_cos, curr, data_spin,  p0=P0,  bounds=B0)
        print(p)
        # P0_unb=[100000, 3, -0.5, 0.7]
        # B0_unb=([0,1,-10, 0],[1e10,4,10,1])
        # p_unb,cov_unb=fit(fit_cos_unb, curr, data_spin, p0=P0_unb,  bounds=B0_unb)
        # err=np.diag(cov)**0.5
        # A=p[0]
        # C=p[1]/p[0]/4
        # C_err+=p[1]**2/p[0]**4*err[0]**2+err[1]**2/p[0]**2
        # A_err=err[0]**2
        curr_plt = np.linspace(curr[0], curr[-1],1000)
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        fig.suptitle(name)
        ax.errorbar(curr,data_spin,yerr=data_spin_err,fmt="ko",capsize=5, ms=3)
        ax.plot(curr_plt,fit_cos(curr_plt, *p), "b")
        ax.set_ylim([0,np.amax(data_spin+10)])
        # print("C=", p[1]/p[0], "+-", ((err[1]/p[0])**2+(err[1]*p[1]/p[0]**2)**2)**0.5)
        # print("C_unb=", p_unb[-1])
        # print(p_unb)
        # print("w_ps=", p[-2], "+-", err[-2])
        # print("phi_0=", p[-1])
        # Dphi[i]=p[3]
        # # print(p[3])
        # if i==0:
        #     phi=curr*p[2]-p[3]
        #     i+=1
exp_z=(Z_u-Z_m)/(Z_u+Z_m)
exp_z_err=abs(exp_z)*((Z_u+Z_m)/(Z_u-Z_m)**2+(Z_u+Z_m)/(Z_u+Z_m)**2)**0.5

exp_x=(X_u-X_m)/(X_u+X_m)
exp_x_err=abs(exp_x)*((X_u+X_m)/(X_u-X_m)**2+(X_u+X_m)/(X_u+X_m)**2)**0.5

exp_y=(Y_u-Y_m)/(Y_u+Y_m)
exp_y_err=abs(exp_y)*((Y_u+Y_m)/(Y_u-Y_m)**2+(Y_u+Y_m)/(Y_u+Y_m)**2)**0.5

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)

ax.errorbar(curr,exp_z, yerr=exp_z_err, fmt=".", color="r", capsize=3, label="<$\sigma_z$>")
# ax.errorbar(curr_plt,np.cos(p[-2]*curr_plt), fmt="-", color="r")

ax.errorbar(curr,exp_x, yerr=exp_x_err, fmt=".", color="g", capsize=3, label="<$\sigma_z$>")
# ax.errorbar(curr_plt,np.cos(p[-2]*curr_plt), fmt="-", color="r")


ax.errorbar(curr,exp_y, yerr=exp_y_err, fmt=".", color="b", capsize=3, label="<$\sigma_z$>")
# ax.errorbar(curr_plt,np.cos(p[-2]*curr_plt), fmt="b", color="r")
# ax.plot(phi_plt, w1(phi_plt, a_21).imag, "b--", alpha=0.5 )
# ax.errorbar(phi,Im_2, Im_2_err, fmt="g.", capsize=3)
# ax.plot(phi_plt, w2(phi_plt, a_21).imag, "g--", alpha=0.5 )

print(-4.10217517e+02 +8.89085783e+02)
print(-2082-4.1*149/13)
plt.show()