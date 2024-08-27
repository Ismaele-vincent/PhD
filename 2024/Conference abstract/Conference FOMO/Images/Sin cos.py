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

a_1= 0.2**0.5
a_2= 0.8**0.5
a_21=a_2/a_1
def w1(chi, a_21):
    return 1/(1+a_21*np.exp(1j*chi))

def w2(chi, a_21):
    return 1-w1(chi, a_21)

chi=np.linspace(-2*np.pi,2*np.pi, 50)
fig = plt.figure(figsize=(3,3), dpi=150)
ax = fig.add_subplot(111)
ax.tick_params(axis="both", bottom=False, labelbottom=False, left=False, labelleft=False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
# ax.plot(chi, -np.cos(chi), "k-", lw=5)
# ax.plot(chi, np.cos(chi), "k-", lw=5)
ax.plot(chi, 0*chi, "r-", lw=5)
# ax.plot(chi, np.cos(chi), "k-", lw=5)
ax.grid(True, ls="dotted")
# ax.plot(chi, - a_1*a_2*np.sin(chi)/(1+2*a_1*a_2*np.cos(chi)), "g--")

# ax.set_ylim([-3,3])