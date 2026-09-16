import os
import pandas as pd
import streamlit as st
import plotly.express as px

# -------------------------------
# LOAD DATA + FIX YEARS (2024–2030)
# -------------------------------
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.dirname(__file__))  
    file_path = os.path.join(base_path, "data", "gdp_forecast_2030.csv")

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    all_years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
    df_full = []

    for country in df["Country"].unique():
        temp = df[df["Country"] == country].copy()
        temp = temp.set_index("Year").reindex(all_years)
        temp["Country"] = country

        temp["GDP_Predicted"] = temp["GDP_Predicted"].interpolate(method="linear")
        temp["GDP_Predicted"] = temp["GDP_Predicted"].bfill()
        temp["GDP_Predicted"] = temp["GDP_Predicted"].ffill()

        temp = temp.reset_index()
        df_full.append(temp)

    return pd.concat(df_full)

df = load_data()
gdp_col = "GDP_Predicted"

# -------------------------------
# TITLE
# -------------------------------
st.title("🌍 Global Economic Scenario Intelligence Platform")

# -------------------------------
# YEAR SELECTION
# -------------------------------
year = st.selectbox("📅 Select Year", sorted(df["Year"].unique()))
df_year = df[df["Year"] == year]

# -------------------------------
# SCENARIO
# -------------------------------
st.subheader("⚡ Scenario Selection")

scenario = st.radio(
    "Choose Scenario",
    ["Custom", "War Shock", "Recession", "Economic Boom"]
)

if scenario == "War Shock":
    oil, inflation, interest, trade = 35, 6, 4, -5
elif scenario == "Recession":
    oil, inflation, interest, trade = 10, 7, 6, -7
elif scenario == "Economic Boom":
    oil, inflation, interest, trade = -5, 2, 2, 6
else:
    oil = st.slider("Oil Change (%)", -20, 50, 20)
    inflation = st.slider("Inflation (%)", 0, 10, 3)
    interest = st.slider("Interest Rate (%)", 0, 10, 2)
    trade = st.slider("Trade Growth (%)", -10, 10, -2)

# -------------------------------
# MODEL
# -------------------------------
def model(df, oil, inflation, interest, trade):
    df = df.copy()
    df["Impact_%"] = (
        (-0.03 * oil) +
        (-0.5 * inflation) +
        (-0.3 * interest) +
        (0.6 * trade)
    )
    df["Adjusted_GDP"] = df[gdp_col] * (1 + df["Impact_%"] / 100)
    return df

df_sim = model(df_year, oil, inflation, interest, trade)

# -------------------------------
# GLOBAL IMPACT
# -------------------------------
st.subheader("🌐 Global Impact")

base = df_year[gdp_col].sum()
new = df_sim["Adjusted_GDP"].sum()

st.metric("Global GDP", f"{new:,.2f}", delta=f"{new-base:,.2f}")

# -------------------------------
# ECONOMIC NARRATIVE
# -------------------------------
st.subheader("🧠 Economic Narrative")

if scenario == "War Shock":
    st.warning("Oil shock → cost ↑ → inflation ↑ → GDP ↓")
elif scenario == "Recession":
    st.warning("Demand ↓ → investment ↓ → GDP ↓")
elif scenario == "Economic Boom":
    st.success("Trade ↑ → production ↑ → GDP ↑")
else:
    st.info("Custom scenario applied")

# -------------------------------
# COUNTRY ANALYSIS
# -------------------------------
st.subheader("🌍 Country Analysis")

country = st.selectbox("Select Country", df_year["Country"].unique())

base_val = df_year[df_year["Country"] == country][gdp_col].iloc[0]
scenario_val = df_sim[df_sim["Country"] == country]["Adjusted_GDP"].iloc[0]

st.metric(country, f"{scenario_val:,.2f}", delta=f"{scenario_val-base_val:,.2f}")

# -------------------------------
# TOP ECONOMIES
# -------------------------------
st.subheader("📊 Top Economies")

top10 = df_year.sort_values(by=gdp_col, ascending=False).head(10)
merged = top10.merge(df_sim[["Country", "Adjusted_GDP"]], on="Country")

fig = px.bar(merged, x="Country", y=[gdp_col, "Adjusted_GDP"], barmode="group")
st.plotly_chart(fig)

# -------------------------------
# MAP
# -------------------------------
st.subheader("🗺️ Global Map")

fig_map = px.choropleth(df_sim, locations="Country",
                       locationmode="country names",
                       color="Adjusted_GDP")

st.plotly_chart(fig_map)

# -------------------------------
# SHOCK DECOMPOSITION (FIXED)
# -------------------------------
st.subheader("📉 Shock Decomposition")

oil_c = -0.03 * oil
inf_c = -0.5 * inflation
int_c = -0.3 * interest
trade_c = 0.6 * trade

decomp = pd.DataFrame({
    "Factor": ["Oil", "Inflation", "Interest", "Trade"],
    "Contribution": [oil_c, inf_c, int_c, trade_c]
})

decomp["Abs"] = decomp["Contribution"].abs()

fig_pie = px.pie(decomp, names="Factor", values="Abs", hole=0.4)
st.plotly_chart(fig_pie)

st.dataframe(decomp)

# -------------------------------
# SENSITIVITY (NEW)
# -------------------------------
st.subheader("📈 Sensitivity Analysis")

sens = pd.DataFrame({
    "Factor": ["Oil", "Inflation", "Interest", "Trade"],
    "Sensitivity": [-0.03, -0.5, -0.3, 0.6]
})

fig_sens = px.bar(sens, x="Factor", y="Sensitivity")
st.plotly_chart(fig_sens)

# -------------------------------
# RISK SCORE
# -------------------------------
st.subheader("⚠️ Risk Level")

risk = abs(df_sim["Impact_%"].mean())

if risk > 5:
    st.error("High Risk")
elif risk > 2:
    st.warning("Medium Risk")
else:
    st.success("Low Risk")

# -------------------------------
# REPORT
# -------------------------------
st.subheader("📄 Download Report")

report = f"""
Scenario: {scenario}
Year: {year}

Oil: {oil}
Inflation: {inflation}
Interest: {interest}
Trade: {trade}

Risk: {risk}
"""

st.download_button("Download Report", report, "report.txt")

st.subheader("📊 Impact Breakdown (Advanced)")

fig_bar = px.bar(
    decomp,
    x="Factor",
    y="Contribution",
    color="Contribution",
    title="Positive vs Negative Impact"
)

st.plotly_chart(fig_bar)