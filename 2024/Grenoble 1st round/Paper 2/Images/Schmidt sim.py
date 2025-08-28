import numpy as np
import matplotlib.pyplot as plt

def plot_feasible_region(angle_degrees):
    # Convert angle to radians
    angle = np.radians(angle_degrees)
    # Define unit vectors v and w based on the angle between them
    v = np.array([np.cos(angle/2), -np.sin(angle/2)])  # v = (1, 0)
    w = np.array([np.cos(angle/2), np.sin(angle/2)])  # w = (cos(theta), sin(theta))
    # Create the grid for plotting (increase resolution for better precision)
    x_vals = np.linspace(-1, 1, 600)  # Increase grid resolution
    y_vals = np.linspace(-1, 1, 600)
    X, Y = np.meshgrid(x_vals, y_vals)
    r_1 = np.array([X,Y])
    r_1_ang=-np.arctan(Y/X)
    r_1_amp=(X**2+Y**2)**0.5
    r_2 = -r_1
    # r_3 = np.array([r_1_amp*np.cos(r_1_ang-angle),r_1_amp*np.sin(r_1_ang-angle)])
    r_3 = np.array([r_1_amp*np.sin(r_1_ang+angle),r_1_amp*np.cos(r_1_ang+angle)])
    # r_3 = np.array([Y, X])
    r_4 = -r_3
    # Calculate the dot products v·r and w·r for each point in the grid
    v_dot_r1 = v[0] * r_1[0] + v[1] * r_1[1]  # v·r = x (since v = (1,0))
    w_dot_r1 = w[0] * r_1[0] + w[1] * r_1[1]  # w·r = cos(theta) * x + sin(theta) * y
    v_dot_r2 = v[0] * r_2[0] + v[1] * r_2[1]  
    w_dot_r2 = w[0] * r_2[0] + w[1] * r_2[1] 
    v_dot_r3 = v[0] * r_3[0] + v[1] * r_3[1]  
    w_dot_r3 = w[0] * r_3[0] + w[1] * r_3[1] 
    v_dot_r4 = v[0] * r_4[0] + v[1] * r_4[1]  
    w_dot_r4 = w[0] * r_4[0] + w[1] * r_4[1] 
        
    # Cosine of the angle between v and w    
    P11 = (1+v_dot_r1)/2
    P12 = (1+v_dot_r2)/2
    P13 = (1+v_dot_r3)/2
    P14 = (1+v_dot_r4)/2
    P21 = (1+w_dot_r1)/2
    P22 = (1+w_dot_r2)/2
    P23 = (1+w_dot_r3)/2
    P24 = (1+w_dot_r4)/2
    
    # Define the inequalities based on projections of r on v and w 
    In_1 = P12+P22-P23-P14 <= 1
    In_2 = P12+P22-P13-P24 <= 1
    In_3 = P22+P13-P12-P24 <= 1
    In_4 = P12+P23-P22-P14 <= 1
    In_5 = P22+P14-P12-P23 <= 1
    In_6 = P23+P14-P12-P22 <= 1
    In_7 = P12+P24-P22-P13 <= 1
    In_8 = P13+P24-P12-P22 <= 1
    
    # Combine all inequalities to find the feasible region
    feasible_region = In_1 & In_2 & In_3 & In_4 & In_5 & In_6 & In_7 & In_8
    
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
