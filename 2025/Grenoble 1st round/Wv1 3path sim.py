import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy.special import jv
from matplotlib.gridspec import GridSpec
matplotlib.rcParams['font.size'] = 13

def wv_1(a1, a2, a3, chi2, chi3):
    if a1<1e-6:
        wv_1=0
    else:
        wv_1=a1/(a1+a2*np.exp(1j*chi2)+a3*np.exp(1j*chi3))
    return wv_1

def wv_2(a1, a2, a3, chi2, chi3):
    if a2<1e-6:
        wv_2=0
    else:
        wv_2=a2*np.exp(1j*chi2)/(a1+a2*np.exp(1j*chi2)+a3*np.exp(1j*chi3))
    return wv_2

def wv_3(a1, a2, a3, chi2, chi3):
    if a3<1e-6:
        wv_3=0
    else:
        wv_3=a3*np.exp(1j*chi3)/(a1+a2*np.exp(1j*chi2)+a3*np.exp(1j*chi3))
    return wv_3

# The parametrized function to be plotted


chi2 = np.linspace(-2*np.pi, 2*np.pi, 1000)

# Define initial parameters

a1_0=1/3**0.5
chi2_0=0 #Gauss
a2_0=1/3**0.5
chi3_0=0
a3_0=(1-a1_0**2-a2_0**2)**0.5

# Create the figure and the line that we will manipulate
fig = plt.figure(figsize=(16,9))
title=fig.suptitle("$a_3=$"+str("%.3f"%(a3_0,)))
gst = GridSpec(2,4, figure=fig, hspace=0)#, wspace=0)#,hspace=0, bottom=0,top=0)
gsb = GridSpec(2,4, figure=fig, hspace=0)#, wspace=0)
axs = [fig.add_subplot(gst[0,0]),
       fig.add_subplot(gst[1,0]),
       fig.add_subplot(gsb[0,1]),
       fig.add_subplot(gsb[1,1]),
       fig.add_subplot(gsb[0,2]),
       fig.add_subplot(gsb[1,2]),
       fig.add_subplot(gsb[-1,-1])]

for ax in axs[:-1]:
    ax.grid(True, ls="dotted")
    ax.set_xticks([-2*np.pi, -3/2*np.pi, -np.pi, -np.pi/2,0,np.pi/2,np.pi,3/2*np.pi,2*np.pi])
    ax.set_xticklabels(["$\mathdefault{-2\pi}$","$\mathdefault{-\\frac{3\pi}{2}}$", "$\mathdefault{-\pi}$","$\mathdefault{-\\frac{\pi}{2}}$", "$\mathdefault{0}$", "$\mathdefault{\\frac{\pi}{2}}$", "$\mathdefault{\pi}$", "$\mathdefault{\\frac{3\pi}{2}}$", "$\mathdefault{2\pi}$"])
    ax.set_xlabel("$\\chi_2$")
axs[-1].yaxis.set_tick_params(labelleft=False)
axs[-1].yaxis.set_label_position("right")
axs[-1].grid(True, ls="dotted")   
axs[0].set_ylabel("Real part")
axs[1].set_ylabel("Imaginary part")
# adjust the main plot to make room for the sliders
line0, = axs[0].plot(chi2, wv_1(a1_0, a2_0, a3_0, chi2, chi3_0).real, "k-", ms=2)
line1, = axs[1].plot(chi2, wv_1(a1_0, a2_0, a3_0, chi2, chi3_0).imag, "r-", ms=2)

line2, = axs[2].plot(chi2, wv_2(a1_0, a2_0, a3_0, chi2, chi3_0).real, "k-", ms=2)
line3, = axs[3].plot(chi2, wv_2(a1_0, a2_0, a3_0, chi2, chi3_0).imag, "r-", ms=2)

line4, = axs[4].plot(chi2, wv_3(a1_0, a2_0, a3_0, chi2, chi3_0).real, "k-", ms=2)
line5, = axs[5].plot(chi2, wv_3(a1_0, a2_0, a3_0, chi2, chi3_0).imag, "r-", ms=2)

rects1=axs[-1].bar([1,2,3], (a1_0**2, a2_0**2, a3_0**2))
texts1=[]
a_vec_0=[a1_0**2, a2_0**2, a3_0**2]
for i in [0,1,2]:
    text=axs[-1].text(i+1, a_vec_0[i], str("%.3f" %(a_vec_0[i],)),ha="center", va="bottom")
    texts1.append(text)
axs[-1].set_xlabel([1, 2, 3])
axs[-1].set_ylim([0,1.1])    

axs[-1].set_xlabel("Path")
axs[-1].set_ylabel("Path transmission (${a_i}^2$)")

# Make horizontal sliders.
fig.subplots_adjust(bottom=0.25, left=0.08)
axa1 = fig.add_axes([0.25, 0.13, 0.5, 0.02])
axa2 = fig.add_axes([0.25, 0.10, 0.5, 0.02])
# axchi2 = fig.add_axes([0.25, 0.07, 0.5, 0.02])
axchi3 = fig.add_axes([0.25, 0.04, 0.5, 0.02])

