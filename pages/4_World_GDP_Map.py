import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("🌍 Global GDP Map")

# Load GDP data
map_df = pd.read_csv("data/world_gdp_map.csv")

# Clean columns
map_df["Country"] = map_df["Country"].astype(str).str.strip()
map_df["GDP"] = pd.to_numeric(map_df["GDP"], errors="coerce")

# Remove invalid rows
map_df = map_df.dropna(subset=["GDP"])

# Country name → ISO-3 mapping
country_codes = {
    "Albania": "ALB",
    "Algeria": "DZA",
    "Andorra": "AND",
    "Angola": "AGO",
    "Antigua and Barbuda": "ATG",
    "Argentina": "ARG",
    "Armenia": "ARM",
    "Aruba": "ABW",
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
    "Bosnia and Herzegovina": "BIH",
    "Botswana": "BWA",
    "Brazil": "BRA",
    "Brunei Darussalam": "BRN",
    "Bulgaria": "BGR",
    "Burkina Faso": "BFA",
    "Burundi": "BDI",
    "Cabo Verde": "CPV",
    "Cambodia": "KHM",
    "Cameroon": "CMR",
    "Canada": "CAN",
    "Central African Republic": "CAF",
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
    "Dominica": "DMA",
    "Dominican Republic": "DOM",
    "Ecuador": "ECU",
    "Egypt": "EGY",
    "El Salvador": "SLV",
    "Equatorial Guinea": "GNQ",
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
    "Grenada": "GRD",
    "Guatemala": "GTM",
    "Guinea": "GIN",
    "Guinea-Bissau": "GNB",
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
    "Kiribati": "KIR",
    "Korea, Republic of": "KOR",
    "Kosovo": "XKX",
    "Kuwait": "KWT",
    "Kyrgyz Republic": "KGZ",
    "Lao P.D.R.": "LAO",
    "Latvia": "LVA",
    "Lesotho": "LSO",
    "Liberia": "LBR",
    "Libya": "LBY",
    "Liechtenstein": "LIE",
    "Lithuania": "LTU",
    "Luxembourg": "LUX",
    "Macao SAR": "MAC",
    "Madagascar": "MDG",
    "Malawi": "MWI",
    "Malaysia": "MYS",
    "Maldives": "MDV",
    "Mali": "MLI",
    "Malta": "MLT",
    "Marshall Islands": "MHL",
    "Mauritania": "MRT",
    "Mauritius": "MUS",
    "Mexico": "MEX",
    "Micronesia, Fed. States of": "FSM",
    "Moldova": "MDA",
    "Mongolia": "MNG",
    "Montenegro": "MNE",
    "Morocco": "MAR",
    "Mozambique": "MOZ",
    "Myanmar": "MMR",
    "Namibia": "NAM",
    "Nauru": "NRU",
    "Nepal": "NPL",
    "Netherlands": "NLD",
    "New Zealand": "NZL",
    "Nicaragua": "NIC",
    "Niger": "NER",
    "Nigeria": "NGA",
    "North Macedonia": "MKD",
    "Norway": "NOR",
    "Oman": "OMN",
    "Palau": "PLW",
    "Panama": "PAN",
    "Papua New Guinea": "PNG",
    "Paraguay": "PRY",
    "Peru": "PER",
    "Philippines": "PHL",
    "Poland": "POL",
    "Portugal": "PRT",
    "Puerto Rico": "PRI",
    "Qatar": "QAT",
    "Romania": "ROU",
    "Russian Federation": "RUS",
    "Rwanda": "RWA",
    "Saint Kitts and Nevis": "KNA",
    "Saint Lucia": "LCA",
    "Saint Vincent and the Grenadines": "VCT",
    "Samoa": "WSM",
    "San Marino": "SMR",
    "Saudi Arabia": "SAU",
    "Senegal": "SEN",
    "Serbia": "SRB",
    "Seychelles": "SYC",
    "Sierra Leone": "SLE",
    "Singapore": "SGP",
    "Slovak Republic": "SVK",
    "Slovenia": "SVN",
    "Solomon Islands": "SLB",
    "Somalia": "SOM",
    "South Africa": "ZAF",
    "South Sudan, Republic of": "SSD",
    "Spain": "ESP",
    "Sudan": "SDN",
    "Suriname": "SUR",
    "Sweden": "SWE",
    "Switzerland": "CHE",
    "São Tomé and Príncipe": "STP",
    "Taiwan Province of China": "TWN",
    "Tajikistan": "TJK",
    "Tanzania": "TZA",
    "Thailand": "THA",
    "Timor-Leste": "TLS",
    "Togo": "TGO",
    "Tonga": "TON",
    "Trinidad and Tobago": "TTO",
    "Tunisia": "TUN",
    "Turkmenistan": "TKM",
    "Tuvalu": "TUV",
    "Türkiye, Republic of": "TUR",
    "Uganda": "UGA",
    "Ukraine": "UKR",
    "United Arab Emirates": "ARE",
    "United Kingdom": "GBR",
    "United States": "USA",
    "Uruguay": "URY",
    "Uzbekistan": "UZB",
    "Vanuatu": "VUT",
    "Venezuela": "VEN",
    "Vietnam": "VNM",
    "Yemen": "YEM",
    "Zambia": "ZMB",
    "Zimbabwe": "ZWE"
}

# Create ISO-3 codes
map_df["ISO3"] = map_df["Country"].map(country_codes)

# Keep only actual countries recognized by the mapping
map_df = map_df.dropna(subset=["ISO3"]).copy()

# Log transformation
map_df["GDP_log"] = np.log10(map_df["GDP"].clip(lower=0) + 1)

st.subheader("Global GDP Distribution (2026)")

fig = px.choropleth(
    map_df,
    locations="ISO3",
    locationmode="ISO-3",
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

fig.update_layout(
    title="Global GDP Distribution (2026)",
    coloraxis_colorbar=dict(
        title="GDP<br>(Log Scale)"
    ),
    margin=dict(l=0, r=0, t=60, b=0),
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.caption(
    "GDP values are expressed in Billion USD. "
    "Log scale is used to improve visualization across countries."
)
