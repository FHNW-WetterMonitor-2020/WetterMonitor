#!/bin/bash

docker build -t wetter_monitor_dash build/
docker stop wetter_monitor_dash
docker rm wetter_monitor_dash

docker run -d \
	--network influxdb \
	-p 8050:8050 \
	--name wetter_monitor_dash \
	wetter_monitor_dash
