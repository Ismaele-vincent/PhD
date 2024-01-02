# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 18:41:54 2023

@author: S18
"""

"""
inf_file_names:
"TOF_vs_chi_S2_ifg_29Aug1924",
"""

import os
import numpy as np
from scipy.special import jv
import shutil
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq, fft, fftfreq, dct, dst
from mpl_toolkits import mplot3d
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from PIL import Image as im
from scipy.optimize import curve_fit as fit
mu_N=-9.6623651#*1e-27 J/T
hbar= 6.62607015/(2*np.pi) #*1e-34 J s
f_1=20
c_1=10
B_0=18.55
T=24.5881
v0=2060.43 #m/s
phi_1=0
order=4
w_ps=0
rad=np.pi/180
chi=0
chi_0=0
C=0

def j0_fit(x, a, b, c):
    w=f_1*2*np.pi
    a_1=mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2)
    return c +abs(a*jv(0,a_1*b*x))

def j1_fit(x, a, b):
    w=f_1*2*np.pi
    a_1=mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2)
    return abs(a*jv(1,a_1*b*x))

def j2_fit(x, a, b):
    w=f_1*2*np.pi
    a_1=mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2)
    return abs(a*jv(2,a_1*b*x))

def j3_fit(x, a, b):
    w=f_1*2*np.pi
    a_1=mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2)
    return abs(a*jv(3,a_1*b*x))

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

def B(T,f,alpha):
    w=f*2*np.pi
    return alpha/(mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2))



def fit_O_beam(t, A, B, a_1, xi_1):
    # a_1=alpha(T,f_1,c_1)
    # xi_1=phi_1+(2*np.pi*f_1*1e-3*T+np.pi)/2#-2*np.pi*f_1*1e3/v0
    chi_fit=chi
    return A + B*np.cos(chi_fit-a_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1))/2

inf_file_name="B_test_long_3kHzB_08Nov1721"
# inf_file_name="B_test_long_2kHz_02Nov1533"
print(inf_file_name)
sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/TOF vs B-field/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"
i=0
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    for name in files:
        if i==0:
            tot_data=np.loadtxt(os.path.join(root, name))[:,:]
            time=tot_data[:,1]
            f_1=3
            print(name)
            i+=1
        else:
            data=np.loadtxt(os.path.join(root, name))[:,:]
            tot_data = np.vstack((tot_data, data))
               
amplitude=tot_data[::len(time),-1]
# current=amplitude/2
current=np.array([0.333, 0.667, 1, 1.333, 1.667, 2, 2.333, 2.667, 3, 3.333, 3.667, 4, 4.333, 4.667, 5, 5.333, 5.667, 6])/2
# current=np.array([0.333, 0.667, 1.333, 1.601, 1.667, 2, 2.333, 2.667, 3, 3.333, 3.667, 4, 4.333, 4.667, 5, 5.333, 5.667, 6])/2
amplitude=amplitude[:-6]
current=current[:-6]
chi=np.pi/4


# current=np.array([1.2, 1.76, 3.6, 5.8, 7.3, 10.3, 13.6, 16.4])/2
# print(amplitude)
N = len(time)
print(N)
S_F=11.1111
matrix=np.zeros((len(amplitude),len(time)))
matrix_err=np.zeros((len(amplitude),len(time)))
for i in range(len(amplitude)):
    matrix[i]=tot_data[:,4][tot_data[:,-1]==amplitude[i]]
    matrix_err[i]=matrix[i]**0.5
P0=[300,300, -0.8, 1]



ps_data=np.sum(matrix, axis=1)
P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, -3]
B0=([1000,0,0.01,-10],[np.amax(ps_data)+1000,np.amax(ps_data)+1000,5, 10])







p_tot=np.zeros((len(amplitude),len(P0)))
err_tot=np.zeros((len(amplitude),len(P0)))
c_0_data=np.zeros((len(amplitude)),dtype=complex)
c_1_data=np.zeros((len(amplitude)),dtype=complex)
c_2_data=np.zeros((len(amplitude)),dtype=complex)
c_3_data=np.zeros((len(amplitude)),dtype=complex)
c_0_data_err=np.zeros((len(amplitude)),dtype=complex)
c_1_data_err=np.zeros((len(amplitude)),dtype=complex)
c_2_data_err=np.zeros((len(amplitude)),dtype=complex)
c_3_data_err=np.zeros((len(amplitude)),dtype=complex)
J_0=np.zeros((len(amplitude)))
J_1=np.zeros((len(amplitude)))
J_2=np.zeros((len(amplitude)))
for i in range(len(amplitude)):
    func_data=matrix[i]
    # print(len(func_data))
    func_data_err=matrix_err[i]
    yf_data = fft(func_data)
    yf_data_err = np.ones(len(yf_data))*np.sum(matrix_err)**0.5
    # print(sum(abs(yf_data)))
    xf = fftfreq(N, S_F)*1e3
    # fig = plt.figure(figsize=(8,6))
    # ax = fig.add_subplot(111)
    # ax.errorbar(time, matrix[i], yerr= matrix_err[i], fmt="ko")
    # ax.set_title(str("%.2f"%amplitude[i],))
    # ax.errorbar(xf, np.abs(yf_data), np.abs(yf_data_err), fmt="k.", capsize=5)
    # ax.set_xlim([-5,5])
    if i==0:
        x_1=f_1#xf[xf>0][abs(yf_data[xf>0])==np.amax(abs(yf_data[xf>0]))]
        # print(x_1)
    c_0_data[i]=abs(yf_data[abs(xf)<1/S_F/2]).astype(complex)#-1000#-30646.5416183380225#-3709.5445367569832#-4384.460247693247#-5080.77771430624
    c_1_data[i]=(yf_data[abs(xf-x_1)<1/S_F/2]).astype(complex)
    c_2_data[i]=(yf_data[abs(xf-2*x_1)<1/S_F/2]).astype(complex)
    c_3_data[i]=(yf_data[abs(xf-3*x_1)<1/S_F/2]).astype(complex)
    var=np.sum(func_data)**0.5
    c_0_data_err[i]=var
    c_1_data_err[i]=var
    c_2_data_err[i]=var
    c_3_data_err[i]=var
chi=np.pi/4
c_0_err_rel=c_0_data_err/abs(c_0_data)
c_1_err_rel=c_1_data_err/abs(c_1_data)
c_2_err_rel=c_2_data_err/abs(c_2_data)
c_3_err_rel=c_3_data_err/abs(c_3_data)

# fig = plt.figure(figsize=(10,6))
# ax = fig.add_subplot(111)
# ax.errorbar(current, np.sum(matrix, axis=1),np.sum(matrix_err, axis=1))


J_0=(2*(c_0_data)-1)/abs(np.cos(chi))
J_1=2*(c_1_data)/abs(np.sin(chi))
J_2=2*(c_2_data)/abs(np.cos(chi))
J_3=2*(c_3_data)/abs(np.cos(chi))

# points=range(len(J_0))#[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
P0=[100000,10]
# p0,cov0=fit(j0_fit, current[:], abs(J_0[:]), p0=[10,5,0], bounds=([0,0,0],[100,50, 20]))
p1,cov1=fit(j1_fit, current, abs(J_1), p0=P0, bounds=([0,0],[1000000,50]))
p2,cov2=fit(j2_fit, current, abs(J_2), p0=P0, bounds=([0,0],[1000000,50]))
p3,cov3=fit(j3_fit, current, abs(J_3), p0=P0, bounds=([0,0],[1000000,50]))
print(p1,p2,p3)
print(np.diag(cov1)**0.5,np.diag(cov2)**0.5,np.diag(cov3)**0.5)
fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111)
# ax.plot(current, abs(J_0), "g.")
alpha_plt=-alpha(T,f_1, p1[-1]*current)
ax.errorbar(alpha_plt, abs(J_1), yerr= abs(J_1)*c_1_err_rel,fmt="k.")
ax.errorbar(alpha_plt, abs(J_2),yerr= abs(J_2)*c_2_err_rel, fmt="r.")
ax.errorbar(alpha_plt, abs(J_3),yerr= abs(J_3)*c_3_err_rel, fmt="b.")
c_plt= np.linspace(0,current[-1],150)
# ax.plot(c_plt*p1[1], j0_fit(c_plt,1, p1[1], 0), "g-")
alpha_plt1=-alpha(T,f_1, p1[-1]*c_plt)
ax.plot(alpha_plt1, j1_fit(c_plt, *p1), "k-")
ax.plot(alpha_plt1,  j2_fit(c_plt,*p2), "r-")
ax.plot(alpha_plt1,  j3_fit(c_plt, *p3), "b-")
ax.vlines(3.8317, 0, j2_fit(1.6,*p2) )
# ax.plot(amplitude, J_2, "bo")
# ax.set_ylim([-10,10])  
# fig = plt.figure(figsize=(6,8))
# param_names=["A", "C", "$\\alpha_1$", "$\\xi_1$"]
# gs = GridSpec(len(param_names),1, figure=fig, hspace=0, wspace=0)
# axs=[]
# for i in range(len(param_names)):
#     axs.append(fig.add_subplot(gs[i,0]))
#     axs[i].set_ylabel(param_names[i])
#     axs[i].errorbar(ps_pos, p_tot[:,i], yerr=err_tot[:,i])
#     y_min=np.amin(p_tot[:,i])
#     y_max=np.amax(p_tot[:,i])
#     axs[i].set_ylim([y_min*(1-np.sign(y_min)*0.1),y_max*(1+np.sign(y_min)*0.1)])

print(alpha(T, f_1, current[0]/2*10.39))
print(B(24.5881,2, np.pi/16)/10.3*2)


  
plt.show()