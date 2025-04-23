import rp2
import network
import ubinascii
import machine
import time
import socket
import math
import errno

from secrets import secrets
from dht import DHT22
from ntc import read_ntc_temp
from tm1637 import TM1637
from buzzer import beep

rp2.country('FI')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ssid = secrets['ssid']
pw = secrets['pw']

led_pin = machine.Pin('LED', machine.Pin.OUT)
led_pin.value(0)

dht_sensor = DHT22(pin=16)
display = TM1637(clk=machine.Pin(2), dio=machine.Pin(3))
buzzer_pin = machine.Pin(15)

current_dht_temp = 0.0
current_dht_hum = 0.0
current_ntc_temp = 0.0
cool_status_message = ""
last_update_ms = time.ticks_ms()
update_interval_ms = 1000
last_beep_ms = 0

wlan.connect(ssid, pw)

timeout = 10
while timeout > 0:
    wlan_status = wlan.status()
    if wlan_status < 0 or wlan_status >= 3:
        break
    timeout -= 1
    time.sleep(1)

wlan_status = wlan.status()

if wlan_status != 3:
    if wlan_status == -3: print("Error: Bad authentication")
    elif wlan_status == -2: print("Error: No network found")
    elif wlan_status == -1: print("Error: Link failure")
    elif wlan_status == 2: print("Error: Connected but no IP address")
    led_pin.value(0)
    raise RuntimeError('Wi-Fi connection failed')
else:
    led_pin.value(1)
    status = wlan.ifconfig()
    ip_address = status[0]
    print(f"Web server: http://{ip_address}/")

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
s.setblocking(False)

def get_html(html_name):
    try:
        with open(html_name, 'r') as file:
            html = file.read()
        return html
    except OSError:
        return None

try:
    while True:
        cl = None
        try:
            cl, web_addr = s.accept()
            cl.settimeout(5.0)
            request_bytes = cl.recv(1024)
            request_str = request_bytes.decode('utf-8')

            request_line = request_str.split('\r\n')[0]
            parts = request_line.split()
            path = "/"
            if len(parts) > 1:
                path = parts[1]

            response_body = None
            status_code = "200 OK"
            content_type = "text/html"

            if path == "/favicon.ico":
                status_code = "404 Not Found"
                response_body = "Not Found"
                content_type = "text/plain"
            elif path == "/":
                html_template = get_html('index.html')
                if html_template:
                     response_body = html_template.replace('{dht_temp}', "{:.2f}".format(current_dht_temp))
                     response_body = response_body.replace('{dht_humidity}', "{:.2f}".format(current_dht_hum))
                     response_body = response_body.replace('{ntc_temp}', "{:.2f}".format(current_ntc_temp))
                     response_body = response_body.replace('{cool_message}', cool_status_message)
                else:
                     print("!!! ERROR: index.html not found!")
                     status_code = "500 Internal Server Error"
                     response_body = "Server error: index.html missing."
                     content_type = "text/plain"
            else:
                status_code = "404 Not Found"
                response_body = "Not Found"
                content_type = "text/plain"

            headers = f'HTTP/1.0 {status_code}\r\nContent-type: {content_type}\r\n\r\n'
            cl.send(headers.encode('utf-8'))

            if response_body:
                 encoded_response = response_body.encode('utf-8')
                 cl.send(encoded_response)

            cl.close()
            cl = None

        except OSError as e:
            if e.args[0] == errno.ETIMEDOUT:
                print("!!! Client request timed out.")
            elif e.args[0] != errno.EAGAIN:
                 print(f"!!! Socket accept/processing error: {e}")
            if cl and e.args[0] != errno.EAGAIN:
                cl.close()
                cl = None
        except Exception as e:
             print(f"!!! Unexpected error during request handling: {e}")
             if cl:
                 try:
                     cl.close()
                     cl = None
                 except Exception as close_err:
                     print(f"!!! Error closing socket after exception: {close_err}")

        current_time_ms = time.ticks_ms()
        if time.ticks_diff(current_time_ms, last_update_ms) >= update_interval_ms:
            last_update_ms = current_time_ms
            try:
                dht_sensor.measure()
                current_dht_temp = dht_sensor.temperature()
                current_dht_hum = dht_sensor.humidity()
                current_ntc_temp = read_ntc_temp()
                print(f"DHT: {current_dht_temp:.1f}°C, {current_dht_hum:.1f}% | NTC: {current_ntc_temp:.1f}°C")

                if current_ntc_temp <= 5:
                    display.show_colon(False)
                    display.show("C00L")
                    cool_status_message = "Drink is ready to be enjoyed!"
                    if time.ticks_diff(current_time_ms, last_beep_ms) >= 5000:
                        beep()
                        last_beep_ms = current_time_ms

                else:
                    cool_status_message = ""
                    dht_temp_int = int(round(current_dht_temp))
                    ntc_temp_int = int(round(current_ntc_temp))
                    if ntc_temp_int < -9: ntc_temp_int = -9
                    if ntc_temp_int > 99: ntc_temp_int = 99
                    dht_str = "{:02d}".format(dht_temp_int)
                    ntc_str = "{:02d}".format(ntc_temp_int)
                    display.show_colon(True)
                    display.show(dht_str + ntc_str)

            except Exception as e:
                print(f"Sensor/Display Update ERROR: {e}")
                try:
                    display.show("Err ")
                except:
                    pass

        time.sleep_ms(100)

except KeyboardInterrupt:
    print("KeyboardInterrupt, stopping server.")
finally:
    if 's' in locals() and s:
        s.close()
    led_pin.value(0)
    print("Exiting.")
