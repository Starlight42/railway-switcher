"""
Augustin Bernachon 28/12/2021
Railway Switcher basic Webserver
"""

from time import sleep
from machine import reset, PWM, Pin
from servo_iface import servoIface
from lcd_iface import lcdIface
import config
import select
import socket
import layout


class HttpServ(object):
  def __init__(self, lcd=None, servos=None):
    print("Started Http web SRV.")
    self.request = b''
    self.socket = None
    self.poller = None
    self.conn = None
    self.cli_addr = None
    self.lcd = lcdIface(lcd).get_lcd()
    self.servos = self._get_servo_list(servos)
    self.action_dict = {servo: self._move_servo for servo in self.servos}
    print('action dict is : {}'.format(self.action_dict))

  def _get_servo_list(self, servos):
    servo_dict = dict()

    if not servos:
      for servo in config.servos:
        servo_dict[servo['servo_req_filter']] = servoIface(servo['servo_pin'], servo['servo_req_filter'], servo['servo_name'])
    else:
      for servo in servos:
        if isinstance(servo, PWM):
          iservo = servoIface(servo=servo)
          servo_dict[iservo.get_req_filter()] = iservo

    return servo_dict

  def _send_response(self):
    try:
      self._format_answer()
      self.conn.sendall(layout.html_template)
    except Exception as exc:
      print("Send Response Err", exc.args[0])
      pass
    finally:
      self.conn.close()

  def _move_servo(self, switch_n):
    old_duty = self.servos[switch_n].get_duty()

    if old_duty == config.DUTY_LOW:
      new_duty = config.DUTY_HIGH
    else:
      new_duty = config.DUTY_LOW

    print('Triggered railway switch {} from {} to {}'.format(switch_n, str(old_duty), str(new_duty)))
    self.servos[switch_n].set_duty(new_duty)

  def _parse_request(self):
    for action in self.action_dict:
      if str(self.request).find(action) > -1:
        self.action_dict[action](action)

    # Reseting request buffer
    self.request = b''

  def _format_answer(self):
    self.conn.send('HTTP/1.1 200 OK\n')
    self.conn.send('Content-Type: text/html\n')
    self.conn.send('Connection: close\n\n')

  def _create_socket(self):
    try:
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.socket.bind((config.BIND_IP, config.BIND_PORT))
      self.socket.listen(5)
    except Exception as exc:
      print("Address in use, restarting", exc.args[0])
      sleep(2)
      reset()
      pass

  def toggle_lcd_backlight(self):
    if self.lcd.backlight:
      self.lcd.backlight_off()
      config.LCD_LIGHT = False
    else:
      self.lcd.backlight_on()
      config.LCD_LIGHT = True

  def run_socket(self):
    if not self.socket:
      self._create_socket()
    self.poller = select.poll()
    self.poller.register(self.socket, select.POLLIN)

    while True:
      res = self.poller.poll(1)
      if res:
        self.conn, self.cli_addr = self.socket.accept()
        self.lcd.clear()
        self.lcd.putstr('cli {}'.format(str(self.cli_addr[0])))
        self.request = str(self.conn.recv(512))
        self.conn.settimeout(None)
        self._parse_request()
        # Returning home page
        self._send_response()

      if config.BTN_LEFT:
        self.toggle_lcd_backlight()
        config.BTN_LEFT = False

    gc.collect()

