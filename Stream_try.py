import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Define parameters
a = 2
b = 5
c = 3
C0 = 1  
C1 = 4

# Define the functions R0 and R1
def R0(x):
    return a * x + b

def R1(x):
    return a * x + (b - c)

# Define the rankings
def rank(x):
    return np.argsort(-x)  # Ranking in descending order

# Compute the rankings
def ranked_ratios(x, k):
    R0_values = R0(x)
    R1_values = R1(x)
    
    # Rank in descending order
    R0_rank = rank(R0_values)
    R1_rank = rank(R1_values)
    
    # Use rankings to compute ratios
    R0_ranked = R0_values[R0_rank]
    R1_ranked = R1_values[R1_rank]
    
    ratio_R0_ranked = (R0_ranked**k) / (C0**(1 - k))
    ratio_R1_ranked = (R1_ranked**k) / (C1**(1 - k))
    
    return ratio_R0_ranked, ratio_R1_ranked

# Streamlit app
st.title('Interactive Plot for Ranked R0 and R1 Ratios')

# Slider for k value
k = st.slider('Select value of k', min_value=0.0, max_value=1.0, value=0.5, step=0.01)

# Define a range of x values
x = np.linspace(0, 10, 100)

# Compute the ranked ratios
R0_plot, R1_plot = ranked_ratios(x, k)

# Create a plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, R0_plot, label=f'Ranked R0(x)^{k} / C0^{round(1-k, 2)}', color='blue')
ax.plot(x, R1_plot, label=f'Ranked R1(x)^{k} / C1^{round(1-k, 2)}', color='red')

# Set axis properties
ax.set_xlabel('x')
ax.set_ylabel('Ratio')
ax.set_title(f'Ranked Ratios for k={k}')
ax.legend()
ax.grid(True)

# Show plot in Streamlit
st.pyplot(fig)
