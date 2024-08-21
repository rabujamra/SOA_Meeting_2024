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

# Define the sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Define the nonlinear modification function using sigmoid
def sigmoid_mod(R, R_min, R_max, alpha):
    sigmoid_value = sigmoid((R - R_min) / (R_max - R_min) - 0.5)
    return R * (1 + alpha * sigmoid_value)

# Define the ratios with cost for R0 and R1, including sigmoid modification
def ratio_R0(x, k, alpha, R_min, R_max):
    R = R0(x)
    R_mod = sigmoid_mod(R, R_min, R_max, alpha)
    return (R_mod**k) / (C0**(1 - k))

def ratio_R1(x, k, alpha, R_min, R_max):
    R = R1(x)
    R_mod = sigmoid_mod(R, R_min, R_max, alpha)
    return (R_mod**k) / (C1**(1 - k))

# Streamlit app
st.title('Interactive Plot for R0 and R1 Ratios with Sigmoid Modification')

# Sliders for k and alpha values
k = st.slider('Select value of k', min_value=0.0, max_value=1.0, value=0.5, step=0.01)
alpha = st.slider('Select value of alpha', min_value=0.0, max_value=2.0, value=0.5, step=0.01)

# Define a range of x values
x = np.linspace(0, 10, 100)

# Calculate R_min and R_max
R_values = np.concatenate([R0(x), R1(x)])
R_min, R_max = R_values.min(), R_values.max()

# Compute the ratios
R0_plot = ratio_R0(x, k, alpha, R_min, R_max)
R1_plot = ratio_R1(x, k, alpha, R_min, R_max)

# Create a plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, R0_plot, label=f'R0(x) (modified) ^ {k} / C0 ^ {round(1-k, 2)}', color='blue')
ax.plot(x, R1_plot, label=f'R1(x) (modified) ^ {k} / C1 ^ {round(1-k, 2)}', color='red')

# Set axis properties
ax.set_xlabel('x')
ax.set_ylabel('Ratio')
ax.set_title(f'Ratios for k={k}, alpha={alpha}')
ax.legend()
ax.grid(True)

# Show plot in Streamlit
st.pyplot(fig)

# Add a section to show the crossover point
crossover_x = x[np.argmin(np.abs(R1_plot - R0_plot))]
st.write(f"Approximate crossover point: x = {crossover_x:.2f}")

# Add a checkbox to show/hide the original (unmodified) ratios
show_original = st.checkbox('Show original (unmodified) ratios')

if show_original:
    R0_original = (R0(x)**k) / (C0**(1 - k))
    R1_original = (R1(x)**k) / (C1**(1 - k))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, R0_original, label=f'R0(x) (original) ^ {k} / C0 ^ {round(1-k, 2)}', color='cyan', linestyle='--')
    ax.plot(x, R1_original, label=f'R1(x) (original) ^ {k} / C1 ^ {round(1-k, 2)}', color='magenta', linestyle='--')
    ax.plot(x, R0_plot, label=f'R0(x) (modified) ^ {k} / C0 ^ {round(1-k, 2)}', color='blue')
    ax.plot(x, R1_plot, label=f'R1(x) (modified) ^ {k} / C1 ^ {round(1-k, 2)}', color='red')
    
    ax.set_xlabel('x')
    ax.set_ylabel('Ratio')
    ax.set_title(f'Modified vs Original Ratios (k={k}, alpha={alpha})')
    ax.legend()
    ax.grid(True)
    
    st.pyplot(fig)
