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

# Define the nonlinear modification function for ratios
def nonlinear_mod(ratio, ratio_min, ratio_max, alpha):
    return ratio**(1 + alpha * (ratio - ratio_min) / (ratio_max - ratio_min))

# Define the ratios with cost for R0 and R1, including nonlinear modification
def modified_ratio(x, R_func, C, k, alpha, ratio_min, ratio_max):
    R = R_func(x)
    base_ratio = ratio(R, C, k)
    return nonlinear_mod(base_ratio, ratio_min, ratio_max, alpha)

# Streamlit app
st.title('Interactive Plot for R0 and R1 Ratios with Nonlinear Modification')

# Sliders for k and alpha values
k = st.slider('Select value of k', min_value=0.0, max_value=1.0, value=0.5, step=0.01)
alpha = st.slider('Select value of alpha', min_value=0.0, max_value=2.0, value=0.5, step=0.01)

# Define a range of x values
x = np.arange(0, 10.1, 0.1)  # Use .1 increment

# Calculate ratio_min and ratio_max
R0_ratios = ratio(R0(x), C0, k)
R1_ratios = ratio(R1(x), C1, k)
ratio_min = min(R0_ratios.min(), R1_ratios.min())
ratio_max = max(R0_ratios.max(), R1_ratios.max())

# Compute the modified ratios
R0_plot = modified_ratio(x, R0, C0, k, alpha, ratio_min, ratio_max)
R1_plot = modified_ratio(x, R1, C1, k, alpha, ratio_min, ratio_max)

# Create a plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, R0_plot, label=f'R0(x) (modified ratio)', color='blue')
ax.plot(x, R1_plot, label=f'R1(x) (modified ratio)', color='red')

# Set axis properties
ax.set_xlabel('x')
ax.set_ylabel('Modified Ratio')
ax.set_title(f'Modified Ratios for k={k}, alpha={alpha}')
ax.legend()
ax.grid(True)

# Show plot in Streamlit
st.pyplot(fig)

# Add a section to show the crossover point
crossover_x = x[np.argmin(np.abs(R1_plot - R0_plot))]
st.write(f"Approximate crossover point: x = {crossover_x:.2f}")

# Calculate and display ratios for the current k value
st.subheader(f"Ratios for k = {k:.2f}")

# Compute treated/untreated values and delta
treated = R1_plot > R0_plot
untreated = ~treated

# Create a DataFrame for the treated/untreated values and delta
data = {
    'x': x,
    'Treated Ratio': np.where(treated, R1_plot, np.nan),
    'Untreated Ratio': np.where(untreated, R0_plot, np.nan),
    'Delta': np.where(treated, R1_plot - R0_plot, np.nan)
}

df = pd.DataFrame(data)

# Display the table in Streamlit
st.write("Treated vs Untreated Ratios and Delta Table:")
st.dataframe(df)

# Add a checkbox to show/hide the original (unmodified) ratios
show_original = st.checkbox('Show original (unmodified) ratios')

if show_original:
    R0_original = ratio(R0(x), C0, k)
    R1_original = ratio(R1(x), C1, k)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, R0_original, label='R0(x) (original ratio)', color='cyan', linestyle='--')
    ax.plot(x, R1_original, label='R1(x) (original ratio)', color='magenta', linestyle='--')
    ax.plot(x, R0_plot, label='R0(x) (modified ratio)', color='blue')
    ax.plot(x, R1_plot, label='R1(x) (modified ratio)', color='red')
    
    ax.set_xlabel('x')
    ax.set_ylabel('Ratio')
    ax.set_title(f'Modified vs Original Ratios (k={k}, alpha={alpha})')
    ax.legend()
    ax.grid(True)
    
    st.pyplot(fig)
