#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 12:39:07 2024

@author: aaa
"""
"""
pi/16
"""

Cb=0.7456183532707045
Cu=0.7472042106925748#0.6098097265142495
Cb_err=0.00646151528318766
Cu_err=0.005485104794295868#0.006398877289498047


print(Cu/Cb, "+-", ((Cu_err/Cb)**2+(Cu*Cb_err/Cb**2)**2)**0.5)

"""
pi/8
"""