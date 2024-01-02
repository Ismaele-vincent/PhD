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

sc_fold_path="D:/data/Cycle 192ter/exp_3-16-14/rawdata/sc/"
bad_apples=["TOF_S2_alpha_ifg_07Sep2027",
"TOF_S2_alpha_ifg_08Sep0110", 
"TOF_S2_alpha_ifg_08Sep1006"]

for root, dirs, files in os.walk(sc_fold_path, topdown=False):
    for name1 in files:
        if ("_alpha_ifg" in name1) and (".inf" in name1):
            if (name1[:-4] in bad_apples):
                print('bad "'+name1[:-4]+'", ')
            else:
                print('"'+name1[:-4]+'", ')
                inf_file_path=os.path.join(root, name1)
                inf_file_name=name1[:-4]
                sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/exp_3-16-14/Sorted data/Alpha Fourier/"+inf_file_name
                
                if not os.path.exists(sorted_fold_path):
                    os.makedirs(sorted_fold_path)
    
                rawdata=sorted_fold_path+"/Rawdata" 
                if not os.path.exists(rawdata):
                    os.makedirs(rawdata)
    
                cleandata=sorted_fold_path+"/Cleantxt"
                if not os.path.exists(cleandata):
                    os.makedirs(cleandata)
                    
                dat_files = np.genfromtxt(inf_file_path, dtype=str)[1::2,:]
                dat_files_ifg = np.genfromtxt(inf_file_path, dtype=str)[::2,:]
                # print(dat_files_ifg)
                current=np.array([range(len(dat_files[:,0])), dat_files[:,2].astype(float)])
                # print(current)
                # print(dat_files)
                for root, dirs, files in os.walk(sc_fold_path, topdown=False):
                    i=0
                    for name in files:
                        if (name in dat_files[:,0]):
                            # print(name)
                            shutil.copy(os.path.join(root, name), rawdata+"/"+name)
                            txt=np.loadtxt(os.path.join(root, name), encoding='windows-1252', comments="*", max_rows=142, delimiter="\t")[:,:]
                            ps=dat_files[:,-1][dat_files[:,0]==name].astype(float) #phashifter position
                            func_gen=dat_files[:,2:5][dat_files[:,0]==name].astype(float)
                            curr=func_gen[0,0]
                            # print(curr)
                            cleantxt =np.hstack((txt,np.ones((len(txt[:,0]),3))*func_gen,np.ones((len(txt[:,0]),1))*ps[0]))
                            # print(cleantxt)
                            with open(cleandata+"/TOF_current_"+str("%02d" % (current[0][dat_files[:,0]==name][0],))+".txt", 'w') as f:
                                    np.savetxt(f, cleantxt, header= "BinNR microsec tot-time (s)  O-Beam AUX Ampl(V) f(Hz) phase(deg) chi(pos)", fmt='%i %.2f %.2f %i %i %.3f %.3f %.3f %.3f')
                        if (name in dat_files_ifg[:,0]) and name[:3]=="ifg":
                            # print(name)
                            cleantxt_ifg=np.loadtxt(os.path.join(root, name), encoding='windows-1252', comments="*", delimiter="\t")[:,1:]
                            with open(cleandata+"/"+"ifg_20s_"+str("%02d" % (current[0][dat_files_ifg[:,0]==name][0],))+".txt", 'w') as f:
                                np.savetxt(f, cleantxt_ifg, header= " ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2", fmt='%f %.1f %i %i %i %i %i %i %f %f')