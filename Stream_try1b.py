import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# [All previous function definitions remain the same]

# Streamlit app
st.title('Interactive Plot for R0 and R1 Ratios with Nonlinear Modification')

# Sliders for k and alpha values
k = st.slider('Select value of k', min_value=0.0, max_value=1.0, value=0.5, step=0.01)
alpha = st.slider('Select value of alpha', min_value=0.0, max_value=2.0, value=0.5, step=0.01)

# Define a range of x values
x = np.linspace(0, 10, 100)

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

# Calculate average ratios for different k values
st.subheader("Average Ratios for Different k Values")
k_values = np.arange(0, 1.1, 0.1)
results = []

for k_val in k_values:
    R0_ratios = ratio(R0(x), C0, k_val)
    R1_ratios = ratio(R1(x), C1, k_val)
    ratio_min = min(R0_ratios.min(), R1_ratios.min())
    ratio_max = max(R0_ratios.max(), R1_ratios.max())
    
    R0_mod = modified_ratio(x, R0, C0, k_val, alpha, ratio_min, ratio_max)
    R1_mod = modified_ratio(x, R1, C1, k_val, alpha, ratio_min, ratio_max)
    
    treated = R1_mod > R0_mod
    untreated = ~treated
    
    avg_treated = np.mean(R1_mod[treated]) if np.any(treated) else 0
    avg_untreated = np.mean(R0_mod[untreated]) if np.any(untreated) else 0
    
    results.append((k_val, avg_treated, avg_untreated))

# Display results in a table
st.table({
    'k': [f"{k:.1f}" for k, _, _ in results],
    'Avg Treated Ratio': [f"{avg_t:.4f}" for _, avg_t, _ in results],
    'Avg Untreated Ratio': [f"{avg_u:.4f}" for _, _, avg_u in results]
})

# [The rest of the code for showing original ratios remains the same]