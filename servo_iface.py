"""
Augustin Bernachon 28/12/2021
Railway Switcher Servo Interface
"""

from machine import PWM, Pin
import gc
import config


class servoIface(object):
  def __init__(self, servo_pin, servo_filter, servo_name,
               servo_freq=config.SERVO_FREQ, servo_duty=30, servo=None):
    gc.collect()
    self.pin = servo_pin
    self.req_filter = servo_filter
    self.name = servo_name
    self.freq = servo_freq
    self.duty = servo_duty
    self.servo = self._check_servo_type() servo if servo isinstance(servo, PWM) else self._get_servo_ptr()

  def _get_servo_ptr(self):
    try:
      print('Creating PWM output')
      return machine.PWM(machine.Pin(self.pin), freq=self.freq, duty=self.duty)
    except:
      print('Can not get PWM output, reseting..')

  def get_duty(self):
    return self.duty

  def set_duty(self, new_duty):
    self.duty = new_duty
    self.servo.duty(self.duty)

  def get_req_filter(self):
    return self.req_filter

  def get_name(self):
    return self.name

