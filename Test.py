import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
ax.plot([1,2,3,4],[1,2,2,1])
st.pyplot(fig)

# arr = np.random.normal(1, 1, size=100)
# fig, ax = plt.subplots()
# ax.hist(arr, bins=20)

# st.pyplot(fig)
