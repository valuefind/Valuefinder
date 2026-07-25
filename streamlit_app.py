import os
import streamlit as st
import pandas as pd
import pickle

def load(path):
    return pickle.load(open(path, 'rb'))

st.set_page_config(page_title="ValueFinder", layout="wide")
st.title("ValueFinder App")
st.write("If you see this, the imports worked!")
