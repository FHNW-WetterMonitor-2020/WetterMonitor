FROM python:3.8

RUN apt-get update
# RUN apt-get install curl gcc g++
# RUN pip3 install pandas==0.23.4

RUN pip3 install install fhnw_ds_weatherstation_client

ADD app /app
WORKDIR /app

CMD ["python", "main.py"]
