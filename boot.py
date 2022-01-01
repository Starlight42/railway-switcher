"""
Augustin Bernachon 28/12/2021
Railway Switcher Boot
"""

# This file is executed on every boot (including wake-boot from deepsleep)
import machine
from time import sleep_ms, ticks_ms
from machine import I2C, Pin
from esp8266_i2c_lcd import I2cLcd
import gc
import network
import ntptime
import utime
import config

print('First boot line : GC Mem Free : {}\nGC Mem allocated : {}'.format(gc.mem_free(), gc.mem_alloc()))
print('Current GC threshold : {}\nSettings threshold to 25000 since total mem size is {}'.format(gc.threshold(), config.MEM_TSIZE))
gc.threshold(config.GC_THRESH)
print('New GC threshold : {}'.format(gc.threshold()))

def do_connect():
  sta_if = network.WLAN(network.STA_IF)
  start = utime.time()
  timed_out = False
  
  if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(config.wifi_config['ssid'], config.wifi_config['password'])
    while not sta_if.isconnected() and not timed_out:
      if utime.time() - start >= 20:
        timed_out = True
      else:
        pass

  if sta_if.isconnected():
    ntptime.settime()
    print('network config:', sta_if.ifconfig())
  else: 
    print('internet not available')

  return timed_out

try:
  timed_out = do_connect()
  if timed_out:
    utime.sleep_ms(10000)
    machine.reset()
  gc.collect()
except KeyboardInterrupt:
  raise

except:
  utime.sleep_ms(10000)
  machine.reset()


i2c = I2C(scl=Pin(config.SCL_PIN), sda=Pin(config.SDA_PIN), freq=500000)
lcd = I2cLcd(i2c, config.DEFAULT_I2C_ADDR, config.LCD_NUM_ROWS, config.LCD_NUM_COLS)
lcd.putstr("AIP: {}\nSIP: {}".format(network.WLAN(network.AP_IF).ifconfig()[0],network.WLAN(network.STA_IF).ifconfig()[0]))
gc.collect()

