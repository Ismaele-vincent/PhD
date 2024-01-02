#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 18:59:22 2023

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
from scipy.special import jv
plt.rcParams.update({'figure.max_open_warning': 0})
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

a_1 = 1/2**0.5
a_2 = 1/2**0.5
f_1 = 2
xi_0=0.1
alpha=-np.pi/4


def fit_cos(x, A, B, C, D):
    return A+jv(0,alpha)*B*np.cos(C*x-D)

def I_px_co(beta, chi, C, alpha):
    I_co=(1+2*a_1*a_2*np.cos(chi-alpha*np.sin(beta)))/2
    return C*I_co

def I_px_in(beta, chi, eta):
    I_in=np.ones((len(chi),len(beta)))/2
    return eta*I_in

# inf_file_name=inf_file_name="TOF_vs_chi_A_22pt_pi8_1200s_06Nov1855"
# inf_file_name="TOF_vs_chi_A_19pt_pi16_1500s_03Nov1230"
# inf_file_name="TOF_vs_chi_A_19pt_pi4_1200s_03Nov2326"
# inf_file_name="TOF_vs_chi_A_19pt_pi4_600s_03Nov1625"
# inf_file_name="TOF_vs_chi_A_19pt_pi8_100s_06Nov1154"
# inf_file_name="TOF_vs_chi_A_19pt_pi8_1200s_04Nov1722"
# inf_file_name="TOF_vs_chi_A_22pt_pi8_1200s_06Nov1855"
# inf_file_name="TOF_vs_chi_A_22pt_pi16_1200s_07Nov1808"
# inf_file_name="TOF_vs_chi_A_22pt_pi4_1200s_08Nov0132"
# inf_file_name="TOF_vs_chi_A_22pt_pi2_1200s_12Nov0455"
# inf_file_name="TOF_vs_chi_A_22pt_pi4_SD_1200s_12Nov2101"
# inf_file_name="TOF_vs_chi_A_22pt_pi2_1200s_13Nov0438"

sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/TOF A/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"

i=0
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    # print(files)
    for name in files:
        if i==0:
            tot_data=np.loadtxt(os.path.join(root, name))[1:-1,:]
            time=tot_data[:,1]
            f_1=tot_data[0,-3]*1e-3
            print(f_1)
            i=1
        else:
            data=np.loadtxt(os.path.join(root, name))[1:-1,:]
            tot_data = np.vstack((tot_data, data))
ps_pos=tot_data[::len(time),-1]
# ps_pos=ps_pos[5:]
matrix=np.zeros((len(ps_pos),len(time)))
matrix_err=np.zeros((len(ps_pos),len(time)))
for i in range(len(ps_pos)):
    matrix[i]=tot_data[:,5][tot_data[:,-1]==ps_pos[i]]
    matrix_err[i]=matrix[i]**0.5
    matrix[i]/=np.sum(tot_data[:,3:6][tot_data[:,-1]==ps_pos[i]])
    matrix_err[i]/=np.sum(tot_data[:,3:6][tot_data[:,-1]==ps_pos[i]])
ps_data=np.sum(matrix, axis=1)
ps_data_err=np.sum(matrix_err, axis=1)
P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, -3]
B0=([0,0,0.01,-10],[np.amax(ps_data)+1000,np.amax(ps_data)+10000,5, 10])
p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
# print(p)
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
beta = 2*np.pi*1e-3*f_1*time+xi_0


def fit_I_px(x, xi_0, A, alpha):
    beta = 2*np.pi*1e-3*f_1*time+xi_0
    # eta = 1-C
    chi = w_ps*ps_pos-chi_0
    I_px_inc=I_px_in(beta, chi, eta)
    beta, chi = np.meshgrid(beta, chi)
    fit_I_px = A*(I_px_co(beta, chi, C, alpha) + I_px_inc)
    # print(fit_I_px)
    return fit_I_px.ravel()

P0 = (xi_0, 1, alpha)
B0 = ([-10, 0, -10], [10, 10,  10])
p, cov = fit(fit_I_px, range(len(matrix.ravel())), matrix.ravel()/np.amax(matrix.ravel()), bounds=B0)
err= np.diag(cov)**0.5
print(p, err)
print("alpha=", p[-1],"+-", err[-1])
xi_0 = p[0]
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
ax.errorbar(np.arange(len(matrix.ravel())),matrix.ravel(), yerr=matrix_err.ravel(), fmt="r.", alpha=0.5, ms=0.5, label="data")
# ax.plot(matrix.ravel(), "r--")
ax.plot(fit_I_px(0, *p)*np.amax(matrix.ravel()), "b", lw=1, label="Fit")
ax.set_xlim([150,250])
f_obs=matrix.ravel()
f_exp=fit_I_px(0,*p)*np.amax(matrix.ravel())
# import glob
# from PIL import Image
#def make_gif(frame_folder):
#    frames = [Image.open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/Animation/chi"+str(j)+".png") for j in range(len(ps_pos))]
#    frame_one = frames[0]
#    frame_one.save("/home/aaa/Desktop/fit.gif", format="GIF", append_images=frames,
#               save_all=True, duration=200, loop=0)
    
#if __name__ == "__main__":
#    make_gif("Phase")

# f_obs/=np.sum(f_obs)
# f_exp/=np.sum(f_exp)

# print((np.sum(f_obs)-np.sum(f_exp))/np.sum(f_obs))
# print(chisquare(f