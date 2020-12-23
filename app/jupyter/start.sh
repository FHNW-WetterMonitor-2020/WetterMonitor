#!/bin/bash

docker build -t wetter_monitor_jupyter:1.0 build/
docker stop wetter_monitor_jupyter
docker rm wetter_monitor_jupyter

docker run -d \
	--network wettermonitor \
	-p 8890:8888 \
	--name wetter_monitor_jupyter \
	-v "$PWD/jupyter-data":/data/jupyter \
	-v "$PWD/jupyter.config":/root/.jupyter/jupyter_notebook_config.py \
	wetter_monitor_jupyter:1.0
