# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:37:41 2023

@author: S18
"""
"""
inf_file_names:
"ifg_20s_3p_29Aug0134", 
"ifg_20s_3p_10Sep2312", 
"ifg_20s_3p_09Sep1210", 
"ifg_20s_3p_26Aug2225", 
"movePS_90_31Aug1423", 
"ifg_20s_3p_27Aug1603", 
"movePS_90_03Sep0612", 
"ifg_5s_1p_28Aug0749", 
"movePS_90_06Sep1502", 
"movePS_270_06Sep1946", 
"ifg_5s_1p_24Aug2356", 
"ifg_20s_3p_29Aug1053", 
"movePS_90_31Aug1506", 
"movePS_270_07Sep1248", 
"movePS_90_28Aug1929", 
"movePS_270_07Sep1136", 
"movePS_270_28Aug1718", 
"ifg_5s_1p_24Aug1743", 
"movePS_90_01Sep1328", 
"ifg_20s_3p_03Sep0634", 
"ifg_20s_3p_04Sep2026", 
"ifg_20s_3p_27Aug2046", 
"movePS_270_06Sep1920", 
"ifg_20s_3p_09Sep0358", 
"ifg_5s_1p_24Aug0020", 
"movePS_0_01Sep1737", 
"ifg_5s_1p_24Aug1737", 
"ifg_5s_1p_24Aug1819", 
"ifg_20s_3p_01Sep2248", 
"ifg_20s_3p_04Sep2013", 
"ifg_20s_3p_25Aug1139", 
"ifg_5s_1p_24Aug1135", 
"ifg_20s_3p_28Aug1957", 
"ifg_5s_1p_24Aug0608", 
"movePS_90_02Sep1937", 
"ifg_20s_3p_26Aug1121", 
"ifg_5s_1p_25Aug0532", 
"ifg_5s_1p_25Aug0522", 
"ifg_5s_1p_24Aug1720", 
"movePS_90_06Sep1336", 
"movePS_90_02Sep0901", 
"movePS_270_07Sep1110", 
"ifg_5s_1p_26Aug1659", 
"ifg_5s_1p_24Aug0558", 
"ifg_20s_3p_25Aug1535", 
"movePS_270_06Sep1755", 
"ifg_5s_1p_24Aug1754", 
"movePS_270_07Sep1314", 
"ifg_5s_1p_23Aug1506", 
"movePS_90_01Sep2226", 
"movePS_90_31Aug1912", 
"movePS_90_31Aug2006", 
"ifg_20s_3p_10Sep2326", 
"ifg_20s_3p_02Sep0923", 
"ifg_5s_1p_24Aug2345", 
"movePS_0_27Aug1900", 
"ifg_5s_1p_23Aug1854", 
"ifg_20s_3p_28Aug1018", 
"movePS_90_28Aug1938", 
"movePS_0_01Sep1725", 
"movePS_90_01Sep1451", 
"ifg_5s_1p_24Aug0031", 
"ifg_5s_1p_24Aug1145", 
"ifg_20s_3p_23Aug1443", 
"ifg_5s_1p_28Aug0223", 
"ifg_5s_1p_24Aug1726", 
"movePS_270_28Aug1602", 
"ifg_20s_3p_09Sep2131", 
"movePS_0_27Aug1800", 
"movePS_270_06Sep1912", 
"movePS_0_06Sep1821", 
"movePS_90_29Aug0718", 
"ifg_20s_3p_02Sep1959",

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
    return A+B*np.cos(C*x-D)

def fit_cos_unb(x, A, C, D, Co): 
    return A*((1 - Co)/2 + Co*(1/2+a_1*a_2*np.cos(C*x-D)))

inf_file_names=[
"ifg_TOF_S2_pi8_26Sep1135",
]

for inf_file_name in inf_file_names:
    # if "20s" in inf_file_name:
        print(inf_file_name)
        sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/exp_3-16-14/Sorted data/Ifg/"+inf_file_name
        cleandata=sorted_fold_path+"/Cleantxt"
        for root, dirs, files in os.walk(cleandata, topdown=False):
            files=np.sort(files) 
            for name in files:
                # print(name)
                tot_data=np.loadtxt(os.path.join(root, name))
                data_ifg=tot_data[:,2]+tot_data[:,5]
                data_ifg_err=data_ifg**0.5
                ps_pos=tot_data[:,0]
                P0=[(np.amax(data_ifg)+np.amin(data_ifg))/2, (np.amax(data_ifg)-np.amin(data_ifg))/2, 3, -1]
                B0=([np.amin(data_ifg),0,0.01,-10],[np.amax(data_ifg),np.amax(data_ifg),5, 10])
                p,cov=fit(fit_cos, ps_pos, data_ifg, p0=P0,  bounds=B0)
                P0_unb=[100000, 3, -0.5, 0.7]
                B0_unb=([0,1,-10, 0],[1e10,4,10,1])
                p_unb,cov_unb=fit(fit_cos_unb, ps_pos, data_ifg, p0=P0_unb,  bounds=B0_unb)
                err=np.diag(cov)**0.5
                # print(p[3], err[3])
                x_plt = np.linspace(ps_pos[0], ps_pos[-1],100)
                fig = plt.figure(figsize=(8,6))
                ax = fig.add_subplot(111)
                fig.suptitle(name[:-4]+".inf")
                ax.errorbar(ps_pos,data_ifg,yerr=data_ifg_err,fmt="ko",capsize=5, ms=3)
                ax.plot(x_plt,fit_cos(x_plt, *p), "b")
                # ax.plot(x_plt,fit_cos_unb(x_plt, *p_unb), "r--")
                # ax.set_ylim([0,1500])
                print("C=", p[1]/p[0], "+-", ((err[1]/p[0])**2+(err[1]*p[1]/p[0]**2)**2)**0.5)
                print("C_unb=", p_unb[-1])
                print(p_unb)
                print("w_ps=", p[-2], "+-", err[-2])
                print("chi_0=", p[-1])
plt.savefig("/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/Report/Images/IFG S2 no in.pdf", format="pdf", bbox_inches="tight")
plt.show()