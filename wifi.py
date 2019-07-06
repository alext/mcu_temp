import network, time

import urequests
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

def send_data(data):
    resp = urequests.put(config.UPDATE_URL, json=data)
    if resp.status_code != 200:
        print("Non-200 response %d updating sensors" % (resp.status_code))
        print(resp.reason)
        print(resp.text)
    resp.close()
