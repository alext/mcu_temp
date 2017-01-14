import config
import urequests

import machine, onewire, ds18x20, time

def load_ds():
    return ds18x20.DS18X20(onewire.OneWire(machine.Pin(config.W1_GPIO)))

def rom_id(raw):
    return ''.join("%02x" % b for b in raw)

def run():
    ds = load_ds()
    roms = ds.scan()

    while True:
        print("Reading temperature")
        ds.convert_temp()
        time.sleep_ms(750)
        for rom in roms:
            r = rom_id(rom)
            if r in config.SENSORS:
                url = config.SENSORS[r]
                temp = ds.read_temp(rom)
                print("Sensor %s, Read temperature %f" % (r, temp))
                data = {"temperature": int(temp * 1000)}
                resp = urequests.put(url, json=data)
                if resp.status_code != 200:
                    print("Sensor %s, Non-200 response %d" % (r, resp.status_code))
                    print(resp.reason)
                    print(resp.text)
            else:
                print("Unknown rom_id %s" % r)

        print("Sleeping for 60 secs")
        time.sleep(60)
