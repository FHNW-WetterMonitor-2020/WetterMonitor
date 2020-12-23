#!/bin/bash

docker build -t wetter-monitor-python:incremental-data build/
docker stop wetter_monitor_python_incremental-data
docker rm wetter_monitor_python_incremental-data

docker run -d \
	--net wettermonitor \
	--name wetter_monitor_python_incremental-data \
	--restart unless-stopped \
	wetter-monitor-python:incremental-data
