# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 15:47:16 2024

@author: Maria Juliana Monte | mjmm.monte@gmail.com
"""

import streamlit as st
from bokeh.plotting import figure
from bokeh.models import HoverTool, PanTool, WheelZoomTool, ResetTool, SaveTool
import geopandas as gpd
from shapely.geometry import Point, Polygon, mapping
from bokeh.models import GeoJSONDataSource, Label, LabelSet
import pandas as pd

#%%

#Opening our trees file
arvre = pd.read_excel(r'C:\Users\julia\Downloads\shapeamazonface\PLOTS_GEORREF_ATUAL.xlsx')
arvre['COORD'] = arvre[['LON', 'LAT']].values.tolist()
arvre['COORD'] = arvre['COORD'].apply(Point)
arvre = gpd.GeoDataFrame(arvre, geometry='COORD')

#Extracting our trunk respiration trees
arvre['DBH_2022'] = arvre['DBH_2022'].astype(int)

anel = arvre[arvre['SOIL_RESP'] == 1.0].copy()
anel = pd.DataFrame(anel)
anel['COORD'] = anel[['LON', 'LAT']].values.tolist()
anel['COORD'] = anel['COORD'].apply(Point)
anel = gpd.GeoDataFrame(anel, geometry='COORD')

arvre50 = arvre[arvre['DBH_2022'] >= 50.0].copy()
arvre50 = pd.DataFrame(arvre50)
arvre50['COORD'] = arvre50[['LON', 'LAT']].values.tolist()
arvre50['COORD'] = arvre50['COORD'].apply(Point)
arvre50 = gpd.GeoDataFrame(arvre50, geometry='COORD')

arvre100 = arvre[arvre['DBH_2022'] >= 100.0].copy()
arvre100 = pd.DataFrame(arvre100)
arvre100['COORD'] = arvre100[['LON', 'LAT']].values.tolist()
arvre100['COORD'] = arvre100['COORD'].apply(Point)
arvre100 = gpd.GeoDataFrame(arvre100, geometry='COORD')

#%%

#Opening our experiments file
exp=pd.read_excel(r'C:\Users\julia\Downloads\shapeamazonface\PLOTS_GEORREF_ATUAL.xlsx', sheet_name='exp')
exp['COORD'] = exp[['LON', 'LAT']].values.tolist()
exp['COORD'] = exp['COORD'].apply(Point)
exp = gpd.GeoDataFrame(exp, geometry='COORD')

litter = exp.iloc[0:30,:]
sresp = exp.iloc[30:60,:]
soil = exp.iloc[60:90,:]
cod = exp.iloc[90:98,:]

#%% ALL TREES

#Creating our GeoJSON data
geodf = gpd.read_file(r'C:\Users\julia\Downloads\shapeamazonface\amzfaceplotscomp.shp')
geodfJSON = geodf.to_json()

#Creating our Plot
p = figure(width=900, height=1900, toolbar_location='left', tools='')

#Adding GeoJSON patches
source = GeoJSONDataSource(geojson=geodfJSON)
p.patches(xs='xs', ys='ys', source=source, fill_alpha=0, line_color='black')

#Creating our GeoJSON Data source and plotting
arvreJSON = arvre.to_json()
source1 = GeoJSONDataSource(geojson=arvreJSON)
glyph_arvre = p.circle('x', 'y', size=5, color='red', alpha=0.8, source=source1)

anelJSON = anel.to_json()
source2 = GeoJSONDataSource(geojson=anelJSON)
glyph_anel = p.circle('x', 'y', size=5, color='navy', alpha=0.8, source=source2)

litterJSON = litter.to_json()
source3 = GeoJSONDataSource(geojson=litterJSON)
test4 = p.star('x', 'y', size=10, color='green', fill_alpha=0.8, source=source3, name='hover3')

srespJSON = sresp.to_json()
source4 = GeoJSONDataSource(geojson=srespJSON)
test5 = p.triangle('x', 'y', size=10, color='pink', fill_alpha=0.8, source=source4, name='hover4')

soilJSON = soil.to_json()
source5 = GeoJSONDataSource(geojson=soilJSON)
test6 = p.square('x', 'y', size=10, color='yellow', fill_alpha=0.8, source=source5, name='hover5')

codJSON = cod.to_json()
source6 = GeoJSONDataSource(geojson=codJSON)
test7 = p.diamond('x', 'y', size=10, color='brown', fill_alpha=0.8, source=source6, name='hover6')

#Adding the tools
hover = HoverTool(tooltips=[('ID', '@IND'), ('DBH (mm)', '@DBH_2022'), ('Height (m)', '@HEIGHT'), ('Family', '@Family'),\
                           ('Genus', '@Genus'), ('Species','@Species')], renderers=[glyph_arvre])
hover3 = HoverTool(tooltips=[('Equipment', '@NAME'), ('Cluster', '@CLUSTER')], renderers=[test4])
hover4 = HoverTool(tooltips=[('Equipment', '@NAME'), ('Cluster', '@CLUSTER')], renderers=[test5])
hover5 = HoverTool(tooltips=[('Equipment', '@NAME'), ('Cluster', '@CLUSTER')], renderers=[test6])
hover6 = HoverTool(tooltips=[('Equipment', '@NAME')], renderers=[test7])

p.add_tools(PanTool(), WheelZoomTool(), ResetTool(), SaveTool(), hover, hover3, hover4, hover5, hover6)

#Adding the tree label
for index, row in arvre.iterrows():
    label = Label(x=row['COORD'].x, y=row['COORD'].y, text=str(row['IND']), text_font_size='8px', x_offset=5, y_offset=5, render_mode='canvas')
    p.add_layout(label)
    
#%% TREES D >= 50mm

#Creating our Plot
p50 = figure(width=900, height=1900, toolbar_location='left', tools='')

#Adding GeoJSON patches
p50.patches(xs='xs', ys='ys', source=source, fill_alpha=0, line_color='black')

#Creating our GeoJSON Data source and plotting
arvre50JSON = arvre50.to_json()
source150 = GeoJSONDataSource(geojson=arvre50JSON)
glyph_arvre50 = p50.circle('x', 'y', size=5, color='red', alpha=0.8, source=source150)

#Trunk Resp
glyph_anel = p50.circle('x', 'y', size=5, color='navy', alpha=0.8, source=source2)
#Litter Trap
test4 = p50.star('x', 'y', size=10, color='green', fill_alpha=0.8, source=source3, name='hover3')
#Soil Resp
test5 = p50.triangle('x', 'y', size=10, color='pink', fill_alpha=0.8, source=source4, name='hover4')
#Soil 1m²
test6 = p50.square('x', 'y', size=10, color='yellow', fill_alpha=0.8, source=source5, name='hover5')
#COD
test7 = p50.diamond('x', 'y', size=10, color='brown', fill_alpha=0.8, source=source6, name='hover6')

#Adding the tools
hover50 = HoverTool(tooltips=[('ID', '@IND'), ('DBH (mm)', '@DBH_2022'), ('Height (m)', '@HEIGHT'), ('Family', '@Family'),\
                           ('Genus', '@Genus'), ('Species','@Species')], renderers=[glyph_arvre50])
hover3 = HoverTool(tooltips=[('Equipment', '@NAME'), ('Cluster', '@CLUSTER')], renderers=[test4])
hover4 = HoverTool(tooltips=[('Equipment', '@NAME'), ('Cluster', '@CLUSTER')], renderers=[test5])
hover5 = HoverTool(tooltips=[('Equipment', '@NAME'), ('Cluster', '@CLUSTER')], renderers=[test6])
hover6 = HoverTool(tooltips=[('Equipment', '@NAME')], renderers=[test7])

p50.add_tools(PanTool(), WheelZoomTool(), ResetTool(), SaveTool(), hover50, hover3, hover4, hover5, hover6)

#Adding the tree label
for index, row in arvre50.iterrows():
    label = Label(x=row['COORD'].x, y=row['COORD'].y, text=str(row['IND']), text_font_size='8px', x_offset=5, y_offset=5, render_mode='canvas')
    p50.add_layout(label)
    
#%% TREES D >= 100mm

#Creating our Plot
p100 = figure(width=900, height=1900, toolbar_location='left', tools='')

#Adding GeoJSON patches
source = GeoJSONDataSource(geojson=geodfJSON)
p100.patches(xs='xs', ys='ys', source=source, fill_alpha=0, line_color='black')

#Creating our GeoJSON Data source and plotting
arvre100JSON = arvre100.to_json()
source1100 = GeoJSONDataSource(geojson=arvre100JSON)
glyph_arvre100 = p100.circle('x', 'y', size=5, color='red', alpha=0.8, source=source1100)

#Trunk Resp
glyph_anel = p100.circle('x', 'y', size=5, color='navy', alpha=0.8, source=source2)
#Litter Trap
test4 = p100.star('x', 'y', size=10, color='green', fill_alpha=0.8, source=source3, name='hover3')
#Soil Resp
test5 = p100.triangle('x', 'y', size=10, color='pink', fill_alpha=0.8, source=source4, name='hover4')
#Soil 1m²
test6 = p100.square('x', 'y', size=10, color='yellow', fill_alpha=0.8, source=source5, name='hover5')
#COD
test7 = p100.diamond('x', 'y', size=10, color='brown', fill_alpha=0.8, source=source6, name='hover6')

#Adding the tools
hover100 = HoverTool(tooltips=[('ID', '@IND'), ('DBH (mm)', '@DBH_2022'), ('Height (m)', '@HEIGHT'), ('Family', '@Family'),\
                           ('Genus', '@Genus'), ('Species','@Species')], renderers=[glyph_arvre100])
hover3 = HoverTool(tooltips=[('Equipment', '@NAME'), ('Cluster', '@CLUSTER')], renderers=[test4])
hover4 = HoverTool(tooltips=[('Equipment', '@NAME'), ('Cluster', '@CLUSTER')], renderers=[test5])
hover5 = HoverTool(tooltips=[('Equipment', '@NAME'), ('Cluster', '@CLUSTER')], renderers=[test6])
hover6 = HoverTool(tooltips=[('Equipment', '@NAME')], renderers=[test7])

p100.add_tools(PanTool(), WheelZoomTool(), ResetTool(), SaveTool(), hover100, hover3, hover4, hover5, hover6)

#Adding the tree label
for index, row in arvre100.iterrows():
    label = Label(x=row['COORD'].x, y=row['COORD'].y, text=str(row['IND']), text_font_size='8px', x_offset=5, y_offset=5, render_mode='canvas')
    p100.add_layout(label)

#%%

# Streamlit UI
st.title('AmazonFACE Plots')

# Selectbox to choose diameter range
diameter_range = st.selectbox('Select Diameter Range (mm)', ["All", "50", "100"])

# Display the appropriate plot based on user selection
if diameter_range == "All":
    st.bokeh_chart(p)
elif diameter_range == "50":
    st.bokeh_chart(p50)
elif diameter_range == "100":
    st.bokeh_chart(p100)
