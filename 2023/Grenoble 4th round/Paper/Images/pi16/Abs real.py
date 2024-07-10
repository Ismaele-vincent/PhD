import os
import numpy as np
import shutil
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq, fft, fftfreq, dct, dst
from mpl_toolkits import mplot3d
from matplotlib.gridspec import GridSpec
plt.rcParams.update({'figure.max_open_warning': 0})
from PIL import Image as im
from scipy.optimize import curve_fit as fit
from scipy.special import jv

def w1(chi, a_21):
    return (1/(1+a_21*np.exp(1j*chi)))
def w2(chi, a_21):
    return 1-w1(chi,a_21)

T_1=0.67
T_2=0.33
a_1=T_1**0.5
a_2=T_2**0.5
a_21=a_2/a_1
alpha=(0.66)**0.5
chi=np.linspace(-2*np.pi, 2*np.pi)

P_1=abs(a_1+a_2*np.exp(1j*chi))**2/2
P_2=abs(a_1*(1-alpha)+a_2*np.exp(1j*chi))**2/2

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.plot(chi,P_1)
ax.plot(chi,P_2)
ax.plot(chi,(P_2-P_1)/P_1/2/alpha, "g")
ax.plot(chi,w1(chi, a_21).real, "r")
ax.set_ylim(-6,1)
