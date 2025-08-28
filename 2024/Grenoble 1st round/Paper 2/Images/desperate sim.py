import numpy as np
import matplotlib.pyplot as plt

def plot_feasible_region(angle_degrees):
    # Convert angle to radians
    angle = np.radians(angle_degrees)

    # Create the grid for plotting (increase resolution for better precision)
    x_vals = np.linspace(0, 2*np.pi, 500)  # Increase grid resolution
    y_vals = np.linspace(0, 2*np.pi, 500)
    X, Y = np.meshgrid(x_vals, y_vals)
        
    mu1p=np.cos(X/2)**2
    mu2p=np.cos((X+Y)/2)**2-mu1p
    mu3p=np.cos(Y/2)**2-mu1p
    mu4p=np.sin(Y/2)**2-np.cos((X+Y)/2)**2+mu1p
    
    mu1m=np.cos(X/2)**2-mu1p
    mu2m=np.sin((X+Y)/2)**2-np.cos(X/2)**2+mu1p
    mu3m=np.cos(Y/2)**2-np.cos(X/2)**2+mu1p
    mu4m=np.sin(Y/2)**2-np.cos((X+Y)/2)**2+np.cos(X/2)**2-mu1p
    
    # Define the inequalities based on projections of r on v and w (reversed to >=)
    # in_1 = np.sin((X+Y)/2)**2-np.cos(X/2)**2<np.sin(X/2)**2
    
    in_1 = ((mu1p>=0) & (mu2p>=0) & (mu3p>=0) & (mu4p>=0) & (mu1m>=0) & (mu2m>=0) & (mu3m>=0) & (mu4m>=0))
    in_2 = ((mu1p<=1) & (mu2p<=1) & (mu3p<=1) & (mu4p<=1) & (mu1m<=1) & (mu2m<=1) & (mu3m<=1) & (mu4m<=1))
    in_3 = (mu1p + mu2p + mu3p + mu4p == 1) & (mu1m + mu2m + mu3m + mu4m == 1)
    in_4 = (X+Y < 2*np.pi) & (X-Y>=0)

    # inequality2 = (mu2p>0) + (mu2p<np.sin(X/2)**2)
    # inequality3 = (mu3p>0) + (mu3p<np.sin(X/2)**2)
    # inequality4 = (mu4p>0) + (mu4p<np.cos(X/2)**2)
    # inequality1 = np.sin((Y)/2)**2-np.cos((X+Y)/2)**2>np.cos(X/2)**2
    
    # Combine all inequalities to find the feasible region
    feasible_region = np.cos(Y)>-np.cos(X)
    
    # Plot the feasible region with improved coloring and high resolution
    plt.figure(figsize=(6, 6))
    
    # Plot the feasible region using contourf with better contrast and resolution
    plt.contourf(X, Y, feasible_region, levels=np.linspace(0, 1, 100), cmap='Oranges', alpha=1)
    
    # Plot the unit circle (radius = 1)
    # circle = plt.Circle((0, 0), 1, color='b', fill=False, linestyle='--', linewidth=1.5)
    # plt.gca().add_artist(circle)
    
    # Set axis limits and aspect ratio
    plt.gca().set_aspect('equal', adjustable='box')
    
    # Title and labels
    plt.title(f'Feasible Region for θ = {angle_degrees}°')
    plt.xlabel('$\\alpha$')
    plt.ylabel('$\\beta$')
    
    # Show the plot with grid
    plt.grid(True)
    plt.show()

# Example usage: Plot for different angles between v and w
angle = 45  # You can change this value to test different angles (e.g., 90, 60, 45)
plot_feasible_region(angle)
