"""
bad apples:
"TOF_S2_alpha_ifg_07Sep2027",
"TOF_S2_alpha_ifg_08Sep0110", 
"TOF_S2_alpha_ifg_08Sep1006",
"""
import os
import numpy as np
import shutil

sc_fold_path="D:/data/Cycle 198/exp_3-16-19/rawdata/sc"
bad_apples=[]

for root1, dirs1, files1 in os.walk(sc_fold_path, topdown=False):
    for name1 in files1:
        if ("ifg1_newPS_2p30s_AP" in name1) and (".sc" in name1):
            file_path1=os.path.join(root1, name1)
            with open(file_path1, 'r') as src:
                lines_ifg1 = src.readlines()
            
           
        if ("ifg2_newPS_2p30s_AP" in name1) and (".sc" in name1):
            if (name1[:-4] in bad_apples):
                print('bad "'+name1+'", ')
            else:
                print('"'+name1+'", ')
                file_path2=os.path.join(root1, name1)
                with open(file_path2, 'r') as src:
                    lines_ifg2 = src.readlines()
                
                    print(lines_ifg2[4])
                
                
with open("D:/data/Cycle 198/exp_3-16-19/rawdata/sc/ifg12_newPS_2p30s_AP.sc", 'w') as dest:
    dest.writelines(lines_ifg1[0:2])
    dest.writelines(lines_ifg2[1:3])
    for i in range(len(lines_ifg1[4:-1])):
        if i%2:
            dest.writelines(lines_ifg1[3+i])
        dest.writelines(lines_ifg2[3+i])
    dest.writelines(lines_ifg2[-2:])

# with open("D:/data/Cycle 198/exp_3-16-19/rawdata/sc/ifg12_newPS_2p30s_AP.sc", 'w') as dest:
#     dest.writelines(lines_ifg1[0])
#     dest.writelines(lines_ifg1[-4])
#     dest.writelines(lines_ifg2[1:3])
#     for i in range(len(lines_ifg1[4:-1])):
#         if i%2:
#             dest.writelines(lines_ifg1[-3-i])
#         dest.writelines(lines_ifg2[3+i])
#     dest.writelines(lines_ifg2[-2:])