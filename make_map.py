import pandas as pd
import folium
import numpy as np
import functools

df = pd.read_csv('coordinates.csv')

# Load map centred on average coordinates
my_map = folium.Map(location=[df.loc[0, 'latitude'], df.loc[0, 'longitude']], 
                    zoom_start=10, max_zoom=14)

def add_dot(point, m):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    folium.CircleMarker(location=[point.latitude, point.longitude], radius=1).add_to(m)

dot = functools.partial(add_dot, m=my_map)
df.apply(dot, axis=1)
 
#add a markers
# for i, point in df.iterrows():  
#     folium.Marker(point.latitude, point.longitude).add_to(my_map)
 
#fadd lines
# folium.PolyLine(np.array([df.loc[::10, 'latitude'].values, df.loc[::10, 'longitude'].values]).T).add_to(my_map)
 
# Save map
my_map.save("./gpx_test.html")