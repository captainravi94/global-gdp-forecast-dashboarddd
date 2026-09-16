import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("🌍 Global GDP Map")

map_df = pd.read_csv("data/world_gdp_map.csv")

# Log transform GDP to improve color distribution
map_df["GDP_log"] = np.log10(map_df["GDP"] + 1)

st.subheader("Global GDP Distribution (2026)")

fig = px.choropleth(
    map_df,
    locations="Country",
    locationmode="country names",
    color="GDP_log",
    hover_name="Country",
    hover_data={"GDP":":,.0f"},
    color_continuous_scale="Viridis",
    labels={"GDP_log": "GDP Scale (Log)", "GDP": "GDP (Billion USD)"},
    title="Global GDP Distribution (2026)"
)

fig.update_layout(
    coloraxis_colorbar=dict(
        title="GDP (Log Scale)"
    )
)

st.plotly_chart(fig, use_container_width=True)

st.caption("GDP values are expressed in Billion USD. Log scale is used for better visualization.")