import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Demand Forecasting",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Demand Forecasting")
st.caption("Forecast business revenue and product demand using Machine Learning models.")

st.divider()

tab1, tab2 = st.tabs([
    "📊 Business Revenue Forecast",
    "📦 Product Demand Forecast"
])

# =====================================================
# TAB 1 : BUSINESS FORECAST
# =====================================================

with tab1:

    days = st.number_input(
        "Forecast Days",
        min_value=1,
        max_value=365,
        value=30,
        key="days"
    )

    if st.button("📈 Generate Revenue Forecast", use_container_width=True):

        try:

            with st.spinner("Generating Forecast..."):

                response = requests.get(
                    "https://retail-pulse-ht37.onrender.com/forecast/predict",
                    params={"days": days}
                )

            if response.status_code == 200:

                result = response.json()

                st.success("Forecast Generated Successfully")

                c1, c2, c3, c4 = st.columns(4)

                c1.metric(
                    "💰 Total Revenue",
                    f"₹{result['TotalForecastRevenue']:,.2f}"
                )

                c2.metric(
                    "📅 Average Revenue",
                    f"₹{result['AverageDailyRevenue']:,.2f}"
                )

                c3.metric(
                    "📈 Highest",
                    f"₹{result['HighestForecastRevenue']:,.2f}"
                )

                c4.metric(
                    "📉 Lowest",
                    f"₹{result['LowestForecastRevenue']:,.2f}"
                )

                forecast_df = pd.DataFrame(result["DailyForecast"])

                forecast_df["Date"] = pd.to_datetime(
                    forecast_df["Date"]
                )

                fig = px.line(
                    forecast_df,
                    x="Date",
                    y="ForecastRevenue",
                    markers=True,
                    title="Revenue Forecast"
                )

                fig.update_layout(
                    template="plotly_white",
                    height=500
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )




                st.dataframe(
                    forecast_df,
                    use_container_width=True,
                    hide_index=True
                )

            else:
                st.error(response.json()["detail"])

        except Exception as e:
            st.error(str(e))


# =====================================================
# TAB 2 : PRODUCT DEMAND FORECAST
# =====================================================

# with tab2:
#     st.subheader("📦 Product Demand Forecast")

# # =====================================
# # User Input
# # =====================================
#     stock_code = st.text_input(
#     "📦 Stock Code",
#     placeholder="Example: 85123A"
# )

# # =====================================
# # Prediction Button
# # =====================================

#     if st.button("🔮 Predict Product Demand", use_container_width=True):

#         if stock_code.strip() == "":
#             st.warning("Please enter a Stock Code.")
#             st.stop()

#         payload = {
#         "StockCode": stock_code.strip()
#     }

#         try:

#             with st.spinner("Predicting Demand..."):

#                 response = requests.post(
#                 "https://retail-pulse-ht37.onrender.com/forecast/product",
#                 json=payload,
#                 timeout=30
#             )

#             if response.status_code == 200:

#                 result = response.json()

#                 st.success("Prediction Completed Successfully")

#             # ===============================
#             # Main KPIs
#             # ===============================

#                 col1, col2, col3 = st.columns(3)

#                 col1.metric(
#                 "📦 Stock Code",
#                 result["StockCode"]
#             )

#                 col2.metric(
#                 "📅 Prediction Date",
#                 result["PredictionDate"]
#             )

#                 col3.metric(
#                 "📈 Forecast Demand",
#                 f"{result['ForecastDemand']} Units"
#             )
            
#                 st.divider()

#             # ===============================
#             # Inventory KPIs
#             # ===============================

#                 col4, col5, col6 = st.columns(3)

#                 col4.metric(
#                 "📦 Current Stock",
#                 result["CurrentStock"]
#             )

#                 col5.metric(
#                 "🛡 Safety Stock",
#                 result["SafetyStock"]
#             )

#                 col6.metric(
#                 "🛒 Suggested Reorder",
#                 result["SuggestedReorder"]
#             )

#                 st.divider()

#             # ===============================
#             # Historical KPIs
#             # ===============================

#                 col7, col8, col9 = st.columns(3)

#                 col7.metric(
#                 "💰 Last Revenue",
#                 f"£{result['LastRevenue']:.2f}"
#             )

#                 col8.metric(
#                 "🛒 Last Order Value",
#                 f"£{result['LastOrderValue']:.2f}"
#             )

#                 col9.metric(
#                 "🧺 Basket Size",
#                 result["LastBasketSize"]
#             )

#                 st.divider()

#             # ===============================
#             # Business Insight
#             # ===============================

#                 demand = result["ForecastDemand"]

#                 if demand >= 50:

#                     st.success(
#                     "📈 High demand expected. Increase inventory to avoid stock-outs."
#                 )

#                 elif demand >= 20:

#                     st.info(
#                     "📊 Moderate demand expected. Monitor stock levels regularly."
#                 )

#                 else:

#                     st.warning(
#                     "📉 Low demand expected. Reordering is currently not necessary."
#                 )
#             else:
#                 try:
#                     st.error(response.json()["detail"])
#                 except Exception:
#                     st.error(f"API Error ({response.status_code})")

#         except requests.exceptions.RequestException as e:
#             st.error(f"Request Failed: {e}")


with tab2:

    st.subheader("📦 Product Demand Forecast")

    stock_code = st.text_input(
        "📦 Stock Code",
        placeholder="Example: 85123A",
        key="stock_code"
    )

    if st.button("🔮 Predict Product Demand", use_container_width=True):

        if not stock_code.strip():
            st.warning("Please enter a Stock Code.")
            st.stop()

        payload = {
            "StockCode": stock_code.strip()
        }

        try:

            with st.spinner("Predicting Demand..."):

                response = requests.post(
                    "https://retail-pulse-ht37.onrender.com/forecast/product",
                    json=payload,
                    timeout=30
                )

            if response.status_code != 200:
                st.error(response.json().get("detail", "Prediction Failed"))
                st.stop()

            result = response.json()

            st.success("Prediction Completed Successfully")

            # ==========================
            # Main Metrics
            # ==========================

            c1, c2, c3 = st.columns(3)

            c1.metric("📦 Stock Code", result["StockCode"])
            c2.metric("📅 Prediction Date", result["PredictionDate"])
            c3.metric("📈 Forecast Demand", f"{result['ForecastDemand']} Units")

            st.divider()

            # ==========================
            # Inventory Metrics
            # ==========================

            c4, c5, c6 = st.columns(3)

            c4.metric("📦 Current Stock", result["CurrentStock"])
            c5.metric("🛡 Safety Stock", result["SafetyStock"])
            c6.metric("🛒 Suggested Reorder", result["SuggestedReorder"])

            st.divider()

            # ==========================
            # Historical Metrics
            # ==========================

            c7, c8, c9 = st.columns(3)

            c7.metric("💰 Last Revenue", f"£{result['LastRevenue']:.2f}")
            c8.metric("🛒 Last Order Value", f"£{result['LastOrderValue']:.2f}")
            c9.metric("🧺 Basket Size", result["LastBasketSize"])

            st.divider()

            # ==========================
            # Business Insight
            # ==========================

            demand = result["ForecastDemand"]

            if demand >= 50:
                st.success(
                    "📈 High demand expected. Increase inventory to avoid stock-outs."
                )

            elif demand >= 20:
                st.info(
                    "📊 Moderate demand expected. Monitor inventory levels regularly."
                )

            else:
                st.warning(
                    "📉 Low demand expected. Reordering is currently not necessary."
                )

        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")

        except Exception as e:
            st.error(f"Unexpected Error: {e}")