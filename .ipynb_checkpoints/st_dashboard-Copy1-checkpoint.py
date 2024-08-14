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

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

####################### Import data #########################################

df = pd.read_csv('split_data_to_plot.csv')
top20 = pd.read_csv('top_20_stations.csv', index_col = 0)
df_rides = pd.read_csv('aggregated_rides.csv', index_col = 0)

####################### DEFINE THE PAGES ####################################


### Intro page

if page == "Intro page":
    st.markdown("#### The dashboard will help analyze bike distribution and analyze expansion for a bike sharing service operated by Citi Bike in New York City.")
    st.markdown("Since launch in 2013, Citi Bikes popularity has increased and has created a higher demand. This has led to complaints about fewer bikes being available at popular stations or stations being fully stocked and no where to return rented bikes. The dashboard is separated into 4 sections:")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Most popular stations")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

###################### line chart page ###########################################

elif page == 'Weather component and bike usage':

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = df_rides['date'], y = df_rides['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df_rides['bike_rides_daily'], 'color': 'purple'}),           secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x = df_rides['date'], y = df_rides['avgTemp'], name = 'Daily temperature', marker={'color': df_rides['avgTemp'], 'color': 'green'}), secondary_y = True)

    fig_2.update_layout(
    title = 'Daily Bike Trips and Temperatures in 2022',
    xaxis_title = 'Months',
    height = 800
    )

      # Set y-axes titles
    fig_2.update_yaxes(
        title_text="Number of Rides", 
        secondary_y=False)
    fig_2.update_yaxes(
        title_text="Temperature", 
        secondary_y=True)
    st.plotly_chart(fig_2, use_container_width=True)
    
    st.markdown("There is an strong correlation between temperatures and their relationship with daily bike trips. Lower temperatures indicate less daily rides and during the very hot temperatures there is also a slight dip in daily rides. Regardless of the slight dip in daily rides in the months of July and August this graph indicates that the most active riding season in from May to November and the bike distribution issues will be most impacted during those months.")    

####################### Most popular stations bar chart page #######################

    # Create the season variable

elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value = (total_rides))
    
    # Bar chart

    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))
    
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker = {'color' : top20['value'], 'color' : 'Purple'}))
    fig.update_layout(
    title = 'Top 20 Most Popular Bike Stations in New York City',
    xaxis_title = 'Start Stations', 
    yaxis_title = 'Sum of Trips', 
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width = True)
    st.markdown("The bar chart shows the top 20 most popular bike stations, W 21st St & 6th Ave, West St & Chambers St, Broadway & W 58th St, and 1st Ave & 68th St have a slight jump up from the rest of the stations indicating their popularity.")

######################## Add the map page #########################################

elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over Chicago")

    path_to_html = "New York Bike Trips Aggregated.html"

# Read file and keep in variable 
    with open(path_to_html, 'r') as f:
        html_data = f.read()

## Show in web page 
    st.header("Aggregated Bike Trips in New York City")
    st.components.v1.html(html_data,height = 1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are:")
    st.markdown("W 21 St & 6 Ave, West St & Chambers St and Broadway & W 58 St are the 3 most commonly used start stations. Sliding the filter to show most commonnly taken trips, we can see that the common start stations do not correlate to most common trips from start to end station.")
    st.markdown("Sliding the filter left there are a significant amount of ride near the water and the most common trips (>8,000) start and end at the same station Central Park S & 6 Ave, 7 Ave & Central Park South, and Roosevelt Island Tramway which may suggest that the most common trips are people using the bikes for a exercise or a casual ride through Central Park or by the water.")

else:
    
    st.header("Conclusions and Recommendations")
    st.markdown("### Our analysis has shown that Citi Bikes should focus on the following suggestions to help with distribution:")
    st.markdown("- More stations should be added around Central Park and the near the water since those are the stations responsible for the most popular trips and add an additional station at the most popular start stations W 21 St & 6 Ave, West St & Chambers St and Broadway & W 58 St. This would improve distribution for the majority of the problem areas and improve customer satisfaction.")
    st.markdown("- From May to November make sure these stations are fully stocked especially the Central Park stations since trips tend to start and end there, the number of bikes can also be reduced in the colder months since there is less of an issue with less rides.")
    st.markdown("- Creating a team that monitors bike stations to keep up with demand and ensure stations are stocked.")
    st.markdown("- Continuing analysis for future expansion.")
 
           

           
           