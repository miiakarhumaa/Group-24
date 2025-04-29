from machine import ADC, Pin
import math

adc = ADC(Pin(26))

def read_ntc_temp():
    analog_value = adc.read_u16()
    voltage = analog_value / 65535 * 3.3
    resistance = (3.3 * 10000 / voltage) - 10000

    # Steinhart-equation
    B = 3892 #beta value
    T = 298.15  # 25°C in kelvins
    R = 10000   # 10k resistor

    temp_k = 1 / (1/T + (1/B) * math.log(resistance/R))
    temp_c = temp_k - 273.15
    return temp_c
