# 📊 Sales Analytics Executive Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://laxmi-sales-pulse.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Visualization-Plotly%20Express-orange.svg)](https://plotly.com/python/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An interactive, production-ready **Executive Sales Analytics Dashboard** designed for real-time business intelligence and revenue monitoring. Built with **Streamlit, Plotly Express, and an automated data pipeline supporting both Snowflake Data Cloud and cached enterprise datasets**.

---

## 🚀 Key Features

* **⚡ Executive KPI Metrics:** Real-time calculation of *Total Sales Revenue, Total Order Volume, Average Order Value (AOV)*, and *Active Customer Base*.
* **📈 Trend Analysis:** Dynamic monthly revenue trend analysis with period sorting and drill-down visualization.
* **🌍 Geospatial & Regional Breakdown:** Comparative revenue breakdown across geographical regions.
* **🥧 Category & Segment Analysis:** Interactive donut charts detailing product category contributions and customer segment performance (Consumer, Corporate, Home Office).
* **🏆 Top 10 Revenue Drivers:** Horizontal Pareto ranking of top revenue-generating enterprise products.
* **🎯 Dynamic Slicing & Dicing:** Real-time sidebar multi-dimensional filtering by *Year, Geographic Region, and Product Category*.
* **🔄 Hybrid Architecture:** Automatically leverages live **Snowflake Data Warehouse** connection when available, with an instant failover to local curated datasets for zero-downtime deployment.

---

## 🛠️ Tech Stack & Architecture

* **Frontend & Interactivity:** [Streamlit](https://streamlit.io/)
* **Data Visualization:** [Plotly Express](https://plotly.com/python/)
* **Data Processing:** Python, Pandas, NumPy
* **Data Warehousing & Modeling:** Snowflake Data Warehouse, dbt (Data Build Tool)

---

## 💻 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/laxmi345/sales-analytics-project.git
   cd sales-analytics-project
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the dashboard:**
   ```bash
   streamlit run app.py
   ```

---

## 🌐 Live Interactive Dashboard

👉 **Live Demo:** [laxmi-sales-pulse.streamlit.app](https://laxmi-sales-pulse.streamlit.app/)

## 🌐 Deploy to Streamlit Community Cloud (Free)

1. Fork or push changes to your GitHub repository.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/) with GitHub.
3. Select your repository: `laxmi345/sales-analytics-project`.
4. Set Main file path: `app.py`.
5. Click **Deploy!**

---

## 👤 Author & Ownership
* **Developer:** Laxmi Sahu ([@laxmi345](https://github.com/laxmi345))
* **Portfolio:** [portfolio-laxmisahu.vercel.app](https://portfolio-laxmisahu.vercel.app/)