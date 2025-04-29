from machine import PWM
from time import sleep
from machine import Pin

buzzer = PWM(Pin(15))

def beep(times=3, freq=2000, delay=0.3):
    for _ in range(times):
        buzzer.freq(freq)
        buzzer.duty_u16(32768)
        sleep(delay)
        buzzer.duty_u16(0)
        sleep(delay)
