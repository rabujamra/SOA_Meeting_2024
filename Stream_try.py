import streamlit as st
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

# Streamlit app
st.title('Interactive Plot for Ranking Scenario')

# Slider for k value
k = st.slider('Select value of k', min_value=0.0, max_value=1.0, value=0.5, step=0.01)

# Define a range of x values
x = np.linspace(0, 10, 100)

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
scatter_R0 = ax.scatter(data['x'], data['Ratio_R0'], c=data['Rank_R0'], cmap='Blues', label='Rank R0', alpha=0.6)
scatter_R1 = ax.scatter(data['x'], data['Ratio_R1'], c=data['Rank_R1'], cmap='Reds', label='Rank R1', alpha=0.6)

# Set axis properties
ax.set_xlabel('x')
ax.set_ylabel('Ratio')
ax.set_title(f'Ratios and Ranking for k={k}')
ax.legend()
ax.grid(True)

# Add colorbar for ranking
cbar = plt.colorbar(scatter_R0, ax=ax, label='Rank for R0')
cbar = plt.colorbar(scatter_R1, ax=ax, label='Rank for R1')

# Show plot in Streamlit
st.pyplot(fig)
