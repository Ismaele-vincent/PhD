#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 10:03:06 2023

@author: aaa
"""
import os
import numpy as np
import shutil

sc_fold_path="D:/data/Cycle 192ter/exp_3-16-14/rawdata/sc/"
for root, dirs, files in os.walk(sc_fold_path, topdown=False):
    for name in files:
        if ("TOF_test_vs_chi" in name) and (".inf" in name):
            print(' "'+name+'", ')
            inf_file_path=os.path.join(root, name)
            inf_file_name=name[:-4]
            sorted_fold_path="C:/Users/S18/Desktop/Grenoble-2023 Ismaele/Grenoble 3rd round/exp_3-16-14/Sorted data/Tests/"+inf_file_name
            
            if not os.path.exists(sorted_fold_path):
                os.makedirs(sorted_fold_path)

            rawdata=sorted_fold_path+"/Rawdata" 
            if not os.path.exists(rawdata):
                os.makedirs(rawdata)

            cleandata=sorted_fold_path+"/Cleantxt"
            if not os.path.exists(cleandata):
                os.makedirs(cleandata)
                

            dat_files = np.genfromtxt(inf_file_path, dtype=str)
            
            if  dat_files[:,-1].astype(float).all()==dat_files[:,-1].astype(float)[0]:
                ps_num=np.array([range(len(dat_files[:,0])), range(len(dat_files[:,0]))])
                dat_files[:,-1]=ps_num[0]
            else:
                ps_num=np.array([range(len(dat_files[:,0])), dat_files[:,-1].astype(float)])
            # print(dat_files)
            # print(ps_num)
            for root, dirs, files in os.walk(sc_fold_path, topdown=False):
                i=0
                for name in files:
                    if (name in dat_files[:,0]):
                        # print(name)
                        shutil.copy(os.path.join(root, name), rawdata+"/"+name)
                        txt=np.loadtxt(os.path.join(root, name), encoding='windows-1252', skiprows=25, comments="*", delimiter="\t")[1:-1,:]
                        ps=dat_files[:,-1][dat_files[:,0]==name].astype(float) #phashifter position
                        # print(ps)
                        cleantxt =np.hstack((txt,np.ones((len(txt[:,0]),1))*ps[0]))
                        # print(cleantxt)
                        with open(cleandata+"/TOF_ps_"+str("%02d" % (ps_num[0][ps_num[1]==ps][0],)[0])+".txt", 'w') as f:
                                np.savetxt(f, cleantxt, header= "BinNR microsec tot-time (s)  O-Beam AUX chi(pos)", fmt='%i %.2f %.2f %i %i %.3f')