# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:01:28 2023

@author: S18
"""
"""
dat file names:
"""
#plus seems to be minus
#Pi2_1_sigma_z has more points

import os
import numpy as np
import shutil
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as fit

def fit_cos(x, A, B, C, D):
    return A*(1+B*np.cos(C*x-D))/2

def fit_cos_sigma(x, A, B, C, D):
    return A+B*np.cos(C*x-D)

def error(p, m):
    p_err=p**0.5
    m_err=m**0.5
    df_dp =  2*m / (p + m)**2
    df_dm = -2*p / (p + m)**2
    f_err = np.sqrt((df_dp * p_err)**2 + (df_dm * m_err)**2)
    return f_err
plt.grid()
bad_apples=[]

data_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Kazu's experiment/data_Isma/data_Isma/"
sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Kazu's experiment/Sorted data"

# rawdata=sorted_fold_path+"/Rawdata" 
# if not os.path.exists(rawdata):
#     os.makedirs(rawdata)

cleandata=sorted_fold_path+"/Data"
if not os.path.exists(cleandata):
    os.makedirs(cleandata)

cleandata_pi2_mix=cleandata+"/Pi_2/Mixed 0p75"
if not os.path.exists(cleandata_pi2_mix):
    os.makedirs(cleandata_pi2_mix)

# rawdata_pi2_mix=rawdata+"/Pi_2/Mixed 0p75"
# if not os.path.exists(rawdata_pi2_mix):
#     os.makedirs(rawdata_pi2_mix)   

cleandata_pi2_pure=cleandata+"/Pi_2/Pure"
if not os.path.exists(cleandata_pi2_pure):
    os.makedirs(cleandata_pi2_pure)

# rawdata_pi2_pure=rawdata+"/Pi_2/Pure"
# if not os.path.exists(rawdata_pi2_pure):
#     os.makedirs(rawdata_pi2_pure)

cleandata_pi4_mix=cleandata+"/Pi_4/Mixed 0p75"
if not os.path.exists(cleandata_pi4_mix):
    os.makedirs(cleandata_pi4_mix)

# rawdata_pi4_mix=rawdata+"/Pi_4/Mixed 0p75"
# if not os.path.exists(rawdata_pi4_mix):
#     os.makedirs(rawdata_pi4_mix)   

cleandata_pi4_pure=cleandata+"/Pi_4/Pure"
if not os.path.exists(cleandata_pi4_pure):
    os.makedirs(cleandata_pi4_pure)

# rawdata_pi4_pure=rawdata+"/Pi_4/Pure"
# if not os.path.exists(rawdata_pi2_pure):
#     os.makedirs(rawdata_pi2_pure)  

for root, dirs, files in os.walk(data_fold_path):
    # files=np.sort(files)
    # print(files)
    for name in files:
        dat_file_path=os.path.join(root, name)
        if ("1mix_1pi4_Iz" in name):
            dat_file = np.genfromtxt(dat_file_path, skip_header=1, delimiter="")
        else:
            dat_file = np.genfromtxt(dat_file_path, skip_header=1, delimiter=",")
        dat_file=(dat_file[np.argsort(dat_file[:,0])])[:17]
        #if ("Zplus" in name) or ("Zminus" in name) or ("Xplus" in name) or ("Xminus" in name) or ("Yplus" in name) or ("Yminus" in name):
        if ("1pi2" in name): 
            if (name[:-4] in bad_apples):
                print('bad "'+name[:-4]+'", ')
            # else:
            #     print('"'+name+'", ')           
            if ("075mix" in name):
                # print('"'+name+'", ')
                if ("Ix_minus" in name):
                    Pi2_075_Ix_plus = dat_file
                if ("Ix_plus" in name):
                    Pi2_075_Ix_minus = dat_file
                if ("Iy_plus" in name):
                    Pi2_075_Iy_plus = dat_file
                if ("Iy_minus" in name):
                    Pi2_075_Iy_minus = dat_file
                if ("Iz_plus" in name):
                    Pi2_075_Iz_plus = dat_file
                if ("Iz_minus" in name):
                    Pi2_075_Iz_minus = dat_file
            if ("1mix" in name):
                # print('"'+name+'", ')
                if ("Ix_minus" in name):
                    Pi2_1_Ix_plus = dat_file
                if ("Ix_plus" in name):
                    Pi2_1_Ix_minus = dat_file
                if ("Iy_plus" in name):
                    Pi2_1_Iy_plus = dat_file
                if ("Iy_minus" in name):
                    Pi2_1_Iy_minus = dat_file
                if ("Iz_plus" in name):
                    Pi2_1_Iz_plus = dat_file
                if ("Iz_minus" in name):
                    Pi2_1_Iz_minus = dat_file
        if ("1pi4" in name): 
            # print('"'+name+'", ')           
            if ("075mix" in name):
                # print('"'+name+'", ')
                if ("Ix_minus" in name):
                    # print(name)
                    # print(dat_file)
                    Pi4_075_Ix_plus = dat_file
                if ("Ix_plus" in name):
                    Pi4_075_Ix_minus = dat_file
                if ("Iy_plus" in name):
                    Pi4_075_Iy_plus = dat_file
                if ("Iy_minus" in name):
                    Pi4_075_Iy_minus = dat_file
                if ("Iz_plus" in name):
                    Pi4_075_Iz_plus = dat_file
                if ("Iz_minus" in name):
                    Pi4_075_Iz_minus = dat_file
            if ("1mix" in name):
                # print('"'+name+'", ')
                if ("Ix_minus" in name):
                    Pi4_1_Ix_plus = dat_file
                if ("Ix_plus" in name):
                    Pi4_1_Ix_minus = dat_file
                if ("Iy_plus" in name):
                    Pi4_1_Iy_plus = dat_file
                if ("Iy_minus" in name):
                    Pi4_1_Iy_minus = dat_file
                if ("Iz_plus" in name):
                    Pi4_1_Iz_plus = dat_file
                if ("Iz_minus" in name):
                    Pi4_1_Iz_minus = dat_file            
                    
x=Pi2_1_Ix_plus[:,0]/10000
y=Pi2_1_Ix_plus[:,1]
P0=[(np.amax(y)+np.amin(y))/2,(np.amax(y)-np.amin(y))/2/(np.amax(y)+np.amin(y)), 0.012, 0]
B0=([1,0,0.01,-np.pi],[np.amax(y)+10000,1,1, 2*np.pi])
p,cov=fit(fit_cos, x, y,  p0=P0,  bounds=B0)
err=np.diag(cov)**0.5
print("Contrast=", p[1],"+-",err[1])
phi=x*p[-2]-p[-1]
phi_plt=np.linspace(phi[0], phi[-1], 500)
x_plt=np.linspace(x[0], x[-1], 500)
# plt.plot(phi,y,"o")
# plt.plot(phi_plt,fit_cos(x_plt,*p),"-")

# plt.plot(Pi2_075_Ix_plus[:,0],Pi2_075_Ix_plus[:,1], "-")
# plt.plot(Pi2_075_Ix_plus[:,0],Pi2_075_Ix_minus[:,1], "-")
# plt.plot(Pi2_075_Iy_plus[:,0],Pi2_075_Iy_plus[:,1], "-")
# plt.plot(Pi2_075_Iy_plus[:,0],Pi2_075_Iy_minus[:,1], "-")
# plt.plot(Pi2_075_Iz_plus[:,0],Pi2_075_Iz_plus[:,1], "-")
# plt.plot(Pi2_075_Iz_plus[:,0],Pi2_075_Iz_minus[:,1], "-")
# plt.plot(Pi2_1_Ix_plus[:,0],Pi2_1_Ix_plus[:,1], "-")
# plt.plot(Pi2_1_Ix_plus[:,0],Pi2_1_Ix_minus[:,1], "-")
# plt.plot(Pi2_1_Iy_plus[:,0],Pi2_1_Iy_plus[:,1], "-")
# plt.plot(Pi2_1_Iy_plus[:,0],Pi2_1_Iy_minus[:,1], "-")
# plt.plot(Pi2_1_Iz_plus[:,0],Pi2_1_Iz_plus[:,1], "-")
# plt.plot(Pi2_1_Iz_plus[:,0],Pi2_1_Iz_minus[:,1], "-")

# plt.plot(Pi4_075_Ix_plus[:,0],Pi4_075_Ix_plus[:,1], "-")
# plt.plot(Pi4_075_Ix_plus[:,0],Pi4_075_Ix_minus[:,1], "-")
# plt.plot(Pi4_075_Iy_plus[:,0],Pi4_075_Iy_plus[:,1], "-")
# plt.plot(Pi4_075_Iy_plus[:,0],Pi4_075_Iy_minus[:,1], "-")
# plt.plot(Pi4_075_Iz_plus[:,0],Pi4_075_Iz_plus[:,1], "-")
# plt.plot(Pi4_075_Iz_plus[:,0],Pi4_075_Iz_minus[:,1], "-")
# plt.plot(Pi4_1_Ix_plus[:,0],Pi4_1_Ix_plus[:,1], "-")
# plt.plot(Pi4_1_Ix_plus[:,0],Pi4_1_Ix_minus[:,1], "-")
# plt.plot(Pi4_1_Iy_plus[:,0],Pi4_1_Iy_plus[:,1], "-")
# plt.plot(Pi4_1_Iy_plus[:,0],Pi4_1_Iy_minus[:,1], "-")
# plt.plot(Pi4_1_Iz_plus[:,0],Pi4_1_Iz_plus[:,1], "-")
# plt.plot(Pi4_1_Iz_plus[:,0],Pi4_1_Iz_minus[:,1], "-")

Pi2_075_sigma_x=(Pi2_075_Ix_plus[:,1]-Pi2_075_Ix_minus[:,1])/(Pi2_075_Ix_plus[:,1]+Pi2_075_Ix_minus[:,1])
Pi2_075_sigma_y=(Pi2_075_Iy_plus[:,1]-Pi2_075_Iy_minus[:,1])/(Pi2_075_Iy_plus[:,1]+Pi2_075_Iy_minus[:,1])
Pi2_075_sigma_z=(Pi2_075_Iz_plus[:,1]-Pi2_075_Iz_minus[:,1])/(Pi2_075_Iz_plus[:,1]+Pi2_075_Iz_minus[:,1])
Pi2_1_sigma_x=(Pi2_1_Ix_plus[:,1]-Pi2_1_Ix_minus[:,1])/(Pi2_1_Ix_plus[:,1]+Pi2_1_Ix_minus[:,1])
Pi2_1_sigma_y=(Pi2_1_Iy_plus[:,1]-Pi2_1_Iy_minus[:,1])/(Pi2_1_Iy_plus[:,1]+Pi2_1_Iy_minus[:,1])
Pi2_1_sigma_z=(Pi2_1_Iz_plus[:,1]-Pi2_1_Iz_minus[:,1])/(Pi2_1_Iz_plus[:,1]+Pi2_1_Iz_minus[:,1])

Pi2_075_sigma_x_err=error(Pi2_075_Ix_plus[:,1], Pi2_075_Ix_minus[:,1])
Pi2_075_sigma_y_err=error(Pi2_075_Iy_plus[:,1], Pi2_075_Iy_minus[:,1])
Pi2_075_sigma_z_err=error(Pi2_075_Iz_plus[:,1], Pi2_075_Iz_minus[:,1])
Pi2_1_sigma_x_err=error(Pi2_1_Ix_plus[:,1], Pi2_1_Ix_minus[:,1])
Pi2_1_sigma_y_err=error(Pi2_1_Iy_plus[:,1], Pi2_1_Iy_minus[:,1])
Pi2_1_sigma_z_err=error(Pi2_1_Iz_plus[:,1], Pi2_1_Iz_minus[:,1])

print(len(Pi2_1_sigma_z), len(phi))
                                                                                  
plt.errorbar(phi, Pi2_075_sigma_x, Pi2_075_sigma_x_err, fmt=".-", capsize=3)
plt.errorbar(phi, Pi2_075_sigma_y,  Pi2_075_sigma_y_err, fmt=".-", capsize=3)
plt.errorbar(phi, Pi2_075_sigma_z, Pi2_075_sigma_z_err, fmt=".-", capsize=3)
plt.errorbar(phi, Pi2_1_sigma_x, Pi2_1_sigma_x_err, fmt=".-", capsize=3)
plt.errorbar(phi, Pi2_1_sigma_y, Pi2_1_sigma_y_err, fmt=".-", capsize=3)
plt.errorbar(phi, Pi2_1_sigma_z, Pi2_1_sigma_z_err, fmt=".-", capsize=3)

Pi4_075_sigma_x=(Pi4_075_Ix_plus[:,1]-Pi4_075_Ix_minus[:,1])/(Pi4_075_Ix_plus[:,1]+Pi4_075_Ix_minus[:,1])
Pi4_075_sigma_y=(Pi4_075_Iy_plus[:,1]-Pi4_075_Iy_minus[:,1])/(Pi4_075_Iy_plus[:,1]+Pi4_075_Iy_minus[:,1])
Pi4_075_sigma_z=(Pi4_075_Iz_plus[:,1]-Pi4_075_Iz_minus[:,1])/(Pi4_075_Iz_plus[:,1]+Pi4_075_Iz_minus[:,1])
Pi4_1_sigma_x=(Pi4_1_Ix_plus[:,1]-Pi4_1_Ix_minus[:,1])/(Pi4_1_Ix_plus[:,1]+Pi4_1_Ix_minus[:,1])
Pi4_1_sigma_y=(Pi4_1_Iy_plus[:,1]-Pi4_1_Iy_minus[:,1])/(Pi4_1_Iy_plus[:,1]+Pi4_1_Iy_minus[:,1])
Pi4_1_sigma_z=(Pi4_1_Iz_plus[:,1]-Pi4_1_Iz_minus[:,1])/(Pi4_1_Iz_plus[:,1]+Pi4_1_Iz_minus[:,1])

Pi4_075_sigma_x_err=error(Pi4_075_Ix_plus[:,1], Pi4_075_Ix_minus[:,1])
Pi4_075_sigma_y_err=error(Pi4_075_Iy_plus[:,1], Pi4_075_Iy_minus[:,1])
Pi4_075_sigma_z_err=error(Pi4_075_Iz_plus[:,1], Pi4_075_Iz_minus[:,1])
Pi4_1_sigma_x_err=error(Pi4_1_Ix_plus[:,1], Pi4_1_Ix_minus[:,1])
Pi4_1_sigma_y_err=error(Pi4_1_Iy_plus[:,1], Pi4_1_Iy_minus[:,1])
Pi4_1_sigma_z_err=error(Pi4_1_Iz_plus[:,1], Pi4_1_Iz_minus[:,1])

# plt.errorbar(phi, Pi4_075_sigma_x, Pi4_075_sigma_x_err, fmt=".-", capsize=3)
# plt.errorbar(phi, Pi4_075_sigma_y,  Pi4_075_sigma_y_err, fmt=".-", capsize=3)
# plt.errorbar(phi, Pi4_075_sigma_z, Pi4_075_sigma_z_err, fmt=".-", capsize=3)
# plt.errorbar(phi, Pi4_1_sigma_x, Pi4_1_sigma_x_err, fmt=".-", capsize=3)
# plt.errorbar(phi, Pi4_1_sigma_y, Pi4_1_sigma_y_err, fmt=".-", capsize=3)
# plt.errorbar(phi, Pi4_1_sigma_z, Pi4_1_sigma_z_err, fmt=".-", capsize=3)

x_s=Pi2_075_Ix_plus[:,0]/10000
y_s=Pi2_1_sigma_x
P0_s=[1,1, p[-2], 0]
B0_s=([-1,0,0.001,-2*np.pi],[1,1,1, 2*np.pi])
p_s,cov_s=fit(fit_cos_sigma, x_s, y_s,  p0=P0_s,  bounds=B0_s)
err_s=np.diag(cov_s)**0.5
# print(p_s, err_s)

print("Contrast=", p_s[1],"+-",err_s[1])
phi_s=x_s*p_s[-2]-p_s[-1]
phi_plt_s=np.linspace(phi_s[0], phi_s[-1], 500)
x_plt_s=np.linspace(x_s[0], x_s[-1], 500)
# plt.plot(phi_s,y_s,"o")
# plt.plot(phi_plt_s,fit_cos_sigma(x_plt_s,*p_s),"-")

Pi2_075_x = np.column_stack((Pi2_075_Ix_plus[:,0], phi, Pi2_075_Ix_minus[:,1], Pi2_075_sigma_x, Pi2_075_sigma_x_err))
Pi2_075_y = np.column_stack((Pi2_075_Iy_plus[:,0], phi, Pi2_075_Iy_minus[:,1], Pi2_075_sigma_y, Pi2_075_sigma_y_err))
Pi2_075_z = np.column_stack((Pi2_075_Iz_plus[:,0], phi, Pi2_075_Iz_minus[:,1], Pi2_075_sigma_z, Pi2_075_sigma_z_err))
Pi2_1_x = np.column_stack((Pi2_1_Ix_plus[:,0], phi, Pi2_1_Ix_minus[:,1], Pi2_1_sigma_x, Pi2_1_sigma_x_err))
Pi2_1_y = np.column_stack((Pi2_1_Iy_plus[:,0], phi, Pi2_1_Iy_minus[:,1], Pi2_1_sigma_y, Pi2_1_sigma_y_err))
Pi2_1_z = np.column_stack((Pi2_1_Iz_plus[:,0], phi, Pi2_1_Iz_minus[:,1], Pi2_1_sigma_z, Pi2_1_sigma_z_err))
Pi4_075_x = np.column_stack((Pi4_075_Ix_plus[:,0], phi, Pi4_075_Ix_minus[:,1], Pi4_075_sigma_x, Pi4_075_sigma_x_err))
Pi4_075_y = np.column_stack((Pi4_075_Iy_plus[:,0], phi, Pi4_075_Iy_minus[:,1], Pi4_075_sigma_y, Pi4_075_sigma_y_err))
Pi4_075_z = np.column_stack((Pi4_075_Iz_plus[:,0], phi, Pi4_075_Iz_minus[:,1], Pi4_075_sigma_z, Pi4_075_sigma_z_err))
Pi4_1_x = np.column_stack((Pi4_1_Ix_plus[:,0], phi, Pi4_1_Ix_minus[:,1], Pi4_1_sigma_x, Pi4_1_sigma_x_err))
Pi4_1_y = np.column_stack((Pi4_1_Iy_plus[:,0], phi, Pi4_1_Iy_minus[:,1], Pi4_1_sigma_y, Pi4_1_sigma_y_err))
Pi4_1_z = np.column_stack((Pi4_1_Iz_plus[:,0], phi, Pi4_1_Iz_minus[:,1], Pi4_1_sigma_z, Pi4_1_sigma_z_err))

with open(cleandata_pi2_mix+"/"+"Measurement_x.txt", 'w') as f:
        np.savetxt(f, Pi2_075_x, header="Coil_pos phi[rad]  I_x_plus I_x_minus sigma_x sigma_x_err")
with open(cleandata_pi2_mix+"/"+"Measurement_y.txt", 'w') as f:
        np.savetxt(f, Pi2_075_y, header="Coil_pos phi[rad]  I_y_plus I_y_minus sigma_y sigma_y_err")
with open(cleandata_pi2_mix+"/"+"Measurement_z.txt", 'w') as f:
        np.savetxt(f, Pi2_075_z, header="Coil_pos phi[rad]  I_z_plus I_z_minus sigma_z sigma_z_err")    
with open(cleandata_pi2_pure+"/"+"Measurement_x.txt", 'w') as f:
        np.savetxt(f, Pi2_1_x, header="Coil_pos phi[rad]  I_x_plus I_x_minus sigma_x sigma_x_err")
with open(cleandata_pi2_pure+"/"+"Measurement_y.txt", 'w') as f:
        np.savetxt(f, Pi2_1_y, header="Coil_pos phi[rad]  I_y_plus I_y_minus sigma_y sigma_y_err")
with open(cleandata_pi2_pure+"/"+"Measurement_z.txt", 'w') as f:
        np.savetxt(f, Pi2_1_z, header="Coil_pos phi[rad]  I_z_plus I_z_minus sigma_z sigma_z_err") 

with open(cleandata_pi4_mix+"/"+"Measurement_x.txt", 'w') as f:
        np.savetxt(f, Pi4_075_x, header="Coil_pos phi[rad]  I_x_plus I_x_minus sigma_x sigma_x_err")
with open(cleandata_pi4_mix+"/"+"Measurement_y.txt", 'w') as f:
        np.savetxt(f, Pi4_075_y, header="Coil_pos phi[rad]  I_y_plus I_y_minus sigma_y sigma_y_err")
with open(cleandata_pi4_mix+"/"+"Measurement_z.txt", 'w') as f:
        np.savetxt(f, Pi4_075_z, header="Coil_pos phi[rad]  I_z_plus I_z_minus sigma_z sigma_z_err")    
with open(cleandata_pi4_pure+"/"+"Measurement_x.txt", 'w') as f:
        np.savetxt(f, Pi4_1_x, header="Coil_pos phi[rad]  I_x_plus I_x_minus sigma_x sigma_x_err")
with open(cleandata_pi4_pure+"/"+"Measurement_y.txt", 'w') as f:
        np.savetxt(f, Pi4_1_y, header="Coil_pos phi[rad]  I_y_plus I_y_minus sigma_y sigma_y_err")
with open(cleandata_pi4_pure+"/"+"Measurement_z.txt", 'w') as f:
        np.savetxt(f, Pi4_1_z, header="Coil_pos phi[rad]  I_z_plus I_z_minus sigma_z sigma_z_err") 
