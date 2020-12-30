from influxdb import InfluxDBClient
import pandas as pd
from datetime import datetime
import numpy as np
from math import sqrt

client = InfluxDBClient('influxdb', 8086, '', '', 'meteorology')

def get_last_timestamp(wetterstation):
    """Aktuellster timestamp einer Wetterstation abfragen"""
    query = 'SELECT last(air_temperature) FROM {}'.format(wetterstation)
    res = client.query(query)
    for item in res:
        timestamp_last = item[0]['time']
        temp_last = item[0]['last']
        return (timestamp_last, temp_last)

def get_datapoint(timestamp):
    """Alle Werte eines timestamps abfragen"""
    bind_params = {'timestamp': str(timestamp)}
    query = 'SELECT * FROM "tiefenbrunnen" WHERE time = $timestamp'
    res = client.query(query, bind_params=bind_params)
    return res

def make_timestamp_readable(timestamp):
    """Einen timestamp so formatieren, dass er als string von SELECT-Statement gelesen werden kann."""
    year = timestamp.year;
    month = timestamp.month;
    day = timestamp.day;
    hour = timestamp.hour
    return pd.Timestamp(year, month, day, hour)

def name_winddir(winddirection):
    """Den Gradangaben der Windrichtung einen Namen geben."""
    if 22.5 <= winddirection < 67.5:
        return 'N/O'
    elif 67.5 <= winddirection < 112.5:
        return 'O'
    elif 112.5 <= winddirection < 157.5:
        return 'S/O'
    elif 157.5 <= winddirection < 202.5:
        return 'S'
    elif 202.5 <= winddirection < 247.5:
        return 'S/W'
    elif 247.5 <= winddirection < 292.5:
        return 'W'
    elif 292.5 <= winddirection < 337.5:
        return 'N/W'
    elif winddirection < 22.5 and winddirection >= 337.5:
        return 'N'
    else:
        return 'kein Wind'

#Alle Werte werden gleich gewichtet; nicht unbedingt optimal
def euclidean_distance(row1, row2):
    """Berechnung der euklidischen Distanz zwischen den Werten der Reihe 1 und 2"""
    distance = 0.0
    for i in range(1, len(row1)):
        distance += (row1[i] - row2[i]) ** 2
    return sqrt(distance)

def get_neighbors(train, test_row, num_neighbors):
    """Aus den train Daten die nächsten Nachbarn für die test_row finden. Die Anzahl nächster Nachbarn kann
    über num_neighbors festgelegt werden."""
    distances = list()
    for train_row in train:
        dist = euclidean_distance(test_row, train_row)
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for i in range(num_neighbors):
        neighbors.append(distances[i][0])
    return neighbors

def make_pred(timestamp, temp, pred_duration):
    """Vorhersage der Lufttemperatur für den timestamp in +pred_duration Stunden machen."""
    timestamp_readable = make_timestamp_readable(timestamp)

    # Ähnliche Daten suchen
    res_akt = get_datapoint(timestamp_readable)
    # Nearest Neighbor wird im Zeitraum vor einem Jahr (+-60 Tage) gesucht; hier könnte man mehrere Jahre miteinbeziehen
    bind_params = {'temp': temp, 'timestamp': str(timestamp_readable)}
    query = 'SELECT * FROM "tiefenbrunnen" WHERE time > $timestamp-425d AND time < $timestamp-305d AND air_temperature = $temp'
    res = client.query(query, bind_params=bind_params)
    points = res.get_points()
    # Zuerst aktuelle Werte, dann Daten im gefilterten Zeitraum mit der gleichen Temperatur und mit similar daytime in array einfügen
    h_intervall = 2
    hour_min = (timestamp.hour - h_intervall) % 24
    hour_max = (timestamp.hour + h_intervall) % 24
    similar_daytime = range(hour_min, hour_max, 1)  # Range der Tageszeit; problematisch ab 22:00 Uhr; noch nicht optimal
    similar_data = []
    for item in res_akt:
        similar_data.append(list(item[0].values()))
    for item in points:
        if pd.Timestamp(item['time']).hour in similar_daytime:
            similar_data.append(list(item.values()))

    # In den ähnlichen Daten die k nächsten Nachbarn suchen; k+1 weil der Punkt sich selbst immer am nächsten ist
    k = 4
    neighbors = get_neighbors(similar_data, similar_data[0], k + 1)  # k+1 nächsten Datensätze als Nachbarn speichern
    neighbors = neighbors[1:]  # der erste ist immer der Datenpunkt selbst, somit kein echter Nachbar

    # Die Zukunftsdaten der nächsten Nachbarn suchen
    neighbor_pred = []
    for neighbor in neighbors:
        neighbor_pred.append(pd.Timestamp(neighbor[0]) + pd.Timedelta(pred_duration, 'h')) #timestamp verschieben
    air_temperature_pred = []
    for timestamp_pred in neighbor_pred:
        res = get_datapoint(make_timestamp_readable(timestamp_pred))
        for item in res:
            air_temperature_pred.append(item[0]['air_temperature'])

    # Aus diesen historischen Daten einen Vorhersagewert berechnen
    Mw_temp_pred = round(sum(air_temperature_pred) / len(air_temperature_pred), 1)
    return (Mw_temp_pred)
