#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 11:56:53 2023

@author: aaa
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq, fft, fftfreq, dct, dst
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from scipy.optimize import curve_fit as fit
from scipy.stats import norm
from scipy.stats import rayleigh

np.random.seed()

def I(t):
    return 150 +30*np.sin(2*2*np.pi*1e-3*t-0.5)+ 30*np.sin(3*2*np.pi*1e-3*t+1) 

N=120
S_F=16.6667
t= np.linspace(0,N*S_F, N, endpoint=False)
t_plt= np.linspace(0,N*S_F, 1000, endpoint=False)
func=I(t) 
noise= np.random.normal(0, func**0.5)
data= func+noise
fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111)
ax.plot(t_plt, I(t_plt), "r-")
ax.errorbar(t, data, yerr=data**0.5, fmt="k.", capsize=5)

xf = fftfreq(N, S_F)
yf = fft(func)
# fig = plt.figure(figsize=(8,8))
# ax = fig.add_subplot(111)
N_sim=50000
sim_data = np.zeros((N_sim,len(data)), dtype=complex)
var_data = np.zeros(N_sim)
sim_data_0kHz=np.zeros(N_sim,dtype=complex)
sim_data_2kHz=np.zeros(N_sim,dtype=complex)
yf_err=np.zeros((len(data)), dtype=complex)
# fig = plt.figure(figsize=(10,6))
# ax = fig.add_subplot(111)
for i in range(N_sim):
    noise= np.random.normal(0, func**0.5)
    data= func+noise
    yf = fft(data)/N**0.5
    xf = fftfreq(N, S_F)*1e3
    sim_data[i]=yf
    sim_data_0kHz[i]=(yf[abs(xf+2)<1/S_F/2])
    sim_data_2kHz[i]=(yf[abs(xf)<1/S_F/2])
    var_data[i]=(np.average(data/2)**0.5)
    # ax.plot(xf, abs(yf), "ko")
    # yf_err+= fft(data**0.5,norm="forward")
    # ax.plot(t, func, "r-")
    # ax.errorbar(xf, abs(yf), fmt="ko", capsize=5)
    # ax.plot(yf.real,yf.imag, "k.", alpha=0.1)
    ax.set_xlim([-10,10])
# yf_err/=N_sim

def gauss(x,a, b, c):
    return a*norm.pdf(x, scale=b, loc=c)

def gauss_r(x,a, b, c):
    return a*rayleigh.pdf(x, scale=b, loc=c)

var=np.average(var_data)
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
ax.errorbar(sim_data_0kHz.real, sim_data_0kHz.imag, fmt="k.", capsize=5)

hist0kHz=sim_data_0kHz.real
print(np.average(hist0kHz))
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)

(n, bins, patches) = ax.hist((hist0kHz), bins=100, color=(0.5,0.5,0.5), alpha=0.5)
p, cov = fit(gauss, bins[:-1]+(bins[1]-bins[0])/2, n, p0=[np.amax(n), var, np.average(hist0kHz)])
var_plt=np.linspace(p[-1], p[-1]+var, 100) 
var_id=np.linspace(p[-1], p[-1]+p[-2], 100) 
ax.plot(bins[:-1]+(bins[1]-bins[0])/2, gauss(bins[:-1]+(bins[1]-bins[0])/2,*p), "r-", lw=3)
print(var,p[1], var/p[1])

# (n, bins, patches) = ax.hist(np.abs(hist), bins=100, color=(0.5,0.5,0.5), alpha=0.5)
# p, cov = fit(gauss_r, bins[:-1]+(bins[1]-bins[0])/2, n, p0=[np.amax(n), var, 0])
# var_plt=np.linspace(p[-1], p[-1]+var, 100) 
# var_id=np.linspace(p[-1], p[-1]+p[-2], 100) 
# ax.plot(bins[:-1]+(bins[1]-bins[0])/2, gauss_r(bins[:-1]+(bins[1]-bins[0])/2,*p), "r-", lw=3)
# print(var,p[1], var/p[1])



# fig = plt.figure(figsize=(8,6))
# ax = fig.add_subplot(111)
# ax.plot((bins[:-1]+(bins[1]-bins[0])/2)/p[-2], gauss(bins[:-1]+(bins[1]-bins[0])/2,1/p[-2],*p[1:]), "r-", lw=3)
# ax.plot(var_plt/p[-2], var_plt*0+ gauss(p[-1]+var,1/p[-2],*p[1:]), "g-")
# ax.plot(var_id/p[-2], var_id*0+ gauss(p[-1]+p[-2],1/p[-2],*p[1:]), "b--")















# yf_id = fft(func)
# var=np.average(var_data)**0.5
# # ax.errorbar(yf_id.real, yf_id.imag, xerr=var, yerr=var, fmt="ro", capsize=5)
# # ax.set_xlim([6000,7000])
# # ax.set_ylim([-1,1])
# # print(sim_data.real)
# fig = plt.figure(figsize=(8,8))
# ax = fig.add_subplot(111)
# # ax.plot(abs(yf_id))

