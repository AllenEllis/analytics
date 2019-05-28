'''
Dash apps for the demonstration of functionality

Copyright (c) 2018 Gibbs Consulting and others - see CONTRIBUTIONS.md

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# pylint: disable=no-member

#import uuid
#import random

#from datetime import datetime

#from django.core.cache import cache





#import plotly.graph_objs as go

#import dpd_components as dpd

from django_plotly_dash import DjangoDash
#from django_plotly_dash.consumers import send_to_pipe_channel

#pylint: disable=too-many-arguments, unused-argument, unused-variable

from .database import Connect, Orders, Events
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
import plotly
import numpy as np

app = DjangoDash('report_orders')

engine = 'postgresql+psycopg2://analytics:dolphins@10.10.30.27/analytics'
with Connect(engine) as db:
    data = db.cursor.query(Orders.createdTime, Orders.total / 100.)
    events = db.cursor.query(Events.startTime, Events.title)

df0 = pd.DataFrame(
    data=[_[1] for _ in events],
    index=[_[0] for _ in events],
    columns=['Events'])
df0.index = pd.to_datetime(df0.index, unit='s').normalize()

df1 = pd.DataFrame(
    data=[_[1] for _ in data],
    index=[_[0] for _ in data],
    columns=['Total'])
df1.index = pd.to_datetime(df1.index, unit='ms').normalize()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='orders'),
    dcc.Checklist(id='checklist-days',
        options=[
          {'label': 'Monday', 'value': 0},
          {'label': 'Tuesday', 'value': 1},
          {'label': 'Wednesday', 'value': 2},
          {'label': 'Thursday', 'value': 3},
          {'label': 'Friday', 'value': 4},
          {'label': 'Saturday', 'value': 5},
          {'label': 'Sunday', 'value': 6},
        ],
        values=[0, 1, 2, 3, 4, 5]
        ),
    dcc.RadioItems(id='radio-agg',
        options=[
          {'label': 'Days', 'value': 'D'},
          {'label': 'Weeks', 'value': 'W'},
          {'label': 'Months', 'value': 'M'},
        ],
        value='D'
    )
])


@app.callback(
    Output('orders', 'figure'),
    [
        Input('checklist-days', 'values'),
        Input('radio-agg', 'value')
    ],
)
def update_figure(days, agg):
    dff = df1.resample(agg).sum()
    dff = dff.join(df0)
    dff.fillna('', inplace=True)
    if agg != 'D':
        days = [0, 1, 2, 3, 4, 5, 6]
    dff = dff[np.in1d(dff.index.dayofweek, days)]

    trace = go.Scatter(
        x=dff.index,
        y=dff['Total'],
        mode="markers+lines",
        text=dff['Events']
    )

    data = [trace]
    layout = go.Layout(
        xaxis={
            'title': 'Date',
            'rangeslider': {'visible': True},
            'type': 'date',
        },
            yaxis={'title': 'Total ($)'},
    )
    figure = {'data': data, 'layout': layout}

    return figure
