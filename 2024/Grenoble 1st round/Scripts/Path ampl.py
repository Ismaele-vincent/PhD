#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 14:51:31 2024

@author: aaa
"""
a=63441
b=27549
R=b/a
DR=(b**2/a**3+b/a**2)**0.5
print("R=",R)
P1=63441
DP1=P1**0.5
P2=63441*R
DP2=(R**2*P2+P2**2*DR**2)**0.5
T_1=P1/(P1+P2)
DT_1=(P1+T_1**2*(P1+P2))**0.5/(P1+P2)
T_2=1-T_1
DT_2=DT_1
print("T_1=", T_1,"+-", DT_1)
print("T_2=", T_2,"+-", DT_2)
a_1=T_1**0.5
Da_1=DT_1/a_1 
a_2=T_2**0.5
Da_2=DT_2/a_2
print("a_1=", a_1,"+-", Da_1)
print("a_2=", a_2,"+-", Da_2)