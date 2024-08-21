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
    return R * (1 + alpha * sigmoid(gamma * (base_ratio - 1)))

# Streamlit app
st.title('Interactive Plot for R0 and R1 with Selective Amplification')

# Sliders for parameters
k = st.slider('Select value of k', min_value=0.0, max_value=1.0, value=0.5, step=0.01)
alpha = st.slider('Select value of alpha', min_value=0.0, max_value=5.0, value=1.0, step=0.1)
gamma = st.slider('Select value of gamma', min_value=0.1, max_value=10.0, value=1.0, step=0.1)

# Define a range of x values
x = np.linspace(0, 10, 100)

# Compute the modified ratios
R0_values = R0(x)
R1_values = R1(x)
R0_mod = modified_ratio(R0_values, C0, k, alpha, gamma)
R1_mod = modified_ratio(R1_values, C1, k, alpha, gamma)

# Create a plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, R0_mod, label='R0 (modified)', color='blue')
ax.plot(x, R1_mod, label='R1 (modified)', color='red')
ax.plot(x, R0_values, label='R0 (original)', color='cyan', linestyle='--')
ax.plot(x, R1_values, label='R1 (original)', color='magenta', linestyle='--')

# Set axis properties
ax.set_xlabel('x')
ax.set_ylabel('R values')
ax.set_title(f'Original and Modified R Values (k={k}, alpha={alpha}, gamma={gamma})')
ax.legend()
ax.grid(True)

# Show plot in Streamlit
st.pyplot(fig)

# Calculate and display ratios
st.subheader(f"Average Ratios")

avg_R0_original = np.mean(R0_values)
avg_R1_original = np.mean(R1_values)
avg_R0_modified = np.mean(R0_mod)
avg_R1_modified = np.mean(R1_mod)

st.write(f"Average R0 (original): {avg_R0_original:.4f}")
st.write(f"Average R1 (original): {avg_R1_original:.4f}")
st.write(f"Average R0 (modified): {avg_R0_modified:.4f}")
st.write(f"Average R1 (modified): {avg_R1_modified:.4f}")

# Calculate and display crossover point
crossover_x = x[np.argmin(np.abs(R1_mod - R0_mod))]
st.write(f"Approximate crossover point: x = {crossover_x:.2f}")