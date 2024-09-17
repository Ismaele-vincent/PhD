# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:37:41 2023

@author: S18
"""
"""
inf_file_names:

"""


import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
a_1=1/2**0.5
a_2=1/2**0.5
sgn=1
colors=["k","#f10d0c","#00a933","#5983b0"]
labels=["$\chi_0=0$", "$\chi_0=\\dfrac{\pi}{2}$", "$\chi_0=\pi$", "$\chi_0=\\dfrac{3\pi}{2}$"]
def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

"""
Indium 0.8mm path2
"""
# P1=(121375+124156)/2/10
# a_1=0.840
# a_1_err=0.003
# a_2=0.542
# a_2_err=0.005
# a_21=a_2/a_1
# lim=0
# inf_file_name="ifgPS1_3p_45pt_In08_17Mar1718"
# points=45

"""
Indium 1.8mm path2
"""
# P1=(121375+124156)/2/10
# a_1=0.915
# a_1_err=0.003
# a_2=0.404
# a_2_err=0.008
# a_21=a_2/a_1
# lim=0
# inf_file_name="ifgPS1_PS2_3p_45pt_In18_18Mar1055"
# points=45

# """
# Indium 0.8mm path2 (Bad, intensity going down)
# """

# # a_1=0.840
# # a_1_err=0.003
# # a_2=0.542
# # a_2_err=0.005
# # a_21=a_2/a_1
# # lim=0
# # inf_file_name="ifgPS1_PS2_42pt_In08_18Mar2141"
# # inf_file_name="ifgPS1_PS2_42pt_In08_19Mar1120"
# # points=42

# """
# Indium 0.8mm path2  (Bad, intensity and/or phase not good. Gets progressively better, but still not good.)
# """
# # a_1=0.840
# # a_1_err=0.003
# # a_2=0.542
# # a_2_err=0.005
# # a_21=a_2/a_1
# # lim=0
# # inf_file_name="ifgPS1_PS2_42pt_In08_18Mar2141"
# # inf_file_name="ifgPS1_PS2_42pt_In08_19Mar1120"
# # inf_file_name="ifgPS1_42pt_In08_19Mar1548"
# # inf_file_name="ifgPS1_42pt_In08_19Mar1726"
# # inf_file_name="ifgPS1_42pt_In08_19Mar1940"
# # inf_file_name="ifgPS1_42pt_In08_19Mar2054"
# # # inf_file_name="ifgPS1_42pt_In08_19Mar2208"
# # # inf_file_name="ifgPS1_42pt_In08_19Mar2322"
# # points=42

"""
Indium 1.8mm path2 (overall good, last two very good)
"""
# P1=(121375+124156)/2/30
# a_1=0.915
# a_1_err=0.003
# a_2=0.404
# a_2_err=0.008
# a_21=a_2/a_1
# lim=0
# # inf_file_name="ifgPS1_42pt_In18_20Mar0121" #weird amplitude
# # inf_file_name="ifgPS1_42pt_In18_20Mar0235" #weird amplitude
# # inf_file_name="ifgPS1_42pt_In18_20Mar0349" 
# # inf_file_name="ifgPS1_42pt_In18_20Mar0503" #wrong phase
# inf_file_name="ifgPS1_42pt_In18_20Mar0617" 
# inf_file_name="ifgPS1_42pt_In18_20Mar0731"
# points=42

"""
No Indium, 3-plates interferometer
"""
# P1=57079/15
# a_1= 0.688
# a_1_err=0.003
# a_2= 0.725
# a_2_err=0.003
# a_21=a_2/a_1
# lim=1
# # sgn=-1
# inf_file_name="ifgPS1_35pt_In00_12Apr1851" #good-ish 3p
# inf_file_name="ifgPS1_35pt_In00_12Apr2026" #good 3p
# inf_file_name="ifgPS1_35pt_In00_13Apr0103" #good
# inf_file_name="ifgPS1_35pt_In00_13Apr0528"  #good
# inf_file_name="ifgPS1_35pt_In00_13Apr0703" #good
# inf_file_name="ifgPS1_35pt_In00_13Apr0838" #good
# points=35

"""
Indium 1.5, 3-plates interferometer
"""
P1=57079/15
a_1= 0.862
a_1_err=0.005
a_2= 0.507
a_2_err=0.008
a_21=a_2/a_1
lim=0
# inf_file_name="ifgPS1_35pt_In15_13Apr2126" #very good
# inf_file_name="ifgPS1_35pt_In15_14Apr0146" #bad
inf_file_name="ifgPS1_35pt_In15_14Apr0322" #very good
# inf_file_name="ifgPS1_35pt_In15_14Apr0742" #very good
points=35

