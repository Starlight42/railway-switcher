"""
Augustin Bernachon 28/12/2021
Railway Switcher basic Webserver
"""
from time import sleep
from machine import reset
import config
import select
import socket
import layout


class HttpServ(object):
  def __init__(self):
    print("Hello Webserver!")
    self.request = b''
    self.socket = None
    self.poller = None
    self.conn = None
    self.cli_addr = None
    self.req = None

  def connection(self, response=None):
    fp = open("index.html", "r")
    while True:
      # chunk = fp.read(450)
      chunk = fp.read(1024) # <-- Test 1024 Chunk Size
      try:
        if not chunk: break
        self.conn.sendall(chunk)
      except Exception as exc:
        # print("Send Data Err", exc.args[0])
        pass
  
    self.conn.close()
    fp.close()

  def send_response(self, content):
    try:
      self.conn.sendall(content)
      sleep(0.2)
    except Exception as exc:
      # print("Send Response Err", exc.args[0])
      pass
    finally:
      self.conn.close()

  def parse_request(self):
    action_list = ['/writeSounds']

    for action in action_list:
      if str(self.request).find(action) > -1:
        if action == '/MAROUTE':
          print('Return write.')
          #self.send_response()

    self.request = b''

  def parse_json(self, request):
    if search("\\s(\".*)[:]\\s(.*\")", request):
      json_string = request.decode().split('\r\n')[-1:]
      for data in json_string:
        json_Data = loads(data)
        return json_Data
    else:
      print("Data Not Found!")
      return 0

  def format_answer(self):
    self.conn.send('HTTP/1.1 200 OK\n')
    self.conn.send('Content-Type: text/html\n')
    self.conn.send('Connection: close\n\n')

  def run_socket(self):
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

    self.poller = select.poll()
    self.poller.register(self.socket, select.POLLIN)
    while True:
      res = self.poller.poll(1)
      if res:
        print('In poller poll')
        self.conn, self.cli_addr = self.socket.accept()
        lcd.clear()
        lcd.putstr('cli {}'.format(str(self.cli_addr[0])))
        self.req = self.conn.recv(512)
        self.conn.settimeout(None)
        print('GET Request Content = {}'.format(str(self.req)))
        sw01 = self.req.find('/?switcher01')
        sw02 = self.req.find('/?switcher02')
        sw01_duty = servo01.duty()
        sw02_duty = servo02.duty()
        if sw01 == 6:
          if sw01_duty == config.DUTY_LOW:
            new_duty = config.DUTY_HIGH
            print('Triggered railway switch 01 from '+str(sw01_duty)+' to '+str(new_duty))
            servo01.duty(new_duty)
        if sw02 == 6:
          if sw02_duty == config.DUTY_LOW:
            new_duty = config.DUTY_HIGH
            print('Triggered railway switch 02 from '+str(sw02_duty)+' to '+str(new_duty))
            servo02.duty(new_duty)

        self.format_answer()
        self.conn.sendall(layout.html_template)
        self.conn.close()

