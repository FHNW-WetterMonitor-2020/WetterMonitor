#!/bin/bash
docker network create influxdb

docker run -d -p 8086:8086 \
	--name influxdb \
	--network influxdb \
	--net-alias influxdb \
	-v "$PWD/influxdb.conf":/etc/influxdb/influxdb.conf:ro \
	-v "$PWD/influxdb-data":/var/lib/influxdb \
	influxdb -config /etc/influxdb/influxdb.conf

docker run -d -p 8888:8888 \
	--name chronograph \
	--net=influxdb \
	--net-alias chronograf \
	chronograf --influxdb-url=http://influxdb:8086
