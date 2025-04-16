from tm1637 import TM1637
from machine import Pin, ADC, PWM
from time import sleep
import dht
import math
from ntc import read_ntc_temp
from buzzer import beep

display = TM1637(clk=Pin(2), dio=Pin(3))
sensor = dht.DHT22(Pin(16))
adc = ADC(Pin(26))
buzzer = PWM(Pin(15))
cool_shown = False


while True:
    try:
        sensor.measure()
        dht_temp = int(round(sensor.temperature()))
        ntc_temp = int(round(read_ntc_temp()))

        if ntc_temp < -9:
            ntc_temp = -9
        if ntc_temp > 99:
            ntc_temp = 99

        print("DHT:", dht_temp, "°C | NTC:", ntc_temp, "°C")

        dht_str = "{:02d}".format(dht_temp)
        ntc_str = "{:02d}".format(ntc_temp)

        display.show_colon(True)
        display.show(dht_str + ntc_str)
        
        if ntc_temp <= 6 and not cool_shown:
            display.show_colon(False)
            print("Drink is ready to be enjoyed!")
            display.show("C00L")
            beep()
            sleep(0.75)
            beep()
            sleep(0.75)
            beep()
            sleep(10)
            cool_shown = True
            display.show_colon(True)
            
            
        if ntc_temp > 6:
            cool_shown = False

            
    except Exception as e:
        print("ERROR:", e)
        display.show("----")

    sleep(1)
