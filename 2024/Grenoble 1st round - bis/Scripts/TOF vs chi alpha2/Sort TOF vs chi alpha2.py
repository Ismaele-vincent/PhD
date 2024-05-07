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

sc_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round - bis/exp_CRG-3126/rawdata/sc"
bad_apples=["TOF_vs_chi_alpha2_22pt_Bessel_0_2kHz_900s_04Apr2354","TOF_vs_chi_alpha2_22pt_pi16_1200s_29Mar1500", "TOF_vs_chi_alpha2_22pt_pi16_1200s_29Mar1500", "TOF_vs_chi_alpha2_22pt_Bessel_0_2kHz_900s_ps_m0.2_07Apr1248","TOF_vs_chi_alpha2_22pt_Bessel_0_2kHz_1200s_07Apr1903"]

for root, dirs, files in os.walk(sc_fold_path, topdown=False):
    for name1 in files:
        if ("TOF_vs_chi_alpha2_" in name1)  and ("Bessel_0" in name1) and (".inf" in name1) and (name1 not in bad_apples):
            if (name1[:-4] in bad_apples):
                print('bad "'+name1[:-4]+'", ')
            else:
                print('inf_file_name="'+name1[:-4]+'"')
                inf_file_path=os.path.join(root, name1)
                inf_file_name=name1[:-4]
                sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Grenoble 1st round - bis/exp_CRG-3126/Sorted data/TOF vs chi alpha2/"+inf_file_name
                
                if not os.path.exists(sorted_fold_path):
                    os.makedirs(sorted_fold_path)
    
                rawdata=sorted_fold_path+"/Rawdata" 
                if not os.path.exists(rawdata):
                    os.makedirs(rawdata)
    
                cleandata=sorted_fold_path+"/Cleantxt"
                if not os.path.exists(cleandata):
                    os.makedirs(cleandata)
                    
                dat_files = np.genfromtxt(inf_file_path, dtype=str)
                
                ps_num=np.array([range(len(dat_files[:,0])), dat_files[:,-1].astype(float)])
                # print(dat_files[:,0])
                # print(ps_num)
                for root, dirs, files in os.walk(sc_fold_path, topdown=False):
                    i=0
                    for name in files:
                        if (name in dat_files[:,0]):
                            # print(name)
                            shutil.copy(os.path.join(root, name), rawdata+"/"+name)
                            txt=np.loadtxt(os.path.join(root, name), encoding='windows-1252', comments="*", delimiter="\t")[:,:]
                            ps=dat_files[:,-1][dat_files[:,0]==name].astype(float) #phashifter position
                            func_gen=dat_files[:,-4:-1][dat_files[:,0]==name].astype(float)
                            # print(func_gen)
                            # print(ps)
                            cleantxt =np.hstack((txt,np.ones((len(txt[:,0]),3))*func_gen,np.ones((len(txt[:,0]),1))*ps[0]))
                            # print(cleantxt)
                            with open(cleandata+"/TOF_ps_"+str("%02d" % (ps_num[0][ps_num[1]==ps][0],)[0])+".txt", 'w') as f:
                                    np.savetxt(f, cleantxt, header= "BinNR microsec tot-time (s)  O-Beam H-beam AUX Ampl(V) f(Hz) phase(deg) chi(pos)", fmt='%i %.2f %.2f %i %i %i %.3f %.3f %.3f %.3f')