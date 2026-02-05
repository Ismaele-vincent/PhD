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
from matplotlib import font_manager
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
a_1=1/2**0.5
a_2=1/2**0.5
sgn=1
font_path = "/home/aaa/root/fonts/cmunrm.ttf"
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [prop.get_name(), "DejaVu Sans"]  # <- DejaVu als Fallback
plt.rcParams["font.size"] = 12
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["figure.dpi"] = 150
# plt.rcParams["legend.markerscale"] = 1
plt.rcParams["legend.fontsize"] = 11
plt.rcParams["axes.unicode_minus"] = False  # <- richtige Variante!

colors=["k","#f10d0c","#00a933","#5983b0"]
# labels=["$\delta=\\frac{\pi}{2}$", "$\delta=\pi$", "$\delta=-\\frac{\pi}{2}$", "$\delta=0$"]
labels=["$I_+(\\frac{\pi}{2})$", "$I_-(0)$", "$I_-(\\frac{\pi}{2})$", "$I_+(0)$"]
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
# Indium 0.8mm path2 (Bad, Interferogram going down)
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
# Indium 0.8mm path2  (Bad, Interferogram and/or phase not good. Gets progressively better, but still not good.)
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
folder_name="Symm In 1p5 path2"
P1=57079/15
P2=19747/15
a_1= 0.862
a_1_err=0.005
a_2= 0.507
a_2_err=0.008
a_21=a_2/a_1
lim=0
inf_file_name="ifgPS1_35pt_In15_13Apr2126" #best
# inf_file_name="ifgPS1_35pt_In15_14Apr0146" #bad
# inf_file_name="ifgPS1_35pt_In15_14Apr0322" #very good
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
# # folder_name="Symm In 1p0 path2"
# P1=57079/15
# P2=27549/15
# a_1= 0.821
# a_1_err=0.004
# a_2= 0.570
# a_2_err=0.006
# a_21=a_2/a_1
# print(a_21)
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
fig = plt.figure(figsize=(2.5,5), dpi=250)
fig_1 = plt.figure(figsize=(2.5,5), dpi=250)
gs = fig.add_gridspec(3,1, hspace=0.0, wspace=0.4)
gs_1 = fig_1.add_gridspec(3,1, hspace=0.0, wspace=0.4)
axs = [fig_1.add_subplot(gs_1[0, 0]),fig.add_subplot(gs[0, 0]),fig_1.add_subplot(gs_1[1, 0]),fig.add_subplot(gs[1, 0]),fig.add_subplot(gs[2, 0]), fig_1.add_subplot(gs[2, 0]),]
# fig = plt.figure(figsize=(5,6), dpi=150)
# gs = fig.add_gridspec(2,2, hspace=0.0, wspace=0)
# axs = [fig.add_subplot(gs[0, 0]),fig.add_subplot(gs[0, 1]),fig.add_subplot(gs[1, 0]),fig.add_subplot(gs[1, 1])]
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    data_ifg_matrix=np.zeros((4,points))
    # print(files[::-1])
    for name in (files[::-1]):
        # print(name)
        tot_data=np.loadtxt(os.path.join(root, name))
        time=tot_data[0,1]
        # print(time)
        data_ifg=tot_data[:,2]
        data_ifg_matrix[3-i]=data_ifg
        data_ifg_err=data_ifg**0.5
        ps_pos=tot_data[:,0]
        P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, -0.6+chi_0[i]]
        B0=([np.amin(data_ifg),0,0.01,-3.5],[np.amax(data_ifg)*2,np.amax(data_ifg)*2,5, 2*np.pi])
        p,cov=fit(fit_cos, ps_pos, data_ifg, sigma=data_ifg_err, p0=P0,  bounds=B0)
        if i==0:
            chi=ps_pos*p[2]-p[3]-np.pi/2
            chi_plt=np.linspace(chi[13],chi[-1],200)
        # P0_unb=[100000, 3, -0.5, 0.7]
        # B0_unb=([0,1,-10, 0],[1e10,4,10,1])
        # p_unb,cov_unb=fit(fit_cos_unb, ps_pos, data_ifg, p0=P0_unb,  bounds=B0_unb)
        err=np.diag(cov)**0.5
        A_avg+=p[0]/4
        C_avg+=p[1]/p[0]/4
        C_err+=p[1]**2/p[0]**4*err[0]**2+err[1]**2/p[0]**2
        A_err=err[0]**2
        x_plt = np.linspace(ps_pos[13], ps_pos[-1],200)
        # axs[(i+2)%4].errorbar(chi,data_ifg/time,yerr=data_ifg_err/time,fmt=".", color=colors[0],capsize=3, ms=3, label="Data")
        axs[(i+2)%4].errorbar(chi_plt,fit_cos(x_plt, *p)/time, fmt="--", color=colors[3], label="Theory")
        # axs[(i+2)%4].text(1.05,0.5,labels[i], rotation=-90, ha="center", va="center", transform=axs[i].transAxes)
        axs[(i+2)%4].set_ylabel(labels[i]+"\n[counts $\mathrm{s}^{-1}$]")
        axs[(i+2)%4].set_ylim([70,420])
        # print((i+2)%4)
        # print("C=", p[1]/p[0], "+-", ((err[1]/p[0])**2+(err[1]*p[1]/p[0]**2)**2)**0.5)
        # print("C_unb=", p_unb[-1])
        # print(p_unb)
        # print("w_ps=", p[-2], "+-", err[-2])1
        # print("chi_0=", p[-1])
        Dchi[i]=p[3]
        # print(p[3])
        i+=1
        
