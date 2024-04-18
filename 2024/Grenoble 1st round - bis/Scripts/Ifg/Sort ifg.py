# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:01:28 2023

@author: S18
"""
"""
inf file names:
"ifgPS1_2p_22pt_30Mar1656", 
"ifgPS1_2p_22pt_30Mar2129", 
"ifgPS1_2p_22pt_31Mar0104", 
"ifgPS1_2p_22pt_31Mar1557", 
"ifgPS1_2p_22pt_31Mar1645", 
"ifgPS1_2p_22pt_31Mar1751", 
"ifgPS1_2p_22pt_31Mar2116", 
"ifgPS1_2p_22pt_01Apr0408", 
"ifgPS1_2p_22pt_01Apr0429", 
"ifgPS1_2p_22pt_01Apr2138", 
"ifgPS1_2p_22pt_01Apr2148", 
"ifgPS1_2p_22pt_02Apr0615", 
"ifgPS1_2p_22pt_02Apr0625", 
"ifgPS1_2p_22pt_02Apr1622", 
"ifgPS1_2p_22pt_02Apr2011", 
"ifgPS1_2p_22pt_02Apr2032", 
"ifgPS1_2p_22pt_03Apr0405", 
"ifgPS1_2p_22pt_03Apr0426", 
"ifgPS1_2p_22pt_03Apr1201", 
"ifgPS1_2p_22pt_03Apr1848", 
"ifgPS1_2p_22pt_03Apr1953",
Indium 1.8 mm: 
"ifgPS1_2p_22pt_03Apr2002", 
"ifgPS1_2p_22pt_03Apr2023", 

"ifgPS1_2p_22pt_03Apr2033", 
"ifgPS1_2p_22pt_03Apr2055", 
"ifgPS1_2p_22pt_03Apr2110", 
Indium 1mm:
"ifgPS1_2p_22pt_03Apr2146", 
"ifgPS1_2p_22pt_04Apr0531", 
"ifgPS1_2p_22pt_04Apr0622", 
"""

import os
import numpy as np
import shutil

sc_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round - bis/exp_CRG-3126/rawdata/sc"
bad_apples=["ifgPS1_2p_22pt_08Apr1523", "ifgPS1_2p_22pt_04Apr2354",]
for root, dirs, files in os.walk(sc_fold_path, topdown=False):
    files=np.sort(files)
    for name in files:
        if ("ifgPS1_2p_" in name) and ("11Apr" in name) and (".inf" in name) and (name not in bad_apples):#(("ifg_" in name) or ("movePS" in name)) and (".inf" in name) and ("TOF_vs_chi" not in name) and ("alpha" not in name) :
            if (name[:-4] in bad_apples):
                print('bad "'+name[:-4]+'", ')
            else:
                print('"'+name[:-4]+'", ')
                inf_file_path=os.path.join(root, name)
                inf_file_name=name[:-4]
                sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round - bis/exp_CRG-3126/Sorted data/Ifg/"+inf_file_name
                
                if not os.path.exists(sorted_fold_path):
                    os.makedirs(sorted_fold_path)
    
                rawdata=sorted_fold_path+"/Rawdata" 
                if not os.path.exists(rawdata):
                    os.makedirs(rawdata)
    
                cleandata=sorted_fold_path+"/Cleantxt"
                if not os.path.exists(cleandata):
                    os.makedirs(cleandata)
                    
    
                dat_files = np.genfromtxt(inf_file_path, dtype=str, usecols=0)
                for root1, dirs1, files1 in os.walk(sc_fold_path, topdown=False):
                    i=0
                    files1=np.sort(files1)
                    for name1 in files1:
                        if (name1 in dat_files):
                            # print(name)
                            shutil.copy(os.path.join(root1, name1), rawdata+"/"+name)
                            if "TOF" in name1:
                                cleantxt=np.loadtxt(os.path.join(root1, name1), encoding='windows-1252', comments="*", delimiter="\t")[:,1:]
                                with open(cleandata+"/"+name1[:-4]+".txt", 'w') as f:
                                        np.savetxt(f, cleantxt, header= "ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2", fmt='%f %.1f %i %i %i %i %i %i %f %f')
                            else:
                                cleantxt=np.loadtxt(os.path.join(root1, name1), encoding='windows-1252', comments="*", skiprows=20,delimiter="\t")[:,1:]
                                with open(cleandata+"/"+name1[:-4]+".txt", 'w') as f:
                                        np.savetxt(f, cleantxt, header= "ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2", fmt='%f %.1f %i %i %i %i %i %i %f %f')
                            i+=1