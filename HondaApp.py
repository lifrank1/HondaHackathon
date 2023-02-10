import plotly.express as px
import streamlit as st
import pandas as pd
import folium

# Load the data
def make_df():
    org_df = pd.read_csv("/Users/suvan/99P Data Challenge/orginization.csv")
    route_df = pd.read_csv("/Users/suvan/99P Data Challenge/route.csv")
    trip_req_df = pd.read_csv("/Users/suvan/99P Data Challenge/trip_request.csv")
    trip_sum_df = pd.read_csv("/Users/suvan/99P Data Challenge/trip_summary.csv")
    vehicle_df = pd.read_csv("/Users/suvan/99P Data Challenge/vehicle.csv")
    return org_df, route_df, trip_req_df, trip_sum_df, vehicle_df

org_df, route_df, trip_req_df, trip_sum_df, vehicle_df = make_df()
dfs = {
        "Organization": org_df, 
        "Route": route_df, 
        "Trip Request": trip_req_df, 
        "Trip Summary": trip_sum_df, 
        "Vehicle": vehicle_df
        }

option = st.selectbox("Select a data frame", dfs.keys())

st.title(f"{option} Data")
st.dataframe(dfs[option])

#Junky Suvan code
trip_sum_df['start_ts'] = pd.to_datetime(trip_sum_df['start_ts'])
mean_lat = trip_sum_df['trip_start_lat'].mean()
mean_long = trip_sum_df['trip_start_lon'].mean()
map = folium.Map(location=[mean_lat, mean_long], zoom_start=12)

for i, row in trip_sum_df.iterrows():
    folium.Marker(
        location=[row['trip_start_lat'], row['trip_start_lon']],
        popup=f"Start Time: {row['start_ts']}",
        icon=None
    ).add_to(map)
    folium.Marker(
        location=[row['trip_end_lat'], row['trip_end_lon']],
        popup=f"End Time: {row['end_ts']}",
        icon=None
    ).add_to(map)

st.title("Map")
trip_sum_df['start_ts_num'] = (trip_sum_df['start_ts'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
fig = px.scatter_mapbox(trip_sum_df, lat='trip_start_lat', lon='trip_start_lon', color='start_ts_num', zoom=12)
fig.update_layout(
    mapbox_style="open-street-map",
    mapbox_center=dict(lat=trip_sum_df['trip_start_lat'].mean(), lon=trip_sum_df['trip_start_lon'].mean()),
    title='Trip Start Times',
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            buttons=[
                dict(
                    label="Play",
                    method="animate",
                    args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True, transition=dict(duration=0))]
                ),
                dict(
                    label="Pause",
                    method="animate",
                    args=[[None], dict(mode="immediate", transition=dict(duration=0), frame=dict(duration=0, redraw=False))]
                )
            ]
        )
    ]
)
st.plotly_chart(fig, use_container_width=True)
