# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 14:46:59 2023

@author: S18
"""

import warnings
from scipy.optimize import curve_fit as fit
from PIL import Image as im
import os
import numpy as np
import shutil
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib.gridspec import GridSpec
from scipy.stats import chisquare
plt.rcParams.update({'figure.max_open_warning': 0})
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

mu_N=-9.6623651#*1e-27 J/T
hbar= 6.62607015/(2*np.pi) #*1e-34 J s
f1=10
B1=10
v0=2060.43 #m/s
phi1=0
phi2=0
order=4
w_ps=3

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def I_O_co(t, chi, C, T, B1):
    a1=alpha(T,f1,B1)
    return C*(1+np.cos(chi-a1*np.sin(t)))/2

# # def I_O_in(t, chi, eta, alpha, gamma):
# #     return eta*(np.cos((alpha+t)/2)**2+(a2/a1)**2*np.cos(t/2)**2)/4
# def I_O_in(t, chi, eta, alpha, gamma):
#     px1=np.cos(gamma/2)*np.cos((alpha+t)/2)+1j*np.sin(gamma/2)*np.sin((alpha+t)/2)
#     px2=np.cos(gamma/2)*np.cos(t/2)+1j*np.sin(gamma/2)*np.sin(t/2)
#     return eta*((a1)**2*np.abs(px1)**2+(a2)**2*np.abs(px2)**2)/2



def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)




rad=np.pi/180
inf_file_name="TOF_test_vs_chi_25Aug0536"
sorted_fold_path="C:/Users/S18/Desktop/Grenoble-2023 Ismaele/Grenoble 3rd round/exp_3-16-14/Sorted data/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"
i=0
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    for name in files:
        if i==0:
            tot_data=np.loadtxt(os.path.join(root, name))
            time=tot_data[:,1]
            i=1
        else:
            data=np.loadtxt(os.path.join(root, name))
            tot_data = np.vstack((tot_data, data))
ps_pos=tot_data[::len(time),-1]
# print(time)
matrix=np.zeros((len(ps_pos),len(time)))
matrix_err=np.zeros((len(ps_pos),len(time)))
for i in range(len(ps_pos)):
    matrix[i]=tot_data[:,4][tot_data[:,-1]==ps_pos[i]]
    matrix_err[i]=matrix[i]**0.5

w_pss=np.zeros(len(time))
ps_0s=np.zeros(len(time))
p=[0,0]
for i in range(len(time)):
    ps_data=matrix[:,i]
    P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3,p[-1]]
    B0=([0,0,0,-3*np.pi],[np.inf,np.inf,5,3*np.pi])
    p,cov=fit(fit_cos,ps_pos,ps_data, p0=P0, bounds=B0)
    print(p)
    x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111)
    ax.errorbar(ps_pos,ps_data,yerr=np.sqrt(ps_data),fmt="ko",capsize=5)
    ax.plot(x_plt,fit_cos(x_plt, *p), "b")
    ax.vlines(p[-1]/p[-2],0,fit_cos(p[-1]/p[-2], *p),ls="dashed")
    w_pss[i]=p[-2]
    ps_0s[i]=p[-1]
w_ps=np.average(w_pss)
ps_0=np.average(ps_0s)
plt.show()

# C = 0.67
# # eta = 1-C

# def fit_I_O(x, phi1, chi0, T, B1, A):
#     chi = w_ps*ps_pos-chi0
#     xi1=phi1+(2*np.pi*f1*1e-3*T+np.pi)/2-2*np.pi*f1*1e3/v0
#     t=2*np.pi*1e-3*f1*time+xi1
#     chi = w_ps*ps_pos-chi0
#     t, chi = np.meshgrid(t, chi)
#     fit_I_O = A*(I_O_co(t,chi, C, T, B1))
#     # print(fit_I_O)
#     return fit_I_O.ravel()

# P0 = (0, ps_0, 10, 10, 100)
# B0 = ([0, 0, 0, 0, 0], [100, 100, 50, 50, 100])
# # p, cov = fit(fit_I_O, range(len(matrix.ravel())), matrix.ravel()/np.amax(matrix.ravel()), bounds=B0)
# # print(p)
# # fig = plt.figure(figsize=(10, 5))
# # ax = fig.add_subplot(111)
# # ax.plot(fit_I_O(0, *p)*np.amax(matrix.ravel()), "b")
# # ax.plot(matrix.ravel(), "r--")
# # ax.errorbar(np.arange(len(matrix.ravel())),matrix.ravel(), yerr=matrix_err.ravel(), fmt="ko", capsize=3, lw=1)
# # ax.set_xlim([0,100])
# f_obs=matrix.ravel()
# # f_exp=fit_I_O(0,*p)*np.amax(matrix.ravel())

# # # f_obs/=np.sum(f_obs)
# # # f_exp/=np.sum(f_exp)


# fig = plt.figure(figsize=(10, 10))
# ax = plt.axes(projection='3d')
# time, ps_pos = np.meshgrid(time, ps_pos)
# Z = matrix
# # Z=I_O_co(t, chi, C, alpha, t)+I_O_in(t, chi, eta, alpha, t)
# ax.contour3D(time, ps_pos, Z, 40, cmap='binary')
# # ax.contour3D(t, chi, Z1, 40, cmap='plasma')  # cmap='Blues')
# ax.set_xlabel('$\\t$')
# ax.set_ylabel('$\chi$')
# ax.set_zlabel('z')
# ax.view_init(40, 45)
# plt.show()


# corrected_matrix=Z-(Z1-Z2)#
# corrected_matrix_err=matrix_err
# for i in range(len(ps_pos)):
#     data_txt=np.array([time, corrected_matrix[i], corrected_matrix_err[i], np.ones(len(time))*ps_pos[i]])
#     with open(correct_fold_path+"/t_ps_"+str("%02d" % (i,))+".txt", 'w') as f:
#         np.savetxt(f, np.transpose(data_txt),  header= "time_pos O-Beam err ps_pos", fmt='%.7f %.7f %.7f %.7f' )

