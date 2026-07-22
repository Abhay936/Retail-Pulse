import streamlit as st
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)


dash = st.Page("pages/Dashbord.py", title="Dashbord", icon="🏠")
sales = st.Page("pages/Sales_Analytics.py", title="Sales Analytics", icon="📊")
segments = st.Page("pages/segments.py", title="Customer Segmentation", icon="👥")
predict = st.Page("pages/Prediction.py", title="Prediction", icon="🤖")
forcast = st.Page("pages/forcasting.py", title="Forcaste", icon="📈")
inventory = st.Page("pages/inventory.py", title="Inventory Suggestion", icon="📦")



pg = st.navigation([dash,sales,segments,predict, forcast,inventory])
pg.run()



