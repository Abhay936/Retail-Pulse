import streamlit as st
import pandas as pd
import plotly.express as px
# from backend.database import collection
import pandas as pd
# import requests



# response = requests.get(
#     "https://retail-pulse-ht37.onrender.com/data_load/dashboard"
# )

# result = response.json()
# df2 = pd.DataFrame(result["data"])

@st.cache_data
def load_data():
    url = "https://huggingface.co/Abhay936/Retail_pulse/resolve/main/feature_engineered_data.csv"
    return pd.read_csv(url)

df2 = load_data()



st.set_page_config(page_title="Sales Analytics",
                   layout="wide")

with st.sidebar:
    st.title("📈 Sales Analytics")
    cust_by = st.radio("Customers by : ",("Orders","Revenue"))
    top_x_cust = st.number_input("Top X Customer : ",min_value=1,value=10,step=5)
    prod_by = st.radio("Products by : ",("Qty_Sold","Revenue"))
    top_x_prod = st.number_input("Top X Products : ",min_value=1,value=10,step=5)
    trans_by = st.selectbox("Transction by : ",["Year","Month","Quater"])
    distribution = st.radio("Distribution by : ",("Quantity","Unit Price"))
    
    if distribution=="Quantity":
        max_quantity = st.number_input("Maximum Purchase Quantity",min_value=10,max_value=int(df2["Quantity"].max()),value=20,step=5)
    else:
        max_price = st.number_input("Distribution of X Price : ",min_value=10,value=50,step=10)

    
    rev_by_countries = st.slider("Top X Revenue Countries : ",min_value=10,max_value=41)

    Revenue_by_months_days = st.selectbox("Revenue by : ",["Monthly","Weekly"])


    
st.markdown(
    """
    <h1 style='text-align: center;'>
        📈 Sales Trends & Analysis
    </h1>
    <br>
    """,
    unsafe_allow_html=True
)


def update_layout(fig, title):
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor="center",   # <-- Add this
            y=0.97,             # <-- Optional
            yanchor="top",
            font=dict(size=24)
        ),
        template="simple_white",
        font=dict(size=16),
        height=450,
        margin=dict(l=60, r=30, t=90, b=60),   # Increase top margin
        xaxis=dict(
            showgrid=True,
            gridcolor="lightgray"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="lightgray"
        ),
        legend_title_text=""
    )
    return fig


col1,col2 = st.columns(2)



