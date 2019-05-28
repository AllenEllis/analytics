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

import uuid
import random

from datetime import datetime

import pandas as pd

from django.core.cache import cache

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go

import dpd_components as dpd

from django_plotly_dash import DjangoDash
from django_plotly_dash.consumers import send_to_pipe_channel

#pylint: disable=too-many-arguments, unused-argument, unused-variable

app = DjangoDash('report_projections')

from fbprophet import Prophet
import dash
from dash.dependencies import Input, Output


engine = 'postgresql+psycopg2://analytics:dolphins@10.10.30.27/analytics'
query = 'SELECT "clientCreatedTime" as time, total / 100. as total FROM orders'
df = pd.io.sql.read_sql(query, con=engine)
df['time'] = pd.to_datetime(df['time'], unit='ms')
df.set_index('time', inplace=True)
df.dropna(inplace=True)
df.sort_index(inplace=True)

epochs = df.index.astype('int64') // 1e9
sample = df.resample('M').sum().index

app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.RangeSlider(
        id='datetimeSlider',
        updatemode='mouseup',
        min=epochs[0],
        max=epochs[-1],
        value=[epochs[0], epochs[-1]],
        marks=dict(
            zip((sample.astype('int64') // 1e9).astype('int64'),
                sample.strftime('%b %y'))),
    ),
    html.Br(),
    dcc.Checklist(
        id='seasonality',
        options=[
            {'label': 'Weekly', 'value': 'weekly'},
            {'label': 'Yearly', 'value': 'yearly'},
        ],
        values=['yearly']
    ),
    dcc.RadioItems(
        id='radio-agg',
        options=[
            {'label': 'Days', 'value': 'D'},
            {'label': 'Weeks', 'value': 'W'},
        ],
        value='D'
    )
])


@app.callback(
    Output('graph', 'figure'),
    [
        Input('datetimeSlider', 'value'),
        Input('seasonality', 'values'),
        Input('radio-agg', 'value')
    ],
)
def update_figure(span, season, agg):
    dff = df.resample(agg).sum()
    dff = dff[dff['total'] > 0]

    span = pd.to_datetime(span, unit='s')
    mask = (dff.index >= span[0]) & (dff.index < span[-1])
    dff = dff[mask]

    ddf = dff.reset_index().dropna()
    ddf.columns = ['ds', 'y']

    parameters = {'weekly_seasonality': False, 'yearly_seasonality': False}
    if 'yearly' in season:
        parameters['yearly_seasonality'] = True
    if ('weekly' in season) & (agg == 'D'):
        parameters['weekly_seasonality'] = True
    m = Prophet(**parameters)
    m.fit(ddf)

    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    forecast = forecast[forecast['ds'] > dff.index.max()]

    trace0 = go.Scatter(
        x=dff.index,
        y=dff['total'],
        mode="markers+lines",
        name='data'
    )
    trace1 = go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat_lower'],
        fill= None,
        mode='lines',
        line={'color':'#0072B2'},
        showlegend=False
    )
    trace2 = go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat_upper'],
        fill='tonexty',
        mode='lines',
        line={'color': '#0072B2'},
        name='uncertainty'
    )
    trace3 = go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat'],
        mode="markers+lines",
        name='forecast'
    )
    data = [trace0, trace1, trace2, trace3]
    layout = go.Layout(
        xaxis={'title': 'Date'},
        yaxis={'title': 'Total ($)'},
    )
    figure = {'data': data, 'layout': layout}

    return figure
