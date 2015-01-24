#!/bin/bash

cp /torstuff/config /etc/polipo/config
cp /torstuff/torrc /etc/tor/torrc

echo "restarting tor"
/etc/init.d/tor restart

echo "restarting polipo"
/etc/init.d/polipo stop | true

echo "Starting polipo daemon"
polipo
