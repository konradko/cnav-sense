#!/bin/bash

mount -t devtmpfs none /dev
udevd --daemon

udevadm trigger
udevadm settle

# Shutdown the unnecessary usb0 spawned by g_mutli
ifconfig usb0 up

systemctl enable avahi-daemon
systemctl enable avahi-dnsconfd
