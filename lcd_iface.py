"""
Augustin Bernachon 28/12/2021
Railway Switcher LCD Interface
Simple class that allow reusing I2CLcd previously created instance
if exists and hide I2C pin creation if lcd need to be instanciated.
"""

from machine import I2C, Pin
from esp8266_i2c_lcd import I2cLcd
import gc
import config

class lcdIface(object):
  def __init__(self, lcd=None, i2c_addr=config.DEFAULT_I2C_ADDR,
               scl_pin=config.SCL_PIN, sda_pin=config.SDA_PIN,
               lcd_rows=config.LCD_NUM_ROWS, lcd_col=config.LCD_NUM_COLS):
    gc.collect()
    self.scl_pin = scl_pin
    self.sda_pin = sda_pin
    self.i2c_addr = i2c_addr
    self.lcd_rows = lcd_rows
    self.lcd_col = lcd_col
    self.lcd = lcd if isinstance(lcd, I2cLcd) else self._get_lcd_ptr()
    self.i2c = None

  def _get_i2c_ptr(self):
    try:
      self.i2c = I2C(scl=Pin(self.scl_pin), sda=Pin(self.sda_pin), freq=500000)
    except:
      print('Can not get I2C Pin, reseting..')

  def _get_lcd_ptr(self):
    try:
      print('Creating lcd pointeur')
      self._get_i2c_ptr()
      return I2cLcd(self.i2c, self.i2c_addr, self.lcd_rows, self.lcd_col)
    except:
      print('Can not get LCD, reseting..')

  def get_lcd(self):
    return self.lcd

