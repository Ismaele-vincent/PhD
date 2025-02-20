# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:01:28 2023

@author: S18
"""
"""
dat file names:
"""

import os
import numpy as np
import shutil

sc_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round/exp_CRG-3125/rawdata/sc"
bad_apples=["ifgPS1_2p_22pt_08Apr1523", "ifgPS1_2p_22pt_04Apr2354","ifgPS1_2p_22pt_11Apr1655", "ifgPS1_2p_22pt_300s_11Apr1707", "ifgPS1_2p_22pt_300s_12Apr1204" ]
for root, dirs, files in os.walk(sc_fold_path, topdown=False):
    files=np.sort(files)
    for name in files:
        if ("ifgPS1_42pt_25Mar2116" in name) and (".dat" in name) and (name not in bad_apples):#(("ifg_" in name) or ("movePS" in name)) and (".dat" in name) and ("TOF_vs_chi" not in name) and ("alpha" not in name) :
            if (name[:-4] in bad_apples):
                print('bad "'+name[:-4]+'", ')
            else:
                print('"'+name[:-4]+'", ')
                dat_file_path=os.path.join(root, name)
                dat_file_name=name[:-4]
                sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round - bis/exp_CRG-3126/Sorted data/Ifg/"+dat_file_name
                
                if not os.path.exists(sorted_fold_path):
                    os.makedirs(sorted_fold_path)
    
                rawdata=sorted_fold_path+"/Rawdata" 
                if not os.path.exists(rawdata):
                    os.makedirs(rawdata)
    
                cleandata=sorted_fold_path+"/Cleantxt"
                if not os.path.exists(cleandata):
                    os.makedirs(cleandata)
                    
                dat_files = np.genfromtxt(dat_file_path, dtype=str, usecols=0)
                shutil.copy(sc_fold_path+name_dat, rawdata+"/"+name)
                cleantxt=np.loadtxt(sc_fold_path+name_dat, encoding='windows-1252', comments="*", skiprows=26,delimiter="\t")[:,1:]
                with open(cleandata+"/ifgPS1_"+name_dat[-13:-4]+chi_names[i]+".txt", 'w') as f:
                        np.savetxt(f, cleantxt, header= "ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2", fmt='%f %.1f %i %i %i %i %i %i %f %f')
                