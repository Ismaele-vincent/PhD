import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Given alpha value
alpha = np.pi / 6  # pi/6
cos_alpha = np.cos(alpha)
sin_alpha = np.sin(alpha)

# Function to solve for a1 given beta
def equation(a1, beta):
    # Trigonometric terms needed for the equation
    cos_alpha_plus_beta_half = np.cos((alpha + beta) / 2)
    cos_beta_half = np.cos(beta / 2)
    sin_beta_half = np.sin(beta / 2)
    
    # Define the variables using the relationships
    a2 = cos_alpha**2 - a1  # Since a2 = cos^2(alpha) - a1
    
    # Calculate b1, c1, d1 terms
    b1 = cos_alpha_plus_beta_half**2 - a1
    c1 = cos_beta_half**2 - a1
    d1 = sin_beta_half**2 - cos_alpha_plus_beta_half**2 + a1
    
    # Calculate b2, c2, d2 terms
    b2 = sin_alpha_plus_beta_half**2 - a2
    c2 = sin_beta_half**2 - a2
    d2 = cos_beta_half**2 - sin_alpha_plus_beta_half**2 + a2
    
    # Equation for sum of b1, c1, d1, a1 = 1
    sum1 = a1 + b1 + c1 + d1 - 1
    
    # Equation for sum of b2, c2, d2, a2 = 1
    sum2 = a2 + b2 + c2 + d2 - 1
    
    # Return both equations (both should be 0 if the system is satisfied)
    return [sum1, sum2]

# Define the range of beta values (for example, from 0 to 2pi)
beta_values = np.linspace(0, 2 * np.pi, 500)

# Solve for a1 for each beta using fsolve (we are using a starting guess of 0.5)
a1_values = []
for beta in beta_values:
    # fsolve returns the solution where the system of equations is satisfied
    a1_solution = fsolve(equation, x0=0.5, args=(beta))  # Initial guess for a1 is 0.5
    a1_values.append(a1_solution[0])

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(beta_values, a1_values, label=r"$a_1(\beta)$", color='b')
plt.title(r"Plot of $a_1$ as a function of $\beta$ for $\alpha = \pi/6$")
plt.xlabel(r"$\beta$")
plt.ylabel(r"$a_1$")
plt.grid(True)
plt.legend()
plt.show()
