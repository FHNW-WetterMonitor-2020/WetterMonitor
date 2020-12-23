#!/bin/bash

cd app

# Stop InfluxDB Container
cd influxdb
./stop.sh

# Stop Base Container
cd ../base-data
./stop.sh

# Stop Increment Container
cd ../increment-data
./stop.sh

# Stop Jupyter Container
cd ../jupyter
./stop.sh

# Stop Dash Container
cd ../dash
./stop.sh
