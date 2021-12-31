"""
Augustin Bernachon 28/12/2021
Railway Switcher Servo api
"""

from machine import PWM, Pin
import gc

class servoApi(object):
  def __init__(self, servo_pin, servo_freq, servo_duty=30):
    gc.collect()
    self.pin = servo_pin
    self.freq = servo_freq
    self.duty = servo_duty
    self.servo = PWM(Pin(self.pin), freq=self.freq, duty=self.duty)

  def get_duty(self):
    return self.duty

  def set_duty(self, new_duty):
    self.duty = new_duty
    self.servo.duty(self.duty)

