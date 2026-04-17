import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Analyzer", layout="wide")

st.title("📊 Sales Data Analyzer Agent")

# 1. Upload file
file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if file:
    # read file
    if file.name.endswith("csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.subheader("📁 Dataset Preview")
    st.dataframe(df)

    # Basic cleaning (optional)
    df.columns = [col.lower() for col in df.columns]

    # 2. Metrics
    st.subheader("📊 Key Metrics")

    if "sales" in df.columns:
        st.metric("Total Sales", df["sales"].sum())
        st.metric("Average Sales", df["sales"].mean())

    # 3. Top products
    if "product" in df.columns and "sales" in df.columns:
        top_products = df.groupby("product")["sales"].sum().sort_values(ascending=False).head(10)

        st.subheader("🏆 Top Products")

        fig, ax = plt.subplots()
        top_products.plot(kind="bar", ax=ax)
        st.pyplot(fig)

    # 4. Region analysis
    if "region" in df.columns and "sales" in df.columns:
        region_sales = df.groupby("region")["sales"].sum()

        st.subheader("🌍 Region Analysis")

        fig2, ax2 = plt.subplots()
        region_sales.plot(kind="bar", ax=ax2, color="orange")
        st.pyplot(fig2)

    # 5. Simple Q&A (rule-based)
    st.subheader("💬 Ask Question")

    question = st.text_input("Ask something about your data:")

    if question:
        question = question.lower()

        if "total" in question and "sales" in question:
            st.success(f"Total Sales: {df['sales'].sum()}")

        elif "top product" in question:
            top = df.groupby("product")["sales"].sum().idxmax()
            st.success(f"Top Product: {top}")

        elif "region" in question:
            top_region = df.groupby("region")["sales"].sum().idxmax()
            st.success(f"Top Region: {top_region}")

        else:
            st.warning("Savolni aniqroq yozing (masalan: top product, total sales)")