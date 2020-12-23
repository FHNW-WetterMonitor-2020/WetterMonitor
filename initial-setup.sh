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

# WETTER_MONITOR_ROOT=$(pwd)
# echo "sudo bash $WETTER_MONITOR_ROOT/start.sh" >> /etc/rc.local