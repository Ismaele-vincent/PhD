# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:37:41 2023

@author: S18
"""
"""
inf_file_names:
"ifg_TOF_A+B_off_05Nov1230",
"""


import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
from scipy.special import jv

mu_N=-9.6623651#*1e-27 J/T
hbar= 6.62607015/(2*np.pi) #*1e-34 J s
chi_fit=0
f_fit=10
def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def fit_abs_sin(x, A, B, T):
    return A+B*abs(np.sin(T*np.pi*x*1e-3))

# def fit_O_beam(t, A, B, a_1, xi_1):
#     return A + B*np.cos(chi_fit-a_1*np.sin(2*np.pi*1e-3*f_fit*t+xi_1))

def contr(x, a, b, c):
    w=2*np.pi*x
    return a*(jv(0, 2*mu_N/hbar*10.4*b/(4*np.pi)*np.sin(w*c*1e-3/2)))

inf_file_name="Freq_test_long_31Oct1702"
    # if "20s" in inf_file_name:
print(inf_file_name)
sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/Freq test/"+inf_file_name
cleandata_ifg=sorted_fold_path+"/Cleantxt/Ifg"
cleandata_freq=sorted_fold_path+"/Cleantxt/Freq"

for root, dirs, files in os.walk(cleandata_ifg, topdown=False):
    files=np.sort(files)
    C_ifg=np.array([])
    w_ps=np.array([])
    chi_0=np.array([])#
    freq=np.array([])
    for name in files[:]:
        # print(name)
        tot_data=np.loadtxt(os.path.join(root, name))[:,:]
        data_ifg=tot_data[:,3]+tot_data[:,6]
        # print(data_ifg)
        data_ifg_err=data_ifg**0.5
        ps_pos=tot_data[:,1]
        freq=np.append(freq,tot_data[0,-1])
        P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, 15]
        B0=([0,0,2.5,0],[np.amax(data_ifg)+1000,np.amax(data_ifg)+1000, 3.5, 30])
        p,cov=fit(fit_cos, ps_pos, data_ifg, p0=P0,  bounds=B0)
        # err=np.diag(cov)**0.5
        # print(p[3], err[3])
        # x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
        # fig = plt.figure(figsize=(8,6))
        # ax = fig.add_subplot(111)
        # fig.suptitle(name[:-4])
        # ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
        # ax.plot(x_plt,fit_cos(x_plt, *p), "b")

        C_ifg=np.append(C_ifg,p[1]/p[0])
        w_ps=np.append(w_ps,p[-2])
        chi_0=np.append(chi_0,p[-1])

        
        # print("C=", p[1]/p[0])
        # print("w_ps=", p[-2])
        # print("chi_0=", p[-1])
freq*=1e-3
# fig = plt.figure(figsize=(8,8))
# axC = fig.add_subplot(311)
# axw_ps = fig.add_subplot(312)
# axchi_0 = fig.add_subplot(313)
# axC.plot(freq, C)
# axC.set_ylabel("C")
# axw_ps.plot(freq, w_ps)
# axw_ps.set_ylabel("$\omega_{ps}$")
# axchi_0.plot(freq, chi_0)
# axchi_0.set_ylabel("$\chi_0$")
p,cov=fit(contr, freq, C_ifg, p0=[0.7,0.0061,25.56])#, bounds=([0.1,0.01, 20],[10, 0.1, 30]) )
print(p, np.diag(cov)**0.5)
freq_plt=np.linspace(freq[0], freq[-1], 1000)
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
ax.plot(freq, C_ifg, "k.")
ax.plot(freq_plt, contr(freq_plt,*p), "b")
plt.show()
i=0
for root, dirs, files in os.walk(cleandata_freq, topdown=False):
    files=np.sort(files)
    C=np.array([])
    A=np.array([])
    w_ps=np.array([])
    chi_0=np.array([])#
    freq=np.array([])
    P0=[7.72390281e+02,  2.46705637e+02,  6.40321797e-02, 0.5454591]
    for name in files[:]:
        # print(name)
        tot_data=np.loadtxt(os.path.join(root, name))[:-1,:]
        data_freq=tot_data[:,5]
        # print(data_freq)
        data_freq_err=data_freq**0.5
        ps_pos=tot_data[:,1]
        freq=np.append(freq,tot_data[0,-1])
        # print(freq)
       
        B0=([0,0,2*np.pi*freq[i]*1e-6-1,-10],[np.amax(data_freq)+1000,np.amax(data_freq)+1000, 2*np.pi*freq[i]*1e-6+1, 20])
        p,cov=fit(fit_cos, ps_pos, data_freq, p0=P0)
        err=np.diag(cov)**0.5
        # print(p, err)
        P0=p.copy()
        x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        fig.suptitle(freq[i])
        ax.errorbar(ps_pos,data_freq,yerr=data_freq_err,fmt="ko",capsize=5, ms=3)
        ax.plot(x_plt,fit_cos(x_plt, *p), "b")

        # B0=([0,0,2*np.pi*freq[i]*1e-6-1,-10],[np.amax(data_freq)+1000,np.amax(data_freq)+1000, 2*np.pi*freq[i]*1e-6+1, 20])
        # p,cov=fit(fit_cos, ps_pos, data_freq, p0=P0,  bounds=B0)
        A=np.append(A,abs(p[1]))
        C=np.append(C,abs(p[1]/p[0]))
        w_ps=np.append(w_ps,p[-2])
        chi_0=np.append(chi_0,p[-1])
        i+=1
        # print("C=", p[1]/p[0])
        # print("w_ps=", p[-2])
        # print("chi_0=", p[-1])
freq*=1e-3
p,cov=fit(fit_abs_sin, freq[:], C[:], p0=[0,1,25])

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
ax.plot(freq, C, "k.")
ax.plot(freq_plt, fit_abs_sin(freq_plt,*p), "b")

plt.show()

freq_plt=np.linspace(freq[0], freq[-1], 10000)
print(1/40760**2*259.796*1e6)
# fig = plt.figure(figsize=(8,8))
# ax = fig.add_subplot(111)
# ax.plot(freq, A, "k.")
# ax.plot(freq_plt, contr(freq_plt,*p), "b")
# plt.show()
print(1/40.6*1e3)
i=0