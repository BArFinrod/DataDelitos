import pandas as pd
import pickle
from pathlib import Path
import folium
import streamlit as st
from folium.plugins import HeatMap, HeatMapWithTime
from folium.plugins import GroupedLayerControl
import plotly.express as px
from streamlit_plotly_events import plotly_events
import plotly.graph_objects as go
from PIL import Image

########### Estilos write
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.medium-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.small-font {
    font-size:10px !important;
}
</style>
""", unsafe_allow_html=True)
########
p = Path(__file__).parent / "Delitos_clustered.pickle"
# p = "Delitos_clustered.pickle"
with open(p,'rb') as f:
  df = pickle.load(f)
  df_list = pickle.load(f)

f = folium.Figure(height=750)
hmap = folium.Map(location=[-16.356240, -71.572237], zoom_start=13, tiles='stamentoner', min_zoom=12, max_zoom=14)

opts = ['Mañana: 06:00 - 11:59 hrs.', 'Tarde: 12:00 - 17:59 hrs.', 'Noche: 18:00 - 05:59 hrs.']
dtime = dict(zip(opts,[0,1,2]))


# time = st.select_slider(
#     'Horario',
#     options=opts)

hm_wide = HeatMapWithTime(df_list,
                  min_opacity=0.1,
                  index = ['Mañana: 06:00-11:59 hrs.','Tarde: 12:00-17:59 hrs.','Noche: 18:00-05:59 hrs.'],
                  radius=30,
                  gradient = {0.2:'cyan', 0.6: 'purple', 0.8:'red',1:'yellow'}, use_local_extrema=True,
                  name='Delitos denunciados',
                  auto_play=False, speed_step=0.1
                 )


hmap.add_child(hm_wide)
f.add_child(hmap)

# Graph zones-clustring
figm = px.scatter_mapbox(df, lon="longitudNoised", lat="latitudNoised", color="Lugares", zoom=11)
figm.update_layout(yaxis_range=[-16.42,-16.28],
                  xaxis_range=[-71.64,-71.49],
                  mapbox_style="stamen-toner", mapbox={'layers':[{"minzoom": 12, "maxzoom": 10 }]})

## distancias ya medidas en el plano cartesiano
## label de cada cluster y uso de la latitud y longitud

#### Graph barras
df0 = df.groupby('Lugares').agg({'Lugares':'count'}).rename({'Lugares':'conteo'}, axis=1).sort_values('conteo', ascending=False)
fig = px.bar(df0.reset_index(), x='Lugares', y='conteo', text_auto=True)
fig.update_layout(
    xaxis_title_text='Lugares', # xaxis label
    yaxis_title_text='Número de delitos', # yaxis label
    bargap=0.2, # gap between bars of adjacent location coordinates
)
######## seleccionar puntos

######## pasar a Streamlit
## Logo
image = Image.open(Path(__file__).parent / 'Logo_blanco.jpeg')
st.image(image, width=150)
##
st.title("Delitos denunciados en Yanahuara, Cayma y Cerro Colorado en 2017")
st.markdown('<p class="medium-font">En los siguientes gráficos interactivos se muestra la distribución geográfica de los delitos denunciados en los distritos de Yanahuara, Cayma y Cerro Colorado del departamento de Arequipa, Perú. La información fue obtenida del Registro Nacional de Denuncias de Delitos y Faltas elaborada por el Instituto Nacional de Estadística e Informática en 2017 - último año en el que se obtuvo esta información con este nivel de detalle -.', unsafe_allow_html=True)
st.markdown('<p class="medium-font">Las direcciones son registradas de forma textual (Ejemplo: "av. Ejército cuadra 07 a la altura del bypass") y se diseñó un algoritmo de consulta a <i>Open Street Maps</i> para obtener las coordenadas aproximadas de ocurrencia (latitud y longitud).', unsafe_allow_html=True)
st.markdown('<p class="medium-font">Luego, se utilizaron técnicas de aprendizaje no supervisado para la identificación de zonas con alta densidad de delitos.', unsafe_allow_html=True)
st.markdown('<p class="medium-font">Debe indicarse que en Perú la tasa de denuncias por delitos es de apenas 16.3% (INEI, 2021).', unsafe_allow_html=True)
st.markdown('<p class="big-font">Gráfico 01. Evolución de los delitos denunciados</p>', unsafe_allow_html=True)
st.components.v1.html(f._repr_html_(), height=750)
st.markdown('<p class="small-font">Nota: Se han utilizado únicamente a los delitos contra el patrimonio, contra la vida, el cuerpo y la salud, contra la seguridad pública y contra la libertad. En total, en los 3 distritos se encontraron 5,033 casos denunciados en 2017. Las ubicaciones son aproximadas y se identificaron realizando consultas de las direcciones que aparecen en el registro policial en <i>Open Street Maps</i> a través de https://photon.komoot.io/api/. Instituto Nacional de Estadística e Informática (INEI) (2021). Informe técnico: Estadísticas de seguridad ciudadana. Marzo-agosto de 2021. Lima: INEI </p>', unsafe_allow_html=True)
st.markdown('<p class="small-font">Fuente: Registro Nacional de Denuncias de Delitos y Faltas 2017, Instituto Nacional de Estadística e Informática, Perú.</p>', unsafe_allow_html=True)
st.markdown("""---""")
st.markdown('<p class="big-font">Gráfico 02. Identificación de zonas de alta densidad de delitos</p>', unsafe_allow_html=True)
st.markdown('<p class="medium-font">Se han identificado hasta 21 zonas con alta densidad de ocurrencia de delitos denunciados. La frecuencia de delitos en cada zona aparece en el Gráfico 03. </p>', unsafe_allow_html=True)
st.plotly_chart(figm, use_container_width=True)
st.markdown('<p class="small-font">Nota: Agrupación preliminar de delitos utilizando el algoritmo <i> Hierarchical Density-Based Spatial Clustering of Application with Noise (HDBSCAN)</i>. Ubicación aproximada.</p>', unsafe_allow_html=True)
st.markdown('<p class="small-font">Fuente: Registro Nacional de Denuncias de Delitos y Faltas 2017, Instituto Nacional de Estadística e Informática, Perú.</p>', unsafe_allow_html=True)
st.markdown('<p class="big-font">Gráfico 03. Número de casos en las zonas identificadas</p>', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown("""---""")
########
# figm2 = px.scatter_mapbox(df, lon="longitudNoised", lat="latitudNoised", zoom=11, colorscale='reds')
figm2 = go.Figure(go.Scattermapbox(lat=df["latitudNoised"], lon=df["longitudNoised"], marker=go.scattermapbox.Marker(
            size=5,
            color='rgb(255, 0, 0)',
            opacity=0.7
        )))
figm2.update_layout(yaxis_range=[-16.42,-16.28],
                  xaxis_range=[-71.64,-71.49],
                  mapbox_style="stamen-toner",
                  margin=dict(l=20, r=20, t=20, b=20))

figm2.update_layout(
    mapbox=dict(
        bearing=0,
        center=dict(
            lat=-16.356771,
            lon=-71.565407
        ),
        pitch=0,
        zoom=10.5
    ),
)

st.markdown('<p class="big-font">Gráfico 04. Delitos según hora de ocurrencia (Mapa interactivo)</p>', unsafe_allow_html=True)
st.markdown('<p class="medium-font">En el siguiente gráfico, utilice las herramientas de selección en la parte superior derecha <i>"Box select"</i> y <i>"Lasso select"</i></p> para elegir un grupo de casos sobre los que se obtendrá la información de la hora de ocurrencia. El resultado se mostrará en el Gráfico 05', unsafe_allow_html=True)
selected_points = plotly_events(figm2, click_event=False, select_event=True)
st.markdown('<p class="small-font">Nota: Ubicación aproximada.</p>', unsafe_allow_html=True)
st.markdown('<p class="small-font">Fuente: Registro Nacional de Denuncias de Delitos y Faltas 2017, Instituto Nacional de Estadística e Informática, Perú.</p>', unsafe_allow_html=True)

# selected_points
# if len(selected_points)>0:
#   st.text_area(f"Hola!{selected_points}")
points = []
for point in selected_points:
  points.append(point['pointIndex'])

# figkde = plt.figure(figsize=(10, 4))
dfpoints = df.iloc[points]
dfpoints = dfpoints.loc[dfpoints["IH204_HOR"]<=24]
dfpoints['IH204_HOR'] = pd.to_datetime(dfpoints['IH204_HOR'], format='%H')#.dt.time
fighist = px.histogram(dfpoints, x="IH204_HOR", color_discrete_sequence=['indianred'], text_auto=True)
# fighist = px.bar(dfpoints, x="IH204_HOR", color_discrete_sequence=['indianred'], text_auto=True)
fighist.update_layout(
    xaxis_title_text='Hora de ocurrencia de los delitos', # xaxis label
    yaxis_title_text='Número de delitos', # yaxis label
    bargap=0.2, # gap between bars of adjacent location coordinates
)
fighist.update_xaxes(type='date', 
                 tickformat='%H:%M', 
                 nticks=24)
fighist.update_traces(hovertemplate ='<i>Hora:</i>:' + '%{x}' + '<extra></extra>',
                  selector=dict(type="histogram"))
st.markdown('<p class="big-font">Gráfico 05. Distribución de los delitos denunciados según hora de ocurrencia</p>', unsafe_allow_html=True)
st.plotly_chart(fighist)
# plt.xlabel('Hora del día')
# st.pyplot(figkde)
