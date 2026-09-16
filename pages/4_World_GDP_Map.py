import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests

st.title("🌍 Global GDP Map")

# ---------------------------------------------------------
# 1. Load GDP data
# ---------------------------------------------------------

map_df = pd.read_csv("data/world_gdp_map.csv")

map_df["Country"] = (
    map_df["Country"]
    .astype(str)
    .str.strip()
)

map_df["GDP"] = pd.to_numeric(
    map_df["GDP"],
    errors="coerce"
)

map_df = map_df.dropna(subset=["GDP"])


# ---------------------------------------------------------
# 2. Country → ISO-3 mapping
# ---------------------------------------------------------

country_codes = {
    "Albania": "ALB",
    "Algeria": "DZA",
    "Andorra": "AND",
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
    "Chad": "TCD",
    "Chile": "CHL",
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
    "Ethiopia": "ETH",
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
    "Tajikistan": "TJK",
    "Tanzania": "TZA",
    "Thailand": "THA",
    "Togo": "TGO",
    "Trinidad and Tobago": "TTO",
    "Tunisia": "TUN",
    "Türkiye, Republic of": "TUR",
    "Uganda": "UGA",
    "Ukraine": "UKR",
    "United Arab Emirates": "ARE",
    "United Kingdom": "GBR",
    "United States": "USA",
    "Uruguay": "URY",
    "Uzbekistan": "UZB",
    "Venezuela": "VEN",
    "Vietnam": "VNM",
    "Yemen": "YEM",
    "Zambia": "ZMB",
    "Zimbabwe": "ZWE"
}

map_df["ISO3"] = map_df["Country"].map(country_codes)

map_df = map_df.dropna(subset=["ISO3"])


# ---------------------------------------------------------
# 3. Log transformation
# ---------------------------------------------------------

map_df["GDP_log"] = np.log10(
    map_df["GDP"].clip(lower=0) + 1
)


# ---------------------------------------------------------
# 4. Load India POV GeoJSON
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
# 5. Create choropleth
# ---------------------------------------------------------

fig = px.choropleth(
    map_df,
    geojson=world_geojson,
    locations="ISO3",
    featureidkey="properties.ADM0_A3",
    color="GDP_log",
    hover_name="Country",
    hover_data={
        "GDP": ":,.0f",
        "GDP_log": False,
        "ISO3": False
    },
    color_continuous_scale="Viridis",
    labels={
        "GDP": "GDP (Billion USD)",
        "GDP_log": "GDP Scale (Log)"
    }
)


# ---------------------------------------------------------
# 6. Map appearance
# ---------------------------------------------------------

fig.update_geos(
    showcoastlines=True,
    coastlinecolor="gray",
    showcountries=True,
    countrycolor="black",
    showland=True,
    landcolor="lightgray",
    showocean=True,
    oceancolor="white",
    projection_type="natural earth",
    fitbounds="locations"
)

fig.update_layout(
    title="Global GDP Distribution (2026)",
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


# ---------------------------------------------------------
# 7. Display
# ---------------------------------------------------------

st.plotly_chart(
    fig,
    use_container_width=True
)

st.caption(
    "GDP values are expressed in Billion USD. "
    "Log scale is used to improve visualization across countries. "
    "Country boundaries use Natural Earth geographic data."
)
