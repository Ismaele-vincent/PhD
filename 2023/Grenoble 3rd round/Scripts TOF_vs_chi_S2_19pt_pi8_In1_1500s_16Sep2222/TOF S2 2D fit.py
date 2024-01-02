#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 10:29:06 2023

@author: aaa
"""

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

a_1 = 1/5**0.5
a_2 = 2/5**0.5
f1 = 10
xi_0=0.1
alpha=np.pi/8


def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def I_px_co(beta, chi, C, alpha):
    I_co=(1+2*a_1*a_2*np.cos(chi-alpha*np.sin(beta)))/2
    return C*I_co

def I_px_in(beta, chi, eta):
    I_in=np.ones((len(chi),len(beta)))/2
    return eta*I_in




inf_file_name="TOF_vs_chi_S2_19pt_pi8_In1_1500s_16Sep2222"
sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/exp_3-16-14/Sorted data/TOF S2/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"

i=0
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    # print(files)
    for name in files:
        if i==0:
            tot_data=np.loadtxt(os.path.join(root, name))[1:-1,:]
            time=tot_data[:,1]
            f_2=tot_data[0,-3]*1e-3
            print(f_2)
            i=1
        else:
            data=np.loadtxt(os.path.join(root, name))[1:-1,:]
            tot_data = np.vstack((tot_data, data))
ps_pos=tot_data[::len(time),-1]
matrix=np.zeros((len(ps_pos),len(time)))
matrix_err=np.zeros((len(ps_pos),len(time)))
for i in range(len(ps_pos)):
    if tot_data[:,4].all()==0:
        matrix[i]=tot_data[:,3][tot_data[:,-1]==ps_pos[i]]
    else:
        matrix[i]=tot_data[:,4][tot_data[:,-1]==ps_pos[i]]
    matrix_err[i]=matrix[i]**0.5
    
ps_data=np.sum(matrix, axis=1)
P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, -3]
B0=([1000,0,0.01,-10],[np.amax(ps_data)+1000,np.amax(ps_data)+1000,5, 10])
p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
chi_0 = p[-1]
w_ps=p[-2]
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
ax.errorbar(ps_pos,ps_data, yerr=ps_data**0.5,fmt="ko",capsize=5, ms=3)
ax.plot(ps_plt,fit_cos(ps_plt, *p), "b")
ax.vlines(p[-1]/p[-2],fit_cos(p[-1]/p[-2]+np.pi,*p),fit_cos(p[-1]/p[-2],*p), color="k")
chi=ps_pos*w_ps-chi_0
chi_plt=np.linspace(chi[0], chi[-1], 100)
C=0.6590116765538198
C_err=0.022491135210979854
eta = 1-C
beta = 2*np.pi*1e-3*f1*time+xi_0


def fit_I_px(x, xi_0, A, alpha):
    beta = 2*np.pi*1e-3*f1*time+xi_0
    chi = w_ps*ps_pos-chi_0
    I_px_inc=I_px_in(beta, chi, eta)
    beta, chi = np.meshgrid(beta, chi)
    fit_I_px = A*(I_px_co(beta, chi, C, alpha) + I_px_inc)
    # print(fit_I_px)
    return fit_I_px.ravel()

P0 = (xi_0, 1, alpha)
B0 = ([-10, 0, -10], [10 ,10, 10])
p, cov = fit(fit_I_px, range(len(matrix.ravel())), matrix.ravel()/np.amax(matrix.ravel()), bounds=B0)
err=np.diag(cov)**0.5
# print(p, err)
print("alpha=", p[-1], "+-", err[-1] )
# print(chi_0)
xi_0 = p[0]
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
ax.errorbar(np.arange(len(matrix.ravel())),matrix.ravel(), yerr=matrix_err.ravel(), fmt="r.", alpha=0.5, capsize=3, lw=0.5, ms=0.5)
ax.plot(fit_I_px(0, *p)*np.amax(matrix.ravel()), "b")
# ax.plot(matrix.ravel(), "r--")
ax.set_xlim([0,1000])
f_obs=matrix.ravel()
f_exp=fit_I_px(0,*p)*np.amax(matrix.ravel())

# f_obs/=np.sum(f_obs)
# f_exp/=np.sum(f_exp)

# print((np.sum(f_obs)-np.sum(f_exp))/np.sum(f_obs))
# print(chisquare(f_obs=f_obs, f_exp=f_exp, ddof=7))

def I_px(x, xi_0, A, B, alpha):
    beta = 2*np.pi*1e-3*f1*time+xi_0
    chi = w_ps*ps_pos-chi_0
    I_px_inc=I_px_in(beta, chi, eta)
    beta, chi = np.meshgrid(beta, chi)
    fit_I_px = A*(I_px_co(beta, chi, C, alpha) + I_px_inc)+B
    # print(fit_I_px)
    return fit_I_px

def I_px_corr_co(x, xi_0, A, B, alpha):
    beta = 2*np.pi*1e-3*f1*time+xi_0
    chi = w_ps*ps_pos-chi_0
    beta, chi = np.meshgrid(beta, chi)
    fit_I_px = I_px_co(beta, chi, C, alpha)
    return fit_I_px

def I_px_corr_in(x, xi_0, A, B, alpha):
    beta = 2*np.pi*1e-3*f1*time+xi_0
    chi = w_ps*ps_pos-chi_0
    I_px_inc=I_px_in(beta, chi, eta)
    beta, chi = np.meshgrid(beta, chi)+B
    fit_I_px = I_px_inc
    # print(fit_I_px)
    return fit_I_px

# beta = 2*np.pi*1e-3*f1*time+xi_0
# fig = plt.figure(figsize=(10, 10))
# ax = plt.axes(projection='3d')
# beta, chi = np.meshgrid(beta, chi)
# Z = matrix
# Z1 = I_px(0, *p)*np.amax(matrix)
# Z2 = I_px_corr_co(0, *p)*np.amax(matrix)
# Z3 = Z-I_px_corr_in(0, *p)*np.amax(matrix)
# # Z=I_px_co(beta, chi, C, alpha, beta)+I_px_in(beta, chi, eta, alpha, beta)
# ax.contour3D(beta, chi, Z, 40, cmap='binary')
# ax.contour3D(beta, chi, Z1, 40, cmap='plasma')  # cmap='Blues')
# ax.set_xlabel('$\\beta$')
# ax.set_ylabel('$\chi$')
# ax.set_zlabel('z')
# ax.view_init(40, 45)
# plt.show()


# corrected_matrix=Z-(Z1-Z2)
# corrected_matrix+=abs(np.amin(corrected_matrix))
# print(corrected_matrix[corrected_matrix<0])
# corrected_matrix_err=matrix_err
# for i in range(len(ps_pos)):
#     data_txt=np.array([c_pos, corrected_matrix[i], corrected_matrix_err[i], np.ones(len(c_pos))*ps_pos[i]])
#     with open(correct_fold_path+"/beta_ps_"+str("%02d" % (i,))+".txt", 'w') as f:
#         np.savetxt(f, np.transpose(data_txt),  header= "Coil_pos O-Beam err ps_pos", fmt='%.7f %.7f %.7f %.7f' )

