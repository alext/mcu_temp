import network, time

import config

def connect(nic):
    if nic.isconnected():
        print('already connected to network, config:', nic.ifconfig())
        return

    print('connecting to network...')
    nic.active(True)
    nic.connect(config.WIFI_NAME, config.WIFI_PASSWORD)

def wait_for_connection(nic):
    print('waiting for connection')
    while not nic.isconnected():
        time.sleep_ms(100)
        print('.')
    print('network config:', nic.ifconfig())

def setup():
    ap = network.WLAN(network.AP_IF)
    if ap.active():
        print('Disabling AP_IF')
        ap.active(False)

    sta = network.WLAN(network.STA_IF)
    connect(sta)
    return sta
