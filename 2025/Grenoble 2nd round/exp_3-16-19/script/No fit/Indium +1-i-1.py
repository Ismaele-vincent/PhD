# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 11:58:42 2025

@author: S18
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
from datetime import datetime
colors=["k","#f10d0c","#00a933","#5983b0"]

dtype_new = np.dtype([
    ("date", "U50"),
    ("value", "f8"),
    ("index", "i8")
])

a_1=0.566
a_1_err=0
a_2=0.567
a_2_err=0
a_3=0.598
a_3_err=0

alpha=np.log((13112/12228+10878/10224)/2)/2

chi_1_0=0
chi_2_0=-np.pi/2
chi_3_0=np.pi

C_12=0.69
C_13=0.74
C_23=0.62

def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

bad_apples=[
    ]
good_apples=[
    ]
def w1(chi_1, chi_2, chi_3):
    return a_1*np.exp(1j*(chi_1_0+chi_1))/(a_1*np.exp(1j*(chi_1_0+chi_1))+a_2*np.exp(1j*(chi_2_0+chi_2))+a_3*np.exp(1j*(chi_3_0+chi_3)))

def w2(chi_1, chi_2, chi_3):
    return a_2*np.exp(1j*(chi_2_0+chi_2))/(a_1*np.exp(1j*(chi_1_0+chi_1))+a_2*np.exp(1j*(chi_2_0+chi_2))+a_3*np.exp(1j*(chi_3_0+chi_3)))

def w3(chi_1, chi_2, chi_3):
    return a_3*np.exp(1j*(chi_3_0+chi_3))/(a_1*np.exp(1j*(chi_1_0+chi_1))+a_2*np.exp(1j*(chi_2_0+chi_2))+a_3*np.exp(1j*(chi_3_0+chi_3)))

sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Ifg Indium/Cleantxt +1-i-1"

for root, dirs, files in os.walk(sorted_fold_path, topdown=False):
    files=np.sort(files)
    counts=np.array([], dtype=dtype_new)
    i=0
    for name in files[:]:
        if (name not in bad_apples):
            # print('"'+name[-13:-7]+'",')
            tot_data=np.loadtxt(os.path.join(root, name))[1:]
            # print(tot_data)
            time_count=tot_data[1]
            data_count=tot_data[2]#/(tot_data[2]+tot_data[3])
            if ("60s_In1" in name):
                counts=np.append(counts, np.array([(name[-13:-4],data_count,1)], dtype=dtype_new))
                print(name)
            if ("60s_In2" in name):
                counts=np.append(counts, np.array([(name[-13:-4],data_count,2)], dtype=dtype_new))
            if ("60s_In3" in name):
                counts=np.append(counts, np.array([(name[-13:-4],data_count,3)], dtype=dtype_new))
            if ("60s_No_In" in name):
                counts=np.append(counts, np.array([(name[-13:-4],data_count,0)], dtype=dtype_new))
            

colors=["k","#f10d0c","#00a933","#5983b0"]
fig = plt.figure(figsize=(7,7))
fig.suptitle(name[16:22], y=0.95)
gs = fig.add_gridspec(4,1, hspace=0.5)
axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[1, 0]),fig.add_subplot(gs[2, 0]),fig.add_subplot(gs[3, 0])]

counts = counts[np.argsort(np.array([datetime.strptime(x, "%d%b%H%M") for x in counts["date"]]))]

x_0=np.arange(len(counts["index"][counts["index"]==0]))
x_1=np.arange(len(counts["index"][counts["index"]==1]))
x_2=np.arange(len(counts["index"][counts["index"]==2]))
x_3=np.arange(len(counts["index"][counts["index"]==3]))
X=[x_0,x_1,x_2,x_3]

counts_No_In=counts["value"][counts["index"]==0]
counts_In1=counts["value"][counts["index"]==1]
counts_In2=counts["value"][counts["index"]==2]
counts_In3=counts["value"][counts["index"]==3]

# print(x_0)
axs[0].errorbar(range(len(counts_No_In)), counts_No_In, yerr=counts_No_In**0.5, fmt="o", color=colors[0], capsize=5, ms=3, label="No In")
axs[1].errorbar(range(len(counts_In1)), counts_In1, yerr=counts_In1**0.5, fmt="o", color=colors[1], capsize=5, ms=3, label="In1")
axs[2].errorbar(range(len(counts_In2)), counts_In2, yerr=counts_In2**0.5, fmt="o", color=colors[2], capsize=5, ms=3, label="In2")
axs[3].errorbar(range(len(counts_In3)), counts_In3, yerr=counts_In3**0.5, fmt="o", color=colors[3], capsize=5, ms=3, label="In3")
# ax[0].set_xticks(range(len(counts_In1)))
# ax.set_xticklabels(["0","1","2","3"])
titles=["No In","In1", "In2", "In3"]
i=0
for ax in axs:
    ax.grid(True, ls="dotted")
    ax.set_title(titles[i])
    # ax.legend()
    # ax.tick_params(axis="x", bottom=False, labelbottom=False)
    ax.set_xticks(X[i])
    ax.set_xticklabels(counts["date"][counts["index"]==i])#,rotation=10, ha='right')
    i+=1
    
counts_array=np.array([np.average(counts_No_In),np.average(counts_In1),np.average(counts_In2),np.average(counts_In3)])
counts_array_err = counts_array**0.5
counts_array_err/=counts_array[0]
counts_array/=counts_array[0]

Re_wv=np.array([0, w1(0, 0, 0).real, w2(0, 0, 0).real, w3(0, 0, 0).real])
Re_wv=1-2*alpha*Re_wv

fig = plt.figure(figsize=(4,4))
fig.suptitle("$\psi=(+e^{-i\pi/3},+1,+e^{2\pi/3})/\\sqrt{3}$")
ax = fig.add_subplot(111)
ax.errorbar([0,1,2,3], counts_array,yerr=counts_array_err,fmt="ko",capsize=5, ms=3, label="Data")
ax.errorbar([0,1,2,3], Re_wv, fmt="s",color=colors[1], ms=5,label="Theory")
ax.set_ylabel("$\mathrm{I_{in}/I_0}$", fontsize=13)
ax.set_xticks([0,1,2,3])
ax.set_xticklabels(["No In","In 1","In 2","In 3"])
ax.legend()

# fig = plt.figure(figsize=(5,5))
# gs = fig.add_gridspec(2,1, hspace=0.3, height_ratios=(2,1))
# axs1 = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[1, 0])]
# fig.suptitle("$\psi$=("+name[16:18]+","+name[18:20]+","+name[20:22]+")/$\\sqrt{3}$" )
# axs1[0].errorbar([0,1,2,3], counts_array,yerr=counts_array_err,fmt="ko",capsize=5, ms=3)
# axs1[0].set_xticks([0,1,2,3])
# axs1[0].set_xticklabels(["No In","In 1","In 2","In 3"])
# axs1[0].set_title("Intensity", fontsize=10)
# axs1[1].errorbar([0,1,2,3], Re_wv, fmt="s",color=colors[1], ms=5)
# axs1[1].set_xticks([0,1,2,3])
# axs1[1].set_xticklabels(["No In","In 1","In 2","In 3"])
# axs1[1].set_title("1-$2 \\alpha Re(w_{+,i})$", fontsize=12)

plt.show()