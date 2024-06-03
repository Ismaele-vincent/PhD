#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:34:47 2024

@author: aaa
"""

import os
import numpy as np
import shutil
import matplotlib.pyplot as plt

raw_fold_path_off="/home/aaa/Desktop/Fisica/PhD/2024/Niels experiment test/Ismaele/Pole 40 Mezei 1/Mezei Off"
raw_fold_path_on="/home/aaa/Desktop/Fisica/PhD/2024/Niels experiment test/Ismaele/Pole 40 Mezei 1/Mezei On"


for root, dirs, files in os.walk(raw_fold_path_on, topdown=False):
    files=np.sort(files)
    Ipp=np.zeros((2000,3))
    ipp=0
    for name in files:
        if ("up.txt" in name):
            # print('"'+name[:-4]+'", ')
            inf_file_path=os.path.join(root, name)
            # inf_file_name=name[:-4]
            sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Niels experiment test/Sorted data/Pole 40 Mezei 1"
            
            # if not os.path.exists(sorted_fold_path):
            #     os.makedirs(sorted_fold_path)
            
            dat_file = np.loadtxt(os.path.join(root, name), skiprows=2,delimiter=",")
            Ipp[:,:2]+=dat_file[:,:2]
            Ipp[:,2]+=dat_file[:,2]**2
            ipp+=1
Ipp[:,:2]/=ipp
# print(Ipp)
Ipp[:,2]=Ipp[:,2]**0.5/ipp
# print(Ipp)
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.errorbar(Ipp[:,0],Ipp[:,1],yerr=Ipp[:,2])
plt.show()

for root, dirs, files in os.walk(raw_fold_path_on, topdown=False):
    files=np.sort(files)
    Ipm=np.zeros((2000,3))
    ipm=0
    for name in files:
        if ("down.txt" in name):
            # print('"'+name[:-4]+'", ')
            inf_file_path=os.path.join(root, name)
            # inf_file_name=name[:-4]
            sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Niels experiment test/Sorted data/Pole 40 Mezei 1"
            
            # if not os.path.exists(sorted_fold_path):
            #     os.makedirs(sorted_fold_path)
            
            dat_file = np.loadtxt(os.path.join(root, name), skiprows=2,delimiter=",")
            Ipm[:,:2]+=dat_file[:,:2]
            Ipm[:,2]+=dat_file[:,2]**2
            ipm+=1
Ipm[:,:2]/=ipm
# print(Ipm)
Ipm[:,2]=Ipm[:,2]**0.5/ipm
# print(Ipm)
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.errorbar(Ipm[:,0],Ipm[:,1],yerr=Ipm[:,2])
plt.show()

for root, dirs, files in os.walk(raw_fold_path_off, topdown=False):
    files=np.sort(files)
    Imp=np.zeros((2000,3))
    imp=0
    for name in files:
        if ("up.txt" in name):
            # print('"'+name[:-4]+'", ')
            inf_file_path=os.path.join(root, name)
            # inf_file_name=name[:-4]
            sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Niels experiment test/Sorted data/Pole 40 Mezei 1"
            
            # if not os.path.exists(sorted_fold_path):
            #     os.makedirs(sorted_fold_path)
            
            dat_file = np.loadtxt(os.path.join(root, name), skiprows=2,delimiter=",")
            Imp[:,:2]+=dat_file[:,:2]
            Imp[:,2]+=dat_file[:,2]**2
            imp+=1
Imp[:,:2]/=imp
# print(Imp)
Imp[:,2]=Imp[:,2]**0.5/imp
# print(Imp)
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.errorbar(Imp[:,0],Imp[:,1],yerr=Ipm[:,2])
plt.show()

for root, dirs, files in os.walk(raw_fold_path_off, topdown=False):
    files=np.sort(files)
    Imm=np.zeros((2000,3))
    imm=0
    for name in files:
        if ("down.txt" in name):
            # print('"'+name[:-4]+'", ')
            inf_file_path=os.path.join(root, name)
            # inf_file_name=name[:-4]
            sorted_fold_path="/home/aaa/Desktop/Fisica/PhD/2024/Niels experiment test/Sorted data/Pole 40 Mezei 1"
            
            # if not os.path.exists(sorted_fold_path):
            #     os.makedirs(sorted_fold_path)
            
            dat_file = np.loadtxt(os.path.join(root, name), skiprows=2,delimiter=",")
            Imm[:,:2]+=dat_file[:,:2]
            Imm[:,2]+=dat_file[:,2]**2
            imm+=1
Imm[:,:2]/=imm
# print(Imm)
Imm[:,2]=Imm[:,2]**0.5/imm
# print(Imm)
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.errorbar(Imm[:,0],Imm[:,1],yerr=Ipm[:,2])
plt.show()

N=(Ipp[:,1]-Ipm[:,1])
D=(Imp[:,1]-Imm[:,1])
P=N/D
Nerr=(Ipp[:,2]**2+Ipm[:,2]**2)**0.5
Derr=(Imp[:,2]**2+Imm[:,2]**2)**0.5
Perr=abs(P)*(Nerr**2/N**2+Derr**2/D**2)**0.5
print(Perr)
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.errorbar(Imm[:-39,0],P[:-39],yerr=Perr[:-39], fmt=".k")
plt.show()