import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 

st.set_page_config(page_title = 'New York City Bike Share Strategy Dashboard', layout='wide')

st.title("New York City Bike Share Strategy Dashboard")

st.markdown("The dashboard will help analyze bike distribution and analyze expansion for a bike sharing service in New York City")

####################### Import data #########################################

df = pd.read_csv('reduced_data_to_plot.csv', index_col = 0)
top20 = pd.read_csv('top_20_stations.csv', index_col = 0)

####################### DEFINE THE CHARTS ###################################


## Bar chart 

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker = {'color' : top20['value'], 'colorscale' : 'Purples'}))
fig.update_layout(
    title = 'Top 20 Most Popular Bike Stations in New York City',
    xaxis_title = 'Start Stations', 
    yaxis_title = 'Sum of Trips', 
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width = True)

####################### Import data #########################################

df_rides = pd.read_csv('aggregated_rides.csv', index_col = 0)


###################### line chart ###########################################

fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
go.Scatter(x = df_rides['date'], y = df_rides['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df_rides['bike_rides_daily'], 'color': 'blue'}), secondary_y = False
)

fig_2.add_trace(
go.Scatter(x = df_rides['date'], y = df_rides['avgTemp'], name = 'Daily temperature', marker={'color': df_rides['avgTemp'], 'color': 'red'}), secondary_y = True)

fig_2.update_layout(
    title = 'Daily Bike Trips and Temperatures in 2022', 
    height = 800
)
st.plotly_chart(fig_2, use_container_width=True)
    
###################### Add the map  #########################################

path_to_html = "New York Bike Trips Aggregated.html"

# Read file and keep in variable 
with open(path_to_html, 'r') as f:
    html_data = f.read()

## Show in web page 
st.header("Aggregated Bike Trips in New York City")
st.components.v1.html(html_data,height = 1000)    
 
           

           
           