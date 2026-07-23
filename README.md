🛍️ Retail Pulse

An AI-Powered Retail Analytics Platform for Business Intelligence, Customer Analytics, Demand Forecasting, and Inventory Optimization.

Retail Pulse is an end-to-end Data Science application that transforms raw retail transaction data into actionable business insights. It integrates Machine Learning, FastAPI, MongoDB Atlas, and Streamlit to provide interactive dashboards and real-time predictions for smarter business decision-making.

⸻

🚀 Features

📊 Sales Analytics

* Interactive business dashboard
* Revenue and sales trend analysis
* Monthly & yearly sales performance
* Top-selling products
* Country-wise sales analysis
* Customer purchase behavior
* Interactive Plotly visualizations

👥 Customer Segmentation

* RFM (Recency, Frequency, Monetary) Analysis
* K-Means Clustering
* Customer segment prediction
* Personalized business recommendations

🤖 Customer Churn Prediction

* Predict customers likely to churn
* Churn probability estimation
* Customer retention insights
* ML-powered prediction API

📈 Product Demand Forecasting

* Product-wise demand prediction
* Historical sales analysis
* Future demand estimation
* Data-driven inventory planning

📦 Inventory Optimization

* Current stock monitoring
* Safety stock estimation
* Suggested reorder quantity
* Inventory optimization recommendations

⸻

🛠️ Tech Stack

Frontend

* Streamlit
* Plotly
* Pandas
* Matplotlib
* Seaborn

Backend

* FastAPI
* Uvicorn
* REST API

Database

* MongoDB Atlas

Machine Learning

* Scikit-Learn
* Random Forest
* K-Means Clustering
* RFM Analysis
* Joblib

Deployment

* Streamlit Community Cloud
* Render
* MongoDB Atlas

⸻

📂 Project Structure

Retail-Pulse/
│
├── app/
│   ├── main.py
│   └── pages/
│       ├── Dashboard.py
│       ├── Sales_Analytics.py
│       ├── Prediction.py
│       ├── Segments.py
│       ├── Forecasting.py
│       └── Inventory.py
│
├── backend/
│   ├── models/
│   ├── routers/
│   ├── database.py
│   └── main.py
│
├── dataset/
├── requirements.txt
├── runtime.txt
├── .python-version
├── .gitignore
└── README.md

⸻

🤖 Machine Learning Models

Module	Algorithm
Customer Churn Prediction	Random Forest Classifier
Customer Segmentation	K-Means Clustering
Product Demand Forecasting	Random Forest Regressor
Inventory Recommendation	Rule-Based Logic

⸻

🌐 API Endpoints

Endpoint	Description
/data_load/dashboard	Dashboard data
/customer-segmentation/predict	Customer segmentation
/churn/predict-cust_ID	Customer churn prediction
/forecast/predict	Sales forecasting
/forecast/product	Product demand prediction
/inventory/predict	Inventory optimization

⸻

📊 Dashboard Modules

* 🏠 Dashboard
* 📊 Sales Analytics
* 👥 Customer Segmentation
* 🤖 Customer Churn Prediction
* 📈 Product Demand Forecasting
* 📦 Inventory Optimization

⸻

💼 Business Value

* Improve sales performance using analytics
* Identify valuable customer segments
* Predict customer churn before it happens
* Forecast future product demand
* Optimize inventory and reduce stock-outs
* Support data-driven business decisions

⸻

⚙️ Installation

Clone Repository

git clone https://github.com/Abhay936/Retail-Pulse.git
cd Retail-Pulse

Create Virtual Environment

python -m venv venv

Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

⸻

🐍 Python Version

This project is developed and tested using Python 3.12.13.

The repository includes:

.python-version

with the following content:

3.12.13

⸻

▶️ Run Backend

cd backend
uvicorn main:app --reload

Backend URL

http://127.0.0.1:8000

API Documentation

http://127.0.0.1:8000/docs

⸻

▶️ Run Streamlit Frontend

cd app
streamlit run main.py

⸻

📷 Screenshots

Add your dashboard screenshots here.

Example:

images/dashboard.png
images/sales.png
images/churn.png
images/forecast.png
images/inventory.png

⸻

📈 Future Improvements

* Sales forecasting using deep learning
* AI-powered recommendation engine
* Role-based authentication
* Automated report generation
* Real-time business monitoring
* Cloud-native deployment

⸻

👨‍💻 Author

Abhay Sharma

B.Tech (Computer Science) | Data Science & Machine Learning Enthusiast

Skills

* Python
* Machine Learning
* FastAPI
* Streamlit
* MongoDB
* Data Analytics
* REST APIs
* Data Visualization

GitHub:
https://github.com/Abhay936

LinkedIn:
 https://www.linkedin.com/in/abhay-sharma-7252ab328

⸻

⭐ Support

If you found this project useful, consider giving it a Star ⭐ on GitHub.
