import streamlit as st
import requests

st.set_page_config(
    page_title="Inventory Optimization",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inventory Optimization")
st.caption("Optimize inventory using forecasted product demand.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    stock_code = st.text_input(
        "📦 Stock Code",
        placeholder="Example: 22026 or 85123A"
    )

    current_stock = st.number_input(
        "Current Stock",
        min_value=0,
        value=100
    )

with col2:
    safety_stock = st.number_input(
        "Safety Stock",
        min_value=0,
        value=50
    )

    st.number_input(
        "Lead Time (Days)",
        value=7,
        disabled=True
    )

st.divider()

if st.button("📈 Optimize Inventory", use_container_width=True):

    if stock_code.strip() == "":
        st.warning("Please enter a Stock Code.")
        st.stop()

    payload = {
        "StockCode": stock_code.strip(),
        "CurrentStock": current_stock,
        "SafetyStock": safety_stock
    }

    try:

        with st.spinner("Analyzing Inventory..."):

            response = requests.post(
                "https://retail-pulse-ht37.onrender.com/inventory/predict",
                json=payload,
                timeout=60
            )

        if response.status_code == 200:
             
             result = response.json()
             st.success("✅ Inventory Analysis Completed")
             
             c1, c2, c3 = st.columns(3)
             
             c1.metric("📦 Stock Code", result["StockCode"])
             c2.metric("⚠️ Stock-Out Risk", f'{result["StockOutRisk"]:.2f}%')
             c3.metric("📊 Status", result["InventoryStatus"])
             
             st.divider()
             
             c4, c5, c6 = st.columns(3)
             
             c4.metric("💰 Last Revenue", f'₹ {result["LastRevenue"]:.2f}')
             c5.metric("🛒 Last Order Value", f'₹ {result["LastOrderValue"]:.2f}')
             c6.metric("🧺 Basket Size", result["LastBasketSize"])
             st.divider()
             
             if result["InventoryStatus"] == "Safe":
                st.success("🟢 Inventory level is sufficient.")
             else:
                st.warning("🟠 Inventory requires attention.")
                
            

            

        else:
            st.error(f"API Error ({response.status_code})")
            st.json(response.json())

    except requests.exceptions.ConnectionError:
        st.error("❌ FastAPI server is not running.")

    except Exception as e:
        st.error(str(e))