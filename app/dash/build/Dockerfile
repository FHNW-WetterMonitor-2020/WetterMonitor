FROM python:3.8

RUN apt-get update
RUN pip3 install install fhnw_ds_weatherstation_client


RUN pip3 install dash
RUN pip3 install dash-bootstrap-components

ADD app /app
WORKDIR /app


CMD ["python", "main.py"]
