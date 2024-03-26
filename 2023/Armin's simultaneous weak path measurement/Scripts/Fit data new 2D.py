#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 11:25:09 2024

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
from scipy.special import jv
plt.rcParams.update({'figure.max_open_warning': 0})
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
rad = np.pi/180
alpha = np.pi/9
w_1=62.5*1e-3*2*np.pi
w_2=55.5*1e-3*2*np.pi
C = 0.637
eps=1#0.93
chi_aus=0
Ampl_aus=0
a_21=1


def fit_cos(x, A, B, C, D):
    return A+jv(0,alpha)*B*np.cos(C*x-D)

def I_inc_nsr(chi):
    return 1/4

def I_co_nsr(chi):
    return 1/4*(1+np.cos(chi))

def I_inc_sr(t, delta1, delta2):
    return 1/4*(1+alpha/2*(np.sin(w_1*t+delta1)+np.sin(w_2*t+delta2)))

def I_co_sr(t, chi, delta1, delta2):
    return 1/4*np.cos(chi/2)**2-alpha/8*np.cos(chi/2)*(np.sin(chi/2-w_1*t-delta1)-np.sin(chi/2+w_2*t+delta2))

def fit_func(t, Ampl, delta1, delta2):
    return Ampl*((1-eps)*((1-C)*I_inc_nsr(chi_aus)+C*I_co_nsr(chi_aus))+eps*((1-C)*I_inc_sr(t, delta1, delta2)+C*I_co_sr(t, chi_aus, delta1, delta2)))


inf_file_name = "TOF_single_RF1+2_weak_1h.tof_23Jun0620"
sorted_fold_path = "/home/aaa/Desktop/Fisica/PhD/2023//Armin's simultaneous weak path measurement/Sorted data/"+inf_file_name
cleandata = sorted_fold_path+"/Cleantxt"


i = 0
for root, dirs, files in os.walk(cleandata, topdown=False):
    files = np.sort(files)
    for name in files:
        if i == 0:
            tot_data = np.loadtxt(os.path.join(root, name))[1:-1]
            time = tot_data[:, 0]
            i = 1
        else:
            data = np.loadtxt(os.path.join(root, name))[1:-1]
            tot_data = np.vstack((tot_data, data))
ps_pos = tot_data[::len(time), -1]
matrix = np.zeros((len(ps_pos), len(time)))
matrix_err = np.zeros((len(ps_pos), len(time)))

for i in range(len(ps_pos)):
    matrix[i]=tot_data[:,3][tot_data[:,-1]==ps_pos[i]]/tot_data[:,1][tot_data[:,-1]==ps_pos[i]][0]*10
    matrix_err[i]=tot_data[:,3][tot_data[:,-1]==ps_pos[i]]**0.5/tot_data[:,1][tot_data[:,-1]==ps_pos[i]][0]*10

ps_data=np.average(matrix, axis=1)
ps_data_err=np.sum(matrix_err, axis=1)**0.5/len(time)

ps_pos*=rad

P0=[(np.amax(ps_data)+np.amin(ps_data))/2, 0.6, 1, 0]
B0=([0,0,0.01,-10],[np.amax(ps_data)+1000,1000,3, 10])
p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
err=np.diag(cov)**0.5

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
ax.set_title("Integrated intensities")
ax.errorbar(ps_pos, ps_data, yerr=ps_data_err, fmt="ko", capsize=5)
x_plt = np.linspace(ps_pos[0], ps_pos[-1], 500)
ax.plot(x_plt, fit_cos(x_plt, *p))
chi_0 = p[-1]
w_ps=p[-2]
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
ax.errorbar(ps_pos,ps_data, yerr=ps_data_err,fmt="ko",capsize=5, ms=3)
ax.plot(ps_plt,fit_cos(ps_plt, *p), "b")
ax.vlines(p[-1]/p[-2],fit_cos(p[-1]/p[-2]+np.pi,*p),fit_cos(p[-1]/p[-2],*p), color="k")
chi=ps_pos*w_ps-chi_0
C=p[1]/p[0]
# C=0.7609707360123743
# w_ps= 3.00982007
# chi_0=-1.86377038e+00
print("Contrast = ",C)
print("p = ",p)
# chi_plt=np.linspace(chi[0], chi[-1], 100)
# C_err=0.022491135210979854
eta = 1-C
# beta = w_1*time+xi_0

def fit_I_px(x, delta_1, delta_2, A):
    fit_I_px = A*(I_px_co(beta_1, beta_2, chi, C, alpha_1, alpha_2) + I_px_inc)
    # print(fit_I_px)
    return fit_I_px.ravel()

# def fit_I_px(x, xi_0, A, alpha):
#     beta = 2*np.pi*1e-3*f_1*time+xi_0
#     # eta = 1-C
#     chi = w_ps*ps_pos-chi_0
#     I_px_inc=I_px_in(beta, chi, eta)
#     beta, chi = np.meshgrid(beta, chi)
#     fit_I_px = A*(I_px_co(beta, chi, C, alpha) + I_px_inc)
#     # print(fit_I_px)
#     return fit_I_px.ravel()

# P0 = (xi_0, 1, alpha)
# B0 = ([-10, 0, -10], [10, 10,  10])
# p, cov = fit(fit_I_px, range(len(matrix.ravel())), matrix.ravel()/np.amax(matrix.ravel()), bounds=B0)
# err= np.diag(cov)**0.5
# print(p, err)
# print("alpha=", p[-1],"+-", err[-1])
# xi_0 = p[0]
# fig = plt.figure(figsize=(10, 5))
# ax = fig.add_subplot(111)
# ax.errorbar(np.arange(len(matrix.ravel())),matrix.ravel(), yerr=matrix_err.ravel(), fmt="r.", alpha=0.5, ms=0.5, label="data")
# # ax.plot(matrix.ravel(), "r--")
# ax.plot(fit_I_px(0, *p)*np.amax(matrix.ravel()), "b", lw=1, label="Fit")
# ax.set_xlim([150,250])
# f_obs=matrix.ravel()
# f_exp=fit_I_px(0,*p)*np.amax(matrix.ravel())
# # import glob
# # from PIL import Image
# #def make_gif(frame_folder):
# #    frames = [Image.open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/Animation/chi"+str(j)+".png") for j in range(len(ps_pos))]
# #    frame_one = frames[0]
# #    frame_one.save("/home/aaa/Desktop/fit.gif", format="GIF", append_images=frames,
# #               save_all=True, duration=200, loop=0)
    
# #if __name__ == "__main__":
# #    make_gif("Phase")

# # f_obs/=np.sum(f_obs)
# # f_exp/=np.sum(f_exp)

# # print((np.sum(f_obs)-np.sum(f_exp))/np.sum(f_obs))
# # print(chisquare(f