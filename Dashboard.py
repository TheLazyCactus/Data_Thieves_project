import pandas as pd
pd.DataFrame.iteritems = pd.DataFrame.items
import numpy as np
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
import pickle
import folium


st.set_page_config(layout="wide")

retirement_homes_df = pd.read_csv(r'C:\Users\biave\Documents\IronHack\Quests\Data_Thieves_Mine\retirement_homes_df.csv')
schools_df = pd.read_csv(r'C:\Users\biave\Documents\IronHack\Quests\Data_Thieves_Mine\schools_df.csv')

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


map_html = 'map.html'
map.save(map_html)

with open(map_html, 'r') as f:
    components.html(f.read(), height=600)

