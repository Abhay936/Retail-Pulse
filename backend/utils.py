import pandas as pd
import streamlit as st
from database import collection

@st.cache_data(ttl=600)
def load_data():
    cursor = collection.find({}, {"_id": 0})
    return pd.DataFrame(list(cursor))