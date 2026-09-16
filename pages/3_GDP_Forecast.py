import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🔮 GDP Forecast (2027–2030)")

# Load datasets
hist = pd.read_csv("data/gdp_cleaned.csv")
forecast = pd.read_csv("data/gdp_forecast_2030.csv")

# Clean country column
hist["Country"] = hist["Country"].astype(str)
hist = hist[hist["Country"] != "nan"]

forecast["Country"] = forecast["Country"].astype(str)
forecast = forecast[forecast["Country"] != "nan"]

# Country selector
country = st.selectbox(
    "Select Country",
    sorted(hist["Country"].unique())
)

# Filter data
hist_country = hist[hist["Country"] == country]
forecast_country = forecast[forecast["Country"] == country]

st.subheader(f"{country} GDP Historical vs Forecast")

# Create chart
fig = px.line(
    hist_country,
    x="Year",
    y="GDP",
    markers=True,
    labels={
        "GDP": "GDP (Billion USD)",
        "Year": "Year"
    }
)

# Add forecast line
fig.add_scatter(
    x=forecast_country["Year"],
    y=forecast_country["GDP_Predicted"],
    mode="lines+markers",
    name="Forecast (Billion USD)"
)

fig.update_layout(
    yaxis_title="GDP (Billion USD)",
    xaxis_title="Year"
)

st.plotly_chart(fig, use_container_width=True)

st.caption("GDP values are expressed in Billion USD.")