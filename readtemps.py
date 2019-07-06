import config

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

    temps = {}
    for rom in roms:
        r = rom_id(rom)
        temp = ds.read_temp(rom)
        print("Sensor %s, Read temperature %f" % (r, temp))
        temps[r] = int(temp * 1000)

    return temps
