import machine, network, sys, time

import config
import readtemps

def wifi_connect(nic):
    if nic.isconnected():
        print('already connected to network, config:', nic.ifconfig())
        return

    print('connecting to network...')
    nic.active(True)
    nic.connect(config.WIFI_NAME, config.WIFI_PASSWORD)
    print('waiting for connection')
    while not nic.isconnected():
        time.sleep_ms(100)
        print('.')
    print('network config:', nic.ifconfig())

nic = network.WLAN(network.STA_IF)
wifi_connect(nic)

try:
    readtemps.run()
except Exception as e:
    print("Got exception")
    sys.print_exception(e)
    machine.reset()
