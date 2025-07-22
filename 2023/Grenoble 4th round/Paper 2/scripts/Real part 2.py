import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d


# Define the grid of x and y values
theta = np.linspace(0, 2 * np.pi, 400)
phi = np.linspace(0, 2*np.pi, 400)
X, Y = np.meshgrid(theta, phi)

# Compute the expression
Z_px = 0.5*(1 + np.cos(X) + np.sin(X) * np.cos(Y))/(1 + np.sin(X) * np.cos(Y))
Z_mx = 0.5*(1 + np.cos(X) - np.sin(X) * np.cos(Y))/(1 - np.sin(X) * np.cos(Y))
Z_py = 0.5*(1 + np.cos(X) + np.sin(X) * np.cos(Y))/(1 + np.sin(X) * np.cos(Y))
Z_my = 0.5*(1 + np.cos(X) - np.sin(X) * np.cos(Y))/(1 - np.sin(X) * np.cos(Y))



ax = plt.figure(figsize=(8, 8)).add_subplot()

# Create the plot


# Plot the region where Z_px < 0 in one color (lightcoral)
ax.contourf(X, Y, Z_px, levels=[-np.inf, 0], colors=['lightcoral'], alpha=0.7)
ax.contourf(X, Y, Z_px, levels=[1, np.inf], colors=['lightgreen'], alpha=0.7)
ax.contourf(X, Y, Z_mx, levels=[-np.inf, 0], colors=['lightblue'], alpha=0.7)
ax.contourf(X, Y, Z_mx, levels=[1, np.inf], colors=['lightyellow'], alpha=0.7)
ax.contour(X, Y, Z_px, cmap=cm.coolwarm)
# Plot the region where Z_px >= 0 in another color (lightgreen)
# ax.contourf(X, Y, Z_px, levels=[0, 1], colors=['lightgreen'], alpha=0.5)

# Add the boundary line where the expression equals zero
contours = [ax.contour(X, Y, Z_px, levels=[0], colors='black', linewidths=1),
ax.contour(X, Y, Z_px, levels=[1], colors='black', linewidths=1),
ax.contour(X, Y, Z_mx, levels=[0], colors='black', linewidths=1),
ax.contour(X, Y, Z_mx, levels=[1], colors='black', linewidths=1)]

x_coords = []
y_coords = []
for contour in contours:
    contour_paths = contour.collections[0].get_paths()
    
    # Extract the coordinates from the paths
    for path in contour_paths:
        vertices = path.vertices
        x_coords.extend(vertices[:, 0])  # x-coordinates
        y_coords.extend(vertices[:, 1])  # y-coordinates
    print(vertices[:, 0])
    # Convert to numpy arrays if needed
x_coords = np.array(x_coords)
y_coords = np.array(y_coords)

y_coords = y_coords[abs(x_coords-np.pi)>1e-4]
x_coords = x_coords[abs(x_coords-np.pi)>1e-4]
# for path in contour_paths:
#     vertices = path.vertices
# print(vertices)

ax.plot(np.cos(x_coords),np.sin(x_coords)*np.cos(y_coords), color='blue', label=r'$x = \cos(y)$', linewidth=2)


# Plot formatting
# ax.title(r'Region where $\Re(w) < 0, \ \Re(w) > 1 $')
ax.set_xlabel('x')
ax.set_ylabel('y')
# ax.set_axhline(0, color='gray', linewidth=0.5)
# ax.set_axvline(0, color='gray', linewidth=0.5)
ax.grid(True, linestyle='--', alpha=0.3)
ax.set_xlim([0,2*np.pi])
ax.set_ylim([0,2*np.pi])
# ax.aspect('equal', adjustable='box')
# ax.tight_layout()

ax = plt.figure(figsize=(8, 8)).add_subplot(projection='3d')
ax.view_init(45, 70)
# ax.set_xlim([1,1])
# ax.set_ylim([1,1])
# ax.set_zlim([1,1])
x_cube=np.linspace(-1,1,500)
y_cube=np.linspace(-1,1,500)
X_c, Y_c = np.meshgrid(x_cube, y_cube)
Z_c=(1-abs(X_c))
ax.plot(np.sin(x_coords)*np.cos(y_coords), np.sin(x_coords)*np.sin(y_coords), np.cos(x_coords), linewidth=2)
ax.plot_surface(X_c, Y_c, Z_c, color='lightcoral', alpha=0.4)
ax.plot_surface(X_c, Y_c, -Z_c, color='lightcoral', alpha=0.4)
ax.plot_surface(np.sin(X)*np.cos(Y), np.sin(X)*np.sin(Y), np.cos(X), color='lightblue', alpha=0.1)


ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
