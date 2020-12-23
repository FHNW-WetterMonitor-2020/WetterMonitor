# Base Data Import

## !This will clear the database and load all Data until the end of 2020 from Files!

This process must be manually started in the first time setup and will most likely not be needed again.

## Start import process
Run start-script in:
/wettermonitor/base-data/start.sh

This will run a container which will clear the influxdb and load all the Data stored in:
/wettermonitor/base-data/build/data/*.csv
