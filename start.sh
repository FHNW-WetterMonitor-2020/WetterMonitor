#!/bin/bash

cd /home/pi/fhnw2/WetterMonitor/app

sleep 10

# Start InfluxDB Container
cd influxdb
sudo ./start.sh
sleep 2

# Start Incremental-Data Container
cd ../incremental-data
sudo ./start.sh

# Start Jupyter Container
#cd ../jupyter
#./start.sh

# Start Dash Container
cd ../dash
sudo ./start.sh

# Wait for dash to start
sleep 3

chromium-browser --no-sandbox http://localhost:8050/
