import socket
import layout
import config

def format_answer():
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((config.BIND_IP, config.BIND_PORT))
s.listen(5)

while True:
    new_duty = 30
    print('In Da while')

    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(512)
        conn.settimeout(None)
        request = str(request)
        # print('GET Rquest Content = %s' % request)
        sw01 = request.find('/?switcher01')
        sw02 = request.find('/?switcher02')
        sw01_duty = servo01.duty()
        sw02_duty = servo02.duty()
        if sw01 == 6:
          if sw01_duty == 30:
            new_duty = 115
          print('Triggered railway switch 01 from '+str(sw01_duty)+' to '+str(new_duty))
          servo01.duty(new_duty)
        if sw02 == 6:
          if sw02_duty == 30:
            new_duty = 115
          print('Triggered railway switch 02 from '+str(sw02_duty)+' to '+str(new_duty))
          servo02.duty(new_duty)
        response = layout.html_template
        format_answer()
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')



