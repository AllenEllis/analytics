from reports.database import Connect, Orders, Events
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
import plotly
import numpy as np


def rendercode():
    return "Closeouts was rendered"


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
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
    [Input('checklist-days', 'values'),
    Input('radio-agg', 'value')],
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


if __name__ == '__main__':
    app.run_server(debug=True)