from machine import Pin
import time

class TM1637:
    def __init__(self, clk, dio):
        self.clk = clk
        self.dio = dio
        self.clk.init(Pin.OUT)
        self.dio.init(Pin.OUT)
        self.brightness = 7
        self.colon = False

        self._SEGMENTS = [
            0x3f, 0x06, 0x5b, 0x4f,
            0x66, 0x6d, 0x7d, 0x07,
            0x7f, 0x6f,
            0x40, 0x00
        ]

    def _start(self):
        self.dio.value(1)
        self.clk.value(1)
        self.dio.value(0)
        self.clk.value(0)

    def _stop(self):
        self.clk.value(0)
        self.dio.value(0)
        self.clk.value(1)
        self.dio.value(1)

    def _write_byte(self, b):
        for i in range(8):
            self.dio.value((b >> i) & 1)
            self.clk.value(1)
            time.sleep_us(5)
            self.clk.value(0)
        self.clk.value(1)
        self.clk.value(0)

    def show_colon(self, state=True):
        self.colon = state

    def show(self, data):
        segments = []

        for i, char in enumerate(data[:4]):
            if char == "-":
                seg = 0x40
            elif char == "_":
                seg = 0x40
            elif char == " ":
                seg = 0x00
            elif char.isdigit():
                seg = self._SEGMENTS[int(char)]
            else:
                seg = 0x00

            if i == 1 and self.colon:
                seg |= 0x80  # double dot

            segments.append(seg)

        while len(segments) < 4:
            segments.append(0x00)

        self._start()
        self._write_byte(0x40)
        self._stop()

        self._start()
        self._write_byte(0xC0)
        for seg in segments:
            self._write_byte(seg)
        self._stop()

        self._start()
        self._write_byte(0x88 | self.brightness)
        self._stop()

