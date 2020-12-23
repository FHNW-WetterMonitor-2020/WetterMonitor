# InfluxDB

This process start automatically when the system starts up.

## Start import process
Run start-script in:
/wettermonitor/influxdb/start.sh

This will run a container which contains the InfluxDB database and a container with Chronograph running at: http://localhost:8888

`influxdb-data` and `influxdb.conf` are mounted into the container so it persists even when the container gets removed.
