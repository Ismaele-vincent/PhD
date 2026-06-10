import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import font_manager

font_path = "/home/aaa/root/fonts/cmunrm.ttf"
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [prop.get_name(), "DejaVu Sans"]  # <- DejaVu als Fallback
plt.rcParams["font.size"] = 12
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["figure.dpi"] = 150
# plt.rcParams["legend.markerscale"] = 1
plt.rcParams["legend.fontsize"] = 11
plt.rcParams["axes.unicode_minus"] = False  # <- richtige Variante!

# Create figure
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Positions of the bars
x = np.array([1, 2, 1])
y = np.array([1, 2, 3])
z = np.zeros(3)

# Dimensions of the bars
dx = np.full(3, 0.6)
dy = np.full(3, 0.6)
dz = np.array([2/10, 5/10, 3/10])


# Colors
colors = [
    "#D97A00",  # burnt orange
    "#c32d9b",  # magenta
    "#006699",  # TU blue
    # "#2A9D8F",  # teal
    # "#7A8F3A",  # olive green
    # "#6A4C93"   # deep violet
]

# Draw bars
ax.bar3d(x - dx/2, y - dy/2, z,
         dx, dy, dz,
         color=colors,
         edgecolor='black',
         shade=True)

# # Remove background
# ax.set_frame_on(False)

# Draw grid lines on z=0 plane
for xg in [1.5, 2.5]:
    ax.plot([xg, xg], [0.5, 3.5], [0, 0],
            color='lightgray', linewidth=1)

for yg in [1.5, 2.5, 3.5]:
    ax.plot([0.5, 2.5], [yg, yg], [0, 0],
            color='lightgray', linewidth=1)

# Remove pane backgrounds
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
# ax.zaxis.pane.fill = False

# Remove pane edges
ax.xaxis.pane.set_edgecolor((1, 1, 1, 0))
ax.yaxis.pane.set_edgecolor((1, 1, 1, 0))
# ax.zaxis.pane.set_edgecolor((1, 1, 1, 0))

# # Remove grid
# ax.grid(False)

# Axis labels
ax.set_xlabel(r'$\lambda_1$', fontsize=14, labelpad=10)
ax.set_ylabel(r'$\lambda_2$', fontsize=14, labelpad=10)
ax.text(0.2,3,1.1,r'$\mu(\lambda)$', fontsize=14)
# ax.zaxis.set_label_coords(2.05, -0.025)
# ax.set_box_aspect(None, zoom=0.85)
# Axis limits
ax.set_xlim(0.5, 2.5)
ax.set_ylim(0.5, 3.5)
ax.set_zlim(0, 1)

# Ticks
ax.set_xticks([1, 2])
ax.set_xticklabels(["circle", "square"])
ax.set_yticks([1, 2, 3])
ax.set_yticklabels(["orange", "purple", "blue"])
ax.set_zticks([1])
ax.set_zticklabels(['1'])

# ax.set_zticks([1/3, 2/3, 1])
# ax.set_zticklabels([r'$1/3$', r'$2/3$', '1'])

ax.grid(False)

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
# ax.zaxis.pane.fill = False

# ax.yaxis.set_ticks_position('lower')

ax.xaxis.pane.set_edgecolor('w')
# ax.yaxis.pane.set_edgecolor('w')
# ax.zaxis.pane.set_edgecolor('w')

# Viewing angle
ax.view_init(elev=20, azim=220)
# plt.tight_layout()
plt.show()