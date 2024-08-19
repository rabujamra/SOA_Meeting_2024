import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def calculate_model_value(R, C, k, alpha):
    # Simplified model calculation for demonstration
    return (R**k / C**(1-k)) * (1 + alpha * (R/C - 1))

# Streamlit app
st.title("Interactive 3D Visualization of R/C Ratios with k and α")

# Slider for alpha
alpha = st.slider("Select α value", 0.0, 2.0, 0.5, 0.1)

# Generate data
k_values = np.linspace(0, 1, 50)
rc_ratios = np.linspace(0.1, 10, 50)  # Assuming R/C ratios from 0.1 to 10
K, RC = np.meshgrid(k_values, rc_ratios)

# Calculate Z values
Z = np.zeros_like(K)
for i in range(K.shape[0]):
    for j in range(K.shape[1]):
        Z[i, j] = calculate_model_value(RC[i, j], 1, K[i, j], alpha)

# Create 3D surface plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(K, RC, Z, cmap='viridis')

ax.set_xlabel('k')
ax.set_ylabel('R/C Ratio')
ax.set_zlabel('Model Value')
ax.set_title(f'Model Values for Varying k and R/C Ratios (α = {alpha})')

# Add colorbar
fig.colorbar(surf, shrink=0.5, aspect=5)

# Display the plot
st.pyplot(fig)

# Additional explanations
st.write("""
This 3D surface plot shows how the model values change with different k values and R/C ratios.
- The x-axis represents k values from 0 to 1.
- The y-axis represents R/C ratios.
- The z-axis (and color) represent the resulting model values.
- Use the slider above to change the α value and see how it affects the surface.
""")