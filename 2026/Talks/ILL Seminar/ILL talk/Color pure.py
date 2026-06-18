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
prob=np.array([0,1])
x = np.array([1, 2])
heights = np.array(prob)

colors = [
    "#D97A00",  # burnt orange
    "#c32d9b",  # magenta
    "#006699",  # TU blue
    "#2A9D8F",  # teal
    "#7A8F3A",  # olive green
    "#6A4C93"   # deep violet
]

# Figure
fig, ax = plt.subplots(figsize=(4, 3.5), dpi=250)

ax.bar(
    x,
    heights,
    width=0.6,
    color="black",
    edgecolor="black"
)
ax.plot(1,prob[0]+0.07, "s", color=colors[1], ms=20, clip_on=False)
ax.plot(2,prob[1]+0.07, "s", color=colors[2], ms=20, clip_on=False)
# ax.plot(3,prob[2]+0.08, "Dk", ms=20, clip_on=False)
# Axes
ax.set_xlabel(r'$\lambda_2$', fontsize=14)
ax.set_ylabel(r'$\mu(\lambda_2|P)$', fontsize=14)

ax.set_xlim(0.5, 2.5)
ax.set_ylim(0, 1)

ax.set_xticks([1, 2])
# ax.set_xticklabels(["circle", "square", "romboid"])

ax.set_yticks([0,1/2,1])
ax.set_yticklabels(['0','0.5','1'])

# Light horizontal grid
ax.grid(axis='y', color='lightgray', linestyle='-', linewidth=0.8)
ax.set_axisbelow(True)

# Remove top/right frame
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False) 
plt.tight_layout()
plt.savefig("/home/aaa/Desktop/Fisica/PhD/2026/Talks/ILL Seminar/Classical pure state color.svg", format="svg", bbox_inches='tight', pad_inches=0, transparent=True)
plt.show()