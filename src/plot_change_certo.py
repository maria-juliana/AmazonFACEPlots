# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 15:47:16 2024

@author: Maria Juliana Monte | mjmm.monte@gmail.com
"""

import streamlit as st
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, PanTool, WheelZoomTool, ResetTool, SaveTool, BoxZoomTool, WheelPanTool, ZoomInTool, ZoomOutTool
import geopandas as gpd
from shapely.geometry import Point, Polygon, mapping
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from bokeh.models import GeoJSONDataSource, Label, LabelSet, ColumnDataSource
from math import pi
import pandas as pd

#%%

#Opening our trees file
arvre = pd.read_csv('data/plot_trees.csv')
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
exp=pd.read_csv('data/plot_exp.csv')
exp['COORD'] = exp[['LON', 'LAT']].values.tolist()
exp['COORD'] = exp['COORD'].apply(Point)
exp = gpd.GeoDataFrame(exp, geometry='COORD')

litter = exp.iloc[0:30,:]
sresp = exp.iloc[30:60,:]
soil = exp.iloc[60:90,:]
cod = exp.iloc[90:98,:]

#%% ALL TREES

#Creating our GeoJSON data
geodf = gpd.read_file('data/shp/amzfaceplotscomp.shp')
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

#%% CREATING THE PLOT IN BARS WITH FEW INFO WHEN CLICKING 100mm

plot1 = arvre100.iloc[0:42,:].sort_values(by='HEIGHT', ascending=True)
plot1['IND'] = plot1['IND'].astype(str)
data1 = {'x': plot1['HEIGHT'], 'y': plot1['IND'], 'family': plot1['Family']}
sourcep1 = ColumnDataSource(data=data1)

plot2 = arvre100.iloc[42:100,:].sort_values(by='HEIGHT', ascending=True)
plot2['IND'] = plot2['IND'].astype(str)
data2 = {'x': plot2['HEIGHT'], 'y': plot2['IND'], 'family': plot2['Family']}
sourcep2 = ColumnDataSource(data=data2)

plot3 = arvre100.iloc[100:158,:].sort_values(by='HEIGHT', ascending=True)
plot3['IND'] = plot3['IND'].astype(str)
data3 = {'x': plot3['HEIGHT'], 'y': plot3['IND'], 'family': plot3['Family']}
sourcep3 = ColumnDataSource(data=data3)

plot4 = arvre100.iloc[158:210,:].sort_values(by='HEIGHT', ascending=True)
plot4['IND'] = plot4['IND'].astype(str)
data4 = {'x': plot4['HEIGHT'], 'y': plot4['IND'], 'family': plot4['Family']}
sourcep4 = ColumnDataSource(data=data4)

plot6 = arvre100.iloc[210:252,:].sort_values(by='HEIGHT', ascending=True)
plot6['IND'] = plot6['IND'].astype(str)
data6 = {'x': plot6['HEIGHT'], 'y': plot6['IND'], 'family': plot6['Family']}
sourcep6 = ColumnDataSource(data=data6)

plot7 = arvre100.iloc[252:298,:].sort_values(by='HEIGHT', ascending=True)
plot7['IND'] = plot7['IND'].astype(str)
data7 = {'x': plot7['HEIGHT'], 'y': plot7['IND'], 'family': plot7['Family']}
sourcep7 = ColumnDataSource(data=data7)

infos1 = figure(width=900, height=500, toolbar_location='left', tools='', x_range=plot1['IND'])
plot1i = infos1.vbar(x='y', top='x', source=sourcep1, width=0.75, color='navy', name='hovertree1')
infos1.xaxis.major_label_orientation = 0.7
infos1.xaxis.axis_label = "Tree ID"
infos1.yaxis.axis_label = "Height (m)"
infos1.grid.grid_line_color = None

infos2 = figure(width=900, height=500, toolbar_location='left', tools='', x_range=plot2['IND'])
plot2i = infos2.vbar(x='y', top='x', source=sourcep2, width=0.75, color='navy', name='hovertree2')
infos2.xaxis.major_label_orientation = 0.7
infos2.xaxis.axis_label = "Tree ID"
infos2.yaxis.axis_label = "Height (m)"
infos2.grid.grid_line_color = None

infos3 = figure(width=900, height=500, toolbar_location='left', tools='', x_range=plot3['IND'])
plot3i = infos3.vbar(x='y', top='x', source=sourcep3, width=0.75, color='navy', name='hovertree3')
infos3.xaxis.major_label_orientation = 0.7
infos3.xaxis.axis_label = "Tree ID"
infos3.yaxis.axis_label = "Height (m)"
infos3.grid.grid_line_color = None

infos4 = figure(width=900, height=500, toolbar_location='left', tools='', x_range=plot4['IND'])
plot4i = infos4.vbar(x='y', top='x', source=sourcep4, width=0.75, color='navy', name='hovertree4')
infos4.xaxis.major_label_orientation = 0.7
infos4.xaxis.axis_label = "Tree ID"
infos4.yaxis.axis_label = "Height (m)"
infos4.grid.grid_line_color = None

infos6 = figure(width=900, height=500, toolbar_location='left', tools='', x_range=plot6['IND'])
plot6i = infos6.vbar(x='y', top='x', source=sourcep6, width=0.75, color='navy', name='hovertree6')
infos6.xaxis.major_label_orientation = 0.7
infos6.xaxis.axis_label = "Tree ID"
infos6.yaxis.axis_label = "Height (m)"
infos6.grid.grid_line_color = None

infos7 = figure(width=900, height=500, toolbar_location='left', tools='', x_range=plot7['IND'])
plot7i = infos7.vbar(x='y', top='x', source=sourcep7, width=0.75, color='navy', name='hovertree7')
infos7.xaxis.major_label_orientation = 0.7
infos7.xaxis.axis_label = "Tree ID"
infos7.yaxis.axis_label = "Height (m)"
infos7.grid.grid_line_color = None

hovertree1 = HoverTool(tooltips=[('ID', '@y'), ('Height (m)', '@x'), ('Family', '@family')], 
                        renderers=[plot1i])
hovertree2 = HoverTool(tooltips=[('ID', '@y'), ('Height (m)', '@x'), ('Family', '@family')], 
                        renderers=[plot2i])
hovertree3 = HoverTool(tooltips=[('ID', '@y'), ('Height (m)', '@x'), ('Family', '@family')], 
                        renderers=[plot3i])
hovertree4 = HoverTool(tooltips=[('ID', '@y'), ('Height (m)', '@x'), ('Family', '@family')], 
                        renderers=[plot4i])
hovertree6 = HoverTool(tooltips=[('ID', '@y'), ('Height (m)', '@x'), ('Family', '@family')], 
                        renderers=[plot6i])
hovertree7 = HoverTool(tooltips=[('ID', '@y'), ('Height (m)', '@x'), ('Family', '@family')], 
                        renderers=[plot7i])

infos1.add_tools(hovertree1)
infos2.add_tools(hovertree2)
infos3.add_tools(hovertree3)
infos4.add_tools(hovertree4)
infos6.add_tools(hovertree6)
infos7.add_tools(hovertree7)

#%%
#Pie chart PLOT1
pie1 = arvre.iloc[0:197,:]
pie1['sum'] = 1
pie1 = pie1['sum'].groupby(pie1['Family']).sum()
pie1 = pie1.reset_index().sort_values(by='sum', ascending=False)
pie1 = pie1.iloc[0:11,:]

pie1['angle'] = pie1['sum'] / pie1['sum'].sum() * 2 * pi
pie1['color'] = Category20c[len(pie1)]

pie1c = figure(height=350, title="Family Distribution", toolbar_location='left', tools="hover", tooltips="@Family: @sum", x_range=(-0.5, 1.0))

plotp1 = pie1c.wedge(x=0, y=1, radius=0.4, 
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Family', source=pie1)

pie1c.axis.axis_label = None
pie1c.axis.visible = False
pie1c.grid.grid_line_color = None

#Pie chart PLOT2
pie2 = arvre.iloc[197:444,:]
pie2['sum'] = 1
pie2 = pie2['sum'].groupby(pie2['Family']).sum()
pie2 = pie2.reset_index().sort_values(by='sum', ascending=False)
pie2 = pie2.iloc[0:11,:]

pie2['angle'] = pie2['sum'] / pie2['sum'].sum() * 2 * pi
pie2['color'] = Category20c[len(pie2)]


pie2c = figure(height=350, title="Family Distribution", toolbar_location=None, tools="hover", tooltips="@Family: @sum", x_range=(-0.5, 1.0))

plotp2 = pie2c.wedge(x=0, y=1, radius=0.4, 
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Family', source=pie2)

pie2c.axis.axis_label = None
pie2c.axis.visible = False
pie2c.grid.grid_line_color = None

#Pie chart PLOT3
pie3 = arvre.iloc[444:674,:]
pie3['sum'] = 1
pie3 = pie3['sum'].groupby(pie3['Family']).sum()
pie3 = pie3.reset_index().sort_values(by='sum', ascending=False)
pie3 = pie3.iloc[0:11,:]

pie3['angle'] = pie3['sum'] / pie3['sum'].sum() * 2 * pi
pie3['color'] = Category20c[len(pie3)]

pie3c = figure(height=350, title="Family Distribution", toolbar_location=None, tools="hover", tooltips="@Family: @sum", x_range=(-0.5, 1.0))

plotp3 = pie3c.wedge(x=0, y=1, radius=0.4, 
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Family', source=pie3)

pie3c.axis.axis_label = None
pie3c.axis.visible = False
pie3c.grid.grid_line_color = None

#Pie chart PLOT4
pie4 = arvre.iloc[674:908,:]
pie4['sum'] = 1
pie4 = pie4['sum'].groupby(pie4['Family']).sum()
pie4 = pie4.reset_index().sort_values(by='sum', ascending=False)
pie4 = pie4.iloc[0:11,:]

pie4['angle'] = pie4['sum'] / pie4['sum'].sum() * 2 * pi
pie4['color'] = Category20c[len(pie4)]

pie4c = figure(height=350, title="Family Distribution", toolbar_location=None, tools="hover", tooltips="@Family: @sum", x_range=(-0.5, 1.0))

plotp4 = pie4c.wedge(x=0, y=1, radius=0.4, 
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Family', source=pie4)

pie4c.axis.axis_label = None
pie4c.axis.visible = False
pie4c.grid.grid_line_color = None

#Pie chart PLOT6
pie6 = arvre.iloc[908:1136,:]
pie6['sum'] = 1
pie6 = pie6['sum'].groupby(pie6['Family']).sum()
pie6 = pie6.reset_index().sort_values(by='sum', ascending=False)
pie6 = pie6.iloc[0:11,:]

pie6['angle'] = pie6['sum'] / pie6['sum'].sum() * 2 * pi
pie6['color'] = Category20c[len(pie6)]

pie6c = figure(height=350, title="Family Distribution", toolbar_location=None, tools="hover", tooltips="@Family: @sum", x_range=(-0.5, 1.0))

plotp6 = pie6c.wedge(x=0, y=1, radius=0.4, 
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Family', source=pie6)

pie6c.axis.axis_label = None
pie6c.axis.visible = False
pie6c.grid.grid_line_color = None

#Pie chart PLOT7
pie7 = arvre.iloc[1136:1360,:]
pie7['sum'] = 1
pie7 = pie7['sum'].groupby(pie7['Family']).sum()
pie7 = pie7.reset_index().sort_values(by='sum', ascending=False)
pie7 = pie7.iloc[0:11,:]

pie7['angle'] = pie7['sum'] / pie7['sum'].sum() * 2 * pi
pie7['color'] = Category20c[len(pie7)]

pie7c = figure(height=350, title="Family Distribution", toolbar_location=None, tools="hover", tooltips="@Family: @sum", x_range=(-0.5, 1.0))

plotp7 = pie7c.wedge(x=0, y=1, radius=0.4, 
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Family', source=pie7)

pie7c.axis.axis_label = None
pie7c.axis.visible = False
pie7c.grid.grid_line_color = None
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
    
    plot_info = st.selectbox('Select Plot', ["Plot 1", "Plot 2", "Plot 3", "Plot 4", "Plot 6", "Plot 7"])
    
    if plot_info == "Plot 1":
        st.bokeh_chart(infos1)
        st.bokeh_chart(pie1c)
    elif plot_info == "Plot 2":
        st.bokeh_chart(infos2)   
        st.bokeh_chart(pie2c)
    elif plot_info == "Plot 3":
        st.bokeh_chart(infos3) 
        st.bokeh_chart(pie3c)
    elif plot_info == "Plot 4":
        st.bokeh_chart(infos4)
        st.bokeh_chart(pie4c)
    elif plot_info == "Plot 6":
        st.bokeh_chart(infos6) 
        st.bokeh_chart(pie6c)
    elif plot_info == "Plot 7":
        st.bokeh_chart(infos7)
        st.bokeh_chart(pie7c)    
