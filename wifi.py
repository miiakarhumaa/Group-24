import network
import time

ssid = "YOUR_WIFI_SSID"
password = "YOUR_WIFI_PASSWORD"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print("Waiting for connection...")
    time.sleep(1)

if wlan.isconnected():
    print("Connected!")
    print("IP Address:", wlan.ifconfig()[0])
else:
    print("Connection failed. Status:", wlan.status())