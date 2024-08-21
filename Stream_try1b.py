import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Define parameters
a, b, c = 2, 5, 3
C0, C1 = 1, 4

# Define the functions R0 and R1
def R0(x):
    return a * x + (b - c)

def R1(x):
    return 1.2 * R0(x)

# Define the ratio function
def ratio(R, C, k):
    return (R**k) / (C**(1 - k))

# Define a combined nonlinear modification function for ratios
def modified_ratio_combined(x, R_func, C, k, beta, ratio_min, ratio_max):
    base_ratio = ratio(R_func(x), C, k)
    log_mod = np.log1p((base_ratio - ratio_min) / (ratio_max - ratio_min))
    return base_ratio**(1 + beta * log_mod)

# Streamlit app
st.title('Interactive Plot for R0 and R1 Ratios with Nonlinear Modification')

# Sliders for k and beta values
k = st.slider('Select value of k', min_value=0.0, max_value=1.0, value=0.5, step=0.01)
beta = st.slider('Select value of beta', min_value=0.0, max_value=2.0, value=0.5, step=0.01)

# Define a range of x values
x = np.linspace(1, 10, 10)

# Calculate ratio_min and ratio_max
R0_ratios = ratio(R0(x), C0, k)
R1_ratios = ratio(R1(x), C1, k)
ratio_min = min(R0_ratios.min(), R1_ratios.min())
ratio_max = max(R0_ratios.max(), R1_ratios.max())

# Compute the modified ratios
R0_plot = modified_ratio_combined(x, R0, C0, k, beta, ratio_min, ratio_max)
R1_plot = modified_ratio_combined(x, R1, C1, k, beta, ratio_min, ratio_max)

# Create a plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, R0_plot, label=f'R0(x) (modified ratio)', color='blue')
ax.plot(x, R1_plot, label=f'R1(x) (modified ratio)', color='red')

# Set axis properties
ax.set_xlabel('x')
ax.set_ylabel('Modified Ratio')
ax.set_title(f'Modified Ratios for k={k}, beta={beta}')
ax.legend()
ax.grid(True)

# Show plot in Streamlit
st.pyplot(fig)

# Add a section to show the crossover point
crossover_x = x[np.argmin(np.abs(R1_plot - R0_plot))]
st.write(f"Approximate crossover point: x = {crossover_x:.2f}")

# Calculate and display ratios for the current k value
st.subheader(f"Ratios for k = {k:.2f}")

# Compute and display the modified ratios
delta = R1_plot - R0_plot
table_data = {
    'x': x,
    'Treated (R1)': R1_plot,
    'Untreated (R0)': R0_plot,
    'Delta (Treated - Untreated)': delta
}

st.write(pd.DataFrame(table_data))
