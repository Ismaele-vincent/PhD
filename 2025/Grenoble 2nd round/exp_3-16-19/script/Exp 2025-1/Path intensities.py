# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 15:50:57 2025

@author: S18
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
import My_module_Exp_2025_1 as mymod

sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Ifg wv no fit/Int measurements"

I_1=np.array([])
I_2=np.array([])
I_3=np.array([])
I_1_err=np.array([])
I_2_err=np.array([])
I_3_err=np.array([])
times=np.array([])
names=np.array([])
for root, dirs, files in os.walk(sorted_fold_path, topdown=False):
    files=np.sort(files)
    for name in files[1:]:
        # print(name)
        names=np.append(names, name)
        int_data=np.loadtxt(os.path.join(root, name), encoding='windows-1252', comments="*",skiprows=13,delimiter="\t")[:,3]
        I_1=np.append(I_1,int_data[1])
        I_2=np.append(I_2,int_data[0])
        I_3=np.append(I_3,int_data[2])
        I_1_err=np.append(I_1_err,int_data[1]**0.5)
        I_2_err=np.append(I_2_err,int_data[0]**0.5)
        I_3_err=np.append(I_3_err,int_data[2]**0.5)
        time_int=np.loadtxt(os.path.join(root, name), encoding='windows-1252', comments="*",skiprows=13,delimiter="\t")[0,2]
        times=np.append(time_int, times)
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.errorbar(np.arange(len(I_1)), I_1,yerr=I_1_err,fmt="ro",capsize=5, ms=3)
ax.errorbar(np.arange(len(I_2)), I_2,yerr=I_2_err,fmt="go",capsize=5, ms=3)
ax.errorbar(np.arange(len(I_3)), I_3,yerr=I_3_err,fmt="bo",capsize=5, ms=3)

a_1=(I_1/(I_1+I_2+I_3))**0.5
a_2=(I_2/(I_1+I_2+I_3))**0.5
a_3=(I_3/(I_1+I_2+I_3))**0.5
print(np.average(I_1)/60, np.average(I_1_err)**0.5/60, np.std(I_1/60))
print(np.average(I_2)/60, np.average(I_2_err)**0.5/60, np.std(I_2/60))
print(np.average(I_3)/60, np.average(I_3_err)**0.5/60, np.std(I_3/60))

print("a_1,a_2,a_3=",np.average(a_1), ",", np.average(a_2), ",", np.average(a_3))
print((np.average(I_1)/(np.average(I_1+I_2+I_3))))
print((np.average(I_2)/(np.average(I_1+I_2+I_3))))
print((np.average(I_3)/(np.average(I_1+I_2+I_3))))
plt.show()