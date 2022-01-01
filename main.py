"""
Augustin Bernachon 28/12/2021
Railway Switcher Main
"""

from websrv import HttpServ
from lcd_iface import lcdIface

try:
  server = HttpServ(lcd)
except OSError:
  import machine
  machine.reset()
  pass

server.run_socket()

