#!/bin/sh

set -eu

PORT=${PORT:-/dev/ttyUSB0}
BAUD=${2:-115200}

ampy --port "${PORT}" --baud "${BAUD}" put vendor/urequests.py
ampy --port "${PORT}" --baud "${BAUD}" put boot.py
ampy --port "${PORT}" --baud "${BAUD}" put readtemps.py
ampy --port "${PORT}" --baud "${BAUD}" put wifi.py
ampy --port "${PORT}" --baud "${BAUD}" put config.py
ampy --port "${PORT}" --baud "${BAUD}" put main.py
