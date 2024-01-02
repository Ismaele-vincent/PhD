# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:01:28 2023

@author: S18
"""
"""
bad apples:
"""

import os
import numpy as np
import shutil

sc_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/rawdata/sc"

bad_apples=[]
for root, dirs, files in os.walk(sc_fold_path, topdown=False):
    for name in files:
        if ("ifg_-2" in name) and (".inf" in name)  :
            if (name[:-4] in bad_apples):
                print('bad "'+name[:-4]+'", ')
            else:
                print('"'+name[:-4]+'", ')
                inf_file_path=os.path.join(root, name)
                inf_file_name=name[:-4]
                sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/Ifg off/"+inf_file_name
                
                if not os.path.exists(sorted_fold_path):
                    os.makedirs(sorted_fold_path)
    
                rawdata=sorted_fold_path+"/Rawdata" 
                if not os.path.exists(rawdata):
                    os.makedirs(rawdata)
    
                cleandata=sorted_fold_path+"/Cleantxt"
                if not os.path.exists(cleandata):
                    os.makedirs(cleandata)
                    
    
                dat_files = np.genfromtxt(inf_file_path, dtype=str, usecols=0)
                for root, dirs, files in os.walk(sc_fold_path, topdown=False):
                    i=0
                    for name in files:
                        if (name in dat_files):
                            # print(name)
                            shutil.copy(os.path.join(root, name), rawdata+"/"+name)
                            cleantxt=np.loadtxt(os.path.join(root, name), encoding='windows-1252', comments="*", delimiter="\t")[:,1:]
                            with open(cleandata+"/"+name[:-4]+".txt", 'w') as f:
                                    np.savetxt(f, cleantxt, header= "ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H encod1 encod2", fmt='%f %.1f %i %i %i %i %i %i %f %f')