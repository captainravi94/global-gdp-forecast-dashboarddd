import os
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import requests


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Global Economic Scenario Intelligence",
    page_icon="🌍",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    base_path = os.path.dirname(os.path.dirname(__file__))

    file_path = os.path.join(
        base_path,
        "data",
        "gdp_forecast_2030.csv"
    )

    df = pd.read_csv(file_path)

    df.columns = df.columns.str.strip()

    # Clean country names
    df["Country"] = (
        df["Country"]
        .astype(str)
        .str.strip()
    )

    # Convert numeric columns
    df["Year"] = pd.to_numeric(
        df["Year"],
        errors="coerce"
    )

    df["GDP_Predicted"] = pd.to_numeric(
        df["GDP_Predicted"],
        errors="coerce"
    )

    # Remove invalid rows
    df = df.dropna(
        subset=["Country", "Year", "GDP_Predicted"]
    )

    all_years = [
        2024,
        2025,
        2026,
        2027,
        2028,
        2029,
        2030
    ]

    df_full = []

    for country in df["Country"].unique():

        temp = df[
            df["Country"] == country
        ].copy()

        # If duplicate country-year observations exist,
        # keep the first one.
        temp = temp.drop_duplicates(
            subset=["Year"]
        )

        temp = temp.set_index("Year")

        temp = temp.reindex(all_years)

        temp["Country"] = country

        temp["GDP_Predicted"] = (
            temp["GDP_Predicted"]
            .interpolate(method="linear")
            .bfill()
            .ffill()
        )

        temp = temp.reset_index()

        df_full.append(temp)

    return pd.concat(
        df_full,
        ignore_index=True
    )


df = load_data()

gdp_col = "GDP_Predicted"


# =========================================================
# COUNTRY → ISO-3 CODES
# =========================================================

