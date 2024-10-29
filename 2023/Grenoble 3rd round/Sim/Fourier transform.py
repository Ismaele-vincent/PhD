# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 14:21:47 2023

@author: S18
"""

from scipy.fft import rfft, rfftfreq, fft, fftfreq, dct, dst
import matplotlib.pyplot as plt
import numpy as np

mu_N=-9.6623651#*1e-27 J/T
hbar= 6.62607015/(2*np.pi) #*1e-34 J s
f_1=10
B_1=10
B_0=18.55
T=5
v0=2060.43 #m/s
phi_1=0
order=4
w_ps=3
rad=np.pi/180
alpha_1=-0.2
time=np.linspace(0,420,140)
N=len(time)
T=1/3
x=np.linspace(0.0, N*T, N, endpoint=False)
print(x[-1])
def w1(chi):
    return 1/(1+np.exp(1j*chi)).astype(complex)

def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

def O_beam(t, chi, xi_1):
    return (1+np.cos(chi+alpha_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)))/2

# def O_beam_weak(t, chi, xi_1):
#     A=1/(2*np.cos(chi/2))
#     rho=np.arctan(np.tan(chi/2))
#     return np.cos(chi/2)**2*(1+A**2*alpha_1**2/2-A**2*alpha_1**2/2*np.cos(2*(2*np.pi*1e-3*f_1*t+xi_1))-A*alpha_1*2*np.sin(rho)*np.sin(2*np.pi*1e-3*f_1*t+xi_1))

def O_beam_weak(t, chi, xi_1):
    w_re=w1(chi).real
    w_im=w1(chi).imag
    w_abs=np.abs(w1(chi))
    return np.cos(chi/2)**2*(1+alpha_1**2/2*(w_abs**2-w_re)-alpha_1**2/2*(w_abs**2-w_re)*np.cos(2*(2*np.pi*1e-3*f_1*t+xi_1))+2*alpha_1*w_im*np.sin(2*np.pi*1e-3*f_1*t+xi_1))



chi=np.linspace(-2*np.pi,2*np.pi,22)
Re=np.zeros((len(chi)))
Re_weak=np.zeros((len(chi)))
Im=np.zeros((len(chi)))
Im_weak=np.zeros((len(chi)))
rho=np.zeros((len(chi)))
for i in range(len(chi)):
    func=O_beam(time,chi[i], 0)
    func_weak=O_beam_weak(time,chi[i], 0)
    yf = fft(func)
    yf_weak = fft(func_weak)
    xf = fftfreq(N, T)*100
    print(len(xf), len(yf))
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)
    ax.set_title(str("%.2f"%chi[i],))
    ax.plot(xf, np.abs(yf)/(3*N*T), "k")
    ax.plot(xf, np.abs(yf_weak)/(N*3*T), "r--")
    ax.plot(x,func, "k-")
    ax.plot(x,func_weak, "r--")
    
    # ax.set_xlim([0,40])
    # ax.set_ylim([0,0.005])
    if i==0:
        x_1=xf[2:][yf[2:]==np.amax(yf[2:])]
    a_2=abs((yf[abs(xf-2*x_1)<1/N/6]/N).astype(complex))
    b_1=abs((yf[abs(xf-x_1)<1/N/6]/N).astype(complex))
    a_0=abs((yf[abs(xf)<1/N/6]/N).astype(complex))
    # # Re[i]=1+(0.25-(b_1**2 + 2*a_0*(a_0+2*a_2)**2)/(alpha_1**2*(a_0+2*a_2)**2))**0.5
    Im[i]=b_1/(a_0+2*a_2)
    if i==0:
        x_1=xf[2:][yf_weak[2:]==np.amax(yf_weak[2:])]
    a_2_weak=abs((yf_weak[abs(xf-2*x_1)<1/N/6]/N).astype(complex))
    b_1_weak=abs((yf_weak[abs(xf-x_1)<1/N/6]/N).astype(complex))
    a_0_weak=abs((yf_weak[abs(xf)<1/N/6]/N).astype(complex))
    # print(chi[i], a_2, a_0)
    # Re_weak[i]=1+(0.25-(b_1_weak**2 + 2*a_0_weak*(a_0_weak+2*a_2_weak)**2)/(alpha_1**2*(a_0_weak+2*a_2_weak)**2))**0.5
    Im_weak[i]=b_1_weak/(a_0_weak+2*a_2_weak)
    # # print(np.amax(abs(yf))/N)
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.plot(chi, Im, "k-")
ax.plot(chi, Im_weak, "r--")
# ax.plot(chi, w1(chi).imag,"b--")  
# ax.set_ylim([-10,10])  
# print(chi[A==np.amin(A)], np.pi/2)
plt.show()


