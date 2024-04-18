# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:37:41 2023

@author: S18
"""
"""
inf_file_names:
    "alpha_01Sep2232", 
    "alpha_02Sep0907", 
    "alpha_02Sep1943", 
    "alpha_03Sep0618", 
    "alpha_ifg_01Sep2302", 
    "alpha_ifg_02Sep0937", 
    "alpha_ifg_02Sep2013", 
    "alpha_ifg_03Sep0648", 

"""


from scipy.optimize import curve_fit as fit
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
mu_N = -9.6623651*1e-27  # J/T
hbar = 6.62607015/(2*np.pi)*1e-34  # J s
v0 = 2060.43  # m/s


def fit_cos(x, A, B, C, D):
    return A+B*np.cos(C*x-D)


def fit_lin(x, A, B):
    return A+B*x


inf_file_names = [
    # "alpha_01Sep2232",
    # "alpha_02Sep0907",
    # "alpha_02Sep1943",
    # "alpha_03Sep0618",
    # "alpha_ifg_01Sep2302",
    "alpha_ifg_02Sep0937",
    "alpha_ifg_temp_04Sep1022",
    # "alpha_ifg_03Sep0648",
]

for inf_file_name in inf_file_names:
    # print(inf_file_name)
    sorted_fold_path = "/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/exp_3-16-14/Sorted data/Alpha/"+inf_file_name
    cleandata = sorted_fold_path+"/Cleantxt"
    if "ifg" not in inf_file_name:
        for root, dirs, files in os.walk(cleandata, topdown=False):
            files = np.sort(files)
            for name in files:
                # print(name)
                tot_data = np.loadtxt(os.path.join(root, name))
                data_alpha = tot_data[:, 2]+tot_data[:, 5]
                data_alpha_err = data_alpha**0.5
                current = tot_data[:, 0]
                P0 = [(np.amax(data_alpha)+np.amin(data_alpha))/2,
                      (np.amax(data_alpha)-np.amin(data_alpha))/2, 0.1, 1.5]
                B0 = ([np.amin(data_alpha), 0, 0.01, -10],
                      [np.amax(data_alpha), np.amax(data_alpha), 1, 10])
                p, cov = fit(fit_cos, current, data_alpha, p0=P0,  bounds=B0)
                # err=np.diag(cov)**0.5
                # print(p[3], err[3])
                x_plt = np.linspace(current[0], current[-1], 100)
                fig = plt.figure(figsize=(8, 6))
                ax = fig.add_subplot(111)
                fig.suptitle(name[:-4])
                ax.errorbar(current*(1-0.25*current), data_alpha,
                            yerr=data_alpha_err, fmt="ko", capsize=5, ms=3)
                # ax.plot(x_plt,fit_cos(x_plt, *p), "b")
                # ax.set_ylim([0,1500])
    else:
        if "temp" in inf_file_name:
            for root, dirs, files in os.walk(cleandata, topdown=False):
                files = np.sort(files)
                # print(files)
                i = 0
                for name in files[:34]:
                    # print(inf_file_name)
                    if i == 0:
                        tot_data = np.loadtxt(os.path.join(root, name))
                        ps_pos = tot_data[:, 0]
                        # print(ps_pos)
                        i = 1
                    else:
                        data = np.loadtxt(os.path.join(root, name))
                        tot_data = np.vstack((tot_data, data))
                current = tot_data[::len(ps_pos), -1]
                # print(tot_data)
                chi_temp = np.zeros(len(current))
                chi_temp_err = np.zeros(len(current))
                matrix = np.zeros((len(current), len(ps_pos)))
                matrix_err = np.zeros((len(current), len(ps_pos)))
                for i in range(len(current)):
                    matrix[i] = tot_data[:, 2][tot_data[:, -1] == current[i]
                                               ]+tot_data[:, 5][tot_data[:, -1] == current[i]]
                    matrix_err[i] = matrix[i]**0.5
                P0 = [np.average(matrix), (np.amax(matrix) -
                                           np.average(matrix)), 3, -np.pi]
                for i in range(len(current)):
                    data_ifg = matrix[i]
                    data_ifg_err = matrix_err[i]
                    B0 = ([np.amin(data_ifg), 0, 2, -3*np.pi],
                          [np.amax(data_ifg), np.amax(data_ifg), 5, 3*np.pi])
                    p, cov = fit(fit_cos, ps_pos, data_ifg, p0=P0,  bounds=B0)
                    P0 = p.copy()
                    chi_temp[i] = p[-1]
                    err = np.diag(cov)**0.5
                    chi_temp_err[i] = err[-1]

                    # print(p)
                    x_plt = np.linspace(ps_pos[0], ps_pos[-1], 100)
                    # if current[i]==-1.5:
                    # fig = plt.figure(figsize=(8,6))
                    # ax = fig.add_subplot(111)
                    # fig.suptitle(str(current[i]))
                    # ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                    # ax.plot(x_plt,fit_cos(x_plt, *p), "b")
                    # ax.set_ylim([0,1500])
                    # C= p[1]/p[0]/3
                    # w_ps=p[-2]/3
                    # chi_0=p[-1]/3
                # for i in range(len(ps_pos)):
                #     data_ifg=matrix[:,i]
                #     data_ifg_err=matrix_err[:,i]
                #     B0=([np.amin(data_ifg),0,2,-np.pi],[np.amax(data_ifg),np.amax(data_ifg),5, np.pi])
                #     # p,cov=fit(fit_cos, current, data_ifg, p0=P0,  bounds=B0)
                #     P0=p.copy()
                #     # err=np.diag(cov)**0.5
                #     # print(p)
                #     x_plt = np.linspace(current[0], current[-1],100)
                #     fig = plt.figure(figsize=(8,6))
                #     ax = fig.add_subplot(111)
                #     fig.suptitle(str(ps_pos[i]))
                #     ax.errorbar(current,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                #     # ax.plot(x_plt,fit_cos(x_plt, *p), "b")
                #     # ax.set_ylim([0,1500])
                #     # C= p[1]/p[0]/3
                #     # w_ps=p[-2]/3
        else:
            for root, dirs, files in os.walk(cleandata, topdown=False):
                files = np.sort(files)
                # print(files)
                i = 0
                for name in files[:34]:
                    # print(inf_file_name)
                    if i == 0:
                        tot_data = np.loadtxt(os.path.join(root, name))
                        ps_pos = tot_data[:, 0]
                        # print(ps_pos)
                        i = 1
                    else:
                        data = np.loadtxt(os.path.join(root, name))
                        tot_data = np.vstack((tot_data, data))
                current = tot_data[::len(ps_pos), -1]
                # print(current)
                chi_0 = np.zeros(len(current))
                chi_0_err = np.zeros(len(current))
                matrix = np.zeros((len(current), len(ps_pos)))
                matrix_err = np.zeros((len(current), len(ps_pos)))
                for i in range(len(current)):

                    matrix[i] = tot_data[:, 2][tot_data[:, -1] == current[i]
                                               ]+tot_data[:, 5][tot_data[:, -1] == current[i]]
                    matrix_err[i] = matrix[i]**0.5
                    # print(current[i])
                P0 = [np.average(matrix), (np.amax(
                    matrix)-np.average(matrix)), 3, 0]
                for i in range(len(current)):
                    data_ifg = matrix[i]
                    data_ifg_err = matrix_err[i]
                    B0 = ([np.amin(data_ifg), 0, 2, -3*np.pi],
                          [np.amax(data_ifg), np.amax(data_ifg), 5, 3*np.pi])
                    p, cov = fit(fit_cos, ps_pos, data_ifg, p0=P0,  bounds=B0)
                    P0 = p.copy()
                    chi_0[i] = p[-1]
                    err = np.diag(cov)**0.5
                    chi_0_err[i] = err[-1]
                    # print(p)
                    x_plt = np.linspace(ps_pos[0], ps_pos[-1], 100)
                    # fig = plt.figure(figsize=(8,6))
                    # ax = fig.add_subplot(111)
                    # fig.suptitle(str(current[i]))
                    # ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                    # ax.plot(x_plt,fit_cos(x_plt, *p), "b")
                    # ax.set_ylim([0,1500])
                    # C= p[1]/p[0]/3
                    # w_ps=p[-2]/3
                    # chi_0=p[-1]/3
                # for i in range(len(ps_pos)):
                #     data_ifg=matrix[:,i]
                #     data_ifg_err=matrix_err[:,i]
                #     B0=([np.amin(data_ifg),0,2,-np.pi],[np.amax(data_ifg),np.amax(data_ifg),5, np.pi])
                #     # p,cov=fit(fit_cos, current, data_ifg, p0=P0,  bounds=B0)
                #     P0=p.copy()
                #     # err=np.diag(cov)**0.5
                #     # print(p)
                #     x_plt = np.linspace(current[0], current[-1],100)
                #     fig = plt.figure(figsize=(8,6))
                #     ax = fig.add_subplot(111)
                #     fig.suptitle(str(ps_pos[i]))
                #     ax.errorbar(current,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                #     # ax.plot(x_plt,fit_cos(x_plt, *p), "b")
                #     # ax.set_ylim([0,1500])
                #     # C= p[1]/p[0]/3
                #     # w_ps=p[-2]/3

fig = plt.figure(figsize=(8, 6))
# chi_temp-=chi_temp[current==0]
chi_0 -= chi_0[current == 0]
p, cov = fit(fit_lin, current,  chi_0-chi_temp, p0=[4, 1])
ax = fig.add_subplot(111)
ax.errorbar(current, chi_0, yerr=chi_0_err, fmt="k.", capsize=3)
ax.errorbar(current, chi_temp, yerr=chi_temp_err, fmt="b.", capsize=3)
ax.errorbar(current, chi_0-chi_temp, yerr=chi_0_err +
            chi_temp_err, fmt="r.", capsize=3)
ax.plot(current, fit_lin(current, *p), "b-")
T=10e-6
print(p[1]*hbar/(mu_N*4*T))
m=p[1]*hbar/(mu_N*4*T)
B=m*0.42
w=2*np.pi*10e3
alpha=2*mu_N*B*np.sin(w*T/2)/(hbar*w)

print(alpha)

plt.show()
