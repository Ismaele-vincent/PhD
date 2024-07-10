import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy.special import jv
from matplotlib.gridspec import GridSpec
matplotlib.rcParams['font.size'] = 13
m=1.6749*1e-27 #Kg
mu_N=-9.6623651#*1e-27 J/T
hbar= 6.62607015/(2*np.pi)*1e-34 #J s
 #m/s
phi1=0
phi2=0
order=4

# The parametrized function to be plotted
def alpha(T,f,B):
    w=f*2*np.pi
    return mu_N*B/(hbar*w)*2*np.sin(w*T*1e-3/2)

t = np.linspace(0, 200, 1000)

# Define initial parameters
v0=2060.43*1e-12
k_0=2*np.pi/(2*1e-10) #Gauss
w_0=hbar*k_0**2/(2*m)*1e-12*0
# k_0=2*np.pi/(2*1e-10)*0
print(w_0)
x_0=0
w1_0=2000*2*np.pi*1e-12
t_0=0
alpha_1=np.pi/8
# T_0=19.4 #\mu s
# f1_0=10 #kHz
# B1_0=10 #Gauss
x=0
t=0
# Create the figure and the line that we will manipulate
fig = plt.figure(figsize=(16,9))
ax=fig.add_subplot(111)
# gst = GridSpec(2,3, figure=fig, hspace=0, wspace=0)#,hspace=0, bottom=0,top=0)
# gsb = GridSpec(2,3, figure=fig, hspace=0, wspace=0)
# axs = [fig.add_subplot(gst[:,:-1]),
#        fig.add_subplot(gst[0,-1]),
#        fig.add_subplot(gsb[1,-1])]

x = np.linspace(0, 200, 1000)*1e-2
    
ax.set_xlabel("x")

# adjust the main plot to make room for the sliders
lineO, = ax.plot(x, (np.exp(-1j*(w_0*(t+t_0)-k_0*(x-x_0)-alpha_1*np.sin(w1_0*(t+t_0)-w1_0/v0*x)))).real, "k-", ms=2)
line1, = ax.plot(x, np.exp(-1j*(w_0*(t+t_0)-k_0*(x-x_0))).real, "r--", ms=2)


# Make horizontal sliders.
fig.subplots_adjust(bottom=0.25, left=0.08)
axt = fig.add_axes([0.25, 0.13, 0.5, 0.02])

t_slider = Slider(
    ax=axt,
    label="t",
    valmin=0,
    valmax=1,
    valinit=t_0,
)

fig.subplots_adjust(bottom=0.25, left=0.08)
axx_0 = fig.add_axes([0.25, 0.10, 0.5, 0.02])

x_0_slider = Slider(
    ax=axx_0,
    label="x",
    valmin=0,
    valmax=1e-9,
    valinit=x_0,
)

# The function to be called anytime a slider"s value changes
def update(val):
    lineO.set_ydata((np.exp(-1j*(w_0*(t+t_slider.val)-k_0*(x-x_0_slider.val)-alpha_1*np.sin(w1_0*(t+t_slider.val)-w1_0/v0*(x-x_0_slider.val))))).real)
    line1.set_ydata(np.exp(-1j*(w_0*(t+t_slider.val)-k_0*(x-x_0_slider.val))).real)
    fig.canvas.draw_idle()

# register the update function with each slider
t_slider.on_changed(update)
x_0_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.85, 0.025, 0.1, 0.04])
buttonr = Button(resetax, "Reset", hovercolor="0.975")
def reset(event):
    t_slider.reset()
    x_0_slider.reset()
buttonr.on_clicked(reset)

# setxi = fig.add_axes([0.85, 0.1, 0.1, 0.04])
# buttons = Button(setxi, "Set $\\xi_i=\pi$", hovercolor="0.975")
# def setxi(event):
#     xi1=np.pi
#     xi2=np.pi
#     a1=alpha(T_slider.val, f1_slider.val, B1_slider.val)
#     a2=alpha(T_slider.val, f2_slider.val, B2_slider.val)
#     lineO.set_ydata((1+np.cos(chi_slider.val-a1*np.sin(2*np.pi*f1_slider.val*1e-3*t+xi1)+a2*np.sin(2*np.pi*1e-3*f2_slider.val*t+xi2)))/2)
# buttons.on_clicked(setxi)

plt.show()