with col1:
    if cust_by == "Orders":
        # st.header("Top 10 customers by Orders")
        # st.image("charts/top_10_customers_orders_equal.png") 
        customer_orders = (
    df2.groupby("Customer ID", as_index=False)["Invoice"]
    .nunique()
    .rename(columns={"Invoice": "Orders"})
    .sort_values("Orders", ascending=False)
    .head(int(top_x_cust))
    )

        fig = px.bar(
    customer_orders,
    y="Orders",
    x="Customer ID",
    orientation="v",
    color="Orders",
    color_continuous_scale="Blues",
    text_auto=True,
    )

        fig.update_traces(textposition="outside")
        fig = update_layout(
            fig,
            f"Top {int(top_x_cust)} Customers by Orders"
        )

        st.plotly_chart(fig, use_container_width=True)








        i_1 = st.toggle("💡 Business Insights",key="i_1")
        if(i_1):
            st.markdown("""- <h5>Customer 14911 placed the highest number of orders (398), followed by 12748 (336).</h5>
- <h5>A small group of customers places orders very frequently, indicating a strong base of loyal and repeat buyers.</h5>
- <h5>Retaining these high-value customers through loyalty programs and personalized offers can improve long-term revenue.</h5>""",unsafe_allow_html=True)
        else:
            st.write()
    else:
        # st.header("Top 10 customers by Revenue")
        # st.image("charts/top_10_customers_equal.png")
        customer_revenue = (
        df2.groupby("Customer ID", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue", ascending=False)
    .head(int(top_x_cust))
    )

        fig = px.bar(
    customer_revenue,
    x="Revenue",
    y="Customer ID",
    orientation="h",
    color="Revenue",
    color_continuous_scale="Blues",
    text_auto=True,
    # title="Top "+str(top_x_cust)+" Customers by Revenue"
    )

        fig.update_traces(textposition="outside")
        fig = update_layout(
            fig,
            f"Top {int(top_x_cust)} Customers by Revenue"
        )

        st.plotly_chart(fig, use_container_width=True)
        i_8 = st.toggle("💡Business Insights",key="i_8")
        if i_8:
            st.markdown("""- <h5>Customer ID 18102 is the highest revenue-generating customer (580,987.04).</h5>
- <h5>The Top 10 customers contribute a significant share of total revenue.</h5>
- <h5>Revenue is concentrated among a few high-value customers.</h5>
- <h5>The company should focus on customer retention and loyalty programs for these customers.</h5>""",unsafe_allow_html=True)

with col2:
    if prod_by == "Qty_Sold":
        # st.header("Top 10 Products by Qty Sold")
        # st.image("charts/top_10_products_quantity_equal.png")

        product_quantity = (
    df2.groupby("Description", as_index=False)["Quantity"]
    .sum()
    .sort_values("Quantity", ascending=False)
    .head(top_x_prod)
    )

        fig = px.bar(
    product_quantity,
    x="Quantity",
    y="Description",
    orientation="h",
    color="Quantity",
    color_continuous_scale="Viridis",
    text_auto=True,
    # title="Top "+str(top_x_prod)+" Products by Quantity Sold"
    )

        fig.update_traces(textposition="outside")
        fig = update_layout(
            fig,
            f"Top {int(top_x_cust)} Products by Quantity Sold"
        )

        st.plotly_chart(fig, use_container_width=True)
        i_6 = st.toggle("💡Business Insights",key="i_6")
        if(i_6):
            st.markdown("""
                    - <h5>WORLD WAR 2 GLIDERS ASSTD DESIGNS is the best-selling product with 105,185 units sold.</h5>
                    - <h5>WHITE HANGING HEART T-LIGHT HOLDER is the second most sold product.</h5>
                    
                    - <h5>The Top 10 products have very high sales, showing they are the most popular items.</h5>
                    - <h5>These products should be kept well-stocked and promoted to maximize sales.</h5>
                    """,unsafe_allow_html=True)
        else:
            st.write()
    else:
        # st.header("Top 10 Products by Revenue")
        # st.image("charts/top_10_products_by_revenue_equal.png")
        product_rev = (
    df2.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(int(top_x_prod))
    .reset_index()
    )

        fig = px.bar(
    product_rev,
    x="Revenue",
    y="Description",
    orientation="h",
    text_auto=True,
    color="Revenue",
    color_continuous_scale="Blues"
    )



        fig = update_layout(
            fig,
            f"Top {int(top_x_cust)} Products by Revenue"
        )


        st.plotly_chart(fig,use_container_width=True)
        
        i_11 = st.toggle("💡Business Insights",key="i_11")
        if i_11:
            st.markdown("""
                        <ul>
                           <li><h5><b>REGENCY CAKESTAND 3 TIER</b> is the highest revenue-generating product.</h5></li>

                           <li><h5><b>WHITE HANGING HEART T-LIGHT HOLDER</b> ranks second in revenue.</h5></li>

                           <li><h5>Top products contribute most of the overall revenue.</h5></li>

                           <li><h5>Focus on these products to boost sales and inventory efficiency.</h5></li>
                        </ul>
                        """, unsafe_allow_html=True)
        else:
            st.write()




st.header("Transactions by Duration")
if trans_by=="Year":
    # st.write("Yearly Tansations")
    # st.image("charts/yearly_transactions.png")
    yearly = (
    df2.groupby("Year")
    .size()
    .reset_index(name="Transactions"))

    fig = px.line(
    yearly,
    x="Year",
    y="Transactions",
    markers=True
    )

    fig.update_traces(line_width=4,marker_size=9)

    fig = update_layout(fig,"Yearly Transaction Trend")

    st.plotly_chart(fig,use_container_width=True)

    
    i_2 = st.toggle("💡Business Insights",key="i_2")
    if(i_2):
            st.markdown("""
                - <h5>2010 recorded the highest number of transactions.</h5>
                - <h5>2011 maintained a similarly high transaction volume with a slight decline.</h5>
                - <h5>2009 had fewer transactions, likely due to partial year data.</h5>
                    """,unsafe_allow_html=True)
    else:
        st.write()
elif trans_by=="Month":
    # st.write("Monthly Transactions")
    # st.image("charts/monthly_transactions.png")
    monthly = (
    df2.groupby("Month")
    .size()
    .reset_index(name="Transactions"))

    fig = px.line(
    monthly,
    x="Month",
    y="Transactions",
    markers=True
    )

    fig.update_traces(line_width=4,marker_size=9)

    fig = update_layout(fig,"Monthly Transaction Trend")

    st.plotly_chart(fig,use_container_width=True)



    i_3 = st.toggle("💡Business Insights",key="i_3")
    if(i_3):
        st.markdown("""
                - <h5>Transaction volume generally increased toward the end of each year.</h5>
                - <h5>November 2011 recorded the highest number of transactions (63,168), indicating peak business activity.</h5>
                - <h5>Transaction counts were comparatively lower at the beginning of the year and highest during the festive/holiday season (October-November).</h5>""",unsafe_allow_html=True)
    else:
        st.write()
else:
    quaterly = (
    df2.groupby("Quarter")
    .size()
    .reset_index(name="Transactions"))

    fig = px.line(
    quaterly,
    x="Quarter",
    y="Transactions",
    markers=True
    )

    fig.update_traces(line_width=4,marker_size=9)

    fig = update_layout(fig,"Quarter Transaction Trend")

    st.plotly_chart(fig,use_container_width=True)
    i_10 = st.toggle("Business Insights",key="i_10")
    if i_10:
        st.markdown("""
- <h5>Transactions increased consistently from Q1 to Q4, showing steady business growth throughout the year.</h5>

- <h5>Q4 recorded the highest transaction volume, indicating peak customer activity during the year-end period.</h5>

- <h5>The sharp rise from Q3 to Q4 suggests strong seasonal demand, making Q4 the most critical quarter for sales.</h5>
""", unsafe_allow_html=True)
    else:
        st.write()




if distribution == "Quantity":
    # st.header("Mostly Common Pursched Quantity")
    # st.image("charts/quantity_distribution.png")
    

    quantity_dist = (
    df2[df2["Quantity"] <= max_quantity]["Quantity"]
    .value_counts()
    .sort_index()
    .reset_index()
    )

    quantity_dist.columns = ["Quantity", "Transactions"]

    fig = px.bar(
    quantity_dist,
    x="Quantity",
    y="Transactions",
    color="Transactions",
    color_continuous_scale="Viridis",
    text_auto=True,
    title=f"Most Common Purchase Quantities (1–{max_quantity})"
    )

    st.plotly_chart(fig, use_container_width=True)
    


    i_4 = st.toggle("💡Business Insights",key="i_4")
    if(i_4):
        st.markdown("""
                - <h5>Most transactions involve purchasing a small number of items.</h5>
                - <h5>Large purchase quantities occur less frequently and are identified as outliers.</h5>
                - <h5>These outliers may represent bulk purchases or wholesale orders</h5>
                """, unsafe_allow_html=True)
    else:
        st.write()
else:
    # st.header("Distribution of Unit Price")
    # st.image("charts/unit_price_distribution.png")
    fig = px.histogram(
    df2[df2["Price"] <= int(max_price)],
    x="Price",
    nbins=20,
    marginal="violin", 
    color_discrete_sequence=["#4F46E5"],
    title="Distribution of Unit Price"
    )

    st.plotly_chart(fig, use_container_width=True)

    i_5 = st.toggle("💡Business Insights",key="i_5")
    if(i_5):
        st.markdown("""
                - <h5>Most products are priced in the lower price range.</h5>
                - <h5>The price distribution is positively skewed due to a few high-priced transactions.</h5>
                - <h5>Price outliers were identified but retained, as they may represent genuine premium items or business-related charges.</h5>
                """, unsafe_allow_html=True)
    else:
        st.write()


col5,col6 = st.columns(2)

with col5:
    # st.header("Countries by Revenue")
    # st.image("charts/top_10_countries_equal.png")

    country = (
    df2.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(int(rev_by_countries))
    .reset_index()
)

    fig = px.bar(
    country,
    x="Country",
    y="Revenue",
    text_auto=".2s",
    color="Revenue",
    color_continuous_scale="Blues"
)

    fig = update_layout(fig,f"Top {int(rev_by_countries)}Countries by Revenue")

    st.plotly_chart(fig,use_container_width=True)

    i_7=st.toggle("💡Business Insights",key="i_7")
    if i_7:
       st.markdown("""- <h5>United Kingdom generated the highest sales revenue (14.39 million), far exceeding all other countries.</h5>
- <h5>EIRE and Netherlands are the second and third highest revenue-generating countries.</h5>
- <h5>Most of the revenue comes from a few countries, with the United Kingdom dominating sales.</h5>
- <h5>The company should maintain its strong presence in the UK while expanding in other high-potential markets.</h5>""",unsafe_allow_html=True)
    else:
       st.write()

with col6:
    # st.header("Revenue by Days of week")
    # st.image("charts/day_of_week_sales_equal.png")
    if Revenue_by_months_days == "Weekly":
        days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        sales = (
    df2.groupby("DayOfWeek")["Revenue"]
    .sum()
    .reindex(days)
    .reset_index()
    )
        fig = px.bar(
    sales,
    x="DayOfWeek",
    y="Revenue",
    text_auto=True,
    color="Revenue",
    color_continuous_scale="Blues"
    )
        
        fig = update_layout(fig,f"Revenue by Day of {Revenue_by_months_days}")
        st.plotly_chart(fig,use_container_width=True)
        i_9 = st.toggle("💡Business Insights",key="i_9")
        if i_9:
            st.markdown("""- <h5>Thursday recorded the highest sales revenue (3.75 million).</h5>
        - <h5>Tuesday and Wednesday also showed strong sales performance.</h5>
- <h5>Saturday had the lowest sales revenue (9.8 thousand).</h5>
- <h5>Sales are highest on weekdays, indicating customers purchase more during the working week.</h5>""",unsafe_allow_html=True)
        else:
            st.write()
    else:
        Months=["January","February","March","April","May","June","July","August","September","October","November","December"]
        sales = (
            df2.groupby("MonthName")["Revenue"].sum()
            .reindex(Months)
            .reset_index()
            )
        fig = px.bar(
    sales,
    x="MonthName",
    y="Revenue",
    text_auto=True,
    color="Revenue",
    color_continuous_scale="Blues"
    )
        
        fig = update_layout(fig,f"Revenue by Day of {Revenue_by_months_days}")
        st.plotly_chart(fig,use_container_width=True)
        i_9 = st.toggle("💡Business Insights",key="i_9")
        if i_9:
            st.markdown("""
- <h5>📈 November generated the highest revenue (~2.32M), while September and October also showed strong growth, indicating that the final quarter is the peak sales period.</h5>

- <h5>📉 February recorded the lowest revenue (~950K), suggesting a seasonal decline and highlighting an opportunity for targeted promotions to improve sales.</h5>

- <h5>📊 Revenue remained relatively stable from January to August before increasing significantly from September onward, reflecting strong year-end customer demand.</h5>
""", unsafe_allow_html=True)
        else:
            st.write()



    


st.success("""
**Summary:** A small number of products contribute the majority of total revenue. Prioritizing these high-performing products through effective inventory management, demand forecasting, and targeted promotions can significantly improve sales, customer satisfaction, and overall business profitability.
""")
