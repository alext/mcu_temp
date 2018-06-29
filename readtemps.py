import config
import urequests

import machine, onewire, ds18x20, time

def load_ds():
    return ds18x20.DS18X20(onewire.OneWire(machine.Pin(config.W1_GPIO)))

def rom_id(raw):
    return ''.join("%02x" % b for b in raw)

def start_read():
    ds = load_ds()
    print("Initiating temperature read")
    ds.convert_temp()
    return time.ticks_ms()

def complete_read(prep_time):
    ds = load_ds()
    roms = ds.scan()

    delay = 750 - time.ticks_diff(time.ticks_ms(), prep_time)
    if delay > 0:
        time.sleep_ms(delay)

    data = {"temperatures": {}}
    for rom in roms:
        r = rom_id(rom)
        temp = ds.read_temp(rom)
        print("Sensor %s, Read temperature %f" % (r, temp))
        data["temperatures"][r] = int(temp * 1000)

    resp = urequests.put(config.UPDATE_URL, json=data)
    if resp.status_code != 200:
        print("Non-200 response %d updating sensors" % (resp.status_code))
        print(resp.reason)
        print(resp.text)
    resp.close()


def run():
    while True:
        complete_read(prepare_read())

        print("Sleeping for 60 secs")
        time.sleep(60)
