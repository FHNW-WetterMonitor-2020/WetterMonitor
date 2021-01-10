
# WetterMonitor

Project of Masar Mojzis, Strasser Chantal and Schertenleib Simon

## Application

The purpose of this Application is to provide a graphical user interface that shows weather data.

The weather data is automatically updated every 30 minutes and displayed through a custom `dash`-Dashboard.

The main entrypoint of the application is the `start.sh`-script in the root of the project. Everything needed will be started with this script.  

>IMPORTANT: MAKE SURE TO IMPORT THE BASE DATA FIRST WITH: `initial-setup.sh`!
>This initial setup adds the `start.sh`-script to the autostart of the raspberry-pi.  

## Docker

Through Docker, it is easy to abstract the applications away into docker images. They can easily be started and stopped through the Docker-CLI.

All Docker containers are part of a Docker Network `wettermonitor`, this allows them to reach each other over tcp connections.

Application critical containers have an automatic restart policy, so if an error occurs and they crash, 
they will automatically try to restart.  

A possible improvement could be to manage the docker containers through docker-compose, however that would require another package to be installed and maintained.

>IMPORTANT: When the incremental-data container cannot connect to the internet, add `nameserver 8.8.8.8` to the file `/etc/resolv.conf` to fix the issue.

## Components

### InfluxDB with Chronograph

Directory: `/WetterMonitor/app/influxdb/`

This is the Data part of the application. InfluxDB stores timeseries data of weather measurements (air-, and watertemperature, air pressure, etc.)

InfluxDB can be queried with SQL, see official documentation: https://docs.influxdata.com/influxdb/v1.8/query_language/explore-data/

Chronograph offers a native look on the data and can easily be used to manually explore the data really fast.

Chronograph is running on http://localhost:8888/

### Base-Data with Python

Directory: /WetterMonitor/app/base-data/

This component is only needed in the initial setup and must be manually started with the `initial-setup.sh`-script.

This component uses the public python package: `fhnw_ds_weatherstation_client` created by: `jelleschutter` https://pypi.org/project/fhnw-ds-weatherstation-client/

### Incremental-Data with Python

Directory: /WetterMonitor/app/incremental-data/

This component will automatically update the weather data every 30 minutes and save it in the InfluxDB.

>IMPORTANT: MAKE SURE TO IMPORT THE BASE DATA IN THE INITIAL SETUP FIRST!  

This component uses the public python package: `fhnw_ds_weatherstation_client` created by: `jelleschutter` https://pypi.org/project/fhnw-ds-weatherstation-client/

This component can be modified to add more sources of weather data.

### Dash User Interface

Directory: /WetterMonitor/app/dash/

The Dash component creates an HTML-UI with `python` and `dash`. It retrieves data from InfluxDB through SQL and visualizes it.

Dash is running on http://localhost:8050/

When starting the `WetterMonitor`, a fullscreen browser should automatically open with this:
`firefox -kiosk 'http://localhost:8050/'`

### Jupyter Notebook

Directory: /WetterMonitor/app/jupyter/

This provides a standard Jupyter-Notebook for development purposes.

Jupyter is running on http://localhost:8890/

With password: `wettermonitor`
