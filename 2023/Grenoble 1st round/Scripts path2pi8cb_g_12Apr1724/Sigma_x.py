#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 11:36:09 2024

@author: aaa
"""
import os
import numpy as np
import shutil
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from PIL import Image as im
from scipy.optimize import curve_fit as fit
plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams.update({'figure.max_open_warning': 0})
alpha=np.pi/8
w_ps=8.002
a1 = 1/5**0.5
a2 = 2*a1
a21=a2/a1
C=0.687
def w2p(x,x0):
    return (1-1/(1+a21*np.exp(-1j*(x+x0)))).real

def fit_cos(x,A,B,C,D):
    return A+B*np.cos(C*x-D)

def I_px(beta, chi, C):
    px=((a2*np.cos((alpha+beta)/2))**2+(a1*np.cos(beta/2))**2+C*2*a1*a2*np.cos((alpha+beta)/2)*np.cos(beta/2)*np.cos(chi))/2
    return px

def s_px(beta, chi, C):
    s_x=(I_px(beta, chi, C)-I_px(beta+np.pi, chi, C))/(I_px(beta, chi, C)+I_px(beta+np.pi, chi, C))
    return s_x


rad=np.pi/180
inf_file_name="path2pi8cb_g_12Apr1724"
sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 1st round/exp_3-16-13/Sorted data/"+inf_file_name
correct_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 1st round/exp_3-16-13/Corrected data/"+inf_file_name
beta_fold_clean=correct_fold_path+"/Beta"

i=0
for root, dirs, files in os.walk(beta_fold_clean, topdown=False):
    files=np.sort(files)
    for name in files:
        if i==0:
            tot_data=np.loadtxt(os.path.join(root, name))
            coil=tot_data[:,0]
            i=1
        else:
            data=np.loadtxt(os.path.join(root, name))
            tot_data = np.vstack((tot_data, data))
ps_pos=tot_data[::len(coil),-1]
# ps_i=109
# ps_f=ps_pos[-10]
# ps_pos=ps_pos[abs(ps_pos-(ps_i+ps_f)/2)<(ps_f-ps_i)/2]
# print(tot_data)
matrix=np.zeros((len(ps_pos),len(coil)))
matrix_err=np.zeros((len(ps_pos),len(coil)))
b=np.zeros(len(ps_pos))
beta=np.zeros(len(ps_pos))
w=np.zeros(len(ps_pos))
err_b=np.zeros(len(ps_pos))
# fit_res0=[1.32214076e+03, 1.17144255e+03, 1.31186510e-01, 1.8086273e+00]
fit_res0=[1.32214076e+03, 1.17144255e+03, 1.31186510e-01, 1.8171]
err_res0=[8.10516385e+00, 1.16683697e+01, 3.20540294e-04, 1.75421950e-02]
b0=fit_res0[-1]
for i in range(len(ps_pos)):
    matrix[i]=tot_data[:,1][tot_data[:,-1]==ps_pos[i]]
    matrix_err[i]=tot_data[:,2][tot_data[:,-1]==ps_pos[i]]

ps_data=np.average(matrix, axis=1)
ps_err=np.sum(matrix, axis=1)**0.5/len(coil)
P0_chi=[(np.amax(ps_data)+np.amin(ps_data))/2, np.amax(ps_data)-np.amin(ps_data), 8, 0.09]
B0_chi=([0,10,0,-2*np.pi],[3000,3000,10, 2*np.pi])
p_chi,cov=fit(fit_cos,ps_pos,ps_data, p0=P0_chi, bounds=B0_chi, sigma=ps_err)
chi=p_chi[-2]*ps_pos-p_chi[-1]
chi_plt=np.linspace(chi[0], chi[-1], 100)
x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
ax.errorbar(ps_pos,ps_data,yerr=ps_err,fmt="ko",capsize=5)  
ax.plot(x_plt,fit_cos(x_plt, *p_chi), "b")
ax.vlines((p_chi[-1]+276*np.pi)/p_chi[-2],0,fit_cos(p_chi[-1]/p_chi[-2], *p_chi),ls="dashed")

s_x=np.zeros((len(ps_pos), len(coil)))
i_pi=np.array([*range(14,len(coil)),*range(1,15)])
print(len(coil),len(i_pi))
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
ax.errorbar(coil, matrix[0], yerr=matrix_err[0], fmt="k-o", capsize=5)
ax.errorbar(coil, matrix[0][i_pi], yerr=matrix_err[0][i_pi], fmt="r-o", capsize=5)

w_c=1.32114454e-01
b_0=1.81#0.053

beta=w_c*coil-b_0
coil_plt = np.linspace(coil[0], coil[-1],100)
beta_plt = 1.32114454e-01*coil_plt-b_0

fig = plt.figure(figsize=(5,5), dpi=200)
ax = fig.add_subplot(111)
colors=["r","b","g"]
k=0
w=np.zeros(len(ps_pos))
w_err=np.zeros(len(ps_pos))
for i in range(len(ps_pos)):
        s_x[i]=(matrix[i]-matrix[i][i_pi])/(matrix[i]+matrix[i][i_pi])
        P0=[0, 1, 0.1, 1.8]
        B0=([0,0,0,-10],[5,5,50,2*np.pi])
        p,cov=fit(fit_cos,coil ,s_x[i], p0=P0, bounds=B0)
        err=np.diag(cov)**0.5 
        w[i]=(b_0-p[-1])/alpha
        w_err[i]=2*err[-1]/alpha
        print(p)
        if i==12 or i==17:
            ax.errorbar(beta, s_x[i], fmt="o", color=colors[k], capsize=5, label="$\chi=$"+str("%.2f" % (chi[i]-278*np.pi),)+"\n$\Delta \\beta$="+str("%.2f" % (b_0-p[-1]),)+"\n$w$="+str("%.2f" % ((b_0-p[-1])/alpha),))
            ax.plot(beta_plt, fit_cos(coil_plt,*p), color=colors[k])
            # ax.plot(beta_plt, fit_cos(beta_plt,0,1,1,0), color="y")
            ax.plot(beta_plt, s_px(beta_plt,chi[i],1), color="y")
            
            s_x_c=(s_x[i]/s_px(beta[i], chi[i], C))*s_px(beta[i], chi[i], 1)
            ax.plot(beta, s_x_c, "ok")
            k+=1
ax.legend()

fig = plt.figure(figsize=(5,5), dpi=200)
ax = fig.add_subplot(111)
ax.errorbar(chi,w, yerr=w_err,fmt="ko")
ax.plot(chi_plt,w2p(chi_plt,0),"b")
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
k=0   
for i in range(len(ps_pos)):
    s_x[i]=(matrix[i]-matrix[i][i_pi])/(matrix[i]+matrix[i][i_pi])
    P0=[0, 1, 0.1, 1.8]
    B0=([0,0,0,-10],[5,5,50,2*np.pi])
    p,cov=fit(fit_cos,coil ,s_x[i], p0=P0, bounds=B0)
    err=np.diag(cov)**0.5 
    if i==20 or i==25:
        ax.set_title(ps_pos[i])
        ax.errorbar(beta, s_x[i], fmt="o", color=colors[k], capsize=5)
        ax.plot(beta_plt, fit_cos(coil_plt,*p), color=colors[k],label="$\chi=$"+str("%.2f" % (chi[i]-278*np.pi),)+"\n$\Delta \\beta$="+str("%.2f" % (b_0-p[-1]),)+"\n$w$="+str("%.2f" % ((b_0-p[-1])/alpha),))
        ax.plot(beta_plt, fit_cos(beta_plt,0,1,1,0), color="y")
        k+=1
ax.legend()

plt.show()