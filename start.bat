#!/bin/bash

cd wettermonitor

# Start InfluxDB Container
cd influxdb
call start.bat

# Start Python Container
cd ../python
call start.bat

