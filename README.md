# Railway Switcher
The main goal of this project is to turn old analog model railroading switchers to digital world.
This repot contains basic code that runs on a nodemcu esp8266 flashed with Micropython.
It is more like a reminder for me but if it seems usefull for someone do not hesitate to use it!
It consists on a webpage that exposes a couple of buttons. Thoses inputs control a bunch of servomotor connected to the old manual railway switchers.

You need to flash MicroPython on your board first. (TODO : add full working step by step for my specific board)

### File explanation
> from me
boot.py				-> executed when the nodemcu starts (or reset). In this file we set basic wifi client connection. You need to set your wifi SSID and PWD in the config file.
config.py			-> contains several usefull variables.
layout.py			-> contains the webpage html source.
main.py				-> containes the "core" app code. 
> from https://github.com/dhylands/python_lcd
esp8266_i2c_lcd.py	-> library that facilitate i2c lcd handling.
lcd_api.py			-> generic Micropython api to control lcd screens.
