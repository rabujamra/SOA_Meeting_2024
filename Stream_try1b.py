import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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

# Define transformations
def enhanced_transform(R, R_min, R_max, beta, alpha, high=True):
    if high:
        # Enhance high values more aggressively
        return R * np.exp(beta * (R - R_min))
    else:
        # Increase low values or reduce impact of high values
        return R * np.log(1 + beta * (R - R_min))

# Streamlit app
st.title('Interactive Plot for R0 and R1 Ratios with Nonlinear Transformation')

# Sliders for k and alpha values
k = st.slider('Select value of k', min_value=0.0, max_value=1.0, value=0.5, step=0.01)
alpha = st.slider('Select value of alpha', min_value=0.0, max_value=2.0, value=0.5, step=0.01)
beta = st.slider('Select value of beta', min_value=0.0, max_value=2.0, value=1.0, step=0.1)

# Define a range of x values
x = np.linspace(1, 10, 10)

# Calculate ratios
R0_values = R0(x)
R1_values = R1(x)
R0_ratios = ratio(R0_values, C0, k)
R1_ratios = ratio(R1_values, C1, k)

# Apply transformations
R0_transformed = enhanced_transform(R0_values, R0_values.min(), R0_values.max(), beta, alpha, high=False)
R1_transformed = enhanced_transform(R1_values, R1_values.min(), R1_values.max(), beta, alpha, high=True)

# Plot transformed values
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, R0_transformed, label='R0(x) (transformed)', color='blue')
ax.plot(x, R1_transformed, label='R1(x) (transformed)', color='red')

# Set axis properties
ax.set_xlabel('x')
ax.set_ylabel('Transformed Values')
ax.set_title(f'Transformed Values for k={k}, alpha={alpha}, beta={beta}')
ax.legend()
ax.grid(True)

# Show plot in Streamlit
st.pyplot(fig)

# Calculate and display crossover point
crossover_x = x[np.argmin(np.abs(R1_transformed - R0_transformed))]
st.write(f"Approximate crossover point: x = {crossover_x:.2f}")

# Create a table of values
import pandas as pd
df = pd.DataFrame({
    'x': x,
    'R0_transformed': R0_transformed,
    'R1_transformed': R1_transformed
})

st.write(df)
