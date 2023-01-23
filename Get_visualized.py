# librerías
import pandas as pd



with open('/content/drive/MyDrive/Investigaciones/Delitos/Ubicaciones2/Base_vias.pickle','rb') as f:
  neg_via_poly = pickle.load(f)
  vias = pickle.load(f)



with open('/content/drive/MyDrive/Investigaciones/Delitos/Ubicaciones2/Base_yanahuara_cerrocolorado_cayma_2017_ubicaciones_V3.pickle','rb') as f:
  df = pickle.load(f)

dfH = df[['place_long_url_key','latitud','longitud','IH204_HOR']].sort_values('place_long_url_key').dropna().set_index('place_long_url_key')
# agregando time
# Dtotal = dfH.shape[0]
dfHm = dfH.loc[(dfH['IH204_HOR']>5) & (dfH['IH204_HOR']<=11)].groupby(['place_long_url_key','latitud','longitud']).agg({'IH204_HOR':'count'}).reset_index().set_index('place_long_url_key')
dfHt = dfH.loc[(dfH['IH204_HOR']>11) & (dfH['IH204_HOR']<=17)].groupby(['place_long_url_key','latitud','longitud']).agg({'IH204_HOR':'count'}).reset_index().set_index('place_long_url_key')
dfHn = dfH.loc[(dfH['IH204_HOR']>17) | (dfH['IH204_HOR']<=5)].groupby(['place_long_url_key','latitud','longitud']).agg({'IH204_HOR':'count'}).reset_index().set_index('place_long_url_key')
Dtotal = max(dfHm['IH204_HOR'].max(), dfHt['IH204_HOR'].max(), dfHn['IH204_HOR'].max())
dfHm['weight'] = dfHm['IH204_HOR']/Dtotal#/dfHm['IH204_HOR'].max()#/Dtotal
dfHt['weight'] = dfHt['IH204_HOR']/Dtotal#/dfHt['IH204_HOR'].max()#/Dtotal
dfHn['weight'] = dfHn['IH204_HOR']/Dtotal#/dfHn['IH204_HOR'].max()#/Dtotal
dfHmtn_list = [dfHm[['latitud','longitud','weight']].to_numpy().tolist(), dfHt[['latitud','longitud','weight']].to_numpy().tolist(), dfHn[['latitud','longitud','weight']].to_numpy().tolist()]
# dfHm['weight'].sum() + dfHt['weight'].sum() + dfHn['weight'].sum()


# heat map

hmap = folium.Map(location=[-16.391241, -71.542952], zoom_start=13)#, tiles='stamentoner')#, tiles='Stamen Terrain')

hm_wide = HeatMapWithTime(dfHmtn_list,
                  min_opacity=0.1,
                  radius=30,
                  gradient = {0.2:'cyan', 0.6: 'purple', 0.8:'red',1:'yellow'}, use_local_extrema=True
                 )

hmap.add_child(hm_wide)
# folium.GeoJson(neg_via_poly, style_function=lambda x: {'color':None,'fillColor':'black', 'fillOpacity' : 1}).add_to(hmap)
hmap
