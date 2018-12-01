#!/usr/bin/env bash

systemctl stop snipslogger

cp snipslogger.service /etc/systemd/system

systemctl daemon-reload
systemctl enable snipslogger
systemctl start snipslogger
