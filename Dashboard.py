import pandas as pd
pd.DataFrame.iteritems = pd.DataFrame.items
import numpy as np
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
import pickle
import folium


st.set_page_config(layout="wide")

retirement_homes_df = pd.read_csv('https://raw.githubusercontent.com/TheLazyCactus/Data_Thieves_project/refs/heads/main/retirement_homes_df.csv')
schools_df = pd.read_csv('https://raw.githubusercontent.com/TheLazyCactus/Data_Thieves_project/refs/heads/main/schools_df.csv')
#retirement_location = 'https://raw.githubusercontent.com/TheLazyCactus/Data_Thieves_project/refs/heads/main/retirement_coordinate.csv'
#school_location = 'https://raw.githubusercontent.com/TheLazyCactus/Data_Thieves_project/refs/heads/main/school_coordinate.csv'
cat_location = 'https://raw.githubusercontent.com/TheLazyCactus/Data_Thieves_project/refs/heads/main/cat_coordinate.csv'

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

if 'location' in locals() and not selection == "":
    lat = location['geometry_location_lat']
    lng = location['geometry_location_lng']
    folium.Marker(
        location=[lat, lng],
        tooltip=selection,
        popup=selection,
        icon=folium.Icon(icon=icon_type, prefix='fa', color=color)
).add_to(map)

#Function to transform the selection in coordinate
from geopy.geocoders import Nominatim

def address_to_coordinates(address):
    """
    Transforms a given address into geographic coordinates (latitude and longitude).
    
    Args:
        address (str): The address to be geocoded.
        
    Returns:
        tuple: A tuple containing latitude and longitude as floats.
               Returns None if the address cannot be geocoded.
    """
    try:
        # Initialize geolocator
        geolocator = Nominatim(user_agent="address_to_coordinates_app")
        # Geocode the address
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            print("Address not found.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

coordinate = address_to_coordinates(location)

#function to calculate the distance
from geopy.distance import geodesic
def calculate_distance(coord):
    '''selected coordinate and coord need to be topple of lat, long  '''
    try:
        return geodesic(coordinate, coord).kilometers
    except:
        return None
    
cat_location['Distance'] = cat_location['Coordinate'].apply(calculate_distance)
filtered_cat = cat_location[cat_location['Distance'] < 20]

map_html = 'map.html'
map.save(map_html)

with open(map_html, 'r') as f:
    components.html(f.read(), height=600)

