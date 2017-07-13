import machine, network, sys, time

import config
import readtemps

def deep_sleep(duration):
    print("Deep sleeping for %d secs" % duration)
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, duration * 1000)
    machine.deepsleep()

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

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')

ap = network.WLAN(network.AP_IF)
if ap.active():
    print('Disabling AP_IF')
    ap.active(False)

nic = network.WLAN(network.STA_IF)
wifi_connect(nic)

try:
    readtemps.read_temps()
    deep_sleep(60)
except Exception as e:
    print("Got exception")
    sys.print_exception(e)
    machine.reset()
