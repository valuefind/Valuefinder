
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="ValueFinder", layout="wide")
st.title("⚽ ValueFinder App - DEMO MODE")
st.write("This is using fake data so you can see it work")

# ========== FAKE DATA BUILT INTO APP ==========
data = {
    'Player': ['Messi', 'Ronaldo', 'Haaland', 'Mbappe', 'De Bruyne'],
    'Age': [36, 39, 24, 25, 33],
    'Position': ['RW', 'ST', 'ST', 'LW', 'CM'],
    'Rating': [93, 91, 90, 92, 91],
    'Value': ['$50M', '$45M', '$180M', '$170M', '$100M']
}
df = pd.DataFrame(data)

st.success("Demo data loaded!")

# ========== INPUT SECTION ==========
st.header("Find Similar Players")

col1, col2 = st.columns(2)
with col1:
    position = st.selectbox("Position", ['ST', 'CM', 'RW', 'LW', 'CB'])
with col2:
    min_rating = st.slider("Min Rating", 80, 95, 88)

if st.button("🔍 Find Matches", type="primary"):
    matches = df[df['Position'] == position]
    matches = matches[matches['Rating'] >= min_rating]
    
    st.subheader("Top Matches")
    st.dataframe(matches, use_container_width=True)

st.caption("Upload your real model.pkl and data.csv later to use your own data")
