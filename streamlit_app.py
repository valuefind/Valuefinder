
import osimport streamlit as st
import pandas as pd
import pickle
def load(path):
return pickle.load(open(path, 'rb'))
from dotenv import load_dotenv

st.set_page_config(page_title="ValueFinder V4 - FotMob XGBoost", page_icon="🌍", layout="wide")

load_dotenv()

st.title("🌍 ValueFinder V4 - FotMob XGBoost")
st.markdown("Find undervalued players using FotMob data + ML model")

# Sidebar
st.sidebar.header("Settings")
league = st.sidebar.selectbox("Select League", ["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"])

# Search box
player_name = st.text_input("🔍 Search Player Name")

if st.button("Find Value"):
    if player_name:
        with st.spinner("Fetching data from FotMob..."):
            # Example API call - replace with your actual FotMob logic
            try:
                # This is where your FotMob scraping/API code goes
                st.success(f"Searching for {player_name} in {league}")
                
                # Example data - replace with real model prediction
                data = {
                    "Player": [player_name],
                    "Market Value": ["€20M"],
                    "Predicted Value": ["€35M"],
                    "Value Gap": ["+€15M"],
                    "xG": [0.45],
                    "xA": [0.32]
                }
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
                
                st.info("⚠️ Connect your real FotMob API and joblib model here")
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a player name")

st.sidebar.markdown("---")
st.sidebar.markdown("**ValueFinder V4**")
st.sidebar.markdown("Powered by XGBoost + FotMob")
