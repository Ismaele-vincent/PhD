import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = "/home/aaa/root/fonts/cmunrm.ttf"
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [prop.get_name(), "DejaVu Sans"]
plt.rcParams["font.size"] = 12
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["figure.dpi"] = 150
plt.rcParams["legend.fontsize"] = 11
plt.rcParams["axes.unicode_minus"] = False

# Data
x = np.array([1, 2, 3])
heights = np.array([0,0,1])

colors = [
    "#D97A00",  # burnt orange
    "#c32d9b",  # magenta
    "#006699",  # TU blue
    "#2A9D8F",  # teal
    "#7A8F3A",  # olive green
    "#6A4C93"   # deep violet
]

# Figure
fig, ax = plt.subplots(figsize=(6, 4))

ax.bar(
    x,
    heights,
    width=0.6,
    color="k",
    edgecolor="black"
)
ax.plot(1,0.06, "ok", ms=20, clip_on=False)
ax.plot(2,0.06, "^k", ms=20, clip_on=False)
ax.plot(3,1.08, "Dk", ms=20, clip_on=False)
# Axes
ax.set_xlabel(r'$\lambda_1$', fontsize=14)
ax.set_ylabel(r'$\mu(\lambda)$', fontsize=14)

ax.set_xlim(0.5, 3.5)
ax.set_ylim(0, 1.2)

ax.set_xticks([1, 2, 3])
# ax.set_xticklabels(["circle", "square", "romboid"])

ax.set_yticks([1/3,2/3,1])
ax.set_yticklabels(['1/3','2/3','1'])

# Light horizontal grid
ax.grid(axis='y', color='lightgray', linestyle='-', linewidth=0.8)
ax.set_axisbelow(True)

# Remove top/right frame
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False) 

plt.tight_layout()
plt.show()