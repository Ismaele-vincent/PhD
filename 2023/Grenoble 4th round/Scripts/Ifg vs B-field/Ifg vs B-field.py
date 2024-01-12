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

def contr(x, A, a_1):
    B=a_1*x
    return A*abs(jv(0,B))

def B(T,f,alpha):
    w=f*2*np.pi
    return alpha/(mu_N/(hbar*w)*2*np.sin(w*T*1e-3/2))



def fit_O_beam(t, A, B, a_1, xi_1):
    # a_1=alpha(T,f_1,c_1)
    # xi_1=phi_1+(2*np.pi*f_1*1e-3*T+np.pi)/2#-2*np.pi*f_1*1e3/v0
    chi_fit=chi
    return A + B*np.cos(chi_fit-a_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1))/2
# inf_file_name="ifg_vs_A_2kHzB_12p_14Nov0129"
# inf_file_name="ifg_vs_A_2kHzB_12p_13Nov2313"
# inf_file_name="ifg_vs_A_2kHzB_12p_13Nov2129"
inf_file_name="ifg_vs_B_3kHzB_09Nov1137"
# inf_file_name="ifg_vs_B_3kHzB_13p_30s_17Nov0603"
print(inf_file_name)
sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/Ifg vs B-field/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"
i=0
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    for name in files:
        if i==0:
            tot_data=np.loadtxt(os.path.join(root, name))[:,:]
            ps_pos=tot_data[:,0]
            f_1=2
            print(name)
            i+=1
        else:
            data=np.loadtxt(os.path.join(root, name))[:,:]
            tot_data = np.vstack((tot_data, data))
               
amplitude=tot_data[::len(ps_pos),-1]
print(amplitude)
current=amplitude
# current=np.array([0.333, 0.667, 1, 1.333, 1.667, 2, 2.333, 2.667, 3, 3.333, 3.667, 4, 4.333, 4.667, 5, 5.333, 5.667, 6])/2
# current=np.array([0,0.45, 0.884, 1.315, 1.75, 2.18, 2.6, 3.02, 3.22, 3.42, 3.645])/2
# current=np.array([0,0.402, 0.788, 1.18, 1.57, 1.95, 2.09, 2.23, 2.35, 2.73, 3.11, 3.49, 3.85])/2

# amplitude=amplitude[:-10]
# current=current[:-10]


# current=np.array([1.2, 1.76, 3.6, 5.8, 7.3, 10.3, 13.6, 16.4])/2
# print(amplitude)
N = len(ps_pos)
print(N)
S_F=11.1111
matrix=np.zeros((len(amplitude),len(ps_pos)))
matrix_err=np.zeros((len(amplitude),len(ps_pos)))
for i in range(len(amplitude)):
    matrix[i]=tot_data[:,2][tot_data[:,-1]==amplitude[i]]+tot_data[:,5][tot_data[:,-1]==amplitude[i]]
    matrix_err[i]=matrix[i]**0.5

ps_plt=np.linspace(ps_pos[0], ps_pos[-1], 500)
chi_0=np.zeros(len(amplitude))
chi_0_err=np.zeros(len(amplitude))
C=np.zeros(len(amplitude))
C_err=np.zeros(len(amplitude))

for i in range(len(amplitude)):
    ps_data=matrix[i]
    P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, -3]
    B0=([0,0,2.5,-10],[np.amax(ps_data)+100,np.amax(ps_data)+100,3.5, 10])
    p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0, sigma=matrix_err[i])
    err=np.diag(cov)**0.5
    C[i] = p[1]/p[0]
    C_err[i] = ((1/p[0]*err[1])**2+(p[1]/p[0]**2*err[0])**2)**0.5
    w_ps=p[-2]
    chi_0[i]=p[-1]
    chi_0_err[i]=err[-1]
    # fig = plt.figure(figsize=(8,6))
    # ax = fig.add_subplot(111)
    # ax.errorbar(ps_pos, matrix[i], yerr= matrix_err[i], fmt="ko")
    # ax.plot(ps_plt, fit_cos(ps_plt,*p))
    # ax.set_title(str("%.2f"%amplitude[i],))
    # print(C[i], w_ps, chi_0[i])
# C[6]=0
curr_plt=np.linspace(current[0], current[-1], 10000)
ampl_plt=np.linspace(0, amplitude[-1], 1000)
p,cov=fit(contr, current, C, p0=[2500,0.5])
err=np.diag(cov)**0.5
print(p, np.diag(cov)**0.5)
print(curr_plt[contr(curr_plt,*p)==np.amin(contr(curr_plt,*p))])
alpha_plt=p[-1]*curr_plt#alpha(T, f_1, p[-1]*curr_plt)
alpha_0=alpha_plt[contr(curr_plt,*p)==np.amin(contr(curr_plt,*p))]
curr_0=curr_plt[contr(curr_plt,*p)==np.amin(contr(curr_plt,*p))]
print(alpha_0, curr_0)
print("alpha/V_c=",p[1],"+-",err[1])
print("alpha=",p[1]*2.01,"+-", err[1]*2.01)
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
# ax.errorbar(amplitude, chi_0, yerr= chi_0_err, fmt="ko")
ax.errorbar(current, C, yerr= C_err, fmt="k.")
ax.errorbar(curr_plt, contr(curr_plt,*p))
ax.set_xlabel("$V_p$ [V]")
# ax.vlines(curr_0, 0, 0.5, color="k", ls="dashed")
# ax.text(curr_0, 0.5, "$\\alpha\\approx$"+str("%.4f" %(alpha_0,)) ,va="bottom", ha="center")
# ax.set_ylim([0,1])
# plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/Report/Images/C_bessel_B_3kHz.pdf", format="pdf",bbox_inches="tight")
plt.show()
# print(0.5943036898178375/0.7253879170974153)