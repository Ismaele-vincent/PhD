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


pi=np.pi
np.random.seed(12345)

N=133
S_F=3
t= np.linspace(0,N*S_F, N, endpoint=False)
func= 50 + 20*np.sin(2*pi*10e-3*t)# + 30*np.sin(15*2*np.pi*t) 
noise= np.random.normal(0, func**0.5)
data= func+noise
# fig = plt.figure(figsize=(10,6))
# ax = fig.add_subplot(111)
# ax.plot(t, func, "r-")
# ax.errorbar(t, data, yerr=data**0.5, fmt="ko", capsize=5)

xf = fftfreq(N, S_F)
yf = fft(func)
# fig = plt.figure(figsize=(8,8))
# ax = fig.add_subplot(111)
N_sim=100000
sim_data = np.zeros((N_sim,len(data)), dtype=complex)
var_data = np.zeros(N_sim)
yf_err=np.zeros((len(data)), dtype=complex)
for i in range(N_sim):
    noise= np.random.normal(0, func**0.5)
    data= func+noise
    yf = fft(data)
    sim_data[i]=yf
    var_data[i]=sum(abs(data))**0.5
    # ax.plot(xf, abs(yf), "ko")
    # yf_err+= fft(data**0.5,norm="forward")
    # ax.plot(t, func, "r-")
    # ax.errorbar(xf, abs(yf), fmt="ko", capsize=5)
    # ax.plot(yf.real,yf.imag, "k.", alpha=0.1)
    # ax.set_xlim([-20,20])
# yf_err/=N_sim

def gauss(x,a, b, c):
    return a*norm.pdf(x, scale=b, loc=c)

def gauss_r(x,a, b, c):
    return x*a*norm.pdf(x, scale=b, loc=c)


yf_id = fft(func)
var=np.average(var_data)
# ax.errorbar(yf_id.real, yf_id.imag, xerr=var, yerr=var, fmt="ro", capsize=5)
# ax.set_ylim([1830.76873077,730.76873077])
# ax.set_xlim([-541,469])

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
# ax.plot(abs(yf_id))

# numpy.histogram(a, bins=10, range=None, density=None, weights=None)
print(yf_id.imag[yf_id.imag>500], yf_id.real[yf_id.imag>500])
# hist=np.ravel(np.abs(yf - yf_id.real[yf_id.imag>500]- 1j*yf_id.imag[yf_id.imag>500]))
hist= sim_data - yf_id.real[yf_id.imag>500] - 1j*yf_id.imag[yf_id.imag>500]
hist=hist[abs(hist)<5*var]
# hist+= yf_id.real[yf_id.imag>500] + 1j*yf_id.imag[yf_id.imag>500]
# for i in range(N_sim):
ax.errorbar(0, 0, xerr=var, yerr=var,  fmt="ro",  capsize=5)
ax.plot(hist.real, hist.imag, "k.", alpha=0.1)
ax.set_xlim([-500,500])
ax.set_ylim([-500,500])


fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
# ax.hist(np.abs(hist), bins="auto")
(n, bins, patches) = ax.hist(np.abs(hist), bins=100, color=(0.5,0.5,0.5), alpha=0.5)

p, cov = fit(gauss_r, bins[:-1]+(bins[1]-bins[0])/2, n, p0=[np.amax(n), bins[len(bins)//2],var])
var_plt=np.linspace(p[-1], p[-1]+var, 100) 
var_id=np.linspace(p[-1], p[-1]+p[-2], 100) 
ax.plot(bins[:-1]+(bins[1]-bins[0])/2, gauss_r(bins[:-1]+(bins[1]-bins[0])/2,*p), "r-", lw=3)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.plot((bins[:-1]+(bins[1]-bins[0])/2)/p[-2], gauss(bins[:-1]+(bins[1]-bins[0])/2,1/p[-2],*p[1:]), "r-", lw=3)
ax.plot(var_plt/p[-2], var_plt*0+ gauss(p[-1]+var,1/p[-2],*p[1:]), "g-")
ax.plot(var_id/p[-2], var_id*0+ gauss(p[-1]+p[-2],1/p[-2],*p[1:]), "b--")
plt.show()
print(p[-2], var)


"""
"""
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fft import rfft, rfftfreq, fft, fftfreq, dct, dst
# from matplotlib.gridspec import GridSpec
# plt.rcParams.update({'figure.max_open_warning': 0})
# from scipy.optimize import curve_fit as fit
# from scipy.stats import norm

# def gauss(x,a, b, c):
#     return a*norm.pdf(x, scale=b, loc=c)
# x_plt=np.linspace(-4, 4)

# fig = plt.figure(figsize=(8,6))
# ax = fig.add_subplot(111)
# ax.plot(x_plt, gauss(x_plt, 1, 1,0), "g-", lw=3)
# plt.show()




