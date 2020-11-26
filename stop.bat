cd app

# Stop InfluxDB Container
cd influxdb
call stop.bat

# Stop Python Container
cd ../python
call stop.bat

# Stop Jupyter Container
cd ../jupyter
call stop.bat
