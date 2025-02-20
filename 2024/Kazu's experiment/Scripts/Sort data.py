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

sc_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Kazu's experiment/Rawdata"
bad_apples=[]
for root, dirs, files in os.walk(sc_fold_path):
    # files=np.sort(files)
    for name in files:
        if ("Zplus" in name) or ("Zminus" in name) or ("Xplus" in name) or ("Xminus" in name) or ("Yplus" in name) or ("Yminus" in name):
            if (name[:-4] in bad_apples):
                print('bad "'+name[:-4]+'", ')
            else:
                print('"'+name+'", ')
                dat_file_path=os.path.join(root, name)
                fold_name=root.split("/")[-1]
                
                sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Kazu's experiment/Sorted data/"+fold_name
                print(sorted_fold_path)
                if not os.path.exists(sorted_fold_path):
                    os.makedirs(sorted_fold_path)
    
                rawdata=sorted_fold_path+"/Rawdata" 
                if not os.path.exists(rawdata):
                    os.makedirs(rawdata)
    
                cleandata=sorted_fold_path+"/Cleantxt"
                if not os.path.exists(cleandata):
                    os.makedirs(cleandata)
                    
                
                dat_file = np.genfromtxt(dat_file_path, skip_header=4)[:]
                header="IScan(mA):\tDetector(cnts):\tMonitor_Max,Min (cnts/sec):\tNorm(1/s):\terr(1/s):\tFlippRI Scan (mA):  Detector (cnts):   Monitor_Max,Min (cnts/sec):   Norm(1/s):   err(1/s) :     FlippRatio:     ErrFlippRatioatio:\tErrFlippRatio"
                # print(dat_file)
                with open(cleandata+"/"+name, 'w') as f:
                        np.savetxt(f, dat_file, header= header)
                shutil.copyfile(dat_file_path, rawdata+"/"+name)
                # chi_names=["_0","_pi2","_pi","_3pi2"]
                # for root1, dirs1, files1 in os.walk(sc_fold_path, topdown=False):
                #     i=0
                #     files1=np.sort(files1)
                #     for name in files1:
                #         if (name in dat_files):
                #             print(name)
                #             # shutil.copy(os.path.join(root, name), rawdata+"/"+name)
                #             # cleantxt=np.loadtxt(os.path.join(root, name), encoding='windows-1252', comments="*", skiprows=20,delimiter="\t")[:,1:]
                #             # with open(cleandata+"/"+name[:-4]+chi_names[i]+".txt", 'w') as f:
                #             #         np.savetxt(f, cleantxt, header= "ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2", fmt='%f %.1f %i %i %i %i %i %i %f %f')
                #             i+=1