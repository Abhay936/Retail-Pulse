import streamlit as st
import pandas as pd
from  backend.database import collection
import pandas as pd
import requests


# response = requests.get(
#     "https://retail-pulse-ht37.onrender.com/data_load/dashboard"
# )

# result = response.json()
# df1 = pd.DataFrame(result["data"])


@st.cache_data
def load_data():
    url = "https://huggingface.co/Abhay936/Retail_pulse/resolve/main/feature_engineered_data.csv"
    return pd.read_csv(url)

df1 = load_data()






st.set_page_config(layout="wide",
                   page_title="Dashbord")

st.title("📊 RetailPulse: AI-Powered Customer Analytics & Demand Forecasting")
st.write("📝 RetailPulse is an AI-powered retail analytics platform designed to analyze sales performance, customer purchasing behavior, and demand trends. The dashboard provides interactive visualizations, customer segmentation, churn prediction, and demand forecasting to support data-driven business decisions and improve overall retail performance.")





# df1 = load_data()




total_revenue = df1["Revenue"].sum()

total_transactions = df1["Invoice"].nunique()

total_customers = df1["Customer ID"].nunique()

total_products = df1["StockCode"].nunique()

total_countries = df1["Country"].nunique()


st.header("📈 KPI Cards")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Total Revenue", f"£{total_revenue:,.0f}")

with col2:
    st.metric("👥 Customers", total_customers)

with col3:
    st.metric("🛒 Transactions", total_transactions)

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("📦 Products", total_products)

with col5:
    st.metric("🌍 Countries", total_countries)

with col6:
    st.metric("📅 Years", "2009–2011")


st.header("📋 Dataset Information")
dataset_info = pd.DataFrame({
    "Attribute": [
        "Original Records",
        "Original Features",
        "Processed Features",
        "Processed Records",
        "Time Period",
    ],
    "Value": [
        1067371,
        8,
        df1.shape[1],
        len(df1),
        "Dec 2009 - Dec 2011",
    ]
})
st.table(dataset_info)


st.header("👀 Dataset Preview")
st.dataframe(df1.head(10))

st.header("🔧Data Preprocessing Summary")
st.markdown("""- <h5>✔ Successfully merged both sheets of the Online Retail II dataset into a single dataset.</h5>
- <h5>✔ Cleaned the data by removing duplicates, cancelled transactions, invalid records, and handling missing values.</h5>
- <h5>✔ Performed feature engineering by creating Revenue, time-based features, Basket Size, and Order Value.</h5>
- <h5>✔ Validated data quality by checking data types, missing values, duplicates, and feature consistency.</h5>
- <h5>✔ Prepared a clean, feature-engineered dataset ready for exploratory analysis, machine learning, and dashboard visualization.</h5>
- <h5>✔ Saved the processed dataset for downstream analytics, customer segmentation, churn prediction, and demand forecasting.</h5>""",unsafe_allow_html=True)

st.header("🔥 Correlation Heatmap")

st.image("charts/correlation_heatmap_equal.png")
i_10=st.toggle("💡 Correlation Insights")
if i_10:
    st.markdown("""

- **Quantity and Revenue** have a strong positive correlation (**0.83**), indicating that higher quantities sold generally result in higher revenue.

- **Unit Price and Revenue** have a weak positive correlation (**0.14**), suggesting that revenue is influenced more by sales volume than product price.

- **Quantity and Unit Price** have almost no correlation (**-0.005**), showing that the quantity purchased is largely independent of product price.
""")
else:
   st.write()



st.header("⭐ Business Highlights")

top_product = (
    df1.groupby("Description")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

highest_product = top_product.index[0]
highest_product_revenue = top_product.iloc[0]

top_customer = (
    df1.groupby("Customer ID")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

customer_id = top_customer.index[0]

customer_revenue = top_customer.iloc[0]

top_country = (
    df1.groupby("Country")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

country = top_country.index[0]
country_revenue = top_country.iloc[0]

top_month = (
    df1.groupby("Month")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

month = top_month.index[0]
month_revenue = top_month.iloc[0]


col1, col2 = st.columns(2)

with col1:
    st.info(f"📈 Highest Revenue Product\n\n{highest_product} \n\n💰 Revenue : {highest_product_revenue}")

with col2:
    st.info(f"👤 Highest Spending Customer\n\n{customer_id} \n\n💰 Revenue : {customer_revenue}")

col3, col4 = st.columns(2)

with col3:
    st.info(f"🌍 Best Performing Country\n\n{country} \n\n💰 Revenue : {country_revenue}")

with col4:
    st.info(f"📅 Peak Sales Month\n\n{month} \n\n💰 Revenue : {month_revenue}")

# import requests
# import streamlit as st
# import pandas as pd

# API_URL = "https://retail-pulse-ht37.onrender.com/data_load/dashboard"

# try:
#     response = requests.get(API_URL, timeout=30)

#     st.write("Status Code:", response.status_code)
#     st.write("Content-Type:", response.headers.get("content-type"))

#     if response.status_code != 200:
#         st.error(f"API Error: {response.status_code}")
#         st.code(response.text)
#         st.stop()

#     try:
#         result = response.json()
#     except ValueError:
#         st.error("API did not return JSON")
#         st.code(response.text)
#         st.stop()

#     df = pd.DataFrame(result["data"])
#     st.dataframe(df.head())

# except requests.exceptions.RequestException as e:
#     st.error(f"Request Failed: {e}")


# import requests
# import streamlit as st

# url = "https://retail-pulse-ht37.onrender.com/data_load/dashboard"

# response = requests.get(url)

# st.write(response.url)
# st.write(response.status_code)
# st.code(response.text[:1000])