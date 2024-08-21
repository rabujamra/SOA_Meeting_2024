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

# Define sigmoid function
def sigmoid(x, alpha):
    return 1 / (1 + np.exp(-alpha * x))

# Define the modified ratio function with sigmoid adjustment
def modified_ratio_with_sigmoid(x, R_func, C, k, alpha):
    R = R_func(x)
    base_ratio = ratio(R, C, k)
    adjustment = sigmoid(R - R.min(), alpha)
    return base_ratio * (1 + adjustment)

# Streamlit app
st.title('Interactive Plot for R0 and R1 Ratios with Sigmoid Nonlinear Modification')

# Sliders for k and alpha values
k = st.slider('Select value of k', min_value=0.0, max_value=1.0, value=0.5, step=0.01)
alpha = st.slider('Select value of alpha', min_value=0.0, max_value=10.0, value=1.0, step=0.1)

# Define a range of x values
x = np.linspace(1, 10, 10)  # Updated to have 10 values between 1 and 10

# Compute modified ratios
R0_plot = modified_ratio_with_sigmoid(x, R0, C0, k, alpha)
R1_plot = modified_ratio_with_sigmoid(x, R1, C1, k, alpha)

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

# Calculate and display ratios for the current k value
st.subheader(f"Ratios for k = {k:.2f}")

# Calculate the treated and untreated values
treated = R1_plot > R0_plot
untreated = ~treated

# For each x value, compute the treated and untreated values
treated_values = R1_plot[treated]
untreated_values = R0_plot[untreated]

# If there are no treated or untreated values, set average to 0
avg_treated = np.mean(treated_values) if len(treated_values) > 0 else 0
avg_untreated = np.mean(untreated_values) if len(untreated_values) > 0 else 0
delta = avg_treated - avg_untreated

# Display results in a table
results = {
    'x': x,
    'R0 (Untreated)': R0_plot,
    'R1 (Treated)': R1_plot,
    'Delta': [R1 - R0 for R0, R1 in zip(R0_plot, R1_plot)]
}

st.write(pd.DataFrame(results))

st.write(f"Average Treated Ratio: {avg_treated:.4f}")
st.write(f"Average Untreated Ratio: {avg_untreated:.4f}")
st.write(f"Delta (Treated - Untreated): {delta:.4f}")

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
