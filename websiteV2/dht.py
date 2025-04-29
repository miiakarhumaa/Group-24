from machine import Pin
import dht

class DHT22:
    def __init__(self, pin):
        self.sensor = dht.DHT22(Pin(pin))

    def read_temperature(self):
        self.sensor.measure()
        return self.sensor.temperature()

    def read_humidity(self):
        self.sensor.measure()
        return self.sensor.humidity()
