FROM wetter-monitor-python:1.1

RUN pip install jupyterlab

RUN mkdir -p /data/jupyter
WORKDIR /data/jupyter

CMD ["jupyter", "lab", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
