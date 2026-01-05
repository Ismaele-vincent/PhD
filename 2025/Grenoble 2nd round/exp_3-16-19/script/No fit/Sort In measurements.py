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
sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Ifg Indium"
bad_apples=["count_60s_In1_+1+1+1_23Oct1915.dat","count_60s_In1_+1-i-1_23Oct1927.dat","count_60s_In1_+exp(-i60)+1+exp(i120)_23Oct1939.dat", "count_60s_In3_+1+1+1_23Oct1953.dat" #probably no In measurement
            ]


if not os.path.exists(sorted_fold_path):
    os.makedirs(sorted_fold_path)


for root1, dirs1, files1 in os.walk(sc_fold_path, topdown=False):
    for name1 in files1:
        if ("count_60s_" in name1) and ("+1+1+1" in name1) and (".dat" in name1) and (name1 not in bad_apples):
            # inf_file_path=os.path.join(root1, name1)
            # print(name1)
            # dat_file=np.loadtxt(inf_file_path, encoding='windows-1252', usecols=0, comments="*",delimiter="\t", dtype=str)
            
            # print(dat_file)
            
            # rawdata=sorted_fold_path+"/Ifg wv1/"+name1[:-4]+"/Rawdata" 
            # if not os.path.exists(rawdata):
            #     os.makedirs(rawdata)

            # cleandata=sorted_fold_path+"/"+name1[:-4]+"/Cleantxt"
            cleandata=sorted_fold_path+"/Cleantxt +1+1+1"
            if not os.path.exists(cleandata):
                os.makedirs(cleandata)
          
            # for dat_name in inf_file:
            #     shutil.copy(os.path.join(root1, dat_name), rawdata+"/"+dat_name)
           
            dat_file_path=os.path.join(root1, name1)
            
            # with open(dat_file_path, 'r') as src:
            #     lines_ifg2 = src.readlines()
            # print(lines_ifg2[15:-1])
            
            cleantxt_ifg=np.loadtxt(dat_file_path, encoding='windows-1252', comments="*",skiprows=5,delimiter="\t")#15
            # print(cleantxt_ifg)
            with open(cleandata+"/"+name1[:-4]+".txt", 'w') as f:
                    np.savetxt(f, cleantxt_ifg, delimiter="\t", header= "ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2")#, fmt='%i %f %.1f %i %i %i %i %i %i %f %f')
        if ("count_60s_" in name1) and ("+1-i-1" in name1) and (".dat" in name1) and (name1 not in bad_apples):
            # inf_file_path=os.path.join(root1, name1)
            # print(name1)
            # dat_file=np.loadtxt(inf_file_path, encoding='windows-1252', usecols=0, comments="*",delimiter="\t", dtype=str)
            
            # print(dat_file)
            
            # rawdata=sorted_fold_path+"/Ifg wv1/"+name1[:-4]+"/Rawdata" 
            # if not os.path.exists(rawdata):
            #     os.makedirs(rawdata)

            # cleandata=sorted_fold_path+"/"+name1[:-4]+"/Cleantxt"
            cleandata=sorted_fold_path+"/Cleantxt +1-i-1"
            if not os.path.exists(cleandata):
                os.makedirs(cleandata)
          
            # for dat_name in inf_file:
            #     shutil.copy(os.path.join(root1, dat_name), rawdata+"/"+dat_name)
           
            dat_file_path=os.path.join(root1, name1)
            
            # with open(dat_file_path, 'r') as src:
            #     lines_ifg2 = src.readlines()
            # print(lines_ifg2[15:-1])
            
            cleantxt_ifg=np.loadtxt(dat_file_path, encoding='windows-1252', comments="*",skiprows=5,delimiter="\t")#15
            # print(cleantxt_ifg)
            with open(cleandata+"/"+name1[:-4]+".txt", 'w') as f:
                    np.savetxt(f, cleantxt_ifg, delimiter="\t", header= "ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2")#, fmt='%i %f %.1f %i %i %i %i %i %i %f %f')
        if ("count_60s_" in name1) and ("+exp(-i60)+1+exp(i120)" in name1) and (".dat" in name1) and (name1 not in bad_apples):
            # inf_file_path=os.path.join(root1, name1)
            # print(name1)
            # dat_file=np.loadtxt(inf_file_path, encoding='windows-1252', usecols=0, comments="*",delimiter="\t", dtype=str)
            
            # print(dat_file)
            
            # rawdata=sorted_fold_path+"/Ifg wv1/"+name1[:-4]+"/Rawdata" 
            # if not os.path.exists(rawdata):
            #     os.makedirs(rawdata)

            # cleandata=sorted_fold_path+"/"+name1[:-4]+"/Cleantxt"
            cleandata=sorted_fold_path+"/Cleantxt +exp(-i60)+1+exp(i120)"
            if not os.path.exists(cleandata):
                os.makedirs(cleandata)
          
            # for dat_name in inf_file:
            #     shutil.copy(os.path.join(root1, dat_name), rawdata+"/"+dat_name)
           
            dat_file_path=os.path.join(root1, name1)
            
            # with open(dat_file_path, 'r') as src:
            #     lines_ifg2 = src.readlines()
            # print(lines_ifg2[15:-1])
            
            cleantxt_ifg=np.loadtxt(dat_file_path, encoding='windows-1252', comments="*",skiprows=5,delimiter="\t")#15
            # print(cleantxt_ifg)
            with open(cleandata+"/"+name1[:-4]+".txt", 'w') as f:
                    np.savetxt(f, cleantxt_ifg, delimiter="\t", header= "ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2")#, fmt='%i %f %.1f %i %i %i %i %i %i %f %f')
          