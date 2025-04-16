
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Excel data
reports_df = pd.read_excel("Operation Heatmap (1).xlsx", sheet_name='Reports')
cbsa_coords_df = pd.read_csv("cbsa_coordinates_official_verified.csv")

# Merge CBSA coordinates into the main dataframe
cbsa_coords_df = cbsa_coords_df[["CBSA", "Latitude", "Longitude"]]
df = reports_df.merge(cbsa_coords_df, on="CBSA", how="left")
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
