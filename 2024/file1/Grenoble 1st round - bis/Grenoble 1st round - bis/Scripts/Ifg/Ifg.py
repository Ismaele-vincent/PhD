# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:37:41 2023

@author: S18
"""
"""
inf_file_names:
No indium:
"ifgPS1_2p_22pt_03Apr1953", 
"ifgPS1_2p_22pt_03Apr2023",
Indium 1.8 mm:
"ifgPS1_2p_22pt_03Apr2002", 
"ifgPS1_2p_22pt_03Apr2033"



inf file names:
"ifgPS1_2p_22pt_30Mar1656", 
"ifgPS1_2p_22pt_30Mar2129", 
"ifgPS1_2p_22pt_31Mar0104", 
"ifgPS1_2p_22pt_31Mar1557", 
"ifgPS1_2p_22pt_31Mar1645", 
"ifgPS1_2p_22pt_31Mar1751", 
"ifgPS1_2p_22pt_31Mar2116", 
"ifgPS1_2p_22pt_01Apr0408", 
"ifgPS1_2p_22pt_01Apr0429", 
"ifgPS1_2p_22pt_01Apr2138", 
"ifgPS1_2p_22pt_01Apr2148", 
"ifgPS1_2p_22pt_02Apr0615", 
"ifgPS1_2p_22pt_02Apr0625", 
"ifgPS1_2p_22pt_02Apr1622", 
"ifgPS1_2p_22pt_02Apr2011", 
"ifgPS1_2p_22pt_02Apr2032", 
"ifgPS1_2p_22pt_03Apr0405", 
"ifgPS1_2p_22pt_03Apr0426", 
"ifgPS1_2p_22pt_03Apr1201", 
"ifgPS1_2p_22pt_03Apr1848", 
"ifgPS1_2p_22pt_03Apr1953",
Indium 1.8 mm: 
"ifgPS1_2p_22pt_03Apr2002", 
"ifgPS1_2p_22pt_03Apr2023", 

"ifgPS1_2p_22pt_03Apr2033", 
"ifgPS1_2p_22pt_03Apr2055", 
"ifgPS1_2p_22pt_03Apr2110", 
Indium 1mm:
"ifgPS1_2p_22pt_03Apr2146", 
"ifgPS1_2p_22pt_04Apr0531", 
"ifgPS1_2p_22pt_04Apr0622", 



"ifgPS1_2p_22pt_06Apr1714", 
"ifgPS1_2p_22pt_06Apr1735",
"""


import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
a_1=1/2**0.5
a_2=1/2**0.5

def fit_cos(x, A, B, C, D):
    return A/2*(1+B*np.cos(C*x-D))



inf_file_name_ifg="ifgPS1_2p_22pt_06Apr1735"
sorted_fold_path_ifg="C:/Users/S18/Desktop/Grenoble-2024 Ismaele/2024/Grenoble 1st round - bis/exp_CRG-3126/Sorted data/Ifg/"+inf_file_name_ifg
cleandata_ifg=sorted_fold_path_ifg+"/Cleantxt"
a_21=1/2
for root, dirs, files in os.walk(cleandata_ifg, topdown=False):
    for name in files:
         tot_data=np.loadtxt(os.path.join(root, name))
data_ifg=tot_data[:,2]
data_ifg_err=data_ifg**0.5
ps_pos=tot_data[:,0]
P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, -0.5]
print(P0)
B0=([np.amin(data_ifg),0,0.001,-6],[np.amax(data_ifg)*2,np.amax(data_ifg)*2,6, 6])

p_ifg,cov_ifg=fit(fit_cos, ps_pos, data_ifg, p0=P0,  bounds=B0)
err_ifg=np.diag(cov_ifg)**0.5
Co = p_ifg[1]
A=p_ifg[0]*(1-Co)/2
A_err= (((1-Co)/2*err_ifg[0])**2+(p_ifg[0]/2*err_ifg[1])**2)**0.5
w_ps=p_ifg[-2]
chi_0=p_ifg[-1]
chi_0_err=err_ifg[-1]
print("A(1-C)/2=", A, "+-", A_err)
print("C=",Co, "+-", err_ifg[1])
print("chi_err=",err_ifg[-1])
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
ax.errorbar(ps_pos,data_ifg, yerr=data_ifg**0.5,fmt="ko",capsize=5, ms=3)
ax.plot(ps_plt,fit_cos(ps_plt, *p_ifg), "b")
# ax.vlines(p_ifg[-1]/p_ifg[-2],fit_cos(p_ifg[-1]/p_ifg[-2]+np.pi,*p_ifg),fit_cos(p_ifg[-1]/p_ifg[-2],*p_ifg), color="k")
plt.show()