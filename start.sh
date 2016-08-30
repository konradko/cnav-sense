#!/bin/bash

echo "Starting Papertrail"
bash /usr/src/app/config/papertrail.sh

echo "Starting OpenSSH"
bash /usr/src/app/config/openssh.sh

echo "Starting Prometheus"
bash /usr/src/app/config/prometheus.sh

echo "Starting Avahi deamon"
systemctl enable avahi-daemon
systemctl enable avahi-dnsconfd

python cnavsense/main.py