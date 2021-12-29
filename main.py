from websrv import HttpServ

try:
  server = HttpServ()
except OSError:
  import machine
  machine.reset()
  pass

server.run_socket()

