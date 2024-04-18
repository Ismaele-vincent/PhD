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

sc_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/exp_3-16-14/rawdata/sc/"

bad_apples=[]
for root, dirs, files in os.walk(sc_fold_path, topdown=False):
    for name0 in files:
        if ("alpha_" in name0) and (".inf" in name0)  :
            if (name0[:-4] in bad_apples):
                print('bad "'+name0[:-4]+'", ')
            else:
                print('"'+name0[:-4]+'", ')
                inf_file_path=os.path.join(root, name0)
                inf_file_name=name0[:-4]
                sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/exp_3-16-14/Sorted data/Alpha/"+inf_file_name
                
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
                    for name1 in files:
                        if ("ifg" in name1) and ("ifg" in name0):
                            if (name1 in dat_files[2:]):
                                # print(name1)
                                shutil.copy(os.path.join(root, name1), rawdata+"/"+name1)
                                txt=np.loadtxt(os.path.join(root, name1), encoding='windows-1252', comments="*", delimiter="\t")[:,1:]
                                current=np.linspace(-2,2,len(dat_files[2:]))
                                current=abs(current[np.argsort(abs(current))])
                                current[1::2]*=-1
                                cleantxt =np.hstack((txt, np.ones((len(txt[:,0]),1))*current[dat_files[2:]==name1]))
                                order=current*10+20
                                with open(cleandata+"/alpha"+str("%02d" % (order[dat_files[2:]==name1],))+".txt", 'w') as f:
                                    np.savetxt(f, cleantxt, header= "ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2 current(Amp)", fmt='%f %.1f %i %i %i %i %i %i %f %f %f')
                        else:
                            if (name1 in dat_files) and ("ifg" not in name0):
                                # print(name1)
                                cleantxt=np.loadtxt(os.path.join(root, name1), encoding='windows-1252', comments="*", delimiter="\t")[:,1:]
                                current= cleantxt[:,0]
                                cleantxt=cleantxt[np.argsort(current)]
                                with open(cleandata+"/"+name1[:-4]+".txt", 'w') as f:
                                    np.savetxt(f, cleantxt, header= "current(Amp) exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2", fmt='%f %.1f %i %i %i %i %i %i %f %f')