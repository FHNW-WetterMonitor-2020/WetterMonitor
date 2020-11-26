#!/bin/bash

docker build -t wetter-monitor-python:1.1 build/
docker stop wetter_monitor_python
docker rm wetter_monitor_python

docker run -it \
	--network influxdb \
	--name wetter_monitor_python \
	wetter-monitor-python:1.1

