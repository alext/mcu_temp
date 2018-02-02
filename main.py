import machine, network, sys, time

import config
import wifi
import readtemps

def deep_sleep(duration):
    print("Deep sleeping for %d secs" % duration)
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, duration * 1000)
    machine.deepsleep()

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')

try:
    wifi.setup()

    readtemps.read_temps()
    deep_sleep(60)
except Exception as e:
    print("Got exception")
    sys.print_exception(e)
    machine.reset()