# # numpy.histogram(a, bins=10, range=None, density=None, weights=None)
# # print(yf_id.imag[yf_id.imag>500], yf_id.real[yf_id.imag>500])
# # # hist=np.ravel(np.abs(yf - yf_id.real[yf_id.imag>500]- 1j*yf_id.imag[yf_id.imag>500]))
# hist0= sim_data - yf_id.real[yf_id.imag>500] - 1j*yf_id.imag[yf_id.imag>500]
# hist0=hist0[abs(hist0)<5*var]
# # hist+= yf_id.real[yf_id.imag>500] + 1j*yf_id.imag[yf_id.imag>500]np.average(np.sum(var_data)**2)**0.5
# # for i in range(N_sim):
# # ax.errorbar(hist.real, hist.imag, fmt="k.", alpha=0.1)
# # ax.errorbar(0, 0, xerr=var, yerr=var,  fmt="ro",  capsize=5)
# # ax.set_xlim([-500,500])
# # ax.set_ylim([-500,500])

# fig = plt.figure(figsize=(8,6))
# ax = fig.add_subplot(111)
# # ax.hist(np.abs(hist), bins="auto")
# (n, bins, patches) = ax.hist(np.abs(hist0), bins=100, color=(0.5,0.5,0.5), alpha=0.5)

# p, cov = fit(gauss_r, bins[:-1]+(bins[1]-bins[0])/2, n, p0=[np.amax(n), var, 0])
# var_plt=np.linspace(p[-1], p[-1]+var, 100) 
# var_id=np.linspace(p[-1], p[-1]+p[-2], 100) 
# ax.plot(bins[:-1]+(bins[1]-bins[0])/2, gauss_r(bins[:-1]+(bins[1]-bins[0])/2,*p), "r-", lw=3)

# fig = plt.figure(figsize=(8,6))
# ax = fig.add_subplot(111)
# ax.plot((bins[:-1]+(bins[1]-bins[0])/2)/p[-2], gauss(bins[:-1]+(bins[1]-bins[0])/2,1/p[-2],*p[1:]), "r-", lw=3)
# ax.plot(var_plt/p[-2], var_plt*0+ gauss(p[-1]+var,1/p[-2],*p[1:]), "g-")
# ax.plot(var_id/p[-2], var_id*0+ gauss(p[-1]+p[-2],1/p[-2],*p[1:]), "b--")
# plt.show()
# print(p[-2], var)

# yf_id = fft(func)
# var=np.average(var_data)
# # ax.errorbar(yf_id.real, yf_id.imag, xerr=var, yerr=var, fmt="ro", capsize=5)
# # ax.set_xlim([6000,7000])
# # ax.set_ylim([-1,1])
# # print(sim_data.real)

# # numpy.histogram(a, bins=10, range=None, density=None, weights=None)
# # print(yf_id.imag[yf_id.imag>500], yf_id.real[yf_id.imag>500])
# # hist=np.ravel(np.abs(yf - yf_id.real[yf_id.imag>500]- 1j*yf_id.imag[yf_id.imag>500]))
# hist= sim_data - yf_id.real[yf_id.imag==0]
# hist=hist[abs(hist)<5*var]
# # hist+= yf_id.real[yf_id.imag>500] + 1j*yf_id.imag[yf_id.imag>500]
# # for i in range(N_sim):
# # fig = plt.figure(figsize=(8,8))
# # ax = fig.add_subplot(111)
# # ax.errorbar(hist.real, hist.imag, fmt="k.", alpha=0.1)
# # ax.errorbar(0, 0, xerr=var, yerr=var,  fmt="ro",  capsize=5)
# # ax.set_xlim([-500,500])
# # ax.set_ylim([-500,500])

# fig = plt.figure(figsize=(8,6))
# ax = fig.add_subplot(111)
# # ax.hist(np.abs(hist), bins="auto")
# (n, bins, patches) = ax.hist(hist.real, bins=100, color=(0.5,0.5,0.5), alpha=0.5)
# p, cov = fit(gauss, bins[:-1]+(bins[1]-bins[0])/2, n, p0=[np.amax(n), var,0])
# var_plt=np.linspace(p[-1], p[-1]+var, 100) 
# var_id=np.linspace(p[-1], p[-1]+p[-2], 100) 
# ax.plot(bins[:-1]+(bins[1]-bins[0])/2, gauss(bins[:-1]+(bins[1]-bins[0])/2,*p), "r-", lw=3)

# fig = plt.figure(figsize=(8,6))
# ax = fig.add_subplot(111)
# ax.plot((bins[:-1]+(bins[1]-bins[0])/2)/p[-2], gauss(bins[:-1]+(bins[1]-bins[0])/2,1/p[-2],*p[1:]), "r-", lw=3)
# ax.plot(var_plt/p[-2], var_plt*0+ gauss(p[-1]+var,1/p[-2],*p[1:]), "g-")
# ax.plot(var_id/p[-2], var_id*0+ gauss(p[-1]+p[-2],1/p[-2],*p[1:]), "b--")
# plt.show()
# print(p[-2], var)
plt.show()



