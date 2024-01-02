#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 10:03:06 2023

@author: aaa
"""
"""
bad apples:
"""
import os
import numpy as np
import shutil

sc_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/rawdata/sc"
bad_apples=["TOF_vs_chi_A_19pt_pi16_1500s_03Nov1230"]

for root, dirs, files in os.walk(sc_fold_path, topdown=False):
    for name1 in files:
        if ("Freq_test_long" in name1) and (".inf" in name1):
            if (name1[:-4] in bad_apples):
                print('bad "'+name1[:-4]+'", ')
            else:
                print('inf_file_name="'+name1[:-4]+'"')
                inf_file_path=os.path.join(root, name1)
                inf_file_name=name1[:-4]
                sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2023/Grenoble 4th round/exp_CRG-3061/Sorted data/Freq test/"+inf_file_name
                
                if not os.path.exists(sorted_fold_path):
                    os.makedirs(sorted_fold_path)
    
                rawdata=sorted_fold_path+"/Rawdata" 
                if not os.path.exists(rawdata):
                    os.makedirs(rawdata)
                
                rawdata_ifg=sorted_fold_path+"/Rawdata/Ifg" 
                if not os.path.exists(rawdata_ifg):
                    os.makedirs(rawdata_ifg)
                    
                rawdata_freq=sorted_fold_path+"/Rawdata/Freq" 
                if not os.path.exists(rawdata_freq):
                    os.makedirs(rawdata_freq)
                
                cleandata=sorted_fold_path+"/Cleantxt"
                if not os.path.exists(cleandata):
                    os.makedirs(cleandata)
                
                cleandata_ifg=sorted_fold_path+"/Cleantxt/Ifg" 
                if not os.path.exists(cleandata_ifg):
                    os.makedirs(cleandata_ifg)
                    
                cleandata_freq=sorted_fold_path+"/Cleantxt/Freq" 
                if not os.path.exists(cleandata_freq):
                    os.makedirs(cleandata_freq)
                    
                
                dat_files_freq = np.genfromtxt(inf_file_path, dtype=str)[1::2,:]
                dat_files_ifg = np.genfromtxt(inf_file_path, dtype=str)[::2,:]
                # print(dat_files_ifg)
                freq_num=np.array([range(len(dat_files_freq[:,0])), dat_files_freq[:,4].astype(float)])
                for root, dirs, files in os.walk(sc_fold_path, topdown=False):
                    i=0
                    for name in files:
                        if (name in dat_files_ifg[:,0]):
                            # print(name)
                            shutil.copy(os.path.join(root, name), rawdata_ifg+"/"+name)
                            txt=np.loadtxt(os.path.join(root, name), encoding='windows-1252', comments="*", delimiter="\t")[:,:]
                            freq=dat_files_freq[:,4][dat_files_ifg[:,0]==name].astype(float)
                            cleantxt =np.hstack((txt,np.ones((len(txt[:,0]),1))*freq))
                            # print(freq)
                            # print(func_gen)
                            # print(ps)
                            # print(cleantxt)
                            with open(cleandata_ifg+"/ifg_freq_"+str("%02d" % (freq_num[0][freq_num[1]==freq][0],))+".txt", 'w') as f:
                                    np.savetxt(f, cleantxt, header= "ps_pos exposure_time(s) O-Beam H-Beam Monitor AUX-Beam time(s) O+H encod1 encod2", fmt='%i %f %.1f %i %i %i %i %i %i %f %f %.2f')
                        if (name in dat_files_freq[:,0]):
                            # print(name)
                            shutil.copy(os.path.join(root, name), rawdata_freq+"/"+name)
                            txt=np.loadtxt(os.path.join(root, name), encoding='windows-1252', comments="*", delimiter="\t")[:,:]
                            freq=dat_files_freq[:,4][dat_files_freq[:,0]==name].astype(float) 
                            # print(func_gen)
                            # print(ps)
                            cleantxt =np.hstack((txt,np.ones((len(txt[:,0]),1))*freq))
                            # print(cleantxt)
                            with open(cleandata_freq+"/TOF_freq_"+str("%02d" % (freq_num[0][freq_num[1]==freq][0],))+".txt", 'w') as f:
                                    np.savetxt(f, cleantxt, header= "BinNR microsec tot-time (s) O-Beam H-beam AUX chi(pos)", fmt='%i %.2f %.2f %i %i %i %.3f')