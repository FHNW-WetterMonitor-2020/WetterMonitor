import dash
import dash_bootstrap_components as dbc
#from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import datetime
import pytz
from influxdb import InfluxDBClient
from Vorhersage import get_datapoint, get_last_timestamp, make_pred, make_timestamp_readable, name_winddir

client = InfluxDBClient('influxdb', 8086, '', '', 'meteorology')

#Zeitzonen festlegen
old_timezone = pytz.timezone('UTC')
new_timezone = pytz.timezone('Europe/Zurich')

#Aktuellster timestamp von Tiefenbrunnen
last_data = get_last_timestamp("tiefenbrunnen")
timestamp_now = pd.Timestamp(last_data[0])

#Meldung, wenn nicht die aktuellsten Daten angezeigt werden (älter als 35min = 2100s).
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
liste = [str(timestamp_now.year-1), "-", "{0:0=2d}".format(timestamp_now.month), "-", "{0:0=2d}".format(timestamp_now.day), " ", "{0:0=2d}".format(timestamp_now.hour), ":", "{0:0=2d}".format(timestamp_now.minute), ":00"]
timestamp_hist = "".join(liste)
datapoint = get_datapoint(timestamp_hist)
for item in datapoint:
    temperature_hist = item[0]['air_temperature']
    luftdruck_hist = item[0]['barometric_pressure_qfe']

#Graph für die Lufttemperatur definieren
liste = [str(timestamp_now.year), "-", "{0:0=2d}".format(timestamp_now.month), "-", "{0:0=2d}".format(timestamp_now.day), " ", "{0:0=2d}".format(timestamp_now.hour-5), ":", "{0:0=2d}".format(timestamp_now.minute), ":00"]
timestamp_dauer = "".join(liste)
query = 'SELECT air_temperature FROM "tiefenbrunnen" WHERE time > $timestamp'
bind_params = {'timestamp': timestamp_dauer}
res = client.query(query, bind_params=bind_params)
zeitverlauf = []
temperaturverlauf = []
for item in res:
    data = item
for i in range(len(data)):
    timestamp = pd.Timestamp(item[i]['time'])
    old = old_timezone.localize(datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, 0))
    timestamp_loc = old.astimezone(new_timezone)
    zeitverlauf.append(timestamp_loc)
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


# Zeitzone ändern
old_now = old_timezone.localize(datetime.datetime(timestamp_now.year, timestamp_now.month, timestamp_now.day, timestamp_now.hour, timestamp_now.minute, 0))
tst_now_loc = old_now.astimezone(new_timezone)
timestamp_hist = pd.Timestamp(timestamp_hist)
old_hist = old_timezone.localize(datetime.datetime(timestamp_hist.year, timestamp_hist.month, timestamp_hist.day, timestamp_hist.hour, timestamp_hist.minute, 0))
tst_hist_loc = old_hist.astimezone(new_timezone)

app = dash.Dash(
        # external_stylesheets=[dbc.themes.BOOTSTRAP]
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
            html.H3(["Aktualisiert am ", tst_now_loc.day, ".", tst_now_loc.month, ".", tst_now_loc.year, " um ", tst_now_loc.hour, ":", tst_now_loc.minute]),
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


    #rechter Abschnitt: Wettervorhersage
    html.Div([
        html.Div([
            html.H1("Wettervorhersage"),
        ]),

        html.Div([
            html.P(["Lufttemperatur um ", (tst_now_loc.hour +s)%24, ":", tst_now_loc.minute, " Uhr"]),
            html.H3([temperature_pred, " °C"]),
        ], style={'marginBottom': 30, 'marginTop': 25}),

        html.Div([
            html.P("Niederschlag in 24h: "),
            html.H3(niederschlag),
        ], style={'marginBottom': 30, 'marginTop': 25}),

        html.Div([
            html.H1("Historische Daten"),
            html.H3(["vom ", tst_hist_loc.day, ".", tst_hist_loc.month, ".", tst_hist_loc.year, " um ", tst_hist_loc.hour, ":", tst_hist_loc.minute]),
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
    app.run_server(debug=True, host='0.0.0.0')
