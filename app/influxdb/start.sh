#!/bin/bash
docker network create wettermonitor
docker stop influxdb
docker stop chronograph
docker rm influxdb
docker rm chronograph


docker run -d -p 8086:8086 \
	--name influxdb \
	--net wettermonitor \
	--net-alias influxdb \
	-v "/home/pi/fhnw2/WetterMonitor/app/influxdb/influxdb.conf":/etc/influxdb/influxdb.conf:ro \
	-v "/home/pi/fhnw2/WetterMonitor/app/influxdb/influxdb-data":/var/lib/influxdb \
	influxdb -config /etc/influxdb/influxdb.conf

docker run -d -p 8888:8888 \
	--name chronograph \
	--net wettermonitor \
	--net-alias chronograf \
	chronograf --influxdb-url=http://influxdb:8086
