#!/bin/bash

# Create and enable a systemd service that autostarts the wettermonitor

sudo cp wetterMonitor.service /etc/systemd/system
sudo systemctl enable wetterMonitor.service


