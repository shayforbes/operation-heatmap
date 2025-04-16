
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_excel("Operation Heatmap (1).xlsx", sheet_name="Reports")

# Full CBSA coordinates
cbsa_coords = {41620: {'Latitude': 40.7608, 'Longitude': -111.891}, 14260: {'Latitude': 43.615, 'Longitude': -116.2023}, 39340: {'Latitude': 40.2338, 'Longitude': -111.6585}, 41100: {'Latitude': 37.0965, 'Longitude': -113.5684}, 19740: {'Latitude': 39.7392, 'Longitude': -104.9903}, 31140: {'Latitude': 41.2565, 'Longitude': -95.9345}, 35620: {'Latitude': 40.7128, 'Longitude': -74.006}}

df["Latitude"] = df["CBSA"].map(lambda x: cbsa_coords.get(x, {}).get("Latitude"))
df["Longitude"] = df["CBSA"].map(lambda x: cbsa_coords.get(x, {}).get("Longitude"))
df = df.dropna(subset=["Latitude", "Longitude"])
df["Avg CS"] = df[["CS", "CS.1", "CS.2", "CS.3", "CS.4", "CS.5"]].mean(axis=1)

carrier_cols = [
    ("Carrier 1", "CS"),
    ("Carrier 2", "CS.1"),
    ("Carrier 2.1", "CS.2"),
    ("Carrier 3", "CS.3"),
    ("Carrier 4", "CS.4"),
    ("Carrier 5", "CS.5"),
]

# UI
st.title("CBSA Carrier Confidence Dashboard")

carriers = pd.unique([carrier for col, _ in carrier_cols for carrier in df[col].dropna()])
selected_carrier = st.selectbox("Select a carrier to filter by", sorted(carriers))
min_score = st.slider("Minimum Confidence Score", 1, 5, 3)

def carrier_filter(row):
    for col, cs_col in carrier_cols:
        if row[col] == selected_carrier and row[cs_col] >= min_score:
            return True
    return False

filtered_df = df[df.apply(carrier_filter, axis=1)]

fig = px.scatter_mapbox(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Market Name",
    hover_data={"Avg CS": True},
    color="Avg CS",
    zoom=3,
    mapbox_style="carto-positron",
    size_max=15
)

st.plotly_chart(fig)
st.subheader("Filtered CBSA Data")
st.dataframe(filtered_df[["CBSA", "Market Name", "State", "Avg CS"] + [col for col, _ in carrier_cols]])
