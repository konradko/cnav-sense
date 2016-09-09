#!/bin/bash

echo "Enabling I2C"
modprobe i2c-dev

case "$PAPERTRAIL_ON" in
 true) bash /usr/src/app/config/papertrail.sh ;;
    *) echo "Papertrail not enabled" ;;
esac

case "$LOCAL_SSH_ON" in
 true) bash /usr/src/app/config/openssh.sh ;;
    *) echo "Local SSH not enabled" ;;
esac

case "$PROMETHEUS_ON" in
 true) bash /usr/src/app/config/prometheus.sh ;;
    *) echo "Prometheus not enabled" ;;
esac

python cnavsense/main.py
