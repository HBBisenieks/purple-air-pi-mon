# purple-air-pi-mon
A color-based at-a-glance station to show local air quality with a raspi pico w and some rgb leds

## Getting Started
Copy `example.config.py` to `config.py` and fill in the values for your API key, SSID, password, and nearby sensors. Sensors should be entered as tuples, with the first value of each being a string of the ID of a nearby sensor, and the second being an int for the weight of that sensor. Higher numbers should be used for closer sensors because of how the math gets done.

Once that info is filled in, use `ampy` to load `config.py` and `main.py` onto your board, reboot, and you're good.