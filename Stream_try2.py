import streamlit as st
import numpy as np
import plotly.graph_objects as go

def calculate_model_value(R, C, k, alpha):
    # Your model calculation here
    # This incorporates both k and alpha
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
fig = go.Figure(data=[go.Surface(z=Z, x=K, y=RC)])
fig.update_layout(
    title=f'Model Values for Varying k and R/C Ratios (α = {alpha})',
    scene=dict(
        xaxis_title='k',
        yaxis_title='R/C Ratio',
        zaxis_title='Model Value'
    ),
    width=700,
    margin=dict(r=20, b=10, l=10, t=40)
)

# Display the plot
st.plotly_chart(fig)

# Additional explanations
st.write("""
This 3D surface plot shows how the model values change with different k values and R/C ratios.
- The x-axis represents k values from 0 to 1.
- The y-axis represents R/C ratios.
- The z-axis (and color) represent the resulting model values.
- Use the slider above to change the α value and see how it affects the surface.
""")