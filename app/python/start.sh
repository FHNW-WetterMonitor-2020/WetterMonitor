#!/bin/bash

docker build -t wetter-monitor-python build/
docker stop wetter_monitor_python
docker rm wetter_monitor_python

docker run -it \
	--network host \
	--name wetter_monitor_python \
	wetter-monitor-python

