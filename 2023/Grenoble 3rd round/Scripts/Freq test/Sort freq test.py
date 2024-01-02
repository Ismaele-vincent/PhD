# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 16:27:20 2023

@author: S18
"""

"""
bad apples:
"Freq_test_26Aug1048",
"Freq_test_26Aug1051",
"Freq_test_26Aug1051",
"Freq_test_26Aug1054",
"Freq_test_26Aug1103",
"Freq_test_26Aug1108", 
"Freq_test_27Aug1420",
"Freq_test_27Aug1501",  
"Freq_test_31Aug1410", 
"""

import os
import numpy as np
import shutil

sc_fold_path="D:/data/Cycle 192ter/exp_3-16-14/rawdata/sc/"
bad_apples=[
"Freq_test_26Aug1048",
"Freq_test_26Aug1051",
"Freq_test_26Aug1051",
"Freq_test_26Aug1054",
"Freq_test_26Aug1103",
"Freq_test_26Aug1108", 
"Freq_test_27Aug1420",
"Freq_test_27Aug1501", 
"Freq_test_31Aug1410", ]
for root, dirs, files in os.walk(sc_fold_path, topdown=False):
    for name in files:
        if ("Freq_test" in name) and (".inf" in name):
            if (name[:-4] in bad_apples):
                print('bad "'+name[:-4]+'", ')
            else:
                print('"'+name[:-4]+'", ')
                inf_file_path=os.path.join(root, name)
                inf_file_name=name[:-4]
                sorted_fold_path="C:/Users/S18/Desktop/Grenoble-2023 Ismaele/Grenoble 3rd round/exp_3-16-14/Sorted data/Freq test/"+inf_file_name
                
                if not os.path.exists(sorted_fold_path):
                    os.makedirs(sorted_fold_path)
    
                rawdata=sorted_fold_path+"/Rawdata" 
                if not os.path.exists(rawdata):
                    os.makedirs(rawdata)
    
                cleandata=sorted_fold_path+"/Cleantxt"
                if not os.path.exists(cleandata):
                    os.makedirs(cleandata)
                    
                dat_files = np.genfromtxt(inf_file_path, dtype=str)
                # print(dat_files)
                for root, dirs, files in os.walk(sc_fold_path, topdown=False):
                    i=0
                    for name in files:
                        if (name in dat_files[:,0]):
                            # print(name)
                            shutil.copy(os.path.join(root, name), rawdata+"/"+name)
                            txt=np.loadtxt(os.path.join(root, name), encoding='windows-1252', comments="*", delimiter="\t")[1:-1,:]
                            # print(txt)
                            ps_pos=dat_files[:,3][dat_files[:,0]==name].astype(float)
                            func_gen=dat_files[:,4:][dat_files[:,0]==name].astype(float)[0]
                            # print(ps_pos)
                            cleantxt =np.hstack((txt,np.ones((len(txt[:,0]),3))*func_gen,np.ones((len(txt[:,0]),1))*ps_pos))
                            # print(func_gen)
                            # print(cleantxt)
                            with open(cleandata+"/Freq_test_"+str("%.1f" % (func_gen[0],))+"V_"+str("%.1f" % (func_gen[1]*1e-3,))+"kHz.txt", 'w') as f:
                                    np.savetxt(f, cleantxt, header="BinNR microsec tot-time (s)  O-Beam AUX Ampl(V) f(Hz) phase(deg) chi(pos)", fmt='%i %.2f %.2f %i %i %.3f %.3f %.3f %.3f')