"""
Augustin Bernachon 28/12/2021
Railway Switcher basic Webserver
"""
from time import sleep
from machine import reset
from servoapi import servoApi
import config
import select
import socket
import layout


class HttpServ(object):
  def __init__(self, lcd):
    print("Hello Webserver!")
    self.request = b''
    self.lcd = lcd
    self.socket = None
    self.poller = None
    self.conn = None
    self.cli_addr = None
    self.servos = {'GET /?switcher01': servoApi(config.SERVO01, 50),
                   'GET /?switcher02': servoApi(config.SERVO02, 50)}

  def _send_response(self):
    try:
      self._format_answer()
      self.conn.sendall(layout.html_template)
      sleep(0.2)
    except Exception as exc:
      # print("Send Response Err", exc.args[0])
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
    action_dict = {
    'GET /?switcher01': self._move_servo,
    'GET /?switcher02': self._move_servo
    }

    for action in action_dict:
      if str(self.request).find(action) > -1:
        print('Matched an action ! {}'.format(action))
        action_dict[action](action)

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

  def run_socket(self):
    if not self.socket:
      self._create_socket()
    self.poller = select.poll()
    self.poller.register(self.socket, select.POLLIN)

    while True:
      res = self.poller.poll(1)
      if res:
        print('In poller poll')
        self.conn, self.cli_addr = self.socket.accept()
        self.lcd.clear()
        self.lcd.putstr('cli {}'.format(str(self.cli_addr[0])))
        self.request = str(self.conn.recv(512))
        self.conn.settimeout(None)
        print('GET Request Content = {}'.format(self.request))
        self._parse_request()
        # Returning home page
        self._send_response()

    gc.collect()

