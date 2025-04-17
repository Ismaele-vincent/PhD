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
def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

"""
Indium 0.8mm path2
"""
# folder_name="Skew In 0p8 path2"
# P1=(121375+124156)/2/10
# P2=0.538*P1
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
# folder_name="Skew In 1p8 path2"
# P1=(121375+124156)/2/10
# P2=0.252*P1
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

# folder_name="Skew In 1p8 path2"
# P1=(121375+124156)/2/30
# P2=0.252*P1
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
# # inf_file_name="ifgPS1_42pt_In18_20Mar0617" 
# # inf_file_name="ifgPS1_42pt_In18_20Mar0731"
# points=42

"""
No Indium, 3-plates interferometer
"""
# folder_name="Symm No In"
# P1=57079/15
# P2=63441/15
# a_1= 0.688
# a_1_err=0.003
# a_2= 0.725
# a_2_err=0.003

# P1=57079/15
# P2=P1#63441/15
# a_1= 0.5**0.5
# a_1_err=0.003
# a_2= 0.5**0.5
# a_2_err=0.003

# a_21=a_2/a_1
# lim=1
# # sgn=-1
# # inf_file_name="ifgPS1_35pt_In00_12Apr1851" #good-ish 3p
# # inf_file_name="ifgPS1_35pt_In00_12Apr2026" #good 3p
# # inf_file_name="ifgPS1_35pt_In00_13Apr0103" #good
# # inf_file_name="ifgPS1_35pt_In00_13Apr0528"  #good
# # inf_file_name="ifgPS1_35pt_In00_13Apr0703" #good
# inf_file_name="ifgPS1_35pt_In00_13Apr0838" #good
# points=35

"""
Indium 1.5, 3-plates interferometer
"""
# folder_name="Symm In 1p5 path2"
# P1=57079/15
# P2=19747/15
# a_1= 0.862
# a_1_err=0.005
# a_2= 0.507
# a_2_err=0.008
# a_21=a_2/a_1
# lim=0
# inf_file_name="ifgPS1_35pt_In15_13Apr2126" #best
# # inf_file_name="ifgPS1_35pt_In15_14Apr0146" #bad
# # inf_file_name="ifgPS1_35pt_In15_14Apr0322" #very good
# # inf_file_name="ifgPS1_35pt_In15_14Apr0742" #very good
# points=35

"""
Indium 0.5, 3-plates interferometer
"""
# folder_name="Symm In 0p5 path2"
# P1=57079/15
# P2=39190/15
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
# inf_file_name="ifgPS1_35pt_In05_15Apr2218" #probably best
# # inf_file_name="ifgPS1_35pt_In05_15Apr2354" #good-ish (1 bad point)
# # inf_file_name="ifgPS1_35pt_In05_16Apr0130" #good
# # inf_file_name="ifgPS1_35pt_In05_16Apr0305" #good-ish
# # inf_file_name="ifgPS1_35pt_In05_16Apr0441" #good
# # inf_file_name="ifgPS1_35pt_In05_16Apr0617" #good-ish (phase a bit bad)
# # inf_file_name="ifgPS1_35pt_In05_16Apr0752" #bad, last measurement incomplete
# points=35

"""
Indium 1.0, 3-plates interferometer
"""
folder_name="Symm In 1p0 path2"
P1=57079/15
P2=27549/15
a_1= 0.821
a_1_err=0.004
a_2= 0.570
a_2_err=0.006
a_21=a_2/a_1
lim=0
# inf_file_name="ifgPS1_35pt_In10_14Apr2054" #bad (wrong ps pos)
# inf_file_name="ifgPS1_35pt_In10_15Apr0115" #bad (wrong ps pos)
# inf_file_name="ifgPS1_35pt_In10_15Apr0250" #bad (wrong ps pos)
# inf_file_name="ifgPS1_35pt_In10_15Apr0710" #bad (wrong ps pos)
# inf_file_name="ifgPS1_35pt_In10_15Apr0845" #bad (wrong ps pos)
inf_file_name="ifgPS1_35pt_In10_15Apr1050" #good
# inf_file_name="ifgPS1_35pt_In10_15Apr1225" #good
points=35

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
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    data_ifg_matrix=np.zeros((4,points))
    for name in files:
        # print(name)
        tot_data=np.loadtxt(os.path.join(root, name))
        data_ifg=tot_data[:,2]
        data_ifg_matrix[i]=data_ifg
        data_ifg_err=data_ifg**0.5
        ps_pos=tot_data[:,0]
        P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, -0.6+chi_0[i]]
        B0=([np.amin(data_ifg),0,0.01,-3.5],[np.amax(data_ifg)*2,np.amax(data_ifg)*2,5, 2*np.pi])
        p,cov=fit(fit_cos, ps_pos, data_ifg, sigma=data_ifg_err, p0=P0,  bounds=B0)
        # P0_unb=[100000, 3, -0.5, 0.7]
        # B0_unb=([0,1,-10, 0],[1e10,4,10,1])
        # p_unb,cov_unb=fit(fit_cos_unb, ps_pos, data_ifg, p0=P0_unb,  bounds=B0_unb)
        err=np.diag(cov)**0.5
        A_avg+=p[0]/4
        C_avg+=p[1]/p[0]/4
        C_err+=p[1]**2/p[0]**4*err[0]**2+err[1]**2/p[0]**2
        A_err=err[0]**2
        x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
        # fig = plt.figure(figsize=(8,6))
        # ax = fig.add_subplot(111)

        # fig.suptitle(name[:-4])
        # ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
        # ax.plot(x_plt,fit_cos(x_plt, *p), "b")
        # # ax.set_ylim([0,1500])
        # print("C=", p[1]/p[0], "+-", ((err[1]/p[0])**2+(err[1]*p[1]/p[0]**2)**2)**0.5)
        # print("C_unb=", p_unb[-1])
        # print(p_unb)
        # print("w_ps=", p[-2], "+-", err[-2])
        # print("chi_0=", p[-1])
        Dchi[i]=p[3]
        # print(p[3])
        if i==0:
            chi=ps_pos*p[2]-p[3]
        i+=1
