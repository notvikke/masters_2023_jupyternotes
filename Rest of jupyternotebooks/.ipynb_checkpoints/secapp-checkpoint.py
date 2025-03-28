import json
import zipfile
import geopandas
import time
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.express as px
import utils


import zipfile
import geopandas
import pandas as pd
import plotly.express as px
import streamlit as st


def read_and_preprocess_data():
    with zipfile.ZipFile('data/uber-data.zip') as zip:
        with zip.open('madrid-barrios-2020-1-All-DatesByHourBucketsAggregate.csv') as csv:
            data = pd.read_csv(csv)
        with zip.open('madrid_barrios.json') as geojson:
            codes = geopandas.read_file(geojson, encoding="utf-8")

    # change data types in codes because they are not the same as in data
    codes['GEOCODIGO'] = codes['GEOCODIGO'].astype(int)
    codes['MOVEMENT_ID'] = codes['MOVEMENT_ID'].astype(int)

    codes["DISPLAY_NAME"] = codes["DISPLAY_NAME"].str.split().str[1:].str.join(" ")

    # Merge the data with the codes (source)
    data = data.merge(codes[["GEOCODIGO", "MOVEMENT_ID", "DISPLAY_NAME"]], left_on="sourceid", right_on="MOVEMENT_ID",
                      how="left")
    data = data.rename(columns={"GEOCODIGO": "src_neigh_code", "DISPLAY_NAME": "src_neigh_name"}).drop(
        columns=["MOVEMENT_ID"])

    data = data.merge(codes[["GEOCODIGO", "MOVEMENT_ID", "DISPLAY_NAME"]], left_on="dstid", right_on="MOVEMENT_ID",
                      how="left")
    data = data.rename(columns={"GEOCODIGO": "dst_neigh_code", "DISPLAY_NAME": "dst_neigh_name"}).drop(
        columns=["MOVEMENT_ID"])

    # Create a new date column
    data["year"] = "2020"
    data["date"] = pd.to_datetime(
        data["day"].astype(str) + data["month"].astype(str) + data["year"].astype(str) + ":" + data[
            "start_hour"].astype(str), format="%d%m%Y:%H")

    # Create a new day_period column
    data["day_period"] = data.start_hour.astype(str) + "-" + data.end_hour.astype(str)
    data["day_of_week"] = data.date.dt.weekday
    data["day_of_week_str"] = data.date.dt.day_name()

    return data, codes


data, codes = read_and_preprocess_data()

st.title("Uber Travel Data in Madrid")
st.text("This Streamlit app shows the average travel time between two neighborhoods in Madrid.")
st.text("Further it shows a map of the chosen destination and origin")

st.sidebar.title("Filters")
st.sidebar.header("Select Origin and Destination")
st.sidebar.text("Please set the origin and destination to see the results")

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "Choose origin",
    (data.src_neigh_name.sort_values().unique().tolist())
)

add_selectbox2 = st.sidebar.selectbox(
    "Choose destination",
    (data.dst_neigh_name.sort_values().unique().tolist())
)

with st.spinner('Loading Data...'):
    # Filter the data
    data_filtered = data[(data.src_neigh_name == add_selectbox) & (data.dst_neigh_name == add_selectbox2)]

    # group by date
    data_grouped = data_filtered.groupby("date").agg({"mean_travel_time": "mean"}).reset_index()

    data_grouped.mean_travel_time = data_grouped.mean_travel_time.astype(int) / 60

    # plot
    fig1 = px.line(data_grouped, x="date", y="mean_travel_time", title="Average Travel Time per Day",
                   labels={"mean_travel_time": "Mean travel time (minutes)", "date": "Date"})
    st.plotly_chart(fig1, use_container_width=True)

with st.spinner("Loading Data..."):
    data_grouped = data.groupby(["day_of_week_str", "day_period"]).agg({"mean_travel_time": "mean"}).reset_index()
    data_grouped.mean_travel_time = data_grouped.mean_travel_time.astype(int) / 60

    fig2 = px.bar(data_grouped, x="day_of_week_str", y="mean_travel_time", color="day_period", facet_col="day_period",
                  title="Average Travel Time per Day Period and Day of week",
                  labels={"mean_travel_time": "Mean travel time (minutes)",
                          "day_period": "Day Period", "day_of_week_str": "Day of Week"})
    st.plotly_chart(fig2, use_container_width=True)

with st.spinner("Loading Data..."):
    # Filter the GeoDataFrame to select two points
    gdf = codes[(codes.DISPLAY_NAME == add_selectbox) | (codes.DISPLAY_NAME == add_selectbox2)]

    fig3 = px.choropleth_mapbox(gdf, geojson=gdf.geometry, locations=gdf.index, hover_data=['DISPLAY_NAME'],
                                color_continuous_scale='OrRd', mapbox_style='open-street-map', zoom=10,
                                center={'lat': gdf.geometry.centroid.y.mean(), 'lon': gdf.geometry.centroid.x.mean()})

    # Show the map
    st.header("Map of Madrid")
    st.plotly_chart(fig3, use_container_width=True)