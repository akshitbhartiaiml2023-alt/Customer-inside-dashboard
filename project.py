import pandas as pd
import streamlit as st
import plotly.express as px

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("clean_customers.csv")

# -------------------------
# CREATE TOTAL SPENDING
# -------------------------
df["Total_Spending"] = (
    df["MntWines"] + df["MntFruits"] + df["MntMeatProducts"] +
    df["MntFishProducts"] + df["MntSweetProducts"] + df["MntGoldProds"]
)

# -------------------------
# PAGE TITLE
# -------------------------
st.set_page_config(layout="wide")
st.title("📊 Customer Insights Dashboard")

# -------------------------
# KPI CARDS
# -------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", df["ID"].count())
col2.metric("Total Income", int(df["Income"].sum()))
col3.metric("Total Spending", int(df["Total_Spending"].sum()))
col4.metric("Total Purchases", int(df["NumStorePurchases"].sum()))

# -------------------------
# FILTERS (SIDEBAR)
# -------------------------
st.sidebar.header("Filters")

education = st.sidebar.multiselect(
    "Select Education", df["Education"].unique(), default=df["Education"].unique()
)

marital = st.sidebar.multiselect(
    "Select Marital Status", df["Marital_Status"].unique(), default=df["Marital_Status"].unique()
)

df = df[(df["Education"].isin(education)) & (df["Marital_Status"].isin(marital))]

# -------------------------
# CHARTS
# -------------------------
col1, col2 = st.columns(2)

# BAR CHART
bar = px.bar(
    df, x="Education", y="Total_Spending",
    title="Total Spending by Education",
    color="Education"
)
col1.plotly_chart(bar, use_container_width=True)

# PIE CHART
pie = px.pie(
    df, names="Marital_Status",
    title="Customers by Marital Status"
)
col2.plotly_chart(pie, use_container_width=True)

# -------------------------
# LINE CHART
# -------------------------
df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], errors='coerce')

line = px.line(
    df, x="Dt_Customer", y="Total_Spending",
    title="Spending Over Time"
)

st.plotly_chart(line, use_container_width=True)

# -------------------------
# TABLE
# -------------------------
st.subheader("Customer Data")
st.dataframe(df.head(50))