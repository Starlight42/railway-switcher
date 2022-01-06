"""
Augustin Bernachon 28/12/2021
Railway Switcher Main
"""

from websrv import HttpServ
from config import BTN_LEFT

def btn_action(btn):
  config.BTN_LEFT = True

flag = True
btn_left = Pin(15, Pin.IN)
btn_top = Pin(14, Pin.IN)
btn_right = Pin(13, Pin.IN)
btn_bott = Pin(12, Pin.IN)

#btn_left.irq(trigger=Pin.IRQ_RISING, handler=btn_action)
btn_right.irq(trigger=Pin.IRQ_RISING, handler=btn_action)
#btn_bott.irq(trigger=Pin.IRQ_RISING, handler=btn_action)
#btn_top.irq(trigger=Pin.IRQ_RISING, handler=btn_action)

try:
  server = HttpServ(lcd)
except OSError:
  import machine
  machine.reset()
  pass

server.run_socket()

