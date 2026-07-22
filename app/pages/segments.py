import streamlit as st
import requests

st.set_page_config(layout="centered")

st.title("👥 Customer Segmentation")

st.markdown("---")


customer_id = st.number_input(
    "Customer ID",
    min_value=1,
    step=1
)

if st.button("🔍 Predict Segment", use_container_width=True):

    url = "https://retail-pulse-ht37.onrender.com/customer-segmentation/predict"

    payload = {
        "customer_id": int(customer_id)
    }

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:

            result = response.json()

            st.success("✅ Prediction Successful")

            st.markdown("### 📊 Customer RFM Summary")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "🆔 Customer ID",
                    result["Customer ID"]
                )

            with col2:
                st.metric(
                    "🎯 Cluster",
                    result["Cluster"]
                )

            col3, col4, col5 = st.columns(3)

            with col3:
                st.metric(
                    "📅 Recency",
                    result["Recency"]
                )

            with col4:
                st.metric(
                    "🛒 Frequency",
                    result["Frequency"]
                )

            with col5:
                st.metric(
                    "💰 Monetary",
                    f"₹{result['Monetary']:,.2f}"
                )

            st.markdown("---")

            st.success(
                f"🏆 Customer Segment : **{result['Segment']}**"
            )

        else:
            st.error(response.json()["detail"])

    except requests.exceptions.ConnectionError:
        st.error("❌ FastAPI server is not running.")