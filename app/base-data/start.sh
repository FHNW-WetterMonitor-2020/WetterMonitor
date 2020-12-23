#!/bin/bash

docker build -t wetter-monitor-python:base-import build/
docker stop wetter_monitor_python_base-import
docker rm wetter_monitor_python_base-import

docker run -it \
	--net wettermonitor \
	--name wetter_monitor_python_base-import \
	wetter-monitor-python:base-import
