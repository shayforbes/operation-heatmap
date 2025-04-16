
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Excel data
file_path = "Operation Heatmap (1).xlsx"
reports_df = pd.read_excel(file_path, sheet_name='Reports')

# CBSA coordinates (extend this as needed)
cbsa_coords = {
    41620: (40.7608, -111.8910),
    14260: (43.6150, -116.2023),
    39340: (40.2338, -111.6585),
    41100: (37.0965, -113.5684),
    19740: (39.7392, -104.9903),
}

# Clean data and compute avg confidence
df = reports_df.copy()
df["Latitude"] = df["CBSA"].map(lambda x: cbsa_coords.get(x, (None, None))[0])
df["Longitude"] = df["CBSA"].map(lambda x: cbsa_coords.get(x, (None, None))[1])
df = df.dropna(subset=["Latitude", "Longitude"])
df["Avg CS"] = df[["CS", "CS.1", "CS.2", "CS.3", "CS.4", "CS.5"]].mean(axis=1)

# App UI
st.title("CBSA Carrier Confidence Dashboard")

# Carrier filter options
carrier_cols = [
    ("Carrier 1", "CS"),
    ("Carrier 2", "CS.1"),
    ("Carrier 2.1", "CS.2"),
    ("Carrier 3", "CS.3"),
    ("Carrier 4", "CS.4"),
    ("Carrier 5", "CS.5"),
]

# Gather unique carrier names
carriers = pd.unique([carrier for col, _ in carrier_cols for carrier in df[col].dropna()])
selected_carrier = st.selectbox("Select a carrier to filter by", sorted(carriers))
min_score = st.slider("Minimum Confidence Score", 1, 5, 3)

# Filter function
def carrier_filter(row):
    for col, cs_col in carrier_cols:
        if row[col] == selected_carrier and row[cs_col] >= min_score:
            return True
    return False

filtered_df = df[df.apply(carrier_filter, axis=1)]

# Map
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

# Table
st.subheader("Filtered CBSA Data")
st.dataframe(filtered_df[["CBSA", "Market Name", "State", "Avg CS"] + [col for col, _ in carrier_cols]])
