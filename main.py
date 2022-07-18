"""
Purple Air local AQI status monitor box

by Hilary B. Brenum
"""

import network
import time
import machine
import neopixel
import config
import _thread
import urequests as requests

"""
Constants
"""
BASE_URL = "https://api.purpleair.com/v1/sensors/"
API_KEY = config.API_KEY
SSID = config.SSID
WPA3 = config.WPA3
sensors = config.sensors
pixels = 4

SENSOR_WEIGHT = 0
for sensor in sensors:
    SENSOR_WEIGHT = SENSOR_WEIGHT + sensor[1]

"""
Physical components
"""
led = machine.Pin("LED", machine.Pin.OUT)
display_button = machine.Pin(27, machine.Pin.IN) # pushbutton switch on GP27
color_display = neopixel.NeoPixel(machine.Pin(28), pixels) # neopixel (WS2812) strip on GP28

"""
Colors
"""
CURRENT_COLOR = (0, 0, 0)
GREEN = (0, 255, 0)
MID_GREEN = (153, 255, 51)
YELLOW = (255, 255, 0)
MID_YELLOW = (255, 153, 50)
ORANGE = (255, 128, 0)
MID_ORANGE = (255, 105, 50)
RED = (255, 0, 0)
MAROON = (156, 30, 102)
HELLA_MAROON = (153, 51, 255)
OFF = (0, 0, 0)


def get_aqi(sensor_id):
    """
    make an API request against sensor_id and return the PM2.5 numbers
    """
    headers = {
        "X-API-Key" : API_KEY,
        }

    request_url = f"{BASE_URL}{sensor_id}?fields=pm2.5_10minute"

    try:
        data = requests.get(request_url, headers=headers)
        # process data
        data.close()
    except:
        data.close()
        return None


def calculate_aqi(current_aqi):
    """
    Run average for AQI numbers and update as long as all readings can be
    collected; otherwise, keep most-recent complete reading

    This could be made more fault-tolerant and probably should be, but that's
    a problem for future-Hilary to solve (the solution is just to calculate the
    sensor number/weight at runtime every time, but I already wrote it this way)
    """
    new_aqi = 0
    new_reading = True

    for sensor in sensors:
        aqi = get_aqi(sensor[0])
        if aqi:
            new_aqi = new_aqi + (aqi * sensor[1])
        else:
            new_reading = False
            break

    if new_reading:
        new_aqi = new_aqi / SENSOR_WEIGHT
    else:
        new_aqi = current_aqi

    return new_aqi


def set_color(aqi):
    """
    sets color value for LED strip based on AQI input 
    """
    global CURRENT_COLOR
    CURRENT_COLOR = YELLOW


def update_aqi():
    """
    Get the current AQI, set the color for the RGB display, and then wait 10
    minutes and do it again
    """
    current_aqi = 50 # Set AQI to moderate before data is collected
    while True:
        set_color(calculate_aqi(current_aqi))
        time.sleep(600)


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
    wlan.connect(SSID, WPA3)

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


def display_aqi():
    color_display.write()
    time.sleep(30)
    


def main():
    initialize_net() # Initialize network connection

    _thread.start_new_thread(update_aqi, ()) # Start the AQI collection

    while True: # Start main loop waiting for button press




if __name__ == "__main__":
    main()