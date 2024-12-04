import pandas as pd
pd.DataFrame.iteritems = pd.DataFrame.items
import numpy as np
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
import pickle
import folium
import geopy


st.set_page_config(layout="wide")

retirement_homes_df = pd.read_csv('https://raw.githubusercontent.com/TheLazyCactus/Data_Thieves_project/refs/heads/main/retirement_homes_df.csv')
schools_df = pd.read_csv('https://raw.githubusercontent.com/TheLazyCactus/Data_Thieves_project/refs/heads/main/schools_df.csv')
cats_df = pd.read_csv('https://raw.githubusercontent.com/TheLazyCactus/Data_Thieves_project/refs/heads/main/Cat%20Scraped.csv', sep=";", low_memory =False, encoding='latin1',on_bad_lines='skip')
#dogs_df = pd.read_csv('https://raw.githubusercontent.com/TheLazyCactus/Data_Thieves_project/refs/heads/main/Dog%20Scraped.csv', encoding='latin1')
cats_coordinates = pd.read_csv('https://raw.githubusercontent.com/TheLazyCactus/Data_Thieves_project/refs/heads/main/cat_coordinate.csv')
#dog_coordinates = pd.read_csv('https://raw.githubusercontent.com/TheLazyCactus/Data_Thieves_project/refs/heads/main/dog_coordinate.csv')
filtered_cat = {}

map = folium.Map(location=(34.04621475184492, -118.27514966412589))

st.sidebar.title("The Guardians of the Voiceless")
first_option = st.sidebar.selectbox(
    'What type of establishment would you like to choose?', 
    ('Retirement Home', 'School'),
    index = None,
    placeholder= 'Please select one of the available options...'
)

def add_markers(df, icon_type, color):
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['geometry_location_lat'], row['geometry_location_lng']],
            tooltip=row['name'],
            popup=row['name'],
            icon=folium.Icon(icon=icon_type, prefix='fa', color=color)
).add_to(map)

if first_option == 'Retirement Home':
    show_all = st.sidebar.checkbox('Show all Retirement Homes', value=False)
    if show_all:
        add_markers(retirement_homes_df, 'home', 'darkgreen')
    else:
        options = retirement_homes_df['name'].sort_values().tolist()
        selection = st.sidebar.selectbox('Select a Retirement Home:', options, index=0) 
        location = retirement_homes_df[retirement_homes_df['name'] == selection].iloc[0]
        icon_type = 'home'
        color = 'darkgreen'

        lat = location['geometry_location_lat']
        lng = location['geometry_location_lng']
        phone_number = location['phone_number']
        address = location['vicinity']

        st.sidebar.markdown(f"**Phone Number:** {phone_number}")
        st.sidebar.markdown(f"**Address:** {address}")
        
elif first_option == 'School':
    show_all = st.sidebar.checkbox('Show all Schools', value=False)
    if show_all:
        add_markers(schools_df, 'graduation-cap', 'darkred')
    else:
        options = schools_df['name'].sort_values().tolist()
        selection = st.sidebar.selectbox('Select a School:', options, index=0)
        location = schools_df[schools_df['name'] == selection].iloc[0]

        icon_type = 'graduation-cap'
        color = 'darkred'

        lat = location['geometry_location_lat']
        lng = location['geometry_location_lng']
        phone_number = location['phone_number']
        address = location['vicinity']

        st.sidebar.markdown(f"**Phone Number:** {phone_number}")
        st.sidebar.markdown(f"**Address:** {address}")

st.sidebar.write('**Please select one of the following:**')
dog_option = st.sidebar.checkbox('Dogs')
cat_option = st.sidebar.checkbox('Cats')

if 'location' in locals() and not selection == "":
    lat = location['geometry_location_lat']
    lng = location['geometry_location_lng']
    folium.Marker(
        location=[lat, lng],
        tooltip=selection,
        popup=selection,
        icon=folium.Icon(icon=icon_type, prefix='fa', color=color)
).add_to(map)

#need to recalculate cat coordinate

#function to calculate the distance
from geopy.distance import geodesic
def calculate_distance(coord):
    '''selected coordinate and coord need to be topple of lat, long  '''
    try:
        return geodesic((lat,lng), coord).kilometers
    except:
        return None

if cat_option is True:
    cats_coordinates['Distance'] = cats_coordinates['Coordinate'].apply(calculate_distance)
    # Filter for rows where Distance < 20
    filtered_cat = cats_coordinates[cats_coordinates['Distance'] < 50]
    # Use 'Street Address' for the multiselect options
    options = filtered_cat['Street Address'].tolist()
    # Display the multiselect widget
    selected_options = st.multiselect(
        'Select your options:',
        options,  # List of addresses to display
    )
    if selected_options:
        selected_rows = filtered_cat[filtered_cat['Street Address'].isin(selected_options)]
        st.write('Selected shelters/rescues:', selected_rows)




#elif dog_option is True:
    #dog_coordinates['Distance'] = dog_coordinates['Coordinate'].apply(calculate_distance)
    #filtered_dog = dog_coordinates[dog_coordinates['Distance'] < 20]


map_html = 'map.html'
map.save(map_html)

with open(map_html, 'r') as f:
    components.html(f.read(), height=600)

