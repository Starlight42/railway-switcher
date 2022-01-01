"""
Augustin Bernachon 28/12/2021
Railway Switcher basic Python code style config file.
"""

# Railway Switcher configuration File
wifi_config = {
  'ssid': 'YOURSSID',
  'password': 'YOURPWD'
}

servos = (
  {'servo_pin': 4,
  'servo_name': 'servo01',
  'servo_req_filter': 'GET /?switcher01'},
  {'servo_pin': 5,
  'servo_name': 'servo02',
  'servo_req_filter': 'GET /?switcher02'}
)

MEM_TSIZE = 38000
GC_THRESH = 10000
BIND_PORT = 80
BIND_IP = '0.0.0.0'
SERVO_FREQ = 50
DUTY_HIGH = 115
DUTY_LOW = 30
SCL_PIN = 0
SDA_PIN = 2
LCD_NUM_ROWS = 2
LCD_NUM_COLS = 16
DEFAULT_I2C_ADDR = 0x27

