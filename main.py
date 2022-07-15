"""
Purple Air local AQI status monitor box

by Hilary B. Brenum
"""

import network
import time
import machine
import config
import urequests as requests

"""
Constants (get the secrets moved into a .gitignore-able jawn)
"""

BASE_URL = "https://api.purpleair.com/v1/sensors/"

led = machine.Pin("LED", machine.Pin.OUT)

"""
Since there's not a sensor right by my place, sensors are entered as tuples
where the first value is the sensor id and the second value is the weight of
the sensor data, where higher numbers mean a closer sensor with more weight
"""
sensors = [("106120", 4), ("119485", 2), ("46331", 1), ("67261", 1)]

def get_aqi(sensor_id):
    """
    make an API request against sensor_id and return the PM2.5 numbers
    """
    headers = {
        "X-API-Key" : config.API_KEY,
        }

    request_url = f"{BASE_URL}{sensor_id}?fields=pm2.5_10minute"

    try:
        data = requests.get(request_url, headers=headers)
        # process data
        data.close()
    except:
        data.close()
        return None



def set_color(aqi):
    """
    sets color value for LED strip based on AQI input 
    """
    return None


def initialize_net():
    """
    Initializes network connection
    """
    led.off()
    led.toggle()
    time.sleep(3)
    led.toggle()

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config.SSID, config.WPA3)

    max_wait = 10
    for i in range(max_wait):
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        time.sleep(1)

    if wlan.status() != 3:
        for i in range(3):
            led.on()
            time.sleep(.5)
            led.off()
            time.sleep(.5)
        raise RuntimeError('network connection failed')
    else:
        led.on()
        time.sleep(3)
        led.off()


def main():
    initialize_net()


if __name__ == "__main__":
    main()