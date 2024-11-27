#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 15:03:44 2023

@author: aaa
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

w_ps = 8.002

a1 = 1/5**0.5
a2 = 2*a1


def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def I_px_co(beta, chi, C, alpha):
    px=(a1*np.cos((alpha+beta)/2)+np.exp(1j*chi)*a2*np.cos(beta/2))/2**0.5
    return C*np.abs(px)**2

# def I_px_in(beta, chi, eta, alpha, gamma):
#     return eta*(np.cos((alpha-beta)/2)**2+(a2/a1)**2*np.cos(beta/2)**2)/4
def I_px_in(beta, chi, eta, alpha):
    px1=a1*np.cos((alpha+beta)/2)/2**0.5
    px2=a2*np.cos(beta/2)/2**0.5
    return eta*(np.abs(px1)**2+np.abs(px2)**2)

inf_file_name = "path1pi8cb_g_09Apr1441"
sorted_fold_path = "/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 1st round/exp_3-16-13/Sorted data/"+inf_file_name
cleandata = sorted_fold_path+"/Cleantxt"
beta_fold_clean = cleandata+"/Beta"
plots_fold = sorted_fold_path+"/Plots/"
correct_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 1st round/exp_3-16-13/Corrected data/"+inf_file_name+"/Beta"
if not os.path.exists(correct_fold_path):
    os.makedirs(correct_fold_path)
else:
    shutil.rmtree(correct_fold_path)
    os.makedirs(correct_fold_path)


i = 0
for root, dirs, files in os.walk(beta_fold_clean, topdown=False):
    files = np.sort(files)
    for name in files:
        if i == 0:
            tot_data = np.loadtxt(os.path.join(root, name))
            coil = tot_data[:, 0]
            i = 1
        else:
            data = np.loadtxt(os.path.join(root, name))
            tot_data = np.vstack((tot_data, data))
ps_pos = tot_data[::len(coil), -1]
# ps_i=109
# ps_f=ps_pos[-1]
# ps_pos=ps_pos[abs(ps_pos-(ps_i+ps_f)/2)<(ps_f-ps_i)/2]
matrix = np.zeros((len(ps_pos), len(coil)))
matrix_err = np.zeros((len(ps_pos), len(coil)))
w = np.zeros(len(ps_pos))
err_b = np.zeros(len(ps_pos))
for i in range(len(ps_pos)):
    matrix[i] = tot_data[:, 2][tot_data[:, -1] == ps_pos[i]]
    matrix_err[i] = tot_data[:, 2][tot_data[:, -1] == ps_pos[i]]**0.5
w_pss=np.zeros(len(coil))
ps_0s=np.zeros(len(coil))
for i in range(len(coil)):
    ps_data=matrix[:,i]
    ps_err=matrix_err[:,i]
    P0=[(np.amax(ps_data)+np.amin(ps_data))/2, np.amax(ps_data)-np.amin(ps_data), 8,-np.pi]
    B0=([0,10,0,-np.pi],[3000,3000,10, np.pi])
    p,cov=fit(fit_cos,ps_pos,ps_data, p0=P0, bounds=B0, sigma=ps_err)
    x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
    # fig = plt.figure(figsize=(5,5))
    # ax = fig.add_subplot(111)
    # ax.errorbar(ps_pos,ps_data,yerr=np.sqrt(ps_data),fmt="ko",capsize=5)  
    # ax.plot(x_plt,fit_cos(x_plt, *p), "b")
    # ax.vlines((p[-1]+276*np.pi)/p[-2],0,fit_cos(p[-1]/p[-2], *p),ls="dashed")
    # ax.vlines((p[-1]+276*np.pi-np.pi/2)/p[-2],0,fit_cos(p[-1]/p[-2], *p),ls="dashed", color="r")
    # ax.set_title(p[-1])
    w_pss[i]=p[-2]
    ps_0s[i]=p[-1]
    # print("A=",p[0], ps_pos[9])
w_ps=np.average(w_pss)
ps_0=np.average(ps_0s)
print(w_ps,ps_0)

c_data = np.sum(matrix, axis=0)
P0 = [(np.amax(c_data)+np.amin(c_data))/2, np.amax(c_data)/2, 0.1, coil[0]*0.1]
B0 = ([10, 10, 0.001, 0], [np.inf, np.inf, np.inf, 100])
p, cov = fit(fit_cos, coil, c_data, p0=P0, bounds=B0)
# print(coil)
x_plt = np.linspace(coil[0], coil[-1], 100)
# fig = plt.figure(figsize=(5,5))
# ax = fig.add_subplot(111)
# ax.errorbar(coil,c_data,yerr=np.sqrt(c_data),fmt="ko",capsize=5)
# ax.plot(x_plt,fit_cos(x_plt, *p), "b")
# ax.vlines(p[-1],0,fit_cos(p[-1], *p),ls="dashed")
w_c = p[-2]
# print(w_c)
# print(p[1]/p[0])
# c_0 = p[-1]
c_0 = 1.8086
# beta=np.linspace(-3*np.pi,3*np.pi,500)#coil.copy()#
# chi=np.linspace(-3*np.pi,3*np.pi,500)#ps_pos.copy()#
beta = w_c*coil-c_0
chi = w_ps*ps_pos-ps_0

