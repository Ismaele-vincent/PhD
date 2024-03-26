#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 11:09:15 2024

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
rad = np.pi/180
alpha = np.pi/9
w_1=62.5*1e-3*2*np.pi
w_2=55.5*1e-3*2*np.pi
C = 0.637
eps=1
chi_aus=0
Ampl_aus=0
a_21=1

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x+D)

def I_inc_nsr(chi):
    return 1/4

def I_co_nsr(chi):
    return 1/4*(1+np.cos(chi))

def I_inc_sr(t, delta1, delta2):
    return 1/4*(1+alpha/2*(np.sin(w_1*t+delta1)+np.sin(w_2*t+delta2)))

def I_co_sr(t, chi, delta1, delta2):
    return 1/2*np.cos(chi/2)**2-alpha/4*np.cos(chi/2)*(np.sin(chi/2-w_1*t-delta1)-np.sin(chi/2+w_2*t+delta2))


def fit_func(t, Ampl, delta1, delta2):
    return Ampl*((1-eps)*((1-C)*I_inc_nsr(chi_aus)+C*I_co_nsr(chi_aus))+eps*((1-C)*I_inc_sr(t, delta1, delta2)+C*I_co_sr(t, chi_aus, delta1, delta2)))


# def fit_func(t, A1, phi1, A2, phi2, delta1, delta2):
#     delta1=1.422
#     delta2=2.328
#     return Ampl_aus*((1-eps)*((1-C)*I_inc_nsr(chi_aus)+C*I_co_nsr(chi_aus))+eps*((1-C)*I_inc_sr(t, delta1, delta2)+C*np.cos(chi_aus/2)**2/2*(1+alpha*(A1*np.sin(phi1-w_1*t-delta1)+A2*np.sin(phi2-w_2*t-delta2)))))

def w1(chi):
    return (1/(1+a_21*np.exp(1j*chi)))

def w2(chi):
    return (1-1/(1+a_21*np.exp(1j*chi)))



# "TOF_PS_RF1_pi2_1h_10Jun1748" #"TOF_PS_RF2_weak_1h.tof_18Jun1231"#"TOF_PS_RF2_pi2_1h_12Jun0717"#
inf_file_name = "TOF_single_RF1+2_weak_1h.tof_23Jun0620"
sorted_fold_path = "/home/aaa/Desktop/Fisica/PhD/2023//Armin's simultaneous weak path measurement/Sorted data/"+inf_file_name
cleandata = sorted_fold_path+"/Cleantxt"
# correct_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 1st round/exp_3-16-13/Corrected data/"+inf_file_name+"/Beta"

# if not os.path.exists(correct_fold_path):
#     os.makedirs(correct_fold_path)
# else:
#     shutil.rmtree(correct_fold_path)
#     os.makedirs(correct_fold_path)


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
# print(ps_pos)
# ps_i=109
# ps_f=ps_pos[-1]
# ps_pos=ps_pos[abs(ps_pos-(ps_i+ps_f)/2)<(ps_f-ps_i)/2]
matrix = np.zeros((len(ps_pos), len(time)))
matrix_err = np.zeros((len(ps_pos), len(time)))

