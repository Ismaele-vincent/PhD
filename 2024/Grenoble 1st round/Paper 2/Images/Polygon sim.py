import numpy as np
import matplotlib.pyplot as plt

def plot_feasible_region(angle_degrees):
    # Convert angle to radians
    angle = np.radians(angle_degrees)
    
    # Define unit vectors v and w based on the angle between them
    v = np.array([1, 0])  # v = (1, 0)
    w = np.array([np.cos(angle), np.sin(angle)])  # w = (cos(theta), sin(theta))
    
    # Create the grid for plotting (increase resolution for better precision)
    x_vals = np.linspace(-1, 1, 600)  # Increase grid resolution
    y_vals = np.linspace(-1, 1, 600)
    X, Y = np.meshgrid(x_vals, y_vals)
    
    # Calculate the dot products v·r and w·r for each point in the grid
    v_dot_r = v[0] * X + v[1] * Y  # v·r = x (since v = (1,0))
    w_dot_r = w[0] * X + w[1] * Y  # w·r = cos(theta) * x + sin(theta) * y
    
    # Cosine of the angle between v and w
    cos_theta = np.cos(angle)
    
    # Define the inequalities based on projections of r on v and w (reversed to >=)
    inequality1 = v_dot_r + w_dot_r + cos_theta >= -1
    inequality2 = v_dot_r - w_dot_r - cos_theta >= -1
    inequality3 = -v_dot_r + w_dot_r - cos_theta >= -1
    inequality4 = -v_dot_r - w_dot_r + cos_theta >= -1
    
    # Combine all inequalities to find the feasible region
    feasible_region = inequality1 & inequality2 & inequality3 & inequality4
    
    # Plot the feasible region with improved coloring and high resolution
    plt.figure(figsize=(6, 6))
    
    # Plot the feasible region using contourf with better contrast and resolution
    plt.contourf(X, Y, feasible_region, levels=np.linspace(0, 1, 100), cmap='Oranges', alpha=0.7)
    
    # Plot the unit circle (radius = 1)
    circle = plt.Circle((0, 0), 1, color='b', fill=False, linestyle='--', linewidth=1.5)
    plt.gca().add_artist(circle)
    
    # Set axis limits and aspect ratio
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.gca().set_aspect('equal', adjustable='box')
    
    # Title and labels
    plt.title(f'Feasible Region for θ = {angle_degrees}°')
    plt.xlabel('x (projection onto v)')
    plt.ylabel('y (projection onto w)')
    
    # Show the plot with grid
    plt.grid(True)
    plt.show()

# Example usage: Plot for different angles between v and w
angle = 45  # You can change this value to test different angles (e.g., 90, 60, 45)
plot_feasible_region(angle)