alpha = np.pi/8
gamma = 0
C = 0.687
eta = 1-C

def fit_I_px(x, A, ps_0, c_0):
    beta = w_c*coil-c_0
    chi = w_ps*ps_pos-ps_0
    beta, chi = np.meshgrid(beta, chi)
    fit_I_px = A*(I_px_co(beta, chi, C, alpha) + I_px_in(beta, chi, eta, alpha))
    # print(fit_I_px)
    return fit_I_px.ravel()

P0 = (1264*2, ps_0, c_0)
B0 = ([0,-np.pi,0], [5000, np.pi,2*np.pi])
p, cov = fit(fit_I_px, range(len(matrix.ravel())), matrix.ravel(), bounds=B0, sigma=matrix_err.ravel())
print(p)
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
ax.plot(fit_I_px(0, *p), "bo")
ax.plot(matrix.ravel(), "r-")
# ax.errorbar(np.arange(len(matrix.ravel())),matrix.ravel(), yerr=matrix_err.ravel(), fmt="ko", capsize=3, lw=1)
ax.set_xlim([0,200])
f_obs=matrix.ravel()
f_exp=fit_I_px(0,*p)

# f_obs/=np.sum(f_obs)
# f_exp/=np.sum(f_exp)

# print((np.sum(f_obs)-np.sum(f_exp))/np.sum(f_obs))
# print(chisquare(f_obs=f_obs, f_exp=f_exp, ddof=7))

def I_px(x, A, ps_0, c_0):
    beta = w_c*coil-c_0
    chi = w_ps*ps_pos-ps_0
    beta, chi = np.meshgrid(beta, chi)
    fit_I_px = A*(I_px_co(beta, chi, C, alpha) + I_px_in(beta, chi, eta, alpha))
    # print(fit_I_px)
    return fit_I_px

def I_px_corr_co(x, A, ps_0, c_0):
    beta = w_c*coil-c_0
    chi = w_ps*ps_pos-ps_0
    beta, chi = np.meshgrid(beta, chi)
    fit_I_px = A*I_px_co(beta, chi, C, alpha) 
    # print(fit_I_px)
    return fit_I_px

def I_px_corr_in(x, A, ps_0, c_0):
    beta = w_c*coil-c_0
    chi = w_ps*ps_pos-ps_0
    beta, chi = np.meshgrid(beta, chi)
    fit_I_px = A*I_px_in(beta, chi, eta, alpha)
    # print(fit_I_px).858109
    return fit_I_px

# c_0=p[-1]
# ps_0=p[-2]

fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection='3d')
beta = w_c*coil-c_0
chi = w_ps*ps_pos-ps_0
beta, chi = np.meshgrid(beta, chi)
Z = matrix
Z1 = I_px(0, *p)
Z2 = I_px_corr_co(0, *p)
Z3 = I_px_corr_in(0, *p)
# Z=I_px_co(beta, chi, C, alpha, beta)+I_px_in(beta, chi, eta, alpha, beta)
ax.contour3D(beta, chi, Z, 40, cmap='binary')
ax.contour3D(beta, chi, Z1, 40, cmap='plasma')  # cmap='Blues')
ax.set_xlabel('$\\beta$')
ax.set_ylabel('$\chi$')
ax.set_zlabel('z')
ax.view_init(40, 45)
plt.show()
print("p=",p)
print("p0=", P0)
A=2452.5
# corrected_matrix=(Z-Z3)/(C)#
corrected_matrix=(Z-I_px_corr_in(0, A, ps_0, c_0))/(C)#
# corrected_matrix=Z-(Z1-Z2)#Z2#
corrected_matrix_err=matrix_err
for i in range(len(ps_pos)):
    data_txt=np.array([coil, corrected_matrix[i], corrected_matrix_err[i], np.ones(len(coil))*ps_pos[i]])
    with open(correct_fold_path+"/beta_ps_"+str("%02d" % (i,))+".txt", 'w') as f:
        np.savetxt(f, np.transpose(data_txt),  header= "Coil_pos O-Beam err ps_pos", fmt='%.7f %.7f %.7f %.7f' )

