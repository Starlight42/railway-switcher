"""
Augustin Bernachon 28/12/2021
Railway Switcher Main
"""

from websrv import HttpServ

try:
  server = HttpServ(lcd)
except OSError:
  import machine
  machine.reset()
  pass

server.run_socket()

