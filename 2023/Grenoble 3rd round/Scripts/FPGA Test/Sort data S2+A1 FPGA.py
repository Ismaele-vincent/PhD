# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 16:47:34 2023

@author: S18
"""

import os
import numpy as np
import shutil

sc_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/exp_3-16-14/rawdata/sc/"

for root, dirs, files in os.walk(sc_fold_path, topdown=False):
    for name in files:
        if ("TOFx_vs_chi_S2+A1_19pt_" in name) and (".inf" in name):
            print('"'+name[:-4]+'", ')
            inf_file_path=os.path.join(root, name)
            inf_file_name=name[:-4]
            sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 3rd round/exp_3-16-14/Sorted data/FPGA Test/"+inf_file_name
            
            if not os.path.exists(sorted_fold_path):
                os.makedirs(sorted_fold_path)

            rawdata=sorted_fold_path+"/Rawdata" 
            if not os.path.exists(rawdata):
                os.makedirs(rawdata)

            cleandata=sorted_fold_path+"/Cleantxt"
            if not os.path.exists(cleandata):
                os.makedirs(cleandata)

            dat_files = np.genfromtxt(inf_file_path, dtype=str)
            
            if  dat_files[1:,-1].astype(float).all()==dat_files[1:,-1].astype(float)[0]:
                ps_num=np.array([range(len(dat_files[:,0])), range(len(dat_files[:,0]))])
                print( dat_files[:,-1])
                dat_files[:,-1]=ps_num[0]
                
            else:
                ps_num=np.array([range(len(dat_files[:,0])), dat_files[:,-1].astype(float)])
            # print(dat_files)
            # print(ps_num)
            for root, dirs, files in os.walk(sc_fold_path, topdown=False):
                i=0
                for name in files:
                    if (name in dat_files[:,0]):
                        if ("ifg" in name) and (name==dat_files[0,0] or name==dat_files[6,0] or name==dat_files[13,0]):
                            # print(name)
                            cleantxt=np.loadtxt(os.path.join(root, name), encoding='windows-1252', skiprows=20, comments="*", delimiter="\t")[:,1:]
                            with open(cleandata+"/"+"ifg_20s_3p_"+name[-8:-4]+".txt", 'w') as f:
                                np.savetxt(f, cleantxt, header= " ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H+AUX encod1 encod2", fmt='%f %.1f %i %i %i %i %i %i %f %f')
                        else:
                            # print(name)
                            shutil.copy(os.path.join(root, name), rawdata+"/"+name)
                            txt=np.loadtxt(os.path.join(root, name), encoding='windows-1252', comments="*", delimiter="\t")[:,:]
                            ps=dat_files[:,-1][dat_files[:,0]==name].astype(float) #phashifter position
                            func_gen=dat_files[:,-7:-1][dat_files[:,0]==name].astype(float)
                            # print(ps)
                            cleantxt =np.hstack((txt,np.ones((len(txt[:,0]),6))*func_gen,np.ones((len(txt[:,0]),1))*ps[0]))
                            # print(cleantxt)
                            with open(cleandata+"/TOF_ps_"+str("%02d" % (ps_num[0][ps_num[1]==ps][0],)[0])+".txt", 'w') as f:
                                    np.savetxt(f, cleantxt, header= "BinNR microsec tot-time (s)  O-Beam H-Beam AUX Ampl_1(V) f_1(Hz) phase_1(deg) Ampl_2(V) f_2(Hz) phase_2(deg) chi(pos)", fmt='%i %.2f %.2f %i %i %i %.3f %.3f %.3f %.3f %.3f %.3f %.3f')