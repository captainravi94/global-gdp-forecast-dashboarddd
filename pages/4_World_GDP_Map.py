import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("🌍 Global GDP Map")

# Load data
map_df = pd.read_csv("data/world_gdp_map.csv")

# Clean country names
map_df["Country"] = (
    map_df["Country"]
    .astype(str)
    .str.strip()
)

# Remove missing/invalid countries
map_df = map_df[
    map_df["Country"].notna() &
    (map_df["Country"] != "") &
    (map_df["Country"] != "nan")
].copy()

# Make sure GDP is numeric
map_df["GDP"] = pd.to_numeric(
    map_df["GDP"],
    errors="coerce"
)

# Remove rows where GDP is missing
map_df = map_df.dropna(subset=["GDP"])

# Log transform GDP
map_df["GDP_log"] = np.log10(map_df["GDP"].clip(lower=0) + 1)

st.subheader("Global GDP Distribution (2026)")

fig = px.choropleth(
    map_df,
    locations="Country",
    locationmode="country names",
    color="GDP_log",
    hover_name="Country",
    hover_data={
        "GDP": ":,.0f",
        "GDP_log": False
    },
    color_continuous_scale="Viridis",
    labels={
        "GDP": "GDP (Billion USD)",
        "GDP_log": "GDP Scale (Log)"
    }
)

fig.update_layout(
    coloraxis_colorbar=dict(
        title="GDP (Log Scale)"
    ),
    margin=dict(l=0, r=0, t=30, b=0)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.caption(
    "GDP values are expressed in Billion USD. "
    "Log scale is used for better visualization."
)