country_codes = {

    "Albania": "ALB",
    "Algeria": "DZA",
    "Angola": "AGO",
    "Argentina": "ARG",
    "Armenia": "ARM",
    "Australia": "AUS",
    "Austria": "AUT",
    "Azerbaijan": "AZE",

    "Bahamas, The": "BHS",
    "Bahrain": "BHR",
    "Bangladesh": "BGD",
    "Barbados": "BRB",
    "Belarus": "BLR",
    "Belgium": "BEL",
    "Belize": "BLZ",
    "Benin": "BEN",
    "Bhutan": "BTN",
    "Bolivia": "BOL",
    "Bosnia and Herzegovina": "BIH",
    "Botswana": "BWA",
    "Brazil": "BRA",
    "Brunei Darussalam": "BRN",
    "Bulgaria": "BGR",
    "Burkina Faso": "BFA",
    "Burundi": "BDI",

    "Cambodia": "KHM",
    "Cameroon": "CMR",
    "Canada": "CAN",
    "Central African Republic": "CAF",
    "Chad": "TCD",
    "Chile": "CHL",
    "China": "CHN",
    "China, People's Republic of": "CHN",
    "Colombia": "COL",
    "Comoros": "COM",
    "Congo, Dem. Rep. of the": "COD",
    "Congo, Republic of": "COG",
    "Costa Rica": "CRI",
    "Croatia": "HRV",
    "Cyprus": "CYP",
    "Czech Republic": "CZE",
    "Côte d'Ivoire": "CIV",

    "Denmark": "DNK",
    "Djibouti": "DJI",
    "Dominican Republic": "DOM",

    "Ecuador": "ECU",
    "Egypt": "EGY",
    "El Salvador": "SLV",
    "Estonia": "EST",
    "Eswatini": "SWZ",
    "Ethiopia": "ETH",

    "Fiji": "FJI",
    "Finland": "FIN",
    "France": "FRA",

    "Gabon": "GAB",
    "Gambia, The": "GMB",
    "Georgia": "GEO",
    "Germany": "DEU",
    "Ghana": "GHA",
    "Greece": "GRC",
    "Guatemala": "GTM",
    "Guinea": "GIN",
    "Guyana": "GUY",

    "Haiti": "HTI",
    "Honduras": "HND",
    "Hong Kong SAR": "HKG",
    "Hungary": "HUN",

    "Iceland": "ISL",
    "India": "IND",
    "Indonesia": "IDN",
    "Iran": "IRN",
    "Iraq": "IRQ",
    "Ireland": "IRL",
    "Israel": "ISR",
    "Italy": "ITA",

    "Jamaica": "JAM",
    "Japan": "JPN",
    "Jordan": "JOR",

    "Kazakhstan": "KAZ",
    "Kenya": "KEN",
    "Korea, Republic of": "KOR",
    "South Korea": "KOR",
    "Kuwait": "KWT",
    "Kyrgyz Republic": "KGZ",

    "Latvia": "LVA",
    "Lebanon": "LBN",
    "Liberia": "LBR",
    "Libya": "LBY",
    "Lithuania": "LTU",
    "Luxembourg": "LUX",

    "Malaysia": "MYS",
    "Maldives": "MDV",
    "Mali": "MLI",
    "Malta": "MLT",
    "Mauritania": "MRT",
    "Mauritius": "MUS",
    "Mexico": "MEX",
    "Moldova": "MDA",
    "Mongolia": "MNG",
    "Montenegro": "MNE",
    "Morocco": "MAR",
    "Mozambique": "MOZ",
    "Myanmar": "MMR",

    "Namibia": "NAM",
    "Nepal": "NPL",
    "Netherlands": "NLD",
    "New Zealand": "NZL",
    "Nicaragua": "NIC",
    "Niger": "NER",
    "Nigeria": "NGA",
    "North Macedonia": "MKD",
    "Norway": "NOR",

    "Oman": "OMN",

    "Pakistan": "PAK",
    "Panama": "PAN",
    "Papua New Guinea": "PNG",
    "Paraguay": "PRY",
    "Peru": "PER",
    "Philippines": "PHL",
    "Poland": "POL",
    "Portugal": "PRT",

    "Qatar": "QAT",

    "Romania": "ROU",
    "Russia": "RUS",
    "Russian Federation": "RUS",
    "Rwanda": "RWA",

    "Saudi Arabia": "SAU",
    "Senegal": "SEN",
    "Serbia": "SRB",
    "Singapore": "SGP",
    "Slovak Republic": "SVK",
    "Slovenia": "SVN",
    "South Africa": "ZAF",
    "Spain": "ESP",
    "Sri Lanka": "LKA",
    "Sudan": "SDN",
    "Suriname": "SUR",
    "Sweden": "SWE",
    "Switzerland": "CHE",

    "Taiwan Province of China": "TWN",
    "Tajikistan": "TJK",
    "Tanzania": "TZA",
    "Thailand": "THA",
    "Togo": "TGO",
    "Trinidad and Tobago": "TTO",
    "Tunisia": "TUN",
    "Türkiye": "TUR",
    "Türkiye, Republic of": "TUR",

    "Uganda": "UGA",
    "Ukraine": "UKR",
    "United Arab Emirates": "ARE",
    "United Kingdom": "GBR",
    "United States": "USA",
    "United States of America": "USA",
    "Uruguay": "URY",
    "Uzbekistan": "UZB",

    "Venezuela": "VEN",
    "Vietnam": "VNM",
    "Viet Nam": "VNM",

    "Yemen": "YEM",
    "Zambia": "ZMB",
    "Zimbabwe": "ZWE"
}


# =========================================================
# PAGE TITLE
# =========================================================

st.title(
    "🌍 Global Economic Scenario Intelligence Platform"
)

st.caption(
    "Explore how macroeconomic shocks can affect projected GDP."
)


# =========================================================
# YEAR SELECTION
# =========================================================

st.subheader("📅 Select Forecast Year")

year = st.selectbox(
    "Year",
    sorted(df["Year"].unique()),
    index=len(sorted(df["Year"].unique())) - 1
)

df_year = df[
    df["Year"] == year
].copy()


# =========================================================
# SCENARIO SELECTION
# =========================================================

st.subheader("⚡ Scenario Selection")

scenario = st.radio(
    "Choose Scenario",
    [
        "Custom",
        "War Shock",
        "Recession",
        "Economic Boom"
    ],
    horizontal=True
)


if scenario == "War Shock":

    oil = 35
    inflation = 6
    interest = 4
    trade = -5

elif scenario == "Recession":

    oil = 10
    inflation = 7
    interest = 6
    trade = -7

elif scenario == "Economic Boom":

    oil = -5
    inflation = 2
    interest = 2
    trade = 6

else:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        oil = st.slider(
            "Oil Change (%)",
            -20,
            50,
            20
        )

    with col2:
        inflation = st.slider(
            "Inflation (%)",
            0,
            10,
            3
        )

    with col3:
        interest = st.slider(
            "Interest Rate (%)",
            0,
            10,
            2
        )

    with col4:
        trade = st.slider(
            "Trade Growth (%)",
            -10,
            10,
            -2
        )


# =========================================================
# SCENARIO MODEL
# =========================================================

