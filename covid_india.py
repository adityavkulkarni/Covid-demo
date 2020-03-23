#!/usr/bin/env python
import pandas as pd 
import plotly.express as px
from plotly.offline import init_notebook_mode, iplot 
import plotly.graph_objs as go
import plotly.offline as py
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
import json
import plotly
import plotly.express as px
from utils import highlight_max,create_table,update_data,yesterday
import warnings
from flask import Flask,render_template,Markup
from datetime import date

d1 = yesterday()

warnings.filterwarnings('ignore')

new_cases = update_data()
df= pd.read_csv('data/covidin.csv')
df_india = df.copy()

#India_coord = pd.read_csv('data/indian_coord.csv')

dbd_India = pd.read_csv('data/perday.csv')

#df.drop(['S. No.'],axis=1,inplace=True)
df['Total cases'] = df['Total Confirmed cases (Indian National)'] + df['Total Confirmed cases ( Foreign National )'] 
df['Active cases'] = df['Total cases'] - (df['Cured/Discharged/Migrated'] + df['Deaths'])

confirmed_cases = df['Total cases'].sum()
active_cases = df['Active cases'].sum()
cured_cases = df['Cured/Discharged/Migrated'].sum()
death_d =df['Deaths'].sum()
'''
print(f'Total number of Confirmed COVID 2019 cases across India:', df['Total cases'].sum())
print(f'Total number of Active COVID 2019 cases across India:', df['Active cases'].sum())
print(f'Total number of Cured/Discharged/Migrated COVID 2019 cases across India:', df['Cured/Discharged/Migrated'].sum())
print(f'Total number of Deaths due to COVID 2019  across India:', df['Deaths'].sum())
print(f'Total number of States/UTs affected:', len(df['Name of State / UT']))
'''
highlighted_df  = df.style.apply(highlight_max,subset=['Cured/Discharged/Migrated', 'Deaths','Total cases','Active cases'])

total_state_wise  = df.groupby('Name of State / UT')['Active cases'].sum().sort_values(ascending=False).to_frame()
#total_state_wise  = total_state_wise .style.background_gradient(cmap='Reds')

fig1 = px.bar(df.sort_values('Active cases', ascending=False).sort_values('Active cases', ascending=True),
             x="Active cases", y="Name of State / UT", 
             
             text='Active cases', 
             orientation='h', 
             height=550,width=900, range_x = [0, max(df['Active cases'])])
fig1.update_traces(marker_color='#f44336', opacity=0.8, textposition='inside')
fig1.update_layout(plot_bgcolor='rgb(236, 236, 236)',paper_bgcolor='rgba(0,0,0,0)')
#fig.show()
total_active_cases = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)


fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=dbd_India['Date'], y=dbd_India['Total Cases'],
                    mode='lines+markers',name='Total Cases'))
fig2.add_trace(go.Scatter(x=dbd_India['Date'], y=dbd_India['Recovered'],
                mode='lines',name='Recovered'))
fig2.add_trace(go.Scatter(x=dbd_India['Date'], y=dbd_India['Active'],
                mode='lines',name='Active'))
fig2.add_trace(go.Scatter(x=dbd_India['Date'], y=dbd_India['Deaths'],
                mode='lines',name='Deaths'))
fig2.update_layout(plot_bgcolor='rgb(236, 236, 236)',paper_bgcolor='rgba(0,0,0,0)',height=900,width=1800)
#fig2.show()
trends = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)


fig3= px.bar(dbd_India, x="Date", y="New Cases", barmode='group',  height=550,width=900)
fig3.update_layout(plot_bgcolor='rgb(236, 236, 236)',paper_bgcolor='rgba(0,0,0,0)')
fig3.update_traces(marker_color='#8bc34a', opacity=0.8)
#fig.show()
new_cases_per_day = map_html = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

#467dcf
#print(Markup(create_table(total_state_wise)))



app = Flask(__name__)

@app.route('/')
def index():

    #return render_template('index.html', plot1=total_active_cases,plot2 = trends, plot3 = new_cases_per_day)
    return render_template('dash.html',date = d1,active_cases = active_cases, total_confirmed = confirmed_cases, cured_cases = cured_cases, deaths = death_d ,table = Markup(create_table(total_state_wise)),plot1=total_active_cases,plot2 = trends, plot3 = new_cases_per_day,new_cases=new_cases)



app.run()

