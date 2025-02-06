try:
  import usocket as socket
except:
  import socket

import network
import time
#import gc

def tcp_ping(host, port=80, timeout=2):
    """Ping a server via TCP for a specific port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except Exception:
        return False

#gc.collect()

wifi_ssid = "lo-def173"
wifi_password = "starhotspot"

ssid = 'MicroPython'
password = 'micro1234'

wlan = network.WLAN(network.STA_IF)  # Create a WLAN object in station mode
wlan.active(True) # Activate the interface
networks = wlan.scan()

print("Available WiFi Networks:")
for network_info in networks:
    print(network_info)

wlan.connect(wifi_ssid, wifi_password) 


while wlan.isconnected() == False:
    print("Not connected, re-trying...", wlan.isconnected())
    time.sleep(1)
    continue

networks = wlan.scan()

print("Connected to wifi:")
print(wlan.ifconfig()[0])
print("Is wifi connected?: ", wlan.isconnected())
if tcp_ping('google.com'):
    print("Server is reachable via TCP!")
else:
    print("Server is not reachable via TCP.")

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

while ap.active() == False:
  pass

print('Connection is successful')
print(ap.ifconfig()[0])
def web_page():
  html = """
  <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
      <h1>Welcome to microcontrollerslab!</h1>
    </body>
  </html>
  """
  return html
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
s.bind(('', 80))
s.listen(5)
while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Content = %s' % str(request))
  response = web_page()
  conn.send(response)
  conn.close()