print(abs(Dchi-Dchi[[1,2,3,0]])/np.pi*2)
C_err=C_err**0.5/4
A_err=A_err**0.5/4
print("A_avg=",A_avg, "+-",A_err)

C_id=C_avg/(2*a_1*a_2)
C_id_err=(C_err**2+C_avg**2/(a_1**2)*a_1_err**2+C_avg**2/(a_2**2)*a_2_err**2)**0.5/(2*a_1*a_2)
print("C_avg=",C_avg, "+-",C_err, "C_ideal=", C_id, "+-", C_id_err)

data_ifg_matrix_err=(data_ifg_matrix+((1-C_id)/2)**2*A_err**2+(A_avg/2)**2*C_id_err**2)**0.5
# data_ifg_matrix_err=(data_ifg_matrix/C_id**2+((1/C_id+1)/2)**2*A_err**2+(A_avg/2-data_ifg_matrix)**2*(C_id_err/C_id**2)**2)**0.5
data_ifg_matrix-=A_avg*(1-C_id)
P1_corr=C_id*P1
P1_corr_err=(C_id**2*P1+P1**2*C_id_err**2)**0.5
P2_corr=C_id*P2
P2_corr_err=(C_id**2*P2+P2**2*C_id_err**2)**0.5

chi_plt=np.linspace(chi[0], chi[-1], 1000)
Im_1=(data_ifg_matrix[3]-data_ifg_matrix[1])/data_ifg_matrix[0]/4
Im_1_err=(data_ifg_matrix_err[1]**2+data_ifg_matrix_err[3]**2+(4*Im_1)**2*data_ifg_matrix_err[0]**2)**0.5/(4*abs(data_ifg_matrix[0]))

Im_2=-(data_ifg_matrix[3]-data_ifg_matrix[1])/data_ifg_matrix[0]/4
Im_2_err=(data_ifg_matrix_err[1]**2+data_ifg_matrix_err[3]**2+(4*Im_2)**2*data_ifg_matrix_err[0]**2)**0.5/(4*abs(data_ifg_matrix[0]))

sa=data_ifg_matrix[2]/data_ifg_matrix[0]-4*Im_1**2
s=np.sign(sa)*abs(sa)**0.5
Re_1_1=(1+s)/2
Re_1_1_err=((data_ifg_matrix_err[2]/data_ifg_matrix[0])**2+(data_ifg_matrix[2]*data_ifg_matrix_err[0]/data_ifg_matrix[0]**2)**2+64*Im_1**2*Im_1_err**2)**0.5/abs(s)/4

Re_1_2=P1_corr/data_ifg_matrix[0] + 1/4 - data_ifg_matrix[2]/(data_ifg_matrix[0]*4)
Re_1_2_err=(P1_corr_err**2+(data_ifg_matrix_err[2]/4)**2+(Re_1_2-1/4)**2*data_ifg_matrix_err[0]**2)**0.5/abs(data_ifg_matrix[0])

s_1=P1_corr/data_ifg_matrix[0]-Im_1**2
Re_1_3=np.sign(s_1)*np.abs(s_1)**0.5
Re_1_3_err=((P1_corr_err/data_ifg_matrix[0])**2+(P1_corr/data_ifg_matrix[0]**2)**2*data_ifg_matrix_err[0]**2+4*Im_1**2*Im_1_err**2)**0.5/Re_1_3/2

