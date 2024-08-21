import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Define parameters
a = 2
b = 5
c = 3
C0 = 1  
C1 = 4

# Define the functions R0 and R1
def R0(x):
    return a * x + b

def R1(x):
    return a * x + (b - c)

# Define the ratios with cost for R0 and R1
def ratio_R0(x, k):
    return (R0(x)**k) / (C0**(1 - k))

def ratio_R1(x, k):
    return (R1(x)**k) / (C1**(1 - k))

# Define a range of x values
x = np.linspace(0, 10, 100)

# Slider value for k
k = 0.5  # You can change this value as needed

# Compute the ratios
R0_plot = ratio_R0(x, k)
R1_plot = ratio_R1(x, k)

# Combine data into a DataFrame for ranking
data = pd.DataFrame({
    'x': x,
    'R0': R0_plot,
    'R1': R1_plot,
    'Ratio_R0': ratio_R0(x, k),
    'Ratio_R1': ratio_R1(x, k)
})

# Rank the data based on the ratio for R0 and R1
data['Rank_R0'] = data['Ratio_R0'].rank(ascending=False)
data['Rank_R1'] = data['Ratio_R1'].rank(ascending=False)

# Create a plot
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the ratios
ax.plot(data['x'], data['Ratio_R0'], label='Ratio R0(x)', color='blue')
ax.plot(data['x'], data['Ratio_R1'], label='Ratio R1(x)', color='red')

# Highlight the ranks
scatter_R0 = ax.scatter(data['x'], data['Ratio_R0'], c=data['Rank_R0'], cmap='Blues', label='Rank R0')
scatter_R1 = ax.scatter(data['x'], data['Ratio_R1'], c=data['Rank_R1'], cmap='Reds', label='Rank R1')

# Set axis properties
ax.set_xlabel('x')
ax.set_ylabel('Ratio')
ax.set_title(f'Ratios and Ranking for k={k}')
ax.legend()
ax.grid(True)

# Add colorbar for ranking
cbar = plt.colorbar(scatter_R0, ax=ax, label='Rank for R0')
cbar = plt.colorbar(scatter_R1, ax=ax, label='Rank for R1')

# Show plot
plt.show()
