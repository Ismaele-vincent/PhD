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

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

inf_file_names=[
"ifg_-2to2_30s_07Nov1755"
]

for inf_file_name in inf_file_names:
    # if "20s" in inf_file_name:
        print(inf_file_name)
        sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/Ifg off/"+inf_file_name
        cleandata=sorted_fold_path+"/Cleantxt"
        for root, dirs, files in os.walk(cleandata, topdown=False):
            files=np.sort(files) 
            C=np.array([])
            C_err=np.array([])
            for name in files[:]:
                # print(name)
                tot_data=np.loadtxt(os.path.join(root, name))[:,:]
                data_ifg=tot_data[:,2]+tot_data[:,5]
                # print(data_ifg)
                data_ifg_err=data_ifg**0.5
                ps_pos=tot_data[:,0]
                P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, 0]
                B0=([np.amin(data_ifg),0,0.01,-10],[np.amax(data_ifg),np.amax(data_ifg),5, 10])
                p,cov=fit(fit_cos, ps_pos, data_ifg, p0=P0,  bounds=B0)
                err=np.diag(cov)**0.5
                # print(p[3], err[3])
                x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
                fig = plt.figure(figsize=(8,6))
                ax = fig.add_subplot(111)
                fig.suptitle(name[:-4])
                ax.set_xlabel("Phase shifter")
                ax.set_ylabel("Arb.")
                ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                ax.plot(x_plt,fit_cos(x_plt, *p), "b")
                # ax.set_ylim([0,1500])
                C=np.append(C, p[1]/p[0])
                C_err=np.append(C_err,  ((err[1]/p[0])**2+(err[1]*p[1]/p[0]**2)**2)**0.5)
print("C=", np.average(C), "+-", np.average(C_err))
plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Report/Images/C_ifg_07Nov.pdf", format="pdf",bbox_inches="tight")
# print("w_ps=", p[-2])
# print("chi_0=", p[-1])
plt.show()