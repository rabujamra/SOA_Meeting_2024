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

# Define the modified ratio function
def modified_ratio(R, C, k, alpha, gamma):
    base_ratio = (R**k) / (C**(1-k))
    return base_ratio * (1 + alpha * sigmoid(gamma * (base_ratio - 1)))

# Streamlit app
st.title('Interactive Plot for R0 and R1 Ratios with Selective Amplification')

# Sliders for parameters
k = st.slider('Select value of k', min_value=0.0, max_value=1.0, value=0.5, step=0.01)
alpha = st.slider('Select value of alpha', min_value=0.0, max_value=5.0, value=1.0, step=0.1)
gamma = st.slider('Select value of gamma', min_value=0.1, max_value=10.0, value=1.0, step=0.1)

# Define a range of x values
x = np.linspace(0, 10, 100)

# Compute the ratios
R0_values = R0(x)
R1_values = R1(x)
ratio_R0 = modified_ratio(R0_values, C0, k, alpha, gamma)
ratio_R1 = modified_ratio(R1_values, C1, k, alpha, gamma)

# Create a plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, ratio_R0, label='R0^k/C0^(1-k) (modified)', color='blue')
ax.plot(x, ratio_R1, label='R1^k/C1^(1-k) (modified)', color='red')

# Set axis properties
ax.set_xlabel('x')
ax.set_ylabel('Modified Ratio (R^k/C^(1-k))')
ax.set_title(f'Modified Ratios (k={k}, alpha={alpha}, gamma={gamma})')
ax.legend()
ax.grid(True)

# Show plot in Streamlit
st.pyplot(fig)

# Calculate and display average ratios
st.subheader(f"Average Ratios")

avg_ratio_R0 = np.mean(ratio_R0)
avg_ratio_R1 = np.mean(ratio_R1)

st.write(f"Average R0^k/C0^(1-k) (modified): {avg_ratio_R0:.4f}")
st.write(f"Average R1^k/C1^(1-k) (modified): {avg_ratio_R1:.4f}")

# Calculate and display crossover point
crossover_x = x[np.argmin(np.abs(ratio_R1 - ratio_R0))]
st.write(f"Approximate crossover point: x = {crossover_x:.2f}")