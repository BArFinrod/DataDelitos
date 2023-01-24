# librerías
import pandas as pd
import pickle
from pathlib import Path
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap, HeatMapWithTime
import streamlit as st


p = Path(__file__).parent / "Base_places_shapes.pickle"
with open(p,'rb') as f:
  df = pickle.load(f)
  df_list = pickle.load(f)
  shape_vias = pickle.load(f)

# heat map
hmap = folium.Map(location=[-16.356240, -71.572237], zoom_start=13, tiles='stamentoner', min_zoom=14, max_zoom=15)

time = st.slider('Horario', 0, 2, 1)

hm_wide = HeatMap(df_list[time],
                  min_opacity=0.1,
                  radius=30,
                  gradient = {0.2:'cyan', 0.6: 'purple', 0.8:'red',1:'yellow'}, use_local_extrema=True
                 )

hmap.add_child(hm_wide)
# folium.GeoJson(shape_vias, style_function=lambda x: {'color':None,'fillColor':'black', 'fillOpacity' : 1}).add_to(hmap)
map_data = st_folium(hmap, key="fig1", width=700, height=700)
