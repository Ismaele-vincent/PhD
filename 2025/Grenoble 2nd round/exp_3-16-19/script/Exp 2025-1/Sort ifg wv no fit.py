# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 10:26:29 2025

@author: S18
"""

import os
import numpy as np
import shutil
chi_names=["_0","_-pi2","_+pi2","_pi"]

sc_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/rawdata/sc"
sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Ifg wv no fit"
bad_apples=[]


if not os.path.exists(sorted_fold_path):
    os.makedirs(sorted_fold_path)


for root1, dirs1, files1 in os.walk(sc_fold_path, topdown=False):
    for name1 in files1:
        if ("ifg_wv3_psi_+1-i-1_no_fit_25Oct0631" in name1) and (".inf" in name1):
            inf_file_path=os.path.join(root1, name1)
            print(name1)
            inf_file=np.loadtxt(inf_file_path, encoding='windows-1252', usecols=0, comments="*",delimiter="\t", dtype=str)
            
            # print(inf_file)
            
            rawdata=sorted_fold_path+"/"+name1[:-4]+"/Rawdata" 
            if not os.path.exists(rawdata):
                os.makedirs(rawdata)

            cleandata=sorted_fold_path+"/"+name1[:-4]+"/Cleantxt"
            if not os.path.exists(cleandata):
                os.makedirs(cleandata)
            i=0
            for dat_name in inf_file:
                shutil.copy(os.path.join(root1, dat_name), rawdata+"/"+dat_name)
            for dat_name in inf_file[:-1]:
                dat_file_path=os.path.join(root1, dat_name)
                
                # with open(dat_file_path, 'r') as src:
                #     lines_ifg2 = src.readlines()
                # print(lines_ifg2[15:-1])
                
                cleantxt_ifg=np.loadtxt(dat_file_path, encoding='windows-1252', comments="*",skiprows=13,delimiter="\t")#15
                print(cleantxt_ifg[:,0])
                with open(cleandata+"/"+dat_name[:-4]+chi_names[i]+".txt", 'w') as f:
                        np.savetxt(f, cleantxt_ifg, delimiter="\t", header= "ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2", fmt='%i %f %.1f %i %i %i %i %i %i %f %f')
                i+=1
            int_file_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/rawdata/sc/ifg_wv3_psi_+1-1-1_no_fit_22Oct1455.dat"#os.path.join(root1, inf_file[-1])
            # int_file_path=os.path.join(root1, inf_file[-1])
            cleantxt_int=np.loadtxt(int_file_path, encoding='windows-1252', comments="*",skiprows=13,delimiter="\t")
            # print(cleantxt_int)
            with open(cleandata+"/"+inf_file[-1][:-4]+".txt", 'w') as f:
                    np.savetxt(f, cleantxt_int,delimiter="\t", header= "ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2", fmt='%i %f %.1f %i %i %i %i %i %i %f %f')
                    

# bad_int=["ifg_wv2_psi_+1-1-1_no_fit_22Oct1338.inf", "ifg_wv1_psi_+1-i-1_no_fit_21Oct1454.inf", "ifg_wv1_psi_+1-i-1_no_fit_21Oct1742.inf"]
# int_meas=sorted_fold_path+"/Int measurements" 
# if not os.path.exists(int_meas):
#     os.makedirs(int_meas)
# for root2, dirs2, files2 in os.walk(sc_fold_path, topdown=False):
#     for name2 in files2:
#         if ("ifg_" in name2) and ("no_fit_21Oct" in name2) and (".inf" in name2) and (name2 not in bad_int):
                                                                                     
#             inf_file_path=os.path.join(root2, name2)
#             # print(name2)
#             inf_file=np.loadtxt(inf_file_path, encoding='windows-1252', usecols=0, comments="*",delimiter="\t", dtype=str)
#             int_meas=sorted_fold_path+"/Int measurements" 
            
#             shutil.copy(os.path.join(root2, inf_file[-1]), int_meas+"/"+inf_file[-1])
# for root2, dirs2, files2 in os.walk(int_meas, topdown=False):
#     for name2 in files2:
#             print(name2)