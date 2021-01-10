#!/bin/bash

cd app

# Start InfluxDB Container
cd influxdb
./start.sh

# Start Base-Data Container
cd ../base-data
./start.sh

cd ../../
./stop.sh

cd ../../../autostart
./autostart.sh