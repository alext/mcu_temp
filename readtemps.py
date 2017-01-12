import config
import urequests

import machine, onewire, ds18x20, time

def run():
    ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(config.W1_GPIO)))
    roms = ds.scan()

    while True:
        print("Reading temperature")
        ds.convert_temp()
        time.sleep_ms(750)
        temp = ds.read_temp(roms[0])
        print("Read temperature %f" % temp)
        data = {"temperature": int(temp * 1000)}
        resp = urequests.put(config.SENSOR_URL, json=data)
        if resp.status_code != 200:
            print("Non-200 response %d" % resp.status_code)
            print(resp.reason)
            print(resp.text)

        print("Sleeping for 60 secs")
        time.sleep(60)