for i in range(len(ps_pos)):
    matrix[i]=tot_data[:,3][tot_data[:,-1]==ps_pos[i]]/tot_data[:,1][tot_data[:,-1]==ps_pos[i]][0]*100
    matrix_err[i]=tot_data[:,3][tot_data[:,-1]==ps_pos[i]]**0.5/tot_data[:,1][tot_data[:,-1]==ps_pos[i]][0]*100

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
print(p[1]/p[0])
A1 = np.zeros(len(ps_pos))
A2 = np.zeros(len(ps_pos))
phi1 = np.zeros(len(ps_pos))
phi2 = np.zeros(len(ps_pos))
A1_err = np.zeros(len(ps_pos))
A2_err = np.zeros(len(ps_pos))
phi1_err = np.zeros(len(ps_pos))
phi2_err = np.zeros(len(ps_pos))
p_aus=np.array([0,0,0])
for i in range(len(ps_pos)):
    data=matrix[i]
    # print(Ampl_aus)
    chi_aus=ps_pos[i]
    # P0 = [abs(w1(ps_pos[i])), np.angle(w1(ps_pos[i])), abs(w2(ps_pos[i])), np.angle(w2(ps_pos[i])), -1.3, -2.3]
    # B0 = ([0, -6, 0, -6,-6,-6], [1000, 6, 1000, 6,6,6])
    P0 = [12, 1.4, 2.3]
    B0 = ([0,0, 0], [100, np.pi, np.pi])
    p, cov = fit(fit_func, time, data, p0=P0, bounds=B0)
    print(p)
    p_aus=p
    err = np.diag(cov)**0.5
    # print(p)
    # A1[i] = p[0]
    # A1_err[i] = err[0]
    # A2[i] = p[2]
    # A2_err[i] = err[2]
    # phi1[i] = p[1]
    # phi1_err[i] = err[1]
    # phi2[i] = p[3]
    # phi2_err[i] = err[3]
    x_plt = np.linspace(time[0], time[-1], 100)
    fig = plt.figure(figsize=(15,5))
    ax = fig.add_subplot(111)
    ax.errorbar(time,data,yerr=matrix_err[i],fmt="k.",capsize=5)
    # ax.plot(time,matrix[i],"k-")
    ax.plot(x_plt,fit_func(x_plt, *p), "b", lw=5)
    # ax.plot(x_plt,fit_cos(x_plt, *p), "b")
    # ax.set_xlim([100,200])
# P0 = [30, 80, 0.7, 1.5, -1]
# B0 = ([0, 0, 0.5, 0.01, -5], [100, 200, 1, 50, 5])
# fig = plt.figure(figsize=(10, 5))
# ax = fig.add_subplot(111)
# ax.set_title("Amplitude1")
# ax.errorbar(ps_pos, A1, yerr=A1_err, fmt="ko", capsize=5)
# x_plt = np.linspace(ps_pos[0], ps_pos[-1], 500)
# ax.plot(x_plt, abs(w2(x_plt)))
# ax.set_ylim([0,3])

# fig = plt.figure(figsize=(10, 5))
# ax = fig.add_subplot(111)
# ax.set_title("Amplitude2")
# ax.errorbar(ps_pos, A2, yerr=A2_err, fmt="ko", capsize=5)
# x_plt = np.linspace(ps_pos[0], ps_pos[-1], 500)
# ax.plot(x_plt, abs(w2(x_plt)))
# ax.set_ylim([0,3])

# fig = plt.figure(figsize=(10, 5))
# ax = fig.add_subplot(111)
# ax.set_title("phase1")
# ax.errorbar(ps_pos, phi1, yerr=phi1_err, fmt="ko", capsize=5)
# x_plt = np.linspace(ps_pos[0], ps_pos[-1], 500)
# ax.plot(x_plt, np.angle(w1(x_plt)))
# ax.set_ylim([-10,10])

# fig = plt.figure(figsize=(10, 5))
# ax = fig.add_subplot(111)
# ax.set_title("phase2")
# ax.errorbar(ps_pos, phi2, yerr=phi2_err, fmt="ko", capsize=5)
# x_plt = np.linspace(ps_pos[0], ps_pos[-1], 500)
# ax.plot(x_plt, np.angle(w1(x_plt)))
# ax.set_ylim([-10,10])

# fig = plt.figure(figsize=(10, 5))
# ax = fig.add_subplot(111)
# ax.set_title("Imag")
# ax.errorbar(ps_pos, A1*np.sin(phi1), yerr=phi2_err, fmt="ko", capsize=5)
# x_plt = np.linspace(ps_pos[0], ps_pos[-1], 500)
# ax.plot(x_plt, w1(x_plt).imag)
# ax.set_ylim([-10,10])

# # # P0 = [30, 80, 1,  -1]
# # # B0 = ([0, 0, 0.01, -5], [100, 200, 50, 5])


