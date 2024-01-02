# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 16:13:20 2023

@author: S18
"""

"""
bad apples:
"TOF_S2_alpha_ifg_07Sep2027",
"TOF_S2_alpha_ifg_08Sep0110", 
"TOF_S2_alpha_ifg_08Sep1006",
"""
import os
import numpy as np
import shutil

sc_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/rawdata/sc"
bad_apples=[]

for root, dirs, files in os.walk(sc_fold_path, topdown=False):
    for name1 in files:
        if ("ifg_vs_B" in name1) and (".inf" in name1):
            if (name1[:-4] in bad_apples):
                print('bad "'+name1[:-4]+'", ')
            else:
                print('"'+name1[:-4]+'", ')
                inf_file_path=os.path.join(root, name1)
                inf_file_name=name1[:-4]
                sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/Ifg vs B-field/"+inf_file_name
                
                if not os.path.exists(sorted_fold_path):
                    os.makedirs(sorted_fold_path)
    
                rawdata=sorted_fold_path+"/Rawdata" 
                if not os.path.exists(rawdata):
                    os.makedirs(rawdata)
    
                cleandata=sorted_fold_path+"/Cleantxt"
                if not os.path.exists(cleandata):
                    os.makedirs(cleandata)
                    
                dat_files = np.genfromtxt(inf_file_path, dtype=str)[:,:]
                dat_files_ifg = np.genfromtxt(inf_file_path, dtype=str)[:,:]
                # print(dat_files_ifg)
                current=np.array([range(len(dat_files[:,0])), dat_files[:,-1].astype(float)])
                # print(current)
                # print(dat_files)
                for root, dirs, files in os.walk(sc_fold_path, topdown=False):
                    i=0
                    for name in files:
                        if (name in dat_files[:,0]):
                            # print(name)
                            shutil.copy(os.path.join(root, name), rawdata+"/"+name)
                            txt=np.loadtxt(os.path.join(root, name), encoding='windows-1252', comments="*", delimiter="\t")[:,1:]
                            curr=dat_files[:,-1][dat_files[:,0]==name].astype(float) #phashifter position
                            # print(curr)
                            cleantxt =np.hstack((txt,np.ones((len(txt[:,0]),1))*curr))
                            # print(cleantxt)
                            with open(cleandata+"/TOF_current_"+str("%02d" % (current[0][dat_files[:,0]==name][0],))+".txt", 'w') as f:
                                    np.savetxt(f, cleantxt, header= "BinNR ps_pos tot-time (s)  O-Beam H-Beam AUX Amplitude(func. gen.)", fmt='%f %.1f %i %i %i %i %i %i %f %f %f')
                        