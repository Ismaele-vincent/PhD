# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 18:35:01 2023

@author: S18
"""

"""
.inf file names:
"Freq_test_27Aug1755", 
"Freq_test_27Aug1806", 
"Freq_test_27Aug1906", 
"Freq_test_28Aug1639", 
"Freq_test_28Aug1724", 
"Freq_test_29Aug0725", 
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
mu_N=-9.6623651#*1e-27 J/T
hbar= 6.62607015/(2*np.pi) #*1e-34 J s
f_1=10
B_1=10
B_0=18.55#
T=10
v0=2060.43 #m/s
phi_1=0
order=4
w_ps=3
rad=np.pi/180

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

def fit_O_beam(t, A, C, chi, B_1, phi_1, T):
    a_1=alpha(T,f_1,B_1)
    xi_1=phi_1+(2*np.pi*f_1*1e-3*T+np.pi)/2#-2*np.pi*f_1*1e3/v0
    return A*(1-C+C*(1+np.cos(chi+a_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)))/2)

inf_file_names=[
"Freq_test_27Aug1755", 
"Freq_test_27Aug1806", 
"Freq_test_27Aug1906", 
"Freq_test_28Aug1639", 
"Freq_test_28Aug1724", 
"Freq_test_29Aug0725", 
"Freq_test_31Aug1512", 
"Freq_test_31Aug1918", 
"Freq_test_31Aug2012",]

for inf_file_name in inf_file_names:
    print(inf_file_name)
    sorted_fold_path="C:/Users/S18/Desktop/Grenoble-2023 Ismaele/Grenoble 3rd round/exp_3-16-14/Sorted data/Freq test/"+inf_file_name
    cleandata=sorted_fold_path+"/Cleantxt"
    for root, dirs, files in os.walk(cleandata, topdown=False):
        # files=np.sort(files)
        for name in files:
            print(name)
            tot_data=np.loadtxt(os.path.join(root, name))
            data_f_test=tot_data[:,4]
            data_f_test_err=data_f_test**0.5
            time=tot_data[:,0]
            ps_pos=tot_data[0,-1]
            f_1=tot_data[0,-3]*1e-3
            print(f_1)
            P0=[(np.amax(data_f_test)+np.amin(data_f_test))/2, 0.7, 3*ps_pos, 10, 0.1, 10]
            B0=([np.amin(data_f_test),0.1,-3*np.pi,2,-3*np.pi,5],[3000,1,3*np.pi, 30, 3*np.pi,30])
            # p,cov=fit(fit_O_beam, time, data_f_test, p0=P0,  bounds=B0)
            # err=np.diag(cov)**0.5
            # print(p[3], err[3])
            x_plt = np.linspace(time[0], time[-1],100)
            fig = plt.figure(figsize=(10,6))
            ax = fig.add_subplot(111)
            fig.suptitle(inf_file_name+"\n"+name[:])
            ax.errorbar(time,data_f_test,yerr=data_f_test_err,fmt="ko",capsize=5, ms=3)
            # ax.plot(x_plt,fit_O_beam(x_plt, *p), "b")
            # ax.set_ylim([0,1500])
            # print("C=", p[1]/p[0])
        
plt.show()