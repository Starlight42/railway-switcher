"""
Augustin Bernachon 28/12/2021
Railway Switcher Servo Interface
Simple class that allow reusing PWM servo previously created instance
if exists and hide PWM creation if it needs to be instanciated.
"""

from machine import PWM, Pin
import gc
import config


class servoIface(object):
  def __init__(self, servo_pin=None, servo_filter=None, servo_name=None,
               servo_freq=config.SERVO_FREQ, servo_duty=30, servo=None):
    gc.collect()
    self.freq = servo_freq

    if isinstance(servo, PWM):
      print('Servo is an instance of PWM')
      self.servo = servo
      self.pin = int(str(servo)[4])

      for svo in config.servos:
        if svo['servo_pin'] == self.pin:
          self.req_filter = svo['servo_req_filter']
          self.name = svo['servo_name']
          self.duty = int(servo.duty())
    else:
      print('Servo is not an instance of PWM creating Servo')
      self.pin = servo_pin
      self.req_filter = servo_filter
      self.name = servo_name
      self.duty = servo_duty
      self.servo = self._get_servo_ptr()

  def _get_servo_ptr(self):
    pwm = None

    try:
      pwm = PWM(Pin(self.pin), freq=self.freq, duty=self.duty)
    except:
      print('Can not get PWM output, reseting..')

    return pwm

  def get_duty(self):
    return self.duty

  def set_duty(self, new_duty):
    self.duty = new_duty
    self.servo.duty(self.duty)

  def get_req_filter(self):
    return self.req_filter

  def get_name(self):
    return self.name

