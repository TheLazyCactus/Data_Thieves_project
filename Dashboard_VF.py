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
dogs_df = pd.read_csv('https://raw.githubusercontent.com/TheLazyCactus/Data_Thieves_project/refs/heads/main/Dog_CA.csv', encoding='latin1')
#cats_coordinates = pd.read_csv(r'C:\Users\biave\Downloads\cat_coordinate.csv')
#dog_coordinates = pd.read_csv('https://raw.githubusercontent.com/TheLazyCactus/Data_Thieves_project/refs/heads/main/dog_coordinate.csv')
filtered_cat = {}

map = folium.Map(location=(34.04621475184492, -118.27514966412589))

st.sidebar.title("The Guardians of the Voiceless")
first_option = st.sidebar.selectbox(
    '**What type of establishment would you like to choose?** :house_buildings:', 
    ('Retirement Home', 'School'),
    index = None,
    placeholder= 'Please select one of the available options...'
)


def add_markers(df, icon_type, color):
    """This function will help us add the pins in the map for the retirement homes/schools - when we select show all"""
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['geometry_location_lat'], row['geometry_location_lng']],
            tooltip=row['name'],
            popup=row['name'],
            icon=folium.Icon(icon=icon_type, prefix='fa', color=color)
).add_to(map)
        


def add_markers_dogs(df, icon_type, color):
    """This function will help us add the pins in the map for the dogs coordinates - when we select show all"""
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['lat'], row['lng']],
            tooltip=row['Location'],
            popup=row['Location'],
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

        folium.Marker(
            location=[location['geometry_location_lat'], location['geometry_location_lng']],
            tooltip=location,
            popup=location,
            icon=folium.Icon(icon='home', prefix='fa', color='darkgreen')
).add_to(map)
        
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

        folium.Marker(
                location=[location['geometry_location_lat'], location['geometry_location_lng']],
                tooltip=location['name'],
                popup=location['name'],
                icon=folium.Icon(icon='graduation-cap', prefix='fa', color='darkred')
).add_to(map)
        
        lat = location['geometry_location_lat']
        lng = location['geometry_location_lng']
        phone_number = location['phone_number']
        address = location['vicinity']

        st.sidebar.markdown(f"**Phone Number:** {phone_number}")
        st.sidebar.markdown(f"**Address:** {address}")




second_option = st.sidebar.selectbox(
    '**What shelter would you like to choose?** :black_cat:', 
    (dogs_df["Shelter"].drop_duplicates().tolist()),
    index = None,
    placeholder= 'Please select one of the available options...'
)

show_all_shelters = st.sidebar.checkbox('Show every shelter', value=False)

if show_all_shelters:
    add_markers_dogs(dogs_df, 'paw', 'beige')
else:
    if second_option:
        # Add markers for all rows
        for _, row in dogs_df.iterrows():
            folium.Marker(
                location=[row['lat'], row['lng']],  # Pass lat and lng as a list
                popup=row['Shelter']  # Optional: Add a popup with the name
            ).add_to(map)
    
        # Get the specific row matching 'second_option'
        location = dogs_df[dogs_df['Shelter'] == second_option].iloc[0]
        lat = location['lat']  # Extract lat from the filtered row
        lng = location['lng']  # Extract lng from the filtered row
    
        # Add the highlighted marker
        folium.Marker(
            location=[lat, lng],
            tooltip=second_option,
            popup=second_option,
            icon=folium.Icon(icon='paw', prefix='fa', color='beige')
        ).add_to(map)


map_html = 'map.html'
map.save(map_html)

with open(map_html, 'r') as f:
    components.html(f.read(), height=600)

if second_option:
    filtered_dogs = dogs_df[dogs_df['Shelter'] == second_option]

    # Show the filtered dogs' information
    st.write(f"**Dogs available in {second_option}:**")

    # Loop through the filtered dogs and display their information
    for idx, row in filtered_dogs.iterrows():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <img src="{row['Image URL']}" alt="Dog Image"
                    class="profile-image" style="width:250px;height:250px;object-fit:cover;">
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.write(f"**Name:** {row['NAME']}")
            st.write(f"**Age:** {row['Age']}")
            st.write(f"**Breed:** {row['Breed']}")
            st.write(f"**Phone:** {row['Telephone']}")
            st.write(f"**Email:** {row['Email']}")