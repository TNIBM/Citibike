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
from numerize.numerize import numerize
from PIL import Image


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout='wide')
st.title("Citi Bike Strategy Dashboard")

# Define Side Bar

page = st.sidebar.selectbox('Select an aspect of the analysis',
   ["Intro page",  "Weather component and bike usage",
    "Most popular stations",
     "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot_7.csv').sort_values(by='date')
top20 = pd.read_csv('top20.csv', index_col = 0)

######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful insights on the expansion problems Citi Bike currently faces.")
    st.markdown("Right now, Citi Bike runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    myImage = Image.open("Visualizations/CitiBike.jpg") #source: https://www.xbedeals.site/?path=page/ggitem&ggpid=1269823
    st.image(myImage)


    ### Create the dual axis line chart page ###
    
elif page == 'Weather component and bike usage':

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df['bike_rides_daily'],'color': 'blue'}),
    secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature', marker={'color': df['avgTemp'],'color': 'red'}),
    secondary_y=True
    )

    fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022',
    height = 400
    )

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")

### Most popular stations page

    # Create the season variable

elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))
    
    # Bar chart

    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("From the bar chart it is shown that there are some start stations that are more popular than others - in the top 3 we can see 1 Ave & E 68 St, W 21 St and 6th Ave, and Broadway & W 58th St. There is a big jump between the highest and lowest bars of the plot, indicating some clear preferences for the leading stations. This is a finding that we could cross reference with the interactive map that you can access through the side bar select box.")

elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over New York")

    path_to_html = "Bike_Rides.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data,height=1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are:")
    st.markdown("1 Ave & E 68 St, W 21 St and 6th Ave, as well as Broadway & W 58th St. While having the aggregated bike trips filter enabled, we can see that even though Broadway & W 58 St is a popular start stations, it doesn't account for the most commonly taken trips.")
    st.markdown("The most common routes (>900) are between 1 Ave & E 62 St - 1 Ave & E68 St, Vesey St & Church St - North Moore St & Greenwich St, W21 St & 6 Ave - 9 Ave & W 22 St, Roosevelt Island Tramway - Southpoint Park, E 68 St & 3 Ave - 1 Ave & E68 St, Soissons Landing - Yankee Ferry Terminal, some of them are located in the city center area and some are located along the Hudson River and in the islands.")

else:
    
    st.header("Conclusions and recommendations")
    bikes = Image.open("Visualizations/conclusion.jpg")  #source: https://depositphotos.com/photo/flipchart-business-project-strategy-bicycle-wall-light-modern-office-213024472.html
    st.image(bikes)
    st.markdown("### Our analysis has shown that Citi Bike should focus on the following objectives moving forward:")
    st.markdown("- Add more stations to the locations around the Hudson River line, such as Vesey St & Church St - North Moore St & Greenwich St, Roosevelt Island Tramway - Southpoint Park(in island) and Soissons Landing - Yankee Ferry Terminal(in island), and around the city center areas, such as 1 Ave & E 62 St - 1 Ave & E68 St, E 68 St & 3 Ave - 1 Ave & E68 St, and W21 St & 6 Ave - 9 Ave & W 22 St.")
    st.markdown("- Ensure that bikes are fully stocked in all these stations during the warmer months in order to meet the higher demand, but provide a lower supply in winter and late autumn to reduce logistics costs.")