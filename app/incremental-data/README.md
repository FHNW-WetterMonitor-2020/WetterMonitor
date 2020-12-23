# Incremental Data Import

This process start automatically when the system starts up.

## Start import process
Run start-script in:
/wettermonitor/incremental-data/start.sh

This will run a container which updates the wheater data to the most recent point in time.
After finishing, it will restart in 30 minutes.
