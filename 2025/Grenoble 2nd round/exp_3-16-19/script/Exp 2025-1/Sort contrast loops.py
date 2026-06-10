# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 10:26:29 2025

@author: S18
"""

import os
import numpy as np
import shutil

sc_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/rawdata/sc"
sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2025/Grenoble 2nd round/exp_3-16-19/Sorted data/Contrast loops"
bad_apples=[
"Contrast_loops_B_1_2_3_11Oct1915.inf", 
"Contrast_loops_B_1_2_3_11Oct1951.inf",
"Contrast_loops_B_1_2_3_quick_12Oct1349.inf",
"Contrast_loops_B_1_2_3_11Oct1930.inf",
"Contrast_loops_B_1_2_3_quick_11Oct2120.inf",
"Contrast_loops_B_1_2_3_13Oct2010.inf",]


if not os.path.exists(sorted_fold_path):
    os.makedirs(sorted_fold_path)

cleandata_all=sorted_fold_path+"/Cleantxt all"
if not os.path.exists(cleandata_all):
    os.makedirs(cleandata_all)

for root1, dirs1, files1 in os.walk(sc_fold_path, topdown=False):
    for name1 in files1:
        if ("Contrast_loops_B_1_2_3" in name1) and (".inf" in name1) and (name1 not in bad_apples):
            inf_file_path=os.path.join(root1, name1)
            # print(name1)
            inf_file=np.loadtxt(inf_file_path, encoding='windows-1252', usecols=0, comments="*",delimiter="\t", dtype=str)

            rawdata=sorted_fold_path+"/"+name1[:-4]+"/Rawdata" 
            if not os.path.exists(rawdata):
                os.makedirs(rawdata)

            cleandata=sorted_fold_path+"/"+name1[:-4]+"/Cleantxt"
            if not os.path.exists(cleandata):
                os.makedirs(cleandata)

            i=0
            label=["B1_ps1_", "B2_ps1_","B2_ps2_", "B3_ps2_"]
            for dat_name in inf_file:
                shutil.copy(os.path.join(root1, dat_name), rawdata+"/"+dat_name)
            for dat_name in inf_file[:]:
                dat_file_path=os.path.join(root1, dat_name)
                
                # with open(dat_file_path, 'r') as src:
                #     lines_ifg2 = src.readlines()
                # print(lines_ifg2[15:-1])
                
                cleantxt_ifg=np.loadtxt(dat_file_path, encoding='windows-1252', comments="*",skiprows=33,delimiter="\t")[:,1:]
                # print(cleantxt_ifg[:,0])
                new_name="Contrast_loops_"+label[i]+dat_name[-13:-4]+".txt"
                print(new_name)
                with open(cleandata+"/"+new_name, 'w') as f:
                        np.savetxt(f, cleantxt_ifg, delimiter="\t", header= "ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2", fmt='%f %.1f %i %i %i %i %i %i %f %f')
                with open(cleandata_all+"/"+new_name, 'w') as f:
                        np.savetxt(f, cleantxt_ifg, delimiter="\t", header= "ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2", fmt='%f %.1f %i %i %i %i %i %i %f %f')
                i+=1

          