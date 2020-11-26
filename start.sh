#!/bin/bash

cd app

# Start InfluxDB Container
cd influxdb
./start.sh

# Start Python Container
cd ../python
./start.sh

# Start Jupyter Container
cd ../jupyter
./start.sh

