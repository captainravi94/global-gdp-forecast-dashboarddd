import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Country GDP Analysis")

# Load dataset
df = pd.read_csv("data/gdp_cleaned.csv")

# Clean country column
df["Country"] = df["Country"].astype(str)
df = df[df["Country"] != "nan"]

# Country selector
country = st.selectbox(
    "Select Country",
    sorted(df["Country"].unique())
)

# Filter data
country_df = df[df["Country"] == country]

st.subheader(f"{country} GDP Trend")

# GDP Trend Chart
fig = px.line(
    country_df,
    x="Year",
    y="GDP",
    markers=True,
    labels={
        "GDP": "GDP (Billion USD)",
        "Year": "Year"
    }
)

fig.update_layout(
    yaxis_title="GDP (Billion USD)",
    xaxis_title="Year"
)

st.plotly_chart(fig, use_container_width=True)

st.caption("GDP values are expressed in Billion USD.")

# GDP Growth Rate
country_df["Growth Rate (%)"] = country_df["GDP"].pct_change() * 100

st.subheader(f"{country} GDP Growth Rate")

fig2 = px.bar(
    country_df,
    x="Year",
    y="Growth Rate (%)",
    labels={
        "Growth Rate (%)": "GDP Growth (%)",
        "Year": "Year"
    }
)

fig2.update_layout(
    yaxis_title="GDP Growth (%)",
    xaxis_title="Year"
)

st.plotly_chart(fig2, use_container_width=True)

st.caption("GDP growth rate is calculated as the year-over-year percentage change in GDP.")