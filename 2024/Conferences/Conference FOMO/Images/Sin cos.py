#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 16:26:36 2024

@author: aaa
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 10:41:40 2023

@author: aaa
"""

import numpy as np
import matplotlib.pyplot as plt
colors=["k","#f10d0c","#00a933","#5983b0"]
a_1= 0.2**0.5
a_2= 0.8**0.5
a_21=a_2/a_1
def w1(chi, a_21):
    return 1/(1+a_21*np.exp(1j*chi))

def w2(chi, a_21):
    return 1-w1(chi, a_21)

chi_points=np.array([-np.pi/2,0,np.pi/2])
chi=np.linspace(-2*np.pi,2*np.pi, 500)
fig = plt.figure(figsize=(4,3), dpi=300)
ax = fig.add_subplot(111)
ax.tick_params(axis="y", bottom=False, labelbottom=False, left=False, labelleft=False)
# ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.plot(chi, np.cos(chi+1), "k--", lw=1)
# ax.plot(chi_points[0], np.cos(chi_points[0]+1), "o", colors lw=2)
# ax.plot(chi_points[1], np.cos(chi_points[1]+1), "o", lw=2)
# ax.plot(chi_points[2], np.cos(chi_points[2]+1), "o", lw=2)
ax.set_xlabel("$\\chi_0$")
# ax.set_xticks([0])
# ax.set_xticklabels(["-$\pi/2$", "0", "$\pi/2$"])

ax.set_xticks([-np.pi/2,0,np.pi/2,np.pi])
ax.set_xticklabels(["-$\pi/2$", "0", "$\pi/2$", "$\pi$"])

# ax.plot(chi, np.cos(chi), "k-", lw=5)
# ax.plot(chi, 0*chi, "r-", lw=5)
# ax.plot(chi, np.cos(chi), "k-", lw=5)
ax.grid(True, ls="dotted")
# ax.plot(chi, - a_1*a_2*np.sin(chi)/(1+2*a_1*a_2*np.cos(chi)), "g--")

# ax.set_ylim([-3,3])