a1_slider = Slider(
    ax=axa1,
    label="$a_1$ (kHz)",
    valmin=0,
    valmax=1,
    valinit=a1_0,
)

a2_slider = Slider(
    ax=axa2,
    label="$a_2$ (kHz)",
    valmin=0,
    valmax=1,
    valinit=a2_0,
)

# a3_slider = Slider(
#     ax=axa3,
#     label="$a_3$ (kHz)",
#     valmin=0,
#     valmax=1,
#     valinit=a3_0,
# )


# chi2_slider = Slider(
#     ax=axchi2,
#     label="$B_1$ (Gauss)",
#     valmin=0,
#     valmax=60,
#     valinit=chi2_0,
#     # orientation="vertical"
# )


chi3_slider = Slider(
    ax=axchi3,
    label="$\\chi_3$",
    valmin=0,
    valmax=2*np.pi,
    valinit=chi3_0,
    # orientation="vertical"
)

# # The function to be called anytime a slider"s value changes
def update(val):
    if (a1_slider.val**2+a2_slider.val**2>1 and a1_slider.val>a2_slider.val):
        a2=(1-a1_slider.val**2)**0.5
        a2_slider.set_val(a2)
        a3=0
    elif (a1_slider.val**2+a2_slider.val**2>1 and a1_slider.val>a2_slider.val):
        a1=(1-a2_slider.val**2)**0.5
        a1_slider.set_val(a1)
        a3=0
    else: 
        a1=a1_slider.val
        a2=a2_slider.val
        a3=(1-a1**2-a2**2)**0.5
    a_vec=[a1**2, a2**2, a3**2]
    chi3=chi3_slider.val
    line0.set_ydata(wv_1(a1, a2, a3, chi2, chi3).real)
    line1.set_ydata(wv_1(a1, a2, a3, chi2, chi3).imag)
    line2.set_ydata(wv_2(a1, a2, a3, chi2, chi3).real)
    line3.set_ydata(wv_2(a1, a2, a3, chi2, chi3).imag)
    line4.set_ydata(wv_3(a1, a2, a3, chi2, chi3).real)
    line5.set_ydata(wv_3(a1, a2, a3, chi2, chi3).imag)
    for ax in axs[:-1]:
        ax.relim()
        ax.autoscale_view()
    # line0.set_ylim([(wv_1(a1, a2, a3, chi2, chi3).real).min*(1-0.1),(wv_1(a1, a2, a3, chi2, chi3).real).max*(1+0.1)])
    for rect, h in zip(rects1, a_vec):
        rect.set_height(h)
    for text,i in zip(texts1,[0,1,2]):
        text.set_text(str("%.3f" %(a_vec[i]),))
        text.set_y((a_vec[i]))
        
    fig.canvas.draw_idle()

# register the update function with each slider
a1_slider.on_changed(update)
a2_slider.on_changed(update)
# chi2_slider.on_changed(update)
chi3_slider.on_changed(update)


# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.85, 0.025, 0.1, 0.04])
buttonr = Button(resetax, "Reset", hovercolor="0.975")
def reset(event):
    a1_slider.reset()
    a2_slider.reset()
    # chi2_slider.reset()
    chi3_slider.reset()

buttonr.on_clicked(reset)

setchi3 = fig.add_axes([0.85, 0.1, 0.1, 0.04])
buttons = Button(setchi3, "Set $\\chi_3=\pi/2$", hovercolor="0.975")
def setchi3(event):
    chi3=np.pi/2
    chi3_slider.set_val(chi3)
    a1=a1_slider.val
    a2=a2_slider.val
    a3=(1-a1**2-a2**2)**0.5
    line0.set_ydata(wv_1(a1, a2, a3, chi2, chi3).real)
    line1.set_ydata(wv_1(a1, a2, a3, chi2, chi3).imag)
    line2.set_ydata(wv_2(a1, a2, a3, chi2, chi3).real)
    line3.set_ydata(wv_2(a1, a2, a3, chi2, chi3).imag)
    line4.set_ydata(wv_3(a1, a2, a3, chi2, chi3).real)
    line5.set_ydata(wv_3(a1, a2, a3, chi2, chi3).imag)
    a_vec=[a1**2, a2**2, a3**2]
    for ax in axs[:-1]:
        ax.relim()
        ax.autoscale_view()
    # line0.set_ylim([(wv_1(a1, a2, a3, chi2, chi3).real).min*(1-0.1),(wv_1(a1, a2, a3, chi2, chi3).real).max*(1+0.1)])
    for rect, h in zip(rects1, a_vec):
        rect.set_height(h)
    for text,i in zip(texts1,[0,1,2]):
        text.set_text(str("%.3f" %(a_vec[i]),))
        text.set_y((a_vec[i]))
        
    fig.canvas.draw_idle()
buttons.on_clicked(setchi3)

plt.show()