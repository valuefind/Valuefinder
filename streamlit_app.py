import streamlit as st
import pandas as pd
import pickle

def load(path):
    return pickle.load(open(path, 'rb'))

st.set_page_config(page_title="ValueFinder", layout="wide")
st.title("⚽ ValueFinder App")
st.write("Find your best matches!")

# ========== LOAD YOUR FILES HERE ==========
# CHANGE THESE FILENAMES TO MATCH WHAT YOU UPLOADED TO GITHUB
try:
    model = load('model.pkl')  # change to your model name
    df = pd.read_csv('data.csv')  # change to your data name
    st.success("Model and Data loaded successfully!")
except Exception as e:
    st.error(f"Error loading files: {e}")
    st.stop()

# ========== INPUT SECTION ==========
st.header("Enter Details to Find Matches")

col1, col2 = st.columns(2)

with col1:
    # EXAMPLE: change these to match your data columns
    player_name = st.text_input("Player Name")
    age = st.number_input("Age", min_value=16, max_value=45, value=25)
    
with col2:
    # EXAMPLE: change these to match your data columns
    position = st.selectbox("Position", ['ST', 'CM', 'CB', 'GK'])
    rating = st.slider("Rating", 0, 100, 75)

if st.button("🔍 Find Matches", type="primary"):
    # ========== MATCHING LOGIC ==========
    # CHANGE THIS TO YOUR REAL PREDICTION/MATCHING CODE
    st.subheader("Top Matches")
    
    # Example: just show first 5 rows as "matches"
    # Replace this with: model.predict() or your similarity logic
    matches = df.head(5) 
    
    st.dataframe(matches, use_container_width=True)
    st.success(f"Found {len(matches)} matches!")

st.caption("Built with Streamlit")
