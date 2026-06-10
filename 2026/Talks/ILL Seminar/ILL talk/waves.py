import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import random

tilt=[0,40,48,61,69,71,79,80,81,77.88,76.76,75.64,74.52]
colors=["#D97A00", "#c32d9b", "#006699"]

x = np.linspace(0, 2*np.pi,1000)

fig = plt.figure(figsize=(16, 0.5))#constrained_layout=True
ax = fig.add_subplot()
for i in [0,1,2]:
    ax.plot(x, np.cos(random.uniform(0.5, 1)*12.5*x+random.uniform(0, 1)*2*np.pi), lw=2, color=colors[i])
for i in range(30):
    ax.plot(random.uniform(0, 1)*2*np.pi, np.cos(random.uniform(0.7, 1)*10*random.uniform(0, 1)*2*np.pi+random.uniform(0, 1)*2*np.pi), "o", color=colors[i%3])
ax.set_xlim([0,2*np.pi])
ax.set_ylim([-1.3,1.3])
ax.axis('off')

# plt.savefig('/home/aaa/Desktop/Fisica/PhD/2026/Talks/ILL Seminar/waves vec1.svg',format='svg', bbox_inches='tight', pad_inches=0, transparent=True)
plt.show()