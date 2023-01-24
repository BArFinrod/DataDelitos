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
hmap = folium.Map(location=[-16.356240, -71.572237], zoom_start=13, tiles='stamentoner', min_zoom=12, max_zoom=14)

opts = ['Mañana: 06:00 - 11:59 hrs.', 'Tarde: 12:00 - 17:59 hrs.', 'Noche: 18:00 - 05:59 hrs.']
dtime = dict(zip(opts,[0,1,2]))

# time = st.slider('Horario', 0, 2, 1)
time = st.select_slider(
    'Horario',
    options=opts)

hm_wide = HeatMap(df_list[dtime[time]],
                  min_opacity=0.1,
                  radius=30,
                  gradient = {0.2:'cyan', 0.6: 'purple', 0.8:'red',1:'yellow'}, use_local_extrema=True
                 )

hmap.add_child(hm_wide)
# folium.GeoJson(shape_vias, style_function=lambda x: {'color':None,'fillColor':'black', 'fillOpacity' : 1}).add_to(hmap)
map_data = st_folium(hmap, key="fig1", width=700, height=700)
