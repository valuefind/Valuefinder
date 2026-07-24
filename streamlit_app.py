
import streamlit as st
import pandas as pd
import requests
import os
import joblib
from datetime import datetime

# ==================== CONFIG ====================
st.set_page_config(page_title="ValueFinder V4", layout="wide")

FOTMOB_API = "https://www.fotmob.com/api"

# XGBoost Model - Upload your trained model.joblib to GitHub repo
MODEL_PATH = "model.joblib" 

# League multipliers for market value
LEAGUE_MULTIPLIERS = {
    "Premier League": 1.8, "La Liga": 1.6, "Bundesliga": 1.5, 
    "Serie A": 1.4, "Ligue 1": 1.3, "Eredivisie": 1.0,
    "Primeira Liga": 0.9, "MLS": 0.7, "Other": 0.6
}

# ==================== FUNCTIONS ====================
@st.cache_data(ttl=3600)
def search_player_fotmob(name):
    """Search player on FotMob"""
    try:
        url = f"{FOTMOB_API}/search/"
        params = {"q": name}
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        
        players = data.get('players', [])
        if players:
            return players[0] # Return first match
        return None
    except:
        return None

@st.cache_data(ttl=3600)
def get_player_stats_fotmob(player_id):
    """Get player stats from FotMob"""
    try:
        url = f"{FOTMOB_API}/playerData"
        params = {"id": player_id}
        r = requests.get(url, params=params, timeout=10)
        return r.json()
    except:
        return None

def predict_value(features_df, model):
    """Predict market value using XGBoost"""
    try:
        prediction = model.predict(features_df)
        return float(prediction[0])
    except:
        return None

# ==================== UI ====================
st.title("🌍 ValueFinder V4 - FotMob XGBoost")
st.markdown("**AI-powered football player market value prediction using live FotMob data**")

col1, col2 = st.columns([2,1])

with col1:
    player_name = st.text_input("🔍 Player Name", placeholder="e.g. Erling Haaland")
    club = st.text_input("Club", placeholder="e.g. Manchester City")
    league = st.selectbox("League", list(LEAGUE_MULTIPLIERS.keys()))
    age = st.number_input("Age", min_value=16, max_value=45, value=24)
    position = st.selectbox("Position", ["GK", "DF", "MF", "FW"])

with col2:
    st.metric("Model", "XGBoost V4")
    st.metric("Data Source", "FotMob API")
    st.metric("Last Updated", datetime.now().strftime("%d %b %Y"))

if st.button("🚀 Predict Market Value", type="primary"):
    if not player_name:
        st.error("Please enter a player name")
    else:
        with st.spinner("Fetching live data from FotMob..."):
            player_data = search_player_fotmob(player_name)
            
        if player_data:
            player_id = player_data.get('id')
            player_full_name = player_data.get('name')
            player_team = player_data.get('teamName', club)
            
            stats = get_player_stats_fotmob(player_id)
            
            # Extract features - customize based on your model training
            features = {
                'age': age,
                'goals': stats.get('goals', 0) if stats else 0,
                'assists': stats.get('assists', 0) if stats else 0,
                'minutes': stats.get('minutes', 0) if stats else 0,
                'league_multiplier': LEAGUE_MULTIPLIERS.get(league, 0.6),
                'position_encoded': 1 if position == "FW" else 2 if position == "MF" else 3 if position == "DF" else 4
            }
            
            features_df = pd.DataFrame([features])
            
            # Load model and predict
            if os.path.exists(MODEL_PATH):
                model = joblib.load(MODEL_PATH)
                predicted_value = predict_value(features_df, model)
                
                if predicted_value:
                    # Apply league multiplier
                    final_value = predicted_value * LEAGUE_MULTIPLIERS.get(league, 0.6)
                    
                    st.success("### Prediction Complete!")
                    colA, colB, colC = st.columns(3)
                    
                    with colA:
                        st.metric("Player", player_full_name)
                    with colB:
                        st.metric("Team", player_team)
                    with colC:
                        st.metric("Predicted Value", f"€{final_value/1000000:.2f}M")
                    
                    st.info(f"Base XGBoost: €{predicted_value/1000000:.2f}M | League Adj: {LEAGUE_MULTIPLIERS.get(league, 0.6)}x")
                    
                    if stats:
                        st.subheader("📊 Live Stats from FotMob")
                        st.json(stats)
            else:
                st.warning("⚠️ model.joblib not found. Upload your trained model to the repo or run in demo mode.")
                st.info("Demo Value: €25.50M")
        else:
            st.error("Player not found on FotMob. Try a different name.")

st.markdown("---")
st.caption("ValueFinder V4 | Built with Streamlit + FotMob API + XGBoost")