axs[4].set_xlabel("${\phi}$ [rad]")
axs[5].set_xlabel("${\phi}$ [rad]")
# axs[1].text(-0.13,0,"Interferogram (count/s)",rotation=90, ha="center", va="center", transform=axs[1].transAxes)
for ax in axs[:-2]:
    ax.set_yticks([150,250,350])
    ax.set_facecolor("#fffff2")
# for ax in axs[-2:]:
#     ax.set_facecolor("#fff2ff")

for ax in axs:
    ax.set_xticks([0,np.pi/2,np.pi,3*np.pi/2])
    ax.set_xticklabels(["${0}$","${\\dfrac{\pi}{2}}$","${\pi}$","${\\dfrac{3\pi}{2}}$",])
    ax.grid(True, ls="dotted")  
    
axs[0].tick_params(axis="x", bottom=False, labelbottom=False)
axs[1].tick_params(axis="x", bottom=False, labelbottom=False)
axs[2].tick_params(axis="x", bottom=False, labelbottom=False)
axs[3].tick_params(axis="x", bottom=False, labelbottom=False)

axs[1].errorbar(chi[26],(data_ifg_matrix[0])[26]/time, (data_ifg_matrix[0]**0.5)[26]/time, fmt=".", color=colors[0],capsize=3, label="Data")
# axs[1].vlines(chi[26],0,(data_ifg_matrix[0])[26]/time-12, color=colors[1],  lw=1) #ls=(2, (8, 3)),
axs[3].errorbar(chi[26],(data_ifg_matrix[2])[26]/time, (data_ifg_matrix[2]**0.5)[26]/time, fmt=".", color=colors[0],capsize=3, label="Data")
# axs[3].vlines(chi[26],(data_ifg_matrix[2])[26]/time+12,520, color=colors[1],  lw=1) #ls=(2, (8, 3)),
# axs[3].vlines(chi[26],0,(data_ifg_matrix[2])[26]/time-12, color=colors[1],  lw=1) #ls=(2, (8, 3)),

axs[0].errorbar(chi[26],(data_ifg_matrix[1])[26]/time, (data_ifg_matrix[1]**0.5)[26]/time, fmt=".", color=colors[0],capsize=3, label="Data")
# axs[0].vlines(chi[26],0,(data_ifg_matrix[1])[26]/time-12, color=colors[1],  lw=1) #ls=(2, (8, 3)),
axs[2].errorbar(chi[26],(data_ifg_matrix[3])[26]/time, (data_ifg_matrix[3]**0.5)[26]/time, fmt=".", color=colors[0],capsize=3, label="Data")
# axs[2].vlines(chi[26],(data_ifg_matrix[3])[26]/time+12,520, color=colors[1],  lw=1) #ls=(2, (8, 3)),
print("chi=",chi[26], 4*np.pi/5)

