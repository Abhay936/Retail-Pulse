import streamlit as st
import requests

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Customer Churn Prediction")
st.caption("Predict whether a customer is likely to churn using the trained Machine Learning model.")

st.divider()

tab1, tab2 = st.tabs([
    "👤 Predict using Customer ID",
    "📊 Predict using RFM"
])

# ==========================================================
# Customer ID Prediction
# ==========================================================

with tab1:

    customer_id = st.number_input(
        "Customer ID",
        min_value=1,
        step=1,
        key="custid"
    )

    if st.button("🔍 Predict Churn", use_container_width=True):

        payload = {
            "customer_id": int(customer_id)
        }

        try:

            with st.spinner("Predicting..."):

                response = requests.post(
                    "http://127.0.0.1:8000/churn/predict-cust_ID",
                    json=payload
                )

            if response.status_code == 200:

                result = response.json()

                st.success("Prediction Completed Successfully")

                c1, c2 = st.columns(2)

                c1.metric(
                    "🆔 Customer ID",
                    result["CustomerID"]
                )

                c2.metric(
                    "📉 Churn Probability",
                    f"{result['ChurnProbability']*100:.2f}%"
                )

                st.divider()

                col1, col2 = st.columns(2)

                with col1:
                    st.info(
                        f"🎯 Prediction : **{result['Prediction']}**"
                    )

                with col2:

                    risk = result["RiskLevel"]

                    if risk == "Low":
                        st.success(f"🟢 Risk Level : {risk}")

                    elif risk == "Medium":
                        st.warning(f"🟡 Risk Level : {risk}")

                    else:
                        st.error(f"🔴 Risk Level : {risk}")

            else:
                st.error(response.json()["detail"])

        except requests.exceptions.ConnectionError:
            st.error("FastAPI server is not running.")

# ==========================================================
# Manual RFM Prediction
# ==========================================================

with tab2:

    c1, c2, c3 = st.columns(3)

    with c1:
        recency = st.number_input(
            "📅 Recency",
            min_value=0,
            value=30
        )

    with c2:
        frequency = st.number_input(
            "🛒 Frequency",
            min_value=1,
            value=5
        )

    with c3:
        monetary = st.number_input(
            "💰 Monetary",
            min_value=0.0,
            value=1000.0
        )

    if st.button(
        "📊 Predict using RFM",
        use_container_width=True
    ):

        payload = {
            "Recency": recency,
            "Frequency": frequency,
            "Monetary": monetary
        }

        try:

            with st.spinner("Predicting..."):

                response = requests.post(
                    "http://127.0.0.1:8000/churn/predict-rfm",
                    json=payload
                )

            if response.status_code == 200:

                result = response.json()

                st.success("Prediction Completed Successfully")

                c1, c2 = st.columns(2)

                c1.metric(
                    "📉 Churn Probability",
                    f"{result['Probility']*100:.2f}%"
                )

                c2.metric(
                    "🎯 Prediction",
                    result["prediction"]
                )

            else:
                st.error(response.json()["detail"])

        except requests.exceptions.ConnectionError:
            st.error("FastAPI server is not running.")