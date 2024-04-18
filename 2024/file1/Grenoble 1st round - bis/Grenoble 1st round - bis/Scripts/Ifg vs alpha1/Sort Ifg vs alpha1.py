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

sc_fold_path="D:/data/cycle 195/exp_CRG-3126/rawdata/sc"
bad_apples=[]

for root1, dirs1, files1 in os.walk(sc_fold_path, topdown=False):
    for name1 in files1:
        if ("ifg_vs_alpha1" in name1) and ("alpha2" not in name1) and ("1946" in name1) and (".inf" in name1):
            if (name1[:-4] in bad_apples):
                print('bad "'+name1[:-4]+'", ')
            else:
                print('"'+name1[:-4]+'", ')
                inf_file_path=os.path.join(root1, name1)
                inf_file_name=name1[:-4]
                sorted_fold_path="C:/Users/S18/Desktop/Grenoble-2024 Ismaele/2024/Grenoble 1st round - bis/exp_CRG-3126/Sorted data/Ifg vs alpha1/"+inf_file_name
                
                if not os.path.exists(sorted_fold_path):
                    os.makedirs(sorted_fold_path)
    
                rawdata=sorted_fold_path+"/Rawdata" 
                if not os.path.exists(rawdata):
                    os.makedirs(rawdata)
    
                cleandata=sorted_fold_path+"/Cleantxt"
                if not os.path.exists(cleandata):
                    os.makedirs(cleandata)
                    
                dat_files = np.genfromtxt(inf_file_path, dtype=str)[:,:]
                # print(dat_files)
                Vpp=np.array([range(len(dat_files[:,0])), dat_files[:,-3].astype(float)])
                print(Vpp)
              
                for root, dirs, files in os.walk(sc_fold_path, topdown=False):
                    i=0
                    files=(np.sort(files))
                    for name in files:
                        if (name in dat_files[:,0]):
                            print(name)
                            shutil.copy(os.path.join(root, name), rawdata+"/"+name)
                            txt=np.loadtxt(os.path.join(root, name), encoding='windows-1252', comments="*", delimiter="\t")[:,1:]
                            Vpp_aux=dat_files[:,-3][dat_files[:,0]==name].astype(float) #phashifter position
                            # print(curr)
                            cleantxt =np.hstack((txt,np.ones((len(txt[:,0]),1))*Vpp_aux))
                            # print(Vpp_aux)
                            with open(cleandata+"/ifg_vs_Vpp1_"+str("%02d" % (Vpp[0][dat_files[:,0]==name],))+".txt", 'w') as f:
                                    np.savetxt(f, cleantxt, header= "BinNR ps_pos tot-time (s)  O-Beam H-Beam AUX Amplitude(func. gen.)", fmt='%f %.1f %i %i %i %i %i %i %f %f %f')
                        