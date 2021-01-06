#!/bin/bash

cd app

# Start InfluxDB Container
cd influxdb
./start.sh

# Start Incremental-Data Container
cd ../incremental-data
./start.sh

# Start Jupyter Container
#cd ../jupyter
#./start.sh

# Start Dash Container
cd ../dash
./start.sh

# Wait for dash to start
sleep 3

chromium-browser --no-sandbox http://localhost:8050/
