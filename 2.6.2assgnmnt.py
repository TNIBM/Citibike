################################################ CITIBIKE DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout='wide')
st.title("Citi Bike Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems Citi currently faces")
st.markdown("Right now, Citi bikes runs into a situation where customers complain about bikes not being avaibale at certain times. This analysis aims to look at the potential reasons behind this.")

########################## Import data ###########################################################################################

df = pd.read_csv('Data/output/reduced_data_to_plot.csv', index_col = 0)
top20 = pd.read_csv('Data/output/top20.csv', index_col = 0)

########################################### DEFINE THE CHARTS #####################################################################

## Bar chart

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width=True)

## Line chart

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Filter data from 2022 onward
df = df[df['date'].dt.year >= 2022]

# Reduce the dataset to 100,000 rows by sampling
df_sampled = df.sample(n=100000, random_state=42).sort_values(by='date')

# Create subplot with secondary y-axis
fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

# Add daily bike rides trace
fig_2.add_trace(
    go.Scatter(x=df_sampled['date'], y=df_sampled['bike_rides_daily'], name='Daily bike rides'),
    secondary_y=False
)

# Add daily temperature trace
fig_2.add_trace(
    go.Scatter(x=df_sampled['date'], y=df_sampled['avgTemp'], name='Daily temperature'),
    secondary_y=True
)

fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022',
    height = 600
)

st.plotly_chart(fig_2, use_container_width=True)


### Add the map ###

path_to_html = "Citi_Bike_TripsAggregated.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in New York")
st.components.v1.html(html_data,height=1000)
