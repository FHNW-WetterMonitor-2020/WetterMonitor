import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go

from influxdb import InfluxDBClient
import pandas as pd
from datetime import datetime
import numpy as np
from math import sqrt

client = InfluxDBClient('influxdb', 8086, '', '', 'meteorology')
query = 'SELECT last(air_temperature) FROM "{}"'.format("tiefenbrunnen")
res = client.query(query)
for item in res:
    timestamp_now = pd.Timestamp(item[0]['time'])
    temperature_now = item[0]['last']

print (timestamp_now, temperature_now)

#start = datetime.datetime.today() - relativedelta(years=13)
#end = datetime.datetime.today()
temp = temperature_now
water_temp = 5
#df = []
#trace_close = go.Scatter(x=list(df.index),
                         #y=list(df.close),
                         #name = "Close"
                         #line = dict(color="#3B7AA9"))
#data= {trace_close}
#layout = dict(title="Luftfeuchtigkeit",
              #showlegend=False)
#fig = dict (data=data, layout = layout)

app = dash.Dash()


app.layout = html.Div([
    html.Div([
        html.P(children ="Wählen Sie die gewünschte Wetterstation aus:"),
        dcc.Dropdown(
            id="slct-station",
            options=[
                {'label': 'Tiefenbrunnen', 'value': 'tiefenbrunnen'},
                {'label': 'Mythenquai', 'value': 'mythenquai'}
            ],
            value='TF',
            style={'width': "40%"}
        )
    ]),

    html.Div(html.H1(children ="Aktuelle Wetterdaten"), style={'text-align': 'left'}),
    #html.Label("Dash Graph")
    #html.Div(
        #dcc.Graph(id="Stock Chart",
                  #figure=fig)

    html.Div([
        html.H3(children ="Lufttemperatur"),
        html.P(children ="Die Lufttemperatur beträgt:"),
        html.P(children = [temp, " °C"]),
    ], style={'marginBottom': 50, 'marginTop': 25}),

    html.Div([
        html.H3(children ="Wassertemperatur"),
        dcc.Markdown("So kann ich **Fett** oder *kursiv* schreiben."),
        html.P(children ="Die Wassertemperatur beträgt:"),
        html.P(children = [water_temp, " °C"])
    ], style={'color': 'blue', 'fontSize': 14}),

    html.Div(html.H1(children ="Wettervorhersage"), style={'text-align': 'left'})

])

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')
