#!/bin/bash

cd wettermonitor

# Start InfluxDB Container
cd influxdb
call stop.bat

# Start Python Container
#cd ../python
#call stop.bat

# Start Python Container
cd ../jupyter
call stop.bat
