#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:08:44 2024

@author: aaa
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.patches as patches
# import plotly

th= np.pi/4
a_2= np.sin(th/2)
a_1= np.cos(th/2)
# a_1= 1/5**0.5
# a_2= 2/5**0.5
# a_1= 0.51**0.5
# a_2= 0.49**0.5
# a_1= 0.5**0.5
# a_2= 0.5**0.5
a_21=a_2/a_1

def wp1_Re(chi,a_2):
    a_1 = abs(1-a_2**2)**0.5
    return (a_1/(a_1+a_2*np.exp(1j*chi))).real
    # return (a_1**2+a_1*a_2*np.cos(chi))/(1+2*a_1*a_2*np.cos(chi))

def wm1_Re(chi,a_2):
    a_1 = abs(1-a_2**2)**0.5
    return (a_1/(a_1-a_2*np.exp(1j*chi))).real

def wp2_Re(chi, a_1):
    return (1-wp1_Re(chi,a_1)).real

def wm2_Re(chi, a_1):
    return (1-wm1_Re(chi,a_1)).real

def wp1_Im(chi,a_1):
    a_2 = abs(1-a_1**2)**0.5
    return (a_1/(a_1+a_2*np.exp(1j*chi))).imag
    # return (a_1**2+a_1*a_2*np.cos(chi))/(1+2*a_1*a_2*np.cos(chi))

def wm1_Im(chi,a_1):
    a_2 = abs(1-a_1**2)**0.5
    return (a_1/(a_1-a_2*np.exp(1j*chi))).imag

def wp2_Im(chi, a_1):
    return (1-wp1_Im(chi,a_1)).imag

def wm2_Im(chi, a_1):
    return (1-wm1_Im(chi,a_1)).imag

def wp1(chi):
    # return (1/(1+a_21*np.exp(1j*chi)))
    return (a_1/(a_1+a_2*np.exp(1j*chi)))

def wp2(chi):
    return (1-wp1(chi))

def wm1(chi):
    return (1/(1-a_21*np.exp(1j*chi)))

def wm2(chi):
    return (1-wm1(chi))



a_1_plt=np.linspace(0,1,200)
chi_plt=np.linspace(-np.pi,np.pi, 100)
chi_plt_1=np.linspace(-2*np.pi,2*np.pi, 100)
circle = patches.Circle((0, 0), 1, edgecolor='blue', facecolor='none')

X, Y = np.meshgrid(chi_plt, a_1_plt)
X_1, Y = np.meshgrid(chi_plt_1, a_1_plt)
Zp = wp1_Re(X,Y)
Zm = wm1_Re(X,Y)

Zcos = 2*(Y**2*(1-Y**2))**0.5*np.cos(X)/4
# print(wp1(chi_plt,a_1_plt).real)
levels = np.linspace(-10, 0, 400)
levels1 = np.linspace(1, 10, 400)
# levels = np.linspace(0, 1, 100)
# levels1 = np.linspace(0, 1, 400)
fig = plt.figure(figsize=(6,6), dpi=200)
ax = fig.add_subplot(111)
# ax.add_patch(circle)
# ax.contourf(X, Y, Zm, levels=levels)
# ax.contourf(X, Y, Zm, levels=levels1)
# ax.contourf(X, Y, Zp, levels=levels)
# ax.contourf(X, Y, Zp, levels=levels1)
ax.contourf(2*(Y**2*(1-Y**2))**0.5*np.cos(X_1), (2*Y**2-1), Zm, levels=levels)
ax.contourf(2*(Y**2*(1-Y**2))**0.5*np.cos(X_1), (2*Y**2-1), Zm, levels=levels1)
ax.contourf(2*(Y**2*(1-Y**2))**0.5*np.cos(X), (2*Y**2-1), Zp, levels=levels)
ax.contourf(2*(Y**2*(1-Y**2))**0.5*np.cos(X), (2*Y**2-1), Zp, levels=levels1)
ax.set_xlabel("$\sigma_x$")
ax.set_ylabel("$\sigma_z$")
# ax.set_xlim([-1,1])
# ax.set_ylim([-1,1])
# ax.set_aspect('equal', adjustable='box')

