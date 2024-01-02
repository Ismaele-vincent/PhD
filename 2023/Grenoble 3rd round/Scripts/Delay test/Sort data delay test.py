#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 10:03:06 2023

@author: aaa
"""
"""
"TOF_A1_06Sep1225.inf", 
"TOF_A1_06Sep1402.inf", 
"TOF_A1_06Sep1528.inf", 
"TOF_A1_06Sep1801.inf", 
"TOF_S2+A1_06Sep1245.inf", 
"TOF_S2+A1_06Sep1422.inf", 
"TOF_S2+A1_06Sep1548.inf", 
"TOF_S2+A1_06Sep1733.inf", 
"TOF_S2+A1_06Sep1734.inf", 
"TOF_S2+A1_06Sep1737.inf", 
"TOF_S2+A1_06Sep1742.inf", 
"TOF_S2+A1_06Sep1743.inf", 
"TOF_S2_06Sep1117.inf", 
"TOF_S2_06Sep1129.inf", 
"TOF_S2_06Sep1132.inf", 
"TOF_S2_06Sep1134.inf", 
"TOF_S2_06Sep1137.inf", 
"TOF_S2_06Sep1205.inf", 
"TOF_S2_06Sep1342.inf", 
"TOF_S2_06Sep1508.inf", 
"TOF_S2_06Sep1729.inf", 
"TOF_S2_06Sep1731.inf", 
"TOF_S2_06Sep1739.inf", 
"TOF_S2_06Sep1827.inf", 
"""
import os
import numpy as np
import shutil

inf_file_names=["TOF_S2_delay_07Sep1539.inf", "TOF_A1_delay_07Sep1529.inf", ]

sc_fold_path="D:/data/Cycle 192ter/exp_3-16-14/rawdata/sc/"
for root, dirs, files in os.walk(sc_fold_path, topdown=False):
    for name in files:
        
        if name in inf_file_names:
            # print('"'+name+'", ')
            inf_file_path=os.path.join(root, name)
            inf_file_name=name[:-4]
            sorted_fold_path="C:/Users/S18/Desktop/Grenoble-2023 Ismaele/Grenoble 3rd round/exp_3-16-14/Sorted data/Delay tests/"+inf_file_name
            
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
            # print(ps_num)
            for root, dirs, files in os.walk(sc_fold_path, topdown=False):
                i=0
                for name1 in files:
                    if (name1 in dat_files[0]):
                        if ("_S2+A1_" in name1):
                            shutil.copy(os.path.join(root, name1), rawdata+"/"+name1)
                            txt=np.loadtxt(os.path.join(root, name1), encoding='windows-1252', comments="*", delimiter="\t")[:,:]
                            ps=dat_files[2].astype(float) #phashifter position
                            func_gen=dat_files[-6:][dat_files[0]==name1].astype(float)
                            # print(func_gen)
                            # cleantxt =np.hstack((txt,np.ones((len(txt[:,0]),6))*func_gen,np.ones((len(txt[:,0]),1))*ps[0]))
                            # # print(cleantxt)
                            # with open(cleandata+"/TOF_ps_"+str("%02d" % (ps_num[0][ps_num[1]==ps][0],)[0])+".txt", 'w') as f:
                            #         np.savetxt(f, cleantxt, header= "BinNR microsec tot-time (s)  O-Beam AUX Ampl_1(V) f_1(Hz) phase_1(deg) Ampl_2(V) f_2(Hz) phase_2(deg) chi(pos)", fmt='%i %.2f %.2f %i %i %.3f %.3f %.3f %.3f %.3f %.3f %.3f')
                        if ("_S2_" in name1):
                            shutil.copy(os.path.join(root, name1), rawdata+"/"+name1)
                            txt=np.loadtxt(os.path.join(root, name1), encoding='windows-1252', comments="*", delimiter="\t")[:,:]
                            ps=dat_files[2].astype(float) #phashifter position
                            func_gen=dat_files[-4:][dat_files[0]==name1].astype(float)
                            # print(name,func_gen)
                            cleantxt =np.hstack((txt,np.ones((len(txt[:,0]),4))*func_gen))
                            # print(cleantxt)
                            with open(cleandata+"/TOF.txt", 'w') as f:
                                    np.savetxt(f, cleantxt, header= "BinNR microsec tot-time (s)  O-Beam AUX Ampl_1(V) f_1(Hz) phase_1(deg) Ampl_2(V) f_2(Hz) phase_2(deg) chi(pos)", fmt='%i %.2f %.2f %i %i %.3f %.3f %.3f %.3f')
                        if ("_A1_" in name):
                            shutil.copy(os.path.join(root, name1), rawdata+"/"+name1)
                            txt=np.loadtxt(os.path.join(root, name1), encoding='windows-1252', comments="*", delimiter="\t")[:,:]
                            ps=dat_files[2].astype(float) #phashifter position
                            func_gen=dat_files[-4:][dat_files[0]==name1].astype(float)
                            # print(name,func_gen)
                            cleantxt =np.hstack((txt,np.ones((len(txt[:,0]),4))*func_gen))
                            # # print(cleantxt)
                            with open(cleandata+"/TOF.txt", 'w') as f:
                                    np.savetxt(f, cleantxt, header= "BinNR microsec tot-time (s)  O-Beam AUX Ampl_1(V) f_1(Hz) phase_1(deg) Ampl_2(V) f_2(Hz) phase_2(deg) chi(pos)", fmt='%i %.2f %.2f %i %i %.3f %.3f %.3f %.3f')