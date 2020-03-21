import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
import pandas as pd 
import random
import math
import time
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
import datetime
import operator
plt.style.use('seaborn')

confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
deaths_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
recoveries_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')

cols = confirmed_df.keys()


confirmed = confirmed_df.loc[:, cols[4]:cols[-1]]
deaths = deaths_df.loc[:, cols[4]:cols[-1]]
recoveries = recoveries_df.loc[:, cols[4]:cols[-1]]

x = confirmed.keys()
y = []
i = 0 
while confirmed_df.loc[i,'Country/Region'] != 'India':
	i+=1
#i+=1 
reg = confirmed_df.loc[i,'Country/Region']
width=[]
for i in confirmed.loc[i,:]:
    y.append(i)
    width.append(1.5)


def create_plot():


    N = 40
    #x = np.linspace(0, 1, N)
    #y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
	

    data = [
        go.Bar(
	    
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y'],
	    
            text= y,
  	    textposition= 'auto',
  	    hoverinfo= 'none',
	    marker_color='rgb(55, 83, 109)'
            
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
from flask import Flask,render_template
app = Flask(__name__)
@app.route('/')
def index():

    bar = create_plot()
    return render_template('index.html', plot=bar,region = reg)

app.run()
