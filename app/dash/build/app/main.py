import dash
#from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
import pandas as pd
import datetime
import pytz
from influxdb import InfluxDBClient
from Vorhersage import get_datapoint, get_last_timestamp, make_pred, make_timestamp_readable, name_winddir

client = InfluxDBClient('influxdb', 8086, '', '', 'meteorology')

#Aktuellster timestamp von Tiefenbrunnen
last_data = get_last_timestamp("tiefenbrunnen")
timestamp_now = pd.Timestamp(last_data[0])

#Meldung, wenn nicht die aktuellsten Daten angezeigt werden.
diff_now = (datetime.datetime.now(pytz.utc) - timestamp_now).seconds
if diff_now > 2100:
    inet = "Bitte prüfen Sie die Internetverbindung."
else:
    inet = "Sie sehen die aktuellsten Daten."

#Alle aktuellen Werte abfragen
datapoint = get_datapoint(make_timestamp_readable(timestamp_now))
for item in datapoint:
    temperature_now = item[0]['air_temperature']
    windchill_now = item[0]['windchill']
    winddir_now = item[0]['wind_direction']
    windspeed_now = item[0]['wind_speed_avg_10min']
    watertemp_now = item[0]['water_temperature']
    luftdruck_now = item[0]['barometric_pressure_qfe']

winddir = name_winddir(winddir_now)

#historische Daten
#str(timestamp_now.minute)
liste = [str(timestamp_now.year-1), "-", str(timestamp_now.month), "-", str(timestamp_now.day), " ", str(timestamp_now.hour), ":", "00", ":00"]
timestamp_hist = "".join(liste)
print(timestamp_hist)
datapoint = get_datapoint(timestamp_hist)
for item in datapoint:
    temperature_hist = item[0]['air_temperature']
    luftdruck_hist = item[0]['barometric_pressure_qfe']

#Graph für die Lufttemperatur definieren
liste = [str(timestamp_now.year), "-", str(timestamp_now.month), "-", str(timestamp_now.day), " ", str(timestamp_now.hour-5), ":", str(timestamp_now.minute), ":00"]
timestamp_dauer = "".join(liste)
query = 'SELECT air_temperature FROM "tiefenbrunnen" WHERE time > $timestamp'
bind_params = {'timestamp': timestamp_dauer}
res = client.query(query, bind_params=bind_params)
zeitverlauf = []
temperaturverlauf = []
for item in res:
    data = item
for i in range(len(data)):
    zeitverlauf.append(item[i]['time'])
    temperaturverlauf.append(item[i]['air_temperature'])
fig = go.Figure(data=[go.Scatter(x=zeitverlauf, y=temperaturverlauf)])
fig.update_xaxes(title_text="Uhrzeit")
fig.update_yaxes(title_text="Lufttemperatur [°C]")


#Vorhersage der Lufttemperatur in s Stunden
s = 5
temperature_pred = make_pred(timestamp_now, temperature_now, s)

#Vorhersage von Niederschlag innerhalb der nächsten 24h
if luftdruck_now <= 955:
    niederschlag = "JA"
else:
    niederschlag = "NEIN"

app = dash.Dash(
	external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = html.Div([
    dcc.Interval(
        id="update",
        interval=10*60*1000
    ),
    html.Div([
        html.P("Wählen Sie die gewünschte Wetterstation aus:"),
        dcc.Dropdown(
            id="slct-station",
            options=[
                {'label': 'Tiefenbrunnen', 'value': 'tiefenbrunnen'},
                {'label': 'Mythenquai', 'value': 'mythenquai'}
            ],
            value='tiefenbrunnen',
            style={'width': "40%"}
        )
    ]),

    html.Div([
        dcc.Graph(id="Temperaturverlauf", figure=fig)
    ],style={'text-align': 'left', 'display': 'inline-block'}),

    #Mittlerer Abschnitt: Aktuelle Wetterdaten
    html.Div([
        html.Div([
            html.H1("Aktuelle Wetterdaten"),
            html.H3(["Aktualisiert am ", timestamp_now.day, ".", timestamp_now.month, ".", timestamp_now.year, " um ", timestamp_now.hour, ":", timestamp_now.minute]),
            html.H4(inet),
        ]),

        html.Div([
            html.P("Lufttemperatur: "),
            html.H3([temperature_now, " °C"]),
        ], style={'marginBottom': 30, 'marginTop': 25}),

        html.Div([
            html.P("Gefühlte Lufttemperatur: "),
            html.H3([windchill_now, " °C"]),
        ], style={'marginBottom': 30, 'marginTop': 25} ),

        html.Div([
            html.P("Windrichtung: "),
            html.H3([winddir," (", winddir_now, "°)"]),
        ], style={'marginBottom': 30, 'marginTop': 25}),

        html.Div([
            html.P("Windgeschwindigkeit: "),
            html.H3([windspeed_now, " m/s"]),
        ], style={'marginBottom': 30, 'marginTop': 25}),

        html.Div([
            html.P("Wassertemperatur: "),
            html.H3([watertemp_now, " °C"]),
        ], style={'marginBottom': 30, 'marginTop': 25}),

        html.Div([
            html.P("Luftdruck: "),
            html.H3([luftdruck_now, " hPa"]),
        ], style={'marginBottom': 30, 'marginTop': 25}),

    ], style={'text-align': 'left', 'display': 'inline-block'}),

    #html.Div([
        #html.H3(children ="Wassertemperatur"),
        #dcc.Markdown("So kann ich **Fett** oder *kursiv* schreiben."),
        #html.P(children ="Die Wassertemperatur beträgt:"),
        #html.P(children = [water_temp, " °C"])
    #], style={'color': 'blue', 'fontSize': 14}),

    #html.Div([
        #html.Div([
            #html.H1(" __ ")
        #])
    #], style={'display': 'inline-block'}),

    #rechter Abschnitt: Wettervorhersage
    html.Div([
        html.Div([
            html.H1("Wettervorhersage"),
        ]),

        html.Div([
            html.P(["Lufttemperatur um ", (timestamp_now.hour +s)%24, ":", timestamp_now.minute, " Uhr"]),
            html.H3([temperature_pred, " °C"]),
        ], style={'marginBottom': 30, 'marginTop': 25}),

        html.Div([
            html.P("Niederschlag in 24h: "),
            html.H3(niederschlag),
        ], style={'marginBottom': 30, 'marginTop': 25}),

        html.Div([
            html.H1("Historische Daten"),
            html.H3(["von ", timestamp_hist]),
        ]),

        html.Div([
            html.P("Lufttemperatur: "),
            html.H3([temperature_hist, " °C"]),
        ], style={'marginBottom': 30, 'marginTop': 25}),

        html.Div([
            html.P("Luftdruck: "),
            html.H3([luftdruck_hist, " hPa"]),
        ], style={'marginBottom': 30, 'marginTop': 25}),
    ], style= {'text-align': 'left', 'display': 'inline-block'}),

], style= {'text-align': 'left', 'display': 'inline-block', 'vertical-align': 'middle'})



if __name__ == "__main__":
    app.run_server(debug=True, host = '0.0.0.0')
