import machine, sys

import config
import wifi
import readtemps

def deep_sleep(duration):
    print("Deep sleeping for %d secs" % duration)
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, duration * 1000)
    machine.deepsleep()

def device_id():
    return ''.join("%02x" % b for b in machine.unique_id())


def read_psu_voltage():
    raw = machine.ADC(0).read()
    return raw / config.VOLTAGE_DIVISOR


if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')

try:
    w = wifi.setup()
    s = readtemps.start_read()

    data = {
        "device_id": device_id(),
        "supply_voltage": read_psu_voltage(),
        "temperatures": readtemps.complete_read(s),
    }

    wifi.wait_for_connection(w)
    wifi.send_data(data)

    deep_sleep(60)
except Exception as e:
    print("Got exception")
    sys.print_exception(e)
    machine.reset()