def model(data, oil, inflation, interest, trade):

    data = data.copy()

    data["Impact_%"] = (
        (-0.03 * oil)
        + (-0.5 * inflation)
        + (-0.3 * interest)
        + (0.6 * trade)
    )

    data["Adjusted_GDP"] = (
        data[gdp_col]
        * (1 + data["Impact_%"] / 100)
    )

    return data


df_sim = model(
    df_year,
    oil,
    inflation,
    interest,
    trade
)


# =========================================================
# GLOBAL IMPACT
# =========================================================

st.subheader("🌐 Global Impact")

base = df_year[gdp_col].sum()

new = df_sim[
    "Adjusted_GDP"
].sum()

change = new - base

change_pct = (
    (change / base) * 100
    if base != 0
    else 0
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Baseline GDP",
        f"{base:,.2f}"
    )

with col2:

    st.metric(
        "Scenario GDP",
        f"{new:,.2f}",
        delta=f"{change:,.2f}"
    )

with col3:

    st.metric(
        "GDP Change (%)",
        f"{change_pct:.2f}%"
    )


# =========================================================
# ECONOMIC NARRATIVE
# =========================================================

st.subheader("🧠 Economic Narrative")

if scenario == "War Shock":

    st.warning(
        "Oil shock → higher production costs → inflationary pressure → lower GDP."
    )

elif scenario == "Recession":

    st.warning(
        "Lower demand → lower investment → weaker economic activity."
    )

elif scenario == "Economic Boom":

    st.success(
        "Stronger trade → higher production → stronger economic activity."
    )

else:

    st.info(
        "Custom macroeconomic assumptions have been applied."
    )


# =========================================================
# COUNTRY ANALYSIS
# =========================================================

st.subheader("🌍 Country Analysis")

countries = sorted(
    df_year["Country"]
    .dropna()
    .astype(str)
    .unique()
)

country = st.selectbox(
    "Select Country",
    countries
)

country_base = df_year[
    df_year["Country"] == country
][gdp_col]

country_scenario = df_sim[
    df_sim["Country"] == country
]["Adjusted_GDP"]

if not country_base.empty and not country_scenario.empty:

    base_val = country_base.iloc[0]

    scenario_val = country_scenario.iloc[0]

    country_change_pct = (
        ((scenario_val - base_val) / base_val) * 100
        if base_val != 0
        else 0
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Baseline GDP",
            f"{base_val:,.2f}"
        )

    with col2:

        st.metric(
            "Scenario GDP",
            f"{scenario_val:,.2f}"
        )

    with col3:

        st.metric(
            "Scenario Impact",
            f"{country_change_pct:.2f}%"
        )


# =========================================================
# TOP ECONOMIES
# =========================================================

st.subheader("📊 Top Economies")

top10 = (
    df_year
    .sort_values(
        by=gdp_col,
        ascending=False
    )
    .head(10)
)

merged = top10.merge(
    df_sim[
        ["Country", "Adjusted_GDP"]
    ],
    on="Country",
    how="left"
)