# fig = plt.figure(figsize=(6,6), dpi=200)
# ax = fig.add_subplot(111)
# ax.contourf(2*(Y**2*(1-Y**2))**0.5*np.sin(X), (2*Y**2-1), Zm, levels=levels)
# ax.contourf(2*(Y**2*(1-Y**2))**0.5*np.sin(X), (2*Y**2-1), Zm, levels=levels1)
# ax.contourf(2*(Y**2*(1-Y**2))**0.5*np.sin(X), (2*Y**2-1), Zp, levels=levels)
# ax.contourf(2*(Y**2*(1-Y**2))**0.5*np.sin(X), (2*Y**2-1), Zp, levels=levels1)
# ax.set_xlabel("$\sigma_y$")
# ax.set_ylabel("$\sigma_z$")
# ax.set_xlim([-1,1])
# ax.set_ylim([-1,1])
# ax.set_aspect('equal', adjustable='box')

# fig = plt.figure(figsize=(6,6), dpi=200)
# ax = fig.add_subplot(111)
# ax.contourf(2*(Y**2*(1-Y**2))**0.5*np.cos(X), 2*(Y**2*(1-Y**2))**0.5*np.sin(X), Zm, levels=levels)
# ax.contourf(2*(Y**2*(1-Y**2))**0.5*np.cos(X), 2*(Y**2*(1-Y**2))**0.5*np.sin(X), Zm, levels=levels1)
# ax.contourf(2*(Y**2*(1-Y**2))**0.5*np.cos(X), 2*(Y**2*(1-Y**2))**0.5*np.sin(X), Zp, levels=levels)
# ax.contourf(2*(Y**2*(1-Y**2))**0.5*np.cos(X), 2*(Y**2*(1-Y**2))**0.5*np.sin(X), Zp, levels=levels1)
# ax.set_xlabel("$\sigma_x$")
# ax.set_ylabel("$\sigma_y$")
# ax.set_xlim([-1,1])
# ax.set_ylim([-1,1])
# ax.set_aspect('equal', adjustable='box')


# X, Y = np.meshgrid(chi_plt, a_1_plt)
# Zp = wp1_Im(X,Y)
# Zm = wm1_Im(X,Y)
# # print(wp1(chi_plt,a_1_plt).real)
# levels = np.linspace(-5, 5, 10)
# fig = plt.figure(figsize=(8,6), dpi=200)
# ax = fig.add_subplot(111)
# ax.contourf(X, Y**2, Zm, levels=levels)
# # ax.contourf(X, Y**2, Zp, levels=levels)
# ax.set_xlabel("$\chi$")

# X, Y = np.meshgrid(chi_plt, a_1_plt)
# Zp = wp2_Re(X,Y)
# Zm = wm2_Re(X,Y)
# # print(wp1(chi_plt,a_1_plt).real)
# levels = np.linspace(-9, 0, 10)
# levels1 = np.linspace(1, 10, 10)
# levels2 = np.linspace(-1, 1, 2)
# fig = plt.figure(figsize=(8,6), dpi=200)
# ax = fig.add_subplot(111)
# ax.contourf(X, Y**2, Zm, levels=levels)
# ax.contourf(X, Y**2, Zm, levels=levels1)
# ax.contourf(X, Y**2, Zp, levels=levels)
# ax.contourf(X, Y**2, Zp, levels=levels1)
# ax.contourf(X, Y**2, Zp*0+np.cos(chi_plt)**2, levels=levels1)
# ax.set_xlabel("$\chi$")
# ax.set_ylabel("$a_1^2$")


# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# ax.view_init(10, 45)
# ax.plot_wireframe(X, Y**2, Zp, rstride=200, cstride=50)
# ax.plot_wireframe(X, Y**2, Zm, rstride=200, cstride=50, color="r")
# ax.set_zlim([-10,10])
# plt.show()