sa=data_ifg_matrix[2]/data_ifg_matrix[0]-4*Im_2**2
s=np.sign(sa)*abs(sa)**0.5
Re_2_1=(1-s)/2
Re_2_1_err=((data_ifg_matrix_err[2]/data_ifg_matrix[0])**2+(data_ifg_matrix[2]*data_ifg_matrix_err[0]/data_ifg_matrix[0]**2)**2+64*Im_1**2*Im_1_err**2)**0.5/abs(s)/4

Re_2_2=P2_corr/data_ifg_matrix[0] +1/4 - data_ifg_matrix[2]/(data_ifg_matrix[0]*4) 
Re_2_2_err=(P1_corr_err**2+(data_ifg_matrix_err[2]/4)**2+(Re_2_2-1/4)**2*data_ifg_matrix_err[0]**2)**0.5/abs(data_ifg_matrix[0])

s_2=P2_corr/data_ifg_matrix[0]-Im_2**2
Re_2_3=np.sign(s_2)*np.abs(s_2)**0.5
Re_2_3_err=((P2_corr_err/data_ifg_matrix[0])**2+(P2_corr/data_ifg_matrix[0]**2)**2*data_ifg_matrix_err[0]**2+4*Im_1**2*Im_1_err**2)**0.5/Re_2_3/2

fig = plt.figure(figsize=(5,6), dpi=150)
gs = fig.add_gridspec(2,2 , height_ratios=(1,1), hspace=0.0, wspace=0.3)
axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[0, 1]),fig.add_subplot(gs[1, 0]),fig.add_subplot(gs[1, 1])]
axs[0].set_title("$w_{1,+}$", fontsize=13)
axs[1].set_title("$w_{2,+}$", fontsize=13)
axs[0].set_ylabel("Real part")
axs[2].set_ylabel("Imaginary part")
# fig.suptitle(inf_file_name)
colors=["k","#f10d0c","#00a933","#5983b0"]
plt.rcParams["mathtext.fontset"]="cm"
for ax in axs:
    ax.set_xticks([-np.pi,0,np.pi])
    ax.set_xticklabels(["$\mathdefault{-\pi}$", "$\mathdefault{0}$","$\mathdefault{\pi}$"])
    ax.grid(True, ls="dotted")
for ax in axs[2:]:
    ax.set_xlabel("$\mathdefault{\\chi_0}$ [rad]")
axs[0].tick_params(axis="x", bottom=False, labelbottom=False)
axs[1].tick_params(axis="x", bottom=False, labelbottom=False)
# axs[1].tick_params(axis="y", left=False, labelleft=False)
# axs[3].tick_params(axis="y", left=False, labelleft=False)
    
axs[2].errorbar(chi,Im_1, Im_1_err, fmt="k.", capsize=3)
axs[2].plot(chi_plt, w1(chi_plt, a_21).imag, color=colors[3], alpha=0.8 )
axs[3].errorbar(chi,Im_2, Im_2_err, fmt="k.", capsize=3)
axs[3].plot(chi_plt, w2(chi_plt, a_21).imag, color=colors[3], alpha=0.8 )

axs[0].set_ylim([0.25,3.75])
axs[1].set_ylim([-3,0.5])
axs[0].set_yticks([1,2,3])
axs[1].set_yticks([-2,-1,-0])

axs[2].set_ylim([-1.75,1.75])
axs[3].set_ylim([-1.75,1.75])
axs[2].set_yticks([-1,0,1])
axs[3].set_yticks([-1,0,1])

if a_1==0.5**0.5 or lim:
    axs[0].set_ylim([-1,2])
    axs[1].set_ylim([-1,2])
    axs[2].set_ylim([-3,9])
    axs[3].set_ylim([-9,3])
    for ax in axs:
        ax.set_yticks(ticks=ax.get_yticks()[1:-1])
# axs[1].tick_params(axis="y", left=False, labelleft=False, right=True, labelright=True)
# axs[3].tick_params(axis="y", left=False, labelleft=False, right=True, labelright=True)
axs[0].errorbar(chi,Re_1_1, Re_1_1_err, fmt="k.", capsize=3)
axs[1].errorbar(chi,Re_2_1, Re_2_1_err, fmt="k.", capsize=3)
axs[0].errorbar(chi_plt, w1(chi_plt, a_21).real, color=colors[3], alpha=0.8)
axs[1].errorbar(chi_plt, w2(chi_plt, a_21).real, color=colors[3], alpha=0.8)

plt.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Images/Results"+folder_name[5:]+".pdf", format="pdf",bbox_inches="tight")

plt.show()