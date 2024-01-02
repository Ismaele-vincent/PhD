import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy.special import jv
from matplotlib.gridspec import GridSpec
matplotlib.rcParams['font.size'] = 9

mu_N=-9.6623651#*1e-27 J/T
hbar= 6.62607015/(2*np.pi) #*1e-34 J s
v0=2060.43 #m/s
phi1=1
phi2=0.3
order=4
# Define initial parameters
T_0=5 #\mu s
f_1=10 #kHz
B1_0=2 #Gauss
xi1_0=np.pi#phi1+(2*np.pi*f_1*1e-3*T_0+np.pi)/2-2*np.pi*f_1*1e3/v0
chi_0=np.pi/4

def w1(chi):
    return 1/(1+np.exp(1j*chi)).astype(complex)


# The parametrized function to be plotted
def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

def O_beam(t, chi, a_1, xi_1):
    return (1+np.cos(chi+a_1*np.sin(2*np.pi*1e-3*f_1*t+xi_1)))/2

# def O_beam_weak(t, chi, a_1, xi_1):
#     A=1/(2*np.cos(chi/2))
#     rho=np.arctan(np.tan(chi/2))
#     return np.cos(chi/2)**2*(1+A**2*a_1**2/2-A**2*a_1**2/2*np.cos(2*(2*np.pi*1e-3*f_1*t+xi_1))-A*a_1*2*np.sin(rho)*np.sin(2*np.pi*1e-3*f_1*t+xi_1))

def O_beam_weak(t, chi, alpha_1, xi_1):
    w_re=w1(chi).real
    w_im=w1(chi).imag
    w_abs=np.abs(w1(chi))
    return np.cos(chi/2)**2*(1+alpha_1**2/2*(w_abs**2-w_re)-alpha_1**2/2*(w_abs**2-w_re)*np.cos(2*(2*np.pi*1e-3*f_1*t+xi_1))+2*alpha_1*w_im*np.sin(2*np.pi*1e-3*f_1*t+xi_1))


t = np.linspace(0, 401, 500)

a1_0=alpha(T_0,f_1, B1_0)

# Create the figure and the line that we will manipulate
fig = plt.figure(figsize=(12,9))
title=fig.suptitle("$\\alpha1=$"+str("%.3f"%(alpha(T_0, f_1, B1_0),)))
gst = GridSpec(2,3, figure=fig, hspace=0, wspace=0)#,hspace=0, bottom=0,top=0)
gsb = GridSpec(2,3, figure=fig, hspace=0, wspace=0)
axs = [fig.add_subplot(gst[:,:-1]),
       fig.add_subplot(gst[:,-1])]
for ax in axs[1:]:
    ax.yaxis.set_tick_params(labelleft=False)
    ax.yaxis.set_label_position("right")
    
axs[0].set_xlabel("Time ($\mu$s)")
axs[0].set_ylabel("$I_o$")
axs[0].set_ylim([-0.1,1.1])
axs[0].set_yticks(np.linspace(0,1,10))

# adjust the main plot to make room for the sliders
lineO, = axs[0].plot(t,O_beam(t, chi_0, a1_0, xi1_0), "k--", ms=2, label="O Beam")
line1, = axs[0].plot(t,O_beam_weak(t, chi_0, a1_0, xi1_0), "r-", ms=2, label="O Beam $\\alpha<<1$")
axs[0].legend()
axs[1].set_xlabel("Order")
axs[1].set_ylabel("$J_n^2$ Path1")
rects1=axs[1].bar(range(-order, order+1), jv(range(-order, order+1), alpha(T_0, f_1, B1_0))**2)
texts1=[]
for i in range(-order,order+1):
    text=axs[1].text(i, jv(i, alpha(T_0, f_1, B1_0))**2, str("%.3f" %(jv(i, alpha(T_0, f_1, B1_0))**2),),ha="center", va="bottom")
    texts1.append(text)
axs[1].set_xticks(range(-order, order+1))
axs[1].set_ylim([0,1.1])    

# Make horizontal sliders.
fig.subplots_adjust(bottom=0.25, left=0.08)
axa1 = fig.add_axes([0.25, 0.13, 0.5, 0.02])
axchi = fig.add_axes([0.01, 0.25, 0.02, 0.5])

a1_slider = Slider(
    ax=axa1,
    label="$a_1$",
    valmin=-3,
    valmax=0,
    valinit=a1_0,
)


chi_slider = Slider(
    ax=axchi,
    label="$\chi$",
    valmin=-np.pi,
    valmax=np.pi,
    valinit=chi_0,
    orientation="vertical"
)

# The function to be called anytime a slider"s value changes
def update(val):
    lineO.set_ydata(O_beam(t, chi_slider.val, a1_slider.val, xi1_0))
    line1.set_ydata(O_beam_weak(t, chi_slider.val, a1_slider.val, xi1_0),)
    for rect, h in zip(rects1, jv(range(-order, order+1), a1_slider.val)**2):
        rect.set_height(h)
    for text,i in zip(texts1,range(-order,order+1)):
        text.set_text(str("%.3f" %(jv(i, a1_slider.val)**2),))
        text.set_y((jv(i, a1_slider.val)**2))  
        # axs[0].relim()
        # axs[0].autoscale_view()
    fig.canvas.draw_idle()

# register the update function with each slider
a1_slider.on_changed(update)
chi_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.85, 0.025, 0.1, 0.04])
buttonr = Button(resetax, "Reset", hovercolor="0.975")
def reset(event):
    a1_slider.reset()
    chi_slider.reset()
buttonr.on_clicked(reset)

setxi = fig.add_axes([0.85, 0.1, 0.1, 0.04])
buttons = Button(setxi, "Set $\\xi_i=\pi$", hovercolor="0.975")
def setxi(event):
    xi1=np.pi
    lineO.set_ydata((1+np.cos(chi_slider.val+a1_slider.val*np.sin(2*np.pi*f_1*1e-3*t+xi1)))/2)
buttons.on_clicked(setxi)

plt.show()
