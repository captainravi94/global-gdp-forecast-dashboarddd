import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Global Economic Insights")

# Load data
df = pd.read_csv("data/gdp_cleaned.csv")

latest_year = df["Year"].max()

# Remove aggregate regions
aggregates = [
    "World",
    "Advanced economies",
    "Emerging market and developing economies",
    "Major advanced economies (G7)",
    "European Union",
    "ASEAN-5"
]

df_countries = df[~df["Country"].isin(aggregates)]

latest_data = df_countries[df_countries["Year"] == latest_year]

# -----------------------------------------------------
# 1️⃣ Global GDP Growth Rate
# -----------------------------------------------------

st.subheader("📈 Global GDP Growth Rate")

world_df = df[df["Country"] == "World"].copy()

world_df["Growth"] = world_df["GDP"].pct_change()*100

fig1 = px.line(
    world_df,
    x="Year",
    y="Growth",
    markers=True,
    labels={"Growth":"Growth Rate (%)"}
)

st.plotly_chart(fig1,use_container_width=True)

st.caption("Annual percentage change in global GDP.")

# -----------------------------------------------------
# 2️⃣ Fastest Growing Economies
# -----------------------------------------------------

st.subheader("🚀 Top 10 Fastest Growing Economies")

df_growth = df_countries.copy()

df_growth["Growth"] = df_growth.groupby("Country")["GDP"].pct_change()*100

latest_growth = df_growth[df_growth["Year"]==latest_year]

top_growth = latest_growth.sort_values("Growth",ascending=False).head(10)

fig2 = px.bar(
    top_growth,
    x="Country",
    y="Growth",
    color="Growth",
    labels={"Growth":"GDP Growth (%)"}
)

st.plotly_chart(fig2,use_container_width=True)

# -----------------------------------------------------
# 3️⃣ Key Reasons Behind Growth
# -----------------------------------------------------

st.subheader("🧠 Key Drivers Behind Top 10 GDP Growth")

reasons = {
"India":"Digital economy expansion, infrastructure investment and strong domestic demand.",
"Vietnam":"Export driven manufacturing and strong foreign investment inflows.",
"Bangladesh":"Rapid textile export growth and manufacturing expansion.",
"Indonesia":"Commodity exports and strong domestic consumption.",
"Philippines":"Service sector growth and remittance inflows.",
"China":"Industrial production and technology sector expansion.",
"Ethiopia":"Infrastructure investment and agriculture modernization.",
"Rwanda":"Economic reforms and services sector expansion.",
}

for country in top_growth["Country"]:
    
    reason = reasons.get(
        country,
        "Growth driven by trade expansion, investment and structural reforms."
    )
    
    st.write(f"**{country}** — {reason}")

# -----------------------------------------------------
# 4️⃣ Global GDP Treemap
# -----------------------------------------------------

st.subheader("🌍 Global GDP Treemap")

top20 = latest_data.sort_values("GDP",ascending=False).head(20)

fig3 = px.treemap(
    top20,
    path=["Country"],
    values="GDP",
    title="Top 20 Economies by GDP"
)

st.plotly_chart(fig3,use_container_width=True)

# -----------------------------------------------------
# 5️⃣ Largest Economies
# -----------------------------------------------------

st.subheader("🏦 Top 10 Economies by GDP")

top_gdp = latest_data.sort_values("GDP",ascending=False).head(10)

fig4 = px.bar(
    top_gdp,
    x="Country",
    y="GDP",
    labels={"GDP":"GDP (Billion USD)"},
    color="GDP"
)

st.plotly_chart(fig4,use_container_width=True)

# -----------------------------------------------------
# 6️⃣ GDP Growth Heatmap
# -----------------------------------------------------

st.subheader("🔥 GDP Growth Heatmap (Top Economies)")

top10_countries = latest_data.sort_values("GDP",ascending=False).head(10)["Country"]

heatmap_df = df[df["Country"].isin(top10_countries)]

pivot = heatmap_df.pivot(index="Country",columns="Year",values="GDP")

fig,ax = plt.subplots(figsize=(12,6))

sns.heatmap(
    pivot,
    cmap="YlGnBu",
    linewidths=.5
)

st.pyplot(fig)