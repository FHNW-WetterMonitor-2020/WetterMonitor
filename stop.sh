#!/bin/bash

cd app

# Stop InfluxDB Container
cd influxdb
./stop.sh

# Stop Base Container
cd ../base-data
./stop.sh

# Stop Incremental Container
cd ../incremental-data
./stop.sh

# Stop Jupyter Container
cd ../jupyter
./stop.sh

# Stop Dash Container
cd ../dash
./stop.sh

docker network rm wettermonitor