"""
Indium 0.5, 3-plates interferometer
"""
# P1=57079/15
# a_1= 0.770
# a_1_err=0.004
# a_2= 0.638
# a_2_err=0.005
# a_21=a_2/a_1
# lim=0
# # inf_file_name="ifgPS1_35pt_In05_14Apr0929" #good-ish (phase a bit bad)
# # inf_file_name="ifgPS1_35pt_In05_14Apr1349" #bad (wrong ps pos)
# # inf_file_name="ifgPS1_35pt_In05_14Apr1524" #bad (wrong ps pos)
# # inf_file_name="ifgPS1_35pt_In05_15Apr1731" #good-ish (big error bars)
# # inf_file_name="ifgPS1_35pt_In05_15Apr1907" #good-ish (phase a bit bad)
# # inf_file_name="ifgPS1_35pt_In05_15Apr2042" #good-ish (phase a bit bad)
# # inf_file_name="ifgPS1_35pt_In05_15Apr2218" #probably best
# # inf_file_name="ifgPS1_35pt_In05_15Apr2354" #good-ish (1 bad point)
# # inf_file_name="ifgPS1_35pt_In05_16Apr0130" #good
# # inf_file_name="ifgPS1_35pt_In05_16Apr0305" #good-ish
# inf_file_name="ifgPS1_35pt_In05_16Apr0441" #good
# # inf_file_name="ifgPS1_35pt_In05_16Apr0617" #good-ish (phase a bit bad)
# # inf_file_name="ifgPS1_35pt_In05_16Apr0752" #bad, last measurement incomplete
# points=35

"""
Indium 1.0, 3-plates interferometer
"""
# P1=57079/15
# a_1= 0.821
# a_1_err=0.004
# a_2= 0.570
# a_2_err=0.006
# a_21=a_2/a_1
# lim=0
# # inf_file_name="ifgPS1_35pt_In10_14Apr2054" #bad (wrong ps pos)
# # inf_file_name="ifgPS1_35pt_In10_15Apr0115" #bad (wrong ps pos)
# # inf_file_name="ifgPS1_35pt_In10_15Apr0250" #bad (wrong ps pos)
# # inf_file_name="ifgPS1_35pt_In10_15Apr0710" #bad (wrong ps pos)
# # inf_file_name="ifgPS1_35pt_In10_15Apr0845" #bad (wrong ps pos)
# inf_file_name="ifgPS1_35pt_In10_15Apr1050" #good
# # inf_file_name="ifgPS1_35pt_In10_15Apr1225" #good
# points=35

def w1(chi, a_21):
    return 1/(1+a_21*np.exp(1j*chi))

def w2(chi, a_21):
    return 1-w1(chi, a_21)

print(inf_file_name)
sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/exp_CRG-3125/Sorted data/Ifg/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"
chi_0=[0, np.pi/2, np.pi, 3*np.pi/2]
i=0
A_avg=0
Dchi=np.zeros(4)
C_avg=0
C_err=0
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111)
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    # data_ifg_matrix=np.zeros((4,points))
    # data_ifg_matrix=np.zeros((4,points))
    for name in files:
        # print(name)
        tot_data=np.loadtxt(os.path.join(root, name))
        time=tot_data[0,1]
        print(time)
        data_ifg=tot_data[:,2]
        data_ifg_err=data_ifg**0.5
        ps_pos=tot_data[:,0]
        P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, -0.6+chi_0[i]]
        B0=([np.amin(data_ifg),0,0.01,-3.5],[np.amax(data_ifg)*2,np.amax(data_ifg)*2,5, 2*np.pi])
        p,cov=fit(fit_cos, ps_pos, data_ifg, sigma=data_ifg_err, p0=P0,  bounds=B0)
        if i==0:
            chi=ps_pos*p[2]-p[3]
            chi_plt=np.linspace(chi[0],chi[-1],200)
        # P0_unb=[100000, 3, -0.5, 0.7]
        # B0_unb=([0,1,-10, 0],[1e10,4,10,1])
        # p_unb,cov_unb=fit(fit_cos_unb, ps_pos, data_ifg, p0=P0_unb,  bounds=B0_unb)
        err=np.diag(cov)**0.5
        A_avg+=p[0]/4
        C_avg+=p[1]/p[0]/4
        C_err+=p[1]**2/p[0]**4*err[0]**2+err[1]**2/p[0]**2
        A_err=err[0]**2
        x_plt = np.linspace(ps_pos[0], ps_pos[-1],200)
        ax.errorbar(chi,data_ifg/time,yerr=data_ifg_err/time,fmt="o",color=colors[i],capsize=5, ms=3)
        ax.fill_between([], [],color=colors[i],label=labels[i])
        ax.errorbar(chi_plt,fit_cos(x_plt, *p)/time, fmt="--", color=colors[i])
        # # ax.set_ylim([0,1500])
        # print("C=", p[1]/p[0], "+-", ((err[1]/p[0])**2+(err[1]*p[1]/p[0]**2)**2)**0.5)
        # print("C_unb=", p_unb[-1])
        # print(p_unb)
        # print("w_ps=", p[-2], "+-", err[-2])
        # print("chi_0=", p[-1])
        Dchi[i]=p[3]
        # print(p[3])
        i+=1
fig.legend(loc=9,framealpha=1, ncol=4)
ax.legend("none")
ax.errorbar([],[],[],fmt="o",color=(0.5, 0.5, 0.5), capsize=5, ms=3, label="Data")
ax.errorbar([],[],fmt="--",color=(0.5, 0.5, 0.5), label="Fit")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[-2:], framealpha=1, loc=2)
ax.set_xlabel("$\chi$ [rad]")
ax.set_ylabel("Neutron rate (count / s)")

# plt.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Images/Measurement example.pdf", format="pdf",bbox_inches="tight")
plt.show()