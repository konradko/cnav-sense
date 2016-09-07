#!/bin/bash

echo "Enabling I2C"
modprobe i2c-dev

echo "Starting Papertrail"
bash /usr/src/app/config/papertrail.sh

echo "Starting OpenSSH"
bash /usr/src/app/config/openssh.sh

echo "Starting Prometheus"
bash /usr/src/app/config/prometheus.sh

python cnavsense/main.py
