# import the library
import fhnw_ds_weatherstation_client as weather
import time
# import os

# DB and CSV config
config = weather.Config()
config.db_host='influxdb'

# connect to DB
weather.connect_db(config)

# import latest data (delta between last data point in DB and current time)
weather.import_latest_data(config)

# Wait 30 minutes and then restart
time.sleep(1800)
