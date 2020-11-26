cd app

# Start InfluxDB Container
cd influxdb
call start.bat

# Start Python Container
cd ../python
call start.bat

# Start Jupyter Container
cd ../jupyter
call start.bat

