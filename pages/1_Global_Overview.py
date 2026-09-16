import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌍 Global GDP Overview")

# Load dataset
df = pd.read_csv("data/gdp_cleaned.csv")

# -----------------------------
# Latest Year
# -----------------------------
latest_year = df["Year"].max()

# Global GDP from World row
world_row = df[(df["Country"] == "World") & (df["Year"] == latest_year)]

global_gdp = world_row["GDP"].values[0]

# -----------------------------
# Top Economy (remove aggregates)
# -----------------------------
aggregates = [
    "World",
    "Advanced economies",
    "Emerging market and developing economies",
    "Major advanced economies (G7)",
    "European Union",
    "ASEAN-5"
]

countries_df = df[~df["Country"].isin(aggregates)]

latest_countries = countries_df[countries_df["Year"] == latest_year]

top_country = latest_countries.sort_values("GDP", ascending=False).iloc[0]

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Global GDP",
    f"{global_gdp/1000:.1f} Trillion USD"
)

col2.metric(
    "Top Economy",
    top_country["Country"]
)

col3.metric(
    "Top Economy GDP",
    f"{top_country['GDP']/1000:.1f} Trillion USD"
)

# -----------------------------
# Global GDP Trend
# -----------------------------
st.subheader("📈 Global GDP Growth Trend")

world_trend = df[df["Country"] == "World"].copy()

world_trend["GDP_Trillion"] = world_trend["GDP"] / 1000

fig = px.line(
    world_trend,
    x="Year",
    y="GDP_Trillion",
    markers=True,
    labels={"GDP_Trillion": "GDP (Trillion USD)"}
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Top 10 Economies
# -----------------------------
st.subheader("🏆 Top 10 Economies")

top10 = latest_countries.sort_values("GDP", ascending=False).head(10)

top10["Global Share (%)"] = (top10["GDP"] / global_gdp) * 100

table = top10[["Country", "GDP", "Global Share (%)"]].copy()

table["GDP (Billion USD)"] = table["GDP"].map("{:,.0f}".format)
table["Global Share (%)"] = table["Global Share (%)"].map("{:.2f}".format)

table = table.drop(columns=["GDP"])

st.dataframe(table, use_container_width=True)

# -----------------------------
# GDP Share Chart
# -----------------------------
st.subheader("📊 Share of Global GDP")

fig2 = px.bar(
    top10,
    x="Country",
    y="Global Share (%)",
    labels={"Global Share (%)": "Global GDP Share (%)"},
    color="Global Share (%)"
)

st.plotly_chart(fig2, use_container_width=True)