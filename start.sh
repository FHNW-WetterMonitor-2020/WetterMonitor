#!/bin/bash

# Start InfluxDB Container
cd app/influxdb
./start.sh

# Start InfluxDB Container
cd ../python
./start.sh

