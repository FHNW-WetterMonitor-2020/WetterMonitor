#!/bin/bash

cd app

# Start InfluxDB Container
cd influxdb
./stop.sh

# Start Python Container
cd ../python
./stop.sh

# Start Jupyter Container
cd ../jupyter
./stop.sh

