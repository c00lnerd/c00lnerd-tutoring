# -*- coding: utf-8 -*-
"""
Simpson's Rule Integral Plotting
Created on Fri Sep 26 19:15:04 2025

This script plots the integral E(x) = ∫₀ˣ e^(-t²) dt using Simpson's Rule
This integral is related to the error function (erf) in statistics and physics.

@author: MSI Sword
"""

import numpy as np
import matplotlib.pyplot as plt

# Simpson's Rule implementation
def simpsonsrule(f, a, b, steps):
    """
    Compute definite integral using Simpson's Rule
    
    Parameters:
    f: function to integrate
    a: lower limit
    b: upper limit  
    steps: number of steps (must be even)
    
    Returns:
    Approximation of the integral
    """
    if steps % 2 == 1:
        return "Error: n must be even for Simpson's Rule."
    
    h = (b - a) / steps
    x = np.linspace(a, b, steps + 1)
    y = f(x)
    
    # Simpson's Rule formula: (h/3)[y₀ + 4(y₁ + y₃ + ...) + 2(y₂ + y₄ + ...) + yₙ]
    S = y[0] + y[-1] + 4 * np.sum(y[1::2]) + 2 * np.sum(y[2:-1:2])
    return (h / 3) * S

# Function to integrate: e^(-t²)
def f(t):
    """Gaussian function e^(-t²)"""
    return np.exp(-t**2)

# Create range of x values for plotting
x_values = np.linspace(0, 3, 100)  # From 0 to 3 with 100 points
E_values = []

# Calculate E(x) = ∫₀ˣ e^(-t²) dt for each x value
print("Computing integral values...")
for i, x in enumerate(x_values):
    if x == 0:
        E_x = 0  # Integral from 0 to 0 is 0
    else:
        E_x = simpsonsrule(f, 0.0, x, 100)  # 100 steps for accuracy
    E_values.append(E_x)
    
    # Progress indicator
    if (i + 1) % 20 == 0:
        print(f"Completed {i + 1}/{len(x_values)} calculations")

# Convert to numpy array for plotting
E_values = np.array(E_values)

# Create the plot
plt.figure(figsize=(12, 8))

# Main plot: E(x) vs x
plt.subplot(2, 2, 1)
plt.plot(x_values, E_values, "b-", linewidth=2, label="E(x) = ∫₀ˣ e^(-t²) dt")
plt.xlabel("x")
plt.ylabel("E(x)")
plt.title("Integral of e^(-t²) from 0 to x")
plt.grid(True, alpha=0.3)
plt.legend()

# Plot the integrand function
plt.subplot(2, 2, 2)
t_values = np.linspace(0, 3, 200)
plt.plot(t_values, f(t_values), "r-", linewidth=2, label="f(t) = e^(-t²)")
plt.xlabel("t")
plt.ylabel("f(t)")
plt.title("Integrand: e^(-t²)")
plt.grid(True, alpha=0.3)
plt.legend()

# Show area under curve for a specific x value
plt.subplot(2, 2, 3)
x_demo = 2.0
t_fill = np.linspace(0, x_demo, 200)
plt.plot(t_values, f(t_values), "r-", linewidth=2, label="f(t) = e^(-t²)")
plt.fill_between(t_fill, f(t_fill), alpha=0.3, color='blue', 
                label=f"Area = E({x_demo:.1f}) = {simpsonsrule(f, 0, x_demo, 100):.4f}")
plt.xlabel("t")
plt.ylabel("f(t)")
plt.title(f"Area under curve from 0 to {x_demo}")
plt.grid(True, alpha=0.3)
plt.legend()

# Compare with analytical solution (error function)
plt.subplot(2, 2, 4)
from scipy.special import erf
analytical = (np.sqrt(np.pi)/2) * erf(x_values)
plt.plot(x_values, E_values, "b-", linewidth=2, label="Simpson's Rule")
plt.plot(x_values, analytical, "r--", linewidth=2, label="Analytical (erf)")
plt.xlabel("x")
plt.ylabel("E(x)")
plt.title("Comparison: Numerical vs Analytical")
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()

# Print some key values
print("\nKey Results:")
print("x\t\tE(x) (Simpson's)\tE(x) (Analytical)\tError")
print("-" * 60)
for x in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
    simpson_val = simpsonsrule(f, 0, x, 100)
    analytical_val = (np.sqrt(np.pi)/2) * erf(x)
    error = abs(simpson_val - analytical_val)
    print(f"{x:.1f}\t\t{simpson_val:.6f}\t\t{analytical_val:.6f}\t\t{error:.2e}")

print(f"\nNote: E(∞) ≈ √π/2 ≈ {np.sqrt(np.pi)/2:.6f}")
print("This integral is related to the error function: E(x) = (√π/2) × erf(x)")