# print(abs(Dchi-Dchi[[1,2,3,0]])/np.pi*2)
C_err=C_err**0.5/4
A_err=A_err**0.5/4
# print("A_avg=",A_avg, "+-",A_err)

C_id=C_avg/(2*a_1*a_2)
C_id_err=(C_err**2+C_avg**2/(a_1**2)*a_1_err**2+C_avg**2/(a_2**2)*a_2_err**2)**0.5/(2*a_1*a_2)
# print("C_avg=",C_avg, "+-",C_err, "C_ideal=", C_id, "+-", C_id_err)

# chi+=np.pi/2
data_ifg_matrix_err=(data_ifg_matrix+((1-C_id)/2)**2*A_err**2+(A_avg/2)**2*C_id_err**2)**0.5
# data_ifg_matrix_err=(data_ifg_matrix/C_id**2+((1/C_id+1)/2)**2*A_err**2+(A_avg/2-data_ifg_matrix)**2*(C_id_err/C_id**2)**2)**0.5
data_ifg_matrix-=A_avg*(1-C_id)
P1_corr=C_id*P1
P1_corr_err=(C_id**2*P1+P1**2*C_id_err**2)**0.5
P2_corr=C_id*P2
P2_corr_err=(C_id**2*P2+P2**2*C_id_err**2)**0.5

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

# axs[0].set_title("$w_{1,+}$", fontsize=13)
# axs[1].set_title("$w_{2,+}$", fontsize=13)
axs[4].set_ylabel("Weak value\n(real part)")
axs[5].set_ylabel("Weak value\n(imaginary part)")
# fig.suptitle(inf_file_name)
colors=["k","#f10d0c","#00a933","#5983b0"]
plt.rcParams["mathtext.fontset"]="cm"
# for ax in axs:
#     ax.set_xticks([-np.pi,0,np.pi])
#     ax.set_xticklabels(["${-\pi}$", "${0}$","${\pi}$"])
#     ax.grid(True, ls="dotted")

axs[0].tick_params(axis="x", bottom=False, labelbottom=False)
axs[1].tick_params(axis="x", bottom=False, labelbottom=False)
# axs[1].tick_params(axis="y", left=False, labelleft=False)
# axs[3].tick_params(axis="y", left=False, labelleft=False)
    
axs[4].set_ylim([0.5,2.5])
axs[4].set_yticks([1,1.5,2])
axs[4].errorbar(chi_plt, w1(chi_plt, a_21).real, fmt="--",color=colors[3], label="Theory")
# axs[4].errorbar(chi,Re_1_1, Re_1_1_err, fmt=".", color="grey", capsize=3, label="Data")
axs[4].errorbar(chi[26],Re_1_1[26], Re_1_1_err[26], fmt="k.", capsize=3, label="Data")
# axs[4].errorbar(chi[26],Re_1_1[26], fmt=".",color=colors[1],  ms=15, mfc="none")
# axs[4].vlines(chi[26],0,3, color=colors[1],  lw=1)

axs[5].set_ylim([-1.2,1.2])
axs[5].set_yticks([-1,-0.5,0,0.5,1])
# axs[5].errorbar(chi,Im_1, Im_1_err, fmt="k.", capsize=3,label="Data")
axs[5].plot(chi_plt, w1(chi_plt, a_21).imag, "--",color=colors[3], label="Theory")
axs[5].errorbar(chi[26], Im_1[26], Im_1_err[26], fmt=".", color=colors[0],capsize=3, label="Data")
# axs[5].errorbar(chi[26], Im_1[26], Im_1_err[26], fmt="k.", capsize=3,label="Data")
# axs[5].vlines(chi[26],-2,2, color=colors[1],  lw=1)

# axs[4].legend(loc=1, ncol=1, handlelength=1)
# axs[5].legend(loc=1, ncol=1, handlelength=1)
# axs[i].set_ylabel("Neutron rate (count / s)")
# axs[i].set_ylim([0,430])

fig.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Images NatCom/Measurement example and wv real.pdf", format="pdf",bbox_inches="tight")
fig_1.savefig("/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/Paper/Images NatCom/Measurement example and wv imag.pdf", format="pdf",bbox_inches="tight")
plt.show()