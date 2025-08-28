import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator,FormatStrFormatter)

colors = ["k", "#f10d0c", "#00a933", "#5983b0"]

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(projection='3d')

# Fake data
x = np.arange(4) + 0.5
y = np.arange(4) + 0.5
X, Y = np.meshgrid(x, y)
x, y = X.ravel(), Y.ravel()

top = x * 0 + y * 0
top[5] = 1
bottom = np.zeros_like(top)
width = depth = 1

# Plot a single bar
# ax.bar3d(x, y, bottom, width, depth, bottom, shade=False, facecolor="w", edgecolor="k", zorder=2)
ax.bar3d(x[5], y[5], bottom[5], width, depth, top[5], shade=True, color=colors[3], zorder=1)
# Major ticks every 20, minor ticks every 5
major_ticks = np.arange(5)
minor_ticks = np.arange(5)
ax.set_xticks(major_ticks)
ax.set_yticks(major_ticks)
ax.set_xticklabels(minor_ticks)
ax.set_yticklabels(minor_ticks)
ax.set_xlim([0.5, 4.5])
ax.set_ylim([0.5, 4.5])
ax.set_zlim([0, 1])
ax.set_xlabel("$\lambda_1$")
ax.set_ylabel("$\lambda_2$")
ax.set_zlabel("$\\mu_\Lambda$")

# Enable grid only on minor ticks (half-integer positions)
ax.grid(True)  # Disable grid for major ticks
# Show the plot
plt.show()




# set up the figure and Axes
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(projection='3d', proj_type='ortho')

# fake data
x = np.arange(4)+0.5
y = np.arange(4)+0.5
X,Y = np.meshgrid(x, y)
x, y = X.ravel(), Y.ravel()

index=[1,5,7,9,10,13,14,15]
indexm=[0,2,3,4,6,8,11,12]
top = x*0+y*0
top[index]=0
bottom = np.zeros_like(top)
width = depth = 1
top1=top
# ax.set_facecolor('white')
# ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
# ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

ax.bar3d(x[indexm], y[indexm], bottom[indexm], width, depth, top1[indexm], shade=False, edgecolor='black', color=colors[2])
ax.bar3d(x[index], y[index], bottom[index], width, depth, top[index], shade=False, edgecolor='black', color=colors[1])
# ax.zaxis.set_ticks('none')
# ax.set_title('Shaded')
ax.set_xticks(np.arange(5) + 0.5)  # Shift X-axis grid lines by 0.5
ax.set_yticks(np.arange(5) + 0.5)  # Shift Y-axis grid lines by 0.5

# Enable grid and apply the shifted grid lines
ax.grid(False, which='both', axis='both')

# Keep the original ticks (if you don't want them shifted)
ax.set_xticks(np.arange(5))  # Original X-tick positions
ax.set_yticks(np.arange(5))  # Original Y-tick positions

ax.set_xlim([0.5,4.5])
ax.set_ylim([0.5,4.5])
ax.set_zlim([0,1])
ax.view_init(elev=90, azim=0, roll=90)
ax.zaxis.set_ticks([])              # Remove z-axis ticks
ax.zaxis.set_ticklabels([])         # Remove z-axis tick labels
ax.zaxis.line.set_color((0, 0, 0, 0))  # Hide z-axis line (make transparent)
ax.zaxis.pane.set_visible(False)    # Hide z-axis background pane
ax.grid(False)  
ax.set_xlabel("$\lambda_1$")
ax.set_ylabel("$\lambda_2$")
plt.show()
