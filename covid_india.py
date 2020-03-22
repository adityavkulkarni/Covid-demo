#!/usr/bin/env python
import numpy as np 
import pandas as pd 
import os
# Visualisation libraries
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry
import plotly.express as px
from plotly.offline import init_notebook_mode, iplot 
import plotly.graph_objs as go
import plotly.offline as py
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
from pywaffle import Waffle
import json
import plotly
import plotly.express as px
import folium
from folium import plugins
from data import get_data_from_kaggle,highlight_max
import warnings
from flask import Flask,render_template

plt.style.use("fivethirtyeight")
plt.rcParams['figure.figsize'] = 10, 8
plt.rcParams['image.cmap'] = 'viridis'
warnings.filterwarnings('ignore')
sns.set()

get_data_from_kaggle()
df= pd.read_csv('data/Covid cases in India.csv')
df_india = df.copy()

India_coord = pd.read_csv('data/indian_coord.csv')

dbd_India = pd.read_excel('data/per_day_cases.xlsx',sheet_name='India')
dbd_Italy = pd.read_excel('data/per_day_cases.xlsx',sheet_name="Italy")
dbd_Korea = pd.read_excel('data/per_day_cases.xlsx',sheet_name="Korea")

df.drop(['S. No.'],axis=1,inplace=True)
df['Total cases'] = df['Total Confirmed cases (Indian National)'] + df['Total Confirmed cases ( Foreign National )'] 
df['Active cases'] = df['Total cases'] - (df['Cured/Discharged/Migrated'] + df['Deaths'])
print(f'Total number of Confirmed COVID 2019 cases across India:', df['Total cases'].sum())
print(f'Total number of Active COVID 2019 cases across India:', df['Active cases'].sum())
print(f'Total number of Cured/Discharged/Migrated COVID 2019 cases across India:', df['Cured/Discharged/Migrated'].sum())
print(f'Total number of Deaths due to COVID 2019  across India:', df['Deaths'].sum())
print(f'Total number of States/UTs affected:', len(df['Name of State / UT']))

highlighted_df  = df.style.apply(highlight_max,subset=['Cured/Discharged/Migrated', 'Deaths','Total cases','Active cases'])

total_state_wise  = df.groupby('Name of State / UT')['Active cases'].sum().sort_values(ascending=False).to_frame()
total_state_wise  = total_state_wise .style.background_gradient(cmap='Reds')

fig1 = px.bar(df.sort_values('Active cases', ascending=False).sort_values('Active cases', ascending=True),
             x="Active cases", y="Name of State / UT", 
             title='Total Active Cases', 
             text='Active cases', 
             orientation='h', 
             width=1000, height=1000, range_x = [0, max(df['Active cases'])])
fig1.update_traces(marker_color='#467dcf', opacity=0.8, textposition='inside')
fig1.update_layout(plot_bgcolor='rgb(250, 242, 242)')
#fig.show()
total_active_cases = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

'''
df_condensed = pd.DataFrame([df['Active cases'].sum(),df['Cured/Discharged/Migrated'].sum(),df['Deaths'].sum()],columns=['Cases'])
df_condensed.index=['Active cases','Recovered','Death']

fig = plt.figure(
    FigureClass=Waffle, 
    rows=5,
    values=df_condensed['Cases'],
    labels=list(df_condensed.index),
    figsize=(10, 3),
    legend={'loc': 'upper left', 'bbox_to_anchor': (1.1, 1)}
)
df_full = pd.merge(India_coord,df,on='Name of State / UT')
map_india = folium.Map(location=[20, 80], zoom_start=3.5,tiles='Stamen Toner')

for lat, lon, value, name in zip(df_full['Latitude'], df_full['Longitude'], df_full['Active cases'], df_full['Name of State / UT']):
    folium.CircleMarker([lat, lon],
                        radius=value*0.7,
                        popup = ('<strong>State</strong>: ' + str(name).capitalize() + '<br>'
                                '<strong>Active Cases</strong>: ' + str(value) + '<br>'),
                        color='red',
                        
                        fill_color='red',
                        fill_opacity=0.3 ).add_to(map_india)
map_india
f, ax = plt.subplots(figsize=(12, 8))
data = df_full[['Name of State / UT','Total cases','Cured/Discharged/Migrated','Deaths']]
data.sort_values('Total cases',ascending=False,inplace=True)
sns.set_color_codes("pastel")
sns.barplot(x="Total cases", y="Name of State / UT", data=data,
            label="Total", color="r")
sns.set_color_codes("muted")
sns.barplot(x="Cured/Discharged/Migrated", y="Name of State / UT", data=data,
            label="Recovered", color="g")


# Add a legend and informative axis label
ax.legend(ncol=2, loc="lower right", frameon=True)
ax.set(xlim=(0, 35), ylabel="",
       xlabel="Cases")
sns.despine(left=True, bottom=True)
'''

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=dbd_India['Date'], y=dbd_India['Total Cases'],
                    mode='lines+markers',name='Total Cases'))
fig2.add_trace(go.Scatter(x=dbd_India['Date'], y=dbd_India['Recovered'],
                mode='lines',name='Recovered'))
fig2.add_trace(go.Scatter(x=dbd_India['Date'], y=dbd_India['Active'],
                mode='lines',name='Active'))
fig2.add_trace(go.Scatter(x=dbd_India['Date'], y=dbd_India['Deaths'],
                mode='lines',name='Deaths'))
fig2.update_layout(title_text='Trend of Coronavirus Cases in India(Cumulative cases)',plot_bgcolor='rgb(250, 242, 242)')
#fig2.show()
trends = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)


fig3= px.bar(dbd_India, x="Date", y="New Cases", barmode='group',  height=400)
fig3.update_layout(title_text='New Coronavirus Cases in India per day',plot_bgcolor='rgb(250, 242, 242)')
#fig.show()
new_cases_per_day = map_html = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)


app = Flask(__name__)
@app.route('/')
def index():

    return render_template('index.html', plot1=total_active_cases,plot2 = trends, plot3 = new_cases_per_day)

app.run()