fig = px.bar(
    merged,
    x="Country",
    y=[
        gdp_col,
        "Adjusted_GDP"
    ],
    barmode="group",
    labels={
        "value": "GDP",
        "variable": "Measure"
    },
    title="Baseline vs Scenario GDP"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# GEOJSON MAP
# =========================================================

st.subheader("🗺️ Global Scenario Map")


# Add ISO-3 codes
df_sim["ISO3"] = (
    df_sim["Country"]
    .map(country_codes)
)


# Keep countries with valid ISO codes
map_df = df_sim.dropna(
    subset=["ISO3"]
).copy()


# Remove duplicate country codes
map_df = (
    map_df
    .drop_duplicates(
        subset=["ISO3"]
    )
)


# Log scale makes large and small economies
# easier to distinguish visually.
map_df["GDP_Map_Value"] = np.log10(
    map_df["Adjusted_GDP"].clip(lower=0) + 1
)


# ---------------------------------------------------------
# Load India POV Natural Earth GeoJSON
# ---------------------------------------------------------

GEOJSON_URL = (
    "https://raw.githubusercontent.com/"
    "nvkelso/natural-earth-vector/master/"
    "geojson/ne_10m_admin_0_countries_ind.geojson"
)


@st.cache_data
def load_geojson():

    response = requests.get(
        GEOJSON_URL,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


world_geojson = load_geojson()


# ---------------------------------------------------------
# Create map
# ---------------------------------------------------------

fig_map = px.choropleth(
    map_df,
    geojson=world_geojson,
    locations="ISO3",
    featureidkey="properties.ADM0_A3",
    color="GDP_Map_Value",
    hover_name="Country",
    hover_data={
        "Adjusted_GDP": ":,.2f",
        "GDP_Predicted": ":,.2f",
        "Impact_%": ":.2f",
        "GDP_Map_Value": False,
        "ISO3": False
    },
    color_continuous_scale="Viridis",
    labels={
        "Adjusted_GDP": "Scenario GDP",
        "GDP_Predicted": "Baseline GDP",
        "Impact_%": "Impact (%)",
        "GDP_Map_Value": "GDP Scale"
    }
)


# ---------------------------------------------------------
# Map layout
# ---------------------------------------------------------

fig_map.update_geos(
    showcoastlines=True,
    coastlinecolor="gray",

    showcountries=True,
    countrycolor="black",

    showland=True,
    landcolor="lightgray",

    showocean=True,
    oceancolor="white",

    projection_type="natural earth",

    center={
        "lat": 15,
        "lon": 0
    },

    projection_scale=1.05
)


fig_map.update_layout(
    title=(
        f"Global GDP Under '{scenario}' Scenario — {int(year)}"
    ),

    coloraxis_colorbar=dict(
        title="GDP<br>(Log Scale)"
    ),

    margin=dict(
        l=0,
        r=0,
        t=60,
        b=0
    ),

    height=600
)


st.plotly_chart(
    fig_map,
    use_container_width=True
)


# =========================================================
# SHOCK DECOMPOSITION
# =========================================================

st.subheader("📉 Shock Decomposition")

oil_c = -0.03 * oil

inf_c = -0.5 * inflation

int_c = -0.3 * interest

trade_c = 0.6 * trade


decomp = pd.DataFrame({

    "Factor": [
        "Oil",
        "Inflation",
        "Interest",
        "Trade"
    ],

    "Contribution": [
        oil_c,
        inf_c,
        int_c,
        trade_c
    ]
})


decomp["Abs"] = (
    decomp["Contribution"].abs()
)


fig_pie = px.pie(
    decomp,
    names="Factor",
    values="Abs",
    hole=0.4,
    title="Relative Contribution of Scenario Factors"
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)

st.dataframe(
    decomp,
    use_container_width=True
)


# =========================================================
# SENSITIVITY ANALYSIS
# =========================================================

st.subheader("📈 Sensitivity Analysis")

sens = pd.DataFrame({

    "Factor": [
        "Oil",
        "Inflation",
        "Interest",
        "Trade"
    ],

    "Sensitivity": [
        -0.03,
        -0.5,
        -0.3,
        0.6
    ]
})


fig_sens = px.bar(
    sens,
    x="Factor",
    y="Sensitivity",
    title="GDP Sensitivity to Macroeconomic Factors"
)

st.plotly_chart(
    fig_sens,
    use_container_width=True
)


# =========================================================
# RISK SCORE
# =========================================================

st.subheader("⚠️ Risk Level")

risk = abs(
    df_sim["Impact_%"].mean()
)


if risk > 5:

    st.error(
        f"High Risk — {risk:.2f}% average GDP impact"
    )

elif risk > 2:

    st.warning(
        f"Medium Risk — {risk:.2f}% average GDP impact"
    )

else:

    st.success(
        f"Low Risk — {risk:.2f}% average GDP impact"
    )


# =========================================================
# DOWNLOAD REPORT
# =========================================================

st.subheader("📄 Download Scenario Report")


report = f"""
GLOBAL ECONOMIC SCENARIO REPORT
================================

Scenario: {scenario}
Forecast Year: {int(year)}

Macroeconomic Assumptions
--------------------------
Oil Change: {oil}%
Inflation: {inflation}%
Interest Rate: {interest}%
Trade Growth: {trade}%

GDP Impact
----------
Baseline Global GDP: {base:,.2f}
Scenario Global GDP: {new:,.2f}
GDP Change: {change:,.2f}
GDP Change (%): {change_pct:.2f}%

Risk Level
----------
Average Impact: {risk:.2f}%

Note:
This scenario model represents a simplified
sensitivity framework based on the specified
macroeconomic assumptions.
"""


st.download_button(
    "⬇️ Download Report",
    report,
    "global_economic_scenario_report.txt"
)


# =========================================================
# ADVANCED IMPACT BREAKDOWN
# =========================================================

st.subheader("📊 Impact Breakdown")

fig_bar = px.bar(
    decomp,
    x="Factor",
    y="Contribution",
    title="Positive vs Negative Economic Impact",
    labels={
        "Contribution": "GDP Impact (%)"
    }
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)
