import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales AI Dashboard", layout="wide")

# ======================
# 🎨 HEADER UI
# ======================
st.markdown("""
    <style>
    .main-title {
        font-size:40px;
        font-weight:bold;
        color:#4CAF50;
    }
    .card {
        padding:20px;
        border-radius:15px;
        background-color:#f5f5f5;
        text-align:center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>📊 Sales AI Analyzer Agent</div>", unsafe_allow_html=True)
st.write("Upload CSV/Excel and analyze your business like BI tool 🚀")

# ======================
# 📂 UPLOAD FILE
# ======================
file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

if file:
    if file.name.endswith("csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.success("File uploaded successfully!")

    # lowercase columns
    df.columns = [c.lower() for c in df.columns]

    # ======================
    # 📊 KPI METRICS
    # ======================
    col1, col2, col3 = st.columns(3)

    if "sales" in df.columns:
        col1.metric("💰 Total Sales", f"{df['sales'].sum():,.0f}")
        col2.metric("📊 Average Sales", f"{df['sales'].mean():,.0f}")
        col3.metric("📦 Max Sale", f"{df['sales'].max():,.0f}")

    st.divider()

    # ======================
    # 📁 DATA PREVIEW
    # ======================
    with st.expander("📁 View Dataset"):
        st.dataframe(df)

    # ======================
    # 🏆 TOP PRODUCTS
    # ======================
    if "product" in df.columns and "sales" in df.columns:
        st.subheader("🏆 Top Products")

        top_products = df.groupby("product")["sales"].sum().sort_values(ascending=False).head(10)

        fig, ax = plt.subplots()
        top_products.plot(kind="bar", ax=ax)
        st.pyplot(fig)

    # ======================
    # 🌍 REGION ANALYSIS
    # ======================
    if "region" in df.columns and "sales" in df.columns:
        st.subheader("🌍 Region Analysis")

        region = df.groupby("region")["sales"].sum()

        fig2, ax2 = plt.subplots()
        region.plot(kind="bar", ax=ax2)
        st.pyplot(fig2)

    # ======================
    # 📅 DATE ANALYSIS
    # ======================
    if "date" in df.columns:
        st.subheader("📅 Time Trend")

        df["date"] = pd.to_datetime(df["date"])
        time_sales = df.groupby("date")["sales"].sum()

        fig3, ax3 = plt.subplots()
        time_sales.plot(ax=ax3)
        st.pyplot(fig3)

    st.divider()

    # ======================
    # 💬 SMART Q&A ENGINE
    # ======================
    st.subheader("💬 AI Analyst (Ask Questions)")

    question = st.text_input("Ask: top product? total sales? best region?")

    if question:
        q = question.lower()

        if "total" in q:
            st.success(f"💰 Total Sales: {df['sales'].sum():,.0f}")

        elif "average" in q:
            st.success(f"📊 Average Sales: {df['sales'].mean():,.0f}")

        elif "top product" in q:
            result = df.groupby("product")["sales"].sum().idxmax()
            st.success(f"🏆 Top Product: {result}")

        elif "region" in q:
            result = df.groupby("region")["sales"].sum().idxmax()
            st.success(f"🌍 Top Region: {result}")

        elif "max" in q:
            st.success(f"📦 Max Sale: {df['sales'].max():,.0f}")

        else:
            st.warning("Try: 'top product', 'total sales', 'best region'")

    # ======================
    # 📥 DOWNLOAD REPORT
    # ======================
    st.download_button(
        label="📥 Download Clean Data",
        data=df.to_csv(index=False),
        file_name="clean_sales_data.csv",
        mime="text/csv"
    )

else:
    st.info("⬆ Upload CSV or Excel file to start analysis")