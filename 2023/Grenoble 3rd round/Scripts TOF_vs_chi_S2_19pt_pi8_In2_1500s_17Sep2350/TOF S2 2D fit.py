#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 10:29:06 2023

@author: aaa
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 15:03:44 2023

@author: aaa
"""


import warnings
from scipy.optimize import curve_fit as fit
from PIL import Image as im
import os
import numpy as np
import shutil
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib.gridspec import GridSpec
from scipy.stats import chisquare
plt.rcParams.update({'figure.max_open_warning': 0})
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

a_1 = 2/5**0.5
a_2 = 1/5**0.5
f1 = 10
xi_0=0.1
alpha=np.pi/8


def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def I_px_co(beta, chi, C, alpha):
    I_co=(1+2*a_1*a_2*np.cos(chi-alpha*np.sin(beta)))/2
    return C*I_co

def I_px_in(beta, chi, eta):
    I_in=np.ones((len(chi),len(beta)))/2
    return eta*I_in




inf_file_name="TOF_vs_chi_S2_19pt_pi8_In2_1500s_17Sep2350"
sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/exp_3-16-14/Sorted data/TOF S2/"+inf_file_name
cleandata=sorted_fold_path+"/Cleantxt"

i=0
for root, dirs, files in os.walk(cleandata, topdown=False):
    files=np.sort(files)
    # print(files)
    for name in files:
        if i==0:
            tot_data=np.loadtxt(os.path.join(root, name))[1:-1,:]
            time=tot_data[:,1]
            f_2=tot_data[0,-3]*1e-3
            print(f_2)
            i=1
        else:
            data=np.loadtxt(os.path.join(root, name))[1:-1,:]
            tot_data = np.vstack((tot_data, data))
ps_pos=tot_data[::len(time),-1]
matrix=np.zeros((len(ps_pos),len(time)))
matrix_err=np.zeros((len(ps_pos),len(time)))
for i in range(len(ps_pos)):
    if tot_data[:,4].all()==0:
        matrix[i]=tot_data[:,3][tot_data[:,-1]==ps_pos[i]]
    else:
        matrix[i]=tot_data[:,4][tot_data[:,-1]==ps_pos[i]]
    matrix_err[i]=matrix[i]**0.5
    
ps_data=np.sum(matrix, axis=1)
P0=[(np.amax(ps_data)+np.amin(ps_data))/2, (np.amax(ps_data)-np.amin(ps_data))/2, 3, -3]
B0=([1000,0,0.01,-10],[np.amax(ps_data)+1000,np.amax(ps_data)+1000,5, 10])
p,cov=fit(fit_cos, ps_pos, ps_data, p0=P0,  bounds=B0)
chi_0 = p[-1]
w_ps=p[-2]
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ps_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
ax.errorbar(ps_pos,ps_data, yerr=ps_data**0.5,fmt="ko",capsize=5, ms=3)
ax.plot(ps_plt,fit_cos(ps_plt, *p), "b")
ax.vlines(p[-1]/p[-2],fit_cos(p[-1]/p[-2]+np.pi,*p),fit_cos(p[-1]/p[-2],*p), color="k")
chi=ps_pos*w_ps-chi_0
chi_plt=np.linspace(chi[0], chi[-1], 100)
C=0.6590116765538198
C_err=0.022491135210979854
eta = 1-C
beta = 2*np.pi*1e-3*f1*time+xi_0


def fit_I_px(x, xi_0, A, alpha):
    beta = 2*np.pi*1e-3*f1*time+xi_0
    chi = w_ps*ps_pos-chi_0
    I_px_inc=I_px_in(beta, chi, eta)
    beta, chi = np.meshgrid(beta, chi)
    fit_I_px = A*(I_px_co(beta, chi, C, alpha) + I_px_inc)
    # print(fit_I_px)
    return fit_I_px.ravel()

P0 = (xi_0, 1, alpha)
B0 = ([-10, 0, -10], [10 ,10, 10])
p, cov = fit(fit_I_px, range(len(matrix.ravel())), matrix.ravel()/np.amax(matrix.ravel()), bounds=B0)
print(p, np.diag(cov)**0.5)
print(chi_0)
xi_0 = p[0]
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
ax.errorbar(np.arange(len(matrix.ravel())),matrix.ravel(), yerr=matrix_err.ravel(), fmt="r.", alpha=0.5, ms=0.5, label="data")
# ax.plot(matrix.ravel(), "r--")
ax.plot(fit_I_px(0, *p)*np.amax(matrix.ravel()), "b", lw=2, label="Fit")
ax.set_xlim([500,1000])
f_obs=matrix.ravel()
f_exp=fit_I_px(0,*p)*np.amax(matrix.ravel())
# import glob
# from PIL import Image
# def make_gif(frame_folder):
#     frames = [Image.open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/Animation/chi"+str(j)+".png") for j in range(len(ps_pos))]
#     frame_one = frames[0]
#     frame_one.save("/home/aaa/Desktop/fit.gif", format="GIF", append_images=frames,
#                save_all=True, duration=200, loop=0)
    
# if __name__ == "__main__":
#     make_gif("Phase")

# f_obs/=np.sum(f_obs)
# f_exp/=np.sum(f_exp)

# print((np.sum(f_obs)-np.sum(f_exp))/np.sum(f_obs))
# print(chisquare(f_obs=f_obs, f_exp=f_exp, ddof=7))

def I_px(x, xi_0, A, alpha):
    beta = 2*np.pi*1e-3*f1*time+xi_0
    chi = w_ps*ps_pos-chi_0
    I_px_inc=I_px_in(beta, chi, eta)
    beta, chi = np.meshgrid(beta, chi)
    fit_I_px = A*(I_px_co(beta, chi, C, alpha) + I_px_inc)
    # print(fit_I_px)
    return fit_I_px

def I_px_corr_co(x, xi_0, A, alpha):
    beta = 2*np.pi*1e-3*f1*time+xi_0
    chi = w_ps*ps_pos-chi_0
    beta, chi = np.meshgrid(beta, chi)
    fit_I_px = I_px_co(beta, chi, C, alpha)
    return fit_I_px

def I_px_corr_in(x, xi_0, A, alpha):
    beta = 2*np.pi*1e-3*f1*time+xi_0
    chi = w_ps*ps_pos-chi_0
    I_px_inc=I_px_in(beta, chi, eta)
    beta, chi = np.meshgrid(beta, chi)
    fit_I_px = I_px_inc
    # print(fit_I_px)
    return fit_I_px
data_plt=matrix[2,:]
beta = time#2*np.pi*1e-3*f1*time+xi_0

# fig = plt.figure(figsize=(7, 5))
# ax = plt.axes(projection='3d')
# beta, chi = np.meshgrid(beta, chi)
# Z = matrix
# Z1 = I_px(0, *p)*np.amax(matrix)
# Z2 = I_px_corr_co(0, *p)*np.amax(matrix)
# Z3 = Z-I_px_corr_in(0, *p)*np.amax(matrix)
# # Z=I_px_co(beta, chi, C, alpha, beta)+I_px_in(beta, chi, eta, alpha, beta)
# ax.contour3D(beta, chi, Z, 20, cmap='binary')
# # ax.contour3D(beta, chi, Z1, 40, cmap='plasma')  # cmap='Blues')
# ax.set_xlabel('$\mu s$')
# ax.set_ylabel('$\chi$')
# ax.set_zlabel('z')
# ax.view_init(30, 45)
# plt.show()

# gs=GridSpec(3,1, figure=fig)
# fig = plt.figure(figsize=(10, 10))
# axs=[fig.add_subplot(gs[0,0]),fig.add_subplot(gs[1:,0],projection='3d'),fig.add_subplot(gs[:,:]) ]
# axs[-1].tick_params(
#     axis='both',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     bottom=False,      # ticks along the bottom edge are off
#     top=False,         # ticks along the top edge are off
#     left=False,
#     right=False,
#     labelleft=False,
#     labelbottom=False,
#     labelright=False) # labels along the bottom edge are off
# axs[-1].spines["top"].set_visible(False)
# axs[-1].spines["left"].set_visible(False)
# axs[-1].spines["bottom"].set_visible(False)
# axs[-1].spines["right"].set_visible(False)
# axs[-1].patch.set_alpha(0)
# # axs[1] = plt.axes(projection='3d')
# Z = matrix
# Z1 = I_px(0, *p)*np.amax(matrix)
# Z2 = I_px_corr_co(0, *p)*np.amax(matrix)
# Z3 = Z-I_px_corr_in(0, *p)*np.amax(matrix)
# # Z=I_px_co(beta, chi, C, alpha, beta)+I_px_in(beta, chi, eta, alpha, beta)
# axs[1].contour3D(beta, chi, Z, 20, cmap='binary')
# # axs[1].contour3D(beta, chi, Z1, 40, cmap='plasma')  # cmap='Blues')
# axs[1].plot3D( time,chi[2]+time*0, data_plt, 'r', lw=5,label="Interferogram (coil pos=15)")
# # axs[1].plot3D( time,chi[2]+time*0, data_plt, 'r', lw=5,label="Interferogram (coil pos=15)")
# axs[1].set_xlabel("$\mu s$")
# axs[1].set_ylabel('$\chi$')
# axs[1].view_init(30, 45)

# axs[0].set_frame_on(True)
# axs[0].errorbar(time, matrix[2], matrix_err[2], fmt="ro")
# axs[0].set_xlabel("$\mu s$")
# axs[-1].arrow(0.2, 0.37, 0,0.35, lw=3, color="r", head_width=0.02)
# plt.show()
def I_px_anim(time, chi, xi_0, A, alpha):
    beta = 2*np.pi*1e-3*f1*time+xi_0
    fit_I_px = A*(I_px_co(beta, chi, C, alpha) + eta/2)
    # print(fit_I_px)
    return fit_I_px


chi=ps_pos*w_ps-chi_0

# for i in range(len(ps_pos)):
#     fig = plt.figure(figsize=(10, 3), dpi=200)
#     gs=GridSpec(1,4, figure=fig)
#     axs = [fig.add_subplot(gs[0,:-1]), fig.add_subplot(gs[0,-1],projection='polar')]
#     axs[-1].tick_params(axis="y", labelbottom=False, bottom = False,labelleft=False, left = False)
#     axs[-1].tick_params(axis="x", pad=-4)
#     axs[-1].set_xticks([0,np.pi/2,np.pi,np.pi*3/2])
#     axs[-1].set_xticklabels(['0','$\pi/2$','$\pi$','$3\pi/2$'])
#     axs[-1].grid(False)
#     axs[-1].set_ylim([0,1])
#     axs[-1].set_title("$\chi$", y=1.1, bbox=dict(facecolor='none', edgecolor='k'))
#     axs[0].errorbar(time, matrix[i], yerr= matrix_err[i], fmt="k.")
#     axs[0].plot(time, I_px_anim(time, chi[i], *p)*np.amax(matrix), "b")    
#     axs[0].set_title("$\chi=$"+str("%.2f"%(chi[i]/np.pi,))+ " $\pi$")
#     axs[0].set_ylim([100, 800])
#     axs[-1].plot([0,chi[i]],[0,1], "-k.")
#     plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/Animation/chi"+str(i)+".png", format='png',bbox_inches='tight')
#     plt.close(fig)



# import glob
# from PIL import Image
# def make_gif(frame_folder):
#     frames = [Image.open("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/Animation/chi"+str(j)+".png") for j in range(len(ps_pos))]
#     frame_one = frames[0]
#     frame_one.save("/home/aaa/Desktop/fit.gif", format="GIF", append_images=frames,
#                save_all=True, duration=200, loop=0)
    
# if __name__ == "__main__":
#     make_gif("Phase")
